import tkinter
from tkinter import ttk
from tkinter.messagebox import showerror

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
						if (l not in disp):
							disp.append(l)
						else:
							break
		for i,j in self.storage.items():
			if (i in disp):
				self.tv.insert(j[0], "end", i, text=j[1][0], values= j[1][1:])
				#self.tv.insert(j[0], "end", i, values= j[1])
				if (i in self.opens):
					self.tv.item(i, open=True)
	
	def selected(self):
		return self.tv.selection()
	
	def move(self, what, where, loc = 0):
		self.tv.move(what, where , loc)
		self.storage[what][0] = where 

	def delete(self, id):
#		print(id)
		print(list(self.storage.keys()))
#		return
		if (type(id) in [list, tuple]):
			for i in id:
				if (i in self.storage):
					del self.storage[i]
				elif(int(i) in self.storage):
					del self.storage[int(i)]
				else:
					del self.storage[str(i)] # Is this not good enough for you?!
		else:
			del self.storage[int(id)]
		self.tv.delete(id)
		# We need to solve recursive deletes here?
		pass
	
	def item(self, item):
		return self.tv.item(item)
		
	def add(self, data, parent = ""):
		self.storage[data[0]] = [parent, data[1:]]
		self.tv.insert(parent, "end", data[0], text=data[1], values= data[2:])

	def update_closed_items(self, event):
		tree = event.widget
		item_id = tree.focus()
		self.opens.discard(item_id)
		#showerror(event.type, self.opens)
		
	def update_open_items(self, event):
		tree = event.widget
		item_id = tree.focus()
    
		if event.type == "35" or "Open" in str(event):  # <<TreeviewOpen>>
			self.opens.add(item_id)
		#elif event.type == "36" or "Close" in str(event):  # <<TreeviewClose>>
		#	self.opens.discard(item_id)
		#showerror(event.type, self.opens)
        
	def __init__(self, master, storeSize = 2, **kw):
		self.storage = {}
		self.opens = set()
		super().__init__(master, **kw)
		self.tt = tkinter.StringVar()

		self.search_label = tkinter.Label(self, text="search")
		self.search_label.grid(padx=5, pady=5)
		self.search_box = tkinter.Entry(self, textvariable=self.tt)
		self.tt.trace_add('write', self.search)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(1, weight=1)
	
		self.search_box.grid(column=1, columnspan=2, row=0,sticky="ew")
		
		self.tv = ttk.Treeview(self,columns=list(range(1,storeSize+1)),show="tree headings")
		self.tv.bind("<<TreeviewOpen>>", self.update_open_items)
		self.tv.bind("<<TreeviewClose>>", self.update_closed_items)

		self.tv.grid(columnspan=2, row=1, sticky="news")
		self.sb = tkinter.Scrollbar(self)
		self.sb.grid(column=2,row=1,sticky="ns")
		self.sb.config(command=self.tv.yview)
		self.tv.config(yscrollcommand=self.sb.set)
