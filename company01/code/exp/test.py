# Some minimal tests of the classes 
# Code mainly used for debugging/checks

from point import Point
from share import Share
from random import randrange


# Check FiniteField 
from field import FiniteField as FF
p = 11
f = FF(p)
a = Point(2)
b = Point(4)

f.add(a,b)
f.sub(a,b)
f.mult(a,b)
f.exp(a,b)
f.inv(a)

# Check Party
from party import Party
pp = Party(1,Point(3),Point(1),f)
pp.proto4(2,Point(4),att=0)


# Check SSS implementation
from sss import SSS
s = SSS(3,2,f)
ai = s.instantiate()

for i in range(20):
	vi = randrange(0,p)
	si = s.share(vi,ai)
	vf = s.reconstruct(si,ai)
	if vi != vf:
		print("{} != {}".format(vi,vf)) 


# Check Fabb
from fabb import Fabb
from point import Point 
from share import Share

f = Fabb(3,3,11)

f.getPoints()

v1 = 3
v2 = 5
s1 = f.share(v1)
s2 = f.share(v2)
f.open(s1)
f.open(s2)


sp = f.product(s1,s2)
f.open(sp)

f.compare(s1,s2)
f.compare(s2,s1)
f.equal(s1,s2)
f.equal(s2,f.share(v2))

f.open(f.srand(0))
f.open(f.srand(1))

f.open(f.ideal_pub_exp_pri(2, s1))
f.open(f.ideal_pri_exp_pub(s1, 3))


as1 = f.share(v1,m=1)
f.open(f.proto4_pub_exp_pri(2,as1))

f.open(f.proto7_pri_exp_pub(s1,3))
f.open(f.proto7_pri_exp_pub(s1,3,ideal=False))

f.proto5_pub_exp_pri(2,s1)
f.proto5_pub_exp_pri(3,s1)
f.proto5_pub_exp_pri(2,s2)
f.proto5_pub_exp_pri(5,s1)

f.proto6_pub_exp_pri(2,as1,ideal=False)
f.proto6_pub_exp_pri(3,as1,ideal=False)
f.proto6_pub_exp_pri(2,as2,ideal=False)
f.proto6_pub_exp_pri(5,as1,ideal=False)
