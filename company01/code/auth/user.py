# Class abstracting a User

from random import randrange
from cpsigma import CPSigma

class User:
	
	def __init__(self,name="User"):
		self.name = name
	
	def __repr__(self):
		return f"{self.name}"
		
		
	def connect(self,cps):
		self.cps = cps
	
	def setSecret(self,x):
		self.x = x
	
	def register(self):
		return (self.name,self.cps.init(self.x))
	
	def reqAuth(self):
		ri,r = self.cps.commit()
		self.r = r
		return (self.name,ri)
	
	def repAuth(self,c):
		return self.cps.open(self.x,self.r,c)

