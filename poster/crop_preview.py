# -*- coding: utf-8 -*-
"""Служебный скрипт: растровый предпросмотр фрагмента плаката.

    python3 poster/crop_preview.py X Y W H имя_файла [ширина_px]

Координаты — в миллиметрах плаката (600 × 900).
"""

import os
import re
import sys

import cairosvg

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out",
                   "shturm_doma_60x90.svg")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out",
                       "_crops")


def main():
    x, y, w, h = (float(v) for v in sys.argv[1:5])
    name = sys.argv[5]
    px = int(sys.argv[6]) if len(sys.argv) > 6 else 1500

    with open(SRC, encoding="utf-8") as f:
        svg = f.read()
    svg = re.sub(r'viewBox="[^"]*"', 'viewBox="%g %g %g %g"' % (x, y, w, h), svg, count=1)
    svg = re.sub(r'width="[\d.]+mm"', 'width="%gmm"' % w, svg, count=1)
    svg = re.sub(r'height="[\d.]+mm"', 'height="%gmm"' % h, svg, count=1)

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, name + ".png")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out,
                     output_width=px, output_height=int(px * h / w),
                     background_color="white")
    print(out)


if __name__ == "__main__":
    main()
