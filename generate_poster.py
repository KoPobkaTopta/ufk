#!/usr/bin/env python3
"""Generate a safe 600 × 900 mm training-site poster in XLSX, PDF and PNG."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "artifacts"
PNG_PATH = OUTPUT_DIR / "uchebnaya_tochka_60x90.png"
PDF_PATH = OUTPUT_DIR / "uchebnaya_tochka_60x90.pdf"
XLSX_PATH = OUTPUT_DIR / "uchebnaya_tochka_60x90.xlsx"

WIDTH_PX = 3600
HEIGHT_PX = 5400
WIDTH_MM = 600
HEIGHT_MM = 900

FONT_REGULAR = Path("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf")
FONT_BOLD = Path("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf")

COLORS = {
    "paper": "#F4F0E3",
    "paper_dark": "#E8DFCA",
    "ink": "#1C2723",
    "green": "#173B31",
    "olive": "#617052",
    "tan": "#C9A46D",
    "tan_light": "#E7D4AF",
    "orange": "#C96F3A",
    "red": "#A83A30",
    "white": "#FFFFFF",
    "gray": "#69706C",
    "gray_light": "#D8D8D2",
    "safe": "#3A7A57",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold else FONT_REGULAR
    if not path.exists():
        raise FileNotFoundError(f"Required font is missing: {path}")
    return ImageFont.truetype(str(path), size)


def text_width(draw: ImageDraw.ImageDraw, text: str, text_font: ImageFont.FreeTypeFont) -> float:
    box = draw.textbbox((0, 0), text, font=text_font)
    return box[2] - box[0]


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    text_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split()
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and text_width(draw, candidate, text_font) > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    text_font: ImageFont.FreeTypeFont,
    fill: str,
    max_width: int,
    line_gap: int = 10,
) -> int:
    x, y = xy
    line_height = text_font.size + line_gap
    for line in wrap_text(draw, text, text_font, max_width):
        draw.text((x, y), line, font=text_font, fill=fill)
        y += line_height
    return y


def draw_centered(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    text_font: ImageFont.FreeTypeFont,
    fill: str,
) -> None:
    x0, y0, x1, y1 = box
    bounds = draw.textbbox((0, 0), text, font=text_font)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    draw.text(
        (x0 + (x1 - x0 - width) / 2, y0 + (y1 - y0 - height) / 2 - bounds[1]),
        text,
        font=text_font,
        fill=fill,
    )


def rounded_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: str,
    outline: str | None = None,
    width: int = 4,
    radius: int = 30,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_section_label(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    number: str,
    title: str,
) -> None:
    draw.rounded_rectangle((x, y, x + 76, y + 76), radius=18, fill=COLORS["orange"])
    draw_centered(draw, (x, y, x + 76, y + 76), number, font(38, True), COLORS["white"])
    draw.text((x + 100, y + 4), title, font=font(47, True), fill=COLORS["green"])


def dashed_line(
    draw: ImageDraw.ImageDraw,
    points: tuple[int, int, int, int],
    fill: str,
    width: int = 12,
    dash: int = 28,
    gap: int = 18,
) -> None:
    x0, y0, x1, y1 = points
    if x0 == x1:
        direction = 1 if y1 >= y0 else -1
        cursor = y0
        while (cursor - y1) * direction <= 0:
            end = cursor + direction * dash
            if (end - y1) * direction > 0:
                end = y1
            draw.line((x0, cursor, x1, end), fill=fill, width=width)
            cursor = end + direction * gap
    elif y0 == y1:
        direction = 1 if x1 >= x0 else -1
        cursor = x0
        while (cursor - x1) * direction <= 0:
            end = cursor + direction * dash
            if (end - x1) * direction > 0:
                end = x1
            draw.line((cursor, y0, end, y1), fill=fill, width=width)
            cursor = end + direction * gap


def draw_down_arrow(draw: ImageDraw.ImageDraw, x: int, y0: int, y1: int) -> None:
    color = COLORS["safe"]
    draw.line((x, y0, x, y1 - 38), fill=color, width=16)
    draw.polygon(
        [(x, y1), (x - 42, y1 - 58), (x + 42, y1 - 58)],
        fill=color,
    )


def draw_checkpoint(draw: ImageDraw.ImageDraw, x: int, y: int, label: str) -> None:
    draw.ellipse((x - 37, y - 37, x + 37, y + 37), fill=COLORS["orange"])
    draw_centered(
        draw,
        (x - 37, y - 37, x + 37, y + 37),
        label,
        font(26, True),
        COLORS["white"],
    )


def draw_building_plan(draw: ImageDraw.ImageDraw) -> None:
    panel = (135, 840, 2575, 3270)
    rounded_panel(draw, panel, COLORS["white"], COLORS["paper_dark"], width=6, radius=34)
    draw_section_label(draw, 190, 895, "1", "СХЕМА УЧЕБНОГО ОБЪЕКТА")
    draw.text(
        (193, 983),
        "Три входа · модульная планировка · внутренний маршрут задаёт руководитель",
        font=font(29),
        fill=COLORS["gray"],
    )

    left, top, right, bottom = 275, 1125, 2440, 2815
    wall = COLORS["green"]
    room_fill = COLORS["tan_light"]
    wall_width = 18

    draw.rectangle((left, top, right, bottom), fill=room_fill, outline=wall, width=wall_width)

    bay_width = (right - left) / 3
    divider_xs = [int(left + bay_width), int(left + bay_width * 2)]
    for divider_x in divider_xs:
        draw.line((divider_x, top, divider_x, bottom), fill=wall, width=wall_width)

    entrance_centers: list[int] = []
    for bay_index in range(3):
        x0 = int(left + bay_width * bay_index)
        x1 = int(left + bay_width * (bay_index + 1))
        entrance_x = (x0 + x1) // 2
        entrance_centers.append(entrance_x)

        # A long observation corridor and alternating room partitions.
        corridor_x = x0 + 165
        draw.line((corridor_x, top + 155, corridor_x, bottom - 120), fill=wall, width=14)

        partition_ys = [top + 425, top + 840, top + 1255]
        for partition_index, partition_y in enumerate(partition_ys):
            if partition_index % 2 == 0:
                draw.line(
                    (corridor_x, partition_y, x1 - 145, partition_y),
                    fill=wall,
                    width=14,
                )
                draw.line(
                    (x1 - 60, partition_y, x1, partition_y),
                    fill=wall,
                    width=14,
                )
            else:
                draw.line(
                    (corridor_x + 105, partition_y, x1, partition_y),
                    fill=wall,
                    width=14,
                )

        # Mask a doorway in the lower exterior wall.
        draw.rectangle(
            (entrance_x - 72, bottom - wall_width, entrance_x + 72, bottom + wall_width),
            fill=COLORS["white"],
        )
        draw.line(
            (entrance_x - 72, bottom, entrance_x - 72, bottom - 105),
            fill=COLORS["orange"],
            width=10,
        )
        draw.arc(
            (entrance_x - 72, bottom - 145, entrance_x + 72, bottom),
            start=180,
            end=270,
            fill=COLORS["orange"],
            width=8,
        )

        label = chr(ord("А") + bay_index)
        rounded_panel(
            draw,
            (entrance_x - 112, bottom + 48, entrance_x + 112, bottom + 125),
            COLORS["green"],
            radius=20,
        )
        draw_centered(
            draw,
            (entrance_x - 112, bottom + 48, entrance_x + 112, bottom + 125),
            f"ВХОД {label}",
            font(28, True),
            COLORS["white"],
        )

        room_centers = [
            top + 225,
            top + 625,
            top + 1040,
            top + 1455,
        ]
        for room_index, room_y in enumerate(room_centers, start=1):
            draw.text(
                (corridor_x + 55, room_y),
                f"ЗОНА {bay_index + 1}.{room_index}",
                font=font(24, True),
                fill=COLORS["green"],
            )

        draw_checkpoint(draw, entrance_x, bottom - 145, f"К{bay_index + 1}")
        draw_checkpoint(draw, x1 - 110, top + 95, f"К{bay_index + 4}")

        # Evacuation arrows point out of, not into, the object.
        draw_down_arrow(draw, entrance_x, bottom + 145, bottom + 330)

    draw.text(
        (left + 15, top - 58),
        "ДЕРЕВЯННЫЙ УЧЕБНЫЙ МАКЕТ",
        font=font(28, True),
        fill=COLORS["olive"],
    )

    # Instructor and medical positions are outside the participant area.
    for x in (left + 45, right - 45):
        draw.ellipse((x - 38, bottom + 250, x + 38, bottom + 326), fill=COLORS["olive"])
        draw_centered(
            draw,
            (x - 38, bottom + 250, x + 38, bottom + 326),
            "И",
            font(31, True),
            COLORS["white"],
        )

    med_x, med_y = right - 90, top - 95
    draw.rounded_rectangle(
        (med_x - 62, med_y - 38, med_x + 62, med_y + 38),
        radius=12,
        fill=COLORS["white"],
        outline=COLORS["red"],
        width=5,
    )
    draw.line((med_x - 22, med_y, med_x + 22, med_y), fill=COLORS["red"], width=14)
    draw.line((med_x, med_y - 22, med_x, med_y + 22), fill=COLORS["red"], width=14)

    dashed_line(
        draw,
        (left, bottom + 390, right, bottom + 390),
        COLORS["safe"],
        width=9,
        dash=34,
        gap=20,
    )
    draw_centered(
        draw,
        (left + 340, bottom + 420, right - 340, bottom + 500),
        "ПУНКТ СБОРА ПОСЛЕ ВЫХОДА",
        font(29, True),
        COLORS["safe"],
    )


def draw_legend_and_staff(draw: ImageDraw.ImageDraw) -> None:
    box = (2660, 840, 3465, 3270)
    rounded_panel(draw, box, COLORS["green"], radius=34)
    draw_section_label(draw, 2720, 895, "2", "УСЛОВНЫЕ")
    draw.text((2820, 954), "ОБОЗНАЧЕНИЯ", font=font(47, True), fill=COLORS["white"])

    legend_items = [
        ("ВХОД А–В", COLORS["orange"], "square"),
        ("К  Контрольная точка", COLORS["orange"], "circle"),
        ("И  Инструкторский пост", COLORS["olive"], "circle"),
        ("Медицинская зона", COLORS["red"], "cross"),
        ("Направление эвакуации", COLORS["safe"], "arrow"),
    ]
    y = 1070
    for label, color, kind in legend_items:
        x = 2738
        if kind == "square":
            draw.rounded_rectangle((x, y, x + 68, y + 52), radius=10, fill=color)
        elif kind == "circle":
            draw.ellipse((x + 6, y - 4, x + 66, y + 56), fill=color)
        elif kind == "cross":
            draw.line((x + 13, y + 26, x + 59, y + 26), fill=color, width=14)
            draw.line((x + 36, y + 3, x + 36, y + 49), fill=color, width=14)
        else:
            draw.line((x + 4, y + 25, x + 58, y + 25), fill=color, width=10)
            draw.polygon(
                [(x + 70, y + 25), (x + 48, y + 8), (x + 48, y + 42)],
                fill=color,
            )
        draw_wrapped(
            draw,
            (x + 92, y - 5),
            label,
            font(29, True),
            COLORS["white"],
            585,
            line_gap=6,
        )
        y += 116

    draw.line((2720, 1700, 3405, 1700), fill=COLORS["olive"], width=4)
    draw.text((2720, 1750), "СОСТАВ УЧЕБНОЙ СМЕНЫ", font=font(34, True), fill=COLORS["white"])
    staff = [
        "Учебная группа А — 3 чел.",
        "Учебная группа Б — 3 чел.",
        "Руководитель занятия — 1",
        "Инструкторы / наблюдатели — по схеме",
        "Медицинское обеспечение — назначено",
    ]
    y = 1830
    for item in staff:
        draw.ellipse((2730, y + 12, 2748, y + 30), fill=COLORS["orange"])
        y = draw_wrapped(
            draw,
            (2775, y),
            item,
            font(28),
            COLORS["white"],
            570,
            line_gap=7,
        )
        y += 24

    rounded_panel(
        draw,
        (2710, 2455, 3415, 3165),
        "#234C40",
        outline=COLORS["olive"],
        width=4,
        radius=24,
    )
    draw.text((2760, 2510), "ВАЖНО", font=font(35, True), fill=COLORS["orange"])
    note = (
        "Маршрут внутри объекта, последовательность действий и учебное оборудование "
        "определяет только руководитель занятия по утверждённой программе."
    )
    draw_wrapped(
        draw,
        (2760, 2580),
        note,
        font(29),
        COLORS["white"],
        600,
        line_gap=12,
    )
    draw.text((2760, 2960), "САМОСТОЯТЕЛЬНЫЙ ВХОД", font=font(27, True), fill="#F5BC8E")
    draw.text((2760, 3010), "В ОБЪЕКТ ЗАПРЕЩЁН", font=font(27, True), fill="#F5BC8E")


def draw_stage_cards(draw: ImageDraw.ImageDraw) -> None:
    draw_section_label(draw, 150, 3390, "3", "ПОРЯДОК ПРОВЕДЕНИЯ ЗАНЯТИЯ")
    stages = [
        ("01", "ИНСТРУКТАЖ", "Цель занятия, границы объекта, сигналы остановки."),
        ("02", "ПРОВЕРКА", "Состав группы, средства защиты, связь и готовность медпоста."),
        ("03", "ДОПУСК", "Доклад о готовности. Вход только по команде руководителя."),
        ("04", "ПРОХОЖДЕНИЕ", "Действовать в пределах задания и указаний инструктора."),
        ("05", "ВЫХОД", "Покинуть объект через назначенный выход и прибыть к пункту сбора."),
        ("06", "РАЗБОР", "Проверка людей и оборудования, замечания, восстановление точки."),
    ]
    x_positions = [150, 1265, 2380]
    top_rows = [3505, 3830]
    card_w, card_h = 1040, 270

    for index, (number, title, body) in enumerate(stages):
        row = index // 3
        col = index % 3
        x = x_positions[col]
        y = top_rows[row]
        rounded_panel(
            draw,
            (x, y, x + card_w, y + card_h),
            COLORS["white"],
            COLORS["paper_dark"],
            width=4,
            radius=26,
        )
        draw.rounded_rectangle(
            (x + 24, y + 24, x + 134, y + 134),
            radius=20,
            fill=COLORS["green"],
        )
        draw_centered(
            draw,
            (x + 24, y + 24, x + 134, y + 134),
            number,
            font(36, True),
            COLORS["white"],
        )
        draw.text((x + 165, y + 29), title, font=font(34, True), fill=COLORS["green"])
        draw_wrapped(
            draw,
            (x + 165, y + 91),
            body,
            font(27),
            COLORS["ink"],
            825,
            line_gap=7,
        )


def draw_safety_panels(draw: ImageDraw.ImageDraw) -> None:
    y0, y1 = 4205, 5120
    left_box = (150, y0, 1780, y1)
    right_box = (1820, y0, 3450, y1)
    rounded_panel(draw, left_box, COLORS["green"], radius=32)
    rounded_panel(draw, right_box, COLORS["white"], COLORS["paper_dark"], width=5, radius=32)

    draw.text((220, y0 + 55), "МЕРЫ БЕЗОПАСНОСТИ", font=font(43, True), fill=COLORS["white"])
    safety = [
        "Допуск — только после инструктажа и проверки средств защиты.",
        "Не входить в объект без команды и не менять назначенный порядок.",
        "Учебные и имитационные средства применяются только по решению ответственного руководителя.",
        "При потере связи, видимости участника или контроля — немедленно остановить упражнение.",
        "Проходы, выходы и доступ к медицинской зоне должны оставаться свободными.",
    ]
    y = y0 + 145
    for item in safety:
        draw.ellipse((222, y + 11, 242, y + 31), fill=COLORS["orange"])
        y = draw_wrapped(
            draw,
            (270, y),
            item,
            font(28),
            COLORS["white"],
            1415,
            line_gap=8,
        )
        y += 22

    draw.text((1890, y0 + 55), "ОСТАНОВКА И ПОМОЩЬ", font=font(43, True), fill=COLORS["green"])
    draw.rounded_rectangle(
        (1890, y0 + 145, 3378, y0 + 285),
        radius=24,
        fill="#F0D4C6",
        outline=COLORS["red"],
        width=5,
    )
    draw.text((1940, y0 + 171), "КОМАНДА: «СТОП УПРАЖНЕНИЕ»", font=font(36, True), fill=COLORS["red"])
    emergency = [
        "1. Немедленно прекратить действия и оставаться на месте.",
        "2. Сообщить руководителю причину остановки.",
        "3. При травме вызвать медика; не перемещать пострадавшего без необходимости.",
        "4. Возобновление — только после команды руководителя.",
    ]
    y = y0 + 340
    for item in emergency:
        y = draw_wrapped(
            draw,
            (1900, y),
            item,
            font(29),
            COLORS["ink"],
            1420,
            line_gap=9,
        )
        y += 25

    draw.line((1900, y1 - 170, 3370, y1 - 170), fill=COLORS["paper_dark"], width=4)
    draw.text((1900, y1 - 125), "Экстренный контакт:", font=font(27, True), fill=COLORS["gray"])
    draw.line((2230, y1 - 88, 3370, y1 - 88), fill=COLORS["gray"], width=3)


def create_poster_png() -> None:
    image = Image.new("RGB", (WIDTH_PX, HEIGHT_PX), COLORS["paper"])
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, WIDTH_PX, 670), fill=COLORS["green"])
    draw.rectangle((0, 650, WIDTH_PX, 670), fill=COLORS["orange"])
    draw.text((145, 115), "УЧЕБНАЯ ТОЧКА", font=font(116, True), fill=COLORS["white"])
    draw.text((150, 250), "«ТАКТИЧЕСКИЙ ДОМ»", font=font(94, True), fill="#E7D4AF")
    draw.text(
        (155, 392),
        "ОРГАНИЗАЦИЯ ПРОХОЖДЕНИЯ И ТРЕБОВАНИЯ БЕЗОПАСНОСТИ",
        font=font(43, True),
        fill=COLORS["white"],
    )
    draw.text(
        (155, 482),
        "Учебно-методический плакат · схема уточняется руководителем занятия",
        font=font(31),
        fill="#DDE7E2",
    )

    rounded_panel(
        draw,
        (2700, 105, 3445, 545),
        "#234C40",
        outline=COLORS["olive"],
        width=4,
        radius=28,
    )
    draw.text((2760, 155), "УТВЕРЖДАЮ", font=font(29, True), fill=COLORS["orange"])
    draw.text((2760, 215), "________________________", font=font(26), fill=COLORS["white"])
    draw.text((2760, 267), "Должность / Ф. И. О.", font=font(22), fill="#C7D8D1")
    draw.text((2760, 333), "«____» __________ 20___ г.", font=font(25), fill=COLORS["white"])
    draw.text((2760, 425), "ФОРМАТ 600 × 900 ММ", font=font(25, True), fill="#E7D4AF")

    draw_building_plan(draw)
    draw_legend_and_staff(draw)
    draw_stage_cards(draw)
    draw_safety_panels(draw)

    draw.line((150, 5210, 3450, 5210), fill=COLORS["paper_dark"], width=4)
    draw.text(
        (150, 5250),
        "МАКЕТ ДЛЯ ОРГАНИЗАЦИИ УЧЕБНОГО ЗАНЯТИЯ. НЕ ЗАМЕНЯЕТ УТВЕРЖДЁННУЮ ПРОГРАММУ И ИНСТРУКТАЖ.",
        font=font(25, True),
        fill=COLORS["gray"],
    )
    draw.text(
        (3160, 5250),
        "ЛИСТ 1/1",
        font=font(25, True),
        fill=COLORS["green"],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(PNG_PATH, format="PNG", optimize=True, dpi=(152.4, 152.4))


def create_pdf() -> None:
    page_width = WIDTH_MM * mm
    page_height = HEIGHT_MM * mm
    pdf = canvas.Canvas(str(PDF_PATH), pagesize=(page_width, page_height), pageCompression=1)
    pdf.setTitle("Учебная точка «Тактический дом» — 600 × 900 мм")
    pdf.setAuthor("Учебно-методический макет")
    pdf.setSubject("Организация учебного занятия и требования безопасности")
    pdf.drawImage(
        str(PNG_PATH),
        0,
        0,
        width=page_width,
        height=page_height,
        preserveAspectRatio=False,
        mask="auto",
    )
    pdf.showPage()
    pdf.save()


def set_all_borders(
    worksheet,
    min_row: int,
    max_row: int,
    min_col: int,
    max_col: int,
    color: str,
    style: str = "thin",
) -> None:
    side = Side(style=style, color=color)
    border = Border(left=side, right=side, top=side, bottom=side)
    for row in worksheet.iter_rows(
        min_row=min_row,
        max_row=max_row,
        min_col=min_col,
        max_col=max_col,
    ):
        for cell in row:
            cell.border = border


def style_heading(cell, fill: str = "173B31", size: int = 16) -> None:
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(name="Arial", size=size, bold=True, color="FFFFFF")
    cell.alignment = Alignment(horizontal="left", vertical="center")


def create_editable_sheet(workbook: Workbook) -> None:
    ws = workbook.create_sheet("Редактирование")
    ws.sheet_view.showGridLines = False
    for column, width in {
        "A": 4,
        "B": 23,
        "C": 23,
        "D": 23,
        "E": 23,
        "F": 23,
        "G": 23,
        "H": 23,
        "I": 4,
    }.items():
        ws.column_dimensions[column].width = width

    ws.merge_cells("B2:H3")
    ws["B2"] = "РЕДАКТИРУЕМЫЕ ДАННЫЕ ПЛАКАТА"
    style_heading(ws["B2"], size=20)
    ws["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.merge_cells("B4:H4")
    ws["B4"] = (
        "Измените значения в светлых ячейках и повторно запустите generate_poster.py "
        "для обновления печатного макета."
    )
    ws["B4"].font = Font(name="Arial", size=11, italic=True, color="69706C")
    ws["B4"].alignment = Alignment(wrap_text=True, vertical="center")

    sections = [
        (6, "РЕКВИЗИТЫ", [("Наименование точки", "Учебная точка «Тактический дом»"), ("Руководитель", ""), ("Дата занятия", ""), ("Экстренный контакт", "")]),
        (13, "СОСТАВ СМЕНЫ", [("Учебная группа А", "3 чел."), ("Учебная группа Б", "3 чел."), ("Руководитель занятия", "1 чел."), ("Инструкторы / наблюдатели", "по схеме"), ("Медицинское обеспечение", "назначено")]),
        (21, "ПРИМЕЧАНИЯ РУКОВОДИТЕЛЯ", [("Уточнение по объекту", ""), ("Дополнительные ограничения", ""), ("Место сбора", "")]),
    ]
    for start_row, title, values in sections:
        ws.merge_cells(start_row=start_row, start_column=2, end_row=start_row, end_column=8)
        heading = ws.cell(start_row, 2, title)
        style_heading(heading, size=14)
        for offset, (label, value) in enumerate(values, start=1):
            row = start_row + offset
            ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=3)
            ws.merge_cells(start_row=row, start_column=4, end_row=row, end_column=8)
            ws.cell(row, 2, label).font = Font(name="Arial", size=11, bold=True, color="173B31")
            ws.cell(row, 4, value).font = Font(name="Arial", size=11, color="1C2723")
            ws.cell(row, 4).fill = PatternFill("solid", fgColor="FFF9E9")
            for col in range(2, 9):
                ws.cell(row, col).alignment = Alignment(vertical="center", wrap_text=True)
            set_all_borders(ws, row, row, 2, 8, "D6CDBB")
            ws.row_dimensions[row].height = 32 if start_row != 21 else 46

    ws.merge_cells("B27:H27")
    ws["B27"] = "ОГРАНИЧЕНИЕ МАКЕТА"
    style_heading(ws["B27"], fill="A83A30", size=14)
    ws.merge_cells("B28:H30")
    ws["B28"] = (
        "Этот файл предназначен для оформления и организации безопасного учебного занятия. "
        "Маршруты внутри объекта, применение оборудования и последовательность специальных "
        "действий в макет не включены и утверждаются ответственным руководителем отдельно."
    )
    ws["B28"].font = Font(name="Arial", size=11, color="1C2723")
    ws["B28"].alignment = Alignment(wrap_text=True, vertical="center")
    ws["B28"].fill = PatternFill("solid", fgColor="F0D4C6")
    set_all_borders(ws, 28, 30, 2, 8, "A83A30")

    ws.freeze_panes = "B6"
    ws.print_area = "B2:H30"
    ws.page_setup.orientation = "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def create_schematic_sheet(workbook: Workbook) -> None:
    ws = workbook.create_sheet("Схема объекта")
    ws.sheet_view.showGridLines = False
    for col in range(1, 26):
        ws.column_dimensions[get_column_letter(col)].width = 4.5
    for row in range(1, 39):
        ws.row_dimensions[row].height = 24

    ws.merge_cells("B2:X4")
    ws["B2"] = "СХЕМА УЧЕБНОГО ОБЪЕКТА — РЕДАКТИРУЕМЫЙ ЛИСТ"
    style_heading(ws["B2"], size=18)
    ws["B2"].alignment = Alignment(horizontal="center", vertical="center")

    wall_color = "173B31"
    room_fill = PatternFill("solid", fgColor="E7D4AF")
    wall_side = Side(style="medium", color=wall_color)
    thin_side = Side(style="thin", color=wall_color)

    bay_ranges = [(2, 8), (9, 15), (16, 22)]
    for bay_index, (start_col, end_col) in enumerate(bay_ranges, start=1):
        for row in range(7, 30):
            for col in range(start_col, end_col + 1):
                ws.cell(row, col).fill = room_fill
                ws.cell(row, col).border = Border(
                    left=wall_side if col == start_col else thin_side if col == start_col + 2 else Side(),
                    right=wall_side if col == end_col else Side(),
                    top=wall_side if row == 7 else thin_side if row in (13, 19, 25) and col >= start_col + 2 else Side(),
                    bottom=wall_side if row == 29 else Side(),
                )
        for room_number, row in enumerate((9, 15, 21, 27), start=1):
            ws.merge_cells(
                start_row=row,
                start_column=start_col + 3,
                end_row=row + 1,
                end_column=end_col - 1,
            )
            room_cell = ws.cell(row, start_col + 3)
            room_cell.value = f"ЗОНА {bay_index}.{room_number}"
            room_cell.font = Font(name="Arial", size=10, bold=True, color=wall_color)
            room_cell.alignment = Alignment(horizontal="center", vertical="center")

        center_col = (start_col + end_col) // 2
        ws.merge_cells(start_row=31, start_column=center_col - 1, end_row=32, end_column=center_col + 1)
        entry = ws.cell(31, center_col - 1)
        entry.value = f"ВХОД {chr(ord('А') + bay_index - 1)}"
        entry.fill = PatternFill("solid", fgColor=wall_color)
        entry.font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
        entry.alignment = Alignment(horizontal="center", vertical="center")
        ws.merge_cells(start_row=34, start_column=center_col - 1, end_row=34, end_column=center_col + 1)
        exit_cell = ws.cell(34, center_col - 1)
        exit_cell.value = "↓ ЭВАКУАЦИЯ"
        exit_cell.font = Font(name="Arial", size=10, bold=True, color="3A7A57")
        exit_cell.alignment = Alignment(horizontal="center")

    ws.merge_cells("B36:V37")
    ws["B36"] = (
        "Маршрут внутри объекта и порядок действий назначает руководитель занятия "
        "по утверждённой программе."
    )
    ws["B36"].fill = PatternFill("solid", fgColor="FFF9E9")
    ws["B36"].font = Font(name="Arial", size=11, italic=True, color="69706C")
    ws["B36"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws.print_area = "B2:V37"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def create_instructions_sheet(workbook: Workbook) -> None:
    ws = workbook.create_sheet("Печать и использование")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 85

    ws.merge_cells("B2:C3")
    ws["B2"] = "ПЕЧАТЬ ПЛАКАТА 600 × 900 ММ"
    style_heading(ws["B2"], size=18)
    ws["B2"].alignment = Alignment(horizontal="center", vertical="center")

    instructions = [
        ("Готовый файл", "Для точной печати используйте PDF: uchebnaya_tochka_60x90.pdf."),
        ("Excel", "Лист «Плакат 60x90» настроен на одну страницу с пользовательским размером 600 × 900 мм."),
        ("Настройки печати", "Масштаб 100 %, без полей, книжная ориентация. Отключите «Подогнать к области печати» в драйвере типографии."),
        ("Редактирование", "Текстовые поля находятся на листе «Редактирование», схема — на листе «Схема объекта»."),
        ("Важно", "Перед использованием данные, схема объекта и меры безопасности должны быть проверены ответственным руководителем."),
    ]
    row = 5
    for title, value in instructions:
        ws.cell(row, 2, title)
        ws.cell(row, 3, value)
        ws.cell(row, 2).font = Font(name="Arial", size=12, bold=True, color="173B31")
        ws.cell(row, 3).font = Font(name="Arial", size=12, color="1C2723")
        ws.cell(row, 3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 48
        set_all_borders(ws, row, row, 2, 3, "D6CDBB")
        row += 1

    ws.print_area = f"B2:C{row}"


def create_xlsx() -> None:
    workbook = Workbook()
    poster_ws = workbook.active
    poster_ws.title = "Плакат 60x90"
    poster_ws.sheet_view.showGridLines = False

    # 60 × 90 cm at Excel's screen density of 96 dpi.
    for col in range(1, 25):
        poster_ws.column_dimensions[get_column_letter(col)].width = 12.0
    for row in range(1, 82):
        poster_ws.row_dimensions[row].height = 32.0
    poster_ws.merge_cells("A1:X81")
    poster_ws["A1"] = ""

    poster_image = XLImage(str(PNG_PATH))
    poster_image.width = 2268
    poster_image.height = 3402
    poster_ws.add_image(poster_image, "A1")

    poster_ws.print_area = "A1:X81"
    poster_ws.page_setup.orientation = "portrait"
    poster_ws.page_setup.paperWidth = "600mm"
    poster_ws.page_setup.paperHeight = "900mm"
    poster_ws.page_setup.fitToWidth = 1
    poster_ws.page_setup.fitToHeight = 1
    poster_ws.sheet_properties.pageSetUpPr.fitToPage = True
    poster_ws.page_margins.left = 0
    poster_ws.page_margins.right = 0
    poster_ws.page_margins.top = 0
    poster_ws.page_margins.bottom = 0
    poster_ws.page_margins.header = 0
    poster_ws.page_margins.footer = 0

    create_editable_sheet(workbook)
    create_schematic_sheet(workbook)
    create_instructions_sheet(workbook)

    workbook.calculation.fullCalcOnLoad = True
    workbook.calculation.forceFullCalc = True
    workbook.save(XLSX_PATH)


def verify_outputs() -> Iterable[str]:
    with Image.open(PNG_PATH) as image:
        assert image.size == (WIDTH_PX, HEIGHT_PX)
        yield f"PNG: {image.width} × {image.height} px"

    with PDF_PATH.open("rb") as pdf_file:
        header = pdf_file.read(8)
        assert header.startswith(b"%PDF-")
        yield f"PDF: {PDF_PATH.stat().st_size:,} bytes, page 600 × 900 mm"

    workbook = load_workbook(XLSX_PATH, read_only=False)
    assert workbook.sheetnames == [
        "Плакат 60x90",
        "Редактирование",
        "Схема объекта",
        "Печать и использование",
    ]
    poster_ws = workbook["Плакат 60x90"]
    assert poster_ws.page_setup.paperWidth == "600mm"
    assert poster_ws.page_setup.paperHeight == "900mm"
    assert len(poster_ws._images) == 1
    workbook.close()
    yield f"XLSX: {XLSX_PATH.stat().st_size:,} bytes, 4 sheets"


def main() -> None:
    create_poster_png()
    create_pdf()
    create_xlsx()
    for result in verify_outputs():
        print(result)


if __name__ == "__main__":
    main()
