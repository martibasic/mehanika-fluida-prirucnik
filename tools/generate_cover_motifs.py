"""Generate the decorative PDF cover motif assets/cover/velebit_bura.svg.

"Look, a cloud on the mountain that turns into a wave."

The motif is the author's own sketch, traced stroke by stroke and only
lightly smoothed: Velebit in black (a foothill in front, the ridge behind),
the clouds in grey (they drift over the ridge, and the last one curls like a
breaking wave), the sea in blue with three crests. Where a cloud passes in
front of the mountain the mountain line stops short of it.

STROKES holds the smoothed centre lines of the sketch (drawing units, the
sketch scaled to a width of 300). Each stroke is a list of segments that
share end points; a join between segments is a deliberate corner (a wave
crest). The strokes are drawn like ink: thin where the brush lands and
lifts, fuller in between. Presentation only, no labels.
The script refuses to write the file if any two strokes come closer than
2 units (about 1 mm on the cover), so lines never cross or touch.

Run: python tools/generate_cover_motifs.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cover"

COLOURS = {"mountain": "#2f3b46", "cloud": "#8b949c", "sea": "#3c86b4"}

# name: (colour, brush width, segments)
STROKES = {
    "ridge": ("mountain", 1.7, [
        [(150.4, 18.1), (153.0, 16.7), (155.7, 15.1), (158.4, 13.5), (161.2, 12.0), (163.9,
         10.6), (166.6, 9.6), (169.4, 8.9), (172.1, 8.4), (174.8, 8.0), (177.5, 7.5), (180.3,
         6.9), (183.0, 6.2), (185.7, 5.6), (188.4, 5.0), (191.2, 4.5), (193.9, 4.5), (196.6,
         5.3), (199.3, 6.8), (202.0, 8.4), (204.8, 9.9), (207.5, 11.1), (210.2, 11.8), (213.0,
         12.1), (215.7, 12.2), (218.5, 12.3), (221.2, 12.5), (223.9, 13.1), (226.6, 14.5),
         (229.2, 16.6), (231.9, 19.1), (234.6, 21.8), (237.3, 24.5), (240.0, 27.2), (242.8,
         29.7), (245.6, 31.9), (248.4, 33.7), (251.0, 35.4), (253.3, 37.3), (255.3, 39.5),
         (257.3, 41.4), (259.5, 42.6), (262.1, 43.0), (264.8, 43.1), (267.5, 42.9), (270.3,
         42.5), (273.0, 41.9), (275.7, 41.4), (278.4, 41.5), (281.0, 42.5), (283.7, 44.2),
         (286.5, 45.7), (289.2, 46.9), (291.9, 47.7), (294.4, 48.4), (296.7, 49.2)],
    ]),
    "hill": ("mountain", 1.7, [
        [(5.0, 87.3), (6.5, 84.9), (8.2, 82.6), (10.3, 80.3), (12.7, 78.2), (15.3, 76.5), (18.0,
         75.2), (20.7, 74.0), (23.4, 73.0), (26.1, 72.1), (28.9, 71.4), (31.6, 70.7), (34.3,
         70.1), (37.0, 69.6), (39.8, 69.2), (42.5, 68.9), (45.3, 68.7), (48.0, 68.6), (50.8,
         68.3), (53.6, 67.7), (56.3, 66.6), (58.9, 64.8), (61.4, 62.6), (63.8, 60.0), (66.2,
         57.2), (68.7, 54.6), (71.3, 52.3), (73.9, 50.4), (76.6, 49.1), (79.4, 48.4), (82.1,
         48.1)],
    ]),
    "cloud1": ("cloud", 1.5, [
        [(0.0, 2.7), (2.5, 5.3), (5.0, 8.0), (7.6, 10.6), (10.3, 13.0), (13.0, 15.2), (15.7,
         16.9), (18.4, 18.4), (21.2, 19.6), (23.9, 20.6), (26.6, 21.4), (29.4, 22.1), (32.1,
         22.7), (34.8, 23.1), (37.6, 23.4), (40.3, 23.5), (43.0, 23.5), (45.7, 23.4), (48.5,
         23.1), (51.2, 22.7), (53.9, 22.2), (56.6, 21.7), (59.3, 21.3), (61.9, 20.9)],
    ]),
    "cloud2": ("cloud", 1.5, [
        [(15.5, 28.6), (18.0, 30.5), (20.6, 32.1), (23.3, 33.3), (26.1, 34.1), (28.9, 34.7),
         (31.6, 35.2), (34.4, 35.6), (37.1, 36.0), (39.8, 36.4), (42.6, 36.7), (45.3, 37.0),
         (48.0, 37.4), (50.7, 37.7), (53.5, 37.9), (56.2, 38.2), (58.9, 38.5), (61.6, 38.7),
         (64.4, 39.0), (67.1, 39.2), (69.8, 39.3), (72.5, 39.3), (75.3, 39.2), (78.0, 38.9),
         (80.7, 38.6), (83.5, 38.2), (86.2, 38.0), (88.9, 37.8), (91.6, 37.6), (94.4, 37.5),
         (97.1, 37.3), (99.8, 37.0), (102.5, 36.8), (105.2, 36.5), (107.9, 36.1), (110.5, 35.7),
         (113.0, 35.2)],
    ]),
    "cloud3": ("cloud", 1.6, [
        [(52.0, 0.0), (54.6, 0.0), (57.2, 0.0), (59.8, 0.0), (62.6, 0.0), (65.3, 0.1), (68.0,
         0.2), (70.7, 0.4), (73.4, 0.6), (76.2, 0.9), (78.9, 1.2), (81.6, 1.4), (84.4, 1.7),
         (87.1, 2.1), (89.8, 2.5), (92.6, 2.9), (95.3, 3.4), (98.0, 3.9), (100.7, 4.6), (103.4,
         5.3), (106.2, 6.0), (108.9, 6.8), (111.7, 7.5), (114.4, 8.4), (117.1, 9.3), (119.9,
         10.3), (122.6, 11.4), (125.3, 12.5), (128.0, 13.8), (130.8, 15.1), (133.5, 16.4),
         (136.2, 17.8), (138.9, 19.1), (141.6, 20.3), (144.4, 21.2), (147.1, 22.0), (149.8,
         22.7), (152.5, 23.2), (155.3, 23.6), (158.0, 23.9), (160.7, 24.0), (163.5, 24.1),
         (166.2, 24.1), (168.9, 24.0), (171.7, 24.0), (174.4, 24.0), (177.2, 24.2), (180.0,
         24.9), (182.6, 26.2), (185.1, 28.1), (187.2, 30.5), (189.1, 33.0), (190.6, 35.7),
         (191.8, 38.4), (192.8, 41.0), (193.7, 43.7)],
    ]),
    "cloud4": ("cloud", 1.4, [
        [(86.8, 47.4), (89.2, 47.8), (91.8, 48.1), (94.4, 48.4), (97.1, 48.7), (99.8, 48.9),
         (102.5, 49.0), (105.3, 49.1), (108.0, 49.2), (110.7, 49.4), (113.4, 49.4), (116.2,
         49.5), (118.9, 49.5), (121.6, 49.4), (124.4, 49.1), (127.1, 48.5), (129.8, 47.8),
         (132.5, 46.9), (135.2, 46.1), (137.9, 45.3), (140.7, 44.5), (143.3, 43.7), (146.0, 42.9)],
    ]),
    "wave": ("cloud", 1.7, [
        [(143.2, 56.5), (145.8, 58.3), (148.5, 60.0), (151.2, 61.4), (153.9, 62.4), (156.7,
         63.1), (159.4, 63.7), (162.1, 64.2), (164.8, 64.5), (167.5, 64.7), (170.3, 64.8),
         (173.0, 64.8), (175.7, 64.5), (178.5, 64.1), (181.2, 63.3), (183.9, 62.4), (186.6,
         61.3), (189.4, 60.2), (192.1, 59.0), (194.8, 57.9), (197.5, 56.7), (200.3, 55.7),
         (203.0, 54.7), (205.7, 53.8), (208.4, 52.9), (211.2, 52.1), (213.9, 51.3), (216.6,
         50.7), (219.4, 50.1), (222.1, 49.6), (224.8, 49.2), (227.5, 48.9), (230.3, 48.6),
         (233.0, 48.5), (235.7, 48.5), (238.5, 48.7), (241.2, 49.1), (243.9, 49.7), (246.7,
         50.4), (249.4, 51.2), (252.1, 52.1), (254.8, 53.1), (257.6, 54.2), (260.3, 55.4),
         (263.0, 56.6), (265.7, 57.9), (268.5, 59.4), (271.2, 60.9), (273.9, 62.7), (276.6,
         64.8), (279.3, 67.1), (281.8, 69.6), (284.2, 72.3), (286.2, 75.1), (287.9, 77.9),
         (289.2, 80.6), (290.2, 83.4), (291.0, 86.1), (291.6, 88.8), (291.9, 91.6), (292.0,
         94.3), (291.7, 97.0), (290.8, 99.7), (289.4, 102.3), (287.4, 104.8), (284.9, 107.1),
         (282.2, 109.1), (279.5, 110.6), (276.7, 111.6), (273.9, 112.1), (271.2, 112.2), (268.5,
         111.8), (265.7, 111.0), (263.1, 109.8), (260.5, 108.1), (258.2, 106.1), (256.1, 103.7),
         (254.6, 101.1), (253.7, 98.5), (253.5, 95.9), (254.2, 93.6), (255.7, 91.7), (257.8,
         90.4), (260.1, 89.5), (262.3, 88.9)],
    ]),
    "sea": ("sea", 1.6, [
        [(8.1, 120.9), (10.6, 121.8), (13.1, 122.7), (15.8, 123.5), (18.5, 124.2), (21.2, 124.8),
         (23.9, 125.1), (26.6, 125.3), (29.4, 125.2), (32.1, 125.0), (34.8, 124.7), (37.5,
         124.3), (40.3, 124.0), (43.0, 123.8), (45.7, 123.6), (48.5, 123.5), (51.2, 123.4),
         (53.9, 123.1), (56.6, 122.9), (59.4, 122.5), (62.1, 122.0), (64.8, 121.4), (67.5,
         120.6), (70.3, 119.7), (73.0, 118.9), (75.7, 118.1), (78.5, 117.2), (81.2, 116.3),
         (83.9, 115.0), (86.7, 113.5), (89.4, 111.7), (92.1, 109.8), (94.8, 108.0), (97.5, 106.4)],
        [(97.5, 106.4), (100.4, 108.1), (103.2, 110.0), (105.8, 112.2), (108.5, 114.3), (111.2,
         116.2), (113.9, 117.7), (116.6, 118.8), (119.4, 119.6), (122.1, 120.1), (124.8, 120.3),
         (127.5, 120.4), (130.3, 120.4), (133.0, 120.4), (135.7, 120.2), (138.5, 119.9), (141.2,
         119.4), (143.9, 118.7), (146.6, 117.8), (149.4, 116.8), (152.1, 115.5), (154.9, 113.9),
         (157.7, 111.9), (160.4, 109.7), (163.2, 107.3)],
        [(163.2, 107.3), (165.7, 109.8), (168.2, 112.1), (170.8, 114.2), (173.5, 115.9), (176.2,
         117.1), (178.9, 117.9), (181.6, 118.6), (184.4, 119.1), (187.1, 119.5), (189.8, 119.8),
         (192.5, 120.1), (195.3, 120.2), (198.0, 120.3), (200.7, 120.3), (203.4, 120.1), (206.2,
         119.7), (208.9, 119.2), (211.6, 118.6), (214.4, 117.8), (217.1, 116.7), (219.9, 115.2),
         (222.7, 113.4), (225.4, 111.2), (227.9, 108.7), (230.2, 106.0), (232.2, 103.2), (234.1,
         100.2), (236.1, 97.0)],
        [(236.1, 97.0), (238.2, 99.2), (240.2, 101.6), (242.5, 104.0), (244.9, 106.2), (247.5,
         108.1), (250.3, 109.8), (253.0, 111.2), (255.7, 112.5), (258.4, 113.7), (261.1, 114.8),
         (263.9, 115.8), (266.6, 116.6), (269.4, 117.2), (272.1, 117.7), (274.8, 118.0), (277.5,
         118.2), (280.3, 118.4), (283.0, 118.6), (285.7, 118.9), (288.4, 119.2), (291.2, 119.3),
         (293.9, 119.2), (296.6, 119.1)],
    ]),
}


def fmt(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def spline(ctrl, step: float = 0.4):
    """Catmull-Rom spline through the points, densely sampled."""
    p = list(ctrl)
    out = [p[0]]
    for i in range(len(p) - 1):
        p0 = p[i - 1] if i else p[i]
        p1, p2 = p[i], p[i + 1]
        p3 = p[i + 2] if i + 2 < len(p) else p2
        n = max(2, int(math.hypot(p2[0] - p1[0], p2[1] - p1[1]) / step))
        for k in range(1, n + 1):
            t = k / n
            out.append(tuple(
                0.5 * (2 * p1[j] + (p2[j] - p0[j]) * t
                       + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                       + (3 * p1[j] - p0[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    return out


def dense(segs):
    """All segments of a stroke as one densely sampled line."""
    pts = []
    for seg in segs:
        s = spline(seg)
        pts += s if not pts else s[1:]
    return pts


def brush(pts, width: float, seed: float) -> str:
    """A stroke as a filled shape: it swells after the brush lands and thins
    where it lifts, with a slow change of pressure along the way."""
    n = len(pts)
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    total = acc[-1]
    lead = tail = min(18.0, 0.3 * total)
    left, right = [], []
    for i, p in enumerate(pts):
        s = acc[i]
        q0, q1 = pts[max(i - 3, 0)], pts[min(i + 3, n - 1)]
        tx, ty = q1[0] - q0[0], q1[1] - q0[1]
        m = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / m, tx / m
        press = 0.78 + 0.22 * math.sin(s / 21.0 + seed) ** 2
        w = width * press * min(1.0, s / lead) ** 0.7 * min(1.0, (total - s) / tail) ** 0.7
        w = max(w, 0.14)
        left.append((p[0] + nx * w / 2, p[1] + ny * w / 2))
        right.append((p[0] - nx * w / 2, p[1] - ny * w / 2))
    outline = left + right[::-1]
    return "M" + " L".join(f"{fmt(a)} {fmt(b)}" for a, b in outline) + " Z"


def motif():
    lines = {name: dense(segs) for name, (_, _, segs) in STROKES.items()}
    every = [q for line in lines.values() for q in line]
    x0, x1 = min(q[0] for q in every) - 4.0, max(q[0] for q in every) + 4.0
    y0, y1 = min(q[1] for q in every) - 4.0, max(q[1] for q in every) + 4.0
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(x0)} {fmt(y0)} {fmt(x1 - x0)} '
         f'{fmt(y1 - y0)}" role="img" aria-label="Autoričin crtež: oblak na planini koji se '
         'pretvara u val. Crno je Velebit, sivo su oblaci koji prelaze greben i zavijaju se '
         'kao val, plavo je more s tri grebena.">']
    for k, (name, (colour, width, _)) in enumerate(STROKES.items()):
        s.append(f'<path d="{brush(lines[name], width, 0.9 * k + 0.4)}" fill="{COLOURS[colour]}"/>')
    s.append("</svg>")
    return "\n".join(s) + "\n", lines


def min_clearance(lines) -> tuple[float, str, str]:
    """Smallest distance between two different strokes."""
    names = list(lines)
    best = (1e9, "", "")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = lines[names[i]][::2], lines[names[j]][::2]
            for p in a:
                for q in b:
                    d = math.hypot(p[0] - q[0], p[1] - q[1])
                    if d < best[0]:
                        best = (d, names[i], names[j])
    return best


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    svg, lines = motif()
    gap, a, b = min_clearance(lines)
    if gap < 2.0:
        if "--draft" not in sys.argv:
            raise SystemExit(f"Strokes {a} and {b} come within {gap:.2f} units; minimum is 2.0.")
        print(f"DRAFT: strokes {a} and {b} come within {gap:.2f} units; minimum is 2.0.")
    (OUT / "velebit_bura.svg").write_text(svg, encoding="utf-8", newline="\n")
    print(f"assets/cover/velebit_bura.svg: smallest gap between strokes {gap:.2f} ({a}, {b})")


if __name__ == "__main__":
    main()
