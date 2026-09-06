import sqlite3
from core.bindings import bindings

class musStore():
	def __init__(self):
		self.con = sqlite3.connect("musScore.db") # Should change this at some point!
		self.cur = self.con.cursor()
		self.bindings = bindings()

class loader():
	def __init__(self):
		self.loaders = {}
	
	def is_loaded(self, mod):
		return (mod in list(self.loaders.keys()))
