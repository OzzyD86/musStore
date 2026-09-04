import tkinter
from tkinter import ttk
from widgets.tkInputBox import tkInputBox
from widgets.treeViewWithSearch import treeViewWithSearch

class labeller(tkinter.Frame):
	
	def useThis(self):
		self.core.cur.execute("DELETE FROM `music_folder`")
		
		for i in self.tv.get_children():
			print(i)
			fold = i.split("-")[1]
			print(fold)
			for j in self.tv.get_children(i):
				self.core.cur.execute("INSERT INTO `music_folder` (`folder_id`, `music_id`) VALUES (?, ?)", (int(fold), int(j)))
				print(j)
		
		self.core.bindings.execute("labeller", "<causeUpdate>")
		pass
		
	def orgaRun(self):
		cur = self.core.cur
		vols = 0
		poses = []
		
		self.tv.clear()
		
		p = cur.execute("sELECT count(*) as `c` FROM `music`")
		total = p.fetchone()[0]
		
		for i in cur.execute("SELECT `id`, `sortkey`, `title` FROM `folder`"):
			vols += 1
			poses.append("f-" + str(i[0]))
			self.tv.add(["f-" + str(i[0]), i[2]])
		
		if (vols == 0):
			return False
		else:
			st = {}
			spl = total / vols

			p = cur.execute("SELECT count(*) as `c`, upper(substr(`sortkey`, 1, 1)) as `a` FROM `music` GROUP BY `a` order by `a` ASC")
			n = 0
			s = 0
			ls = 0
			ql = {0: 0}
			st[s] = []
			for i in p:
				n += i[0]
				ql[s] += i[0]
				b = ((spl*(s+1))-ls, (spl*(s+1))-n)
				#print(b, i, s)
				st[s].append(i)
				ls = n
				if (b[1] < 0):
					#print("Split point reached")
					#print(abs(b[0]), abs(b[1]))
					if (abs(b[1]) <= abs(b[0])):
						ql[s] -= i[0]
						#print("Move last set to next position")
						ql[s+1] = i[0]
					else:
						ql[s+1] = 0
					s+=1
					st[s] = []

		ret = {}
		for i, k in st.items():
			#print(i)
			for j in k:
				#print(i, j)
				ret[j[1]] = poses[i]
		
		for i in cur.execute("select * from music order by sortkey asc"):
			#print(i)
			self.tv.add(i, ret[i[1][0]])
			
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		self.core = self.nametowidget(".").core # Aha! That's how to do it!

		self.tv = treeViewWithSearch(self, 2)
		self.tv.grid(columnspan=3,sticky='news')

		cur = self.core.cur
				
		self.orgaRun()

		#for i in st:
		#	print("Folder " + str(i+1) + ":")
		#	for j in st[i]:
		#		print(j)
		tkinter.Button(self, command=self.orgaRun, text="Re-run").grid(row=1,column=0)
		tkinter.Button(self, command=self.useThis, text="Use This Configuration").grid(row=1,column=1)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
