# -*- coding: utf-8 -*-
"""Сборка всех файлов плаката.

    python3 poster/build.py [каталог_вывода]

Создаёт:
    shturm_doma_60x90.xlsx   — плакат в Excel (лист-холст + рабочие таблицы)
    shturm_doma_60x90.svg    — векторный оригинал 600 × 900 мм
    shturm_doma_60x90.pdf    — файл для печати (точный размер 600 × 900 мм)
    shturm_doma_60x90_preview.png — растровый предпросмотр
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from poster.generator import svg_poster, xlsx_poster  # noqa: E402

BASENAME = "shturm_doma_60x90"


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)

    xlsx_path = os.path.join(out_dir, BASENAME + ".xlsx")
    xlsx_poster.build(xlsx_path)
    print("Excel   :", xlsx_path)

    svg_path = os.path.join(out_dir, BASENAME + ".svg")
    svg_poster.build(svg_path)
    print("SVG     :", svg_path)

    try:
        import cairosvg
    except ImportError:
        print("PDF/PNG : пропущено (нет модуля cairosvg)")
        return

    pdf_path = os.path.join(out_dir, BASENAME + ".pdf")
    cairosvg.svg2pdf(url=svg_path, write_to=pdf_path)
    print("PDF     :", pdf_path)

    png_path = os.path.join(out_dir, BASENAME + "_preview.png")
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=1400,
                     output_height=2100, background_color="white")
    print("PNG     :", png_path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
