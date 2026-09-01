# ECHANGE THERMIQUE (Casio)
# mcdT, latente, melange, debit
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

print("=== ECHANGE THERMIQUE ===")
print("choisir le type de calcul :")
print("1=Q=mcdT   2=Q=mL")
print("3=melange  4=debit")
c = input("1, 2, 3 ou 4 : ")

if c == "1":
    print("")
    print("--- Q = m.c.dT ---")
    m = q("masse m kg", "m= ")
    ce = q("capacite c J/kgK", "c= ")
    t1 = q("temperature initiale C", "Ti= ")
    t2 = q("temperature finale C", "Tf= ")
    qc = m * ce * (t2 - t1)
    p("Q J", qc)
    p("Q kJ", qc / 1000)

elif c == "2":
    print("")
    print("--- Q = m.L (changement d etat) ---")
    m = q("masse m kg", "m= ")
    l = q("chaleur latente L J/kg", "L= ")
    qc = m * l
    p("Q J", qc)
    p("Q kJ", qc / 1000)

elif c == "3":
    print("")
    print("--- MELANGE : temperature finale ---")
    m1 = q("masse 1 kg", "m1= ")
    c1 = q("capacite 1 J/kgK", "c1= ")
    t1 = q("temperature 1 C", "T1= ")
    m2 = q("masse 2 kg", "m2= ")
    c2 = q("capacite 2 J/kgK", "c2= ")
    t2 = q("temperature 2 C", "T2= ")
    tf = (m1 * c1 * t1 + m2 * c2 * t2) / (m1 * c1 + m2 * c2)
    p("Tf C", tf)
    p("Q1 J", m1 * c1 * (tf - t1))
    p("Q2 J", m2 * c2 * (tf - t2))

else:
    print("")
    print("--- CIRCUIT A DEBIT : P=mdot.c.dT ---")
    pu = q("puissance P kW si connue", "P= ")
    md = q("debit mdot kg/s si connu", "mdot= ")
    ce = q("capacite c J/kgK", "c= ")
    dt = q("ecart de temperature dT C", "dT= ")
    if pu is None:
        p("P kW", md * ce * dt / 1000)
    elif md is None:
        p("mdot kg/s", pu * 1000 / (ce * dt))
        p("mdot m3/h eau", pu * 1000 / (ce * dt) * 3.6)
    else:
        p("dT C", pu * 1000 / (md * ce))

print("")
print("=== FIN ===")
