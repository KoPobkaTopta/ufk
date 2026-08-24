# -*- coding: utf-8 -*-
"""Минимальный конструктор SVG: единица измерения — миллиметр."""

FONT = "DejaVu Sans, Arial, Helvetica, sans-serif"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


class SVG:
    def __init__(self, width_mm, height_mm, background="#FFFFFF"):
        self.w = width_mm
        self.h = height_mm
        self.body = []
        self.defs = []
        self._markers = set()
        if background:
            self.rect(0, 0, width_mm, height_mm, fill=background)

    # -- примитивы ---------------------------------------------------------

    @staticmethod
    def _attrs(**kw):
        out = []
        for k, v in kw.items():
            if v is None:
                continue
            out.append('%s="%s"' % (k.replace("_", "-"), v))
        return " ".join(out)

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=0.35, rx=None,
             opacity=None, dash=None):
        self.body.append("<rect " + self._attrs(
            x=r(x), y=r(y), width=r(w), height=r(h), rx=rx,
            fill=fill or "none", stroke=stroke,
            stroke_width=r(sw) if stroke else None,
            stroke_dasharray=dash, opacity=opacity) + "/>")

    def line(self, x1, y1, x2, y2, stroke="#000", sw=0.35, dash=None,
             cap="butt", opacity=None, marker=None):
        m = self.marker(stroke) if marker else None
        self.body.append("<line " + self._attrs(
            x1=r(x1), y1=r(y1), x2=r(x2), y2=r(y2), stroke=stroke,
            stroke_width=r(sw), stroke_dasharray=dash, stroke_linecap=cap,
            opacity=opacity, marker_end=m) + "/>")

    def polyline(self, pts, stroke="#000", sw=0.6, dash=None, marker=False,
                 fill="none", opacity=None, cap="round", join="round"):
        m = self.marker(stroke) if marker else None
        d = " ".join("%s,%s" % (r(x), r(y)) for x, y in pts)
        self.body.append("<polyline " + self._attrs(
            points=d, fill=fill, stroke=stroke, stroke_width=r(sw),
            stroke_dasharray=dash, stroke_linecap=cap, stroke_linejoin=join,
            opacity=opacity, marker_end=m) + "/>")

    def polygon(self, pts, fill="#000", stroke=None, sw=0.3, opacity=None,
                dash=None):
        d = " ".join("%s,%s" % (r(x), r(y)) for x, y in pts)
        self.body.append("<polygon " + self._attrs(
            points=d, fill=fill, stroke=stroke,
            stroke_width=r(sw) if stroke else None, opacity=opacity,
            stroke_dasharray=dash) + "/>")

    def circle(self, cx, cy, rad, fill="#000", stroke=None, sw=0.3,
               opacity=None):
        self.body.append("<circle " + self._attrs(
            cx=r(cx), cy=r(cy), r=r(rad), fill=fill, stroke=stroke,
            stroke_width=r(sw) if stroke else None, opacity=opacity) + "/>")

    def text(self, x, y, s, size=3.2, fill="#16202B", anchor="start",
             weight="normal", style="normal", spacing=None, family=FONT,
             rotate=None, opacity=None):
        transform = None
        if rotate:
            transform = "rotate(%s %s %s)" % (r(rotate), r(x), r(y))
        self.body.append("<text " + self._attrs(
            x=r(x), y=r(y), fill=fill, font_size=r(size), font_family=family,
            font_weight=weight, font_style=style, text_anchor=anchor,
            letter_spacing=spacing, transform=transform,
            opacity=opacity) + ">" + esc(s) + "</text>")

    def lines(self, x, y, texts, size=3.2, step=None, fill="#16202B",
              weight="normal", anchor="start"):
        step = step or size * 1.45
        for i, t in enumerate(texts):
            self.text(x, y + i * step, t, size=size, fill=fill,
                      weight=weight, anchor=anchor)
        return y + len(texts) * step

    # -- маркеры-стрелки ---------------------------------------------------

    def marker(self, color):
        key = color.lstrip("#")
        mid = "arw" + key
        if mid not in self._markers:
            self._markers.add(mid)
            self.defs.append(
                '<marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" '
                'markerWidth="4.2" markerHeight="4.2" orient="auto-start-reverse" '
                'markerUnits="strokeWidth">'
                '<path d="M0.5,0.8 L9.5,5 L0.5,9.2 L2.6,5 z" fill="%s"/>'
                "</marker>" % (mid, color))
        return "url(#%s)" % mid

    def hatch(self, name, color, bg="none", angle=45, spacing=1.2, sw=0.45):
        self.defs.append(
            '<pattern id="%s" width="%s" height="%s" patternUnits="userSpaceOnUse" '
            'patternTransform="rotate(%s)">'
            '%s<line x1="0" y1="0" x2="0" y2="%s" stroke="%s" stroke-width="%s"/>'
            "</pattern>" % (
                name, r(spacing), r(spacing), angle,
                '<rect width="%s" height="%s" fill="%s"/>' % (
                    r(spacing), r(spacing), bg) if bg != "none" else "",
                r(spacing), color, r(sw)))
        return "url(#%s)" % name

    # -- вывод -------------------------------------------------------------

    def tostring(self):
        defs = "<defs>%s</defs>" % "".join(self.defs) if self.defs else ""
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'width="%smm" height="%smm" viewBox="0 0 %s %s" '
            'shape-rendering="geometricPrecision">\n%s\n%s\n</svg>\n'
            % (r(self.w), r(self.h), r(self.w), r(self.h), defs,
               "\n".join(self.body)))

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.tostring())
        return path


def r(v):
    if isinstance(v, str):
        return v
    return ("%.3f" % v).rstrip("0").rstrip(".") if isinstance(v, float) else v
