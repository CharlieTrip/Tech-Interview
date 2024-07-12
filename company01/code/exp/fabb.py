# Ideal functionality interface
# 
# The functionality instantiates all the element of the protocol
# thus requiring number of parties n, threshold t and field size q


from point import Point
from share import Share
from party import Party
from field import FiniteField as FF
from sss import SSS
from functools import reduce

class Fabb:
	
	def __init__(self, n,t,q):
		print("[!!!] Initialized F_ABB has no input sanitization!")
		print("[!!!] Initialized F_ABB has no parties communication!")
		print("[!!!] Proto4 only works for n=t!")
		print("[!!!] Proto7 only works for n=t!")
		
		self.G = FF(q)
		self.S = SSS(n,t,self.G)
		p = self.S.instantiate()
		l = self.S.lagrange(p)
		self.parties = [ Party(i,pi,li,self.G) for i,pi,li in list(zip(range(n),p,l)) ]

	def __repr__(self):
		return f"F_ABB : {self.G},{self.S},{self.parties}"

	
	# Auxiliary functions to get the parties points
	
	def getPoints(self):
		return [pi.point for pi in self.parties]
		

	# Ideal functionalities

	def share(self,x,m=0):
		return self.S.share(x,self.getPoints(),m=m)
	
	def product(self,x,y,m=0):
		p = self.getPoints()
		vx = Point(self.S.reconstruct(x,p))
		vy = Point(self.S.reconstruct(y,p))
		vz = self.G.mult(vx,vy,m=m)._value
		return self.S.share(vz,p,m=0)
	
	def product_fold(self,xs,m=0):
		return reduce((lambda x,y: self.product(x,y,m=m)),xs,self.share(1))

	def product_right_public(self, share, public,m=0):
		p = self.getPoints()
		vx = Point(self.S.reconstruct(share,p,m=m))
		vy = Point(public)
		vz = self.G.mult(vx,vy,m=m)._value
		return self.S.share(vz,p)

	def compare(self,x,y,m=0):
		p = self.getPoints()
		vx = self.S.reconstruct(x,p,m=m)
		vy = self.S.reconstruct(y,p,m=m)
		if vx < vy:
			return 0
		else:
			return 1
	
	def equal(self,x,y,m=0):
		p = self.getPoints()
		vx = self.S.reconstruct(x,p,m=m)
		vy = self.S.reconstruct(y,p,m=m)
		if vx == vy:
			return 1
		else:
			return 0
	
	# Random value in the group
	def srand(self,m=0):
		return self.S.share(self.G.sample(m=m)._value,self.getPoints(),m=m)
		
	
	def open(self,x,m=0):
		return self.S.reconstruct(x,self.getPoints(),m=m)


	# Nomenclature:
	# Private/Public (base) "exp" Private/Public (exponent)
	# [pri,pub] exp [pri,pub]

	def ideal_pub_exp_pri(self, b, e):
		p = self.getPoints()
		ve = self.S.reconstruct(e,p)
		power = self.G.exp(b, ve)
		return self.S.share(power._value,p)
	
	def ideal_pri_exp_pub(self, b, e):
		p = self.getPoints()
		vb = self.S.reconstruct(b,p)
		power = self.G.exp(vb, e)
		return self.S.share(power._value,p)
		
	
	def proto4_pub_exp_pri(self,b,e,att=0,m=0):
		ci = [ self.parties[i].proto4(b,e[i],att=att,m=m) for i in range(len(self.parties))]
		sci = [self.share(c._value,m=0) for c in ci]
		return self.product_fold(sci,m=0)
	
	def proto5_pub_exp_pri(self,b,e,ideal=True):
		if ideal:
			bai = self.ideal_pub_exp_pri(b,e)
		else:
			# Quick fix: fix modulo difference between exponent and base
			ee = self.share(self.open(e),m=1)
			bai = self.proto4_pub_exp_pri(b,ee)
		ri = self.srand(m=1)
		ap = self.product(e,ri,m=1)
		if ideal:
			bapi = self.ideal_pub_exp_pri(b,ap)
		else:
			ap = self.share(self.open(ap),m=1)
			bapi = self.proto4_pub_exp_pri(b,ap)
		r = self.open(ri)
		rpi = self.srand(m=1)
		
		one = self.share(1)
		t1 = self.proto7_pri_exp_pub(bai,r,ideal=ideal)
		t2 = [self.G.sub(t1[i],bapi[i]) for i in range(len(t1))]
		t3 = self.product(rpi, t2)
		t4 = [Share(self.G.add(t3[i],one[i])._value) for i in range(len(t3))]
		return (self.open(t4), bai)
			
		
		
	
	def proto6_pub_exp_pri(self,b,e,ideal=True):
		if ideal:
			bai = self.ideal_pub_exp_pri(b,e)
		else:
			ee = self.share(self.open(e),m=1)
			bai = self.proto4_pub_exp_pri(b,ee)
		one = self.share(1)
		ri = self.srand(m=1)
		t1 = [self.G.sub(ri[i],one[i]) for i in range(len(ri))]
		ap = self.product(e,t1,m=1)
		if ideal:
			bapi = self.ideal_pub_exp_pri(b,ap)
		else:
			ap = self.share(self.open(ap),m=1)
			bapi = self.proto4_pub_exp_pri(b,ap)
		wi = self.product(e,ri,m=1)
		w = self.open(wi)
		bw = self.G.exp(b,(-w))
		rpi = self.srand(m=1)
		t1 = self.product(bai,bapi)
		t2 = [self.G.sub(self.G.mult(t1[i],bw),one[i]) for i in range(len(t1))]
		t3 = self.product(rpi, t2)
		t4 = [Share(self.G.add(t3[i],one[i])._value) for i in range(len(t3))]
		return (self.open(t4), bai)

	def proto6_pub_exp_pri_att(self,b,e):
		ee = self.share(self.open(e),m=1)
		bai = self.proto4_pub_exp_pri(b,ee,att=1)
		one = self.share(1)
		ri = self.srand(m=1)
		t1 = [self.G.sub(ri[i],one[i]) for i in range(len(ri))]
		ap = self.product(e,t1,m=1)
		ap = self.share(self.open(ap),m=1)
		bapi = self.proto4_pub_exp_pri(b,ap,att=2)
		wi = self.product(e,ri,m=1)
		w = self.open(wi)
		bw = self.G.exp(b,(-w))
		rpi = self.srand(m=1)
		t1 = self.product(bai,bapi)
		t2 = [self.G.sub(self.G.mult(t1[i],bw),one[i]) for i in range(len(t1))]
		t3 = self.product(rpi, t2)
		t4 = [Share(self.G.add(t3[i],one[i])._value) for i in range(len(t3))]
		return (self.open(t4), bai)
	
	
	def proto7_pri_exp_pub(self,b,e,ideal=True):
		g = self.G.sample()
		while len(set([self.G.exp(g,i)._value for i in range(self.G.group)])) < (self.G.group -1):
			g = self.G.sample()
		ri = self.srand(m=1)
		if ideal:
			rbi = self.ideal_pub_exp_pri(g,ri)
		else:
			ri = self.share((self.open(ri)),m=1)
			rbi = self.proto4_pub_exp_pri(g,ri)
		ci = self.product(b,rbi)
		c = self.open(ci)
		
		cc = self.G.exp(c,e)
		gg = self.G.exp(g,(self.G.group- 1 - e))
		if ideal:
			tmp = self.ideal_pub_exp_pri(gg,ri)
		else:
			tmp = self.proto4_pub_exp_pri(gg,ri)
		ba = [Share(self.G.mult(cc,tmp[i])._value) for i in range(len(b))]
		return ba
		