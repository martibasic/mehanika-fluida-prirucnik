"""Generate the decorative PDF cover motif assets/cover/dim.svg.

A smoke streak rising from the bottom of the page: a laminar column that
turns sinuous and curls into Kelvin-Helmholtz rolls before dispersing. It is
presentation only, carries no labels and uses the wall ink of the sketches.

Run: python tools/generate_cover_motifs.py
"""
from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cover"

WALL = "#3a4a56"


def fmt(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def polyline(points) -> str:
    head, *rest = points
    return "M" + fmt(head[0]) + " " + fmt(head[1]) + "".join(
        " L" + fmt(x) + " " + fmt(y) for x, y in rest)


def smoothstep(a: float, b: float, x: float) -> float:
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def smoke_motif() -> str:
    W, H = 44.0, 500.0
    cx = 20.0
    y_start = H - 2.0                  # the streak fades in from the bottom
    y_lam = 290.0                      # end of the laminar column
    y_end = 8.0

    def filament(dx: float, phase: float, gain: float) -> list[tuple[float, float]]:
        """One smoke streak: straight laminar column, then a sinuous wave
        whose crests overturn into rolls (an epicycle on the wave makes
        y run backwards briefly at each crest), finally spreading out."""
        pts = [(cx + dx * 0.3, y_start)]
        pts += [(cx + dx * (0.3 + 0.7 * smoothstep(y_start, y_lam, y)), y)
                for y in [y_start - i * 2.0 for i in range(1, int((y_start - y_lam) / 2.0))]]
        th, y_base = 0.0, y_lam
        while y_base > y_end:
            h = (y_lam - y_base) / (y_lam - y_end)          # 0 .. 1 above transition
            lam = 34.0 + 30.0 * h                           # wavelength grows upward
            adv = lam / (2 * math.pi)                       # advance per radian
            onset = smoothstep(0.0, 0.3, h)
            curl = smoothstep(0.15, 0.45, h)
            A = gain * (0.3 + 4.6 * onset + 1.6 * smoothstep(0.5, 1.0, h))
            # epicycle radius; above ~0.6*adv the crests roll into loops
            r = gain * adv * (0.2 * onset + 0.85 * curl) * (1 - 0.3 * smoothstep(0.75, 1.0, h))
            spread = dx * (1.0 + 7.0 * smoothstep(0.35, 1.0, h))
            lean = 3.5 * smoothstep(0.4, 1.0, h) ** 1.4
            ph = th + phase
            x = cx + spread + lean + A * math.sin(ph) - r * math.sin(ph) * math.cos(2 * ph)
            y = y_base - r * math.sin(2 * ph)
            pts.append((x, y))
            th += 0.04
            y_base -= adv * 0.04
        return pts

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(W)} {fmt(H)}" '
             'role="img" aria-label="Ukrasni motiv: dim koji se iz laminarnog stupa '
             'kovrča u Kelvin-Helmholtzove vrtloge.">')
    s.append('<defs>'
             f'<linearGradient id="cs_fade" gradientUnits="userSpaceOnUse" x1="0" y1="{fmt(y_start)}" '
             f'x2="0" y2="{fmt(y_end)}"><stop offset="0" stop-color="{WALL}" stop-opacity="0"/>'
             f'<stop offset="0.12" stop-color="{WALL}" stop-opacity="1"/>'
             f'<stop offset="0.45" stop-color="{WALL}" stop-opacity="0.8"/>'
             f'<stop offset="0.8" stop-color="{WALL}" stop-opacity="0.35"/>'
             f'<stop offset="1" stop-color="{WALL}" stop-opacity="0"/></linearGradient>'
             '</defs>')
    for dx, ph, g, w in ((-0.55, 0.0, 1.0, 0.45), (0.6, 0.75, 0.95, 0.4)):
        s.append(f'<path d="{polyline(filament(dx, ph, g))}" fill="none" stroke="url(#cs_fade)" '
                 f'stroke-width="{fmt(w)}" stroke-linecap="round" stroke-linejoin="round"/>')
    main = filament(0.0, 0.35, 1.08)
    s.append(f'<path d="{polyline(main)}" fill="none" stroke="url(#cs_fade)" '
             'stroke-width="0.7" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append('</svg>')
    return "\n".join(s) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "dim.svg").write_text(smoke_motif(), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
