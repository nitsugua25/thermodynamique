# FRIGO / PAC  (Casio)
# LAISSER VIDE = passer

def d(t):
    s = input(t)
    if s == "":
        return None
    return float(s)

def q(expl, tag):
    print(expl)
    return d(tag)

def p(n, v):
    print(n + " = " + str(round(v, 3)))

print("=== FRIGO / PAC ===")
print("enthalpies h en kJ/kg")

print("")
print("--- LES 4 POINTS (h) ---")
h1 = q("h1 sortie evaporateur", "h1= ")
h3 = q("h3 sortie condenseur", "h3= ")
h2 = q("h2 reel sortie compress", "h2= ")
if h2 is None:
    h2s = q("h2 isentropique", "h2s= ")
    ei = q("rendement isentropique", "eis= ")
    h2 = h1 + (h2s - h1) / ei
    p("h2 calcule", h2)
h4 = h3

w = h2 - h1
q1 = h3 - h2
q2 = h1 - h4

print("")
print("--- PAR KG DE FLUIDE ---")
p("w", w)
p("q1", q1)
p("q2", q2)
p("somme (verif=0)", q1 + q2 + w)
p("PSN", q2 / w)
p("COP", -q1 / w)

print("")
print("--- CARNOT (bornes theoriques) ---")
tf = q("temperature froide C si connue", "Tfroid= ")
if tf is not None:
    tc = q("temperature chaude C", "Tchaud= ")
    t2 = tf + 273.15
    t1 = tc + 273.15
    p("PSNmax", t2 / (t1 - t2))
    p("COPmax", t1 / (t1 - t2))

print("")
print("--- DEBITS ---")
pu = q("puissance utile Putile kW", "Putile= ")
if pu is not None:
    print("frigo ou PAC ?")
    m = input("1=frigo 2=pac : ")
    if m == "1":
        qu = q2
    else:
        qu = -q1
    md = pu / qu
    p("mdot kg/s", md)
    p("Pcomp kW", md * w)
    if m == "1":
        p("Pcond kW", pu + md * w)
    else:
        p("Pevap kW", pu - md * w)
    ce = q("c du secondaire J/kgK si connu", "csec= ")
    if ce is not None:
        dt = q("delta T secondaire C", "dT= ")
        p("mdot2 kg/s", pu * 1000 / (ce * dt))

print("")
print("=== FIN ===")
