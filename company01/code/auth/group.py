# Abstract Finite Field class

from point import Point
from random import randrange
from functools import reduce

# Wrapper for EC coordinates
import collections
Coord = collections.namedtuple("P", ["x", "y"])



class FiniteGroup:

    def __init__(self, p):
        print("[!!!] FG: Initialized group order is not verified to be prime.")
        print("[!!!] FF: Simplified sampling without controls!")
        self.p = p
    
    def __repr__(self):
        return f"G({self.p})"
    
    def init(self):
        pass
    
    # Scalar multiplication
    def g(self,left,i):
        pass

    # Sample exponent
    def s(self,m=0):
        pass

    # Operation 
    def o(self, left, right):
        pass
    
    # Inverse
    def i(self,left):
        pass
    
    # Equal Check
    def e(self,left,right):
        pass
    
    # Fix exponent
    def f(self,i):
        pass
    


# Finite multiplicative group instantiation of p in Z*/pZ group

class ModuloGroup(FiniteGroup):
        
    def __repr__(self):
        return f"Z*/{self.p}Z"
    
    def init(self):
        gg = self.s()
        while len(set([pow(gg,i, self.p) for i in range(self.p+1)])) < (self.p-1):
            gg = self.s()
        self.gg = Point(gg)
        hh = self.s()
        while len(set([pow(hh,i, self.p) for i in range(self.p+1)])) < (self.p-1) | hh == gg:
            hh = self.s()
        self.hh = Point(hh)
        self.z = Point(1)

    def g(self,left,i):
        while i < 0:
            i = i + (self.p - 1)
        return reduce(self.o ,[left for _ in range(i)], self.z)

    def s(self,m=0):
        return randrange(m,self.p-1)

    def o(self, left, right):
        return Point((left._value * right._value) % self.p)
        
    def i(self,left):
        return Point(pow(left._value,-1, self.p))
    
    def e(self,left,right):
        return (left._value == right._value)
    
    def f(self,i):
        while i < 0:
            i = i + (self.p - 1)
        return i
    

# Elliptic curve group
# Adapted Code (source):
#   https://gist.github.com/bellbind/1414867/03b4b2dd79b41e65e51716076e5e2b0171628a10
#
# EC: (y**2 = x**3 + a * x + b) mod q
#   a, b: params of curve formula
#   q: prime number


class EllipticGroup(FiniteGroup):
    def __init__(self, a, b, q):
        print("[!!!] EC: not designed for known curve or big fields q")
        print("[!!!] EC: generator of biggest subgroup is brute forced")
        assert 0 < a and a < q and 0 < b and b < q and q > 2
        assert (4 * (a ** 3) + 27 * (b ** 2))  % q != 0
        self.a = a
        self.b = b
        self.q = q
        self.z = Point(Coord(0, 0))
    
    def __repr__(self):
        return f"EC({self.a},{self.b},Z{self.q})"
        
    def init(self):
        m = 0
        for i in range(1,self.q):
            if self.at(i)[0].y != -1:
                P = Point(self.at(i)[0])
                if max(factors(self.ord(P))) > m:
                    m = max(factors(self.ord(P)))
                    mi = i
        bP = Point(self.at(mi)[0])
        tt = reduce((lambda x,y: x*y),factors(self.ord(bP))[:-1], 1)
        self.gg = self.g(bP,tt)
        self.p = m
        r = self.s(m=2)
        self.hh = self.g(self.gg,r)

    def ord(self,left):
        r = left
        i = 1
        while r._value != self.z._value:
            r = self.o(r,left)
            i = i + 1
        return i

    def at(self, x):
        assert x < self.q
        ysq = (x ** 3 + self.a * x + self.b) % self.q
        y, my = sqrt(ysq, self.q)
        return Coord(x, y), Coord(x, my)

    def v(self, p):
        if p == self.z: return True
        l = (p.y ** 2) % self.q
        r = ((p.x ** 3) + self.a * p.x + self.b) % self.q
        return l == r
       
    def e(self,left,right):
        return (left._value == right._value)

    def i(self, left):
        return Point(Coord(left._value.x, - left._value.y % self.q))

    def o(self, left, right):
        if left._value == self.z._value: return right
        if right._value == self.z._value: return left
        if left._value.x == right._value.x and left._value.y != right._value.y: # left + -left == 0
            return self.z
        if left._value.x == right._value.x: # left + left: use tangent line of left as (left,left) line
            l = (3 * left._value.x * left._value.x + self.a) * inv(2 * left._value.y, self.q) % self.q
        else:
            l = (right._value.y - left._value.y) * inv(right._value.x - left._value.x, self.q) % self.q
        x = (l * l - left._value.x - right._value.x) % self.q
        y = (l * (left._value.x - x) - left._value.y) % self.q
        return Point(Coord(x, y))

    def g(self,left,i):
        while i < 0:
            i = i + self.p
        return reduce(self.o ,[left for _ in range(i)], self.z)
    
    def s(self,m=0):
        return randrange(m,self.p-1)
    
    def f(self,i):
        while i < 0:
            i = i + self.p
        return i
    


# Util functions

def inv(n, q):
    return pow(n,-1,q)

def sqrt(n, q):
    assert n < q
    for i in range(1, q):
        if i * i % q == n:
            return (i, q - i)
    return (-1,-1)
    
def factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors