# Party participating the protocol

from point import Point

class Party:
    
    def __init__(self, idn,point,lagrange,G):
        self.idn = idn
        self.point = point
        self.lagrange = lagrange
        self.G = G
        self.delta = Point(1)
        
    def __repr__(self):
        return f"P_{self.idn}({self.point})"

    
    def corrupt(self,delta):
        self.delta = Point(delta)
    
    
    def proto4(self,b,si,att=0,m=0):
        if att == 1:
            return self.G.mult(self.G.exp(b,self.lagrange._value*si._value,m=m),self.delta,m=m)
        elif att == 2:
            return self.G.mult(self.G.exp(b,self.lagrange._value*si._value,m=m),
                self.G.inv(self.delta,m=m),m=m)
        else:
            return self.G.exp(b,self.lagrange._value*si._value,m=m)
        
