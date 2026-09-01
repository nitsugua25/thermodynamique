# ECHANGE THERMIQUE (Casio)
# mcdT, latente, melange
# ENTREE vide = passer

def d(t):
    s = input(t)
    if s == "":
        return None
    return float(s)

def p(n, v):
    print(n + "=" + str(round(v, 3)))

print("ECH THERMIQUE")
print("1 Q=mcdT")
print("2 Q=mL")
print("3 melange Tf")
c = input("4 debit:")

if c == "1":
    m = d("m kg=")
    ce = d("c J/kgK=")
    t1 = d("Ti C=")
    t2 = d("Tf C=")
    q = m * ce * (t2 - t1)
    p("Q J", q)
    p("Q kJ", q / 1000)

elif c == "2":
    m = d("m kg=")
    l = d("L J/kg=")
    q = m * l
    p("Q J", q)
    p("Q kJ", q / 1000)

elif c == "3":
    m1 = d("m1 kg=")
    c1 = d("c1 J/kgK=")
    t1 = d("T1 C=")
    m2 = d("m2 kg=")
    c2 = d("c2 J/kgK=")
    t2 = d("T2 C=")
    tf = (m1 * c1 * t1 + m2 * c2 * t2) / (m1 * c1 + m2 * c2)
    p("Tf C", tf)
    p("Q1 J", m1 * c1 * (tf - t1))
    p("Q2 J", m2 * c2 * (tf - t2))

else:
    print("P=mdot*c*dT")
    pu = d("P kW=")
    md = d("mdot kg/s=")
    ce = d("c J/kgK=")
    dt = d("dT C=")
    if pu is None:
        p("P kW", md * ce * dt / 1000)
    elif md is None:
        p("mdot kg/s", pu * 1000 / (ce * dt))
        p("mdot m3/h eau", pu * 1000 / (ce * dt) * 3.6)
    else:
        p("dT C", pu * 1000 / (md * ce))

print("FIN")
