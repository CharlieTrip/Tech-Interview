import random
import numpy as np
import math


class Z_Ring:
	
	def __init__(self, secpar, p, q, f, S):
		
		"""
		Initialize the ring:
		+ secpar : security parameter
		+ p : base of the p-ary representation
		+ q : modulus of R_q
		+ f : f-th root of unity (order)
		+ S : subtractive list
		
		Computed/Defined:
		+ gamma : expansion factor of the ring
		+ l : space for representing q in p-ary (log_p q)
		"""
		self.secpar = secpar
		self.p = p
		self.q = q
		self.S = S
		self.f = f
		self.gamma = 1
		self.l = math.ceil(math.log(q) / math.log(p))
	
	def modq(self, n, shift = True):
		
		"""
		Return n modulo q in range [-q/2,q/2) (shift=True)
			or [0,q) (shfit=False)
		"""
		
		r = n % self.q
		return r - self.q if ((r > self.q / 2) and (shift)) else r
	
	
	def member(self,x,beta):
		"""
		Check if x in R_beta 
		"""
		return abs(x) < beta
	
	
	
	"""
	
	Sampling functions
	
	"""
	
	def sample(self):
		"""
		Sample at random an element in [0, q-1].
		"""
		return self.modq(random.randint(0, self.q - 1))
	
	def sampleS(self, seed=None):
		"""
		Sample at random an element in S
		+ seed : used for reproducing sampling
		"""
		temprandom = random
		if seed is not None:
			temprandom = random.Random(seed)
		return temprandom.choice(self.S)
	
	def sampleM(self, n, m):
		"""
		Sample elements from S and create an n x m numpy matrix.
		"""
		return [[self.sample() for _ in range(m)] for _ in range(n)]
	
	
	"""
	
	Conversion functions
	
	"""
	
	def toPary(self, n):
		"""
		Convert n to p-ary representation.
		"""
		n = self.modq(n,shift=False)
		digits = []
		for _ in range(self.l):
			digits.append(n % self.p)
			n //= self.p
		return digits[::-1] if digits else [0]
	
	def toRing(self, n_list):
		"""
		Convert a p-ary representation back to its ring value.
		"""
		n = 0
		for digit in n_list:
			n = n * self.p + digit
		return self.modq(n)
	
	"""
	
	(Matrix) Operations and Gadgets
	
	"""
	
	def add(self, A, B):
		"""
		Return the matrix sum of A and B, element-wise modulo q.
		"""
		return np.vectorize(self.modq)(np.array(A) + np.array(B))
	
	def minus(self, A):
		"""
		Return the matrix sum of A and B, element-wise modulo q.
		"""
		return self.smult(-1,A)
	
	def smult(self, n, A):
		"""
		Return the scalar multiplication of n and matrix A, element-wise modulo q.
		"""
		return np.vectorize(self.modq)(n * np.array(A))
	
	def mult(self, A, B):
		"""
		Return the matrix multiplication of A and B, element-wise modulo q.
		"""
		return np.vectorize(self.modq)(np.matmul(A, B))
	
	def G(self, u):
		"""
		Gadget function
		"""
		chunks = np.array([u[i:i+self.l] for i in range(0, len(u), self.l)])
		return np.array([self.toRing(chunk) for chunk in chunks])
			
	def Ginv(self, xs):
		"""
		Gadget inverse function
		"""
		if isinstance(xs, list) or isinstance(xs, np.ndarray) :
			tmp = np.concatenate([np.vectorize(self.toPary)(x[0]) for x in xs]).tolist()
		else:
			tmp = np.vectorize(self.toPary)(xs).tolist()
		return tmp
		
