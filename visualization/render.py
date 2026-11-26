"""Render the 3D interventional-mean fixture and deterministic offline bundle."""

import math
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 704, 850
FONT_DIR = Path(os.environ.get("Q441_FONT_DIR", "/System/Library/Fonts/Supplemental"))
BG = "#11152b"
PANEL = "#1c2441"
TEXT = "#f4f7ff"
MUTED = "#bdc9e2"
GRID = "#4c5c83"
REF = "#60efc7"
CANDIDATE = "#eeadff"
VERTICES = [(x, z, y) for x in (0, 1) for z in (0, 1) for y in (0, 1)]
EDGES = [
    (a, b)
    for j, a in enumerate(VERTICES)
    for b in VERTICES[j + 1:]
    if sum(abs(s - t) for s, t in zip(a, b)) == 1
]
FIXTURES = [
    ("Null intervention", (20, 20, 24), (20, 20, 26), ("Reward error is +0.02.", "The middle-node predictions agree.")),
    ("Set X = 1", (100, 60, 60), (100, 20, 74), ("Z error is −0.40.", "Reward error is +0.14.")),
    ("Set Z = 1", (20, 100, 64), (60, 100, 66), ("X error is +0.40.", "Reward error is +0.02.")),
]


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ("Arial Bold.ttf" if bold else "Arial.ttf")), size)


def project(point, angle):
    x, z, y = (2 * value - 1 for value in point)
    u, v = math.cos(angle), math.sin(angle)
    return round(354 + 141 * (u * x - v * z)), round(346 + 68 * (v * x + u * z) - 101 * y)


def frame(action, angle):
    title, reference, candidate, caption = FIXTURES[action]
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.text((34, 29), "Interventional means", font=font(53, True), fill=TEXT)
    draw.text((36, 98), "Nodes X, Z and reward Y", font=font(33), fill=MUTED)
    draw.rounded_rectangle((33, 156, 671, 548), radius=24, fill=PANEL)
    for first, second in EDGES:
        draw.line((project(first, angle), project(second, angle)), fill=GRID, width=3)

    for edge, name, offset in (
        ((1, 0, 0), "X", (15, -22)), ((0, 1, 0), "Z", (-35, 6)), ((0, 0, 1), "Y", (-29, -13))
    ):
        x, y = project(edge, angle)
        draw.text((x + offset[0], y + offset[1]), name, font=font(32, True), fill=MUTED)

    actual = project(tuple(value / 100 for value in reference), angle)
    fitted = project(tuple(value / 100 for value in candidate), angle)
    draw.line((actual, fitted), fill=TEXT, width=4)
    x, y = fitted
    radius = 17
    draw.polygon([(x, y - radius), (x + radius, y), (x, y + radius), (x - radius, y)],
                 fill=BG, outline=CANDIDATE, width=4)
    x, y = actual
    radius = 7
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=REF)

    draw.text((34, 565), title, font=font(46, True), fill=TEXT)
    for letter, x in zip(("X", "Z", "Y"), (318, 454, 589)):
        draw.text((x, 618), letter, font=font(33, True), fill=MUTED, anchor="mt")
    for row, (label, colour, values) in enumerate((("Reference", REF, reference), ("Candidate", CANDIDATE, candidate))):
        y = 655 + 40 * row
        draw.text((36, y), label, font=font(34, True), fill=colour)
        for value, x in zip(values, (318, 454, 589)):
            draw.text((x, y), f"{value / 100:.2f}", font=font(34), fill=colour, anchor="mt")
    draw.line(((35, 746), (670, 746)), fill=GRID, width=2)
    for row, line in enumerate(caption):
        draw.text((36, 760 + row * 37), line, font=font(31), fill=TEXT)
    return image.quantize(colors=48, method=Image.Quantize.MEDIANCUT)


def main():
    frames, durations = [], []
    for action in range(len(FIXTURES)):
        for step in range(18):
            angle = 0.40 + 0.26 * math.sin(math.tau * step / 18)
            frames.append(frame(action, angle))
            durations.append(270 if step == 0 else 170)
    frames[0].save(HERE / "mean-predictions.gif", save_all=True, append_images=frames[1:],
                   duration=durations, disposal=1, loop=0, optimize=True)

    item = ZipInfo("index.html", (1980, 1, 1, 0, 0, 0))
    item.external_attr = 0o100644 << 16
    with ZipFile(HERE / "mean-predictions-explorer.zip", "w") as archive:
        archive.writestr(item, (HERE / "index.html").read_bytes(), ZIP_DEFLATED, compresslevel=9)


if __name__ == "__main__":
    main()
