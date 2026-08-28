import math
from common import *

CX, CY = 1120, 965
R1, R2 = 235, 655
a = (R1 + R2) / 2.0
c = a - R1
b = math.sqrt(a*a - c*c)
EX = CX + c
PERI = (CX - R1, CY)
APO  = (CX + R2, CY)

o = [head(seed=11), frame()]
o.append(sheet_header("HOHMANN TRANSFER",
                      "MINIMUM-ENERGY COPLANAR TRANSFER  /  LEO 400 KM → GEO",
                      "SHEET 1 OF 5    REV C    SCALE 1:2.4E4"))

g = ['<g filter="url(#sketch)">']
g.append(f'<g stroke="{INK_DIM}" stroke-opacity=".13" stroke-width="1.4" fill="none">')
for k in range(24):
    ang = math.radians(k*15)
    g.append(f'<path d="M{CX+R1*0.4*math.cos(ang):.1f} {CY+R1*0.4*math.sin(ang):.1f} '
             f'L{CX+(R2+62)*math.cos(ang):.1f} {CY+(R2+62)*math.sin(ang):.1f}"/>')
g.append('</g>')
g.append(f'<g stroke="{INK}" stroke-opacity=".45" stroke-width="1.8" fill="none">'
         f'<path d="M{CX-58} {CY} h116"/><path d="M{CX} {CY-58} v116"/></g>')

g.append(f'<circle cx="{CX}" cy="{CY}" r="{R1}" fill="none" stroke="{INK}" stroke-opacity=".52" '
         f'stroke-width="2.6" stroke-dasharray="16 11"/>')
g.append(f'<circle cx="{CX}" cy="{CY}" r="{R2}" fill="none" stroke="{INK}" stroke-opacity=".44" '
         f'stroke-width="2.6" stroke-dasharray="16 11"/>')
g.append(f'<circle cx="{CX}" cy="{CY}" r="88" fill="{INK}" fill-opacity=".10" stroke="{INK}" '
         f'stroke-opacity=".72" stroke-width="3"/>')
g.append(f'<circle cx="{CX}" cy="{CY}" r="112" fill="none" stroke="{INK}" stroke-opacity=".22" '
         f'stroke-width="1.6" stroke-dasharray="5 9"/>')

# coast half solid (upper), return half ghosted
g.append(f'<path d="M{PERI[0]:.1f} {PERI[1]:.1f} A {a:.1f} {b:.1f} 0 0 1 {APO[0]:.1f} {APO[1]:.1f}" '
         f'fill="none" stroke="{AMBER}" stroke-opacity=".92" stroke-width="4.2" stroke-linecap="round"/>')
g.append(f'<path d="M{PERI[0]:.1f} {PERI[1]:.1f} A {a:.1f} {b:.1f} 0 0 0 {APO[0]:.1f} {APO[1]:.1f}" '
         f'fill="none" stroke="{AMBER}" stroke-opacity=".20" stroke-width="2" stroke-dasharray="9 12"/>')
g.append(f'<path d="M{PERI[0]-130:.1f} {CY} H{APO[0]+130:.1f}" stroke="{INK_DIM}" stroke-opacity=".34" '
         f'stroke-width="1.5" stroke-dasharray="26 8 5 8" fill="none"/>')
F2 = (EX + c, CY)
g.append(f'<g stroke="{INK_DIM}" stroke-opacity=".45" stroke-width="1.8" fill="none">'
         f'<path d="M{F2[0]-20:.1f} {CY} h40"/><path d="M{F2[0]:.1f} {CY-20} v40"/></g>')

for (bx, by, ang) in ((PERI[0], PERI[1], -math.pi/2), (APO[0], APO[1], math.pi/2)):
    g.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="15" fill="{AMBER}" fill-opacity=".95"/>')
    g.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="30" fill="none" stroke="{AMBER}" '
             f'stroke-opacity=".5" stroke-width="2"/>')
    g.append(vector(bx, by, bx + 118*math.cos(ang), by + 118*math.sin(ang), AMBER, .9, 3.4))

T = 232
sx, sy = ellipse_pt(EX, CY, a, b, 0, T)
tan = math.atan2(b*math.cos(math.radians(T)), -a*math.sin(math.radians(T)))
g.append(f'<path d="M{CX} {CY} L{sx:.1f} {sy:.1f}" stroke="{GREEN}" stroke-opacity=".40" '
         f'stroke-width="1.6" stroke-dasharray="7 8" fill="none"/>')
g.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="11" fill="{GREEN}" fill-opacity=".95"/>')
g.append(vector(sx, sy, sx+140*math.cos(tan), sy+140*math.sin(tan), GREEN, .85, 2.8))
g.append('</g>')
o += g

o.append(dim(CX, CY, PERI[0], CY, "r₁ = 6 778 km", off=124))
o.append(dim(CX, CY, APO[0], CY, "r₂ = 42 164 km", off=178))
o.append(dim(PERI[0], CY, APO[0], CY, "2a = 48 942 km", off=-330))

# ---- left annotation column ----
o.append(callout(PERI[0], PERI[1]-118, 800, 470, [
    "BURN 1 — PERIAPSIS INJECTION", "Δv₁ = 2.4260 km/s   prograde",
    "ignition T+00:00:00   mₚ = 1 848 kg"], col=AMBER, anchor="end"))
o.append(callout(sx, sy, 760, 800, [
    "SPACECRAFT — COAST PHASE", "ν = 132.4°   r = 21 470 km", "v = 3.194 km/s   t = 02h 37m"],
    col=GREEN, anchor="end"))
o.append(callout(CX+R1*math.cos(math.radians(146)), CY+R1*math.sin(math.radians(146)), 700, 1180, [
    "PARKING ORBIT — LEO 400 km", "T = 92m 33s   v = 7.6726 km/s"], anchor="end"))

# ---- right annotation column ----
o.append(f'<g stroke="{INK}" stroke-opacity=".22" stroke-width="1.5" fill="none">'
         f'<rect x="2160" y="318" width="628" height="152"/></g>')
o.append(txt(2185, 360, "VIS-VIVA", 21, .48, INK, ls=4))
o.append(txt(2185, 412, "v² = μ ( 2/r − 1/a )", 30, .82, INK, ls=1))
o.append(txt(2185, 450, "μ⊕ = 398 600.4418 km³·s⁻²", 19, .45, INK))

o.append(callout(*ellipse_pt(EX, CY, a, b, 0, 310), 2185, 640, [
    "TRANSFER ELLIPSE", "a = 24 471 km   e = 0.7230", "i = 0.00°   coplanar"], col=AMBER))
o.append(callout(APO[0], APO[1]+118, 2185, 930, [
    "BURN 2 — APOAPSIS CIRCULARISATION", "Δv₂ = 1.4675 km/s   prograde",
    "ignition T+05:15:24   mₚ = 1 026 kg"], col=AMBER))
o.append(callout(CX+R2*math.cos(math.radians(52)), CY+R2*math.sin(math.radians(52)), 2185, 1220, [
    "TARGET ORBIT — GEOSTATIONARY", "T = 23h 56m 04s   v = 3.0747 km/s"]))

o.append(txt(F2[0]+30, CY-22, "F₂ (vacant)", 19, .45, INK_DIM))
o.append(txt(CX-24, CY+152, "F₁", 22, .60, INK, anchor="middle"))

o.append(block(150, 1400, [
    "Δv TOTAL . . . . . 3.8935 km/s",
    "TIME OF FLIGHT . . 05h 15m 24s",
    "PROPELLANT . . . . 2 874 kg",
    "C₃ . . . . . . . . −15.802 km²·s⁻²",
], 22, 34, .50))

o.append(title_block(1990, 1440, "SHEET 01 — TRANSFER", [
    ("EPOCH", "2026-08-28 T 00:00Z"), ("FRAME", "ECI J2000"),
    ("METHOD", "IMPULSIVE 2-BODY"), ("DRAWN", "APOAPSIS DRAFTING"),
], w=790))
o.append(tail())
open("s1.svg", "w").write("".join(o))
