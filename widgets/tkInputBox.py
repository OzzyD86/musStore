import tkinter

class tkInputBox():
	def passFunc(self, loc, func):
		self.funcs[loc].append(func)
		
	def add(self):
		snd={}
		#print("Do stuff here") 
		for i,j in self.vars.items():
			snd[i] = j.get()
		
		for i in self.funcs["add"]:
			i(snd)
		self.win.destroy()
		
	def __init__(self, a):
		self.funcs = {"add": []}
		self.vars = {}
		self.win = tkinter.Tk()
		h = 0
		for i,j in a.items():
			#Only supports Entry at the moment!
			self.vars[i] = tkinter.Entry(self.win)
			tkinter.Label(self.win, text=j["name"]).grid(column=0,row=h, sticky="e")
			self.vars[i].grid(column=1,row=h,pady=5,padx=5, sticky="w")
			h+= 1
		tkinter.Button(self.win, text="Add", command=self.add).grid(column=1,row=h)
