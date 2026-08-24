# -*- coding: utf-8 -*-
"""Служебный скрипт: приблизительный растровый предпросмотр листа-холста Excel.

Читает заливки, рамки и текст листа «ПЛАКАТ 60x90» и перерисовывает их в PNG,
чтобы проверить вёрстку, не открывая Excel.

    python3 poster/preview_xlsx.py [имя_файла] [ширина_px] [c1 r1 c2 r2]
"""

import os
import sys

import cairosvg
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from poster.generator.svgkit import SVG  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "out", "shturm_doma_60x90.xlsx")
CELL = 19 * 25.4 / 96.0            # мм
PT = 25.4 / 72.0


def color_of(cell):
    f = cell.fill
    if f is None or f.patternType != "solid":
        return None
    rgb = getattr(f.fgColor, "rgb", None)
    if not isinstance(rgb, str):
        return None
    return "#" + rgb[-6:]


def font_color(cell):
    rgb = getattr(cell.font.color, "rgb", None) if cell.font.color else None
    return "#" + rgb[-6:] if isinstance(rgb, str) else "#000000"


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "xlsx_full"
    px = int(sys.argv[2]) if len(sys.argv) > 2 else 1400
    if len(sys.argv) > 6:
        c1, r1, c2, r2 = (int(v) for v in sys.argv[3:7])
    else:
        c1, r1, c2, r2 = 1, 1, 120, 180

    wb = load_workbook(SRC)
    ws = wb["ПЛАКАТ 60x90"]

    w = (c2 - c1 + 1) * CELL
    h = (r2 - r1 + 1) * CELL
    svg = SVG(w, h, background="#FFFFFF")

    def bx(c):
        return (c - c1) * CELL

    def by(r):
        return (r - r1) * CELL

    merged = {}
    covered = {}
    for rng in ws.merged_cells.ranges:
        merged[(rng.min_col, rng.min_row)] = rng
        for cc in range(rng.min_col, rng.max_col + 1):
            for rr in range(rng.min_row, rng.max_row + 1):
                covered[(cc, rr)] = rng

    for row in ws.iter_rows(min_row=r1, max_row=r2, min_col=c1, max_col=c2):
        for cell in row:
            if (cell.column, cell.row) in covered:
                continue
            col = color_of(cell)
            if col and col != "#FFFFFF":
                svg.rect(bx(cell.column), by(cell.row), CELL + 0.02,
                         CELL + 0.02, fill=col)

    # объединённый диапазон Excel рисует заливкой своей левой верхней ячейки
    for (mc, mr), rng in merged.items():
        col = color_of(ws.cell(row=mr, column=mc))
        if col and col != "#FFFFFF":
            svg.rect(bx(rng.min_col), by(rng.min_row),
                     (rng.max_col - rng.min_col + 1) * CELL + 0.02,
                     (rng.max_row - rng.min_row + 1) * CELL + 0.02, fill=col)

    for row in ws.iter_rows(min_row=r1, max_row=r2, min_col=c1, max_col=c2):
        for cell in row:
            if cell.value in (None, ""):
                continue
            rng = merged.get((cell.column, cell.row))
            if rng:
                x0, y0 = bx(rng.min_col), by(rng.min_row)
                x1, y1 = bx(rng.max_col + 1), by(rng.max_row + 1)
            else:
                x0, y0 = bx(cell.column), by(cell.row)
                x1, y1 = x0 + CELL, y0 + CELL
            size = (cell.font.size or 11) * PT
            al = cell.alignment
            anchor = {"center": "middle", "right": "end"}.get(
                al.horizontal or "left", "start")
            tx = {"middle": (x0 + x1) / 2, "end": x1 - 1}.get(anchor, x0 + 0.6)
            ty = (y0 + y1) / 2 + size * 0.36
            rot = None
            if al.text_rotation:
                rot = -al.text_rotation
                tx = (x0 + x1) / 2
                ty = (y0 + y1) / 2
                anchor = "middle"
            svg.text(tx, ty, cell.value, size=size, fill=font_color(cell),
                     anchor=anchor,
                     weight="bold" if cell.font.bold else "normal",
                     style="italic" if cell.font.italic else "normal",
                     rotate=rot)

    out_dir = os.path.join(HERE, "out", "_crops")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, name + ".png")
    cairosvg.svg2png(bytestring=svg.tostring().encode("utf-8"), write_to=out,
                     output_width=px, output_height=int(px * h / w),
                     background_color="white")
    print(out, "%.0f × %.0f мм" % (w, h))


if __name__ == "__main__":
    main()
