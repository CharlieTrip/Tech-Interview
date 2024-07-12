# Shamir Secret Sharing
#
# n: number of parties
# t: threshold for reconstruction

from random import randrange
from functools import reduce

from point import Point
from share import Share
from field import FiniteField

class SSS:
    
    def __init__(self, n ,t, G):
        print("[!!!] Initialized SSS has no input sanitization.")
        self.n = n
        self.t = t
        self.G = G
    
    # Instantiate the evaluation points to be given to the parties
    def instantiate(self):
        # ai = [Point(randrange(1,G.group)) for i in range(n)]
        ai = [Point(i) for i in range(1,self.n+1)]
        return ai
    
    # Computes Lagrange coefficients
    def lagrange(self, ai,m=0):
        si = [Point( int(reduce( (lambda x, y: x*y),
                    [ (-ai[j]._value)*((ai[i]._value - ai[j]._value)**(-1))
                        if j != i else 1 for j in range(self.t)] , 1) )) for i in range(self.t)]
        return si
    
    # Computes the shares
    # Random polynomial and evaluation in the points
    def share(self, value, ai,m=0):
        fi = [Point(value)] + [Point(randrange(0,self.G.group)) for i in range(1,self.t)]
        si = [reduce((lambda x, y: self.G.add(x,y,m=m)),[self.G.mult(fi[i], self.G.exp(a,i,m=m),m=m)
                for i in range(self.t)],Point(0)) for a in ai]
        return [Share(s._value) for s in si]
    
    # Reconstruct the secret value
    # Minimal check of the input sizes
    def reconstruct(self, shares, points,m=0):
        if (len(shares) != len(points)):
            print("[Error] #Shares != #Points")
            return Point(0)
        if (len(shares) < self.t):
            print("[Error] Not enough shares, required at least {}".format(self.t))
            return Point(0)
        value = reduce((lambda x, y: self.G.add(x,y,m=m)),
                [ self.G.mult(Point(shares[i]._value) ,
                    reduce((lambda x, y: self.G.mult(x,y,m=m)),
                    [self.G.mult(self.G.sub(Point(0),points[j],m=m),
                        self.G.inv(self.G.sub(points[i],points[j],m=m) ,m=m),m=m )
                        if j != i else Point(1) for j in range(self.t)],
                    Point(1)),m=m) for i in range(self.t)],
                Point(0))
        return value._value
    

    def __repr__(self):
        return f"SSS({self.n},{self.t},{self.G})"
        

