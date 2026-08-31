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

class tkInputBox():
	def passFunc(self, loc, func):
		self.funcs[loc].append(func)
		
	def add(self):
		snd={}
		print("Do stuff here") 
		for i,j in self.vars.items():
			snd[i] = j.get()
		a = self.vars["title"].get()
		b = self.vars["subtitle"].get()
		c = buildName(a,b)
		cur.execute("insert into music (sortkey, title,subtitle) values (?, ?,?)", (c,a,b))
		for i in self.funcs["add"]:
			i()
		pg.insert("", tkinter.END, text=c, values= [c, a, b])
		self.win.destroy()
		
	def __init__(self, a):
		self.funcs = {"add": []}
		self.vars = {}
		self.win = tkinter.Tk()
		h = 0
		for i,j in a.items():
			self.vars[i] = tkinter.Entry(self.win)
			tkinter.Label(self.win, text=j["name"]).grid(column=0,row=h, sticky="e")
			self.vars[i].grid(column=1,row=h,pady=5,padx=5, sticky="w")
			h+= 1
		tkinter.Button(self.win, text="Add", command=self.add).grid(column=1,row=h)

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

s = ttk.Style()
s.configure('Treeview', rowheight=48+8)

class treeViewWithSearch(tkinter.Frame):
	def search(self, a,b,c):
		n = self.tt.get()
		disp = []
		self.tv.delete(*self.tv.get_children())
		for i,j in self.storage.items():
			t=0
			for k in j[1]:
				if (k.upper().find(n.upper()) >= 0):
					t+= 1
			if (t >0):
				if (j not in disp):
					disp.append(i)
					k = j.copy()
					
					while (k[0] != ""):
						l = k[0]
						k = self.storage[k[0]]
						#showerror("", l)
						if (l not in disp):
							disp.append(l)
						else:
							break
		for i,j in self.storage.items():
			if (i in disp):
				self.tv.insert(j[0], "end", i, values= j[1])
				if (i in self.opens):
					self.tv.item(i, open=True)

		#showerror("complete", "done")
					
	def add(self, data, parent = ""):
		self.storage[data[0]] = [parent, data[1:]]
		self.tv.insert(parent, "end", data[0], values= data[1:])

	def update_open_items(self, event):
		tree = event.widget
		item_id = tree.focus()
    
    # Check the actual Tkinter event type to add or remove
		if event.type == "35" or "Open" in str(event):  # <<TreeviewOpen>>
			self.opens.add(item_id)
		elif event.type == "36" or "Close" in str(event):  # <<TreeviewClose>>
			self.opens.discard(item_id)
        
    # Print the current set of open item names for debugging
    #open_names = [tree.item(i, "text") for i in currently_open_items]
    #print(f"Currently open items: {open_names}")

	def __init__(self, master, storeSize = 2, **kw):
		self.storage = {}
		self.opens = set()
		super().__init__(master, **kw)
		self.tt = tkinter.StringVar()

		self.search_label = tkinter.Label(self, text="search")
		self.search_label.grid(padx=5, pady=5)
		self.search_box = tkinter.Entry(self, textvariable=self.tt)
		self.tt.trace('w', self.search)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(1, weight=1)
	
		self.search_box.grid(column=1, columnspan=2, row=0,sticky="ew")
		
		self.tv = ttk.Treeview(self,columns=list(range(1,storeSize+1)),show="headings")
		self.tv.bind("<<TreeviewOpen>>", self.update_open_items)
		self.tv.bind("<<TreeviewClose>>", self.update_open_items)

		self.tv.grid(columnspan=2, row=1, sticky="news")
		self.sb = tkinter.Scrollbar(self)
		self.sb.grid(column=2,row=1,sticky="ns")
		self.sb.config(command=self.tv.yview)
		self.tv.config(yscrollcommand=self.sb.set)

class folders(tkinter.Frame):
	def add(self):
		pass
	
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		
		p = treeViewWithSearch(self, 3)
		p.grid(columnspan=3,rowspan=2,sticky="news")
		p.add(["Nf", "Not in Folder"])
		for i in cur.execute("select * from music order by sortkey asc"):
			p.add(i, "Nf")

		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.sadd = tkinter.Button(self, text="Add...", command=self.add)
		self.sadd.grid(row = 2,column=1)
		
class songs(tkinter.Frame):
	def tvSongSearch(self, a,b,c):
		n = self.tt.get()
		self.tv.delete(*self.tv.get_children())
		for i in cur.execute("select * from music where title like '%"+n+"%' order by sortkey asc"):
			self.tv.insert("", "end", i[0], values= [i[1],i[2],i[3]])

	def delete(self):
		de=self.tv.item(self.tv.selection()[0])["values"]
		lbl.config(text= de)
		cur.execute("delete from music where sortkey = ? and title=?", (de[0], de[1]))
		
		self.tv.delete(pg.selection())
		con.commit()
		
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		self.tt = tkinter.StringVar()
		self.search_label = tkinter.Label(self, text="search")
		self.search_label.grid(padx=5, pady=5)
		self.search_box = tkinter.Entry(self, textvariable=self.tt)
		self.tt.trace('w', self.tvSongSearch)
		self.search_box.grid(column=1, columnspan=1, row=0,sticky="ew")
		self.tv = ttk.Treeview(self,columns=[1,2,3],show="headings")
		for i in cur.execute("select * from music order by sortkey asc"):
			self.tv.insert("", "end", i[0], values= [i[1],i[2],i[3]])
		self.tv.grid(columnspan=2, row=1, sticky="news")
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
pg = f1.tv

mu = ttk.Treeview(f2,columns=[1,2,3],show="headings")
for i in cur.execute("select * from tune order by sortkey asc"):
	mu.insert("", "end", i[0], values= [i[1],i[2]])
mu.grid(columnspan=2, sticky="news")

notebook.add(f1, text='Songs')

#notebook.add(f2, text='Tunes')
notebook.add(fo, text='Folders')
notebook.grid(sticky="news")
lbl = tkinter.Label(f1, text="")
#lbl.grid(row=3,columnspan=3)
sb = tkinter.Scrollbar(f1)
sb.grid(column=3,row=1,sticky="ns")
sb.config(command=pg.yview)
pg.config(yscrollcommand=sb.set)
	
win.rowconfigure(0, weight=1)
win.columnconfigure(0, weight=1)
win.mainloop()
con.commit()
