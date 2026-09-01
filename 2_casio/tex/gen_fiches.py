# -*- coding: utf-8 -*-
# Fiches DEMARCHE + SCHEMA pour Casio fx-CG50 -- Mecathermo Ma0
# 384x216 px (ecran), rendu LaTeX 400 dpi puis reduction + accentuation
# Texte en GRAS et en grande taille : lisible sur l ecran de la calculatrice
import os, subprocess, shutil, sys
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
H_IN = sys.argv[1] if len(sys.argv) > 1 else "2.16"
H_PX = 216 if H_IN == "2.16" else 192
OUT = os.path.join(HERE, "..", "images" if H_PX == 216 else "images_384x192")
TMP = os.path.join(HERE, "_tf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

PRE = r"""
\documentclass[__PT__pt]{extarticle}
\usepackage[paperwidth=3.84in,paperheight=__H__in,margin=1.6mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[french]{babel}
\usepackage{amsmath,amssymb}
\usepackage{bm}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{decorations.pathmorphing,patterns,arrows.meta,positioning,calc}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\abovedisplayskip}{1pt}\setlength{\belowdisplayskip}{1pt}
\setlength{\abovedisplayshortskip}{0pt}\setlength{\belowdisplayshortskip}{0pt}
\definecolor{acc}{HTML}{A81E12}
\definecolor{grn}{HTML}{0C5730}
\definecolor{gry}{HTML}{444444}
\definecolor{blu}{HTML}{0D2E63}
% --- tout le corps en gras, formules comprises ---
\AtBeginDocument{\bfseries\boldmath}
\newcommand{\titre}[1]{{\bfseries\large #1}\par\vspace{0.5mm}%
  {\color{acc}\hrule height 1.0pt}\vspace{1.0mm}}
\newcommand{\sect}[1]{\par\vspace{0.7mm}{\color{acc}\bfseries\small #1}\par\vspace{0.3mm}}
\newcommand{\stp}[2]{\makebox[4.2mm][l]{\color{acc}\bfseries#1}%
  \begin{minipage}[t]{0.92\linewidth}#2\end{minipage}\par\vspace{0.7mm}}
\newcommand{\ex}[1]{\par\vspace{0.7mm}{\color{grn}\hrule height 0.5pt}\vspace{0.6mm}%
  {\color{grn}\bfseries\small \textbf{ex.} #1}\par}
\newcommand{\note}[1]{\par\vspace{0.5mm}{\color{blu}\bfseries\small #1}\par}
\newcommand{\scr}[1]{\hfill{\color{gry}\bfseries\small #1}}
\tikzset{
 blk/.style={draw,line width=0.7pt,minimum width=6mm,minimum height=4mm,inner sep=1pt,font=\small\bfseries},
 sm/.style={draw,line width=0.7pt,circle,minimum size=2.6mm,inner sep=0pt},
 ar/.style={-{Latex[length=1.3mm]},line width=0.7pt}}
"""

F = {}   # nom -> corps LaTeX

# =====================  DEMARCHE  =====================

F["D01-essence-volumes-points"] = r"""
\titre{ESSENCE 1 --- volumes et points}
\stp{1}{$V_A=\dfrac{\text{cyl}/z}{\varepsilon-1}$ \qquad $V_B=\varepsilon\,V_A$}
\stp{2}{$V_C=V_D=V_A$ \qquad $V_E=V_B$}
\stp{3}{$n=\dfrac{p_B V_B}{R\,T_B}$ \quad (B $=$ air aspir\'e)}
\stp{4}{$T_C=T_B\,\varepsilon^{\gamma-1}$ \qquad $p_C=p_B\,\varepsilon^{\gamma}$}
\ex{$\varepsilon{=}10$, $16^\circ$C, 1,2\,L, 4\,cyl :
$V_A{=}33{,}3$\,cm$^3$, $T_C{=}726$\,K}
"""

F["D02-essence-combustion-rendement"] = r"""
\titre{ESSENCE 2 --- fin du cycle}
\stp{5}{Isochore C-D : $T_D=T_C+\dfrac{Q_{CD}}{n\,C_v}$}
\stp{6}{$p_D=p_C\cdot\dfrac{T_D}{T_C}$}
\stp{7}{$T_E=T_D\,\varepsilon^{1-\gamma}$ \qquad $p_E=\dfrac{nRT_E}{V_B}$}
\stp{8}{$\eta_{th}=1-\varepsilon^{1-\gamma}$}
\ex{$Q_{CD}{=}876$\,J $\to T_D{=}3765$\,K, $\eta_{th}{=}60{,}2\%$ \scr{MOTEUR}}
"""

F["D03-diesel-ce-qui-change"] = r"""
\titre{DIESEL 1 --- ce qui change}
\stp{1}{$\varepsilon$ plus grand : $16<\varepsilon<20$}
\stp{2}{On admet de l'\textbf{AIR SEUL}}
\stp{3}{Combustion C-D \textbf{ISOBARE} (pas isochore)}
\stp{4}{Nouveau : $\rho=\dfrac{V_D}{V_C}$ \; donc $V_D=\rho\,V_A$}
\note{$V_A$, $V_B$, $n$, $T_C$, $p_C$ : \textbf{identiques} \`a l'essence.}
"""

F["D04-diesel-points-rendement"] = r"""
\titre{DIESEL 2 --- points et $\eta$}
\stp{5}{$T_D=\rho\,T_C$ \qquad $p_D=p_C$}
\stp{6}{$Q_{CD}=n\,C_p\,(T_D-T_C)$ \quad ($C_p$ !)}
\stp{7}{$T_E=T_D\Big(\dfrac{\rho}{\varepsilon}\Big)^{\gamma-1}$}
\stp{8}{$\eta_{th}=1+\dfrac{\varepsilon^{1-\gamma}(1-\rho^{\gamma})}{\gamma(\rho-1)}$}
\ex{$\varepsilon{=}18$, $\rho{=}2$ : $\eta_{th}{=}63{,}2\%$ \scr{MOTEUR}}
"""

F["D05-moteur-2-temps"] = r"""
\titre{Moteur 2 TEMPS}
\note{Cycle \textbf{identique} \`a l'essence : m\^emes formules.}
\stp{1}{1 tour $=$ \textbf{1 cycle}}
\stp{2}{$P=\dfrac{N}{60}\,W\,z$ \quad \textbf{sans} le $/2$ !}
\stp{3}{\`A r\'egime \'egal : \textbf{2$\times$ plus} de puissance}
\ex{$\varepsilon{=}8{,}5$, $Q{=}95$\,J, 5000\,tr/min $\to 2{,}48$\,kW \scr{MOTEUR}}
"""

F["D06-combustion-reaction"] = r"""
\titre{COMBUSTION 1 --- l'air}
\stp{1}{$C_xH_y+\Big(x+\dfrac{y}{4}\Big)O_2\to xCO_2+\dfrac{y}{2}H_2O$}
\stp{2}{$n_{air}=\dfrac{x+y/4}{0{,}21}$ \quad (air : 21\% O$_2$)}
\stp{3}{Exc\`es d'air : $\times\lambda$}
\ex{CH$_{1,8}$, $\lambda{=}1{,}2$ : $1{,}45$ O$_2$, puis
$8{,}29$ mol air / mol carb \scr{COMB}}
"""

F["D07-combustion-chaleur"] = r"""
\titre{COMBUSTION 2 --- la chaleur}
\stp{4}{$n_{carb}=\dfrac{n}{\lambda\,n_{air}+1}$}
\note{le cylindre contient air \textbf{+} carburant}
\stp{5}{$M=12x+y$ \; $\Rightarrow$ \; $m_{carb}=\dfrac{n_{carb}M}{1000}$ kg}
\stp{6}{$\boxed{Q_{CD}=m_{carb}\cdot PCI}$}
\note{\textbf{PCI en J/kg} : kJ/kg $\times\,1000$ !}
"""

F["D08-exces-air-consequences"] = r"""
\titre{Exc\`es d'air $\lambda$ --- effets}
\stp{$<$}{$\lambda$ un peu $<1$ : production de \textbf{CO}}
\stp{$\ll$}{$\lambda$ tr\`es $<1$ : \textbf{carburant imbr\^ul\'e}}
\stp{$>$}{$\lambda>1$ \textbf{n\'ecessaire} : m\'elange jamais homog\`ene}
\stp{$\gg$}{$\lambda$ trop grand : air comprim\'e \textbf{pour rien}}
\note{Il faut trouver le bon \'equilibre.}
"""

F["D09-frigo-placer-points"] = r"""
\titre{FRIGO 1 --- placer les points}
\stp{1}{$p_{\text{\'ev}}$ et $p_{cond}$ : lire sur la cloche}
\stp{2}{\textbf{1'} : BP, \`a $T_{\text{\'ev}}+5^\circ$ \; (vapeur, droite)}
\stp{3}{\textbf{2'} : HP, via l'\textbf{isentropique} de 1'}
\stp{4}{\textbf{3'} : HP, \`a $T_{cond}-5^\circ$ \; (liquide, gauche)}
\stp{5}{\textbf{4'} : \`a la \textbf{verticale} de 3' \; ($h_4=h_3$)}
"""

F["D10-frigo-energies"] = r"""
\titre{FRIGO 2 --- les \'energies}
\stp{6}{R\'eel : $h_2=h_1+\dfrac{h_{2s}-h_1}{\eta_{isos}}$}
\stp{7}{$w=h_2-h_1>0$ \quad (compresseur)}
\stp{8}{$q_1=h_3-h_2<0$ \quad (condenseur)}
\stp{9}{$q_2=h_1-h_4>0$ \quad (\'evaporateur)}
\ex{V\'erif : $q_1+q_2+w=0$ \; toujours \scr{PAC}}
"""

F["D11-psn-cop"] = r"""
\titre{PSN ou COP ?}
\stp{F}{\textbf{FRIGO} : utile $=$ pris au \textbf{froid}}
\stp{}{$PSN=\dfrac{q_2}{w}=\dfrac{h_1-h_4}{h_2-h_1}$}
\stp{P}{\textbf{PAC} : utile $=$ c\'ed\'e au \textbf{chaud}}
\stp{}{$COP=\dfrac{-q_1}{w}=\dfrac{h_2-h_3}{h_2-h_1}$}
\note{$COP=PSN+1$ \; toujours.}
"""

F["D12-carnot-debits"] = r"""
\titre{Carnot et d\'ebits}
\stp{1}{$PSN_{max}=\dfrac{T_2}{T_1-T_2}$ \quad $COP_{max}=\dfrac{T_1}{T_1-T_2}$}
\note{$T$ des \textbf{SOURCES}, en K. $T_1$ chaude, $T_2$ froide.}
\stp{2}{$\dot m=\dfrac{P_{utile}}{|q_{utile}|}$ \qquad $P_{comp}=\dot m\,w$}
\ex{$COP{=}4{,}36$ pour $COP_{max}{=}6{,}36$ : $69\%$, cr\'edible \scr{PAC}}
"""

F["D13-turbine-joule"] = r"""
\titre{Turbine \`a gaz (Joule)}
\note{Machines \textbf{ouvertes} : par kg, avec $c_p$.}
\stp{1}{Adiab. : $T_2=T_1\Big(\dfrac{p_2}{p_1}\Big)^{\frac{\gamma-1}{\gamma}}$, $w=c_p\Delta T$}
\stp{2}{Isobare : $q=c_p\Delta T$, \; $w_{ut}=0$}
\stp{3}{$\eta=\dfrac{|W_{net}|}{\sum q_{>0}}$ \qquad $P=\dot m\,W_{net}$}
\ex{$r_p{=}8$, $900^\circ$C : $\eta{=}44{,}8\%$ \scr{CYCLEGAZ}}
"""

F["D14-turbine-astuce"] = r"""
\titre{Joule --- l'astuce du sujet}
\note{\og tout le travail de la turbine sert au compresseur \fg}
\stp{$\Rightarrow$}{$|w_{turb}|=|w_{comp}|$}
\stp{$\Rightarrow$}{$T_3-T_4=T_2-T_1$}
\stp{!}{Ce travail \textbf{ne sort pas} de la machine : il ne compte
pas dans $W_{net}$}
\ex{Joule simple : $\eta=1-r_p^{-\frac{\gamma-1}{\gamma}}$ \scr{CYCLEGAZ}}
"""

F["D15-transfo-isobare-isochore"] = r"""
\titre{TRANSFO 1 --- $p$ ou $V$ constant}
\sect{ISOBARE ($p$ cste)}
\stp{}{$\dfrac{V_1}{T_1}=\dfrac{V_2}{T_2}$ \quad $W=-p\,\Delta V$}
\stp{}{$Q=\Delta H=n\,C_p\,\Delta T$}
\sect{ISOCHORE ($V$ cste)}
\stp{}{$\dfrac{p_1}{T_1}=\dfrac{p_2}{T_2}$ \quad $W=0$}
\stp{}{$Q=\Delta U=n\,C_v\,\Delta T$}
"""

F["D16-transfo-isotherme-adiab"] = r"""
\titre{TRANSFO 2 --- $T$ cste ou $Q=0$}
\sect{ISOTHERME ($T$ cste)}
\stp{}{$p_1V_1=p_2V_2$ \qquad $\Delta U=0$}
\stp{}{$W=-nRT\ln\dfrac{V_2}{V_1}=-Q$}
\sect{ADIABATIQUE R\'EVERSIBLE}
\stp{}{$TV^{\gamma-1}=pV^{\gamma}=T^{\gamma}p^{1-\gamma}=$ cste}
\stp{}{$Q=0$ \qquad $W=\Delta U=n\,C_v\,\Delta T$}
"""

F["D17-constantes"] = r"""
\titre{Les constantes \`a poser}
\stp{1}{$C_v=\dfrac{R}{\gamma-1}$ \qquad $C_p=\gamma\,C_v$}
\stp{2}{$C_p-C_v=R$ \qquad $\dfrac{C_p}{C_v}=\gamma$}
\stp{3}{$R=8{,}314$ J/(mol$\cdot$K)}
\ex{$\gamma=1{,}4$ : $\;C_v=20{,}785$ \; et \; $C_p=29{,}099$ \; J/(mol$\cdot$K)}
"""

F["D18-entropie"] = r"""
\titre{Variation d'entropie}
\stp{P}{Isobare : $\Delta S=n\,C_p\ln\dfrac{T_2}{T_1}$}
\stp{V}{Isochore : $\Delta S=n\,C_v\ln\dfrac{T_2}{T_1}$}
\stp{T}{Isotherme : $\Delta S=n\,R\ln\dfrac{V_2}{V_1}$}
\stp{A}{Adiabatique r\'ev. : $\Delta S=0$ (isentropique)}
\note{Sur un cycle : $\Delta S=0$.}
"""

F["D19-echange-thermique"] = r"""
\titre{\'Echange thermique}
\stp{1}{$Q=m\,c\,\Delta T$ \quad (sans changement d'\'etat)}
\stp{2}{$Q=m\,L$ \quad (changement d'\'etat)}
\stp{3}{$\boxed{P=\dot m\,c\,\Delta T}$ \quad (circuit \`a d\'ebit)}
\note{M\^eme \textbf{puissance} des 2 c\^ot\'es de l'\'echangeur.}
\ex{12\,kW, eau $\Delta T{=}5^\circ$ : $\dot m=\dfrac{12000}{4185\cdot5}=0{,}573$\,kg/s \scr{THERM}}
"""

F["D20-rendements-cascade"] = r"""
\titre{Cascade des rendements}
\stp{1}{$|W_{th}|=\eta_{th}\cdot Q_{CD}$}
\stp{2}{$|W_{ind}|=\eta_{forme}\cdot|W_{th}|$}
\stp{3}{$|W_{disp}|=\eta_{m\acute{e}ca}\cdot|W_{ind}|$}
\stp{4}{$\eta_{eff}=\eta_{th}\,\eta_f\,\eta_m=\dfrac{|W_{disp}|}{Q_{CD}}$}
\ex{$527\to395\to316$\,J \; ($0{,}75$ puis $0{,}8$) \scr{MOTEUR}}
"""

F["D21-puissance"] = r"""
\titre{Travail $\to$ puissance}
\stp{4T}{$P=\dfrac{N}{2\cdot 60}\,W\,z$ \quad (1 cycle $=$ 2 tours)}
\stp{2T}{$P=\dfrac{N}{60}\,W\,z$ \quad (1 cycle $=$ 1 tour)}
\stp{!}{$W$ = par cycle \textbf{et par cylindre}, $N$ en tr/min}
\stp{$\leftarrow$}{$N=\dfrac{P\cdot 120}{|W_{disp}|\,z}$ \; (4 temps)}
"""

F["D22-verifications"] = r"""
\titre{\`A v\'erifier avant de rendre}
\stp{1}{Toutes les $T$ en \textbf{KELVIN} ?}
\stp{2}{$\sum W+\sum Q=0$ sur le cycle \textbf{(le meilleur test)}}
\stp{3}{Moteur $W_{cyc}<0$ \; ; frigo/PAC $W>0$}
\stp{4}{$\eta<1-\dfrac{T_2}{T_1}$ \; et \; $COP<COP_{max}$ ?}
\stp{5}{Les 2 chemins donnent le m\^eme $\eta$ ?}
"""

F["D23-ordres-de-grandeur"] = r"""
\titre{Ordres de grandeur}
\stp{$T$}{apr\`es combustion : 2000 \`a 4000 K}
\stp{$p$}{maximale : 25 \`a 130 bar}
\stp{$\eta$}{moteur : 30 \`a 65 \%}
\stp{$COP$}{d'une PAC : 3 \`a 5}
\stp{$N$}{r\'egime : 1000 \`a 6000 tr/min}
\note{Unit\'es : 1\,bar $=10^5$\,Pa \; ; \; 1\,L $=10^{-3}$\,m$^3$}
"""


F["D24-molaire-ou-massique"] = r"""
\titre{Molaire ou massique ?}
\note{2 facons de compter le MEME gaz. Ne jamais melanger les 2 colonnes.}
\stp{n}{\textbf{MOLAIRE} (moles) : $pV=nRT$, \; $R=8{,}314$}
\stp{}{air : $C_v=20{,}785$ \quad $C_p=29{,}099$ \; J/(mol$\cdot$K)}
\stp{m}{\textbf{MASSIQUE} (kg) : $pV=m\,r\,T$, \; $r=R/M=287$}
\stp{}{air : $c_v=717{,}5$ \quad $c_p=1004{,}5$ \; J/(kg$\cdot$K)}
\note{L'enonce decide : volume/cylindree $\to$ moles ;
debit en kg/s ou $c_p{=}1004$ donne $\to$ par kg.}
"""

# =====================  SCHEMA  =====================

F["S01-cycle-essence"] = r"""
\titre{Cycle ESSENCE}
\begin{center}
\begin{tikzpicture}[x=1mm,y=0.82mm,line width=0.7pt]
\draw[ar](0,0)--(52,0) node[right,font=\small\bfseries]{$V$};
\draw[ar](0,0)--(0,30) node[above,font=\small\bfseries]{$p$};
\coordinate(A)at(7,4);\coordinate(B)at(44,4);
\coordinate(C)at(7,19);\coordinate(D)at(7,27);\coordinate(E)at(44,9);
\draw[dashed,gray,line width=0.4pt](7,0)--(7,29);
\draw[dashed,gray,line width=0.4pt](44,0)--(44,11);
\draw[acc,ar,line width=0.9pt](B)to[out=115,in=-70](C);
\draw[acc,ar,line width=0.9pt](D)to[out=-70,in=110](E);
\draw[grn,line width=1.0pt](C)--(D);
\draw[grn,line width=1.0pt](E)--(B);
\draw[blu,ar,line width=0.9pt](B)--(A);
\foreach \p/\l/\po in {A/A/below,B/B/below,C/C/left,D/D/left,E/E/right}
 {\fill(\p)circle(0.6mm);\node[\po,font=\small\bfseries]at(\p){\l};}
\end{tikzpicture}
\end{center}
\note{\textcolor{acc}{adiabatiques} \; \textcolor{grn}{isochores} \;
\textcolor{blu}{isobare} \; --- $\eta_{th}=1-\varepsilon^{1-\gamma}$}
"""

F["S02-cycle-diesel"] = r"""
\titre{Cycle DIESEL}
\begin{center}
\begin{tikzpicture}[x=1mm,y=0.82mm,line width=0.7pt]
\draw[ar](0,0)--(52,0) node[right,font=\small\bfseries]{$V$};
\draw[ar](0,0)--(0,30) node[above,font=\small\bfseries]{$p$};
\coordinate(A)at(7,4);\coordinate(B)at(44,4);
\coordinate(C)at(7,25);\coordinate(D)at(17,25);\coordinate(E)at(44,10);
\draw[dashed,gray,line width=0.4pt](7,0)--(7,28);
\draw[dashed,gray,line width=0.4pt](44,0)--(44,12);
\draw[acc,ar,line width=0.9pt](B)to[out=115,in=-90](C);
\draw[acc,ar,line width=0.9pt](D)to[out=-60,in=150](E);
\draw[blu,line width=1.0pt](C)--(D);
\draw[grn,line width=1.0pt](E)--(B);
\draw[blu,ar,line width=0.9pt](B)--(A);
\foreach \p/\l/\po in {A/A/below,B/B/below,C/C/left,D/D/right,E/E/right}
 {\fill(\p)circle(0.6mm);\node[\po,font=\small\bfseries]at(\p){\l};}
\end{tikzpicture}
\end{center}
\note{\textcolor{blu}{C-D ISOBARE} (injection) $\ne$ essence \; ---
$\rho=V_D/V_C$, \; $T_D=\rho\,T_C$}
"""

F["S03-quatre-transformations"] = r"""
\titre{Les 4 transformations}
\begin{center}
\begin{tikzpicture}[x=1mm,y=0.82mm,line width=0.7pt]
\draw[ar](0,0)--(52,0) node[right,font=\small\bfseries]{$V$};
\draw[ar](0,0)--(0,30) node[above,font=\small\bfseries]{$p$};
\draw[grn,line width=1.0pt](22,3)--(22,28);
\draw[blu,line width=1.0pt](4,15)--(48,15);
\draw[orange!85!black,line width=1.0pt,domain=10:47,samples=40,smooth]
  plot(\x,{22*15/\x});
\draw[acc,line width=1.0pt,domain=12:34,samples=40,smooth]
  plot(\x,{15*(22/\x)^1.4});
\fill(22,15)circle(0.7mm);
\node[grn,font=\small\bfseries,above]at(22,28){isochore};
\node[blu,font=\small\bfseries,right]at(48,15){isobare};
\node[orange!85!black,font=\small\bfseries]at(45,7){isoth.};
\node[acc,font=\small\bfseries]at(34,6){adiab.};
\end{tikzpicture}
\end{center}
\note{L'adiabatique est \textbf{toujours plus pentue} que l'isotherme.}
"""

F["S04-schema-frigo"] = r"""
\titre{Frigo / PAC --- les organes}
\begin{center}
\begin{tikzpicture}[x=1mm,y=0.82mm,line width=0.8pt]
\draw(9,3)--(9,26)--(45,26)--(45,3)--cycle;
\draw[grn,line width=1.0pt](9,9)--(12,12)--(6,16)--(9,19);
\node[grn,font=\small\bfseries,align=center]at(-1,14){\'Evap.};
\draw[blu,line width=1.0pt](45,9)--(48,12)--(42,16)--(45,19);
\node[blu,font=\small\bfseries,align=center]at(54,14){Cond.};
\draw[acc,line width=1.0pt](21,26)--(27,20)--(33,26);
\node[acc,font=\small\bfseries]at(27,30){Compresseur};
\draw[blu,line width=1.0pt](22,6)--(32,6)--(27,3)--cycle;
\draw[blu,line width=1.0pt](22,0)--(32,0)--(27,3)--cycle;
\node[blu,font=\small\bfseries]at(27,-4){D\'etendeur};
\node[font=\small\bfseries]at(13,22){1};\node[font=\small\bfseries]at(31,23){2};
\node[font=\small\bfseries]at(41,22){3};\node[font=\small\bfseries]at(20,5){4};
\end{tikzpicture}
\end{center}
\note{1-2 compr. \; 2-3 cond. \; 3-4 d\'etente ($h$ cste) \; 4-1 \'evap.}
"""

F["S05-diagramme-logp-h"] = r"""
\titre{Diagramme $(\log p,\,h)$}
\begin{center}
\begin{tikzpicture}[x=1mm,y=0.82mm,line width=0.7pt]
\draw[ar](0,0)--(54,0) node[right,font=\small\bfseries]{$h$};
\draw[ar](0,0)--(0,30) node[above,font=\small\bfseries]{$\log p$};
\draw[gray,line width=0.8pt](9,4)to[out=72,in=180](21,26)to[out=0,in=110](36,4);
\draw[gray,dashed,line width=0.4pt](2,23)--(50,23);
\draw[gray,dashed,line width=0.4pt](2,8)--(46,8);
\coordinate(p4)at(17,8);\coordinate(p1)at(27,8);
\coordinate(p2)at(41,23);\coordinate(p3)at(19,23);
\draw[acc,ar,line width=0.9pt](p1)to[out=95,in=-100](p2);
\draw[blu,ar,line width=0.9pt](p2)--(p3);
\draw[grn,ar,line width=0.9pt](p3)--(p4);
\draw[blu,ar,line width=0.9pt](p4)--(p1);
\foreach \p/\l/\po in {p1/1'/below,p2/2'/above,p3/3'/above,p4/4'/below}
 {\fill(\p)circle(0.6mm);\node[\po,font=\small\bfseries]at(\p){\l};}
\end{tikzpicture}
\end{center}
\note{\textcolor{grn}{3'-4' : verticale} ($h_4=h_3$) \; ---
\textcolor{acc}{1'-2' : isentropique}}
"""

F["S06-moteur-ou-recepteur"] = r"""
\titre{Moteur ou r\'ecepteur ?}
\begin{center}
\begin{tikzpicture}[x=1mm,y=0.82mm,line width=0.7pt]
\draw[ar](0,0)--(26,0) node[right,font=\small\bfseries]{$V$};
\draw[ar](0,0)--(0,28) node[above,font=\small\bfseries]{$p$};
\draw[acc,line width=1.0pt](5,11)to[out=70,in=180](13,22)to[out=0,in=110](21,11);
\draw[acc,-{Latex[length=1.3mm]},line width=1.0pt](5,11)to[out=70,in=180](13.2,22);
\draw[blu,line width=1.0pt](21,11)to[out=250,in=0](13,4)to[out=180,in=290](5,11);
\draw[blu,-{Latex[length=1.3mm]},line width=1.0pt](21,11)to[out=250,in=0](12.8,4);
\node[acc,font=\small\bfseries,align=left]at(43,22){horaire :\\ $W<0$};
\node[font=\small\bfseries,align=left]at(43,14){\textbf{MOTEUR}};
\node[blu,font=\small\bfseries,align=left]at(43,6){antihoraire :\\ \textbf{RECEPTEUR}};
\end{tikzpicture}
\end{center}
\note{Aire enferm\'ee $=|W_{cycle}|$. \; Moteur : $Q_1>0$, $Q_2<0$, $W<0$.}
"""

F["S07-ferme-ou-ouvert"] = r"""
\titre{Ferm\'e ou OUVERT ?}
\begin{center}
\begin{tikzpicture}[x=1mm,y=0.82mm,line width=0.8pt]
\draw(3,7)--(3,25)--(21,25)--(21,7)--cycle;
\draw[pattern=north east lines,draw,line width=0.5pt](3,7)rectangle(21,12);
\draw[line width=1.0pt](3,16)--(21,16);
\draw[line width=1.0pt](12,16)--(12,28);
\node[font=\small\bfseries]at(12,13){gaz};
\node[font=\small\bfseries,align=center]at(12,2){FERM\'E};
\draw[ar,line width=0.9pt](27,16)--(33,16);
\draw(35,11)--(35,21)--(52,21)--(52,11)--cycle;
\draw[ar,line width=0.9pt](52,16)--(58,16);
\node[font=\small\bfseries]at(43,16){machine};
\node[font=\small\bfseries,align=center]at(43,2){OUVERT};
\end{tikzpicture}
\end{center}
\note{FERM\'E : $\Delta U=W+Q$, \; $C_v$ \quad
OUVERT : $\Delta H=W_{ut}+Q$, \; $C_p$}
"""

F["S08-cycle-joule"] = r"""
\titre{Cycle de JOULE}
\begin{center}
\begin{tikzpicture}[x=1mm,y=0.82mm,line width=0.7pt]
\draw[ar](0,0)--(52,0) node[right,font=\small\bfseries]{$V$};
\draw[ar](0,0)--(0,29) node[above,font=\small\bfseries]{$p$};
\coordinate(A)at(8,6);\coordinate(B)at(15,23);
\coordinate(C)at(31,23);\coordinate(D)at(45,6);
\draw[acc,ar,line width=0.9pt](A)to[out=70,in=200](B);
\draw[blu,line width=1.0pt](B)--(C);
\draw[acc,ar,line width=0.9pt](C)to[out=-30,in=120](D);
\draw[blu,line width=1.0pt](D)--(A);
\foreach \p/\l/\po in {A/1/below,B/2/left,C/3/above,D/4/right}
 {\fill(\p)circle(0.6mm);\node[\po,font=\small\bfseries]at(\p){\l};}
\end{tikzpicture}
\end{center}
\note{\textcolor{acc}{1-2 et 3-4 adiabatiques} \;
\textcolor{blu}{2-3 et 4-1 isobares} \; --- par kg, avec $c_p$}
"""


# =====================  DEMONSTRATIONS  =====================

F["T01-travail-elem-1"] = r"""
\titre{DEMO Travail elem. (1/3)}
\stp{1}{Piston a l'equilibre : $F=p\cdot S$}
\stp{2}{On ajoute $dF$ infinitesimal : le piston descend de $d\ell$}
\stp{3}{$dW=|(F+dF)\cdot d\ell|$}
\stp{4}{$dF\ll F$ \; donc \; $dW=|F\,d\ell|=|p\,S\,d\ell|$}
"""

F["T02-travail-elem-2"] = r"""
\titre{DEMO Travail elem. (2/3)}
\stp{5}{Signes : $dW>0$, $p>0$, mais $d\ell<0$}
\stp{6}{Il faut donc un signe $-$ : $dW=-p\,S\,d\ell$}
\stp{7}{Or $S\,d\ell=dV$}
\note{$\boxed{dW=-p\,dV}$ \quad puis
$\boxed{W=-\displaystyle\int_{V_i}^{V_f}p\,dV}$}
"""

F["T03-travail-elem-3"] = r"""
\titre{DEMO Travail elem. (3/3)}
\sect{CAS PARTICULIERS}
\stp{V}{Isochore : $dV=0$ \; $\Rightarrow$ \; $W=0$}
\stp{P}{Isobare : $p$ sort de l'integrale
        \; $\Rightarrow$ \; $W=-p\,(V_f-V_i)$}
\stp{T}{Isotherme : $p=\dfrac{nRT}{V}$, $T$ cste}
\stp{}{$\boxed{W=-nRT\ln\dfrac{V_f}{V_i}}$}
"""

F["T04-premier-principe"] = r"""
\titre{DEMO 1er principe}
\stp{1}{$\Delta U+\Delta E_{cin}+\Delta E_{pot}=W+Q$}
\stp{2}{$U$, $E_{cin}$, $E_{pot}$ : \textbf{fonctions d'etat}}
\stp{3}{$W$ et $Q$ dependent du \textbf{chemin} suivi}
\stp{4}{Cycle : etat final $=$ etat initial}
\note{Tout le membre de gauche s'annule :
$\boxed{W+Q=0}$ sur un cycle}
"""

F["T05-machine-ouverte-1"] = r"""
\titre{DEMO Machine ouverte (1/3)}
\stp{1}{$W_t=W_{ut}-p_2V_2+p_1V_1$}
\note{$p_1V_1$ : le fluide qui suit pousse la tranche.
$p_2V_2$ : la tranche pousse le fluide devant.}
\stp{2}{1er principe :
        $U_2-U_1=W_{ut}-p_2V_2+p_1V_1+Q$}
"""

F["T06-machine-ouverte-2"] = r"""
\titre{DEMO Machine ouverte (2/3)}
\stp{3}{On regroupe les termes :}
\stp{}{$(U_2{+}p_2V_2)-(U_1{+}p_1V_1)=W_{ut}+Q$}
\stp{4}{Or $U+pV=H$ (enthalpie)}
\note{$\boxed{\Delta H=W_{ut}+Q}$ \\
A comparer avec $\Delta U=W+Q$ en systeme ferme.}
"""

F["T07-machine-ouverte-3"] = r"""
\titre{DEMO Machine ouverte (3/3)}
\stp{5}{$-p_2V_2+p_1V_1=-\displaystyle\int_1^2 d(pV)$}
\stp{6}{$d(pV)=p\,dV+V\,dp$}
\stp{7}{Or $\Delta U=W_t+Q$ avec $W_t=-\displaystyle\int p\,dV$}
\stp{8}{On soustrait : $\int p\,dV$ et $Q$ s'annulent}
\note{$\boxed{W_{ut}=\displaystyle\int_1^2 V\,dp}$}
"""

F["T08-chaleurs-spec-1"] = r"""
\titre{DEMO Chaleurs spec. (1/3)}
\stp{1}{$dU=dQ+dW=dQ-p\,dV$}
\stp{2}{$\Rightarrow dQ=dU+p\,dV$}
\stp{3}{$C=\dfrac{1}{n}\dfrac{dQ}{dT}
        =\dfrac{1}{n}\Big(\dfrac{dU}{dT}+p\dfrac{dV}{dT}\Big)$}
\note{Formule generale, valable pour toute transformation.}
"""

F["T09-chaleurs-spec-2"] = r"""
\titre{DEMO Chaleurs spec. (2/3)}
\stp{V}{$V$ constant : $dV=0$, le 2e terme disparait}
\stp{}{$\boxed{C_v=\dfrac{1}{n}\dfrac{dU}{dT}}$}
\stp{P}{$p$ constant : on \textbf{ajoute} $V\dfrac{dp}{dT}$ (qui vaut 0)}
\stp{}{$=\dfrac{1}{n}\dfrac{d(U+pV)}{dT}$ \;
       $\Rightarrow$ \; $\boxed{C_p=\dfrac{1}{n}\dfrac{dH}{dT}}$}
"""

F["T10-mayer"] = r"""
\titre{DEMO Mayer (3/3)}
\stp{1}{$C_p=\dfrac{1}{n}\dfrac{dU}{dT}+\dfrac{1}{n}\dfrac{d(pV)}{dT}$}
\stp{2}{Gaz parfait : $pV=nRT$}
\stp{3}{$=C_v+\dfrac{1}{n}\cdot nR$}
\note{$\boxed{C_p-C_v=R}$ \; et \; $\dfrac{C_p}{C_v}=\gamma>1$ \\
Donc $C_p>C_v$ : a $p$ cste, une part sert a dilater.}
"""

F["T11-adiabatique-1"] = r"""
\titre{DEMO Adiabatique (1/4)}
\stp{1}{Adiabatique : $dQ=0$ \; $\Rightarrow$ \; $dU=dW$}
\stp{2}{Reversible : $dW=-p\,dV$}
\stp{3}{Gaz parfait : $dU=nC_v\,dT$}
\stp{4}{$\Rightarrow$ \; $nC_v\,dT+p\,dV=0$}
"""

F["T12-adiabatique-2"] = r"""
\titre{DEMO Adiabatique (2/4)}
\stp{5}{$pV=nRT$ \; $\Rightarrow$ \; $p=\dfrac{nRT}{V}$}
\stp{6}{$nC_v\,dT+nRT\dfrac{dV}{V}=0$}
\stp{7}{On divise par $n\,T$ :}
\stp{}{$\boxed{C_v\dfrac{dT}{T}+R\dfrac{dV}{V}=0}$}
"""

F["T13-adiabatique-3"] = r"""
\titre{DEMO Adiabatique (3/4)}
\stp{8}{On divise par $C_v$, et $\dfrac{R}{C_v}=\gamma-1$}
\stp{9}{$\dfrac{dT}{T}+(\gamma-1)\dfrac{dV}{V}=0$}
\stp{10}{J'integre : $\ln T+(\gamma-1)\ln V=$ cste}
\stp{11}{$\ln(T\,V^{\gamma-1})=$ cste, puis exponentielle}
\note{$\boxed{T\,V^{\gamma-1}=\text{cste}}$}
"""

F["T14-adiabatique-4"] = r"""
\titre{DEMO Adiabatique (4/4)}
\sect{LES 2 AUTRES FORMES}
\stp{a}{$T=\dfrac{pV}{nR}$ : \; $\dfrac{p\,V^{\gamma}}{nR}=$ cste}
\stp{}{$nR$ constant \; $\Rightarrow$ \; $\boxed{p\,V^{\gamma}=\text{cste}}$}
\stp{b}{$V=\dfrac{nRT}{p}$ : \;
        $T\,(nR)^{\gamma-1}T^{\gamma-1}p^{1-\gamma}=$ cste}
\stp{}{$\Rightarrow$ \; $\boxed{T^{\gamma}\,p^{1-\gamma}=\text{cste}}$}
"""

F["T15-reversible-irreversible"] = r"""
\titre{DEMO Rev. / irreversible}
\note{Ferme monotherme : le 2e principe impose $\Delta W\geq 0$.}
\stp{1}{I et II reversibles : cycle $I+(-II)$, $W_{tot}=0$}
\stp{2}{$\Rightarrow W_I=W_{II}$ \; et \; $Q_I=Q_{II}$}
\stp{3}{I irreversible : $W_{tot}>0$}
\note{$\boxed{W_{irr}>W_{rev}}$ \; donc \; $\boxed{Q_{irr}<Q_{rev}}$}
"""

F["T16-carnot-1"] = r"""
\titre{DEMO Carnot (1/3)}
\note{2 adiabatiques rev. $+$ 2 isothermes rev. : les seules
transfos sans irreversibilite.}
\stp{1}{Cycle : $\Delta U=0=Q_1+Q_2+W$}
\stp{2}{$\eta=\dfrac{|W|}{Q_1}=\dfrac{|-Q_1-Q_2|}{Q_1}$}
\stp{3}{$\boxed{\eta=1+\dfrac{Q_2}{Q_1}}$}
"""

F["T17-carnot-2"] = r"""
\titre{DEMO Carnot (2/3)}
\stp{4}{Isotherme : $\Delta U=0$ donc $Q=-W$}
\stp{5}{$\eta=1-\dfrac{T_A\ln(V_A/V_D)}{T_C\ln(V_B/V_C)}$}
\stp{6}{Adiabatiques, avec $T_B=T_C$ et $T_D=T_A$ :}
\stp{}{$\Big(\dfrac{V_A}{V_B}\Big)^{\gamma-1}
       =\dfrac{T_B}{T_A}=\dfrac{T_C}{T_D}
       =\Big(\dfrac{V_D}{V_C}\Big)^{\gamma-1}$}
"""

F["T18-carnot-3"] = r"""
\titre{DEMO Carnot (3/3)}
\stp{7}{$\dfrac{V_A}{V_B}=\dfrac{V_D}{V_C}$
        \; donc \; $\dfrac{V_A}{V_D}=\dfrac{V_B}{V_C}$}
\stp{8}{Les deux $\ln$ sont egaux : ils se simplifient}
\note{$\boxed{\eta_{Carnot}=1-\dfrac{T_2}{T_1}}$ \\
Meme parfait, le rendement n'est jamais 1.}
"""

F["T19-joule-1"] = r"""
\titre{DEMO Joule (1/2)}
\note{2 adiabatiques rev. $+$ 2 \textbf{isobares} (irreversibles).}
\stp{1}{$\eta=1+\dfrac{nC_p(T_A-T_D)}{nC_p(T_C-T_B)}$}
\stp{2}{Adiab. : $T^{\gamma}p^{1-\gamma}=$ cste, avec
        $p_A{=}p_D$ et $p_B{=}p_C$}
\stp{3}{$\Rightarrow \dfrac{T_A}{T_D}=\dfrac{T_B}{T_C}$}
"""

F["T20-joule-2"] = r"""
\titre{DEMO Joule (2/2)}
\stp{4}{$\dfrac{T_A}{T_B}=\dfrac{T_D}{T_C}
        =\dfrac{T_A-T_D}{T_B-T_C}$}
\stp{5}{En reportant : $\boxed{\eta_J=1-\dfrac{T_A}{T_B}}$}
\stp{6}{Or $T_C>T_B$ donc $\dfrac{T_A}{T_C}<\dfrac{T_A}{T_B}$}
\note{$\boxed{\eta_J<\eta_{Carnot}}$ : les isobares
ne sont pas reversibles.}
"""

F["T21-essence-rendement-1"] = r"""
\titre{DEMO Rendement ESSENCE (1/2)}
\stp{1}{Les 2 echanges de chaleur sont \textbf{isochores} :}
\stp{}{$\eta=1+\dfrac{Q_{EB}}{Q_{CD}}
       =1+\dfrac{nC_v(T_B-T_E)}{nC_v(T_D-T_C)}$}
\stp{2}{Adiab. B-C et D-E, avec $V_D{=}V_C$ et $V_E{=}V_B$}
\stp{3}{$\Rightarrow \dfrac{T_B}{T_E}=\dfrac{T_C}{T_D}$}
"""

F["T22-essence-rendement-2"] = r"""
\titre{DEMO Rendement ESSENCE (2/2)}
\stp{4}{Propriete des proportions :
        $\eta=1-\dfrac{T_B}{T_C}$}
\stp{5}{Adiabatique B-C :
        $\dfrac{T_B}{T_C}=\Big(\dfrac{V_C}{V_B}\Big)^{\gamma-1}$}
\stp{6}{Or $\varepsilon=\dfrac{V_B}{V_C}$}
\note{$\boxed{\eta_{th}=1-\varepsilon^{1-\gamma}}$ \\
Ne depend QUE de $\varepsilon$ et $\gamma$.}
"""

F["T23-diesel-rendement-1"] = r"""
\titre{DEMO Rendement DIESEL (1/2)}
\stp{1}{Combustion isobare $\Rightarrow$ $C_p$ au denominateur :}
\stp{}{$\eta=1+\dfrac{nC_v(T_B-T_E)}{nC_p(T_D-T_C)}$}
\stp{2}{$\varepsilon=\dfrac{V_B}{V_C}$ \; $\Rightarrow$ \;
        $\dfrac{T_B}{T_C}=\varepsilon^{1-\gamma}$}
\stp{3}{$\rho=\dfrac{V_D}{V_C}$ \; $\Rightarrow$ \;
        $\dfrac{T_D}{T_C}=\rho$}
"""

F["T24-diesel-rendement-2"] = r"""
\titre{DEMO Rendement DIESEL (2/2)}
\stp{4}{Detente D-E sur $\dfrac{V_D}{V_E}=\dfrac{\rho}{\varepsilon}$ :}
\stp{}{$\dfrac{T_E}{T_C}=\varepsilon^{1-\gamma}\,\rho^{\gamma}$}
\stp{5}{On divise tout par $T_C$ et on remplace}
\note{$\boxed{\eta=1+\dfrac{\varepsilon^{1-\gamma}
      -\varepsilon^{1-\gamma}\rho^{\gamma}}{\gamma(\rho-1)}}$}
"""

F["T25-entropie-1"] = r"""
\titre{DEMO Entropie (1/2)}
\stp{1}{Carnot generalise, reversible :
        $\displaystyle\sum\frac{Q_i}{T_i}=0$}
\stp{2}{2 chemins rev. :
        $\displaystyle\int_I\frac{dQ}{T}=\int_{II}\frac{dQ}{T}$}
\stp{3}{Independant du chemin : c'est une fonction d'etat, $\Delta S$}
\stp{4}{Si irreversible :
        $\displaystyle\int\frac{dQ}{T}+\Delta S_i=\Delta S$, $\Delta S_i>0$}
"""

F["T26-entropie-2"] = r"""
\titre{DEMO Entropie (2/2)}
\note{Reversible : on remplace $dQ$ dans
$\Delta S=\displaystyle\int\frac{dQ}{T}$.}
\stp{P}{$\Delta S=n\,C_p\ln\dfrac{T_2}{T_1}$}
\stp{V}{$\Delta S=n\,C_v\ln\dfrac{T_2}{T_1}$}
\stp{T}{$\Delta S=\dfrac{Q}{T}=n\,R\ln\dfrac{V_2}{V_1}$}
\stp{A}{Adiabatique rev. : $\Delta S=0$}
"""

F["T27-psn-max"] = r"""
\titre{DEMO $PSN_{max}$ (frigo)}
\stp{1}{Cycle : $Q_1+Q_2+W=0$ \; $\Rightarrow$ \; $W=-Q_1-Q_2$}
\stp{2}{Reversible : $\dfrac{Q_1}{T_1}+\dfrac{Q_2}{T_2}=0$}
\stp{3}{$\Rightarrow \dfrac{Q_1}{Q_2}=-\dfrac{T_1}{T_2}$}
\stp{4}{$PSN=\dfrac{Q_2}{-Q_1-Q_2}
        =\dfrac{1}{-(Q_1/Q_2)-1}$}
\note{$\boxed{PSN_{max}=\dfrac{T_2}{T_1-T_2}}$}
"""

F["T28-cop-max"] = r"""
\titre{DEMO $COP_{max}$ (PAC)}
\stp{1}{Meme depart : $W=-Q_1-Q_2$ et
        $\dfrac{Q_2}{Q_1}=-\dfrac{T_2}{T_1}$}
\stp{2}{$COP=\dfrac{-Q_1}{-Q_1-Q_2}
        =\dfrac{1}{(Q_2/Q_1)+1}$}
\stp{3}{$=\dfrac{1}{1-\dfrac{T_2}{T_1}}$}
\note{$\boxed{COP_{max}=\dfrac{T_1}{T_1-T_2}}$ \;
et $COP_{max}=PSN_{max}+1$}
"""



# ============  DEMOS MANQUANTES (mail de la prof)  ============

F["T29-second-principe-enonces"] = r"""
\titre{DEMO 2e principe : enonces}
\note{Le 1er principe donne $W+Q=0$ sur un cycle, mais \textbf{pas les signes}.
Le 2e principe les impose.}
\stp{K}{\textbf{Kelvin} : impossible de trouver une transformation
        \textbf{fermee monotherme} qui produirait du travail}
\stp{C}{\textbf{Clausius} : le passage de chaleur d'un corps froid vers
        un corps chaud n'a jamais lieu spontanement}
\note{Source de chaleur : corps qui echange sans changer de $T$. \\
1 source $=$ monotherme, 2 $=$ ditherme, $n$ $=$ polytherme.}
"""

F["T30-monotherme-fermee"] = r"""
\titre{DEMO Fermee monotherme}
\stp{1}{Kelvin $\Rightarrow$ $\Delta W\geq 0$}
\stp{2}{Donc $W_{A\to B}\geq 0$ \; et \; $W_{B\to A}\geq 0$}
\stp{3}{Si \textbf{reversible} : $W_{A\to B}=-W_{B\to A}$}
\stp{}{Seule possibilite : $\boxed{\Delta W=0 \text{ et } \Delta Q=0}$}
\stp{4}{Si \textbf{irreversible} : $W_{A\to B}\neq-W_{B\to A}$}
\stp{}{Seule possibilite : $\boxed{\Delta W>0 \text{ et } \Delta Q<0}$}
"""

F["T31-formes-des-courbes"] = r"""
\titre{DEMO Formes iso-T / adiab.}
\stp{1}{Isotherme : $pV=$ cste. On derive :}
\stp{}{$p\,dV+V\,dp=0$ \; $\Rightarrow$ \;
       $\dfrac{dp}{dV}=-\dfrac{p}{V}$}
\stp{2}{Adiabatique : $pV^{\gamma}=$ cste. On derive :}
\stp{}{$\gamma p V^{\gamma-1}dV+V^{\gamma}dp=0$ \; $\Rightarrow$ \;
       $\dfrac{dp}{dV}=-\gamma\dfrac{p}{V}$}
\note{$\gamma>1$ : l'adiabatique est \textbf{plus pentue}
que l'isotherme au meme point.}
"""

F["T32-pci-pcs"] = r"""
\titre{PCI et PCS}
\note{Pouvoir calorifique : chaleur degagee par la combustion
totale de l'unite de combustible.}
\stp{S}{\textbf{PCS} : l'eau formee est \textbf{liquide}
        (on recupere sa chaleur de condensation)}
\stp{I}{\textbf{PCI} : l'eau formee est \textbf{vaporisee}
        (cette chaleur est perdue)}
\stp{}{$\boxed{PCI<PCS}$}
\note{Dans un moteur, les fumees sortent chaudes : on utilise
toujours le \textbf{PCI}.}
"""

F["T33-carnot-description"] = r"""
\titre{Carnot : description et utilite}
\stp{A-B}{compression \textbf{adiabatique} reversible}
\stp{B-C}{detente \textbf{isotherme} rev. : la source chaude donne $Q_1$}
\stp{C-D}{detente \textbf{adiabatique} reversible}
\stp{D-A}{compression \textbf{isotherme} rev. : la source froide recoit $Q_2$}
\note{\textbf{Utilite} : ce sont les seules transfos sans irreversibilite,
donc Carnot donne le rendement \textbf{maximal} atteignable entre 2 sources.
C'est une reference, pas une machine reelle.}
"""

F["T34-joule-description"] = r"""
\titre{Joule : description et utilite}
\stp{A-B}{compression \textbf{adiabatique} rev. (compresseur)}
\stp{B-C}{echauffement \textbf{isobare} (chambre de combustion), $Q_1$}
\stp{C-D}{detente \textbf{adiabatique} rev. (turbine)}
\stp{D-A}{refroidissement \textbf{isobare}, $Q_2$}
\note{\textbf{Utilite} : c'est le cycle des \textbf{turbines a gaz}
(centrales, turboreacteurs). Les isobares sont plus faciles a realiser
que les isothermes de Carnot, au prix d'un rendement plus faible.}
"""

F["T35-essence-les-4-temps"] = r"""
\titre{Essence : les 4 temps}
\stp{1}{\textbf{Aspiration} A-B \textcolor{blu}{isobare} : soupape ouverte,
        le piston descend, melange air+carburant}
\stp{2}{\textbf{Compression} B-C \textcolor{acc}{adiabatique} : soupapes
        fermees, trop rapide pour evacuer la chaleur}
\stp{3}{\textbf{Explosion} C-D \textcolor{grn}{isochore} (bougie) puis
        \textbf{detente} D-E \textcolor{acc}{adiabatique}}
\stp{4}{\textbf{Echappement} E-B \textcolor{grn}{isochore} (ouverture)
        puis B-A \textcolor{blu}{isobare} (refoulement)}
"""

# ============  EXERCICES RESOLUS (exemple chiffre)  ============

F["E01-cycle-enonce"] = r"""
\titre{EXO Cycle (1/3) --- enonce}
\note{$n=0{,}5$ mol d'air, $\gamma=1{,}4$.
A : $p{=}1$ bar, $T{=}300$ K. \\
A-B isobare jusqu'a 600 K \; ; \; B-C isochore jusqu'a 300 K \; ; \;
C-A isotherme.}
\stp{1}{$V_A=\dfrac{nRT_A}{p_A}
        =\dfrac{0{,}5\cdot 8{,}314\cdot 300}{10^5}=12{,}47$ L}
\stp{2}{Isobare : $V_B=V_A\dfrac{T_B}{T_A}=24{,}94$ L, \; $p_B=1$ bar}
\stp{3}{Isochore : $V_C=24{,}94$ L, \;
        $p_C=p_B\dfrac{T_C}{T_B}=0{,}5$ bar}
"""

F["E02-cycle-w-et-q"] = r"""
\titre{EXO Cycle (2/3) --- $W$ et $Q$}
\stp{AB}{$W=-p\,\Delta V=-10^5(24{,}94{-}12{,}47)10^{-3}=-1247$ J}
\stp{}{$Q=nC_p\Delta T=0{,}5\cdot 29{,}099\cdot 300=+4365$ J}
\stp{BC}{$W=0$ \; ; \;
         $Q=nC_v\Delta T=0{,}5\cdot 20{,}785\cdot(-300)=-3118$ J}
\stp{CA}{$W=-nRT\ln\dfrac{V_A}{V_C}=-1247\cdot\ln(0{,}5)=+864$ J}
\stp{}{$Q=-W=-864$ J \; (isotherme, $\Delta U=0$)}
"""

F["E03-cycle-bilan"] = r"""
\titre{EXO Cycle (3/3) --- bilan}
\stp{1}{$\sum W=-1247+0+864=\mathbf{-383}$ J}
\stp{2}{$\sum Q=4365-3118-864=\mathbf{+383}$ J}
\stp{3}{$\sum W+\sum Q=0$ \; \textbf{verification OK}}
\stp{4}{$W<0$ : le cycle \textbf{fournit} $\Rightarrow$ moteur}
\stp{5}{$\eta=\dfrac{|W|}{Q_{fourni}}=\dfrac{383}{4365}$}
\ex{$\eta=\mathbf{8{,}8\,\%}$ \; (seul $Q_{AB}>0$ est \og paye \fg)}
"""

F["E04-essence-enonce"] = r"""
\titre{EXO Essence (1/5) --- volumes}
\note{4 temps, 4 cyl., cylindree 1,2 L, $\varepsilon=10$,
air a $16^\circ$C et 1 bar, $\gamma=1{,}4$.}
\stp{1}{Par cylindre : $\dfrac{1{,}2}{4}=0{,}3$ L}
\stp{2}{$V_B-V_A=0{,}3$ \; et \; $\dfrac{V_B}{V_A}=10$}
\stp{3}{$9V_A=0{,}3$ \; $\Rightarrow$ \; $V_A=33{,}3$ cm$^3$}
\ex{$V_A=V_C=33{,}3$ cm$^3$ \; ; \; $V_B=V_E=333{,}3$ cm$^3$}
"""

F["E05-essence-point-C"] = r"""
\titre{EXO Essence (2/5) --- point C}
\stp{1}{$T_B=16+273{,}15=289{,}15$ K, \; $p_B=10^5$ Pa}
\stp{2}{$n=\dfrac{p_BV_B}{RT_B}
        =\dfrac{10^5\cdot 333{,}3\cdot 10^{-6}}{8{,}314\cdot 289{,}15}$}
\stp{}{$n=\mathbf{0{,}01387}$ mol}
\stp{3}{$T_C=T_B\,\varepsilon^{\gamma-1}=289{,}15\cdot 10^{0,4}
        =289{,}15\cdot 2{,}512$}
\ex{$T_C=\mathbf{726{,}3}$ K \; ; \;
$p_C=10^{1,4}=\mathbf{25{,}1}$ bar}
"""

F["E06-essence-combustion"] = r"""
\titre{EXO Essence (3/5) --- combustion}
\note{CH$_{1,8}$, $\lambda=1{,}2$, PCI $=42500$ kJ/kg.}
\stp{1}{$CH_{1,8}+1{,}45\,O_2\to CO_2+0{,}9\,H_2O$}
\stp{2}{$n_{air}=\dfrac{1{,}45}{0{,}21}=6{,}905$, \;
        $\times 1{,}2=8{,}286$}
\stp{3}{$n_{carb}=\dfrac{0{,}01387}{8{,}286+1}=1{,}493\cdot10^{-3}$ mol}
\stp{4}{$m_{carb}=1{,}493\cdot10^{-3}\cdot 13{,}8=20{,}6$ mg}
\ex{$Q_{CD}=2{,}06\cdot10^{-5}\cdot 42{,}5\cdot10^{6}=\mathbf{876}$ J}
"""

F["E07-essence-points-D-E"] = r"""
\titre{EXO Essence (4/5) --- D et E}
\stp{1}{$nC_v=0{,}01387\cdot 20{,}785=0{,}2882$ J/K}
\stp{2}{Isochore : $T_D=T_C+\dfrac{Q_{CD}}{nC_v}
        =726{,}3+\dfrac{876}{0{,}2882}$}
\stp{}{$T_D=\mathbf{3765}$ K \; ; \;
       $p_D=25{,}1\cdot\dfrac{3765}{726{,}3}=\mathbf{130}$ bar}
\stp{3}{$T_E=T_D\,\varepsilon^{1-\gamma}=3765\cdot 0{,}398$}
\ex{$T_E=\mathbf{1499}$ K \; ; \; $p_E=\mathbf{5{,}18}$ bar}
"""

F["E08-essence-rendement"] = r"""
\titre{EXO Essence (5/5) --- $\eta$ et $P$}
\note{$\eta_f=0{,}75$, $\eta_{meca}=0{,}8$, $P_{eff}=20$ kW.}
\stp{1}{$\eta_{th}=1-10^{-0,4}=1-0{,}398=\mathbf{60{,}2\,\%}$}
\stp{2}{$|W_{th}|=0{,}602\cdot 876=527$ J}
\stp{3}{$527\xrightarrow{\times0,75}395
        \xrightarrow{\times0,8}|W_{disp}|=316$ J}
\stp{4}{$N=\dfrac{P\cdot 120}{|W_{disp}|\,z}
        =\dfrac{20000\cdot 120}{316\cdot 4}$}
\ex{$N=\mathbf{1897}$ tr/min}
"""

F["E09-frigo-enonce"] = r"""
\titre{EXO Frigo (1/4) --- les points}
\note{PAC R134a. Evap. $-5^\circ$C, cond. $45^\circ$C,
$\eta_{isos}=0{,}75$. Lu sur le diagramme :
$h_1{=}402{,}5$, $h_{2s}{=}435$, $h_3{=}257$ kJ/kg.}
\stp{1}{$h_4=h_3=\mathbf{257}$ kJ/kg \; (detente isenthalpique)}
\stp{2}{$h_2=h_1+\dfrac{h_{2s}-h_1}{\eta_{isos}}
        =402{,}5+\dfrac{32{,}5}{0{,}75}$}
\ex{$h_2=402{,}5+43{,}33=\mathbf{445{,}8}$ kJ/kg}
"""

F["E10-frigo-energies"] = r"""
\titre{EXO Frigo (2/4) --- energies}
\stp{1}{$w=h_2-h_1=445{,}8-402{,}5=\mathbf{+43{,}3}$ kJ/kg}
\stp{2}{$q_1=h_3-h_2=257-445{,}8=\mathbf{-188{,}8}$ kJ/kg}
\stp{3}{$q_2=h_1-h_4=402{,}5-257=\mathbf{+145{,}5}$ kJ/kg}
\ex{Verif : $-188{,}8+145{,}5+43{,}3=0$ \; OK}
"""

F["E11-frigo-cop"] = r"""
\titre{EXO Frigo (3/4) --- COP}
\stp{1}{C'est une \textbf{PAC} : utile $=$ chaleur cedee au chaud}
\stp{2}{$COP=\dfrac{-q_1}{w}=\dfrac{188{,}8}{43{,}3}=\mathbf{4{,}36}$}
\stp{3}{$T_1=318{,}15$ K, $T_2=268{,}15$ K}
\stp{4}{$COP_{max}=\dfrac{318{,}15}{50}=6{,}36$}
\ex{$4{,}36/6{,}36=69\,\%$ du maximum : credible}
"""

F["E12-frigo-debits"] = r"""
\titre{EXO Frigo (4/4) --- debits}
\note{La maison perd 12 kW ; eau des radiateurs $\Delta T=5^\circ$C,
$c=4185$ J/kg$\cdot$K.}
\stp{1}{$\dot m=\dfrac{P}{|q_1|}=\dfrac{12}{188{,}8}
        =\mathbf{0{,}0636}$ kg/s}
\stp{2}{$P_{comp}=\dot m\,w=0{,}0636\cdot 43{,}3=\mathbf{2{,}75}$ kW}
\stp{3}{$\dot m_{eau}=\dfrac{12000}{4185\cdot 5}$}
\ex{$\dot m_{eau}=\mathbf{0{,}573}$ kg/s $\approx 2{,}1$ m$^3$/h}
"""

# ============  LECTURE DU DIAGRAMME log p-h  ============

F["L01-diagramme-placer-points"] = r"""
\titre{Lire log p-h (1/2) --- placer}
\note{Axes : horizontal $=h$ (kJ/kg), vertical (log) $=p$ (bar).}
\stp{1}{Pt 1 (\'evap.) : isobare $p_{\'evap}(T_{\'evap})$
$\cap$ courbe vapeur satur\'ee (ou $+$loin si surchauffe)}
\stp{2}{Pt 2 (compr.) : suivre l'\textbf{isentropique}
depuis 1 jusqu'\`a $p_{cond}$}
\stp{3}{Pt 3 (cond.) : isobare $p_{cond}$
$\cap$ courbe liquide satur\'e (ou $-$loin si sous-refroid.)}
\stp{4}{Pt 4 (d\'etente) : \textbf{verticale} depuis 3
jusqu'\`a $p_{\'evap}$ \; $\Rightarrow h_4=h_3$}
"""

F["L02-diagramme-lire-psn"] = r"""
\titre{Lire log p-h (2/2) --- calculer}
\stp{1}{Projeter chaque point sur l'axe $h$ : lecture
$h_1,h_2,h_3{=}h_4$ (kJ/kg)}
\stp{2}{$w=h_2-h_1$ \quad (compresseur)}
\stp{3}{$q_1=h_1-h_4$ \quad (\'evapo, effet utile FROID)}
\stp{4}{$q_2=h_2-h_3$ \quad (conden., c\'ed\'e au CHAUD)}
\stp{}{$\boxed{PSN=\dfrac{q_1}{w}}$ \quad
$\boxed{COP_{PAC}=\dfrac{|q_2|}{w}=PSN{+}1}$}
\ex{$h_1{=}1760,h_2{=}2050,h_3{=}700$ : $PSN{=}\mathbf{3{,}66}$ \scr{PAC}}
"""


# ------------------------------------------------------------------
def build(name, body, pt=9):
    tex = os.path.join(TMP, name + ".tex")
    open(tex, "w", encoding="utf-8").write(
        PRE.replace("__PT__", str(pt)).replace("__H__", H_IN) + "\\begin{document}\n" + body + "\n\\end{document}\n")
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-output-directory", TMP, tex],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pdf = os.path.join(TMP, name + ".pdf")
    if not os.path.exists(pdf):
        return None
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    return int([l.split(":")[1] for l in info.splitlines() if l.startswith("Pages")][0])

def render(name, body):
    for pt in (13, 12, 11, 10, 9):
        n = build(name, body, pt)
        if n is None:
            print("  %-32s ECHEC LaTeX" % name)
            log = os.path.join(TMP, name + ".log")
            if os.path.exists(log):
                for l in open(log, encoding="utf-8", errors="ignore"):
                    if l.startswith("!"):
                        print("      ", l.strip())
                        break
            return False
        if n == 1:
            subprocess.run(["pdftoppm", "-png", "-r", "400", "-singlefile",
                            os.path.join(TMP, name + ".pdf"), os.path.join(TMP, name)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            Image.open(os.path.join(TMP, name + ".png")).convert("RGB") \
                 .resize((384, H_PX), Image.LANCZOS) \
                 .filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=2)) \
                 .save(os.path.join(OUT, name + ".png"))
            print("  %-32s OK%s" % (name, "" if pt == 13 else "  (reduit a %dpt)" % pt))
            return True
    print("  %-32s DEBORDE meme en 9pt" % name)
    return False

print("Generation des fiches...")
ok = 0
for name in sorted(F):
    if render(name, F[name]):
        ok += 1
print("--> %d/%d fiches dans %s" % (ok, len(F), os.path.normpath(OUT)))
shutil.rmtree(TMP, ignore_errors=True)
