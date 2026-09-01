# TRANSFO GAZ PARFAIT (Casio)
# systeme ferme
# 1 transformation: p,V,T,W,Q
# ENTREE vide = inconnu

from math import log

R = 8.314

def d(t):
    s = input(t)
    if s == "":
        return None
    return float(s)

def p(n, v):
    print(n + "=" + str(round(v, 3)))

print("TRANSFO GP")
g = d("gamma=")
cv = R / (g - 1)
cp = g * cv

print("--etat 1--")
p1 = d("p1 bar=")
v1 = d("V1 L=")
t1 = d("T1 C=")
nn = d("n mol=")
if p1 is not None:
    p1 = p1 * 100000
if v1 is not None:
    v1 = v1 / 1000.0
if t1 is not None:
    t1 = t1 + 273.15

if nn is None:
    nn = p1 * v1 / (R * t1)
elif p1 is None:
    p1 = nn * R * t1 / v1
elif v1 is None:
    v1 = nn * R * t1 / p1
elif t1 is None:
    t1 = p1 * v1 / (nn * R)

p("n mol", nn)
p("p1 bar", p1 / 100000)
p("V1 L", v1 * 1000)
p("T1 K", t1)

print("--type--")
print("1isob 2isoc")
ty = input("3isoT 4adia:")

print("--etat 2--")
p2 = d("p2 bar=")
v2 = d("V2 L=")
t2 = d("T2 C=")
if p2 is not None:
    p2 = p2 * 100000
if v2 is not None:
    v2 = v2 / 1000.0
if t2 is not None:
    t2 = t2 + 273.15

if ty == "1":
    p2 = p1
    if v2 is None:
        v2 = v1 * t2 / t1
    else:
        t2 = t1 * v2 / v1
elif ty == "2":
    v2 = v1
    if p2 is None:
        p2 = p1 * t2 / t1
    else:
        t2 = t1 * p2 / p1
elif ty == "3":
    t2 = t1
    if v2 is None:
        v2 = p1 * v1 / p2
    else:
        p2 = p1 * v1 / v2
else:
    if v2 is not None:
        t2 = t1 * (v1 / v2) ** (g - 1)
        p2 = p1 * (v1 / v2) ** g
    elif p2 is not None:
        t2 = t1 * (p2 / p1) ** ((g - 1) / g)
        v2 = v1 * (p1 / p2) ** (1 / g)
    else:
        v2 = v1 * (t1 / t2) ** (1 / (g - 1))
        p2 = nn * R * t2 / v2

p("p2 bar", p2 / 100000)
p("V2 L", v2 * 1000)
p("T2 K", t2)

print("--energies--")
du = nn * cv * (t2 - t1)
dh = nn * cp * (t2 - t1)
if ty == "1":
    w = -p1 * (v2 - v1)
    q = dh
elif ty == "2":
    w = 0.0
    q = du
elif ty == "3":
    w = -nn * R * t1 * log(v2 / v1)
    q = -w
else:
    q = 0.0
    w = du
p("W J", w)
p("Q J", q)
p("dU J", du)
p("dH J", dh)
print("FIN")
