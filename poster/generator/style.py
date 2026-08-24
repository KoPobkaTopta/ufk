# -*- coding: utf-8 -*-
"""Единая палитра для обеих версий плаката (Excel и вектор)."""

PAPER = "FFFFFF"
INK = "16202B"
BAND = "16202B"
BAND_2 = "2E3D4F"
LIGHT = "F2F0EA"
LIGHT_2 = "E6E2D8"
GREY = "6B7280"

ACCENT = "B3261E"        # красный — акценты, запреты, рубежи
GREEN = "1E7A44"         # ось «змейки»
BLUE = "1F5FA8"          # ось коридора
ORANGE = "C2691A"        # выдвижение и огонь поддержки
VIOLET = "6D28D9"        # сквозные проёмы

WALL = "3A3227"          # деревянная стена
FLOOR = "FFFFFF"         # пол внутри дома
GROUND = "EDE7D9"        # местность перед фасадом
SMOKE = "C6CBD2"         # дымовая завеса
SUPPRESS = "F6DDBC"      # полоса огневого подавления фасада
SECTOR_LIGHT = "FAEBD6"  # заливка сектора огня на схеме в Excel
DOOR = "C2410C"          # дверной проём
WINDOW = "0E7490"        # оконный проём

SHOOTER = "1E7A44"
MG = "1F5FA8"
GL = "C2410C"

LEGEND_COLORS = {
    "wall": WALL,
    "door": DOOR,
    "window": WINDOW,
    "link": VIOLET,
    "route_snake": GREEN,
    "route_corr": BLUE,
    "route_move": ORANGE,
    "shooter": SHOOTER,
    "mg": MG,
    "gl": GL,
    "sector": SUPPRESS,
    "smoke": SMOKE,
    "line": ACCENT,
    "hold": ACCENT,
}
