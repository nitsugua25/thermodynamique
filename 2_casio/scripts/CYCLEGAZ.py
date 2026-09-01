# CYCLE GAZ / TURBINE  (Casio)
# machines ouvertes enchainees
# Joule, turbine a gaz...
# ENTREE vide = passer

def d(t):
    s = input(t)
    if s == "":
        return None
    return float(s)

def p(n, v):
    print(n + "=" + str(round(v, 2)))

print("CYCLE GAZ")
cp = d("cp J/kgK=")
g = d("gamma=")
md = d("debit kg/s=")
if md is None:
    md = 0.0
t = d("T1 C=") + 273.15
pr = d("p1 (bar/atm)=")

wt = 0.0
qi = 0.0
qt = 0.0
i = 1
print("etat 1:")
p("T K", t)
p("p", pr)

while True:
    print("--etape--")
    print("1adiab 2isob")
    c = input("3=fin:")
    if c == "3":
        break
    if c == "1":
        print("1rap p 2W impose")
        s = input(":")
        if s == "1":
            p2 = d("p fin=")
            t2 = t * (p2 / pr) ** ((g - 1) / g)
        else:
            w = d("w J/kg=")
            t2 = t + w / cp
            p2 = pr * (t2 / t) ** (g / (g - 1))
        w = cp * (t2 - t)
        wt = wt + w
        p("w J/kg", w)
    else:
        t2 = d("T fin C=") + 273.15
        p2 = pr
        q = cp * (t2 - t)
        qt = qt + q
        if q > 0:
            qi = qi + q
        p("q J/kg", q)
    t = t2
    pr = p2
    i = i + 1
    print("etat " + str(i) + ":")
    p("T K", t)
    p("p", pr)

print("--bilan--")
p("Wnet J/kg", wt)
p("Qfourni J/kg", qi)
p("Qtot J/kg", qt)
if qi > 0:
    p("eta %", abs(wt) / qi * 100)
if md > 0:
    p("Pnet kW", md * wt / 1000)
    p("Pth kW", md * qi / 1000)
print("FIN")
