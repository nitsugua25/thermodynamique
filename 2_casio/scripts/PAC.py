# FRIGO / PAC  (Casio)
# ENTREE vide = passer

def d(t):
    s = input(t)
    if s == "":
        return None
    return float(s)

def p(n, v):
    print(n + "=" + str(round(v, 3)))

print("FRIGO/PAC")
print("h en kJ/kg")
h1 = d("h1=")
h3 = d("h3=")
h2 = d("h2 reel=")
if h2 is None:
    h2s = d("h2 isos=")
    ei = d("rend is=")
    h2 = h1 + (h2s - h1) / ei
    p("h2", h2)
h4 = h3

w = h2 - h1
q1 = h3 - h2
q2 = h1 - h4

print("--par kg--")
p("w", w)
p("q1", q1)
p("q2", q2)
p("som", q1 + q2 + w)
p("PSN", q2 / w)
p("COP", -q1 / w)

print("--Carnot--")
tf = d("Tfroide C=")
if tf is not None:
    tc = d("Tchaude C=")
    t2 = tf + 273.15
    t1 = tc + 273.15
    p("PSNmax", t2 / (t1 - t2))
    p("COPmax", t1 / (t1 - t2))

print("--debits--")
pu = d("Putile kW=")
if pu is not None:
    m = input("1frigo 2pac:")
    if m == "1":
        qu = q2
    else:
        qu = -q1
    md = pu / qu
    p("mdot kg/s", md)
    p("Pcomp kW", md * w)
    p("Pautre kW", pu - md * w)
    ce = d("c sec J/kgK=")
    if ce is not None:
        dt = d("deltaT C=")
        p("mdot2 kg/s", pu * 1000 / (ce * dt))

print("FIN")
