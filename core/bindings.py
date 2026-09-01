class bindings():
	def __init__(self):
		self.bindings = {}

	def bind(self, applet, call, func):
		if (applet not in self.bindings):
			self.bindings[applet] = {}
			
		if (call not in self.bindings[applet]):
			self.bindings[applet][call] = []
			
		self.bindings[applet][call].append(func)
		return True
	
	def getBindings(self, applet, call):
		if (applet in self.bindings):
			if (call in self.bindings[applet]):
				return self.bindings[applet][call]
		return False
