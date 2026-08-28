import math
from common import *

CX, CY = 1290, 985
A, B = 600, 440
C = math.sqrt(A*A - B*B)
ECC = C / A
F1 = (CX - C, CY)
F2 = (CX + C, CY)
PERI, APO = (CX - A, CY), (CX + A, CY)

def pt(t): return ellipse_pt(CX, CY, A, B, 0, t)

def sector_pts(t0, t1, n=72):
    return [F1] + [pt(t0 + (t1-t0)*k/n) for k in range(n+1)]

def area(ps):
    s = 0.0
    for i in range(len(ps)):
        x1, y1 = ps[i]; x2, y2 = ps[(i+1) % len(ps)]
        s += x1*y2 - x2*y1
    return abs(s)/2

# choose the apoapsis span so both swept sectors have the same area (Kepler II)
PSPAN = 62.0
target = area(sector_pts(180-PSPAN, 180+PSPAN))
lo, hi = 1.0, PSPAN
for _ in range(60):
    mid = (lo+hi)/2
    if area(sector_pts(-mid, mid)) < target: lo = mid
    else: hi = mid
ASPAN = (lo+hi)/2

def poly(ps): return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)

NU_T = -125.0
P = pt(NU_T)
AUX = (P[0], CY - math.sqrt(max(A*A - (P[0]-CX)**2, 0)))

o = [head(seed=23, freq=0.009, scale=4.0), frame()]
o.append(sheet_header("ORBITAL ELEMENTS",
                      "KEPLERIAN GEOMETRY  /  TRUE, ECCENTRIC AND MEAN ANOMALY",
                      "SHEET 2 OF 5    REV C    SCALE — NTS"))

g = ['<g filter="url(#sketch)">']
for pts in (sector_pts(180-PSPAN, 180+PSPAN), sector_pts(-ASPAN, ASPAN)):
    g.append(f'<polygon points="{poly(pts)}" fill="{VIOLET}" fill-opacity=".10" '
             f'stroke="{VIOLET}" stroke-opacity=".42" stroke-width="1.6"/>')
g.append(f'<circle cx="{CX}" cy="{CY}" r="{A}" fill="none" stroke="{INK_DIM}" stroke-opacity=".26" '
         f'stroke-width="1.6" stroke-dasharray="10 13"/>')
g.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{A}" ry="{B}" fill="none" stroke="{INK}" '
         f'stroke-opacity=".88" stroke-width="4"/>')
g.append(f'<g stroke="{INK_DIM}" stroke-opacity=".36" stroke-width="1.6" fill="none">'
         f'<path d="M{PERI[0]-105} {CY} H{APO[0]+105}" stroke-dasharray="26 8 5 8"/>'
         f'<path d="M{CX} {CY-B-105} V{CY+B+105}" stroke-dasharray="26 8 5 8"/></g>')
for f in (F1, F2):
    g.append(f'<g stroke="{INK}" stroke-opacity=".55" stroke-width="2" fill="none">'
             f'<path d="M{f[0]-22:.1f} {f[1]} h44"/><path d="M{f[0]:.1f} {f[1]-22} v44"/></g>')
g.append(f'<circle cx="{F1[0]:.1f}" cy="{F1[1]:.1f}" r="58" fill="{INK}" fill-opacity=".13" '
         f'stroke="{INK}" stroke-opacity=".72" stroke-width="2.8"/>')
g.append(f'<g stroke="{INK_DIM}" stroke-opacity=".48" stroke-width="1.6" fill="none" stroke-dasharray="7 8">'
         f'<path d="M{P[0]:.1f} {P[1]:.1f} L{AUX[0]:.1f} {AUX[1]:.1f}"/>'
         f'<path d="M{CX} {CY} L{AUX[0]:.1f} {AUX[1]:.1f}"/>'
         f'<path d="M{P[0]:.1f} {P[1]:.1f} V{CY}"/></g>')
g.append(f'<circle cx="{AUX[0]:.1f}" cy="{AUX[1]:.1f}" r="7" fill="none" stroke="{INK_DIM}" '
         f'stroke-opacity=".75" stroke-width="2"/>')
g.append(vector(F1[0], F1[1], P[0], P[1], GREEN, .85, 2.8))
g.append(f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="12" fill="{GREEN}" fill-opacity=".95"/>')
tn = math.atan2(B*math.cos(math.radians(NU_T)), -A*math.sin(math.radians(NU_T)))
g.append(vector(P[0], P[1], P[0]+150*math.cos(tn), P[1]+150*math.sin(tn), GREEN, .8, 2.6))
for q in (PERI, APO):
    g.append(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="11" fill="{AMBER}" fill-opacity=".92"/>')
g.append('</g>')
o += g

def arc_poly(cx, cy, r, a0, a1, col, op, n=48):
    p = [(cx+r*math.cos(a0+(a1-a0)*k/n), cy+r*math.sin(a0+(a1-a0)*k/n)) for k in range(n+1)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p)
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="2"/>'

# ν measured at the focus from the periapsis direction
a0 = math.pi
a1 = a0 + ((math.atan2(P[1]-F1[1], P[0]-F1[0]) - a0) % (2*math.pi))
o.append(arc_poly(F1[0], F1[1], 150, a0, a1, GREEN, .68))
am = (a0+a1)/2
o.append(txt(F1[0]+178*math.cos(am), F1[1]+178*math.sin(am)+10, "ν", 30, .88, GREEN, anchor="middle"))
# E measured at the centre from the periapsis direction
b1 = a0 + ((math.atan2(AUX[1]-CY, AUX[0]-CX) - a0) % (2*math.pi))
o.append(arc_poly(CX, CY, 112, a0, b1, INK_DIM, .72))
o.append(txt(CX+142*math.cos((a0+b1)/2), CY+142*math.sin((a0+b1)/2)+9, "E", 27, .75, INK_DIM, anchor="middle"))

o.append(dim(CX, CY, APO[0], CY, "a = 26 560 km", off=-84))
o.append(dim(CX, CY, CX, CY-B, "b = 19 219 km", off=-88))
o.append(dim(CX, CY, F1[0], CY, "c = a·e", off=84))
o.append(dim(F1[0], CY, PERI[0], CY, "r_p", off=-250))
o.append(dim(F1[0], CY, APO[0], CY, "r_a", off=-370))

o.append(callout(P[0], P[1], 620, 420, [
    "SPACECRAFT STATE VECTOR",
    "r = [ −18 442.7  +9 133.5  0.0 ] km",
    "v = [  −1.8842  −3.0517  0.0 ] km/s"], col=GREEN, anchor="end"))
o.append(callout(*pt(180-40), 600, 1215, [
    "EQUAL AREAS IN EQUAL TIMES",
    "ΔA₁ = ΔA₂ = ½·h·Δt    (Kepler II)"], col=VIOLET, anchor="end"))
o.append(callout(PERI[0], PERI[1], 570, 1490, ["PERIAPSIS", "r_p = a(1−e) = 8 246 km"],
                 col=AMBER, anchor="end"))
o.append(callout(APO[0], APO[1], 2020, 1290, ["APOAPSIS", "r_a = a(1+e) = 44 874 km"], col=AMBER))
o.append(txt(F1[0]-10, F1[1]+92, "F₁", 22, .62, INK, anchor="middle"))
o.append(txt(F2[0]-4, F2[1]+50, "F₂", 22, .48, INK_DIM, anchor="middle"))

o.append(f'<g stroke="{INK}" stroke-opacity=".24" stroke-width="1.5" fill="none">'
         f'<rect x="2180" y="310" width="606" height="452"/><path d="M2180 358 h606"/></g>')
o.append(txt(2204, 344, "CLASSICAL ELEMENTS", 20, .55, INK, ls=3.4))
for i, (k, v) in enumerate([("a", "26 560.0 km"), ("e", "0.6896"), ("i", "63.4349°"),
                            ("Ω", "115.2074°"), ("ω", "270.0000°"), ("M₀", "84.9163°"),
                            ("n", "2.0057 rev/day"), ("T", "11h 58m 02s")]):
    y = 400 + i*48
    o.append(txt(2204, y, k, 24, .60, INK))
    o.append(txt(2762, y, v, 22, .78, INK, anchor="end"))
    if i < 7:
        o.append(f'<path d="M2204 {y+16} h558" stroke="{INK}" stroke-opacity=".10" stroke-width="1.2"/>')

o.append(f'<g stroke="{INK}" stroke-opacity=".22" stroke-width="1.5" fill="none">'
         f'<rect x="2180" y="822" width="606" height="206"/></g>')
o.append(txt(2204, 864, "ORBIT EQUATION / KEPLER", 20, .5, INK, ls=3))
o.append(txt(2204, 920, "r = a(1−e²) / (1 + e·cos ν)", 24, .82, INK, ls=.6))
o.append(txt(2204, 970, "M = E − e·sin E", 24, .82, INK, ls=.6))
o.append(txt(2204, 1006, "tan(ν/2) = √((1+e)/(1−e))·tan(E/2)", 18, .45, INK, ls=.4))

o.append(block(150, 1590, [
    "SPECIFIC ENERGY   ε . . −7.5045 km²·s⁻²",
    "ANG. MOMENTUM     h . . 63 852 km²·s⁻¹",
    "FLIGHT PATH ANGLE γ . . +38.117°",
], 21, 33, .48))

o.append(title_block(1980, 1440, "SHEET 02 — ELEMENTS", [
    ("EPOCH", "2026-08-28 T 00:00Z"), ("FRAME", "ECI J2000"),
    ("SOURCE", "TWO-BODY ANALYTIC"), ("DRAWN", "APOAPSIS DRAFTING"),
], w=800))
o.append(tail())
open("s2.svg", "w").write("".join(o))
