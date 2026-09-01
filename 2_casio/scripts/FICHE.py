# ==============================
# FICHE - Formulaire MECATHERMO
# Transformations, moteurs, frigo
# Affichage ecran (casioplot)
# Casio fx-CG50
# ==============================
from casioplot import *

NO = (0, 0, 0)
RG = (190, 0, 0)
BL = (0, 0, 150)
VE = (0, 110, 0)

# "#" = titre rouge   "=" = vert   "!" = bleu   sinon noir
PG = [
("1. BASES ET CONVENTIONS", [
 "#UNITES SI",
 "energie J   puissance W = J/s",
 "pression Pa (1 bar = 1e5 Pa)",
 "volume m3 (1 L = 1e-3 m3)   T en K",
 "#SIGNES",
 "energie RECUE par le systeme : +",
 "energie CEDEE par le systeme : -",
 "cycle moteur   : W < 0 (il fournit)",
 "cycle recepteur: W > 0 (frigo, PAC)",
 "#GAZ PARFAIT",
 "pV = nRT     R = 8.314 J/mol.K",
 "Cv = R/(g-1)      Cp = g.Cv",
 "Cp - Cv = R       Cp/Cv = g",
 "=g=1.4 : Cv=20.785  Cp=29.099",
]),
("2. 1er PRINCIPE", [
 "#SYSTEME FERME (gaz enferme)",
 "dU = W + Q       dU = n.Cv.dT",
 "W = - integrale p dV",
 "#SYSTEME OUVERT (fluide traverse)",
 "dH = Wut + Q     dH = n.Cp.dT",
 "Wut = integrale V dp",
 "!Compresseur, turbine, echangeur,",
 "!soupape -> OUVERT -> H et Cp",
 "#CYCLE (transfo fermee)",
 "dU = 0  donc  somme W + somme Q = 0",
 "=VERIFICATION la plus puissante",
 "#SECOND PRINCIPE",
 "Q1/T1 + Q2/T2 <= 0",
 "reversible : = 0   irrev : < 0",
]),
("3. LES 4 TRANSFORMATIONS", [
 "#ISOBARE p = cste",
 "V1/T1 = V2/T2",
 "W = -p.dV      Q = dH = n.Cp.dT",
 "#ISOCHORE V = cste",
 "p1/T1 = p2/T2",
 "W = 0          Q = dU = n.Cv.dT",
 "#ISOTHERME T = cste",
 "p1.V1 = p2.V2      dU = 0",
 "W = -nRT.ln(V2/V1) = -Q",
 "#ADIABATIQUE REVERSIBLE",
 "T.V^(g-1) = cste",
 "p.V^g = cste",
 "T^g.p^(1-g) = cste",
 "Q = 0          W = dU = n.Cv.dT",
 "#ENTROPIE (transfo reversible)",
 "isobare  : dS = n.Cp.ln(T2/T1)",
 "isochore : dS = n.Cv.ln(T2/T1)",
 "isotherme: dS = n.R.ln(V2/V1)",
 "adiabatique rev : dS = 0",
 "=sur un cycle : dS = 0",
]),
("4. MOTEUR ESSENCE (4 temps)", [
 "#GEOMETRIE",
 "eps = VB/VA = VB/VC   (8 a 10)",
 "cyl unitaire = VB - VA",
 "VA = cyl/(eps-1)      VB = eps.VA",
 "VC = VD = VA          VE = VB",
 "#POINTS",
 "n = pB.VB/(R.TB)",
 "TC = TB.eps^(g-1)   pC = pB.eps^g",
 "isochore C-D : TD = TC + QCD/(n.Cv)",
 "  pD = pC.TD/TC",
 "TE = TD.eps^(1-g)   pE = nRTE/VB",
 "#RENDEMENT",
 "eta_th = 1 - eps^(1-g)",
 "=verif : eta = |Wcycle|/QCD",
]),
("5. MOTEUR DIESEL (4 temps)", [
 "#DIFFERENCES AVEC ESSENCE",
 "eps plus grand (16 a 20)",
 "on admet de l AIR SEUL",
 "auto-inflammation (pas de bougie)",
 "combustion C-D ISOBARE (pas isochore)",
 "#RAPPORT DE COMBUSTION",
 "rho = VD/VC        VD = rho.VA",
 "TD = rho.TC        pD = pC",
 "QCD = n.Cp.(TD-TC)   <- Cp !",
 "detente : VD/VE = rho/eps",
 "TE = TD.(rho/eps)^(g-1)",
 "#RENDEMENT",
 "eta = 1 + (e - e.rho^g)/(g.(rho-1))",
 "=avec e = eps^(1-g)",
]),
("6. COMBUSTION - EXCES D AIR", [
 "#REACTION",
 "CxHy + (x+y/4) O2",
 "     -> x CO2 + (y/2) H2O",
 "#AIR (21% O2, M = 28.9 g/mol)",
 "n_air_stoe = (x+y/4)/0.21",
 "n_air_reel = lambda . n_air_stoe",
 "lambda = air reel / air stoe",
 "#DANS LE CYLINDRE (air+carburant)",
 "n_carb = n/(n_air_reel + 1)",
 "M = 12x + y  (g/mol)",
 "m_carb = n_carb.M/1000  (kg)",
 "QCD = m_carb . PCI",
 "!PCI en kJ/kg -> x1000 pour des J",
 "=PCI < PCS (eau vaporisee)",
]),
("7. PUISSANCE ET RENDEMENTS", [
 "#CASCADE DES PERTES",
 "|Wth|  = eta_th . QCD",
 "|Wind| = eta_forme . |Wth|",
 "|Wdisp|= eta_meca . |Wind|",
 "eta_eff = eta_th.eta_f.eta_meca",
 "        = |Wdisp|/QCD",
 "#PUISSANCE (W par cycle par cylindre)",
 "4 temps : P = (N/120).W.z",
 "2 temps : P = (N/60).W.z",
 "!2 temps : 1 tour = 1 cycle",
 "N en tr/min, z = nb cylindres",
 "inverse : N = P.120/(|Wdisp|.z)",
 "#PRESSION MOYENNE INDIQUEE",
 "Wreel = pmi.(VB-VA)  pmi = pM-patm",
]),
("8. FRIGO / PAC", [
 "#LE CYCLE (4 organes)",
 "1-2 compresseur : isentropique",
 "2-3 condenseur  : isobare, q1 < 0",
 "3-4 detendeur   : h4 = h3",
 "4-1 evaporateur : isobare, q2 > 0",
 "#PAR KG DE FLUIDE",
 "w  = h2 - h1   (> 0)",
 "q1 = h3 - h2   (< 0, au chaud)",
 "q2 = h1 - h4   (> 0, au froid)",
 "=verif : q1 + q2 + w = 0",
 "#COMPRESSEUR REEL",
 "eta_is = (h2s-h1)/(h2-h1)",
 "h2 = h1 + (h2s-h1)/eta_is",
 "!surchauffe 5C en 1, sous-refr. en 3",
]),
("9. PSN, COP, CARNOT", [
 "#PERFORMANCES",
 "FRIGO : utile = pris au froid",
 "  PSN = q2/w = (h1-h4)/(h2-h1)",
 "PAC   : utile = cede au chaud",
 "  COP = -q1/w = (h2-h3)/(h2-h1)",
 "=COP = PSN + 1",
 "#BORNES (T des SOURCES, en K)",
 "PSN_max = T2/(T1-T2)",
 "COP_max = T1/(T1-T2)",
 "eta_Carnot = 1 - T2/T1  (moteur)",
 "!T1 = chaude, T2 = froide",
 "#DEBITS",
 "mdot = P_utile/|q_utile|",
 "Pcomp = mdot.w   Pcond = Pev + Pcomp",
]),
("10. TURBINE A GAZ (JOULE)", [
 "#MACHINES OUVERTES : par kg, cp",
 "adiabatique : q = 0",
 "  T2 = T1.(p2/p1)^((g-1)/g)",
 "  w = cp.(T2-T1)",
 "isobare : wut = 0",
 "  q = cp.(T2-T1)",
 "#TURBINE QUI ENTRAINE LE COMPR.",
 "|w_turb| = |w_comp|",
 "donc T3 - T4 = T2 - T1",
 "#BILAN",
 "Wnet = somme des w",
 "eta = |Wnet| / somme des q>0",
 "P = mdot . Wnet",
 "=Joule simple: eta = 1-rp^(-(g-1)/g)",
]),
("11. ECHANGE THERMIQUE", [
 "#SANS CHANGEMENT D ETAT",
 "Q = m.c.dT",
 "P = mdot.c.dT   (circuit a debit)",
 "c_eau = 4185 J/kg.K",
 "#CHANGEMENT D ETAT",
 "Q = m.L   (a T constante)",
 "#MELANGE A L EQUILIBRE",
 "Tf = (m1c1T1+m2c2T2)/(m1c1+m2c2)",
 "#LIEN AVEC LE CYCLE FRIGO",
 "meme PUISSANCE des 2 cotes",
 "de l echangeur :",
 "mdot_fluide.|q| = mdot_eau.c.dT",
 "!c est le 1er principe ouvert",
 "!isobare : dH = Q",
]),
("12. AVANT DE RENDRE", [
 "#LES 6 VERIFICATIONS",
 "1 toutes les T en KELVIN ?",
 "2 somme W + somme Q = 0 sur le cycle",
 "3 signe : moteur W<0, frigo/PAC W>0",
 "4 eta < eta_Carnot ? COP < COP_max ?",
 "5 les 2 chemins donnent le meme eta ?",
 "  formule  vs  |Wcycle|/Qfourni",
 "6 ordres de grandeur credibles ?",
 "#ORDRES DE GRANDEUR",
 "T apres combustion : 2000-4000 K",
 "p max : 25-130 bar",
 "eta moteur : 30-65 %",
 "COP d une PAC : 3-5",
 "N : 1000-6000 tr/min",
]),
]

def page(t, L):
  clear_screen()
  draw_string(2, 1, t, BL, "small")
  y = 15
  for s in L:
    c = NO
    if len(s) > 0 and s[0] == "#":
      c = RG
      s = s[1:]
    elif len(s) > 0 and s[0] == "=":
      c = VE
      s = s[1:]
    elif len(s) > 0 and s[0] == "!":
      c = BL
      s = s[1:]
    draw_string(2, y, s, c, "small")
    y = y + 10
  show_screen()

i = 0
while True:
  page(PG[i][0], PG[i][1])
  s = input("")
  if s == "0":
    break
  if s == "p" or s == "P":
    i = (i - 1) % len(PG)
  else:
    i = (i + 1) % len(PG)
