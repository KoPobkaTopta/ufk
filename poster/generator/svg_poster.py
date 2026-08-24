# -*- coding: utf-8 -*-
"""Векторная версия плаката 600 × 900 мм (SVG → PDF/PNG)."""

from . import content as C
from . import plan as P
from . import style as S
from .svgkit import SVG

W, H = 600.0, 900.0
MG = 12.0                       # поле, мм

HEAD = (MG, 12.0, W - 2 * MG, 64.0)
TOP_Y, TOP_H = 80.0, 66.0
MAIN_Y, MAIN_H = 150.0, 358.0
PHASE_ROWS = [(512.0, 78.0), (596.0, 78.0)]
TECH_Y, TECH_H = 678.0, 140.0
FOOT_Y, FOOT_H = 822.0, 66.0

QUAD_W = (W - 2 * MG - 3 * 6.0) / 4.0
QUAD_X = [MG + i * (QUAD_W + 6.0) for i in range(4)]

PLAN_X, PLAN_W = MG, 378.0
SIDE_X, SIDE_W = MG + PLAN_W + 6.0, W - MG - (MG + PLAN_W + 6.0)

# масштаб схемы: 1 м = 15 мм (1:66,7)
MPM = 15.0
HOUSE_LEFT = PLAN_X + 42.0      # слева — стрелка направления, справа — выноски
FRONT_Y = 380.0


def hx(x):
    return HOUSE_LEFT + x * MPM


def hy(y):
    return FRONT_Y - y * MPM


def hc(color):
    return "#" + color


# ===========================================================================


def panel(svg, x, y, w, h, title=None, title_bg=S.BAND, title_fg="FFFFFF",
          body="FFFFFF", border=S.BAND, title_size=4.6, title_h=9.0,
          sw=0.7):
    svg.rect(x, y, w, h, fill=hc(body), stroke=hc(border), sw=sw)
    if title:
        svg.rect(x, y, w, title_h, fill=hc(title_bg))
        svg.text(x + 3.0, y + title_h * 0.71, title, size=title_size,
                 fill=hc(title_fg), weight="bold")
        return y + title_h
    return y


def build_header(svg):
    x, y, w, h = HEAD
    svg.rect(x, y, w, h, fill=hc(S.BAND))
    svg.rect(x, y, 4.0, h, fill=hc(S.ACCENT))
    svg.text(x + 12, y + 30, C.TITLE, size=19, fill="#FFFFFF", weight="bold",
             spacing="1.6")
    svg.text(x + 12, y + 42, C.SUBTITLE, size=5.4, fill="#E8C87A",
             weight="bold")
    svg.text(x + 12, y + 50.5, C.SUBTITLE2, size=4.2, fill="#C9D2DC")
    svg.text(x + 12, y + 59, C.STAMP, size=3.4, fill="#93A2B1", style="italic")
    svg.text(x + w - 8, y + 59, C.FORMAT_NOTE, size=3.4, fill="#93A2B1",
             style="italic", anchor="end")


def build_task(svg):
    x, w = MG, 360.0
    top = panel(svg, x, TOP_Y, w, TOP_H,
                "ОБСТАНОВКА, ЗАДАЧА И РАСПРЕДЕЛЕНИЕ ПО ВХОДАМ",
                body=S.LIGHT, title_size=4.3, title_h=8.5)
    y = top + 6.2
    for label, lines in C.TASK_BLOCKS:
        svg.text(x + 4, y, label, size=3.4, weight="bold", fill=hc(S.ACCENT))
        for line in lines:
            svg.text(x + 34, y, line, size=3.3, fill=hc(S.INK))
            y += 4.6
        y += 1.0
    y += 1.0
    for t in C.DISTRIBUTION:
        bold = t.startswith("ВХОД")
        svg.text(x + 4, y, t, size=3.3, fill=hc(S.INK),
                 weight="bold" if bold else "normal")
        y += 4.6


def build_orbat(svg):
    x = MG + 360.0 + 6.0
    w = W - MG - x
    top = panel(svg, x, TOP_Y, w, TOP_H, C.ORBAT_TITLE, body=S.LIGHT,
                title_size=4.3, title_h=8.5)
    cols = [x + 4, x + 18, x + 62, x + 118]
    y = top + 6.0
    svg.rect(x + 2, y - 4.0, w - 4, 5.6, fill=hc(S.BAND_2))
    for cx, head in zip(cols, ["№", "Кто", "Вооружение / имущество", "Задача"]):
        svg.text(cx, y, head, size=3.1, fill="#FFFFFF", weight="bold")
    y += 6.4
    palette = {"ПК": S.MG, "ГР": S.GL}
    for tag, who, arms, task in C.ORBAT:
        color = palette.get(tag, S.SHOOTER)
        svg.rect(cols[0] - 1.5, y - 3.6, 12.0, 5.0, fill=hc(color), rx=1)
        svg.text(cols[0] + 4.5, y, tag, size=3.0, fill="#FFFFFF",
                 weight="bold", anchor="middle")
        svg.text(cols[1], y, who, size=3.1, fill=hc(S.INK))
        svg.text(cols[2], y, arms, size=3.1, fill=hc(S.INK))
        svg.text(cols[3], y, task, size=3.1, fill=hc(S.GREY))
        y += 5.0
    for i, note in enumerate(C.ORBAT_NOTE):
        svg.text(x + 4, y + 1.2 + i * 4.0, note, size=2.9, fill=hc(S.GREY),
                 style="italic")


# ===========================================================================
#  Схема
# ===========================================================================

def draw_plan(svg):
    top = panel(svg, PLAN_X, MAIN_Y, PLAN_W, MAIN_H,
                "СХЕМА ОБЪЕКТА И ПОРЯДОК ДЕЙСТВИЙ  ·  масштаб 1:66,7  (1 м = 15 мм)",
                title_size=4.3, title_h=9.0)

    wood = svg.hatch("wood", hc(S.WALL), bg=hc("6E5C42"), angle=45,
                     spacing=1.1, sw=0.5)

    # местность
    svg.rect(PLAN_X + 1.5, top + 1.5, PLAN_W - 3, MAIN_Y + MAIN_H - top - 3,
             fill=hc(S.GROUND))
    # пол дома
    svg.rect(hx(0), hy(P.DEPTH), P.WIDTH * MPM, P.DEPTH * MPM,
             fill=hc(S.FLOOR))

    # секторы огня средств поддержки
    for tag, ax, ay, xl, xr, ytgt in P.fire_sectors():
        svg.polygon([(hx(ax), hy(ay)), (hx(xl), hy(ytgt)), (hx(xr), hy(ytgt))],
                    fill=hc(S.SUPPRESS), opacity=0.55)
        for xb in (xl, xr):
            svg.line(hx(ax), hy(ay), hx(xb), hy(ytgt), stroke=hc(S.ORANGE),
                     sw=0.5, dash="2,2")

    # дымовая завеса
    for i in range(11):
        cx = hx(0.9 + i * 1.62)
        svg.circle(cx, hy(-5.0), 8.0, fill=hc(S.SMOKE), opacity=0.85)
        svg.circle(cx + 6, hy(-4.3), 5.5, fill=hc(S.SMOKE), opacity=0.7)
    svg.text(hx(P.WIDTH / 2), hy(-5.0) + 1.6, "Д Ы М О В А Я   З А В Е С А",
             size=3.6, weight="bold", fill="#3E4B58", anchor="middle")

    # рубеж перехода в атаку
    svg.line(hx(-1.0), hy(P.ATTACK_LINE), hx(P.WIDTH + 1.0),
             hy(P.ATTACK_LINE), stroke=hc(S.ACCENT), sw=0.8, dash="5,3")
    svg.text(hx(P.WIDTH / 2), hy(P.ATTACK_LINE) - 2.2,
             "РУБЕЖ ПЕРЕХОДА В АТАКУ  30–50 м", size=3.5, weight="bold",
             fill=hc(S.ACCENT), anchor="middle")

    # стены
    for wall in P.walls():
        svg.rect(hx(wall.x), hy(wall.y + wall.h), wall.w * MPM, wall.h * MPM,
                 fill=wood, stroke=hc(S.WALL), sw=0.25)

    # проёмы
    for op in P.openings():
        x0, y0 = hx(op.x), hy(op.y + op.h)
        w0, h0 = op.w * MPM, op.h * MPM
        if op.tag == "window":
            svg.rect(x0, y0, w0, h0, fill="#FFFFFF", stroke=hc(S.WINDOW),
                     sw=0.5)
            if w0 > h0:
                svg.line(x0, y0 + h0 / 2, x0 + w0, y0 + h0 / 2,
                         stroke=hc(S.WINDOW), sw=0.5)
            else:
                svg.line(x0 + w0 / 2, y0, x0 + w0 / 2, y0 + h0,
                         stroke=hc(S.WINDOW), sw=0.5)
        elif op.tag == "link":
            svg.rect(x0, y0, w0, h0, fill=hc(S.VIOLET), opacity=0.5)
        else:
            svg.rect(x0, y0, w0, h0, fill="#FFFFFF", stroke=hc(S.DOOR),
                     sw=0.6)
            svg.line(x0, y0 + h0 / 2, x0 + w0, y0 + h0 / 2,
                     stroke=hc(S.DOOR), sw=1.4)

    draw_routes(svg)
    draw_marks(svg)
    draw_plan_labels(svg)
    draw_plan_annotations(svg)
    draw_scale(svg)


def _p(points):
    return [(hx(x), hy(y)) for x, y in points]


def draw_routes(svg):
    for i, off in enumerate(P.MODULE_OFFSETS):
        if i == 1:
            svg.polyline(_p([(off + 3.5, -1.0), (off + 3.5, 1.5)]),
                         stroke=hc(S.GREY), sw=1.0, dash="2,1.6", marker=True)
            continue

        door = off + (P.DOOR_X0 + P.DOOR_X1) / 2

        svg.polyline(_p([(off + 1.5, P.ATTACK_LINE + 0.2),
                         (off + 1.5, -2.3)]),
                     stroke=hc(S.ORANGE), sw=1.6, marker=True)

        route = [(off + 2.9, -1.05), (door, -1.05)] + P.snake_route(off)[1:]
        svg.polyline(_p(route), stroke=hc(S.GREEN), sw=1.5, marker=True)

        svg.polyline(_p(P.link_route(off)), stroke=hc(S.BLUE), sw=1.2,
                     dash="3,2")
        svg.polyline(_p([(off + P.CORRIDOR_AXIS, P.LINK_Y),
                         (off + P.CORRIDOR_AXIS, 1.6)]),
                     stroke=hc(S.BLUE), sw=1.2, dash="3,2", marker=True)
        svg.polyline(_p([(off + P.CORRIDOR_AXIS, P.LINK_Y + 0.6),
                         (off + P.CORRIDOR_AXIS, 13.1)]),
                     stroke=hc(S.BLUE), sw=1.2, dash="3,2", marker=True)

        # рубеж удержания коридора замыкающим
        svg.line(hx(off + 0.35), hy(1.95), hx(off + 2.45), hy(1.95),
                 stroke=hc(S.ACCENT), sw=0.7, dash="2,1.5")


def draw_marks(svg):
    palette = {"shooter": S.SHOOTER, "mg": S.MG, "gl": S.GL}
    marks = []
    for i, off in enumerate(P.MODULE_OFFSETS):
        if i == 1:
            continue
        grp = 1 if i == 0 else 2
        for k, x in enumerate((off + 1.0, off + 1.9, off + 2.8)):
            marks.append((x, -1.05, "%d-%d" % (grp, k + 1), "shooter"))
    marks.append((0.7, -6.7, "ГР", "gl"))
    marks.append((17.1, -6.7, "ПК", "mg"))

    for x, y, label, kind in marks:
        cx, cy = hx(x), hy(y)
        svg.circle(cx, cy, 5.0, fill=hc(palette[kind]), stroke="#FFFFFF",
                   sw=0.8)
        svg.text(cx, cy + 1.4, label, size=3.4, fill="#FFFFFF", weight="bold",
                 anchor="middle")

    svg.polyline(_p([(0.7, -6.0), (0.7, -1.9)]), stroke=hc(S.GL), sw=0.8,
                 dash="2,2", marker=True)
    svg.polyline(_p([(17.1, -6.0), (17.1, -1.9)]), stroke=hc(S.MG), sw=0.8,
                 dash="2,2", marker=True)


def _badge(svg, x, y, text, fill, size=3.0, rad=3.4):
    svg.circle(x, y, rad, fill=hc(fill), stroke="#FFFFFF", sw=0.5)
    svg.text(x, y + size * 0.38, text, size=size, fill="#FFFFFF",
             weight="bold", anchor="middle")


def draw_plan_labels(svg):
    for i, off in enumerate(P.MODULE_OFFSETS):
        cx = hx(off + 3.5)
        svg.rect(cx - 15, hy(1.75), 30, 6.0, fill="#FFFFFF", opacity=0.9, rx=1)
        svg.text(cx, hy(1.45), "ВХОД № %d" % (i + 1), size=4.0, weight="bold",
                 fill=hc(S.DOOR), anchor="middle")

    off = P.MODULE_OFFSETS[1]
    svg.text(hx(off + 1.4), hy(0.7), "ТАМБУР", size=3.0, weight="bold",
             fill=hc(S.GREY), anchor="middle")
    svg.text(hx(off + 1.25), hy(7.0), "СКВОЗНОЙ КОРИДОР ДО ТЫЛЬНОЙ СТЕНЫ",
             size=3.4, weight="bold", fill=hc(S.BLUE), anchor="middle",
             rotate=-90)
    svg.text(hx(off + 4.2), hy(13.15), "«ЗМЕЙКА»", size=3.6, weight="bold",
             fill=hc(S.GREEN), anchor="middle")

    for n, y in enumerate([2.4, 4.9, 7.4, 9.9, 11.9], start=1):
        _badge(svg, hx(4.25), hy(y), str(n), S.GREEN, size=2.8, rad=2.9)

    svg.text(hx(P.WIDTH / 2), hy(P.DEPTH) - 3.0,
             "ТЫЛЬНЫЕ ВЫХОДЫ — ПЕРЕКРЫТЬ НАБЛЮДЕНИЕМ И ОГНЁМ", size=3.4,
             weight="bold", fill=hc(S.ACCENT), anchor="middle")

    svg.text(hx(1.6), hy(-6.7) + 1.2, "ГРАНАТОМЁТЧИК  (левый фланг)",
             size=3.2, weight="bold", fill=hc(S.GL))
    svg.text(hx(16.2), hy(-6.7) + 1.2, "ПУЛЕМЁТЧИК  (правый фланг)",
             size=3.2, weight="bold", fill=hc(S.MG), anchor="end")
    svg.text(hx(9.0), hy(-0.5), "полоса огневого подавления фасада",
             size=2.8, style="italic", fill="#8A5A20", anchor="middle")
    svg.text(hx(0.3), hy(-2.4), "накопление у стены, ниже подоконников",
             size=2.8, style="italic", fill=hc(S.GREY))


PLAN_NOTES = [
    ("А", (17.9, 5.0), "Стены — брус 0,25 м. Пуля прошивает их насквозь: "
                       "стена скрывает, но не укрывает."),
    ("Б", (14.6, 10.75), "Сквозной проём коридор — «змейка». Здесь выше всего "
                         "риск поражения своих: работать по рубежам и докладам."),
    ("В", (13.25, 13.6), "Тыльная дверь коридора. Берётся под ствол первой — "
                         "через неё уходят и подходят."),
]


def draw_plan_annotations(svg):
    # общее направление штурма
    ax = PLAN_X + 15
    svg.polyline([(ax, hy(-7.0)), (ax, hy(5.0))], stroke=hc(S.GREY), sw=2.6,
                 marker=True, opacity=0.55)
    svg.text(ax - 5, (hy(-7.0) + hy(5.0)) / 2, "НАПРАВЛЕНИЕ ШТУРМА",
             size=4.0, weight="bold", fill=hc(S.GREY), anchor="middle",
             rotate=-90)

    # выноски справа
    tx = hx(P.WIDTH) + 5.0
    ty = hy(P.DEPTH) + 6.0
    for num, (px, py), _ in PLAN_NOTES:
        _badge(svg, hx(px), hy(py), num, S.ACCENT, size=2.8, rad=3.0)
    for num, _, note in PLAN_NOTES:
        _badge(svg, tx + 3.2, ty - 1.2, num, S.ACCENT, size=2.6, rad=2.8)
        for chunk in _wrap(note, 30):
            svg.text(tx + 8.0, ty, chunk, size=2.8, fill=hc(S.INK))
            ty += 3.9
        ty += 4.0


def draw_scale(svg):
    x0, y0 = PLAN_X + 8, MAIN_Y + MAIN_H - 12
    seg = MPM
    for i in range(5):
        svg.rect(x0 + i * seg, y0, seg, 2.4,
                 fill=hc(S.INK) if i % 2 == 0 else "#FFFFFF",
                 stroke=hc(S.INK), sw=0.3)
    svg.text(x0, y0 + 6.4, "0", size=2.8, fill=hc(S.INK), anchor="middle")
    svg.text(x0 + 5 * seg, y0 + 6.4, "5 м", size=2.8, fill=hc(S.INK),
             anchor="middle")
    svg.text(x0 + 5 * seg + 14, y0 + 2.2,
             "Направление штурма — снизу вверх (фронтальный штурм). "
             "Схема одинакова для всех трёх входов.",
             size=3.0, style="italic", fill=hc(S.GREY))


# ===========================================================================
#  Правая колонка
# ===========================================================================

def legend_symbol(svg, x, y, key):
    color = hc(S.LEGEND_COLORS[key])
    if key == "wall":
        svg.rect(x, y - 1.6, 11, 3.2, fill=color)
    elif key == "door":
        svg.rect(x, y - 1.6, 11, 3.2, fill="#FFFFFF", stroke=color, sw=0.5)
        svg.line(x, y, x + 11, y, stroke=color, sw=1.4)
    elif key == "window":
        svg.rect(x, y - 1.6, 11, 3.2, fill="#FFFFFF", stroke=color, sw=0.5)
        svg.line(x, y, x + 11, y, stroke=color, sw=0.5)
    elif key == "link":
        svg.rect(x, y - 1.6, 11, 3.2, fill=color, opacity=0.5)
    elif key == "route_snake":
        svg.polyline([(x, y + 1.4), (x + 5, y + 1.4), (x + 5, y - 1.4),
                      (x + 11, y - 1.4)], stroke=color, sw=1.3, marker=True)
    elif key == "route_corr":
        svg.polyline([(x, y), (x + 11, y)], stroke=color, sw=1.2, dash="3,2",
                     marker=True)
    elif key == "route_move":
        svg.polyline([(x, y), (x + 11, y)], stroke=color, sw=1.6, marker=True)
    elif key in ("shooter", "mg", "gl"):
        svg.circle(x + 5, y, 3.4, fill=color, stroke="#FFFFFF", sw=0.6)
    elif key == "sector":
        svg.polygon([(x, y + 2.2), (x + 11, y - 2.2), (x + 11, y + 2.2)],
                    fill=color, stroke=hc(S.ORANGE), sw=0.4, dash="1.5,1.5")
    elif key == "smoke":
        svg.circle(x + 3.5, y, 3.0, fill=color)
        svg.circle(x + 7.5, y - 0.8, 2.4, fill=color)
    elif key in ("line", "hold"):
        svg.line(x, y, x + 11, y, stroke=color, sw=0.9,
                 dash="4,2" if key == "line" else "2,1.5")


LEGEND_BOX = (MAIN_Y, 112.0)
SECTORS_BOX = (MAIN_Y + 116.0, 118.0)
ENTRY_BOX = (MAIN_Y + 238.0, 120.0)


def build_legend(svg):
    y0, h = LEGEND_BOX
    top = panel(svg, SIDE_X, y0, SIDE_W, h, C.LEGEND_TITLE, title_size=4.3,
                body=S.LIGHT, title_h=9.0)
    y = top + 7.0
    for key, label in C.LEGEND:
        legend_symbol(svg, SIDE_X + 5, y - 1.0, key)
        svg.text(SIDE_X + 21, y, label, size=3.2, fill=hc(S.INK))
        y += 7.0


def build_sectors(svg):
    y0, h = SECTORS_BOX
    top = panel(svg, SIDE_X, y0, SIDE_W, h, C.SECTORS_TITLE, title_size=4.3,
                title_h=9.0)
    y = top + 7.5
    for who, what in C.SECTORS:
        svg.text(SIDE_X + 5, y, who, size=3.4, weight="bold", fill=hc(S.INK))
        y += 4.6
        for chunk in _wrap(what, 74):
            svg.text(SIDE_X + 9, y, chunk, size=3.1, fill=hc(S.GREY))
            y += 4.4
        y += 1.6
    svg.rect(SIDE_X + 3, y - 3.5, SIDE_W - 6, y0 + h - y + 0.5,
             fill=hc(S.LIGHT))
    y += 2.5
    for rule in C.SECTOR_RULES:
        svg.circle(SIDE_X + 6.5, y - 1.1, 0.9, fill=hc(S.ACCENT))
        for chunk in _wrap(rule, 72):
            svg.text(SIDE_X + 10, y, chunk, size=3.0, fill=hc(S.INK))
            y += 4.2
        y += 1.2


def _entry_diagram(svg, x, y, w, h, mode):
    svg.rect(x, y, w, h, fill="#FFFFFF", stroke=hc(S.WALL), sw=1.2)
    dw = w * 0.22
    dx = x + w - dw - w * 0.12 if mode == "hook" else x + (w - dw) / 2
    svg.rect(dx, y + h - 1.2, dw, 2.4, fill="#FFFFFF", stroke=hc(S.DOOR),
             sw=0.5)
    svg.line(dx, y + h, dx + dw, y + h, stroke=hc(S.DOOR), sw=1.2)

    a = dx + dw * 0.3
    b = dx + dw * 0.7
    if mode == "hook":
        # разворот «крюком» вдоль той же стены, в углы по обе стороны проёма
        svg.polyline([(a, y + h - 1), (a, y + h - 8),
                      (x + w - 4, y + h - 8), (x + w - 4, y + h - 4)],
                     stroke=hc(S.GREEN), sw=1.1, marker=True)
        svg.polyline([(b, y + h - 1), (b, y + h - 13),
                      (x + 4, y + h - 13), (x + 4, y + h - 4)],
                     stroke=hc(S.BLUE), sw=1.1, marker=True)
    else:
        svg.polyline([(a, y + h - 1), (x + w - 3.5, y + 4)],
                     stroke=hc(S.GREEN), sw=1.1, marker=True)
        svg.polyline([(b, y + h - 1), (x + 3.5, y + 4)],
                     stroke=hc(S.BLUE), sw=1.1, marker=True)
    svg.text(x + 2, y - 1.4, "№ 1", size=2.8, weight="bold", fill=hc(S.GREEN))
    svg.text(x + w - 2, y - 1.4, "№ 2", size=2.8, weight="bold",
             fill=hc(S.BLUE), anchor="end")


def build_entry(svg):
    y0, h = ENTRY_BOX
    top = panel(svg, SIDE_X, y0, SIDE_W, h, C.ENTRY_TECHNIQUES_TITLE,
                title_size=4.3, title_h=9.0)
    y = top + 8.0
    for name, sub, lines in C.ENTRY_TECHNIQUES:
        svg.text(SIDE_X + 5, y, name, size=4.0, weight="bold", fill=hc(S.INK))
        svg.text(SIDE_X + 26, y, "— " + sub, size=3.0, style="italic",
                 fill=hc(S.GREY))
        _entry_diagram(svg, SIDE_X + 5, y + 5.0, 42, 34,
                       "hook" if "КРЮК" in name else "cross")
        ty = y + 8.0
        for line in lines:
            svg.text(SIDE_X + 52, ty, line, size=3.0, fill=hc(S.INK))
            ty += 4.4
        y += 48.0


def _wrap(text, width):
    words, out, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


# ===========================================================================
#  Этапы, приёмы, подвал
# ===========================================================================

def build_phases(svg):
    for i, ph in enumerate(C.PHASES):
        x = QUAD_X[i % 4]
        y, h = PHASE_ROWS[i // 4]
        svg.rect(x, y, QUAD_W, h, fill="#FFFFFF", stroke=hc(S.BAND), sw=0.7)
        svg.rect(x, y, QUAD_W, 11.0, fill=hc(S.BAND))
        svg.rect(x, y, 16.0, 11.0, fill=hc(S.ACCENT))
        svg.text(x + 8, y + 7.4, ph["no"], size=5.0, fill="#FFFFFF",
                 weight="bold", anchor="middle")
        svg.text(x + 19, y + 7.2, ph["name"], size=3.6, fill="#FFFFFF",
                 weight="bold")
        ty = y + 18.0
        for line in ph["lines"]:
            svg.text(x + 3.5, ty, line, size=3.3, fill=hc(S.INK))
            ty += 5.6


def build_techniques(svg):
    for i, p in enumerate(C.TECHNIQUE_PANELS):
        x = QUAD_X[i]
        danger = "БЕЗОПАСНОСТ" in p["title"]
        top = panel(svg, x, TECH_Y, QUAD_W, TECH_H, p["title"],
                    title_bg=S.ACCENT if danger else S.BAND,
                    body="FDF3F2" if danger else "FFFFFF",
                    border=S.ACCENT if danger else S.BAND,
                    title_size=3.9, title_h=10.0)
        ty = top + 9.0
        for line in p["lines"]:
            bold = danger and line.startswith("ДЕРЕВО")
            svg.text(x + 3.5, ty, line, size=3.3,
                     fill=hc(S.ACCENT) if bold else hc(S.INK),
                     weight="bold" if bold else "normal")
            ty += 5.6


def build_footer(svg):
    top = panel(svg, MG, FOOT_Y, W - 2 * MG, FOOT_H, C.SOURCES_TITLE,
                body=S.LIGHT, title_size=4.0, title_h=8.5)
    y = top + 6.5
    for i, src in enumerate(C.SOURCES, start=1):
        svg.text(MG + 5, y, "%d." % i, size=3.1, weight="bold",
                 fill=hc(S.ACCENT))
        svg.text(MG + 11, y, src, size=3.1, fill=hc(S.INK))
        y += 4.9
    svg.text(MG + 5, y + 2.5, C.FOOTER_NOTE, size=2.9, style="italic",
             fill=hc(S.GREY))

    fx = W - MG - 150
    svg.line(fx - 6, FOOT_Y + 10, fx - 6, FOOT_Y + FOOT_H - 4,
             stroke=hc(S.LIGHT_2), sw=0.6)
    fy = top + 8.0
    for f in C.FOOTER_FIELDS:
        svg.text(fx, fy, f, size=3.2, fill=hc(S.INK))
        fy += 8.0


def build(path_svg):
    svg = SVG(W, H, background=hc(S.PAPER))
    svg.rect(0, 0, W, H, fill="none", stroke=hc(S.BAND), sw=2.0)
    build_header(svg)
    build_task(svg)
    build_orbat(svg)
    draw_plan(svg)
    build_legend(svg)
    build_sectors(svg)
    build_entry(svg)
    build_phases(svg)
    build_techniques(svg)
    build_footer(svg)
    return svg.save(path_svg)
