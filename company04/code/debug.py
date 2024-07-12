# ! Quick Test/Debug Code !
# Mainly Debugging and minimal manual tests
#
# It would be nice to expand it into an appropriate test-suite!

from ring import Z_Ring
from posw import PoSW
import numpy as np


p = 2
q = 5

# Test code for the Ring class

# Initialize Ring object
ring = Z_Ring(secpar=1, p=p, q=q, f=1, S=[0,1])

# Test modq function
print("modq:\n", [ring.modq(i) for i in range(10)])

# Test sample function
print("sample:\n", [ring.sample() for _ in range(5)])
print("sampleS:\n", [ring.sampleS() for _ in range(5)])
print("sampleS:\n", [ring.sampleS(seed="123") for _ in range(5)])
print("sampleM:\n", [ring.sampleM(3,i+1) for i in range(2)])

# Test toPary function
print("toPary:\n", [ring.toPary(i) for i in range(10)]) 

# Test toRing function
print("toRing([2, 2]):\n", ring.toRing([2, 2]))  # Expected output: 17

# Test Pary Ring inverse
print("P R inv:\n",[ring.toRing(ring.toPary(i)) == ring.modq(i) for i in range(10)])

# Test add function
A = [[1, 2], [3, 4]]
B = [[2, 3], [4, 1]]
print("add(A, B):\n", ring.add(A, B))  

# Test smult function
n = 2
print("smult(2, A):\n", ring.smult(n, A))

# Test mult function
C = [[1, 2], [3, 4]]
D = [[2, 1], [4, 3]]
print("mult(C, D):\n", ring.mult(C, D))  

C = [[1, 2], [3, 4]]
D = np.transpose([[2, 1]])

print("mult(C, D) vect:\n", ring.mult(C, D)) 

# Test G function
u = [1, 2, 3, 4, 5, 6, 7, 8]
print("G(u):\n", ring.G(u)) 

# print("test: ", ring.GinvV([1,2]))

# print("Ginv GinvV:\n", [ring.G(ring.GinvV([i,1])) == [ring.modq(i),ring.modq(i)] for i in range(10)])

# Test G Ginv
print("G Ginv:\n",[ring.G(ring.Ginv([[i]]))[0] == ring.modq(i) for i in range(10)])





# Test code for the PoSW class

p = 2
q = 5
T = 2
n = 3

posw = PoSW(secpar=1, p=p, q=q, f=1, S=[0,1], n = 3)

A,x = posw.generate()
A= [[1, 2, 1, -2, -2, 0, 2, 2, 1], [2, -2, -1, 1, 1, -2, 0, 1, 1], [-1, 0, 0, 0, -2, 2, 0, -2, 1]]; x=[[2], [-1], [1]]

print("gen:\n",A,x)

print("\nEval T {}:".format(T),A,x)
y, witness = posw.evaluate(A,x,T)
print("Result: ",np.transpose(y),witness)



beta = p
r = None

Sp = [A,x,y,p,T,witness]
Sv = [A,x,y,p,T,None]

res = None

while res == None:
	# Executes Prover step (output u)
	u, Sp = posw.prove(Sp[0],Sp[1],Sp[2],Sp[3],Sp[4],Sp[5],Sv[5])
	# Executes Verifier step (output r if necessary as Sv[5])
	res, Sv = posw.verify(u,Sv[0],Sv[1],Sv[2],Sv[3],Sv[4],Sv[5])
	print("{} {}".format(res,Sv))
	if Sp != None:
		print("> w{} Tp{} Tv{} res{}:".format(len(Sp[5]),Sp[4],Sv[4],res))
print(res)
