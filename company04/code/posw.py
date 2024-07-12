from ring import Z_Ring
import numpy as np

class PoSW:
	"""
	PoSW primitive
	"""
	
	def __init__(self, secpar, p, q, f, S, n):
		"""
		Initialize the primitive
		+ ring : ring R_q (and all related parameters)
		+ n : dimensions of the input
		
		Computed
		+ m : n times the p-ary maximal representation length
		"""
		self.ring = Z_Ring(secpar=secpar,p=p,q=q,f=f,S=S)
		self.n = n
		self.m = self.n * self.ring.l
	
	
	def generate(self):
		"""
		Generate a challenge
		+ A : n * m matrix
		+ x : n * 1 vector
		"""
		A = self.ring.sampleM(self.n,self.m)
		x = self.ring.sampleM(self.n,1)
		return (A,x)
	
	
	def evaluate(self,A,x,T):
		"""
		Evaluate T times f(x) = -A*Ginv (x) (mod q)
		while storing the intermediate values u_i = Ginv(y_i)
		"""
		witness = []
		yi = x
		for _ in range(T):
			# Gadget Inverse
			ui = self.ring.minus(self.ring.Ginv(yi))
			# Store the partial evaluation
			witness.append(ui)
			# (-1) (A * ui)
			yi = self.ring.mult(A,ui)
			yi = yi.reshape(yi.shape[0],1)
		return (yi, witness)


	
	def prove(self,A,x,y,beta,T,witness,r=None):
		"""
		Proving procedure
		+ r: randomness provided by the verifier
		
		The procedure will automatically advance to the next stage
		"""
		if T == 0:
			return (None, None)
		t = T // 2
		if T == 1:
			return (
					np.array(witness[0]).reshape(self.m,1),
					None
				)
			
		elif T % 2 == 0:
			ut = np.array(witness[T-1]).reshape(self.m,1)
			yp =  self.ring.minus( self.ring.G(ut))
			witnessp = witness[:-1]
			return (
					ut,
					[A,x,yp,beta,T-1,witnessp,r]
				)
			
		else:
			ut = np.array(witness[t]).reshape(self.m,1)
			if r == None:
				return (
					ut,
					[A,x,y,beta,T,witness,r]
				)
			xp = self.ring.add( x , self.ring.smult(r,self.ring.mult(A,ut)))
			yp = self.ring.add( self.ring.smult(r,y) , self.ring.minus( self.ring.G(ut)) )
			betap = 2 * self.ring.gamma * beta
			witnessp = [self.ring.add(witness[i], self.ring.smult(r,witness[t+i+1])) for i in range(t) ]
			return (
					ut,
					[A,xp,yp,betap,t,witnessp,None]
				)
		
		
	def verify(self,u,A,x,y,beta,T,r=None):
		"""
		Verifying procedure
		+ r: randomness provided by the verifier
		
		The procedure will automatically advance to the next stage
		"""
			
		t = T // 2
		if T == 1:
			if all( [all([ self.ring.member(ui[0], beta) for ui in u ]),
				all(self.ring.G(u) == self.ring.minus(x)),
				all(self.ring.mult(A,u) == y)] ):
				return (True, [A,x,y,beta,T-1,r])
			else:
				return (False, None)
			
		elif T % 2 == 0:
			if all( [all([ self.ring.member(ui[0], beta) for ui in u ]), all(self.ring.mult(A,u) == y)] ):
				yp =  self.ring.minus( self.ring.G(u))
				return (
						None,
						[A,x,yp,beta,T-1,r]
					)
			return (False, None)
			
		else:
			if all([ self.ring.member(ui[0], beta) for ui in u ]):
				if r == None:
					r = self.ring.sampleS()
					r = 1
					return (
						None,
						[A,x,y,beta,T,r]
					)
				xp = self.ring.add( x , self.ring.smult(r,self.ring.mult(A,u)))
				yp = self.ring.add( self.ring.smult(r,y) , self.ring.minus( self.ring.G(u)) )
				betap = 2 * self.ring.gamma * beta
				return (
						None,
						[A,xp,yp,betap,t,None]
					)
			return (False,None)
			
		