# Class abstracting a Server

from random import randrange
from cpsigma import CPSigma

class Server:
	
	def __init__(self,G,name="Server"):
		self.name = name
		self.G = G
		self.G.init()
		self.cps = CPSigma(G)
		self.users = {}
	
	def __repr__(self):
		return f"{self.name}({self.cps})"
		
	def reqConnect(self):
		return self.cps
	
	def register(self,name,yi):
		self.users[name] = yi
	
	def reqAuth(self,name,ri):
		c = self.cps.challenge()
		self.tmp = (name,ri,c)
		return c
	
	def verAuth(self,s):
		(name,ri,c) = self.tmp
		return self.cps.verify(self.users[name],ri,c,s)

