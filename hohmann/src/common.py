# Shared blueprint drafting primitives for the Hohmann theme wallpapers.
import math

W, H = 2880, 1800
FONT = "JetBrainsMono Nerd Font, JetBrainsMono NF, monospace"

BG_MID   = "#141416"   # paper, centre of the vignette
BG_EDGE  = "#050506"   # paper, edges
INK      = "#DEDEE2"   # primary drafting ink
INK_DIM  = "#82828A"   # construction lines
AMBER    = "#F0A45E"   # burns / critical callouts
GREEN    = "#5FD3A0"   # nominal markers / live trajectory
VIOLET   = "#BF9BE0"   # swept area / halo orbits

def head(seed=7, freq=0.010, scale=4.5):
    """SVG preamble: paper, grid, and the hand-drawn displacement filter."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <radialGradient id="paper" cx="46%" cy="44%" r="78%">
    <stop offset="0%" stop-color="{BG_MID}"/><stop offset="100%" stop-color="{BG_EDGE}"/>
  </radialGradient>
  <filter id="sketch" x="-6%" y="-6%" width="112%" height="112%">
    <feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="3" seed="{seed}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="{scale}" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="sketchsoft" x="-6%" y="-6%" width="112%" height="112%">
    <feTurbulence type="fractalNoise" baseFrequency="0.008" numOctaves="2" seed="{seed+3}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <pattern id="fine" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0 L0 0 0 40" fill="none" stroke="{INK}" stroke-opacity=".055" stroke-width="1"/>
  </pattern>
  <pattern id="coarse" width="200" height="200" patternUnits="userSpaceOnUse">
    <path d="M200 0 L0 0 0 200" fill="none" stroke="{INK}" stroke-opacity=".10" stroke-width="1.3"/>
  </pattern>
</defs>
<rect width="{W}" height="{H}" fill="url(#paper)"/>
<rect width="{W}" height="{H}" fill="url(#fine)"/>
<rect width="{W}" height="{H}" fill="url(#coarse)"/>
'''

def frame():
    """Drafting border with corner ticks."""
    m, o = 90, 118
    s = f'<g fill="none" stroke="{INK}" stroke-opacity=".26" stroke-width="1.6">'
    s += f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}"/>'
    s += f'<rect x="{o}" y="{o}" width="{W-2*o}" height="{H-2*o}" stroke-opacity=".13"/></g>'
    # edge zone ticks, the way a real sheet is indexed
    s += f'<g stroke="{INK}" stroke-opacity=".20" stroke-width="1.4">'
    for i in range(1, 8):
        x = m + (W - 2*m) * i / 8
        s += f'<path d="M{x:.0f} {m} v28"/><path d="M{x:.0f} {H-m} v-28"/>'
    for i in range(1, 5):
        y = m + (H - 2*m) * i / 5
        s += f'<path d="M{m} {y:.0f} h28"/><path d="M{W-m} {y:.0f} h-28"/>'
    return s + '</g>'

def txt(x, y, s, size=22, op=.72, col=None, anchor="start", ls=1.6, weight="400"):
    col = col or INK
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'letter-spacing="{ls}" fill="{col}" fill-opacity="{op}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')

def block(x, y, lines, size=21, lh=30, op=.62, col=None, anchor="start"):
    return "".join(txt(x, y + i*lh, l, size, op, col, anchor) for i, l in enumerate(lines) if l != "")

def arrowhead(x, y, ang, col, op=.8, k=13):
    """Filled triangular head pointing along ang (radians)."""
    p = []
    for d, r in ((0, k), (2.6, k*0.62), (-2.6, k*0.62)):
        p.append(f"{x + r*math.cos(ang+d):.1f},{y + r*math.sin(ang+d):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="{col}" fill-opacity="{op}"/>'

def vector(x1, y1, x2, y2, col=None, op=.8, w=2.2, dash=None):
    col = col or INK
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ang = math.atan2(y2-y1, x2-x1)
    sx, sy = x2 - 11*math.cos(ang), y2 - 11*math.sin(ang)
    return (f'<path d="M{x1:.1f} {y1:.1f} L{sx:.1f} {sy:.1f}" stroke="{col}" stroke-opacity="{op}" '
            f'stroke-width="{w}" fill="none" stroke-linecap="round"{d}/>' + arrowhead(x2, y2, ang, col, op))

def dim(x1, y1, x2, y2, label, off=0, size=20, col=None, op=.55, side=1):
    """Dimension line: ticks at both ends, arrows inward, label on the line."""
    col = col or INK_DIM
    ang = math.atan2(y2-y1, x2-x1)
    nx, ny = -math.sin(ang)*off, math.cos(ang)*off
    ax1, ay1, ax2, ay2 = x1+nx, y1+ny, x2+nx, y2+ny
    s = f'<g stroke="{col}" stroke-opacity="{op}" fill="none" stroke-width="1.5">'
    if off:
        s += f'<path d="M{x1:.1f} {y1:.1f} L{ax1:.1f} {ay1:.1f}"/><path d="M{x2:.1f} {y2:.1f} L{ax2:.1f} {ay2:.1f}"/>'
    s += f'<path d="M{ax1:.1f} {ay1:.1f} L{ax2:.1f} {ay2:.1f}"/></g>'
    s += arrowhead(ax1, ay1, ang+math.pi, col, op, 10) + arrowhead(ax2, ay2, ang, col, op, 10)
    mx, my = (ax1+ax2)/2, (ay1+ay2)/2
    deg = math.degrees(ang)
    if deg > 90 or deg < -90: deg += 180
    s += (f'<g transform="translate({mx:.1f},{my:.1f}) rotate({deg:.1f})">'
          f'<rect x="-{len(label)*size*0.34:.0f}" y="-{size*0.85:.0f}" width="{len(label)*size*0.68:.0f}" '
          f'height="{size*1.15:.0f}" fill="{BG_EDGE}" fill-opacity=".62"/>'
          + txt(0, size*0.03, label, size, .78, col, "middle") + '</g>')
    return s

def callout(px, py, tx, ty, lines, size=21, lh=29, col=None, op=.68, anchor="start", rule=True, plate=False):
    """Leader line from a point on the drawing to an annotation block."""
    col = col or INK
    stub = 34 if anchor == "start" else -34
    s = (f'<g stroke="{col}" stroke-opacity="{op*0.65}" stroke-width="1.5" fill="none" stroke-linecap="round">'
         f'<path d="M{px:.1f} {py:.1f} L{tx:.1f} {ty:.1f} l{stub} 0"/></g>'
         f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.6" fill="{col}" fill-opacity="{op}"/>')
    bx = tx + stub
    ty0 = ty - 12
    if plate:
        pw = max(len(l) for l in lines) * size * 0.63
        px0 = bx - 10 if anchor == "start" else bx - pw - 10
        s += (f'<rect x="{px0:.0f}" y="{ty0-size-6:.0f}" width="{pw+20:.0f}" '
              f'height="{lh*len(lines)+size*0.5:.0f}" fill="{BG_EDGE}" fill-opacity=".70"/>')
    if rule:
        wdt = max(len(l) for l in lines) * size * 0.62
        s += (f'<path d="M{bx:.1f} {ty0+7:.1f} h{wdt*(1 if anchor=="start" else -1):.0f}" '
              f'stroke="{col}" stroke-opacity="{op*0.45}" stroke-width="1.3"/>')
    s += block(bx, ty0, lines, size, lh, op, col, anchor)
    return s

def title_block(x, y, title, rows, w=690, size=21):
    """Bottom-corner sheet identification block."""
    rh, hh = 40, 62
    h = hh + rh*len(rows)
    s = (f'<g stroke="{INK}" stroke-opacity=".30" fill="none" stroke-width="1.6">'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>'
         f'<path d="M{x} {y+hh} h{w}"/>')
    for i in range(1, len(rows)):
        s += f'<path d="M{x} {y+hh+rh*i} h{w}" stroke-opacity=".16"/>'
    s += f'<path d="M{x+w*0.42:.0f} {y+hh} v{rh*len(rows)}" stroke-opacity=".16"/></g>'
    s += txt(x+20, y+41, title, 27, .82, INK, ls=3.2, weight="600")
    for i, (k, v) in enumerate(rows):
        yy = y + hh + rh*i + 27
        s += txt(x+20, yy, k, size, .46)
        s += txt(x+w*0.42+20, yy, v, size, .74)
    return s

def sheet_header(title, subtitle, ident):
    s = txt(150, 205, title, 46, .88, INK, ls=8, weight="600")
    s += f'<path d="M150 228 h{len(title)*30}" stroke="{INK}" stroke-opacity=".38" stroke-width="2"/>'
    s += txt(150, 268, subtitle, 23, .48, INK, ls=4.5)
    s += txt(W-150, 205, ident, 23, .46, INK, ls=4.5, anchor="end")
    return s

def ellipse_pt(cx, cy, rx, ry, rot_deg, t_deg):
    t, r = math.radians(t_deg), math.radians(rot_deg)
    x, y = rx*math.cos(t), ry*math.sin(t)
    return (cx + x*math.cos(r) - y*math.sin(r), cy + x*math.sin(r) + y*math.cos(r))

def tail():
    return "</svg>"
