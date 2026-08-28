"""Lock-screen glyph: sheet 1 in miniature, drawn in the same language."""
import math
from common import INK, INK_DIM, AMBER, GREEN, BG_EDGE, FONT

W, H = 880, 660
cx, cy = 414, 300
r1, r2 = 96, 268
a = (r1 + r2) / 2
c = a - r1
b = math.sqrt(a*a - c*c)
ex = cx + c
peri, apo = (cx - r1, cy), (cx + r2, cy)
sat = (ex + a*math.cos(math.radians(215)), cy + b*math.sin(math.radians(215)))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><filter id="s" x="-8%" y="-8%" width="116%" height="116%">
<feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="5" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G"/>
</filter></defs>
<g filter="url(#s)" fill="none" stroke-linecap="round">
  <circle cx="{cx}" cy="{cy}" r="{r1}" stroke="{INK}" stroke-opacity=".55" stroke-width="3.5" stroke-dasharray="12 9"/>
  <circle cx="{cx}" cy="{cy}" r="{r2}" stroke="{INK}" stroke-opacity=".45" stroke-width="3.5" stroke-dasharray="12 9"/>
  <circle cx="{cx}" cy="{cy}" r="40" stroke="{INK}" stroke-opacity=".85" stroke-width="4" fill="{INK}" fill-opacity=".14"/>
  <path d="M{cx-26} {cy} h52" stroke="{INK}" stroke-opacity=".7" stroke-width="3"/>
  <path d="M{cx} {cy-26} v52" stroke="{INK}" stroke-opacity=".7" stroke-width="3"/>
  <path d="M{peri[0]} {peri[1]} A {a:.1f} {b:.1f} 0 0 1 {apo[0]} {apo[1]}" stroke="{AMBER}" stroke-opacity=".95" stroke-width="5"/>
  <path d="M{peri[0]} {peri[1]} A {a:.1f} {b:.1f} 0 0 0 {apo[0]} {apo[1]}" stroke="{AMBER}" stroke-opacity=".26" stroke-width="2.5" stroke-dasharray="9 11"/>
  <path d="M{peri[0]-52} {cy} H{apo[0]+52}" stroke="{INK_DIM}" stroke-opacity=".45" stroke-width="2" stroke-dasharray="24 7 4 7"/>
</g>
<circle cx="{peri[0]}" cy="{peri[1]}" r="12" fill="{AMBER}"/>
<circle cx="{peri[0]}" cy="{peri[1]}" r="25" fill="none" stroke="{AMBER}" stroke-opacity=".55" stroke-width="2.5"/>
<circle cx="{apo[0]}" cy="{apo[1]}" r="12" fill="{AMBER}"/>
<circle cx="{apo[0]}" cy="{apo[1]}" r="25" fill="none" stroke="{AMBER}" stroke-opacity=".55" stroke-width="2.5"/>
<circle cx="{sat[0]:.1f}" cy="{sat[1]:.1f}" r="10" fill="{GREEN}"/>
<g stroke="{INK}" stroke-opacity=".5" stroke-width="2" fill="none">
  <path d="M{peri[0]} {cy+r2+34} v-26"/><path d="M{apo[0]} {cy+r2+34} v-26"/>
  <path d="M{peri[0]} {cy+r2+22} H{apo[0]}"/>
</g>
<polygon points="{peri[0]+13},{cy+r2+22} {peri[0]+1},{cy+r2+18} {peri[0]+1},{cy+r2+26}" fill="{INK}" fill-opacity=".6"/>
<polygon points="{apo[0]-13},{cy+r2+22} {apo[0]-1},{cy+r2+18} {apo[0]-1},{cy+r2+26}" fill="{INK}" fill-opacity=".6"/>
<text x="{(peri[0]+apo[0])/2:.0f}" y="{cy+r2+62}" font-family="{FONT}"
      font-size="24" letter-spacing="3" fill="{INK}" fill-opacity=".62" text-anchor="middle">2a</text>
</svg>'''
open("unlock.svg", "w").write(svg)
