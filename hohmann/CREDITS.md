# Hohmann

A monochrome drafting theme: graphite paper, white ink, and colour reserved for
what the sheets actually annotate — amber for burns and callouts, green for the
live trajectory, violet for swept area and halo orbits.

Every background is an original engineering sheet, generated as SVG and rendered
at 2880×1800. Nothing is traced or downloaded — the geometry is computed from
the mechanics.

| Sheet | Subject |
|---|---|
| 1 | Hohmann transfer — LEO 400 km → GEO, both burns, vis-viva |
| 2 | Keplerian elements — true / eccentric anomaly, equal-area sectors |
| 3 | Ground track — i = 51.64°, 3.2 revolutions, TLE plate |
| 4 | Libration points — Earth–Moon CR3BP, L₁–L₅, L₂ halo orbit |
| 5 | Ascent profile — two-stage gravity turn to 200 km |

The drawings are correct where it matters: sheet 2's two shaded sectors are
solved numerically to equal area (Kepler II), the L₄/L₅ triangles are truly
equilateral, sheet 3's track is propagated from the spherical-Earth ground-track
equations with the right nodal regression, and sheet 5's trajectory is a real
gravity turn — vertical rise, pitch-over, flattening climb.

The hand-drawn wobble is an SVG feTurbulence + feDisplacementMap filter applied
to the geometry only; text stays crisp.

`unlock.png` is sheet 1 in miniature, drawn in the same language.

Source and build instructions: `~/code/omarchy-themes`.
