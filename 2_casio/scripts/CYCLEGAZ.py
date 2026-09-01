# CYCLE GAZ / TURBINE  (Casio)
# machines ouvertes enchainees
# Joule, turbine a gaz...
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
    print(n + " = " + str(round(v, 2)))

print("=== CYCLE GAZ / TURBINE ===")
print("machines ouvertes enchainees")

print("")
print("--- DONNEES GAZ ---")
cp = q("capacite thermique cp J/kgK", "cp= ")
g = q("gamma", "gamma= ")
md = q("debit kg/s si connu", "debit= ")
if md is None:
    md = 0.0
t = q("temperature depart T1 C", "T1= ") + 273.15
pr = q("pression depart p1 bar/atm", "p1= ")

wt = 0.0
qi = 0.0
qt = 0.0
i = 1
print("")
print("etat 1 :")
p("T K", t)
p("p", pr)

while True:
    print("")
    print("--- ETAPE SUIVANTE ---")
    print("adiabatique, isobare ou fin ?")
    c = input("1=adia 2=isob 3=fin : ")
    if c == "3":
        break
    if c == "1":
        print("rapport de pression ou W impose ?")
        s = input("1=rapp p 2=W : ")
        if s == "1":
            p2 = q("pression finale", "pfin= ")
            t2 = t * (p2 / pr) ** ((g - 1) / g)
        else:
            w = q("travail w en J/kg", "w= ")
            t2 = t + w / cp
            p2 = pr * (t2 / t) ** (g / (g - 1))
        w = cp * (t2 - t)
        wt = wt + w
        p("w J/kg", w)
    else:
        t2 = q("temperature finale C", "Tfin= ") + 273.15
        p2 = pr
        qe = cp * (t2 - t)
        qt = qt + qe
        if qe > 0:
            qi = qi + qe
        p("q J/kg", qe)
    t = t2
    pr = p2
    i = i + 1
    print("")
    print("etat " + str(i) + " :")
    p("T K", t)
    p("p", pr)

print("")
print("--- BILAN ---")
p("Wnet J/kg", wt)
p("Qfourni J/kg", qi)
p("Qtot J/kg", qt)
if qi > 0:
    p("eta %", abs(wt) / qi * 100)
if md > 0:
    p("Pnet kW", md * wt / 1000)
    p("Pth kW", md * qi / 1000)

print("")
print("=== FIN ===")
