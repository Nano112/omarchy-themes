import math
from common import *

OX, OY, R, S = 1440, 5600, 4200, 3.4      # planet centre, radius, px per km altitude
PHI0, PHI1 = -0.200, 0.163
WV = 0.06                                  # vertical-rise fraction

def at(h, phi):
    r = R + S*h
    return (OX + r*math.sin(phi), OY - r*math.cos(phi))

def arc(h, x0=210, x1=2670, n=200):
    r = R + S*h
    a0 = math.asin(max(min((x0-OX)/r, 1), -1))
    a1 = math.asin(max(min((x1-OX)/r, 1), -1))
    return [at(h, a0 + (a1-a0)*k/n) for k in range(n+1)]

def poly(ps, col, op, w, dash=None):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in ps)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"{da}/>'

def traj(w):
    """Vertical rise, then a pitch-over that flattens as it approaches insertion."""
    h = 18.0*(w/WV) if w <= WV else 18.0 + 182.0*((w-WV)/(1-WV))**0.62
    phi = PHI0 + (PHI1-PHI0) * (max(w-0.03, 0.0)/0.97)**1.35
    return at(h, phi), h

o = [head(seed=77, freq=0.008, scale=3.6), frame()]
o.append(sheet_header("ASCENT PROFILE",
                      "GRAVITY-TURN TRAJECTORY  /  TWO-STAGE TO 200 KM CIRCULAR  ·  i = 28.5°",
                      "SHEET 5 OF 5    REV C    ALT ×3.4 PX·KM⁻¹"))

g = ['<g filter="url(#sketchsoft)">']
body = arc(0) + [(2670, 1790), (210, 1790)]
g.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in body)}" fill="{INK}" fill-opacity=".05"/>')
for h, op, w, dash in ((12, .26, 1.7, "12 10"), (50, .22, 1.6, "10 12"), (85, .20, 1.6, "8 12"),
                       (100, .48, 2.2, "22 10"), (200, .28, 1.8, "6 14")):
    g.append(poly(arc(h), AMBER if h == 100 else INK, op, w, dash))
g.append(poly(arc(0), INK, .80, 3.4))
g.append(f'<g stroke="{INK_DIM}" stroke-opacity=".13" stroke-width="1.3" fill="none">')
for k in range(-5, 6):
    a, b = at(-40, k*0.05), at(235, k*0.05)
    g.append(f'<path d="M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f}"/>')
g.append('</g>')
g.append(poly([traj(k/500)[0] for k in range(501)], GREEN, .92, 4.2))
g.append('</g>')
o += g

def on_arc(h, x):
    r = R + S*h
    return at(h, math.asin((x-OX)/r))

for h, lab in ((12, "12 km   TROPOPAUSE"), (50, "50 km   STRATOPAUSE"), (85, "85 km   MESOPAUSE"),
               (100, "100 km   KÁRMÁN LINE"), (200, "200 km   INSERTION ALTITUDE")):
    p = on_arc(h, 1700)
    col = AMBER if h == 100 else INK
    o.append(f'<rect x="{p[0]-8:.0f}" y="{p[1]-32:.0f}" width="{len(lab)*11.4+16:.0f}" height="28" '
             f'fill="{BG_EDGE}" fill-opacity=".72"/>')
    o.append(txt(p[0]+2, p[1]-12, lab, 18, .58 if h == 100 else .40, col))

EVENTS = [
    (0.000, "LIFTOFF",         ["T+00:00:00", "h 0.0 km    v 0.000 km/s", "TWR 1.34   9 × MERLIN 1D"], AMBER, 560, 1352, "end"),
    (0.055, "MAX-Q",           ["T+00:01:12", "h 16.5 km   v 0.482 km/s", "q 33.7 kPa   M 1.42"],      AMBER, 560, 1132, "end"),
    (0.300, "MECO / STAGE SEP",["T+00:02:38", "h 95.8 km   v 2.354 km/s", "SEP +4 s   RTLS BOOSTBACK"],AMBER, 930, 620,  "start"),
    (0.520, "FAIRING JETTISON",["T+00:03:24", "h 136.2 km  v 3.081 km/s", "free-molecular flow"],       INK,   1560, 600,  "start"),
    (1.000, "SECO / INSERTION",["T+00:08:44", "h 200.0 km  v 7.784 km/s", "e 0.0003   i 28.50°"],       GREEN, 2270, 1130, "start"),
]
for w, name, lines, col, tx, ty, an in EVENTS:
    p, h = traj(w)
    o.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="13" fill="{col}" fill-opacity=".95"/>')
    o.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="27" fill="none" stroke="{col}" '
             f'stroke-opacity=".5" stroke-width="2"/>')
    o.append(callout(p[0], p[1], tx, ty, [name] + lines, size=20, lh=28, col=col, anchor=an,
                     plate=(w < 0.1 or w > 0.9)))

pI, pP = traj(1.0)[0], traj(0.99)[0]
ang = math.atan2(pI[1]-pP[1], pI[0]-pP[0])
o.append(vector(pI[0], pI[1], pI[0]+128*math.cos(ang), pI[1]+128*math.sin(ang), GREEN, .8, 2.8))

IX, IY, IW, IH = 250, 400, 620, 330
o.append(f'<g stroke="{INK}" stroke-opacity=".26" stroke-width="1.5" fill="none">'
         f'<rect x="{IX}" y="{IY}" width="{IW}" height="{IH}"/></g>')
o.append(f'<g stroke="{INK}" stroke-opacity=".10" stroke-width="1.2" fill="none">')
for k in range(1, 6): o.append(f'<path d="M{IX+IW*k/6:.0f} {IY} v{IH}"/>')
for k in range(1, 4): o.append(f'<path d="M{IX} {IY+IH*k/4:.0f} h{IW}"/>')
o.append('</g>')
o.append(txt(IX+16, IY+30, "VELOCITY / ALTITUDE vs TIME", 18, .5, INK, ls=2.6))
o.append(poly([(IX+IW*k/120, IY+IH-IH*0.84*((k/120)**2.1*0.42 + (k/120)*0.58)) for k in range(121)], GREEN, .85, 2.8))
o.append(poly([(IX+IW*k/120, IY+IH-IH*0.78*((k/120)**1.55)) for k in range(121)], AMBER, .68, 2.4, "9 8"))
o.append(txt(IX+16, IY+IH-16, "T+0", 16, .40, INK))
o.append(txt(IX+IW-16, IY+IH-16, "T+8:44", 16, .40, INK, anchor="end"))
o.append(txt(IX+IW-16, IY+54, "──  v          ╌╌  h", 16, .45, INK, anchor="end"))

o.append(f'<g stroke="{INK}" stroke-opacity=".24" stroke-width="1.5" fill="none">'
         f'<rect x="2160" y="300" width="626" height="350"/><path d="M2160 386 h626"/></g>')
o.append(txt(2182, 366, "VEHICLE / STAGING", 19, .55, INK, ls=3))
for i, (k, v) in enumerate([("GLOW", "549 054 kg"), ("STAGE 1 Isp", "282 s (SL)"),
                            ("STAGE 2 Isp", "348 s (VAC)"), ("BURN 1", "162 s"),
                            ("PAYLOAD", "15 600 kg"), ("MARGIN", "+4.2 %")]):
    y = 428 + i*44
    o.append(txt(2182, y, k, 20, .52, INK))
    o.append(txt(2764, y, v, 20, .76, INK, anchor="end"))

o.append(txt(1420, 300, "Δv BUDGET", 19, .5, INK, ls=3))
o.append(f'<path d="M1420 314 h404" stroke="{INK}" stroke-opacity=".24" stroke-width="1.4"/>')
o.append(block(1420, 352, [
    "Δv IDEAL . . . . .  9 402 m/s",
    "GRAVITY LOSS . . .  1 214 m/s",
    "DRAG LOSS  . . . .    142 m/s",
    "EARTH ROT. GAIN  . −  408 m/s",
], 20, 32, .50))

o.append(title_block(1960, 1462, "SHEET 05 — ASCENT", [
    ("PAD", "LC-39A  28.608°N"), ("AZIMUTH", "44.9° TRUE"),
    ("TARGET", "200 km × 200 km"), ("DRAWN", "APOAPSIS DRAFTING"),
], w=800))
o.append(tail())
open("s5.svg", "w").write("".join(o))
