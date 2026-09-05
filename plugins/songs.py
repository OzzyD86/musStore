import tkinter
from tkinter import ttk
from tkinter.messagebox import showerror
from widgets.tkInputBox import tkInputBox
from widgets.treeViewWithSearch import treeViewWithSearch

def buildName(a,b): # Import this?
	for i in [" ", ",","!", "'"]:
		a = a.replace(i, "")
		b = b.replace(i,"")
		
	if (len(b.strip()) == 0):
		return a[:8].upper()
	return b[:8].upper()
	
class songs(tkinter.Frame):
	def editSong(self, data):
		a = data["title"]
		b = data["subtitle"]
		c = buildName(a,b)
		i = data["val"]
		self.core.cur.execute("update music set sortkey = ?, title = ?, subtitle = ? where id = ?", (c,a,b,i))
		self.tv.update(int(i), [c,a,b])
		self.core.bindings.execute("music", "<update>", title = a, subtitle=b, sortkey = c, dbid = i)
		#showerror(data)
		
	def editD(self): # Class this?
		
		p = self.tv.item(self.tv.selected()[0])
		d = tkInputBox(self, {
			"val" : {
				"name":"Selected",
				"type": "label",
				"text": self.tv.selected()[0],
				"selected": self.tv.selected()[0]
			},
			"title" : {
				"name":"Title",
				"text": p["values"][0]
			},
			"subtitle" : {
				"name":"Subtitle",
				"text": p["values"][1]
			}
		})
		d.passFunc("add", self.editSong)
	def addD(self):
		d = tkInputBox(self, {
			"title" : {
				"name":"Title"
			},
			"subtitle" : {
				"name":"Subtitle"
			}
		})
		d.passFunc("add", self.addSong)
	
	def delete(self):
		if (len(self.tv.selected()) > 0):
			
			for i in self.tv.selected():
				
				de=self.tv.item(i)["values"]
				te=self.tv.item(i)["text"]
			
				self.cur.execute("delete from music where sortkey = ? and title=?", (te, de[0]))
				
				s = i
				#print(de[0], te, s)
				
				self.core.bindings.execute("music", "<delete>", sortkey = de[0], title = te, dbid =  str(s))

				self.tv.delete(int(i))
			self.core.con.commit()
		else:
			showerror("Nothing to delete", "No items or no item selected to delete")
			
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		self.core = self.nametowidget(".").core # Aha! That's how to do it!
		self.cur = self.core.cur
		self.tt = tkinter.StringVar()
		self.tv = treeViewWithSearch(self, 2)
		self.tv.grid(columnspan=3,sticky='news')

		for i in self.cur.execute("select * from music order by sortkey asc"):
			self.tv.add(i)

		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		
		self.sadd = tkinter.Button(self, text="Add...", command=self.addD)
		self.sadd.grid(row = 2,column=1)
		self.srem = tkinter.Button(self, text="Delete", command=self.delete)
		self.srem.grid(row = 2, column=0)
		self.sed = tkinter.Button(self, text="Edit...", command=self.editD)
		self.sed.grid(row = 2,column=2)
	def addSong(self, data):
		a = data["title"]
		b = data["subtitle"]
		c = buildName(a,b)
		self.cur.execute("insert into music (sortkey, title,subtitle) values (?, ?,?)", (c,a,b))
		d = self.cur.lastrowid
		self.core.bindings.execute("music", "<create>", title = a, subtitle=b, sortkey = c, dbid = d)

		self.tv.add([d, c, a, b])
		self.core.con.commit()

	def tvSongSearch(self, a,b,c):
		n = self.tt.get()
		self.tv.delete(*self.tv.get_children())
		for i in self.cur.execute("select * from music where title like '%"+n+"%' order by sortkey asc"):
			self.tv.insert("", "end", i[0], values= [i[1],i[2],i[3]])
		
