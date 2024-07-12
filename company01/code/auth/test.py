# Some minimal tests of the classes 
# Code mainly used for debugging/checks


from point import Point
from random import randrange
from group import ModuloGroup as MP

p = 101

# Test Multiplicative Group

g = MP(p)
g.init()

g1 = g.gg
g2 = g.hh

(g1._value*g2._value) % p 
g.o(g1,g2)

g.o(g1,g1)

g.o(g.i(g.g(g1,5)),g.g(g1,5))

set([g.g(g1,i)._value for i in range(p)])
set([g.g(g2,i)._value for i in range(p)])



from cpsigma import CPSigma

cps = CPSigma(g)

x = randrange(2,p-1)
yi = cps.init(x)
(ri,r) = cps.commit()
c = cps.challenge()
s = cps.open(x,r,c)
cps.verify(yi,ri,c,s)


# User-Server

from random import randrange
from group import ModuloGroup as MP
from user import User
from server import Server

p = 19
G = MP(p)

u = User()
s = Server(G)

cps = s.reqConnect()
u.connect(cps)

x = randrange(2,p-1)
u.setSecret(x)
(name,yi) = u.register()
s.register(name,yi)

(name, ri) = u.reqAuth()
c = s.reqAuth(name,ri)

ss = u.repAuth(c)
s.verAuth(ss)

# EC Tests

from group import EllipticGroup
import collections
Coord = collections.namedtuple("P", ["x", "y"])
from point import Point

a = 1
b = 1
q = 1009
p = q 

G = EllipticGroup(a,b,q)

G.gg = Point(Coord(1,149))
G.hh = Point(Coord(157,876))

G.ord(G.gg)
factors(G.ord(G.gg))

G.o(g1,g2)

G.o(g1,g1)
G.g(g1,2)
G.o(G.i(G.g(g1,5)),G.g(g1,5))
