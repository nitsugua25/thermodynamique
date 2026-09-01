# MOTEUR 4 TEMPS  (Casio)
# essence ou diesel
# ENTREE vide = passer

R = 8.314

def d(t):
    s = input(t)
    if s == "":
        return None
    return float(s)

def p(n, v):
    print(n + "=" + str(round(v, 2)))

ty = input("1ess 2die:")
tp = input("1=4tps 2=2tps:")
if tp == "2":
    kt = 60.0
else:
    kt = 120.0
ep = d("eps=")
g = d("gamma=")
tb = d("Tadm C=") + 273.15
pb = d("padm bar=") * 100000
cy = d("cyl tot L=")
z = d("nb cyl=")

cv = R / (g - 1)
cp = g * cv

# volumes (m3, par cylindre)
cu = cy / z / 1000.0
va = cu / (ep - 1)
vb = va * ep
n = pb * vb / (R * tb)

# point C : compression adiab
tc = tb * ep ** (g - 1)
pc = pb * ep ** g

print("--pts--")
p("VA cm3", va * 1e6)
p("VB cm3", vb * 1e6)
p("n mol", n)
p("TB K", tb)
p("TC K", tc)
p("pC bar", pc / 100000)

# point D : combustion
print("--comb--")
q = d("QCD J=")
if q is None:
    r = None
    if ty == "2":
        r = d("rho=")
    if r is not None:
        td = tc * r
        if ty == "2":
            q = n * cp * (td - tc)
        else:
            q = n * cv * (td - tc)
    else:
        pci = d("PCI kJ/kg=")
        x = d("x de CxHy=")
        y = d("y de CxHy=")
        la = d("lambda=")
        ar = la * (x + y / 4) / 0.21
        nc = n / (1 + ar)
        mc = nc * (12 * x + y) / 1000.0
        q = mc * pci * 1000
        p("air/carb mol", ar)
        p("mcarb mg", mc * 1e6)
        p("QCD J", q)

if ty == "2":
    td = tc + q / (n * cp)
    r = td / tc
    vd = va * r
    pd = pc
else:
    td = tc + q / (n * cv)
    r = 1.0
    vd = va
    pd = pc * td / tc

# point E : detente adiab jusqu a VB
te = td * (vd / vb) ** (g - 1)
pe = n * R * te / vb

p("TD K", td)
p("pD bar", pd / 100000)
if ty == "2":
    p("rho", r)
p("TE K", te)
p("pE bar", pe / 100000)

# rendement theorique
if ty == "2":
    et = 1 + (ep ** (1 - g) - ep ** (1 - g) * r ** g) / (g * (r - 1))
else:
    et = 1 - ep ** (1 - g)

print("--W et Q--")
wbc = n * cv * (tc - tb)
if ty == "2":
    wcd = -pc * (vd - va)
else:
    wcd = 0.0
wde = n * cv * (te - td)
qeb = n * cv * (tb - te)
p("Wbc J", wbc)
p("Wcd J", wcd)
p("Wde J", wde)
p("Qcd J", q)
p("Qeb J", qeb)
p("Wcyc J", wbc + wcd + wde)

print("--rend--")
p("eta th %", et * 100)
wt = et * q
p("Wth J", wt)

ef = d("rend forme=")
if ef is None:
    ef = 1.0
em = d("rend meca=")
if em is None:
    em = 1.0
wi = ef * wt
wd = em * wi
p("Wind J", wi)
p("Wdisp J", wd)
p("eta eff %", et * ef * em * 100)

print("--puiss--")
nn = d("N tr/min=")
if nn is not None:
    p("Pth kW", nn / kt * wt * z / 1000)
    p("Peff kW", nn / kt * wd * z / 1000)
else:
    pe2 = d("Peff kW=")
    if pe2 is not None:
        p("N tr/min", abs(pe2) * 1000 * kt / (wd * z))

print("FIN")
