import tkinter
from tkinter import ttk
from widgets.tkInputBox import tkInputBox
from widgets.treeViewWithSearch import treeViewWithSearch

class labeller(tkinter.Frame):
	def __init__(self, master, **kw):
		super().__init__(master, **kw)
		self.core = self.nametowidget(".").core # Aha! That's how to do it!

		self.tv = treeViewWithSearch(self, 2)
		self.tv.grid(columnspan=3,sticky='news')

		cur = self.core.cur
		
		p = cur.execute("sELECT count(*) as `c` FROM `music`")
		total = p.fetchone()[0]
		#print(total)
				
		vols = 0
		poses = []
		for i in cur.execute("SELECT `id`, `sortkey`, `title` FROM `folder`"):
			vols += 1
			poses.append("f-" + str(i[0]))
			self.tv.add(["f-" + str(i[0]), i[2]])

		spl = total / vols
		#print(spl)
		st = {}
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

		#for i in st:
		#	print("Folder " + str(i+1) + ":")
		#	for j in st[i]:
		#		print(j)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
