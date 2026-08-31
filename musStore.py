import tkinter
from tkinter import ttk
import sqlite3
from tkinter.messagebox import showerror

class musStore():
	def __init__(self):
		self.con = sqlite3.connect("musScore.db")
		self.cur = self.con.cursor()

ms = musStore()
con = ms.con
cur = ms.cur

def report_callback_exception(self, exc, val, tb):
	showerror("Error", message=str(val) + str(val))
	#f = open("whoops", "r")
	#f.write("Oop")
	#f.close()
	
tkinter.Tk.report_callback_exception = report_callback_exception

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
#cur.execute("create table folder (id integer not null primary key autoincrement, sortkey text, title text)")
#cur.execute("create table tune (id integer not null primary key autoincrement, sortkey text, title text)")
#cur.execute("insert into tune (sortkey, title) values ('SLANE', 'SLANE')")

from widgets.tkInputBox import tkInputBox
from widgets.treeViewWithSearch import treeViewWithSearch
win = tkinter.Tk()
	
def add():
	d = tkInputBox({
		"title" : {
			"name":"Title"
		},
		"subtitle" : {
			"name":"Subtitle"
		}
	})
	d.passFunc("add", f1.addSong)

s = ttk.Style()
#s.configure('Treeview', rowheight=48+8)

class folders(tkinter.Frame):

	def delete(self):
		if (len(self.tv.selected()) > 0):
			de=self.tv.item(self.tv.selected()[0])["values"]
			#lbl.config(text= de)
			cur.execute("delete from folder where sortkey = ? and title=?", (de[0], de[1]))
			
			self.tv.delete(self.tv.selected())
			con.commit()
		else:
			showerror("Nothing to delete", "No items or no item selected to delete")
			
	def addFolder(self, data):
		a = data["title"]
		c = buildName(a,a)
		cur.execute("insert into folder (sortkey, title) values (?, ?)", (c,a))
		d = cur.lastrowid
		self.tv.add(["-:" + str(d), c, a])

	def addFolderDialog(self):
		d = tkInputBox({
			"title" : {
				"name":"Folder Name"
			},
		})
		d.passFunc("add", self.addFolder)
		pass
	
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		
		self.tv = treeViewWithSearch(self, 3)
		self.tv.grid(columnspan=3,rowspan=2,sticky="news")
		for i in cur.execute("select * from folder order by sortkey asc"):
			#print(("f-" + str(i[:1][0]),) + i[1:])
			#print(i)
			self.tv.add(("f-" + str(i[:1][0]),) + i[1:])
		self.tv.add(["Nf", "Not in Folder"])
		for i in cur.execute("select * from music order by sortkey asc"):
			self.tv.add(i, "Nf")

		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.sadd = tkinter.Button(self, text="Add...", command=self.addFolderDialog).grid(row = 2,column=1)
		self.sdel = tkinter.Button(self, text="Delete", command=self.delete).grid(row = 2,column=0)
		
class songs(tkinter.Frame):
	
	def addSong(self, data):
		a = data["title"]
		b = data["subtitle"]
		c = buildName(a,b)
		cur.execute("insert into music (sortkey, title,subtitle) values (?, ?,?)", (c,a,b))
		d = cur.lastrowid
		self.tv.add([d, c, a, b])

	def tvSongSearch(self, a,b,c):
		n = self.tt.get()
		self.tv.delete(*self.tv.get_children())
		for i in cur.execute("select * from music where title like '%"+n+"%' order by sortkey asc"):
			self.tv.insert("", "end", i[0], values= [i[1],i[2],i[3]])

	def delete(self):
		if (len(self.tv.selected()) > 0):
			de=self.tv.item(self.tv.selected()[0])["values"]
			#lbl.config(text= de)
			cur.execute("delete from music where sortkey = ? and title=?", (de[0], de[1]))
			
			self.tv.delete(self.tv.selected())
			con.commit()
		else:
			showerror("Nothing to delete", "No items or no item selected to delete")
			
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		self.tt = tkinter.StringVar()
		self.tv = treeViewWithSearch(self, 3)
		self.tv.grid(columnspan=3)
		#self.search_label = tkinter.Label(self, text="search")
		#self.search_label.grid(padx=5, pady=5)
		#self.search_box = tkinter.Entry(self, textvariable=self.tt)
		#self.tt.trace_add('write', self.tvSongSearch)
		#self.search_box.grid(column=1, columnspan=1, row=0,sticky="ew")
		s#elf.tv = ttk.Treeview(self,columns=[1,2,3],show="headings")
		for i in cur.execute("select * from music order by sortkey asc"):
			self.tv.add(i)
			#self.tv.insert("", "end", i[0], values= [i[1],i[2],i[3]])
		#self.tv.grid(columnspan=2, row=1, sticky="news")
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)
		
		self.sadd = tkinter.Button(self, text="Add...", command=add)
		self.sadd.grid(row = 2,column=1)
		self.srem = tkinter.Button(self, text="Delete", command=self.delete)
		self.srem.grid(row = 2, column=0)
		pass

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
