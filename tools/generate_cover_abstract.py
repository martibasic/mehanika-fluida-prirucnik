"""Generate the minimal abstract cover motif assets/cover/vrtlozna_staza.svg.

Streamlines of a Karman vortex street, seen by an observer who moves with
the vortices: two staggered rows of point vortices of opposite sign (spacing
a, rows h apart, h/a = 0.281, von Karman's stable ratio) in a uniform stream.
Closed streamlines around each vortex form the "cat's eyes"; the open ones
weave between them. The band fades in from the left and out to the right.

Every line is an exact contour of the stream function

    psi = U y - G/(4 pi) ln[(cosh k(y - h/2) - cos kx)
                            / (cosh k(y + h/2) - cos k(x - a/2))],  k = 2 pi / a.

Presentation only, no labels.

Run: python tools/generate_cover_abstract.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cover" / "vrtlozna_staza.svg"

INK, ACCENT = "#2f3b46", "#b35d27"
A = 60.0                      # vortex spacing (drawing units, motif 300 wide)
H = 0.281 * A                 # distance between the rows
G = 1.0                       # vortex strength
U = -0.5 * G / A              # stream in the vortex frame
W, Y = 300.0, 34.0            # drawing width, half height
STEP = 0.05                   # psi between neighbouring lines
RMIN = 4.6                    # leave out loops tighter than this


def psi(x, y):
    k = 2 * math.pi / A
    top = np.cosh(k * (y - H / 2)) - np.cos(k * x)
    bot = np.cosh(k * (y + H / 2)) - np.cos(k * (x - A / 2))
    return U * y - G / (4 * math.pi) * np.log(top / bot)


def fade(x):
    """Opacity along the band: in from the left, out to the right."""
    t = np.clip(x / W, 0, 1)
    return np.clip(np.minimum(t / 0.18, (1 - t) / 0.30), 0, 1) ** 1.3


def fmt(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def contours():
    xs = np.linspace(-A / 4, W + A / 4, 1500)
    ys = np.linspace(-Y, Y, 600)
    X, Yg = np.meshgrid(xs, ys)
    with np.errstate(divide="ignore"):          # psi is infinite at the vortex centres
        P = psi(X, Yg)
    centre = 0.0                  # the line through the middle of the street
    levels = [centre + STEP * i for i in range(-12, 13)]
    fig = plt.figure()
    cs = plt.contour(X, Yg, P, levels=levels)
    out = []
    for level, segs in zip(cs.levels, cs.allsegs):
        n = round((level - centre) / STEP)
        for seg in segs:
            span = max(np.ptp(seg[:, 0]), np.ptp(seg[:, 1]))
            closed = np.hypot(*(seg[0] - seg[-1])) < 1.0
            through = np.ptp(seg[:, 0]) > 0.9 * W      # open line across the drawing
            if span > 2 * RMIN and (closed or through):
                out.append((n, seg))
    plt.close(fig)
    return out


def build() -> str:
    stops = "".join(f'<stop offset="{t:.2f}" stop-color="#fff" stop-opacity="{float(fade(t * W)):.3f}"/>'
                    for t in np.linspace(0, 1, 21))
    lines = contours()
    top = Y - max(float(seg[:, 1].max()) for _, seg in lines) - 2.0
    height = 2 * (Y - top)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {fmt(top)} {fmt(W)} {fmt(height)}" '
         'role="img" aria-label="Ukrasni apstraktni motiv: strujnice Kármánove vrtložne '
         'staze, dva niza vrtloga suprotnog smjera vrtnje.">',
         '<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" '
         f'x2="{fmt(W)}" y2="0">{stops}</linearGradient>'
         f'<mask id="m" maskUnits="userSpaceOnUse" x="-5" y="-5" width="{fmt(W + 10)}" '
         f'height="{fmt(2 * Y + 10)}"><rect x="-5" y="-5" width="{fmt(W + 10)}" '
         f'height="{fmt(2 * Y + 10)}" fill="url(#g)"/></mask></defs>',
         '<g mask="url(#m)" fill="none" stroke-linecap="round" stroke-linejoin="round">']
    accent = []
    for n, seg in lines:
        d = "M" + " L".join(f"{fmt(px)} {fmt(Y - py)}" for px, py in seg[::2])
        if n == 0:
            accent.append(f'<path d="{d}" stroke="{ACCENT}" stroke-width="0.9"/>')
        else:
            op = 0.85 - 0.04 * abs(n)
            s.append(f'<path d="{d}" stroke="{INK}" stroke-opacity="{op:.2f}" '
                     f'stroke-width="{0.6 - 0.02 * abs(n):.2f}"/>')
    s += accent + ["</g>", "</svg>"]
    return "\n".join(s) + "\n"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8", newline="\n")
    print(f"{OUT.relative_to(ROOT).as_posix()} written")


if __name__ == "__main__":
    sys.exit(main())
