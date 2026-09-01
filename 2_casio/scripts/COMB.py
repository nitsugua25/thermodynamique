# COMBUSTION CxHy (Casio)
# air, exces d air, chaleur
# ENTREE vide = passer

def d(t):
    s = input(t)
    if s == "":
        return None
    return float(s)

def p(n, v):
    print(n + "=" + str(round(v, 3)))

print("COMBUSTION")
print("CxHy + O2")
x = d("x=")
y = d("y=")
la = d("lambda=")
if la is None:
    la = 1.0

no = x + y / 4
na = no / 0.21
nar = na * la
mm = 12 * x + y

print("--par mol carb--")
p("nO2 stoe", no)
p("nair stoe", na)
p("nair reel", nar)
p("nCO2", x)
p("nH2O", y / 2)
p("M carb g/mol", mm)
p("AF masse", nar * 28.9 / mm)

print("--quantites--")
mc = d("m carb kg=")
if mc is None:
    nc = d("n carb mol=")
else:
    nc = mc * 1000 / mm
if nc is not None:
    p("n carb mol", nc)
    p("m carb g", nc * mm)
    p("n air mol", nc * nar)
    p("m air kg", nc * nar * 28.9 / 1000)
    p("n O2 mol", nc * no * la)
    pci = d("PCI kJ/kg=")
    if pci is not None:
        p("Q J", nc * mm / 1000 * pci * 1000)

print("FIN")
