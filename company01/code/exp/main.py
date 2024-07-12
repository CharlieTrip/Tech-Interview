# Main showcase of the protocol

from fabb import Fabb
from random import randrange

from point import Point 
from share import Share

n = 5
t = 5
p = 101

def main():
    print(">>>> Beware, this is a Proof of Concept")
    print(">>>> Warning will be displayed with [!!!]\n")

    print(">> Initializing the ideal functionality with parameters:")
    print("n parties: {} , t threshold: {}, p prime: {}\n".format(n,t,p))

    f = Fabb(n,t,p)

    print()

    print(">> Initializing two random elements")
    v1 = randrange(2,p-2)
    v2 = randrange(2,p-2)

    s1 = f.share(v1)
    s2 = f.share(v2)
    print("\n\n>> Value -> Shares -> Opening")
    print("{} -> {} -> {}".format(v1,s1,f.open(s1)))
    print("{} -> {} -> {}".format(v2,s2,f.open(s2)))

    sp = f.product(s1,s2)
    print("\n\n>> Value x Value -> Shares -> Opening [Manual Check]")
    print("{} x {} -> {} -> {} [{}]".format(v1,v2,sp,f.open(sp),(v1*v2)%p))

    print("\n\n>> ValueL > ValueR -> 0/1")
    print("{} > {} -> {}".format(v1,v2,f.compare(s1,s2)))
    print("{} > {} -> {}".format(v2,v1,f.compare(s2,s1)))

    print("\n\n>> ValueL == ValueR -> 0/1")
    print("{} == {} -> {}".format(v1,v2,f.equal(s1,s2)))
    print("{} == {} -> {}".format(v2,v2,f.equal(s2,f.share(v2))))

    print("\n\n>> Ideal Exponential Base ** Exp = Value [Manual Check]")
    print("{} ** {} -> {} = {} [{}]".format(2,v1,s1,f.open(f.ideal_pub_exp_pri(2, s1)),(2**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v2,s2,f.open(f.ideal_pub_exp_pri(3, s2)),(3**v2 % p)))
    print("{} -> {} ** {} = {} [{}]".format(v1,s1,3,f.open(f.ideal_pri_exp_pub(s1, 3)),(v1**3 % p)))
    print("{} -> {} ** {} = {} [{}]".format(v2,s2,5,f.open(f.ideal_pri_exp_pub(s2, 5)),(v2**5 % p)))

    as1 = f.share(v1,m=1)
    as2 = f.share(v2,m=1)
    print("\n\n>> Proto4 and Proto7 Exponential Base ** Exp = Value [Manual Check]")
    print("{} ** {} -> {} = {} [{}]".format(2,v1,as1,f.open(f.proto4_pub_exp_pri(2, as1)),(2**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v2,as2,f.open(f.proto4_pub_exp_pri(3, as2)),(3**v2 % p)))
    print("{} -> {} ** {} = {} [{}]".format(v1,s1,3,f.open(f.proto7_pri_exp_pub(s1, 3,ideal=False))
            ,(v1**3 % p)))
    print("{} -> {} ** {} = {} [{}]".format(v2,s2,5,f.open(f.proto7_pri_exp_pub(s2, 5,ideal=False))
            ,(v2**5 % p)))


    tv = lambda x: "({},{})".format(x[0],f.open(x[1]))
    print("\n\n>> Proto5 (Ideal Exp) Base ** Exp = ({0,1},Value) [Manual Check]")
    print("{} ** {} -> {} = {} [{}]".format(2,v1,s1,tv(f.proto5_pub_exp_pri(2, s1)),(2**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v1,s1,tv(f.proto5_pub_exp_pri(3, s1)),(3**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v2,s2,tv(f.proto5_pub_exp_pri(3, s2)),(3**v2 % p)))
    print("{} ** {} -> {} = {} [{}]".format(5,v2,s2,tv(f.proto5_pub_exp_pri(5, s2)),(5**v2 % p)))

    print("\n\n>> Proto5 (Proto4) Base ** Exp = ({0,1},Value) [Manual Check]")
    print("{} ** {} -> {} = {} [{}]".format(2,v1,s1,tv(f.proto5_pub_exp_pri(2, s1,ideal=False)),(2**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v1,s1,tv(f.proto5_pub_exp_pri(3, s1,ideal=False)),(3**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v2,s2,tv(f.proto5_pub_exp_pri(3, s2,ideal=False)),(3**v2 % p)))
    print("{} ** {} -> {} = {} [{}]".format(5,v2,s2,tv(f.proto5_pub_exp_pri(5, s2,ideal=False)),(5**v2 % p)))

    print("\n\n>> Proto6 (Ideal Exp) Base ** Exp = ({0,1},Value) [Manual Check]")
    print("{} ** {} -> {} = {} [{}]".format(2,v1,s1,tv(f.proto6_pub_exp_pri(2, s1)),(2**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v1,s1,tv(f.proto6_pub_exp_pri(3, s1)),(3**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v2,s2,tv(f.proto6_pub_exp_pri(3, s2)),(3**v2 % p)))
    print("{} ** {} -> {} = {} [{}]".format(5,v2,s2,tv(f.proto6_pub_exp_pri(5, s2)),(5**v2 % p)))

    print("\n\n>> Proto6 (Proto4) Base ** Exp = ({0,1},Value) [Manual Check]")
    print("{} ** {} -> {} = {} [{}]".format(2,v1,s1,tv(f.proto6_pub_exp_pri(2, s1,ideal=False)),(2**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v1,s1,tv(f.proto6_pub_exp_pri(3, s1,ideal=False)),(3**v1 % p)))
    print("{} ** {} -> {} = {} [{}]".format(3,v2,s2,tv(f.proto6_pub_exp_pri(3, s2,ideal=False)),(3**v2 % p)))
    print("{} ** {} -> {} = {} [{}]".format(5,v2,s2,tv(f.proto6_pub_exp_pri(5, s2,ideal=False)),(5**v2 % p)))
    
    delta = randrange(2,p-2)
    print("\n\n>> Attack Proto6 (Delta) Base ** Exp -> Shares = ({0,1},AttValue), (1,CorrectValue)")
    f.parties[0].corrupt(delta)
    print("({}) {} ** {} -> {} = {} != {}".format(delta,2,v1,s1,
        tv(f.proto6_pub_exp_pri_att(2, s1)), tv(f.proto6_pub_exp_pri(2, s1))))
    
    

if __name__ == "__main__":
    main()