# Main showcase of the protocol

from random import randrange
from group import ModuloGroup as MP
from group import EllipticGroup as EC
from user import User
from server import Server
from tqdm import tqdm

p = 101
q = 1009
a = 1
b = 1
tests = 10000

def main():
    
    print(">>>> Beware, this is a Proof of Concept")
    print(">>>> Warning will be displayed with [!!!]\n")

    print(">> Initializing the Chaum-Pedersen ∑-protocol for ModuloGroup")
    print("p prime: {}\n".format(p))

    G = MP(p)

    print(">> Initializing a User and Server")
    u = User()
    s = Server(G)

    
    print("[U -> S] Request connection")
    
    cps = s.reqConnect()
    print("[U <- S] Provides ∑-protocol public parameters : {}".format(cps))
    
    u.connect(cps)
    print("[U] Stores ∑-protocol public parameters")

    
    x = randrange(2,cps.G.p-1)
    u.setSecret(x)
    print("[U] Selects secret input x: {}".format(x))
    
    
    (name,yi) = u.register()
    print("[U -> S] Request registration: {}".format((name,yi)))
    s.register(name,yi)
    print("[S] Stores registration information on DB")

    (name, ri) = u.reqAuth()
    print("[U -> S] Request authentication: {}".format((name,ri)))
    c = s.reqAuth(name,ri)
    print("[U <- S] Creates challenge: {}".format(c))
    
    ss = u.repAuth(c)
    print("[U -> S] Answers challenge: {}".format(ss))
    v = s.verAuth(ss)
    print("[S] Checks answer and authenticate: {}".format(v))
    
    fails = tests 
    for i in tqdm(range(tests),desc = "MG tests",leave=False):
        x = randrange(2,cps.G.p-1)
        u.setSecret(x)
        (name,yi) = u.register()
        s.register(name,yi)
        (name, ri) = u.reqAuth()
        c = s.reqAuth(name,ri)
        ss = u.repAuth(c)
        v = s.verAuth(ss)
        fails = fails - v
    
    print("\n>> Failed auth: {} / {}".format(fails,tests))
    
    # ------------------------
    print("\n\n")
    # ------------------------
    
    print(">> Initializing the Chaum-Pedersen ∑-protocol for EllipticCurve group")
    print("q prime: {}\n".format(q))

    G = EC(a,b,q)
    
    print(">> Initializing a User and Server")
    u = User()
    s = Server(G)

    print("[U -> S] Request connection")
    
    cps = s.reqConnect()
    print("[U <- S] Provides ∑-protocol public parameters : {}".format(cps))
    print("EC: g = {} , h = {} , p = {}".format(cps.G.gg,cps.G.hh,cps.G.p))
    
    u.connect(cps)
    print("[U] Stores ∑-protocol public parameters")

    
    x = randrange(2,cps.G.p-1)
    u.setSecret(x)
    print("[U] Selects secret input x: {}".format(x))
    
    
    (name,yi) = u.register()
    print("[U -> S] Request registration: {}".format((name,yi)))
    s.register(name,yi)
    print("[S] Stores registration information on DB")

    (name, ri) = u.reqAuth()
    print("[U -> S] Request authentication: {}".format((name,ri)))
    c = s.reqAuth(name,ri)
    print("[U <- S] Creates challenge: {}".format(c))
    
    ss = u.repAuth(c)
    print("[U -> S] Answers challenge: {}".format(ss))
    v = s.verAuth(ss)
    print("[S] Checks answer and authenticate: {}".format(v))

    fails = tests 
    for i in tqdm(range(tests),desc = "MG tests",leave=False):
        x = randrange(2,cps.G.p-1)
        u.setSecret(x)
        (name,yi) = u.register()
        s.register(name,yi)
        (name, ri) = u.reqAuth()
        c = s.reqAuth(name,ri)
        ss = u.repAuth(c)
        v = s.verAuth(ss)
        if v==0:
            print("{} {} {}".format(x,ss,c))
        fails = fails - v
    
    print("\n>> Failed auth: {} / {}".format(fails,tests))


if __name__ == "__main__":
    main()