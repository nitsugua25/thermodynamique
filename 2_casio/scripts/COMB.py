# COMBUSTION CxHy (Casio)
# air, exces d air, chaleur
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

print("=== COMBUSTION CxHy ===")
print("reaction : CxHy + O2 -> CO2+H2O")

print("")
print("--- CARBURANT ---")
x = q("nombre de carbone x", "x= ")
y = q("nombre d hydrogene y", "y= ")
la = q("exces d air lambda (vide=1)", "lambda= ")
if la is None:
    la = 1.0

no = x + y / 4
na = no / 0.21
nar = na * la
mm = 12 * x + y

print("")
print("--- PAR MOLE DE CARBURANT ---")
p("nO2 stoe", no)
p("nair stoe", na)
p("nair reel", nar)
p("nCO2", x)
p("nH2O", y / 2)
p("M carb g/mol", mm)
p("AF masse", nar * 28.9 / mm)

print("")
print("--- QUANTITES ---")
mc = q("masse carburant kg", "mcarb= ")
if mc is None:
    nc = q("ou moles carburant mol", "ncarb= ")
else:
    nc = mc * 1000 / mm
if nc is not None:
    p("n carb mol", nc)
    p("m carb g", nc * mm)
    p("n air mol", nc * nar)
    p("m air kg", nc * nar * 28.9 / 1000)
    p("n O2 mol", nc * no * la)
    pci = q("PCI carburant kJ/kg", "PCI= ")
    if pci is not None:
        p("Q J", nc * mm / 1000 * pci * 1000)

print("")
print("=== FIN ===")
