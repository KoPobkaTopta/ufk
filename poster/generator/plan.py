"""Геометрия учебного тактического дома (полигон, деревянный сруб).

Все размеры — в метрах, начало координат — левый передний (фасадный) угол дома.
Ось X — вправо вдоль фасада, ось Y — в глубину дома (направление штурма).

Планировка по заданию: три входа в фасаде, за каждым входом — тамбур,
из тамбура вправо уходит «змейка» (последовательность колен с поперечными
стенками), а левее вдоль всего сектора идёт сквозной коридор до тыльной стены.

Модуль (сектор одного входа) повторяется три раза со смещением 0 / 6 / 12 м.
"""

from dataclasses import dataclass
from typing import List, Tuple

# --------------------------------------------------------------------------
# Основные габариты
# --------------------------------------------------------------------------

WALL = 0.25          # толщина стены (брус/бревно), м
MODULE_W = 6.0       # ширина сектора одного входа, м
MODULES = 3          # число входов
WIDTH = MODULE_W * MODULES   # 18.0 м по фасаду
DEPTH = 14.0         # глубина дома, м

VESTIBULE_D = 2.0    # глубина тамбура, м
CORRIDOR_X = 2.5     # положение продольной стены (левый край стены), м от края модуля
DOOR_X0, DOOR_X1 = 3.0, 4.0      # входной проём в модуле, м
CORRIDOR_AXIS = 1.25             # ось коридора в модуле, м

OUTSIDE_D = 7.75     # глубина отображаемой зоны перед фасадом, м
ATTACK_LINE = -6.0   # рубеж перехода в атаку, м от фасада
SMOKE_LINE = -3.0    # рубеж постановки дымов, м от фасада

MODULE_OFFSETS = [0.0, 6.0, 12.0]

# Поперечные стенки «змейки»: (глубина, левый край, правый край) в координатах модуля.
# Проход остаётся с той стороны, где стенка не доходит до продольной/наружной стены.
SNAKE_WALLS = [
    (4.5, 4.0, 6.0),    # проход слева  (2.75 … 4.00), ось 3.4
    (7.0, 2.5, 4.5),    # проход справа (4.50 … 5.75), ось 5.1
    (9.5, 4.0, 6.0),    # проход слева
    (12.0, 2.5, 4.5),   # проход справа
]
SNAKE_LEFT_AXIS = 3.4
SNAKE_RIGHT_AXIS = 5.1

# Проёмы в продольной стене — связь коридора и «змейки»
LINK_OPENINGS = [(5.5, 6.25), (10.5, 11.25)]


@dataclass(frozen=True)
class Rect:
    """Прямоугольник в метрах: левый нижний угол + размеры."""
    x: float
    y: float
    w: float
    h: float
    tag: str = ""


# --------------------------------------------------------------------------
# Проёмы в наружных стенах
# --------------------------------------------------------------------------

def front_doors() -> List[Tuple[float, float]]:
    """Входные проёмы в фасаде (глобальные координаты по X)."""
    return [(off + DOOR_X0, off + DOOR_X1) for off in MODULE_OFFSETS]


def front_windows() -> List[Tuple[float, float]]:
    """Окна фасада: по одному на коридор и на «змейку» в каждом модуле."""
    out = []
    for off in MODULE_OFFSETS:
        out.append((off + 0.75, off + 1.75))
        out.append((off + 4.75, off + 5.75))
    return out


def back_doors() -> List[Tuple[float, float]]:
    """Тыльные выходы — в торце каждого коридора."""
    return [(off + 0.75, off + 1.75) for off in MODULE_OFFSETS]


def back_windows() -> List[Tuple[float, float]]:
    return [(off + 4.25, off + 5.25) for off in MODULE_OFFSETS]


def side_windows() -> List[Tuple[float, float, str]]:
    """Окна в торцевых стенах: (y0, y1, 'L'|'R')."""
    out = []
    for y0 in (3.0, 8.0, 12.0):
        out.append((y0, y0 + 1.0, "L"))
        out.append((y0, y0 + 1.0, "R"))
    return out


def _subtract(span: Tuple[float, float], holes: List[Tuple[float, float]]):
    """Вырезать проёмы из отрезка стены."""
    segments = [span]
    for h0, h1 in sorted(holes):
        new = []
        for s0, s1 in segments:
            if h1 <= s0 or h0 >= s1:
                new.append((s0, s1))
                continue
            if s0 < h0:
                new.append((s0, h0))
            if h1 < s1:
                new.append((h1, s1))
        segments = new
    return [s for s in segments if s[1] - s[0] > 1e-6]


# --------------------------------------------------------------------------
# Стены
# --------------------------------------------------------------------------

def walls() -> List[Rect]:
    """Все стены дома в виде прямоугольников (проёмы уже вырезаны)."""
    out: List[Rect] = []

    # Фасад
    holes = sorted(front_doors() + front_windows())
    for x0, x1 in _subtract((0.0, WIDTH), holes):
        out.append(Rect(x0, 0.0, x1 - x0, WALL, "outer"))

    # Тыльная стена
    holes = sorted(back_doors() + back_windows())
    for x0, x1 in _subtract((0.0, WIDTH), holes):
        out.append(Rect(x0, DEPTH - WALL, x1 - x0, WALL, "outer"))

    # Торцевые стены
    left_holes = [(y0, y1) for y0, y1, s in side_windows() if s == "L"]
    right_holes = [(y0, y1) for y0, y1, s in side_windows() if s == "R"]
    for y0, y1 in _subtract((0.0, DEPTH), left_holes):
        out.append(Rect(0.0, y0, WALL, y1 - y0, "outer"))
    for y0, y1 in _subtract((0.0, DEPTH), right_holes):
        out.append(Rect(WIDTH - WALL, y0, WALL, y1 - y0, "outer"))

    # Стены между секторами входов
    for x in (MODULE_W - WALL, 2 * MODULE_W - WALL):
        out.append(Rect(x, 0.0, WALL, DEPTH, "inner"))

    # Внутренние стены каждого модуля
    for off in MODULE_OFFSETS:
        # продольная стена «коридор / змейка» с двумя сквозными проёмами
        for y0, y1 in _subtract((VESTIBULE_D, DEPTH - WALL), LINK_OPENINGS):
            out.append(Rect(off + CORRIDOR_X, y0, WALL, y1 - y0, "inner"))
        # поперечные стенки «змейки»
        for y, x0, x1 in SNAKE_WALLS:
            x_end = min(off + x1, off + MODULE_W - WALL)
            out.append(Rect(off + x0, y, x_end - (off + x0), WALL, "inner"))

    return out


def openings() -> List[Rect]:
    """Проёмы, которые надо подписать/отрисовать отдельным знаком."""
    out: List[Rect] = []
    for x0, x1 in front_doors():
        out.append(Rect(x0, 0.0, x1 - x0, WALL, "door_front"))
    for x0, x1 in back_doors():
        out.append(Rect(x0, DEPTH - WALL, x1 - x0, WALL, "door_back"))
    for x0, x1 in front_windows():
        out.append(Rect(x0, 0.0, x1 - x0, WALL, "window"))
    for x0, x1 in back_windows():
        out.append(Rect(x0, DEPTH - WALL, x1 - x0, WALL, "window"))
    for y0, y1, side in side_windows():
        x = 0.0 if side == "L" else WIDTH - WALL
        out.append(Rect(x, y0, WALL, y1 - y0, "window"))
    for off in MODULE_OFFSETS:
        for y0, y1 in LINK_OPENINGS:
            out.append(Rect(off + CORRIDOR_X, y0, WALL, y1 - y0, "link"))
    return out


# --------------------------------------------------------------------------
# Маршруты движения
# --------------------------------------------------------------------------

def snake_route(off: float) -> List[Tuple[float, float]]:
    """Ось движения по «змейке» (ортогональная ломаная), метры."""
    a, b = off + SNAKE_LEFT_AXIS, off + SNAKE_RIGHT_AXIS
    door = off + (DOOR_X0 + DOOR_X1) / 2
    return [
        (door, -1.5),
        (door, 1.0),
        (b, 1.0),
        (b, 3.6),
        (a, 3.6),
        (a, 6.1),
        (b, 6.1),
        (b, 8.6),
        (a, 8.6),
        (a, 11.1),
        (b, 11.1),
        (b, 13.0),
    ]


LINK_Y = 10.75           # ось прохода из «змейки» в коридор


def corridor_route(off: float) -> List[Tuple[float, float]]:
    """Ось движения по коридору до тыльной стены, метры."""
    axis = off + CORRIDOR_AXIS
    return [
        (off + (DOOR_X0 + DOOR_X1) / 2, 1.0),
        (axis, 1.0),
        (axis, 13.0),
    ]


def link_route(off: float) -> List[Tuple[float, float]]:
    """Выход из «змейки» в коридор через дальний сквозной проём."""
    return [
        (off + SNAKE_RIGHT_AXIS, 11.1),
        (off + SNAKE_RIGHT_AXIS, LINK_Y),
        (off + CORRIDOR_AXIS, LINK_Y),
    ]


def approach_route(off: float, from_x: float) -> List[Tuple[float, float]]:
    """Выдвижение от рубежа перехода в атаку к своему входу."""
    door = off + (DOOR_X0 + DOOR_X1) / 2
    return [
        (from_x, ATTACK_LINE),
        (from_x, -2.5),
        (door, -2.5),
        (door, -0.6),
    ]


# --------------------------------------------------------------------------
# Боевой расчёт на схеме
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Mark:
    x: float
    y: float
    label: str
    kind: str          # 'shooter' | 'mg' | 'gl' | 'commander'
    note: str = ""


def marks() -> List[Mark]:
    """Положения личного состава к началу этапа входа (Э-3/Э-4)."""
    out: List[Mark] = []

    # Штурмовая группа №1 — вход №1 (левый сектор)
    out.append(Mark(2.6, -0.9, "1-1", "shooter", "головной"))
    out.append(Mark(2.6, -1.7, "1-2", "shooter", "второй"))
    out.append(Mark(2.6, -2.5, "1-3", "shooter", "замыкающий"))

    # Штурмовая группа №2 — вход №3 (правый сектор)
    out.append(Mark(16.4, -0.9, "2-1", "shooter", "головной"))
    out.append(Mark(16.4, -1.7, "2-2", "shooter", "второй"))
    out.append(Mark(16.4, -2.5, "2-3", "shooter", "замыкающий"))

    # Группа огневой поддержки
    out.append(Mark(0.6, -6.6, "ГР", "gl", "гранатомётчик"))
    out.append(Mark(17.2, -6.6, "ПК", "mg", "пулемётчик"))

    return out


def support_positions() -> List[Tuple[str, float, float, float, float]]:
    """Запасные позиции поддержки после сигнала «Внутри»:
    (метка, x0, y0, x1, y1) — перемещение на фланг/в тыл."""
    return [
        ("ГР", 0.6, -6.6, -2.2, 6.0),
        ("ПК", 17.2, -6.6, 20.2, 6.0),
    ]


def fire_sectors():
    """Секторы огня средств поддержки по фасаду: (x, y, x_left, x_right, y_target)."""
    return [
        ("ГР", 0.6, -6.6, 0.5, 9.5, 0.0),
        ("ПК", 17.2, -6.6, 8.5, 17.5, 0.0),
    ]
