# Finite field instantiation of p in Z/pZ group

from point import Point
from random import randrange

class FiniteField:
    
    def __init__(self, group):
        print("[!!!] FF: Initialized group order is not verified to be prime.")
        print("[!!!] FF: Simplified sampling without controls!")
        self.group = group
        
        
    def add(self, left, right, m=0):
        value = (left._value + right._value) % (self.group - m)
        return Point(value)
        
    def sub(self, left, right, m=0):
        value = (left._value - right._value) % (self.group - m)
        return Point(value)
    
    def mult(self, left, right, m=0):
        value = (left._value * right._value) % (self.group -m)
        return Point(value)
    
    def exp(self, base, exponent,m=0):
        b = base
        e = exponent
        if type(base) != int:
            b = base._value
        if type(exponent) != int:
            e = exponent._value
        power = pow(b,e, self.group - m)
        return Point(power)
        
    def inv(self, left,m = 0):
        return self.exp(left,-1,m=m)
    
    def sample(self,m=0):
        return Point(randrange(2,(self.group-m)))
    
    def __repr__(self):
        return f"Z/{self.group}Z"
