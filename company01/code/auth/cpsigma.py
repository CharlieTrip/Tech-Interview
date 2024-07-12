# Chaum-Pedersen ∑-protocol

from random import randrange

class CPSigma:
	def __init__(self, G):
		self.G = G
		G.init()
	
	def __repr__(self):
		return f"CP({self.G})"
	
	def init(self,x):
		return (self.G.g(self.G.gg,x),self.G.g(self.G.hh,x))
	
	def commit(self):
		r = self.G.s()
		return ((self.G.g(self.G.gg,r),self.G.g(self.G.hh,r)),r)
	
	def challenge(self):
		return randrange(0,2)
	
	def open(self,x,r,c):
		return self.G.f(r - c*x)
	
	def verify(self,yi,ri,c,s):
		g1 = self.G.gg
		g2 = self.G.hh
		if (self.G.e(ri[0],self.G.o(self.G.g(g1,s),self.G.g(yi[0],c))) &
				self.G.e(ri[1],self.G.o(self.G.g(g2,s),self.G.g(yi[1],c)))):
			return 1
		return 0
