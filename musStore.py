import tkinter
from tkinter import ttk
import sqlite3
from tkinter.messagebox import showerror

from core.bindings import bindings
import traceback

class musStore():
	def __init__(self):
		self.con = sqlite3.connect("musScore.db") # Should change this at some point!
		self.cur = self.con.cursor()
		self.bindings = bindings()
		
ms = musStore()
con = ms.con
cur = ms.cur

def report_callback_exception(self, exc, val, tb):
	showerror("Error", message=str(val))
	out=""
	for i in traceback.extract_stack():
		out += str(i)+"\n"
	displayText.insert(tkinter.END, out + "\n")
	displayText.insert(tkinter.END, val)
	#f = open("whoops", "r")
	#f.write("Oop")
	#f.close()
	
def buildName(a,b):
	for i in [" ", ",","!", "'"]:
		a = a.replace(i, "")
		b = b.replace(i,"")
		
	if (len(b.strip()) == 0):
		return a[:8].upper()
	return b[:8].upper()
	pass

#cur.execute("drop table music")
#cur.execute("create table music (id integer not null primary key autoincrement, sortkey text, title text, subtitle text)")
#cur.execute("create table music_folder (music_id integer unique, folder_id integer)")
#cur.execute("create table folder (id integer not null primary key autoincrement, sortkey text, title text)")
#cur.execute("create table tune (id integer not null primary key autoincrement, sortkey text, title text)")
#cur.execute("insert into tune (sortkey, title) values ('SLANE', 'SLANE')")

from widgets.tkInputBox import tkInputBox
from widgets.treeViewWithSearch import treeViewWithSearch
win = tkinter.Tk()

win.title("Music Store")
def add():
	d = tkInputBox(win, {
		"title" : {
			"name":"Title"
		},
		"subtitle" : {
			"name":"Subtitle"
		}
	})
	d.passFunc("add", f1.addSong)

s = ttk.Style()
import sys

if hasattr(sys, 'getandroidapilevel'):
	s.configure('Treeview', rowheight=48+8)
	err = tkinter.Tk()
	displayText = tkinter.Text(err, height=20, width=40)
	displayText.grid()
	tkinter.Tk.report_callback_exception = report_callback_exception

class folders(tkinter.Frame):

	def delete(self):
		if (len(self.tv.selected()) > 0):
			if (self.tv.selected()[0] == "Nf"):
				showerror("Deleting built-in folder", "This folder is a built-in folder and cannot be deleted.")
				return False
				
			sel = self.tv.selected()[0]
			de=self.tv.item(self.tv.selected()[0])["values"]
			te=self.tv.item(self.tv.selected()[0])["text"]
			
			#print(sel, te, de)
			
			if (sel.split("-")[0] != "f"):
				showerror("This is not a folder", "Only folders can be deleted here. Their contents cannot.")
				return False				
			
			d = cur.execute("select count(*) as c from music_folder a join folder b on a.folder_id = b.id where b.sortkey = ? and b.title = ?", (te, de[0]))
			ct = d.fetchone()[0]
			if (ct > 0):
				showerror("Folder is not empty", "This folder is not empty and cannot be deleted.")
				return False
				
			cur.execute("delete from folder where sortkey = ? and title=?", (te, de[0]))
			
			self.tv.delete(self.tv.selected())
			con.commit()
		else:
			showerror("Nothing to delete", "No items or no item selected to delete")
			
	def addFolder(self, data):
		a = data["title"]
		c = buildName(a,a)
		cur.execute("insert into folder (sortkey, title) values (?, ?)", (c,a))
		d = cur.lastrowid
		self.tv.add(["f-" + str(d), c, a])
		
	def updateSongToFolder(self, a):
	
		c = self.tv.selected()[0].split("-")[1]

		for b in a["folder"]:
			cur.execute("replace into music_folder (music_id, folder_id) values (?,?)", (c,b))
			if (not self.tv.exists("f-"+str(b))):
				self.tv.forcedisp("f-"+str(b))
			self.tv.move(self.tv.selected()[0], "f-"+str(b),0)
		con.commit()
		pass
		
	def updateSongDialog(self):
		x = {}
		if (len(self.tv.selected()) == 0):
			return False
		for i in cur.execute("select id, title from folder"):
			x[i[0]] = i[1]
			
		p = self.tv.selected()[0].split("-")
		if (p[0] != "s"):
			return False
		#showerror(p)
		
		d = tkInputBox(win, {
			"title" : {
				"name":"Song Name",
				"type": "label",
				"text": "Get Text"
			},
			"folder" : {
				"name":"Folder Name",
				"type": "treeview",
				"items": x,
				"selected": None
			},
		})
		d.passFunc("add", self.updateSongToFolder)
	
	def songsAddedNewSong(self, data):
		print("== NEW SONG ADDED == ")
		self.tv.add(["s-" + str(data['dbid']), data['sortkey'], data['title'], data['subtitle']], "Nf")
		print(data)

	def songsDeletedSong(self, data):
		print("== SONG REMOVED == ")
		self.tv.delete("s-" + str(data['dbid']))
		cur.execute("delete from music_folder where music_id = ?", (data['dbid'],))
		print(data)
		
	def addFolderDialog(self):
		d = tkInputBox(win, {
			"title" : {
				"name":"Folder Name"
			},
		})
		d.passFunc("add", self.addFolder)
		pass
	
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		self.core = self.nametowidget(".").core # Aha! That's how to do it!
		self.core.bindings.bind("music", "<create>", self.songsAddedNewSong)
		self.core.bindings.bind("music", "<delete>", self.songsDeletedSong)
		self.tv = treeViewWithSearch(self, 2)
		self.tv.grid(columnspan=3,rowspan=2,sticky="news")
		for i in cur.execute("select * from folder order by sortkey asc"):
			#print(("f-" + str(i[:1][0]),) + i[1:])
			#print(i)
			self.tv.add(("f-" + str(i[:1][0]),) + i[1:])
		self.tv.add(["Nf", "Not in Folder"])
		for i in cur.execute("select a.*, b.folder_id from music a left join music_folder b on a.id = b.music_id order by a.sortkey asc"):
			if (i[-1] is None):
				gp = "Nf"
			else:
				gp = "f-" + str(i[-1])
			self.tv.add(("s-" + str(i[:1][0]),) + i[1:-1], gp)

		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.sadd = tkinter.Button(self, text="Add...", command=self.addFolderDialog).grid(row = 2,column=2)
		self.supdate = tkinter.Button(self, text="Update...", command=self.updateSongDialog).grid(row = 2,column=1)
		
		self.sdel = tkinter.Button(self, text="Delete", command=self.delete).grid(row = 2,column=0)
		
class songs(tkinter.Frame):
	
	def addSong(self, data):
		a = data["title"]
		b = data["subtitle"]
		c = buildName(a,b)
		cur.execute("insert into music (sortkey, title,subtitle) values (?, ?,?)", (c,a,b))
		d = cur.lastrowid
		if (self.core.bindings.getBindings("music", "<create>")):
			for i in self.core.bindings.getBindings("music", "<create>"):
				i({ "title" : a, "subtitle": b, "sortkey": c, "dbid": d})

		self.tv.add([d, c, a, b])

	def tvSongSearch(self, a,b,c):
		n = self.tt.get()
		self.tv.delete(*self.tv.get_children())
		for i in cur.execute("select * from music where title like '%"+n+"%' order by sortkey asc"):
			self.tv.insert("", "end", i[0], values= [i[1],i[2],i[3]])

	def delete(self):
		if (len(self.tv.selected()) > 0):
			de=self.tv.item(self.tv.selected()[0])["values"]
			te=self.tv.item(self.tv.selected()[0])["text"]
			#print(de, te)
			#lbl.config(text= de)
			cur.execute("delete from music where sortkey = ? and title=?", (te, de[0]))
			
			s = self.tv.selected()

			if (self.core.bindings.getBindings("music", "<delete>")):
				for i in self.core.bindings.getBindings("music", "<delete>"):
					i({ "sortkey" : de[0], "title": te, "dbid": s[0]})

			self.tv.delete(self.tv.selected())
			con.commit()
		else:
			showerror("Nothing to delete", "No items or no item selected to delete")
			
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		self.core = self.nametowidget(".").core # Aha! That's how to do it!

		self.tt = tkinter.StringVar()
		self.tv = treeViewWithSearch(self, 2)
		self.tv.grid(columnspan=3,sticky='news')

		for i in cur.execute("select * from music order by sortkey asc"):
			self.tv.add(i)

		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		
		self.sadd = tkinter.Button(self, text="Add...", command=add)
		self.sadd.grid(row = 2,column=1)
		self.srem = tkinter.Button(self, text="Delete", command=self.delete)
		self.srem.grid(row = 2, column=0)
		pass

setattr(win, "core", ms)
notebook = ttk.Notebook(win, style='lefttab.TNotebook')

f1 = songs(notebook, bg='red')
fo = folders(notebook, bg='green')
f2 = tkinter.Frame(notebook, bg='blue', width=200, height=200)

#mu = ttk.Treeview(f2,columns=[1,2,3],show="headings")
#for i in cur.execute("select * from tune order by sortkey asc"):
#	mu.insert("", "end", i[0], values= [i[1],i[2]])
#mu.grid(columnspan=2, sticky="news")

notebook.add(f1, text='Songs')

#notebook.add(f2, text='Tunes')
notebook.add(fo, text='Folders')
notebook.grid(sticky="news")
#lbl = tkinter.Label(f1, text="")
#lbl.grid(row=3,columnspan=3)

win.rowconfigure(0, weight=1)
win.columnconfigure(0, weight=1)
win.mainloop()
con.commit()
