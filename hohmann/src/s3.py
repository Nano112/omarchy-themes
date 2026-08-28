import math
from common import *

MX, MY, MW, MH = 260, 396, 1960, 940
INC, PER, SIDEREAL = 51.6386, 92.68, 1436.07

def xy(lon, lat):
    return (MX + (lon + 180.0) / 360.0 * MW, MY + (90.0 - lat) / 180.0 * MH)

def track(t):
    th = 2*math.pi * t / PER
    lat = math.degrees(math.asin(math.sin(math.radians(INC)) * math.sin(th)))
    lon = -74.0 + math.degrees(math.atan2(math.cos(math.radians(INC))*math.sin(th), math.cos(th))) \
          - 360.0 * t / SIDEREAL
    return ((lon + 180.0) % 360.0 - 180.0, lat)

o = [head(seed=41, freq=0.008, scale=3.4), frame()]
o.append(sheet_header("GROUND TRACK",
                      "SUB-SATELLITE PATH  /  i = 51.64°  ·  h = 408 km  ·  3.2 REVOLUTIONS",
                      "SHEET 3 OF 5    REV C    PLATE CARRÉE"))

g = [f'<g filter="url(#sketchsoft)">']
g.append(f'<rect x="{MX}" y="{MY}" width="{MW}" height="{MH}" fill="{INK}" fill-opacity=".025" '
         f'stroke="{INK}" stroke-opacity=".42" stroke-width="2.4"/>')
g.append(f'<g stroke="{INK}" stroke-opacity=".16" stroke-width="1.3" fill="none">')
for lon in range(-165, 180, 15):
    x = xy(lon, 0)[0]
    g.append(f'<path d="M{x:.1f} {MY} V{MY+MH}"/>')
for lat in range(-75, 90, 15):
    y = xy(0, lat)[1]
    g.append(f'<path d="M{MX} {y:.1f} H{MX+MW}"/>')
g.append('</g>')
g.append(f'<g stroke="{INK}" stroke-opacity=".34" stroke-width="1.8" fill="none">')
for lon in (-120, -60, 0, 60, 120):
    x = xy(lon, 0)[0]; g.append(f'<path d="M{x:.1f} {MY} V{MY+MH}"/>')
for lat in (-60, -30, 30, 60):
    y = xy(0, lat)[1]; g.append(f'<path d="M{MX} {y:.1f} H{MX+MW}"/>')
g.append('</g>')
# equator + inclination envelope
g.append(f'<path d="M{MX} {xy(0,0)[1]:.1f} H{MX+MW}" stroke="{INK}" stroke-opacity=".62" stroke-width="2.6" fill="none"/>')
for lat in (INC, -INC):
    y = xy(0, lat)[1]
    g.append(f'<path d="M{MX} {y:.1f} H{MX+MW}" stroke="{AMBER}" stroke-opacity=".30" '
             f'stroke-width="1.8" stroke-dasharray="14 10" fill="none"/>')

# the track itself, split on the ±180° seam
seg, prev = [], None
N = 1500
for k in range(N+1):
    t = 3.2 * PER * k / N
    lon, lat = track(t)
    if prev is not None and abs(lon - prev) > 180:
        g.append(f'<polyline points="{" ".join(seg)}" fill="none" stroke="{GREEN}" '
                 f'stroke-opacity=".92" stroke-width="3.4" stroke-linejoin="round"/>')
        seg = []
    p = xy(lon, lat); seg.append(f"{p[0]:.1f},{p[1]:.1f}"); prev = lon
g.append(f'<polyline points="{" ".join(seg)}" fill="none" stroke="{GREEN}" '
         f'stroke-opacity=".92" stroke-width="3.4" stroke-linejoin="round"/>')
g.append('</g>')
o += g

# ascending nodes
for r in range(4):
    lon, lat = track(r * PER)
    p = xy(lon, lat)
    if MX < p[0] < MX+MW:
        o.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="9" fill="none" stroke="{AMBER}" '
                 f'stroke-opacity=".9" stroke-width="2.4"/>')


# ground station + access footprint
ST = xy(-106.6, 32.5)
FR = 21.0 / 180.0 * MH
o.append(f'<circle cx="{ST[0]:.1f}" cy="{ST[1]:.1f}" r="{FR:.1f}" fill="{AMBER}" fill-opacity=".07" '
         f'stroke="{AMBER}" stroke-opacity=".55" stroke-width="2" stroke-dasharray="9 9"/>')
o.append(f'<g stroke="{AMBER}" stroke-opacity=".9" stroke-width="2.4" fill="none">'
         f'<path d="M{ST[0]-16:.1f} {ST[1]:.1f} h32"/><path d="M{ST[0]:.1f} {ST[1]-16:.1f} v32"/></g>')

# graticule labels
for lon in range(-180, 181, 60):
    x = xy(lon, 0)[0]
    o.append(txt(x, MY+MH+34, f"{abs(lon)}°{'' if lon==0 else ('E' if lon>0 else 'W')}", 18, .45, INK, anchor="middle"))
for lat in range(-60, 90, 30):
    y = xy(0, lat)[1]
    o.append(txt(MX-18, y+7, f"{abs(lat)}°{'' if lat==0 else ('N' if lat>0 else 'S')}", 18, .45, INK, anchor="end"))

o.append(callout(*xy(-106.6, 32.5+21), 700, 330, [
    "GROUND STATION  WSMR-01", "32.500°N  106.600°W  el 1 216 m",
    "ACCESS ≥ 5° ELEV  ·  4 PASSES / DAY"], col=AMBER, anchor="end"))
lon, lat = track(1.60*PER); p = xy(lon, lat)
o.append(callout(p[0], p[1], 2300, 1140, [
    "REV 2  ·  DESCENDING NODE", "λ = 22.4°E   φ = 0.0°", "t = 02h 28m 20s"], col=GREEN))
lon, lat = track(0)
o.append(callout(*xy(lon, lat), 700, 1268, [
    "ASCENDING NODE  ·  REV 0", "λ = 74.000°W   Ω = 339.7367°"], col=AMBER, anchor="end"))
o.append(callout(MX+MW-40, xy(0, INC)[1], 2320, 300, [
    "LATITUDE ENVELOPE", "φ_max = ± i = ± 51.6386°"], col=AMBER))

# TLE plate
TY = 1444
o.append(f'<g stroke="{INK}" stroke-opacity=".26" stroke-width="1.5" fill="none">'
         f'<rect x="{MX}" y="{TY}" width="1330" height="176"/><path d="M{MX} {TY+46} h1330"/></g>')
o.append(txt(MX+20, TY+32, "TWO-LINE ELEMENT SET  ·  NORAD 25544", 19, .52, INK, ls=3))
o.append(block(MX+20, TY+84, [
    "1 25544U 98067A   26240.51782528  .00016717  00000+0  10270-3 0  9008",
    "2 25544  51.6386 339.7367 0006703  92.8340 267.3124 15.49309239 12345",
], 19, 34, .66))
o.append(txt(MX+20, TY+156, "CHECKSUM OK   ·   PROPAGATOR SGP4   ·   DRAG B* = 1.0270E-4", 17, .38, INK))

o.append(f'<g stroke="{INK}" stroke-opacity=".24" stroke-width="1.5" fill="none">'
         f'<rect x="2280" y="440" width="510" height="404"/><path d="M2280 486 h510"/></g>')
o.append(txt(2300, 472, "PASS PREDICTION", 19, .52, INK, ls=3))
for i, (k, v) in enumerate([("REV 1", "07:14:02"), ("REV 2", "08:46:40"), ("REV 3", "10:19:18"),
                            ("MAX EL", "78.4°"), ("DURATION", "09m 41s"), ("RANGE", "412 km"),
                            ("DOPPLER", "±48.2 kHz")]):
    y = 524 + i*46
    o.append(txt(2300, y, k, 20, .52, INK))
    o.append(txt(2770, y, v, 20, .76, INK, anchor="end"))

o.append(block(2280, 940, [
    "PERIOD . . . 92m 41s",
    "APOGEE . . . 421 km",
    "PERIGEE  . . 408 km",
    "MEAN MOT . . 15.4931",
    "NODAL REG. . −5.02°/day",
], 20, 33, .48))

o.append(title_block(1980, 1444, "SHEET 03 — TRACK", [
    ("EPOCH", "2026-08-28 T 12:25Z"), ("FRAME", "ECEF WGS-84"),
    ("PROJECTION", "PLATE CARRÉE"), ("DRAWN", "APOAPSIS DRAFTING"),
], w=800))
o.append(tail())
open("s3.svg", "w").write("".join(o))
