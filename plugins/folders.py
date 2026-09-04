import tkinter
from tkinter import ttk
from tkinter.messagebox import showerror
from widgets.tkInputBox import tkInputBox
from widgets.treeViewWithSearch import treeViewWithSearch
from plugins.songs import buildName

class folders(tkinter.Frame):

	def delete(self):
		if (len(self.tv.selected()) > 0):
			if (self.tv.selected()[0] == "Nf"):
				showerror("Deleting built-in folder", "This folder is a built-in folder and cannot be deleted.")
				return False
				
			sel = self.tv.selected()[0]
			de=self.tv.item(self.tv.selected()[0])["values"]
			te=self.tv.item(self.tv.selected()[0])["text"]
			
			if (sel.split("-")[0] != "f"):
				showerror("This is not a folder", "Only folders can be deleted here. Their contents cannot.")
				return False				
			
			d = self.cur.execute("select count(*) as c from music_folder a join folder b on a.folder_id = b.id where b.sortkey = ? and b.title = ?", (te, de[0]))
			ct = d.fetchone()[0]
			if (ct > 0):
				showerror("Folder is not empty", "This folder is not empty and cannot be deleted.")
				return False
				
			self.cur.execute("delete from folder where sortkey = ? and title=?", (te, de[0]))
			
			self.tv.delete(self.tv.selected())
			self.core.con.commit()
		else:
			showerror("Nothing to delete", "No items or no item selected to delete")
			
	def addFolder(self, data):
		a = data["title"]
		c = buildName(a,a)
		self.cur.execute("insert into folder (sortkey, title) values (?, ?)", (c,a))
		d = self.cur.lastrowid
		self.tv.add(["f-" + str(d), c, a])
		
	def updateSongToFolder(self, a):
	
		c = self.tv.selected()[0].split("-")[1]
		parent = self.tv.storage[self.tv.selected()[0]][0]
	
		for b in a["folder"]:
			self.cur.execute("replace into music_folder (music_id, folder_id) values (?,?)", (c,b))
			if (not self.tv.exists("f-"+str(b))):
				self.tv.forcedisp("f-"+str(b))
			self.tv.move(self.tv.selected()[0], "f-"+str(b),0)

		if (len(self.tv.get_children(parent)) == 0 and not self.tv.checkForSearch(parent)):
			self.tv.tv.delete(parent) # Happy over this, but should it be done in checkForSearch?
			
		self.core.con.commit()
		pass
		
	def updateSongDialog(self):
		x = {}
		if (len(self.tv.selected()) == 0):
			return False
		for i in self.cur.execute("select id, title from folder"):
			x[i[0]] = i[1]
			
		p = self.tv.selected()[0].split("-")
		if (p[0] != "s"):
			return False
		#showerror(p)
		
		d = tkInputBox(self, {
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
		self.cur.execute("delete from music_folder where music_id = ?", (data['dbid'],))
		print(data)
		
	def addFolderDialog(self):
		d = tkInputBox(self, {
			"title" : {
				"name":"Folder Name"
			},
		})
		d.passFunc("add", self.addFolder)
		pass
	
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		self.core = self.nametowidget(".").core # Aha! That's how to do it!
		self.cur = self.core.cur
		self.core.bindings.bind("music", "<create>", self.songsAddedNewSong)
		self.core.bindings.bind("music", "<delete>", self.songsDeletedSong)
		self.tv = treeViewWithSearch(self, 2)
		self.tv.grid(columnspan=3,rowspan=2,sticky="news")
		for i in self.cur.execute("select * from folder order by sortkey asc"):
			self.tv.add(("f-" + str(i[:1][0]),) + i[1:])
			
		self.tv.add(["Nf", "Not in Folder"])
		for i in self.cur.execute("select a.*, b.folder_id from music a left join music_folder b on a.id = b.music_id order by a.sortkey asc"):
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
