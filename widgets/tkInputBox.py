import tkinter
import tkinter.ttk as ttk
class tkInputBox():
	def passFunc(self, loc, func):
		self.funcs[loc].append(func)
		
	def add(self):
		snd={}
		#print("Do stuff here") 
		for i,j in self.vars.items():
			if (hasattr(j["obj"], "get")):
				snd[i] = j["obj"].get()
			elif (i in self.a and self.a[i]["type"] == "treeview"):
				snd[i] = j["obj"].selection()
			else:
				if ("selected" in j):
					snd[i] = j["selected"]
				else:
					end[i] = None
					
		for i in self.funcs["add"]:
			i(snd)
		self.win.destroy()
		
	def __init__(self, master, a):
		self.funcs = {"add": []}
		self.vars = {}
		self.a = a
		self.win = tkinter.Toplevel(master)
		h = 0
		for i,j in a.items():
			#Only supports Entry at the moment!
			tkinter.Label(self.win, text=j["name"]).grid(column=0,row=h, sticky="e")
			self.vars[i] = j
			if ("type" in j and j["type"] == "treeview"):
				self.vars[i]["obj"] = ttk.Treeview(self.win)
				for k,l in j["items"].items():
					self.vars[i]["obj"].insert("", tkinter.END, k, text=l)
				self.vars[i]["obj"].grid(column=1,row=h,pady=5,padx=5, sticky="ew")
			elif("type" in j and j["type"] == "label"):
				self.vars[i]["obj"] = tkinter.Label(self.win, text = j['text'])
				self.vars[i]["obj"].grid(column=1,row=h,pady=5,padx=5, sticky="w")
			else:
				self.vars[i]["obj"] = tkinter.Entry(self.win)
				self.vars[i]["obj"].grid(column=1,row=h,pady=5,padx=5, sticky="w")
			h+= 1
		tkinter.Button(self.win, text="Add", command=self.add).grid(column=1,row=h)
		self.win.columnconfigure(1, weight=1)
