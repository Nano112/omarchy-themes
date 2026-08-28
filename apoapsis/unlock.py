"""Lock-screen glyph: planet, elliptical orbit, satellite, apoapsis marker."""
import math

ACCENT = "#5EA9FF"
W, H = 1000, 520
cx, cy, rx, ry, rot = 500, 260, 420, 150, -20


def pt(t):
    r = math.radians(rot)
    x, y = rx*math.cos(math.radians(t)), ry*math.sin(math.radians(t))
    return (cx + x*math.cos(r) - y*math.sin(r), cy + x*math.sin(r) + y*math.cos(r))


sat, apo = pt(200), pt(0)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><radialGradient id="glow">
  <stop offset="0%" stop-color="{ACCENT}" stop-opacity=".5"/>
  <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
</radialGradient></defs>
<circle cx="{cx}" cy="{cy}" r="205" fill="url(#glow)"/>
<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})"
         fill="none" stroke="{ACCENT}" stroke-width="7" stroke-opacity=".75"/>
<circle cx="{cx}" cy="{cy}" r="96" fill="{ACCENT}" fill-opacity=".92"/>
<circle cx="{cx}" cy="{cy}" r="128" fill="none" stroke="{ACCENT}" stroke-width="5" stroke-opacity=".45"/>
<circle cx="{sat[0]:.1f}" cy="{sat[1]:.1f}" r="21" fill="{ACCENT}"/>
<circle cx="{sat[0]:.1f}" cy="{sat[1]:.1f}" r="42" fill="none" stroke="{ACCENT}" stroke-width="4" stroke-opacity=".5"/>
<circle cx="{apo[0]:.1f}" cy="{apo[1]:.1f}" r="13" fill="{ACCENT}" fill-opacity=".85"/>
</svg>'''
open("unlock.svg", "w").write(svg)
