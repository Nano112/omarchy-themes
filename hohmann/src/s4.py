import math
from common import *

P1 = (1230, 980)          # primary
D  = 690                  # mutual separation
MU = 0.012150             # secondary mass fraction
P2 = (P1[0] + D, P1[1])
BC = (P1[0] + MU*D, P1[1])   # barycentre
L1 = (P1[0] + 0.84907*D, P1[1])
L2 = (P1[0] + 1.16783*D, P1[1])
L3 = (P1[0] - 0.99291*D, P1[1])
L4 = (P1[0] + 0.5*D, P1[1] - 0.86603*D)
L5 = (P1[0] + 0.5*D, P1[1] + 0.86603*D)

o = [head(seed=59, freq=0.009, scale=4.2), frame()]
o.append(sheet_header("LIBRATION POINTS",
                      "CIRCULAR RESTRICTED THREE-BODY PROBLEM  /  EARTH–MOON  ·  μ = 0.012150",
                      "SHEET 4 OF 5    REV C    SCALE 1:9.6E5"))

g = ['<g filter="url(#sketch)">']
# secondary's orbit about the barycentre + equilateral construction
g.append(f'<circle cx="{BC[0]:.1f}" cy="{BC[1]:.1f}" r="{D*(1-MU):.1f}" fill="none" stroke="{INK}" '
         f'stroke-opacity=".30" stroke-width="2.0" stroke-dasharray="16 12"/>')
g.append(f'<g stroke="{INK_DIM}" stroke-opacity=".34" stroke-width="1.6" fill="none" stroke-dasharray="9 10">'
         f'<path d="M{P1[0]} {P1[1]} L{L4[0]:.1f} {L4[1]:.1f} L{P2[0]} {P2[1]}"/>'
         f'<path d="M{P1[0]} {P1[1]} L{L5[0]:.1f} {L5[1]:.1f} L{P2[0]} {P2[1]}"/></g>')
g.append(f'<path d="M{L3[0]-120:.1f} {P1[1]} H{L2[0]+140:.1f}" stroke="{INK_DIM}" stroke-opacity=".38" '
         f'stroke-width="1.6" stroke-dasharray="26 8 5 8" fill="none"/>')
# bodies
g.append(f'<circle cx="{P1[0]}" cy="{P1[1]}" r="86" fill="{INK}" fill-opacity=".13" stroke="{INK}" '
         f'stroke-opacity=".78" stroke-width="3.2"/>')
g.append(f'<circle cx="{P2[0]}" cy="{P2[1]}" r="34" fill="{INK}" fill-opacity=".15" stroke="{INK}" '
         f'stroke-opacity=".78" stroke-width="2.6"/>')
g.append(f'<g stroke="{INK}" stroke-opacity=".5" stroke-width="1.8" fill="none">'
         f'<path d="M{BC[0]-18:.1f} {BC[1]} h36"/><path d="M{BC[0]:.1f} {BC[1]-18} v36"/>'
         f'<circle cx="{BC[0]:.1f}" cy="{BC[1]:.1f}" r="13"/></g>')
# halo orbit about L2
g.append(f'<ellipse cx="{L2[0]:.1f}" cy="{L2[1]:.1f}" rx="58" ry="112" fill="none" stroke="{VIOLET}" '
         f'stroke-opacity=".85" stroke-width="3" transform="rotate(-24 {L2[0]:.1f} {L2[1]:.1f})"/>')
g.append(f'<ellipse cx="{L1[0]:.1f}" cy="{L1[1]:.1f}" rx="42" ry="80" fill="none" stroke="{VIOLET}" '
         f'stroke-opacity=".40" stroke-width="2" stroke-dasharray="8 9" '
         f'transform="rotate(-24 {L1[0]:.1f} {L1[1]:.1f})"/>')
g.append('</g>')
o += g

def node(p, name, col, r=15, stable=False):
    s = (f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{col}" fill-opacity=".95"/>'
         f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r+18}" fill="none" stroke="{col}" '
         f'stroke-opacity=".5" stroke-width="2"'
         + (' stroke-dasharray="6 7"' if not stable else '') + '/>')
    return s

for p, col in ((L1, AMBER), (L2, AMBER), (L3, AMBER)):
    o.append(node(p, "", col))
for p in (L4, L5):
    o.append(node(p, "", GREEN, 16, stable=True))

o.append(txt(L1[0], L1[1]-52, "L₁", 26, .9, AMBER, anchor="middle"))
o.append(txt(L2[0], L2[1]-52, "L₂", 26, .9, AMBER, anchor="middle"))
o.append(txt(L3[0], L3[1]-52, "L₃", 26, .9, AMBER, anchor="middle"))
o.append(txt(L4[0]+46, L4[1]+10, "L₄", 26, .9, GREEN))
o.append(txt(L5[0]+46, L5[1]+10, "L₅", 26, .9, GREEN))
o.append(txt(P1[0], P1[1]+130, "M₁  EARTH", 21, .60, INK, anchor="middle"))
o.append(txt(P2[0], P2[1]+78, "M₂  MOON", 21, .60, INK, anchor="middle"))
o.append(txt(BC[0]-14, BC[1]+56, "BARYCENTRE", 17, .42, INK_DIM, anchor="middle"))

o.append(dim(P1[0], P1[1], P2[0], P2[1], "a = 384 400 km", off=-500))
o.append(dim(P1[0], P1[1], L4[0], L4[1], "a", off=58, size=24))
o.append(dim(P2[0], P2[1], L4[0], L4[1], "a", off=-58, size=24))
o.append(dim(P1[0], P1[1], L5[0], L5[1], "a", off=-58, size=24))
o.append(dim(P2[0], P2[1], L5[0], L5[1], "a", off=58, size=24))
o.append(dim(P1[0], P1[1], L1[0], L1[1], "326 400 km", off=190))

# 60° angle mark at the primary
o.append(f'<path d="M{P1[0]+210} {P1[1]} A 210 210 0 0 0 {P1[0]+210*math.cos(math.radians(-60)):.1f} '
         f'{P1[1]+210*math.sin(math.radians(-60)):.1f}" fill="none" stroke="{GREEN}" stroke-opacity=".6" stroke-width="2"/>')
o.append(txt(P1[0]+238, P1[1]-92, "60°", 21, .70, GREEN))

o.append(callout(L2[0]+58, L2[1]-90, 2300, 470, [
    "L₂ HALO — NORTHERN FAMILY", "A_z = 68 000 km   T = 14.8 d",
    "STATION-KEEPING ≈ 2 m/s·yr⁻¹"], col=VIOLET))
o.append(callout(L1[0], L1[1]+33, 2300, 760, [
    "L₁ — COLLINEAR, UNSTABLE", "λ = ±2.9321  saddle × centre"], col=AMBER))
o.append(callout(L4[0], L4[1]-34, 1000, 400, [
    "L₄ — TRIANGULAR, STABLE", "STABLE FOR μ < 0.038520",
    "TADPOLE LIBRATION  T = 89 d"], col=GREEN, anchor="end"))
o.append(callout(L5[0], L5[1]+34, 1000, 1520, [
    "L₅ — TRIANGULAR, STABLE", "EQUILATERAL WITH M₁ AND M₂"], col=GREEN, anchor="end"))
o.append(callout(L3[0], L3[1]+33, 690, 1180, [
    "L₃ — COLLINEAR, UNSTABLE", "r = 381 675 km  (anti-Moon)"], col=AMBER, anchor="end"))

o.append(f'<g stroke="{INK}" stroke-opacity=".22" stroke-width="1.5" fill="none">'
         f'<rect x="2280" y="960" width="506" height="196"/></g>')
o.append(txt(2302, 1002, "COLLINEAR ROOT", 19, .5, INK, ls=3))
o.append(txt(2302, 1058, "ξ⁵ ∓ (3−μ)ξ⁴ + (3−2μ)ξ³", 22, .80, INK, ls=.4))
o.append(txt(2302, 1094, "  − μξ² ∓ 2μξ − μ = 0", 22, .80, INK, ls=.4))
o.append(txt(2302, 1134, "SOLVED BY NEWTON–RAPHSON", 17, .40, INK))

o.append(block(150, 1450, [
    "μ = m₂/(m₁+m₂) . . 0.0121505856",
    "JACOBI C(L₁) . . . 3.20034",
    "JACOBI C(L₂) . . . 3.18416",
    "JACOBI C(L₄,₅) . . 2.98800",
    "SYNODIC PERIOD . . 29.53 d",
], 21, 33, .48))

o.append(title_block(1980, 1440, "SHEET 04 — LIBRATION", [
    ("SYSTEM", "EARTH–MOON CR3BP"), ("FRAME", "SYNODIC, ROTATING"),
    ("MODEL", "CIRCULAR RESTRICTED"), ("DRAWN", "APOAPSIS DRAFTING"),
], w=800))
o.append(tail())
open("s4.svg", "w").write("".join(o))
