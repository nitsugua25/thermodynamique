# MOTEUR 4 TEMPS / 2 TEMPS (Casio)
# essence ou diesel - cycle complet B-C-D-E
# LAISSER VIDE = passer la question
# chaque question est courte, l explication est juste au dessus

R = 8.314

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

print("=== MOTEUR 4 OU 2 TEMPS ===")

print("")
print("Moteur essence ou diesel ?")
ty = input("1 ou 2 : ")
print("Cycle 4 temps ou 2 temps ?")
tp = input("1 ou 2 : ")
if tp == "2":
    kt = 60.0
else:
    kt = 120.0

print("")
print("--- GEOMETRIE ---")
ep = q("taux de compression", "eps= ")
g = q("gamma (Cp/Cv)", "gamma= ")
tb = q("temperature admission C", "Tadm= ") + 273.15
pb = q("pression admission bar", "padm= ") * 100000
cy = q("cylindree TOTALE en L", "cyl= ")
z = q("nombre de cylindres", "nbcyl= ")

cv = R / (g - 1)
cp = g * cv

cu = cy / z / 1000.0
va = cu / (ep - 1)
vb = va * ep
n = pb * vb / (R * tb)

tc = tb * ep ** (g - 1)
pc = pb * ep ** g

print("")
print("--- POINT B et POINT C ---")
p("VA cm3", va * 1e6)
p("VB cm3", vb * 1e6)
p("n mol", n)
p("TB K", tb)
p("TC K", tc)
p("pC bar", pc / 100000)

print("")
print("--- COMBUSTION : POINT D ---")
q1 = q("QCD en Joules si connu", "QCD= ")
if q1 is None:
    r = None
    if ty == "2":
        r = q("rapport de combustion", "rho= ")
    if r is not None:
        td = tc * r
        if ty == "2":
            q1 = n * cp * (td - tc)
        else:
            q1 = n * cv * (td - tc)
    else:
        print("calcul de QCD via le carburant :")
        pci = q("PCI carburant kJ/kg", "PCI= ")
        x = q("x du CxHy", "x= ")
        y = q("y du CxHy", "y= ")
        la = q("exces d air lambda", "lambda= ")
        ar = la * (x + y / 4) / 0.21
        nc = n / (1 + ar)
        mc = nc * (12 * x + y) / 1000.0
        q1 = mc * pci * 1000
        p("air/carb mol", ar)
        p("mcarb mg", mc * 1e6)
        p("QCD J", q1)

if ty == "2":
    td = tc + q1 / (n * cp)
    r = td / tc
    vd = va * r
    pd = pc
else:
    td = tc + q1 / (n * cv)
    r = 1.0
    vd = va
    pd = pc * td / tc

p("TD K", td)
p("pD bar", pd / 100000)
if ty == "2":
    p("rho", r)

print("")
print("--- POINT E ---")
te = td * (vd / vb) ** (g - 1)
pe = n * R * te / vb
p("TE K", te)
p("pE bar", pe / 100000)

if ty == "2":
    et = 1 + (ep ** (1 - g) - ep ** (1 - g) * r ** g) / (g * (r - 1))
else:
    et = 1 - ep ** (1 - g)

print("")
print("--- W et Q par cycle/cylindre ---")
wbc = n * cv * (tc - tb)
if ty == "2":
    wcd = -pc * (vd - va)
else:
    wcd = 0.0
wde = n * cv * (te - td)
qeb = n * cv * (tb - te)
p("W BC J", wbc)
p("W CD J", wcd)
p("Q CD J", q1)
p("W DE J", wde)
p("Q EB J", qeb)
p("W total J", wbc + wcd + wde)

print("")
print("--- RENDEMENT THEORIQUE ---")
p("eta th %", et * 100)
wt = et * q1
p("Wth J", wt)

print("")
print("--- RENDEMENT REEL ---")
ef = q("rendement de forme 0-1", "ef= ")
if ef is None:
    ef = 1.0
em = q("rendement mecanique 0-1", "em= ")
if em is None:
    em = 1.0
wi = ef * wt
wd = em * wi
p("Windique J", wi)
p("Wdispo J", wd)
p("eta eff %", et * ef * em * 100)

print("")
print("--- PUISSANCE / VITESSE ---")
nn = q("vitesse N tr/min si connue", "N= ")
if nn is not None:
    p("Pth kW", nn / kt * wt * z / 1000)
    p("Peff kW", nn / kt * wd * z / 1000)
else:
    pe2 = q("Peff kW si connue", "Peff= ")
    if pe2 is not None:
        p("N tr/min", abs(pe2) * 1000 * kt / (wd * z))

print("")
print("=== FIN ===")
