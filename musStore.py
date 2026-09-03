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

s = ttk.Style()
import sys

if hasattr(sys, 'getandroidapilevel'):
	s.configure('Treeview', rowheight=48+8)
	err = tkinter.Toplevel(win)
	displayText = tkinter.Text(err, height=20, width=40)
	displayText.grid()
	tkinter.Tk.report_callback_exception = report_callback_exception


from plugins.songs import songs
from plugins.folders import folders
from plugins.labeller import labeller

setattr(win, "core", ms)
notebook = ttk.Notebook(win, style='lefttab.TNotebook')

f1 = songs(notebook, bg='red')
fo = folders(notebook, bg='green')
f2 = tkinter.Frame(notebook, bg='blue', width=200, height=200)

notebook.add(f1, text='Songs')
notebook.add(fo, text='Folders')

ao = labeller(notebook, bg='blue')
notebook.add(ao, text='Auto-organise')

notebook.grid(sticky="news")

win.rowconfigure(0, weight=1)
win.columnconfigure(0, weight=1)
win.mainloop()
con.commit()
