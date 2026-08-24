# -*- coding: utf-8 -*-
"""Сборка плаката 60 × 90 см в формате Excel (.xlsx).

Лист «ПЛАКАТ 60x90» — это холст из квадратных ячеек по 5 мм
(120 столбцов × 180 строк = 60 × 90 см). Остальные листы — рабочие
таблицы: расчёт, этапы, секторы, чек-лист руководителя занятия.
"""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties

from . import content as C
from . import plan as P
from . import style as S
from .canvas_xlsx import XlsxCanvas

COLS, ROWS = 120, 180

# --- разметка плаката (в ячейках) ------------------------------------------
M = 1                       # поле
HEAD_R0, HEAD_R1 = 1, 11
TOP_R0, TOP_R1 = 13, 26
MAIN_R0, MAIN_R1 = 28, 118
LEGEND_R = (28, 63)
SECTORS_R = (65, 86)
ENTRY_R = (88, 118)
PHASE_R = [(120, 134), (136, 150)]
TECH_R0, TECH_R1 = 152, 170
FOOT_R0, FOOT_R1 = 172, 178

PLAN_C0_PANEL, PLAN_C1_PANEL = 1, 78
SIDE_C0, SIDE_C1 = 80, 118
QUAD_COLS = [(1, 28), (31, 58), (61, 88), (91, 118)]

# --- привязка плана к сетке -------------------------------------------------
KNEE_Y = [2.4, 4.9, 7.4, 9.9, 11.9]     # середины колен «змейки»
KNEE_BADGE_X = 4.25                     # номера колен — по оси зоны «змейки»

PLAN_X0 = 4                 # столбец, соответствующий x = 0 м
PLAN_Y0 = 87                # строка фасадной стены (y = 0 м)
CPM = 4                     # ячеек в одном метре (ячейка = 0,25 м, масштаб 1:50)


def mx(x):
    return PLAN_X0 + int(round(x * CPM))


def my(y):
    return PLAN_Y0 - int(round(y * CPM))


def mrect(cv, x, y, w, h, color):
    cv.fill(mx(x), my(y + h) + 1, mx(x + w) - 1, my(y), color)


def mpath(pts):
    return [(mx(x), my(y)) for x, y in pts]


# ===========================================================================
#  Шапка
# ===========================================================================

def build_header(cv):
    cv.fill(M, HEAD_R0, COLS - M - 1, HEAD_R1, S.BAND)
    cv.text(M + 1, HEAD_R0 + 1, COLS - M - 2, HEAD_R0 + 5, C.TITLE,
            size=54, bold=True, color="FFFFFF", align="left")
    cv.text(M + 1, HEAD_R0 + 6, COLS - M - 2, HEAD_R0 + 7, C.SUBTITLE,
            size=14, bold=True, color="E8C87A", align="left")
    cv.text(M + 1, HEAD_R0 + 8, COLS - M - 2, HEAD_R0 + 9, C.SUBTITLE2,
            size=11, color="C9D2DC", align="left")
    cv.text(M + 1, HEAD_R0 + 10, 70, HEAD_R0 + 10, C.STAMP,
            size=9, italic=True, color="9AA8B6", align="left")
    cv.text(90, HEAD_R0 + 10, COLS - M - 2, HEAD_R0 + 10, C.FORMAT_NOTE,
            size=9, italic=True, color="9AA8B6", align="right")


# ===========================================================================
#  Верхняя полоса: задача и боевой расчёт
# ===========================================================================

def build_task(cv):
    c0, c1 = M, 66
    cv.panel(c0, TOP_R0, c1, TOP_R1, "ОБСТАНОВКА, ЗАДАЧА И РАСПРЕДЕЛЕНИЕ ПО ВХОДАМ",
             body_bg=S.LIGHT, title_size=11, title_rows=2)
    r = TOP_R0 + 2
    for label, lines in C.TASK_BLOCKS:
        for i, line in enumerate(lines):
            if i == 0:
                cv.text(c0 + 1, r, c0 + 8, r, label, size=10, bold=True,
                        color=S.ACCENT)
            cv.text(c0 + 9, r, c1 - 1, r, line, size=10, color=S.INK)
            r += 1
    for t in C.DISTRIBUTION:
        bold = t.startswith("ВХОД")
        cv.text(c0 + 1, r, c1 - 1, r, t, size=10, color=S.INK, bold=bold)
        r += 1


def build_orbat(cv):
    c0, c1 = 68, COLS - M - 1
    cv.panel(c0, TOP_R0, c1, TOP_R1, C.ORBAT_TITLE,
             body_bg=S.LIGHT, title_size=11, title_rows=2)
    widths = [4, 15, 16, 15]
    xs = [c0 + 1]
    for w in widths:
        xs.append(xs[-1] + w)
    heads = ["№", "Кто", "Вооружение / имущество", "Задача"]
    r = TOP_R0 + 2
    for i, h in enumerate(heads):
        cv.text(xs[i], r, xs[i + 1] - 1, r, h, size=9, bold=True,
                color="FFFFFF", fill=S.BAND_2)
    r += 1
    kinds = {"ПК": S.MG, "ГР": S.GL}
    for tag, who, arms, task in C.ORBAT:
        color = kinds.get(tag, S.SHOOTER)
        cv.text(xs[0], r, xs[1] - 1, r, tag, size=9, bold=True,
                color="FFFFFF", fill=color, align="center")
        cv.text(xs[1], r, xs[2] - 1, r, who, size=9, color=S.INK)
        cv.text(xs[2], r, xs[3] - 1, r, arms, size=9, color=S.INK)
        cv.text(xs[3], r, xs[4] - 1, r, task, size=9, color=S.GREY)
        r += 1
    for note in C.ORBAT_NOTE:
        cv.text(c0 + 1, r, c1 - 1, r, note, size=8, italic=True,
                color=S.GREY)
        r += 1


# ===========================================================================
#  Главная схема
# ===========================================================================

def draw_house(cv):
    # местность и пол
    cv.fill(PLAN_C0_PANEL + 1, MAIN_R0 + 3, PLAN_C1_PANEL - 1, 115, S.GROUND)
    mrect(cv, 0, 0, P.WIDTH, P.DEPTH, S.FLOOR)

    # секторы огня средств поддержки
    for tag, ax, ay, xl, xr, ytgt in P.fire_sectors():
        cv.polygon([(mx(ax) + 0.5, my(ay) + 0.5),
                    (mx(xl), my(ytgt) + 1),
                    (mx(xr), my(ytgt) + 1)], S.SECTOR_LIGHT)
        far = xr if abs(xr - ax) > abs(xl - ax) else xl
        cv.polyline([(mx(ax), my(ay)), (mx(far), my(ytgt) + 1)],
                    S.ORANGE, width=1, dash=(3, 4))

    # полоса огневого подавления фасада
    cv.fill(mx(0), my(0) + 1, mx(P.WIDTH) - 1, my(0) + 2, S.SUPPRESS)

    # дымовая завеса
    cv.fill(mx(0.5), my(-3.75), mx(P.WIDTH - 0.5), my(-5.0), S.SMOKE)
    cv.text(mx(6.0), my(-4.1), mx(12.0), my(-4.6),
            "Д Ы М О В А Я   З А В Е С А", size=9, bold=True,
            color="41505F", align="center", fill=S.SMOKE)

    # рубеж перехода в атаку
    cv.polyline([(mx(0.0), my(P.ATTACK_LINE)), (mx(P.WIDTH), my(P.ATTACK_LINE))],
                S.ACCENT, width=1, dash=(4, 3))
    cv.text(mx(4.0), my(P.ATTACK_LINE) - 2, mx(14.0), my(P.ATTACK_LINE) - 1,
            "РУБЕЖ ПЕРЕХОДА В АТАКУ  30–50 м", size=9, bold=True,
            color=S.ACCENT, align="center", fill=S.GROUND)

    # стены
    for w in P.walls():
        mrect(cv, w.x, w.y, w.w, w.h, S.WALL)

    # проёмы
    for op in P.openings():
        color = {"door_front": S.DOOR, "door_back": S.DOOR,
                 "window": S.WINDOW, "link": S.VIOLET}[op.tag]
        mrect(cv, op.x, op.y, op.w, op.h, color)


def draw_routes(cv):
    for i, off in enumerate(P.MODULE_OFFSETS):
        if i == 1:
            # центральный вход — резервная ось (вход обеспечения)
            cv.polyline(mpath([(off + 3.5, -0.7), (off + 3.5, 1.4)]),
                        S.GREY, width=1, dash=(2, 2), head=1, head_size=2)
            continue

        door = off + (P.DOOR_X0 + P.DOOR_X1) / 2

        # выдвижение к входу
        cv.polyline(mpath([(off + 1.5, P.ATTACK_LINE), (off + 1.5, -2.2)]),
                    S.ORANGE, width=2, head=1, head_size=2)

        # ось «змейки»
        route = [(off + 2.9, -1.0), (door, -1.0)] + P.snake_route(off)[1:]
        cv.polyline(mpath(route), S.GREEN, width=1, head=1, head_size=2)

        # ось коридора (после зачистки «змейки»)
        cv.polyline(mpath(P.link_route(off)), S.BLUE, width=1, dash=(3, 2))
        cv.polyline(mpath([(off + P.CORRIDOR_AXIS, P.LINK_Y),
                           (off + P.CORRIDOR_AXIS, 1.4)]),
                    S.BLUE, width=1, dash=(3, 2), head=1, head_size=2)
        cv.polyline(mpath([(off + P.CORRIDOR_AXIS, P.LINK_Y + 0.5),
                           (off + P.CORRIDOR_AXIS, 13.0)]),
                    S.BLUE, width=1, dash=(3, 2), head=1, head_size=2)

        # рубеж удержания коридора замыкающим
        cv.polyline(mpath([(off + 0.4, 1.9), (off + 2.4, 1.9)]),
                    S.ACCENT, width=1, dash=(2, 2))


def draw_marks(cv):
    palette = {"shooter": S.SHOOTER, "mg": S.MG, "gl": S.GL}
    positions = []
    for i, off in enumerate(P.MODULE_OFFSETS):
        if i == 1:
            continue
        grp = 1 if i == 0 else 2
        for k, x in enumerate((off + 1.0, off + 1.9, off + 2.8)):
            positions.append((x, -1.0, f"{grp}-{k + 1}", "shooter"))
    positions.append((0.7, -6.4, "ГР", "gl"))
    positions.append((17.1, -6.4, "ПК", "mg"))

    for x, y, label, kind in positions:
        c, r = mx(x), my(y)
        cv.fill(c - 1, r - 1, c + 1, r + 1, palette[kind])
        cv.text(c - 1, r - 1, c + 1, r + 1, label, size=8, bold=True,
                color="FFFFFF", align="center")
        cv.outline(c - 1, r - 1, c + 1, r + 1, color="FFFFFF", style="thin")

    # смена позиций поддержки после сигнала «Внутри»
    cv.polyline(mpath([(0.7, -5.7), (0.7, -3.0)]), S.GL,
                width=1, dash=(3, 2), head=1, head_size=2)
    cv.polyline(mpath([(17.1, -5.7), (17.1, -3.0)]), S.MG,
                width=1, dash=(3, 2), head=1, head_size=2)


def draw_plan_labels(cv):
    # номера входов — в тамбурах
    for i, off in enumerate(P.MODULE_OFFSETS):
        c = mx(off + 3.5)
        cv.text(c - 4, my(1.6), c + 4, my(1.1), f"ВХОД № {i + 1}",
                size=9, bold=True, color=S.DOOR, align="center", fill="FFFFFF")

    # экспликация в центральном секторе
    off = P.MODULE_OFFSETS[1]
    cv.text(mx(off + 0.4), my(0.9), mx(off + 2.4), my(0.4), "ТАМБУР",
            size=8, bold=True, color=S.GREY, align="center", fill="FFFFFF")
    cv.text(mx(off + 0.4), my(9.0), mx(off + 2.4), my(4.0),
            "СКВОЗНОЙ  КОРИДОР  ДО  ТЫЛЬНОЙ  СТЕНЫ", size=9, bold=True,
            color=S.BLUE, align="center", rotation=90, fill="FFFFFF")
    cv.text(mx(off + 2.9), my(13.4), mx(off + 5.6), my(12.6), "«ЗМЕЙКА»",
            size=9, bold=True, color=S.GREEN, align="center", fill="FFFFFF")

    # номера колен «змейки» в левом секторе
    for n, y in enumerate(KNEE_Y, start=1):
        c, r = mx(KNEE_BADGE_X), my(y)
        cv.fill(c, r - 1, c + 1, r, S.GREEN)
        cv.text(c, r - 1, c + 1, r, str(n), size=7, bold=True,
                color="FFFFFF", align="center")

    # тыльные выходы
    cv.text(mx(3.0), MAIN_R0 + 3, mx(15.0), MAIN_R0 + 3,
            "ТЫЛЬНЫЕ ВЫХОДЫ — ПЕРЕКРЫТЬ НАБЛЮДЕНИЕМ И ОГНЁМ",
            size=8, bold=True, color=S.ACCENT, align="center", fill=S.GROUND)

    # подписи средств поддержки
    r = my(-6.4)
    cv.text(mx(1.6), r - 1, mx(7.0), r + 1, "ГРАНАТОМЁТЧИК (левый фланг)",
            size=8, bold=True, color=S.GL, fill=S.GROUND)
    cv.text(mx(11.0), r - 1, mx(16.4), r + 1, "ПУЛЕМЁТЧИК (правый фланг)",
            size=8, bold=True, color=S.MG, align="right", fill=S.GROUND)
    cv.text(mx(6.0), my(-0.5), mx(12.0), my(-0.5),
            "полоса огневого подавления фасада", size=7, italic=True,
            color="8A5A20", align="center", fill=S.SUPPRESS)
    cv.text(mx(0.4), my(-2.4), mx(6.5), my(-2.4),
            "накопление у стены, ниже подоконников", size=7, italic=True,
            color=S.GREY, fill=S.SECTOR_LIGHT)


def build_plan(cv):
    cv.panel(PLAN_C0_PANEL, MAIN_R0, PLAN_C1_PANEL, MAIN_R1,
             "СХЕМА ОБЪЕКТА И ПОРЯДОК ДЕЙСТВИЙ · масштаб 1:50 · 1 клетка = 0,25 м",
             body_bg=S.PAPER, title_size=11, title_rows=3)
    draw_house(cv)
    draw_routes(cv)
    draw_marks(cv)
    draw_plan_labels(cv)

    # масштабная линейка 0–5 м
    r = 116
    for i in range(10):
        color = S.INK if i % 2 == 0 else "FFFFFF"
        cv.fill(mx(0) + i * 2, r, mx(0) + i * 2 + 1, r, color)
    cv.outline(mx(0), r, mx(0) + 19, r, color=S.INK, style="thin")
    cv.text(mx(0), r + 1, mx(0) + 19, r + 1, "0                                5 м",
            size=7, color=S.INK)
    cv.text(mx(6), r, mx(17), r + 1,
            "Направление штурма — снизу вверх (фронтальный штурм).",
            size=8, italic=True, color=S.GREY)


# ===========================================================================
#  Правая колонка
# ===========================================================================

def legend_swatch(cv, c, r, key):
    """Образец условного знака в одну строку сетки (5 мм)."""
    color = S.LEGEND_COLORS[key]
    if key in ("route_snake", "route_corr", "route_move"):
        dash = (3, 2) if key == "route_corr" else None
        cv.polyline([(c, r), (c + 4, r)], color, width=1, dash=dash,
                    head=1, head_size=1)
    elif key in ("line", "hold"):
        cv.polyline([(c, r), (c + 4, r)], color, width=1,
                    dash=(3, 2) if key == "line" else (1, 1))
    elif key in ("shooter", "mg", "gl"):
        cv.fill(c + 1, r, c + 3, r, color)
    else:
        cv.fill(c, r, c + 4, r, color)


def build_legend(cv):
    r0, r1 = LEGEND_R
    body = cv.panel(SIDE_C0, r0, SIDE_C1, r1, C.LEGEND_TITLE,
                    body_bg=S.LIGHT, title_size=11, title_rows=3)
    r = body + 1
    for key, label in C.LEGEND:
        legend_swatch(cv, SIDE_C0 + 2, r, key)
        cv.text(SIDE_C0 + 8, r, SIDE_C1 - 1, r + 1, label, size=10,
                color=S.INK)
        r += 2


def build_sectors(cv):
    r0, r1 = SECTORS_R
    body = cv.panel(SIDE_C0, r0, SIDE_C1, r1, C.SECTORS_TITLE,
                    body_bg=S.PAPER, title_size=11, title_rows=3)
    r = body + 1
    for who, what in C.SECTORS:
        cv.text(SIDE_C0 + 2, r, SIDE_C0 + 14, r, who, size=10, bold=True,
                color=S.INK)
        cv.text(SIDE_C0 + 3, r + 1, SIDE_C1 - 1, r + 1, what, size=9,
                color=S.GREY)
        r += 2
    cv.fill(SIDE_C0 + 1, r, SIDE_C1 - 1, r + len(C.SECTOR_RULES), S.LIGHT)
    r += 1
    for rule in C.SECTOR_RULES:
        cv.text(SIDE_C0 + 2, r, SIDE_C1 - 1, r, "•  " + rule, size=9,
                color=S.INK)
        r += 1


def _entry_diagram(cv, c, r, mode):
    """Мини-схема входа: «крюк» или «крест». Комната 10 × 8 ячеек."""
    w, h = 12, 8
    cv.fill(c, r, c + w, r + h, "F6F3EC")
    cv.fill(c, r, c + w, r, S.WALL)
    cv.fill(c, r, c, r + h, S.WALL)
    cv.fill(c + w, r, c + w, r + h, S.WALL)
    cv.fill(c, r + h, c + w, r + h, S.WALL)
    # проём в нижней стене
    if mode == "hook":
        d0 = c + w - 5
    else:
        d0 = c + w // 2 - 2
    cv.fill(d0, r + h, d0 + 3, r + h, S.DOOR)

    if mode == "hook":
        # разворот «крюком» вдоль той же стены, в углы по обе стороны проёма
        cv.polyline([(d0, r + h - 1), (d0, r + h - 2),
                     (c + w - 1, r + h - 2)],
                    S.GREEN, width=1, head=1, head_size=1)
        cv.polyline([(d0 + 3, r + h - 1), (d0 + 3, r + h - 4),
                     (c + 1, r + h - 4)],
                    S.BLUE, width=1, head=1, head_size=1)
    else:
        cv.polyline([(d0 + 1, r + h - 1), (c + w - 1, r + 1)],
                    S.GREEN, width=1, head=1, head_size=1)
        cv.polyline([(d0 + 2, r + h - 1), (c + 1, r + 1)],
                    S.BLUE, width=1, head=1, head_size=1)

    cv.text(c, r + h + 1, c + 5, r + h + 1, "№ 1", size=7, bold=True,
            color=S.GREEN, align="center")
    cv.text(c + 6, r + h + 1, c + w, r + h + 1, "№ 2", size=7, bold=True,
            color=S.BLUE, align="center")


def build_entry(cv):
    r0, r1 = ENTRY_R
    body = cv.panel(SIDE_C0, r0, SIDE_C1, r1, C.ENTRY_TECHNIQUES_TITLE,
                    body_bg=S.PAPER, title_size=11, title_rows=3)
    r = body + 1
    for name, sub, lines in C.ENTRY_TECHNIQUES:
        cv.text(SIDE_C0 + 2, r, SIDE_C0 + 12, r, name, size=10, bold=True,
                color=S.INK)
        cv.text(SIDE_C0 + 13, r, SIDE_C1 - 1, r, "— " + sub, size=9,
                italic=True, color=S.GREY)
        _entry_diagram(cv, SIDE_C0 + 2, r + 1, "hook" if "КРЮК" in name else "cross")
        for i, line in enumerate(lines):
            cv.text(SIDE_C0 + 16, r + 1 + i, SIDE_C1 - 1, r + 1 + i, line,
                    size=9, color=S.INK)
        r += 12


# ===========================================================================
#  Этапы и приёмы
# ===========================================================================

def build_phases(cv):
    for i, ph in enumerate(C.PHASES):
        c0, c1 = QUAD_COLS[i % 4]
        r0, r1 = PHASE_R[i // 4]
        cv.panel(c0, r0, c1, r1, None, body_bg=S.PAPER)
        cv.fill(c0, r0, c1, r0 + 2, S.BAND)
        cv.fill(c0, r0, c0 + 4, r0 + 2, S.ACCENT)
        cv.text(c0, r0, c0 + 4, r0 + 2, ph["no"], size=12, bold=True,
                color="FFFFFF", align="center")
        cv.text(c0 + 6, r0, c1, r0 + 2, ph["name"], size=10, bold=True,
                color="FFFFFF")
        r = r0 + 4
        for line in ph["lines"]:
            cv.text(c0 + 1, r, c1 - 1, r, line, size=10, color=S.INK)
            r += 1


def build_techniques(cv):
    for i, panel in enumerate(C.TECHNIQUE_PANELS):
        c0, c1 = QUAD_COLS[i]
        danger = "БЕЗОПАСНОСТ" in panel["title"]
        body = cv.panel(c0, TECH_R0, c1, TECH_R1, panel["title"],
                        title_bg=S.ACCENT if danger else S.BAND,
                        body_bg="FDF3F2" if danger else S.PAPER,
                        border=S.ACCENT if danger else S.BAND,
                        title_size=10, title_rows=3)
        r = body
        for line in panel["lines"]:
            bold = danger and line.startswith("ДЕРЕВО")
            cv.text(c0 + 1, r, c1 - 1, r, line, size=10,
                    color=S.ACCENT if bold else S.INK, bold=bold)
            r += 1


def build_footer(cv):
    cv.panel(M, FOOT_R0, COLS - M - 1, FOOT_R1, C.SOURCES_TITLE,
             body_bg=S.LIGHT, title_size=10, title_rows=2)
    r = FOOT_R0 + 2
    for i, src in enumerate(C.SOURCES, start=1):
        cv.text(M + 1, r, 96, r, f"{i}.  {src}", size=9, color=S.INK)
        r += 1
    r = FOOT_R0 + 2
    for f in C.FOOTER_FIELDS:
        cv.text(98, r, COLS - M - 2, r, f, size=9, color=S.INK)
        r += 1
    cv.text(98, r, COLS - M - 2, r + 1, C.FOOTER_NOTE, size=7, italic=True,
            color=S.GREY, wrap=True)


def build_poster_sheet(wb):
    ws = wb.create_sheet("ПЛАКАТ 60x90")
    cv = XlsxCanvas(ws, COLS, ROWS, background=S.PAPER)
    cv.fill(0, 0, COLS - 1, 0, S.BAND)
    cv.fill(0, ROWS - 1, COLS - 1, ROWS - 1, S.BAND)
    cv.fill(0, 0, 0, ROWS - 1, S.BAND)
    cv.fill(COLS - 1, 0, COLS - 1, ROWS - 1, S.BAND)

    build_header(cv)
    build_task(cv)
    build_orbat(cv)
    build_plan(cv)
    build_legend(cv)
    build_sectors(cv)
    build_entry(cv)
    build_phases(cv)
    build_techniques(cv)
    build_footer(cv)

    ws.print_area = f"A1:{get_column_letter(COLS)}{ROWS}"
    ws.page_setup.orientation = "portrait"
    ws.page_setup.paperSize = 66            # A2; для 60×90 задать размер в драйвере
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_margins.left = ws.page_margins.right = 0.2
    ws.page_margins.top = ws.page_margins.bottom = 0.2
    ws.sheet_view.zoomScale = 55
    return ws


# ===========================================================================
#  Рабочие листы-таблицы
# ===========================================================================

THIN = Side(style="thin", color="B9B4A8")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def _table_sheet(wb, name, title, headers, rows, widths, wrap_cols=()):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    t = ws.cell(row=1, column=1, value=title)
    t.font = Font(name="Arial", size=14, bold=True, color="FFFFFF")
    t.fill = PatternFill("solid", fgColor=S.BAND)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 28

    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=2, column=i, value=h)
        c.font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=S.BAND_2)
        c.alignment = Alignment(horizontal="center", vertical="center",
                                wrap_text=True)
        c.border = BORDER
    ws.row_dimensions[2].height = 30

    for r, row in enumerate(rows, start=3):
        for i, val in enumerate(row, start=1):
            c = ws.cell(row=r, column=i, value=val)
            c.font = Font(name="Arial", size=10)
            c.alignment = Alignment(vertical="top", wrap_text=True,
                                    horizontal="left")
            c.border = BORDER
            if r % 2 == 1:
                c.fill = PatternFill("solid", fgColor="F7F5F0")
    ws.freeze_panes = "A3"
    return ws


def build_tables(wb):
    _table_sheet(
        wb, "Расчёт", C.ORBAT_TITLE,
        ["№ на схеме", "Должность / номер", "Вооружение и имущество", "Задача"],
        [list(x) for x in C.ORBAT]
        + [["", "Примечание", "\n".join(C.ORBAT_NOTE), ""]],
        [12, 30, 38, 42],
    )

    phase_rows = []
    for ph in C.PHASES:
        phase_rows.append([ph["no"], ph["name"], "\n".join(ph["lines"])])
    ws = _table_sheet(
        wb, "Этапы", "ПОЭТАПНЫЙ ПОРЯДОК ШТУРМА",
        ["Этап", "Наименование", "Содержание действий"],
        phase_rows, [10, 38, 95],
    )
    for r in range(3, 3 + len(phase_rows)):
        ws.row_dimensions[r].height = 112

    _table_sheet(
        wb, "Секторы", C.SECTORS_TITLE + " · ПОЛЕ ВИДИМОСТИ",
        ["Номер расчёта", "Сектор наблюдения и огня"],
        [list(x) for x in C.SECTORS] + [["ПРАВИЛА", r] for r in C.SECTOR_RULES],
        [26, 100],
    )

    tech_rows = []
    for name, sub, lines in C.ENTRY_TECHNIQUES:
        tech_rows.append([name, sub, "\n".join(lines)])
    for panel in C.TECHNIQUE_PANELS:
        tech_rows.append([panel["title"], "", "\n".join(panel["lines"])])
    ws = _table_sheet(
        wb, "Приёмы", "ПРИЁМЫ, ПОЛЕ ВИДИМОСТИ И МЕРЫ БЕЗОПАСНОСТИ",
        ["Приём / раздел", "Условие применения", "Содержание"],
        tech_rows, [34, 30, 95],
    )
    for r in range(3, 3 + len(tech_rows)):
        ws.row_dimensions[r].height = 120

    checklist = [
        ["Перед занятием", "Доведены меры безопасности под роспись", ""],
        ["Перед занятием", "Проверено оружие, магазины, средства имитации", ""],
        ["Перед занятием", "Обозначены границы объекта и «красная зона»", ""],
        ["Перед занятием", "Назначены сигналы «СТОП» и «ОТБОЙ»", ""],
        ["Постановка задачи", "Доведены входы, оси движения, рубежи", ""],
        ["Постановка задачи", "Назначены секторы наблюдения и огня", ""],
        ["Постановка задачи", "Установлен порядок докладов и опознания", ""],
        ["Ход штурма", "Э-1 выдвижение и исходное положение", ""],
        ["Ход штурма", "Э-2 огневое подавление фасада", ""],
        ["Ход штурма", "Э-3 задымление и бросок к стене", ""],
        ["Ход штурма", "Э-4 вход в строение", ""],
        ["Ход штурма", "Э-5 зачистка «змейки»", ""],
        ["Ход штурма", "Э-6 коридор", ""],
        ["Ход штурма", "Э-7 соединение и закрепление", ""],
        ["Разбор", "Ошибки по секторам и мёртвым зонам", ""],
        ["Разбор", "Нарушения мер безопасности", ""],
        ["Разбор", "Оценка каждому номеру расчёта", ""],
    ]
    _table_sheet(
        wb, "Чек-лист", "ЧЕК-ЛИСТ РУКОВОДИТЕЛЯ ЗАНЯТИЯ",
        ["Раздел", "Что проверяется", "Отметка / замечания"],
        checklist, [22, 62, 46],
    )

    _table_sheet(
        wb, "Источники", C.SOURCES_TITLE,
        ["№", "Документ"],
        [[str(i), s] for i, s in enumerate(C.SOURCES, start=1)]
        + [["", C.FOOTER_NOTE]],
        [6, 120],
    )


def build(path):
    wb = Workbook()
    wb.remove(wb.active)
    build_poster_sheet(wb)
    build_tables(wb)
    wb.active = 0
    wb.save(path)
    return path
