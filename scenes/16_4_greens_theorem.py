"""16.4 Green's theorem in the plane (Thomas' Calculus, 13e ed.)

Concept videos (2D, FlatScene):
  DoubleIntegralRefresher  double integrals: tiny rectangles, iterated integrals, vertical strips
  CurlDivergence           curl N_x - M_y (spin per area, paddle wheel), div M_x + N_y (outflow per area)
  GreensTheorem            orientation, inner edges cancel, both forms, old example, area formula

Exercises (fully worked):
  Ex16_4_05  (x-y) i + (y-x) j, unit square        -> circulation 0, flux 2
  Ex16_4_07  (y^2-x^2) i + (x^2+y^2) j, triangle    -> circulation 9, flux -9
  Ex16_4_09  (xy+y^2) i + (x-y) j, lens y=x^2,x=y^2 -> circulation -7/60, flux -11/60
  Ex16_4_22  oint 3y dx + 2x dy, under sin x        -> -2
  Ex16_4_26  area of the ellipse                    -> pi a b

Colours: curl/circulation ORANGE, divergence/flux PURPLE, region R light blue, boundary C BLUE (CCW arrows),
vertical strip YELLOW.  Voiceover: VO dict (literal from the task block).
Render (one at a time): .\\.venv\\Scripts\\python.exe render.py scenes\\16_4_greens_theorem.py <Scene> --low
"""
from manim import *
import numpy as np

from _exercise import FlatScene, C_ANSWER, C_WRONG, NB_LEFT, NB_RIGHT, NB_W, LEFT_CENTER

OUTPUT = {
    "DoubleIntegralRefresher": "16.4 Green's theorem/Concept/0 - Double integrals refresher",
    "CurlDivergence": "16.4 Green's theorem/Concept/1 - Curl & divergence",
    "GreensTheorem": "16.4 Green's theorem/Concept/2 - Green's theorem",
    "Ex16_4_05": "16.4 Green's theorem/Exercises/Ex 05",
    "Ex16_4_07": "16.4 Green's theorem/Exercises/Ex 07",
    "Ex16_4_09": "16.4 Green's theorem/Exercises/Ex 09",
    "Ex16_4_22": "16.4 Green's theorem/Exercises/Ex 22",
    "Ex16_4_26": "16.4 Green's theorem/Exercises/Ex 26",
}

C_CURL = ORANGE
C_DIV = PURPLE
C_REG = BLUE_C          # region fill (with low opacity)
C_BND = BLUE            # boundary C
C_STRIP = YELLOW

CHECK_GREEN = ["1 partials", r"2 curl / div", r"3 $\iint_R$", "4 check"]
CHECK_DI = ["1 sketch", "2 strip", "3 inner", "4 outer"]


# ----------------------------------------------------------------------------- helpers
def card_left(scene, content, color=YELLOW, center=LEFT_CENTER, width=7.4):
    if content.width > width - 0.6:
        content.scale_to_fit_width(width - 0.6)
    if content.height > 7.0:
        content.scale_to_fit_height(7.0)
    content.move_to(center)
    bg = RoundedRectangle(corner_radius=0.2, width=width, height=min(max(content.height + 1.0, 2.2), 7.6),
                          fill_color="#141414", fill_opacity=0.97, stroke_color=color, stroke_width=2)
    bg.move_to(center)
    return VGroup(bg, content)


def put_in(scene, owner, *mobs):
    """Mobjects animated in separately become part of `owner` only (so they scroll/fade with it)."""
    scene.remove(*mobs)
    owner.add(*mobs)


def boxed(scene, mob, color=C_ANSWER, buff=0.12):
    b = SurroundingRectangle(mob, color=color, buff=buff)
    scene.play(Create(b), run_time=0.6)
    put_in(scene, mob, b)
    return b


def settle(scene, mob):
    scene.remove(*mob.get_family()[1:])
    scene.add(mob)


def tip_at(func, t, color=C_BND, reverse=False, size=0.26, eps=0.01):
    a, b = (t + eps, t - eps) if reverse else (t - eps, t + eps)
    p, q = func(a), func(b)
    tri = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(size / 2)
    tri.rotate(np.arctan2(q[1] - p[1], q[0] - p[0]) - PI / 2).move_to((p + q) / 2)
    return tri


def left_axes(x_range, y_range, unit, center=np.array([-3.4, -0.3, 0]), numbers=True, font=22):
    ax = Axes(x_range=x_range, y_range=y_range, x_length=(x_range[1] - x_range[0]) * unit,
              y_length=(y_range[1] - y_range[0]) * unit, tips=False,
              axis_config={"stroke_color": GRAY_B, "include_numbers": numbers, "font_size": font})
    ax.move_to(center)
    lab = VGroup(MathTex("x", font_size=30).next_to(ax.x_axis, RIGHT, buff=0.1),
                 MathTex("y", font_size=30).next_to(ax.y_axis, UP, buff=0.1))
    return ax, lab


def region_between(ax, bottom, top, a, b, n=80, opacity=0.3):
    xs = np.linspace(a, b, n)
    pts = [ax.c2p(x, bottom(x)) for x in xs] + [ax.c2p(x, top(x)) for x in xs[::-1]]
    return Polygon(*pts, stroke_width=0, fill_color=C_REG, fill_opacity=opacity)


def boundary_between(ax, bottom, top, a, b, n=80, tips=(0.5,), width=5):
    """CCW boundary of {a<=x<=b, bottom<=y<=top}: bottom left->right, (right side), top right->left, (left side)."""
    xs = np.linspace(a, b, n)
    pts = [ax.c2p(x, bottom(x)) for x in xs]
    if abs(top(b) - bottom(b)) > 1e-9:
        pts.append(ax.c2p(b, top(b)))
    pts += [ax.c2p(x, top(x)) for x in xs[::-1]]
    if abs(top(a) - bottom(a)) > 1e-9:
        pts.append(ax.c2p(a, bottom(a)))
    curve = VMobject(stroke_color=C_BND, stroke_width=width)
    curve.set_points_as_corners(pts)
    tri = VGroup()
    for s in tips:
        x = a + s * (b - a)
        tri.add(tip_at(lambda u: ax.c2p(u, bottom(u)), x))
        tri.add(tip_at(lambda u: ax.c2p(u, top(u)), x, reverse=True))
    return VGroup(curve, tri)


def strip(ax, xt, bottom, top, w=0.03):
    def mk():
        x = xt.get_value()
        return Polygon(ax.c2p(x - w, bottom(x)), ax.c2p(x + w, bottom(x)), ax.c2p(x + w, top(x)),
                       ax.c2p(x - w, top(x)), stroke_color=C_STRIP, stroke_width=2, fill_color=C_STRIP,
                       fill_opacity=0.55)
    return always_redraw(mk)


def strip_labels(ax, xt, bottom, top, btex, ttex, size=26):
    lb = MathTex(btex, font_size=size, color=C_STRIP)
    lt = MathTex(ttex, font_size=size, color=C_STRIP)
    lb.add_updater(lambda m: m.next_to(ax.c2p(xt.get_value(), bottom(xt.get_value())), DOWN, buff=0.55))
    lt.add_updater(lambda m: m.next_to(ax.c2p(xt.get_value(), top(xt.get_value())), UP, buff=0.15))
    return VGroup(lb, lt)


def paddle(r=0.35, color=WHITE):
    hub = Circle(radius=r * 0.22, fill_color=color, fill_opacity=1, stroke_width=0)
    blades = VGroup(*[Line(ORIGIN, r * np.array([np.cos(a), np.sin(a), 0]), stroke_width=4, color=color)
                      for a in np.arange(4) * PI / 2])
    tips = VGroup(*[Rectangle(width=r * 0.18, height=r * 0.5, fill_color=color, fill_opacity=1, stroke_width=0)
                    .rotate(a).move_to(r * np.array([np.cos(a), np.sin(a), 0])) for a in np.arange(4) * PI / 2])
    return VGroup(blades, tips, hub)


def spin(wheel, omega):
    """Rotate continuously (rad/s); omega > 0 counterclockwise."""
    wheel.add_updater(lambda m, dt: m.rotate(omega * dt))
    return wheel


def mini_field(center, func, half=1.35, n=5, s=0.32, color=GRAY_B):
    """Small arrow field (normalised arrows of length <= s) in a square panel around `center`."""
    g = VGroup()
    vals = []
    pts = np.linspace(-1, 1, n)
    for x in pts:
        for y in pts:
            u, v = func(x, y)
            vals.append(np.hypot(u, v))
    vmax = max(vals) or 1.0
    for x in pts:
        for y in pts:
            u, v = func(x, y)
            L = np.hypot(u, v)
            if L < 1e-9:
                continue
            d = np.array([u, v, 0]) / L
            p = center + half * 0.85 * np.array([x, y, 0])
            ln = s * (0.35 + 0.65 * L / vmax)
            g.add(Arrow(p - 0.5 * ln * d, p + 0.5 * ln * d, buff=0, stroke_width=2.5, color=color,
                        max_tip_length_to_length_ratio=0.35))
    return g


VO = {}

# =============================================================================
VO["refresh"] = [
    "Green's theorem turns a line integral around a closed curve into a double integral over the region inside. So before we start, here is a short refresher on double integrals. If you are already comfortable with them, you can skip this video.",
    "A single integral adds up f of x times d x along an interval. A double integral adds up f of x y times d A over a region in the plane. Cut the region into tiny rectangles of area delta x times delta y, multiply each one by the value of f there, and add everything up.",
    "If f is positive, the double integral is the volume under the surface z equals f of x y, above the region R. And if f equals one, the double integral is simply the area of R.",
    "On a rectangle, we compute a double integral as two ordinary integrals, one inside the other. Example: the integral of x plus y over the square from zero to one, in both directions.",
    "First the inner integral, with respect to y, treating x as a constant. The integral of x plus y, d y, from zero to one, gives x plus one half.",
    "Then the outer integral, with respect to x. The integral of x plus one half, from zero to one, gives one half plus one half, which is one.",
    "Most regions are not rectangles. Take the triangle bounded by y equals zero, x equals one, and y equals x. Draw a vertical strip at position x. The strip starts at the bottom curve, y equals zero, and ends at the top curve, y equals x.",
    "So the inner integral runs from y equals zero to y equals x, and the outer integral runs over all strips, from x equals zero to x equals one. The key rule: the inner limits may depend on x, but the outer limits must be numbers.",
    "Example: the area of this triangle. The inner integral of one, d y, from zero to x, gives x. The outer integral of x from zero to one gives one half. That matches one half, times base, times height.",
    "Between two curves it works the same way. For the region between y equals x squared below and y equals square root of x above, the inner limits are x squared and square root of x.",
    "Pause and think: how do you find where the two curves meet? Set them equal. x squared equals the square root of x gives x equals zero and x equals one. Those are the outer limits.",
    "The area of this region: the integral from zero to one of square root of x minus x squared, which is two thirds minus one third, so one third.",
    "Summary. One: a double integral adds f times d A over a region; with f equals one, it gives the area. Two: compute it as an inner and an outer integral. Three: for a region between curves, draw a vertical strip: the inner limits are the bottom and top curves, and the outer limits are numbers.",
]


def split_at(text, phrase):
    i = text.find(phrase)
    if i < 0:
        raise ValueError(phrase)
    return text[:i].rstrip(), text[i:]


class DoubleIntegralRefresher(FlatScene):
    def construct(self):
        vo = VO["refresh"]
        self.start("16.4 — Double integrals (refresher)",
                   Tex(r"tiny rectangles $\cdot$ iterated integrals $\cdot$ vertical strips", font_size=30,
                       color=GRAY_B), checklist=CHECK_DI)

        # 0 — card
        c0 = card_left(self, Tex(r"line integral around $C$\\$\Longleftrightarrow$\\double integral over $R$",
                                 font_size=44, color=YELLOW))
        text = vo[0]
        with self.voiceover(text=text) as tr:
            self.play(Write(self.title_mob), run_time=1.2)
            self.play(Write(self.problem_mob), run_time=1.2)
            self.play(FadeIn(c0), run_time=0.6)
        self.rest()
        self.play(FadeOut(c0), run_time=0.4)

        # 1 — single vs double: bars and tiny rectangles
        self.chapter(1, "What is a double integral?")
        ax1 = Axes(x_range=[0, 4, 1], y_range=[0, 2, 1], x_length=4.4, y_length=2.0, tips=False,
                   axis_config={"stroke_color": GRAY_B}).move_to([-3.4, 2.0, 0])
        g1 = ax1.plot(lambda x: 1 + 0.5 * np.sin(1.5 * x), x_range=[0, 4], color=YELLOW)
        bars = ax1.get_riemann_rectangles(g1, x_range=[0.2, 3.8], dx=0.3, fill_opacity=0.5, color=YELLOW,
                                          stroke_width=1)
        lab1 = MathTex(r"\int f(x)\,dx", font_size=32).next_to(ax1, LEFT, buff=0.2)
        RC = np.array([-3.4, -1.7, 0])
        blob = Ellipse(width=4.6, height=2.6, color=C_BND, stroke_width=4).move_to(RC)
        blob_fill = blob.copy().set_stroke(width=0).set_fill(C_REG, 0.3)
        cells = VGroup()
        for i in np.arange(-2.2, 2.25, 0.4):
            for j in np.arange(-1.2, 1.25, 0.4):
                if (i / 2.3) ** 2 + (j / 1.3) ** 2 < 0.8:
                    val = 0.5 + 0.5 * np.sin(i) * np.cos(j)
                    cells.add(Square(0.36, stroke_width=1, stroke_color=WHITE,
                                     fill_color=interpolate_color(BLUE_E, YELLOW, val), fill_opacity=0.6)
                              .move_to(RC + np.array([i, j, 0])))
        lab2 = MathTex(r"\iint_R f\,dA", font_size=32).next_to(blob, LEFT, buff=0.15)
        n1 = MathTex(r"\iint_R f(x,y)\,dA\approx\sum f(x_k,y_k)\,\Delta x\,\Delta y", font_size=34)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Create(ax1), Create(g1), run_time=1.0)
            self.play(FadeIn(bars), FadeIn(lab1), run_time=0.8)
            self.sync(tr, text, "A double integral")
            self.play(FadeIn(blob_fill), Create(blob), FadeIn(lab2), run_time=0.8)
            self.sync(tr, text, "Cut the region")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01), run_time=1.5)
            self.nb_add(n1)
        self.rest()
        self.play(FadeOut(VGroup(ax1, g1, bars, lab1, blob, blob_fill, cells, lab2)), run_time=0.5)

        # 2 — volume under z = f; f = 1 gives the area
        base = Ellipse(width=4.6, height=1.3, stroke_color=C_BND, fill_color=C_REG, fill_opacity=0.35).move_to([-3.4, -1.9, 0])
        top = VMobject(stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.25)
        tp = [np.array([-3.4 + 2.3 * np.cos(t), 0.6 + 0.65 * np.sin(t) + 0.35 * np.sin(2 * t + 0.5), 0])
              for t in np.linspace(0, 2 * PI, 60)]
        top.set_points_smoothly(tp)
        sides = VGroup(DashedLine([-5.7, -1.9, 0], [-5.7, tp[30][1], 0], color=GRAY_B),
                       DashedLine([-1.1, -1.9, 0], [-1.1, tp[0][1], 0], color=GRAY_B))
        vol = Tex(r"volume under $z=f(x,y)$", font_size=30, color=YELLOW).move_to([-3.4, 2.2, 0])
        rl = MathTex("R", font_size=34, color=C_BND).move_to([-3.4, -1.9, 0])
        n2 = MathTex(r"\iint_R 1\,dA=\text{area of }R", font_size=36)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(base), FadeIn(rl), run_time=0.5)
            self.play(Create(sides), FadeIn(top), FadeIn(vol), run_time=1.0)
            self.sync(tr, text, "And if f equals one")
            self.nb_add(n2, gray=False)
            boxed(self, n2, color=YELLOW)
        self.rest()
        self.play(FadeOut(VGroup(base, top, sides, vol, rl)), run_time=0.5)

        # 3-5 — rectangle
        self.nb_clear()
        self.chapter(2, "Rectangles")
        ax, axl = left_axes([0, 1.2, 1], [0, 1.2, 1], 4.4)
        sq = Polygon(ax.c2p(0, 0), ax.c2p(1, 0), ax.c2p(1, 1), ax.c2p(0, 1), stroke_color=C_BND, stroke_width=4,
                     fill_color=C_REG, fill_opacity=0.3)
        n3 = MathTex(r"\int_0^1\!\!\int_0^1 (x+y)\,dy\,dx", font_size=38)
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.play(Create(ax), FadeIn(axl), run_time=0.8)
            self.play(FadeIn(sq), run_time=0.6)
            self.sync(tr, text, "Example")
            self.nb_add(n3)
        self.rest()
        xt = ValueTracker(0.6)
        st = strip(ax, xt, lambda x: 0, lambda x: 1)
        frz = Tex(r"$x$ fixed", font_size=28, color=C_STRIP).next_to(ax.c2p(0.6, 1), UP, buff=0.15)
        n4 = MathTex(r"\int_0^1(x+y)\,dy=\Big[xy+\tfrac{y^2}{2}\Big]_0^1=x+\tfrac12", font_size=34)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.play(FadeIn(st), FadeIn(frz), run_time=0.6)
            self.nb_add(n4)
        self.rest()
        n5 = MathTex(r"\int_0^1\big(x+\tfrac12\big)\,dx=\tfrac12+\tfrac12=1", font_size=36)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.play(FadeOut(frz), run_time=0.3)
            xt.set_value(0.05)
            self.play(xt.animate.set_value(0.95), run_time=2.0)
            self.nb_add(n5, buff=0.4)
            boxed(self, n5)
        self.rest()
        st.clear_updaters()
        self.play(FadeOut(VGroup(ax, axl, sq, st)), run_time=0.5)

        # 6-8 — triangle with vertical strips
        self.nb_clear()
        self.chapter(3, "Regions between curves")
        ax, axl = left_axes([0, 1.2, 1], [0, 1.2, 1], 4.4)
        bot, topf = (lambda x: 0.0), (lambda x: x)
        reg = region_between(ax, bot, topf, 0, 1)
        bnd = boundary_between(ax, bot, topf, 0, 1)
        lines = VGroup(MathTex("y=0", font_size=26).next_to(ax.c2p(0.15, 0), UP, buff=0.12),
                       MathTex("x=1", font_size=26).next_to(ax.c2p(1, 0.5), RIGHT, buff=0.12),
                       MathTex("y=x", font_size=26).next_to(ax.c2p(0.45, 0.5), UL, buff=0.05))
        xt = ValueTracker(0.1)
        st = strip(ax, xt, bot, topf)
        sl = strip_labels(ax, xt, bot, topf, r"\text{bottom: }y=0", r"\text{top: }y=x")
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.play(Create(ax), FadeIn(axl), run_time=0.6)
            self.play(FadeIn(reg), Create(bnd[0]), FadeIn(bnd[1]), FadeIn(lines), run_time=1.0)
            self.sync(tr, text, "Draw a vertical strip")
            self.check_step(1)
            self.play(FadeIn(st), run_time=0.4)
            self.play(xt.animate.set_value(0.6), run_time=1.2)
            self.sync(tr, text, "The strip starts")
            self.play(FadeIn(sl), run_time=0.6)
            self.play(xt.animate.set_value(0.9), run_time=1.5)
        self.rest()
        n7 = MathTex(r"\iint_R f\,dA=\int_0^1\!\!\int_0^{x} f\,dy\,dx", font_size=38)
        rule = Tex(r"inner limits may depend on $x$ $\cdot$ outer limits are numbers", font_size=28, color=YELLOW)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.nb_add(n7)
            self.sync(tr, text, "The key rule")
            self.nb_add(rule, gray=False)
            boxed(self, rule, color=YELLOW)
        self.rest()
        n8 = MathTex(r"\int_0^1\!\!\int_0^x 1\,dy\,dx=\int_0^1 x\,dx=\tfrac12\ \checkmark", font_size=36)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.nb_add(n8)
            self.sync(tr, text, "That matches")
            self.nb_add(MathTex(r"\tfrac12\cdot\text{base}\cdot\text{height}=\tfrac12\cdot1\cdot1", font_size=32,
                                color=GRAY_B), gray=False)
        self.rest()
        for m in sl:
            m.clear_updaters()
        st.clear_updaters()
        self.play(FadeOut(VGroup(ax, axl, reg, bnd, lines, st, sl)), run_time=0.5)

        # 9-11 — between y = x^2 and y = sqrt x
        self.nb_clear()
        ax, axl = left_axes([0, 1.2, 1], [0, 1.2, 1], 4.4)
        bot, topf = (lambda x: x * x), (lambda x: np.sqrt(max(x, 0)))
        reg = region_between(ax, bot, topf, 0, 1)
        bnd = boundary_between(ax, bot, topf, 0, 1)
        cl = VGroup(MathTex(r"y=x^2", font_size=28).next_to(ax.c2p(0.8, 0.64), DR, buff=0.05),
                    MathTex(r"y=\sqrt x", font_size=28).next_to(ax.c2p(0.3, np.sqrt(0.3)), UL, buff=0.05))
        xt = ValueTracker(0.15)
        st = strip(ax, xt, bot, topf)
        n9 = MathTex(r"\int_0^1\!\!\int_{x^2}^{\sqrt x} f\,dy\,dx", font_size=38)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.play(Create(ax), FadeIn(axl), run_time=0.6)
            self.play(FadeIn(reg), Create(bnd[0]), FadeIn(bnd[1]), FadeIn(cl), run_time=1.0)
            self.check_step(1)
            self.play(FadeIn(st), run_time=0.4)
            self.play(xt.animate.set_value(0.85), run_time=2.0)
            self.sync(tr, text, "the inner limits are")
            self.nb_add(n9)
        self.rest()
        p1, p2 = split_at(vo[10], "Set them equal")
        self.pause(p1, "How do you find where the curves meet?")
        meet = VGroup(Dot(ax.c2p(0, 0), color=YELLOW), Dot(ax.c2p(1, 1), color=YELLOW))
        n10 = MathTex(r"x^2=\sqrt x\ \Rightarrow\ x=0,\ x=1", font_size=36)
        with self.voiceover(text=p2) as tr:
            self.nb_add(n10)
            self.play(FadeIn(meet, scale=1.5), run_time=0.6)
        self.rest()
        n11 = MathTex(r"\text{area}=\int_0^1(\sqrt x-x^2)\,dx=\tfrac23-\tfrac13=\tfrac13", font_size=34)
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(n11, buff=0.4)
            boxed(self, n11)
        self.rest()
        st.clear_updaters()

        self.summary(vo[12],
                     [r"A double integral adds $f\,dA$ over $R$; with $f=1$ it gives the area.",
                      r"Compute it as an inner and an outer integral.",
                      r"Vertical strip: inner limits = bottom and top curve; outer limits are numbers."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
VO["curldiv"] = [
    "Section sixteen point four is about Green's theorem. Before the theorem itself, we need two new ideas that describe a vector field at a single point: how much it spins, and how much it spreads out. They are called the circulation density, or curl, and the flux density, or divergence.",
    "Imagine a thin layer of water flowing in the plane, with velocity field F equals M i plus N j. Put a tiny paddle wheel in the water, with its axis pointing straight up. Will it spin? And in which direction?",
    "To find out, take a tiny rectangle at the point x, y, with sides delta x and delta y. We compute the circulation around it, counterclockwise: the flow along each of the four edges.",
    "Bottom edge: the flow is M times delta x. The top edge is traversed to the left, so it gives minus M, at height y plus delta y, times delta x. Together, top and bottom give minus the change of M in the y direction: minus M y, times delta y, times delta x.",
    "Right edge: N times delta y. The left edge is traversed downward, so it gives minus N, at the left side, times delta y. Together: the change of N in the x direction, N x times delta x, times delta y.",
    "Adding everything: the circulation around the tiny rectangle is N x minus M y, times delta x delta y. Divide by the area, delta x delta y, and we get the circulation per unit area: N x minus M y.",
    "This is the circulation density of F, also called the k component of the curl. If it is positive, the paddle wheel spins counterclockwise. If it is negative, it spins clockwise. If it is zero, it does not spin.",
    "Let's test this on four fields from the book. First, uniform expansion: F equals c x i plus c y j. N x minus M y is zero minus zero, which is zero. No spin.",
    "Second, uniform rotation: minus c y i plus c x j. N x is c, and M y is minus c, so the curl is two c. The fluid spins at every point, counterclockwise if c is positive.",
    "Third, a shear flow: F equals y i. Pause and think: will a paddle wheel spin here, even though the flow lines are straight?",
    "N is zero and M is y, so the curl is zero minus one, which is minus one. Yes, it spins clockwise! The water above moves faster to the right than the water below, so the wheel is pushed around. Straight flow lines can still have spin.",
    "Fourth, the whirlpool field: minus y i plus x j, divided by x squared plus y squared. Surprisingly, its curl is zero everywhere, except at the origin, where the field is not defined. All the spin is concentrated in the centre. That is why its circulation around the unit circle was two pi.",
    "Now the second question: does fluid flow out of the tiny rectangle, or into it? We compute the flux across the four edges, using the outward normal on each side.",
    "Right and left edges together give M x times delta x delta y. Top and bottom together give N y times delta x delta y.",
    "So the flux per unit area is M x plus N y. This is the flux density, or divergence of F, written div F. Positive divergence means a source, where the fluid spreads out. Negative divergence means a sink, where the fluid is compressed.",
    "For the four fields: uniform expansion has divergence two c, a source everywhere. Rotation, shear and the whirlpool all have divergence zero: they neither expand nor compress. A flow with zero divergence everywhere is called incompressible, like water.",
    "In engineering, divergence appears in the continuity equation for fluids, and curl describes vortices, for example in the air flow behind a fan or a propeller. In electromagnetism, the curl of the magnetic field is linked to the current density.",
    "Summary. One: the curl, N x minus M y, measures spin per unit area; positive means counterclockwise. Two: the divergence, M x plus N y, measures outflow per unit area; positive means a source. Three: note the difference: the curl subtracts the cross derivatives, and the divergence adds the straight derivatives.",
]

PANEL_C = [np.array([-5.1, 1.55, 0]), np.array([-1.7, 1.55, 0]), np.array([-5.1, -1.95, 0]), np.array([-1.7, -1.95, 0])]
FIELDS4 = [(r"(a)\ x\,\mathbf i+y\,\mathbf j", lambda x, y: (x, y)),
           (r"(b)\ -y\,\mathbf i+x\,\mathbf j", lambda x, y: (-y, x)),
           (r"(c)\ y\,\mathbf i", lambda x, y: (y, 0.0)),
           (r"(d)\ \tfrac{-y\,\mathbf i+x\,\mathbf j}{x^2+y^2}",
            lambda x, y: (-y / max(x * x + y * y, 0.05), x / max(x * x + y * y, 0.05)))]


def make_panel(k, hole=False):
    c = PANEL_C[k]
    frame = RoundedRectangle(corner_radius=0.12, width=3.2, height=3.2, stroke_color=GRAY, stroke_width=1.5).move_to(c)
    title = MathTex(FIELDS4[k][0], font_size=26).next_to(frame, UP, buff=0.05).align_to(frame, LEFT).shift(RIGHT * 0.1)
    title.move_to(frame.get_top() + DOWN * 0.25)
    title.add_background_rectangle(opacity=0.85, buff=0.04)
    fld = mini_field(c + DOWN * 0.15, FIELDS4[k][1], half=1.3, n=5, s=0.42)
    g = VGroup(frame, fld, title)
    if hole:
        g.add(Circle(radius=0.12, fill_color=BLACK, fill_opacity=1, stroke_color=C_WRONG, stroke_width=3)
              .move_to(c + DOWN * 0.15))
    return g


class CurlDivergence(FlatScene):
    def construct(self):
        vo = VO["curldiv"]
        self.start("16.4 — Curl & divergence",
                   Tex(r"spin per area $\cdot$ outflow per area", font_size=30, color=GRAY_B))

        # 0 — two icons
        w0 = paddle(0.6).move_to([-4.9, 0.4, 0])
        src = VGroup(Dot([-1.9, 0.4, 0], radius=0.1, color=C_DIV),
                     *[Arrow([-1.9, 0.4, 0] + 0.25 * np.array([np.cos(a), np.sin(a), 0]),
                             [-1.9, 0.4, 0] + 0.95 * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=C_DIV,
                             stroke_width=3) for a in np.linspace(0, 2 * PI, 8, endpoint=False)])
        t0 = VGroup(Tex(r"spin $\to$ curl", font_size=32, color=C_CURL).next_to(w0, DOWN, buff=0.5),
                    Tex(r"spreading $\to$ divergence", font_size=32, color=C_DIV).next_to(src, DOWN, buff=0.35))
        text = vo[0]
        with self.voiceover(text=text) as tr:
            self.play(Write(self.title_mob), run_time=1.0)
            self.play(Write(self.problem_mob), run_time=1.0)
            self.sync(tr, text, "how much it spins")
            spin(w0, 1.2)
            self.play(FadeIn(w0), FadeIn(t0[0]), run_time=0.6)
            self.sync(tr, text, "how much it spreads")
            self.play(FadeIn(src), FadeIn(t0[1]), run_time=0.6)
            self.wait(tr.get_remaining_duration())
        w0.clear_updaters()
        self.play(FadeOut(VGroup(w0, src, t0)), run_time=0.4)

        # 1 — stream lines + paddle wheel
        self.chapter(1, "Spin: the paddle wheel")
        OC = np.array([-3.4, -0.2, 0])

        def flow(p):
            x, y = p[0] - OC[0], p[1] - OC[1]
            return np.array([0.9 + 0.3 * y, 0.12 * x, 0.0])
        sl = StreamLines(flow, x_range=[OC[0] - 3.3, OC[0] + 3.3, 0.45], y_range=[-3.4, 3.4, 0.45], stroke_width=1.5,
                         max_anchors_per_line=20, padding=0.3, virtual_time=3, colors=[BLUE_E, BLUE_C, BLUE_A])
        w1 = paddle(0.45).move_to(OC)
        nb1 = MathTex(r"\mathbf F=M\,\mathbf i+N\,\mathbf j", font_size=36)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.add(sl)
            sl.start_animation(warm_up=False, flow_speed=1.0, time_width=0.5)
            self.nb_add(nb1)
            self.sync(tr, text, "Put a tiny paddle wheel")
            spin(w1, -0.6)
            self.play(FadeIn(w1), run_time=0.6)
            self.wait(tr.get_remaining_duration())
        self.play(sl.end_animation(), run_time=1.0)
        self.remove(sl)
        w1.clear_updaters()
        self.play(FadeOut(w1), run_time=0.3)

        # 2 — the tiny rectangle
        x0, y0, W, H = -5.0, -1.6, 3.2, 2.4
        P00, P10, P11, P01 = [np.array([x0 + a * W, y0 + b * H, 0]) for a, b in [(0, 0), (1, 0), (1, 1), (0, 1)]]
        rect = Polygon(P00, P10, P11, P01, stroke_color=WHITE, stroke_width=2, fill_color=C_REG, fill_opacity=0.15)
        edges = VGroup(*[Arrow(a, b, buff=0.25, color=C_CURL, stroke_width=5, max_tip_length_to_length_ratio=0.12)
                         for a, b in [(P00, P10), (P10, P11), (P11, P01), (P01, P00)]])
        labs = VGroup(MathTex("(x,y)", font_size=28).next_to(P00, DL, buff=0.05),
                      MathTex(r"\Delta x", font_size=30).next_to(rect, DOWN, buff=0.35),
                      MathTex(r"\Delta y", font_size=30).next_to(rect, RIGHT, buff=0.35))
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(Create(rect), FadeIn(labs), run_time=1.0)
            self.sync(tr, text, "We compute the circulation")
            self.play(LaggedStart(*[GrowArrow(e) for e in edges], lag_ratio=0.25), run_time=1.5)
        self.rest()

        # 3-5 — the four edges
        n3 = MathTex(r"M(x,y)\,\Delta x,\ \ -M(x,y+\Delta y)\,\Delta x\ \Rightarrow\ -\frac{\partial M}{\partial y}\Delta y\,\Delta x",
                     font_size=30)
        n4 = MathTex(r"N(x+\Delta x,y)\,\Delta y,\ \ -N(x,y)\,\Delta y\ \Rightarrow\ \frac{\partial N}{\partial x}\Delta x\,\Delta y",
                     font_size=30)
        n5 = MathTex(r"\text{circulation}\approx\Big(\frac{\partial N}{\partial x}-\frac{\partial M}{\partial y}\Big)\Delta x\Delta y"
                     r"\ \Rightarrow\ \frac{\text{circulation}}{\text{area}}\to\frac{\partial N}{\partial x}-\frac{\partial M}{\partial y}",
                     font_size=30)
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.play(Indicate(edges[0]), run_time=0.6)
            self.sync(tr, text, "The top edge")
            self.play(Indicate(edges[2]), run_time=0.6)
            self.sync(tr, text, "Together, top and bottom")
            self.nb_add(n3)
        self.rest()
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.play(Indicate(edges[1]), run_time=0.6)
            self.sync(tr, text, "The left edge")
            self.play(Indicate(edges[3]), run_time=0.6)
            self.sync(tr, text, "Together")
            self.nb_add(n4)
        self.rest()
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.nb_add(n5, gray=False)
        self.rest()

        # 6 — curl box + three wheels
        n6 = MathTex(r"(\text{curl}\,\mathbf F)\cdot\mathbf k=\frac{\partial N}{\partial x}-\frac{\partial M}{\partial y}",
                     font_size=38, color=C_CURL)
        ws = VGroup(*[paddle(0.4).move_to([x, 2.2, 0]) for x in (-5.4, -3.4, -1.4)])
        wl = VGroup(*[Tex(s, font_size=26, color=c).next_to(ws[i], DOWN, buff=0.25) for i, (s, c) in
                      enumerate([(r"$>0$: CCW", C_ANSWER), (r"$<0$: CW", C_WRONG), (r"$=0$: still", GRAY_B)])])
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_clear()
            self.nb_add(n6, buff=0.4, gray=False)
            boxed(self, n6, color=C_CURL)
            self.play(FadeOut(VGroup(rect, edges, labs)), run_time=0.4)
            self.sync(tr, text, "If it is positive")
            spin(ws[0], 1.5)
            self.play(FadeIn(ws[0]), FadeIn(wl[0]), run_time=0.5)
            self.sync(tr, text, "If it is negative")
            spin(ws[1], -1.5)
            self.play(FadeIn(ws[1]), FadeIn(wl[1]), run_time=0.5)
            self.sync(tr, text, "If it is zero")
            self.play(FadeIn(ws[2]), FadeIn(wl[2]), run_time=0.5)
            self.wait(tr.get_remaining_duration())
        for w in ws:
            w.clear_updaters()
        self.play(FadeOut(VGroup(ws, wl)), run_time=0.4)

        # 7-11 — four example fields
        self.chapter(2, "Four example fields")
        panels = [make_panel(k, hole=(k == 3)) for k in range(4)]
        wheels = [paddle(0.3).move_to(PANEL_C[k] + DOWN * 0.15) for k in range(4)]
        curl_t = [MathTex(s, font_size=30, color=C_CURL) for s in
                  [r"\text{curl}=0", r"\text{curl}=2c", r"\text{curl}=0-1=-1", r"\text{curl}=0\ (\text{except }O)"]]
        for k, t in enumerate(curl_t):
            t.next_to(panels[k][0], DOWN, buff=0.05).shift(UP * 0.4)
            t.add_background_rectangle(opacity=1.0, buff=0.04)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(panels[0]), run_time=0.8)
            self.sync(tr, text, "N x minus M y")
            self.play(FadeIn(wheels[0]), FadeIn(curl_t[0]), run_time=0.6)
            self.nb_add(MathTex(r"(a)\ N_x-M_y=0-0=0", font_size=32))
        self.rest()
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(panels[1]), run_time=0.8)
            self.sync(tr, text, "N x is c")
            spin(wheels[1], 1.2)
            self.play(FadeIn(wheels[1]), FadeIn(curl_t[1]), run_time=0.6)
            self.nb_add(MathTex(r"(b)\ N_x-M_y=c-(-c)=2c", font_size=32))
        self.rest()
        self.pause(vo[9], r"Shear flow $y\,\mathbf i$: will the paddle wheel spin?",
                   before=lambda tr: self.play(FadeIn(panels[2]), run_time=0.8))
        fast = VGroup(Arrow(PANEL_C[2] + np.array([-0.45, 0.55, 0]), PANEL_C[2] + np.array([0.45, 0.55, 0]), buff=0,
                            color=YELLOW, stroke_width=4),
                      Arrow(PANEL_C[2] + np.array([0.15, -0.85, 0]), PANEL_C[2] + np.array([-0.15, -0.85, 0]), buff=0,
                            color=YELLOW, stroke_width=4))
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.nb_add(MathTex(r"(c)\ N_x-M_y=0-1=-1", font_size=32))
            self.sync(tr, text, "Yes, it spins clockwise")
            spin(wheels[2], -1.2)
            self.play(FadeIn(wheels[2]), FadeIn(curl_t[2]), run_time=0.6)
            self.sync(tr, text, "The water above")
            self.play(GrowArrow(fast[0]), GrowArrow(fast[1]), run_time=0.8)
        self.rest()
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(panels[3]), run_time=0.8)
            self.sync(tr, text, "Surprisingly")
            self.play(FadeIn(curl_t[3]), run_time=0.6)
            self.sync(tr, text, "That is why")
            self.nb_add(MathTex(r"(d)\ \oint_{\text{unit circle}}=2\pi\ \ (16.2/16.3)", font_size=32), gray=False)
        self.rest()
        for w in wheels:
            w.clear_updaters()
        self.play(FadeOut(VGroup(*panels, *wheels, *curl_t, fast)), run_time=0.5)

        # 12-14 — divergence
        self.nb_clear()
        self.chapter(3, "Spreading out: divergence")
        nrm = VGroup(*[Arrow(m, m + 0.85 * d, buff=0, color=C_DIV, stroke_width=5) for m, d in
                       [((P00 + P10) / 2, DOWN), ((P10 + P11) / 2, RIGHT), ((P11 + P01) / 2, UP), ((P01 + P00) / 2, LEFT)]])
        nlab = MathTex(r"\mathbf n", font_size=32, color=C_DIV).next_to(nrm[1].get_end(), UP, buff=0.05)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.play(Create(rect), FadeIn(labs[0]), run_time=0.8)
            self.sync(tr, text, "using the outward normal")
            self.play(LaggedStart(*[GrowArrow(a) for a in nrm], lag_ratio=0.2), FadeIn(nlab), run_time=1.2)
        self.rest()
        n13 = MathTex(r"\text{right+left}\approx\frac{\partial M}{\partial x}\Delta x\Delta y,\quad "
                      r"\text{top+bottom}\approx\frac{\partial N}{\partial y}\Delta x\Delta y", font_size=30)
        text = vo[13]
        with self.voiceover(text=text) as tr:
            self.play(Indicate(nrm[1]), Indicate(nrm[3]), run_time=0.7)
            self.sync(tr, text, "Top and bottom")
            self.play(Indicate(nrm[0]), Indicate(nrm[2]), run_time=0.7)
            self.nb_add(n13)
        self.rest()
        n14 = MathTex(r"\text{div}\,\mathbf F=\frac{\partial M}{\partial x}+\frac{\partial N}{\partial y}", font_size=40,
                      color=C_DIV)

        def burst(c, inward=False):
            g = VGroup(Dot(c, radius=0.09, color=C_DIV))
            for a in np.linspace(0, 2 * PI, 8, endpoint=False):
                u = np.array([np.cos(a), np.sin(a), 0])
                p, q = c + 0.25 * u, c + 0.85 * u
                g.add(Arrow(q, p, buff=0, color=C_DIV, stroke_width=3) if inward else
                      Arrow(p, q, buff=0, color=C_DIV, stroke_width=3))
            return g
        srcs = VGroup(burst(np.array([-4.8, 0.2, 0])), burst(np.array([-2.0, 0.2, 0]), inward=True))
        sl2 = VGroup(Tex(r"source: div $>0$", font_size=28, color=C_DIV).next_to(srcs[0], DOWN, buff=0.3),
                     Tex(r"sink: div $<0$", font_size=28, color=C_DIV).next_to(srcs[1], DOWN, buff=0.3))
        text = vo[14]
        with self.voiceover(text=text) as tr:
            self.nb_add(n14, buff=0.4, gray=False)
            boxed(self, n14, color=C_DIV)
            self.play(FadeOut(VGroup(rect, labs[0], nrm, nlab)), run_time=0.4)
            self.sync(tr, text, "Positive divergence")
            self.play(FadeIn(srcs[0]), FadeIn(sl2[0]), run_time=0.6)
            self.sync(tr, text, "Negative divergence")
            self.play(FadeIn(srcs[1]), FadeIn(sl2[1]), run_time=0.6)
        self.rest()
        self.play(FadeOut(VGroup(srcs, sl2)), run_time=0.4)

        # 15 — divergence of the four fields
        panels = [make_panel(k, hole=(k == 3)) for k in range(4)]
        div_t = [MathTex(s, font_size=32, color=PURPLE_A) for s in [r"\text{div}=2c", r"\text{div}=0", r"\text{div}=0",
                                                                 r"\text{div}=0"]]
        for k, t in enumerate(div_t):
            t.next_to(panels[k][0], DOWN, buff=0.05).shift(UP * 0.4)
            t.add_background_rectangle(opacity=1.0, buff=0.04)
        inc = Tex(r"div $=0$ $\to$ incompressible", font_size=30, color=YELLOW)
        text = vo[15]
        with self.voiceover(text=text) as tr:
            self.play(*[FadeIn(p) for p in panels], run_time=0.8)
            self.play(FadeIn(div_t[0]), run_time=0.5)
            self.sync(tr, text, "Rotation, shear")
            self.play(*[FadeIn(t) for t in div_t[1:]], run_time=0.6)
            self.sync(tr, text, "A flow with zero divergence")
            self.nb_add(inc, gray=False)
        self.rest()
        self.play(FadeOut(VGroup(*panels, *div_t)), run_time=0.4)

        # 16 — engineering card
        eh = Tex("Engineering", font_size=40, color=YELLOW)
        e1 = VGroup(MathTex(r"\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf v)=0", font_size=36, color=C_DIV),
                    Tex("continuity equation (fluids)", font_size=26, color=GRAY_B)).arrange(DOWN, buff=0.1)
        e2 = Tex(r"curl: vortices behind a fan / propeller", font_size=30, color=C_CURL)
        e3 = VGroup(MathTex(r"\nabla\times\mathbf B=\mu_0\mathbf J", font_size=36, color=C_CURL),
                    Tex("magnetic field and current density", font_size=26, color=GRAY_B)).arrange(DOWN, buff=0.1)
        card = card_left(self, VGroup(eh, e1, e2, e3).arrange(DOWN, buff=0.4))
        text = vo[16]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(card[0]), FadeIn(eh), run_time=0.5)
            self.play(FadeIn(e1), run_time=0.6)
            self.sync(tr, text, "and curl describes")
            self.play(FadeIn(e2), run_time=0.6)
            self.sync(tr, text, "In electromagnetism")
            self.play(FadeIn(e3), run_time=0.6)
        self.rest()

        self.summary(vo[17],
                     [r"Curl $N_x-M_y$: spin per unit area; positive $=$ counterclockwise.",
                      r"Divergence $M_x+N_y$: outflow per unit area; positive $=$ source.",
                      r"Curl: $-$, cross derivatives $\quad$ div: $+$, straight derivatives."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
VO["green"] = [
    "Now the main result of this section: Green's theorem. It connects what happens on the boundary of a region with what happens inside. And it often turns a hard line integral into an easy double integral.",
    "First, a convention. A closed curve can be traversed in two directions. Counterclockwise is called positive: as you walk along the curve, the region is always on your left. Green's theorem always uses this direction.",
    "Cover the region with many tiny rectangles. For each one, the circulation is about the curl times its area. Now add up the circulations of all the rectangles.",
    "Look at an inner edge shared by two neighbours. One rectangle traverses it upward, the other downward. These contributions cancel. Only the outer edges survive, and together they form the boundary curve C.",
    "So the circulation around C equals the sum of the curl times the area, over all the tiny rectangles. In the limit, that sum becomes a double integral.",
    "This is Green's theorem in circulation form, also called tangential form: the counterclockwise circulation around C, the integral of M d x plus N d y, equals the double integral over R of N x minus M y.",
    "The same reasoning with flux gives the second form, the flux form, or normal form: the outward flux across C, the integral of M d y minus N d x, equals the double integral over R of M x plus N y.",
    "Read it like this. The left side is circulation or flux, measured on the boundary. The right side is the total circulation density or flux density, inside. Whatever spins or spreads out inside, shows up on the boundary.",
    "In section sixteen point two, we computed the circulation and flux of F equals x minus y, i, plus x, j, around the unit circle. We found two pi and pi, after quite some work with parametrisations.",
    "With Green's theorem: the curl is N x minus M y, which is one minus minus one, which is two. The double integral of two over the unit disk is two times its area, pi. That gives two pi. Correct.",
    "The divergence is M x plus N y, which is one plus zero, which is one. The double integral of one over the disk is its area, pi. Also correct, and no parametrisation needed.",
    "Pause and think: when is Green's theorem useful, and when is it not?",
    "Use it when the curve is closed, the region inside is simple, and the curl or divergence is easy to integrate. It is especially useful when the curve consists of several pieces, like a triangle or a square: one double integral replaces three or four line integrals. Do not use it for curves that are not closed. And check that M and N are smooth everywhere inside the region.",
    "A beautiful application. Choose M equals minus y over two, and N equals x over two. Then the curl is one half plus one half, which is one. The double integral of one is the area. So the area of R equals one half times the integral around C of x d y minus y d x.",
    "So you can find an area by walking around the boundary. This is exactly how a planimeter works: a mechanical instrument that measures the area of a shape on a map, by tracing its outline.",
    "Summary. One: Green's theorem says that the circulation around C equals the double integral of the curl, and the outward flux across C equals the double integral of the divergence. Two: C must be closed and simple, and traversed counterclockwise, with the region on the left. Three: with M equals minus y over two and N equals x over two, it gives an area formula.",
]


def blob_point(t, c=np.array([-3.4, -0.2, 0]), s=1.0):
    r = 2.0 + 0.35 * np.sin(3 * t) + 0.2 * np.cos(2 * t)
    return c + s * np.array([1.25 * r * np.cos(t), 0.95 * r * np.sin(t), 0])


def blob(c=np.array([-3.4, -0.2, 0]), s=1.0, fill=True):
    curve = ParametricFunction(lambda t: blob_point(t, c, s), t_range=[0, 2 * PI], color=C_BND, stroke_width=5)
    g = VGroup()
    if fill:
        g.add(curve.copy().set_stroke(width=0).set_fill(C_REG, 0.3))
    g.add(curve)
    g.add(VGroup(*[tip_at(lambda t: blob_point(t, c, s), t0) for t0 in (0.4, 2.5, 4.6)]))
    return g


class GreensTheorem(FlatScene):
    def construct(self):
        vo = VO["green"]
        self.start("16.4 — Green's theorem",
                   Tex(r"boundary $C$ $\Longleftrightarrow$ region $R$ inside", font_size=30, color=GRAY_B))

        # 0 — sketch boundary vs inside
        b0 = blob(s=0.9)
        cl = MathTex("C", font_size=40, color=C_BND).move_to(blob_point(0.9, s=0.9) + np.array([0.4, 0.3, 0]))
        rl = MathTex("R", font_size=44).move_to([-3.4, -0.2, 0])
        text = vo[0]
        with self.voiceover(text=text) as tr:
            self.play(Write(self.title_mob), run_time=1.0)
            self.play(Write(self.problem_mob), run_time=1.0)
            self.sync(tr, text, "It connects")
            self.play(FadeIn(b0[0]), Create(b0[1]), FadeIn(b0[2]), FadeIn(cl), FadeIn(rl), run_time=1.2)
        self.rest()
        self.play(FadeOut(VGroup(b0, cl, rl)), run_time=0.4)

        # 1 — orientation: walker with the region on the left
        self.chapter(1, "Orientation")
        b1 = blob()
        tt = ValueTracker(0.0)
        walker = always_redraw(lambda: VGroup(
            Dot(blob_point(tt.get_value()), radius=0.12, color=YELLOW),
            Arrow(blob_point(tt.get_value()), blob_point(tt.get_value() + 0.35), buff=0, color=YELLOW, stroke_width=4,
                  max_tip_length_to_length_ratio=0.4)))
        lft = Tex(r"region on the left", font_size=28, color=C_REG)
        lft.add_updater(lambda m: m.move_to(blob_point(tt.get_value(), s=0.62)))
        pos = Tex(r"positive orientation: region on the left", font_size=30, color=YELLOW).move_to([-3.4, 3.3, 0])
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(b1[0]), Create(b1[1]), run_time=1.0)
            self.sync(tr, text, "Counterclockwise is called positive")
            self.play(FadeIn(b1[2]), FadeIn(walker), FadeIn(lft), run_time=0.5)
            self.play(tt.animate.set_value(2 * PI), run_time=max(tr.get_remaining_duration() - 0.6, 2.0), rate_func=linear)
            self.play(FadeIn(pos), run_time=0.5)
        self.rest()
        walker.clear_updaters()
        lft.clear_updaters()
        self.play(FadeOut(VGroup(b1, walker, lft, pos)), run_time=0.4)

        # 2-4 — tiny rectangles, inner edges cancel
        self.chapter(2, "From tiny rectangles to the whole region")
        s = 0.95
        mask = [(i, j) for i in range(6) for j in range(5) if not ((i, j) in [(0, 0), (5, 0), (0, 4), (5, 4), (4, 4)])]
        org = np.array([-3.4 - 3 * s, -0.2 - 2.5 * s, 0])

        def corner(i, j):
            return org + s * np.array([i, j, 0])
        cells = VGroup()
        circs = VGroup()
        for i, j in mask:
            c = (corner(i, j) + corner(i + 1, j + 1)) / 2
            cells.add(Square(s, stroke_width=1.5, stroke_color=WHITE, fill_color=C_REG, fill_opacity=0.25).move_to(c))
            a = Arc(radius=0.22, start_angle=-PI / 2, angle=1.6 * PI, color=C_CURL, stroke_width=3).move_arc_center_to(c)
            a.add_tip(tip_length=0.12)
            circs.add(a)
        cellset = set(mask)
        inner, outer = VGroup(), VGroup()
        for i, j in mask:
            for (a, b), nb in [((corner(i, j), corner(i + 1, j)), (i, j - 1)), ((corner(i + 1, j), corner(i + 1, j + 1)), (i + 1, j)),
                               ((corner(i + 1, j + 1), corner(i, j + 1)), (i, j + 1)), ((corner(i, j + 1), corner(i, j)), (i - 1, j))]:
                if nb in cellset:
                    if (i, j) < nb:
                        inner.add(Line(a, b, color=WHITE, stroke_width=2))
                else:
                    outer.add(Line(a, b, color=C_BND, stroke_width=6))
        n2 = MathTex(r"\text{circulation of one rectangle}\approx(\text{curl})\,\Delta A", font_size=32)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.03), run_time=1.2)
            self.sync(tr, text, "For each one")
            self.play(LaggedStart(*[Create(a) for a in circs], lag_ratio=0.03), run_time=1.2)
            self.nb_add(n2)
        self.rest()
        # two neighbours: (2,2) and (3,2) share the vertical edge x = 3
        e_a, e_b = corner(3, 2), corner(3, 3)
        up = Arrow(e_a + LEFT * 0.12, e_b + LEFT * 0.12, buff=0.12, color=C_CURL, stroke_width=5)
        dn = Arrow(e_b + RIGHT * 0.12, e_a + RIGHT * 0.12, buff=0.12, color=C_CURL, stroke_width=5)
        hl = VGroup(cells[mask.index((2, 2))], cells[mask.index((3, 2))])
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.play(circs.animate.set_opacity(0.25), hl.animate.set_fill(YELLOW, 0.35), run_time=0.6)
            self.sync(tr, text, "One rectangle traverses")
            self.play(GrowArrow(up), GrowArrow(dn), run_time=0.8)
            self.sync(tr, text, "These contributions cancel")
            self.play(FadeOut(up), FadeOut(dn), run_time=0.8)
            self.sync(tr, text, "Only the outer edges")
            self.play(FadeIn(inner), run_time=0.4)
            self.play(FadeOut(inner), FadeOut(circs), hl.animate.set_fill(C_REG, 0.25), run_time=1.2)
            self.play(Create(outer), run_time=1.2)
            cl = MathTex("C", font_size=40, color=C_BND).next_to(corner(6, 2), RIGHT, buff=0.15)
            self.play(FadeIn(cl), run_time=0.4)
        self.rest()
        n4 = MathTex(r"\oint_C=\sum(\text{curl})\,\Delta A\ \to\ \iint_R(\text{curl})\,dA", font_size=36)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.nb_add(n4, gray=False)
        self.rest()
        self.play(FadeOut(VGroup(cells, outer, cl)), run_time=0.4)

        # 5-7 — the two forms
        self.nb_clear()
        g5 = MathTex(r"\oint_C\mathbf F\cdot\mathbf T\,ds=\oint_C M\,dx+N\,dy=\iint_R\Big(\frac{\partial N}{\partial x}"
                     r"-\frac{\partial M}{\partial y}\Big)dx\,dy", font_size=32, color=C_CURL)
        g6 = MathTex(r"\oint_C\mathbf F\cdot\mathbf n\,ds=\oint_C M\,dy-N\,dx=\iint_R\Big(\frac{\partial M}{\partial x}"
                     r"+\frac{\partial N}{\partial y}\Big)dx\,dy", font_size=32, color=C_DIV)
        h5 = Tex("circulation-curl (tangential) form", font_size=28, color=C_CURL)
        h6 = Tex("flux-divergence (normal) form", font_size=28, color=C_DIV)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.nb_add(h5, gray=False)
            self.nb_add(g5, gray=False, buff=0.4)
            boxed(self, g5, color=C_CURL)
        self.rest()
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_add(h6, gray=False)
            self.nb_add(g6, gray=False, buff=0.4)
            boxed(self, g6, color=C_DIV)
        self.rest()
        L1 = MathTex(r"\oint_C M\,dx+N\,dy", "=", r"\iint_R(N_x-M_y)\,dA", font_size=38, color=C_CURL)
        L2 = MathTex(r"\oint_C M\,dy-N\,dx", "=", r"\iint_R(M_x+N_y)\,dA", font_size=38, color=C_DIV)
        VGroup(L1, L2).arrange(DOWN, buff=1.2).move_to([-3.4, 0.0, 0])
        lb = VGroup(Tex("boundary", font_size=28, color=GRAY_B).next_to(L1[0], UP, buff=0.25),
                    Tex("inside", font_size=28, color=GRAY_B).next_to(L1[2], UP, buff=0.25),
                    Tex("boundary", font_size=28, color=GRAY_B).next_to(L2[0], DOWN, buff=0.25),
                    Tex("inside", font_size=28, color=GRAY_B).next_to(L2[2], DOWN, buff=0.25))
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(L1), FadeIn(L2), run_time=0.8)
            self.sync(tr, text, "The left side")
            self.play(FadeIn(lb[0]), FadeIn(lb[2]), Indicate(L1[0]), Indicate(L2[0]), run_time=0.8)
            self.sync(tr, text, "The right side")
            self.play(FadeIn(lb[1]), FadeIn(lb[3]), Indicate(L1[2]), Indicate(L2[2]), run_time=0.8)
        self.rest()
        self.play(FadeOut(VGroup(L1, L2, lb)), run_time=0.4)

        # 8-10 — the old example on the unit circle
        self.nb_clear()
        self.chapter(3, "Check with an old example")
        CC, U = np.array([-3.4, -0.4, 0]), 2.1
        disk = Circle(radius=U, stroke_width=0, fill_color=C_REG, fill_opacity=0.3).move_to(CC)
        ring = Circle(radius=U, color=C_BND, stroke_width=5).move_to(CC)
        rt = VGroup(*[tip_at(lambda t: CC + U * np.array([np.cos(t), np.sin(t), 0]), t0) for t0 in (PI / 4, 5 * PI / 4)])
        arrs = VGroup()
        for x in np.arange(-1.2, 1.25, 0.6):
            for y in np.arange(-1.2, 1.25, 0.6):
                v = np.array([x - y, x, 0])
                if np.linalg.norm(v) < 1e-6:
                    continue
                p = CC + U * np.array([x, y, 0])
                arrs.add(Arrow(p, p + 0.45 * v, buff=0, color=GRAY_B, stroke_width=2.5, max_tip_length_to_length_ratio=0.3))
        badge = Tex(r"16.2: circulation $2\pi$, flux $\pi$", font_size=30, color=YELLOW).move_to([-3.4, 3.1, 0])
        f8 = MathTex(r"\mathbf F=(x-y)\,\mathbf i+x\,\mathbf j,\ \ C:\ \text{unit circle}", font_size=34)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(disk), Create(ring), FadeIn(rt), FadeIn(arrs), run_time=1.0)
            self.nb_add(f8)
            self.sync(tr, text, "We found two pi")
            self.play(FadeIn(badge), run_time=0.5)
        self.rest()
        f9 = MathTex(r"\frac{\partial N}{\partial x}-\frac{\partial M}{\partial y}=1-(-1)=2,\ \ \iint_R2\,dA=2\cdot\pi=2\pi\ \checkmark",
                     font_size=30, color=C_CURL)
        f10 = MathTex(r"\frac{\partial M}{\partial x}+\frac{\partial N}{\partial y}=1+0=1,\ \ \iint_R1\,dA=\pi\ \checkmark",
                      font_size=30, color=C_DIV)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.nb_add(f9, gray=False)
            self.sync(tr, text, "That gives two pi")
            self.play(Indicate(badge), run_time=0.6)
        self.rest()
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.nb_add(f10, gray=False)
            self.sync(tr, text, "Also correct")
            self.play(Indicate(badge), run_time=0.6)
        self.rest()
        self.play(FadeOut(VGroup(disk, ring, rt, arrs, badge)), run_time=0.4)

        # 11-12 — when to use it
        self.pause(vo[11], r"When is Green's theorem useful — and when not?")
        use = VGroup(Tex("use it", font_size=34, color=C_ANSWER),
                     Tex(r"closed curve", font_size=28), Tex(r"several pieces\\(triangle, square)", font_size=28),
                     Tex(r"easy curl / div", font_size=28)).arrange(DOWN, buff=0.3)
        dont = VGroup(Tex("don't", font_size=34, color=C_WRONG),
                      Tex(r"curve not closed", font_size=28), Tex(r"$M, N$ not smooth\\inside $R$ (hole!)", font_size=28)
                      ).arrange(DOWN, buff=0.3)
        cols = VGroup(use, dont).arrange(RIGHT, buff=1.0, aligned_edge=UP)
        card = card_left(self, cols)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(card[0]), FadeIn(use[0]), FadeIn(dont[0]), run_time=0.5)
            for m, ph in [(use[1], "Use it when"), (use[3], "and the curl"), (use[2], "It is especially useful"),
                          (dont[1], "Do not use it"), (dont[2], "And check that")]:
                self.sync(tr, text, ph)
                self.play(FadeIn(m), run_time=0.4)
        self.rest()
        self.play(FadeOut(card), run_time=0.4)

        # 13 — area formula
        self.nb_clear()
        self.chapter(4, "Area with Green's theorem")
        a1 = MathTex(r"M=-\tfrac y2,\ N=\tfrac x2\ \Rightarrow\ \frac{\partial N}{\partial x}-\frac{\partial M}{\partial y}"
                     r"=\tfrac12+\tfrac12=1", font_size=34)
        a2 = MathTex(r"\text{Area of }R=\tfrac12\oint_C x\,dy-y\,dx", font_size=40)
        text = vo[13]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Choose M equals")
            self.nb_add(a1)
            self.sync(tr, text, "So the area of R")
            self.nb_add(a2, buff=0.45, gray=False)
            boxed(self, a2, color=YELLOW)
        self.rest()

        # 14 — planimeter
        b14 = blob(c=np.array([-2.6, 0.2, 0]), s=0.7)
        pivot = np.array([-6.3, -2.8, 0])
        tq = ValueTracker(0.0)
        L1a, L2a = 3.0, 2.8

        def arm():
            p = blob_point(tq.get_value(), c=np.array([-2.6, 0.2, 0]), s=0.7)
            d = p - pivot
            dist = min(np.linalg.norm(d), L1a + L2a - 1e-3)
            ang = np.arctan2(d[1], d[0]) + np.arccos(np.clip((L1a ** 2 + dist ** 2 - L2a ** 2) / (2 * L1a * dist), -1, 1))
            el = pivot + L1a * np.array([np.cos(ang), np.sin(ang), 0])
            return VGroup(Line(pivot, el, stroke_width=6, color=GRAY_B), Line(el, p, stroke_width=5, color=GRAY_B),
                          Circle(radius=0.18, color=YELLOW, stroke_width=3).move_to((el + p) / 2),
                          Dot(pivot, radius=0.1, color=WHITE), Dot(p, radius=0.09, color=YELLOW))
        plan = always_redraw(arm)
        pl = Tex("planimeter", font_size=32, color=YELLOW).move_to([-5.6, 2.9, 0])
        text = vo[14]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(b14[0]), Create(b14[1]), run_time=0.8)
            self.sync(tr, text, "This is exactly how")
            self.play(FadeIn(plan), FadeIn(pl), run_time=0.5)
            self.play(tq.animate.set_value(2 * PI), run_time=max(tr.get_remaining_duration() - 0.2, 2.5), rate_func=linear)
        self.rest()
        plan.clear_updaters()

        self.summary(vo[15],
                     [r"Circulation around $C$ $=\iint_R$ curl; outward flux across $C$ $=\iint_R$ div.",
                      r"$C$ closed and simple, counterclockwise: region on the left.",
                      r"$M=-\tfrac y2$, $N=\tfrac x2$: Area $=\tfrac12\oint_C x\,dy-y\,dx$."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
#  Exercises
# =============================================================================
def partials_grid(entries, size=32):
    """2x2 grid of partial derivatives: entries = [M_x, M_y, N_x, N_y] (tex)."""
    cells = [MathTex(e, font_size=size) for e in entries]
    g = VGroup(VGroup(cells[0], cells[1]).arrange(RIGHT, buff=0.6), VGroup(cells[2], cells[3]).arrange(RIGHT, buff=0.6))
    g.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    return g


VO["ex05"] = [
    "Exercise five from section sixteen point four. Use Green's theorem to find the counterclockwise circulation and the outward flux of F equals x minus y, i, plus y minus x, j, around the square bounded by x equals zero, x equals one, y equals zero, and y equals one.",
    "The curve is closed, and the region is a simple square. A perfect case for Green's theorem. We need four partial derivatives.",
    "M is x minus y, and N is y minus x. M x is one, M y is minus one, N x is minus one, and N y is one.",
    "The circulation uses the curl, N x minus M y. That is minus one, minus minus one, which is zero.",
    "So the circulation is the double integral of zero over the square, which is zero. The field does not swirl around the square.",
    "The flux uses the divergence, M x plus N y. That is one plus one, which is two.",
    "The flux is the double integral of two over the square. The integrand is constant, so the result is two times the area. The square has area one, so the flux is two.",
    "Positive flux: the field pushes fluid out of the square.",
    "Let's verify the flux directly, to see how much work Green's theorem saved us. The flux is the integral around C of M d y minus N d x, over the four sides, counterclockwise.",
    "Bottom side: y is zero, so d y is zero, and x goes from zero to one. We get minus N d x, which is x d x. That integrates to one half.",
    "Right side: x is one, so d x is zero, and y goes up from zero to one. M d y is one minus y, d y, which gives one half.",
    "Top side: y is one, and x goes back from one to zero. Minus N d x is minus, one minus x, d x, from one to zero, which gives one half. Left side: x is zero, and y goes down from one to zero. M d y is minus y d y, from one to zero, which also gives one half.",
    "Four times one half is two. The same answer, but with four separate integrals instead of one.",
    "Summary. One: compute the four partial derivatives first. Two: the circulation uses N x minus M y, and the flux uses M x plus N y. Three: with a constant integrand, the double integral is that constant times the area.",
]


class Ex16_4_05(FlatScene):
    def construct(self):
        vo = VO["ex05"]
        self.start("16.4 — Exercise 5",
                   r"\mathbf F=(x-y)\,\mathbf i+(y-x)\,\mathbf j,\quad C:\ \text{square }0\le x,y\le1",
                   checklist=CHECK_GREEN)
        ax, axl = left_axes([0, 1.3, 1], [0, 1.3, 1], 4.0)
        sq = region_between(ax, lambda x: 0.0, lambda x: 1.0, 0, 1)
        bnd = boundary_between(ax, lambda x: 0.0, lambda x: 1.0, 0, 1)
        side_tips = VGroup(tip_at(lambda u: ax.c2p(1, u), 0.5), tip_at(lambda u: ax.c2p(0, u), 0.5, reverse=True))
        arrs = VGroup()
        for x in np.linspace(0.1, 1.2, 5):
            for y in np.linspace(0.1, 1.2, 5):
                v = np.array([x - y, y - x])
                if np.linalg.norm(v) < 1e-6:
                    continue
                p = ax.c2p(x, y)
                arrs.add(Arrow(p, p + 0.5 * np.array([*v, 0]), buff=0, color=GRAY_B, stroke_width=2.5,
                               max_tip_length_to_length_ratio=0.3))
        text = vo[0]
        with self.voiceover(text=text) as tr:
            self.play(Write(self.title_mob), run_time=1.0)
            self.play(Write(self.problem_mob), run_time=1.8)
            self.play(Create(ax), FadeIn(axl), FadeIn(sq), Create(bnd[0]), FadeIn(bnd[1]), FadeIn(side_tips), run_time=1.2)
            self.play(FadeIn(arrs), run_time=0.8)
        self.rest()

        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.nb_add(Tex(r"closed curve, simple region $\checkmark$", font_size=32, color=C_ANSWER), gray=False)
        self.rest()

        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.nb_add(MathTex(r"M=x-y,\ \ N=y-x", font_size=36))
            self.sync(tr, text, "M x is one")
            self.nb_add(partials_grid([r"M_x=1", r"M_y=-1", r"N_x=-1", r"N_y=1"]))
        self.rest()

        steps = [(vo[3], MathTex(r"N_x-M_y=-1-(-1)=0", font_size=36, color=C_CURL), 1),
                 (vo[4], MathTex(r"\oint_C\mathbf F\cdot\mathbf T\,ds=\iint_R0\,dA=0", font_size=36, color=C_CURL), 2),
                 (vo[5], MathTex(r"M_x+N_y=1+1=2", font_size=36, color=C_DIV), 1)]
        for text, m, k in steps:
            with self.voiceover(text=text) as tr:
                self.check_step(k)
                self.nb_add(m, gray=False)
            self.rest()
        f6 = MathTex(r"\oint_C\mathbf F\cdot\mathbf n\,ds=\iint_R2\,dA=2\cdot1=2", font_size=36)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.nb_add(f6, buff=0.4, gray=False)
            boxed(self, f6)
        self.rest()
        out = VGroup(*[Arrow(ax.c2p(*p), ax.c2p(*p) + 0.6 * d, buff=0, color=C_DIV, stroke_width=5) for p, d in
                       [((0.5, 0), DOWN), ((1, 0.5), RIGHT), ((0.5, 1), UP), ((0, 0.5), LEFT)]])
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.play(LaggedStart(*[GrowArrow(a) for a in out], lag_ratio=0.15), run_time=0.8)
            self.nb_add(Tex("net outflow", font_size=32, color=C_DIV), gray=False)
        self.rest()
        self.play(FadeOut(out), FadeOut(arrs), run_time=0.4)

        # 8-12 — the long way
        self.nb_clear()
        self.chapter(1, "Check the long way")
        nums = VGroup(*[MathTex(str(i + 1), font_size=30, color=YELLOW).move_to(ax.c2p(*p)) for i, p in
                        enumerate([(0.5, -0.12), (1.12, 0.5), (0.5, 1.12), (-0.12, 0.5)])])
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.play(FadeIn(nums), run_time=0.6)
            self.nb_add(MathTex(r"\oint_C M\,dy-N\,dx", font_size=36))
        self.rest()
        sides = [(vo[9], r"\text{bottom: }y=0,\ dy=0:\ \int_0^1 x\,dx=\tfrac12", 0),
                 (vo[10], r"\text{right: }x=1,\ dx=0:\ \int_0^1(1-y)\,dy=\tfrac12", 1)]
        for text, tex, k in sides:
            with self.voiceover(text=text) as tr:
                self.play(Indicate(nums[k]), run_time=0.5)
                self.nb_add(MathTex(tex, font_size=32))
            self.rest()
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.play(Indicate(nums[2]), run_time=0.5)
            self.nb_add(MathTex(r"\text{top: }\int_1^0-(1-x)\,dx=\tfrac12", font_size=32))
            self.sync(tr, text, "Left side")
            self.play(Indicate(nums[3]), run_time=0.5)
            self.nb_add(MathTex(r"\text{left: }\int_1^0-y\,dy=\tfrac12", font_size=32))
        self.rest()
        f12 = MathTex(r"4\cdot\tfrac12=2\ \checkmark", font_size=40, color=C_ANSWER)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.nb_add(f12, buff=0.4, gray=False)
        self.rest()

        self.summary(vo[13],
                     [r"Compute the four partial derivatives first.",
                      r"Circulation: $N_x-M_y$; flux: $M_x+N_y$.",
                      r"Constant integrand: double integral $=$ constant $\times$ area."],
                     ["One:", "Two:", "Three:"])


VO["ex07"] = [
    "Exercise seven. Find the counterclockwise circulation and the outward flux of F equals y squared minus x squared, i, plus x squared plus y squared, j, around the triangle bounded by y equals zero, x equals three, and y equals x.",
    "First, draw the region. The line y equals zero is the x axis. The line x equals three is vertical. And y equals x is the diagonal. Together they form a triangle with corners at the origin, at three, zero, and at three, three.",
    "Describe it with vertical strips. At position x, the strip runs from the bottom, y equals zero, to the top, y equals x. And x runs from zero to three.",
    "The partial derivatives. M is y squared minus x squared: M x is minus two x, and M y is two y. N is x squared plus y squared: N x is two x, and N y is two y.",
    "The curl: N x minus M y equals two x minus two y.",
    "The circulation is the double integral of two x minus two y over the triangle. The inner integral, with respect to y, gives two x y minus y squared. At y equals x, that is two x squared minus x squared, which is x squared. At y equals zero, it is zero.",
    "The outer integral: x squared from zero to three gives x cubed over three, which is twenty seven over three, which is nine. The circulation is nine.",
    "The divergence: M x plus N y equals minus two x plus two y.",
    "Pause and think: compare this with the curl. Can you predict the flux without calculating?",
    "The divergence is exactly minus the curl. So the double integral is minus nine. The flux is minus nine: a net inflow.",
    "Let's double check with the integral anyway. The inner integral of minus two x plus two y, from zero to x, gives minus x squared. The outer integral of minus x squared from zero to three gives minus nine. Confirmed.",
    "Summary. One: always draw the region, and describe it with vertical strips: bottom curve, top curve, and the range of x. Two: in the inner integral, x is a constant, and the upper limit may depend on x. Three: look for shortcuts, like a divergence that is exactly minus the curl.",
]


class Ex16_4_07(FlatScene):
    def construct(self):
        vo = VO["ex07"]
        self.start("16.4 — Exercise 7",
                   VGroup(MathTex(r"\mathbf F=(y^2-x^2)\,\mathbf i+(x^2+y^2)\,\mathbf j", font_size=30),
                          MathTex(r"C:\ \text{triangle }y=0,\ x=3,\ y=x", font_size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                   checklist=CHECK_GREEN)
        self.intro(vo[0])
        ax, axl = left_axes([0, 3.5, 1], [0, 3.5, 1], 1.55)
        bot, top = (lambda x: 0.0), (lambda x: x)
        reg = region_between(ax, bot, top, 0, 3)
        bnd = boundary_between(ax, bot, top, 0, 3)
        vt = tip_at(lambda u: ax.c2p(3, u), 1.5)
        corners = VGroup(MathTex("(0,0)", font_size=26).next_to(ax.c2p(0, 0), DL, buff=0.05),
                         MathTex("(3,0)", font_size=26).next_to(ax.c2p(3, 0), DR, buff=0.05),
                         MathTex("(3,3)", font_size=26).next_to(ax.c2p(3, 3), UR, buff=0.05))
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Create(ax), FadeIn(axl), run_time=0.8)
            self.sync(tr, text, "Together they form")
            self.play(FadeIn(reg), Create(bnd[0]), FadeIn(bnd[1]), FadeIn(vt), FadeIn(corners), run_time=1.2)
        self.rest()
        xt = ValueTracker(0.3)
        st = strip(ax, xt, bot, top, w=0.08)
        sl = strip_labels(ax, xt, bot, top, "y=0", "y=x")
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(st), FadeIn(sl), run_time=0.5)
            self.play(xt.animate.set_value(2.7), run_time=2.5)
            self.nb_add(MathTex(r"\int_0^3\!\!\int_0^x\dots\,dy\,dx", font_size=36))
        self.rest()
        for m in sl:
            m.clear_updaters()
        self.play(FadeOut(sl), run_time=0.3)

        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.nb_add(partials_grid([r"M_x=-2x", r"M_y=2y", r"N_x=2x", r"N_y=2y"]))
        self.rest()
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            self.nb_add(MathTex(r"N_x-M_y=2x-2y", font_size=36, color=C_CURL), gray=False)
        self.rest()
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.nb_add(MathTex(r"\int_0^x(2x-2y)\,dy=\big[2xy-y^2\big]_0^x=x^2", font_size=34))
        self.rest()
        c6 = MathTex(r"\text{circulation}=\int_0^3x^2\,dx=9", font_size=36)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_add(c6, buff=0.4, gray=False)
            boxed(self, c6)
        self.rest()
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            self.nb_add(MathTex(r"M_x+N_y=-2x+2y", font_size=36, color=C_DIV), gray=False)
        self.rest()
        self.pause(vo[8], "Compare with the curl — predict the flux?")
        c9 = MathTex(r"-2x+2y=-(2x-2y)\ \Rightarrow\ \text{flux}=-9", font_size=36)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.nb_add(c9, buff=0.4, gray=False)
            boxed(self, c9)
            self.sync(tr, text, "a net inflow")
            self.nb_add(Tex("net inflow", font_size=30, color=C_DIV), gray=False)
        self.rest()
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(MathTex(r"\int_0^x(-2x+2y)\,dy=-x^2,\ \ \int_0^3-x^2\,dx=-9\ \checkmark", font_size=32))
        self.rest()
        st.clear_updaters()

        self.summary(vo[11],
                     [r"Draw the region; vertical strips: bottom, top, range of $x$.",
                      r"Inner integral: $x$ is a constant; the upper limit may depend on $x$.",
                      r"Look for shortcuts: here div $=-$curl."],
                     ["One:", "Two:", "Three:"])


VO["ex09"] = [
    "Exercise nine. Find the counterclockwise circulation and the outward flux of F equals x y plus y squared, i, plus x minus y, j, around the boundary of the region enclosed by the curves y equals x squared and x equals y squared.",
    "The region. y equals x squared is a parabola opening upward. x equals y squared is a parabola opening to the right; in the first quadrant, that is y equals the square root of x. The two curves meet at the origin and at one, one. The region is the lens shaped area in between.",
    "Vertical strips: at position x, the bottom is y equals x squared, and the top is y equals the square root of x. And x runs from zero to one. You saw this region in the double integral refresher.",
    "The partial derivatives. M is x y plus y squared: M x is y, and M y is x plus two y. N is x minus y: N x is one, and N y is minus one.",
    "The curl: N x minus M y equals one, minus x, minus two y.",
    "The inner integral, with respect to y, gives: one minus x, times y, minus y squared. We evaluate it between y equals x squared and y equals the square root of x.",
    "At the top, y equals the square root of x: one minus x, times the square root of x, minus x. At the bottom, y equals x squared: one minus x, times x squared, minus x to the fourth.",
    "Subtract and expand: the square root of x, minus x to the three halves, minus x, minus x squared, plus x cubed, plus x to the fourth.",
    "Now the outer integral from zero to one, term by term. The square root of x gives two thirds. Minus x to the three halves gives minus two fifths. Minus x gives minus one half. Minus x squared gives minus one third. x cubed gives one quarter. And x to the fourth gives one fifth.",
    "Group the terms. Two thirds minus one third is one third. Minus two fifths plus one fifth is minus one fifth. Minus one half plus one quarter is minus one quarter. So we get one third, minus one fifth, minus one quarter. In sixtieths: twenty, minus twelve, minus fifteen, which is minus seven sixtieths. The circulation is minus seven sixtieths.",
    "The divergence: M x plus N y equals y minus one.",
    "The inner integral of y minus one, with respect to y, is y squared over two, minus y. At the top, the square root of x: x over two, minus the square root of x. At the bottom, x squared: x to the fourth over two, minus x squared.",
    "Subtract: x over two, minus the square root of x, minus x to the fourth over two, plus x squared.",
    "The outer integral from zero to one: one quarter, minus two thirds, minus one tenth, plus one third. In sixtieths: fifteen, minus forty, minus six, plus twenty, which is minus eleven sixtieths. The flux is minus eleven sixtieths.",
    "Both answers are small and negative: a slight clockwise swirl, and a slight net inflow.",
    "Summary. One: find where the curves meet; that gives the outer limits. Two: evaluate the inner integral at the top curve minus the bottom curve, then expand into powers of x. Three: integrate term by term, and use a common denominator only at the very end.",
]


class Ex16_4_09(FlatScene):
    def construct(self):
        vo = VO["ex09"]
        self.start("16.4 — Exercise 9",
                   VGroup(MathTex(r"\mathbf F=(xy+y^2)\,\mathbf i+(x-y)\,\mathbf j", font_size=30),
                          MathTex(r"C:\ \text{boundary of the region between }y=x^2,\ x=y^2", font_size=28)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                   checklist=CHECK_GREEN)
        self.intro(vo[0])
        ax, axl = left_axes([0, 1.25, 1], [0, 1.25, 1], 4.6)
        bot, top = (lambda x: x * x), (lambda x: np.sqrt(max(x, 0)))
        reg = region_between(ax, bot, top, 0, 1)
        bnd = boundary_between(ax, bot, top, 0, 1)
        full = VGroup(ax.plot(lambda x: x * x, x_range=[0, 1.1], color=GRAY_B, stroke_width=2),
                      ax.plot(lambda x: np.sqrt(x), x_range=[0, 1.2], color=GRAY_B, stroke_width=2))
        cl = VGroup(MathTex(r"y=x^2", font_size=28).next_to(ax.c2p(0.85, 0.72), DR, buff=0.05),
                    MathTex(r"y=\sqrt x", font_size=28).next_to(ax.c2p(0.25, 0.5), UL, buff=0.05),
                    MathTex("(1,1)", font_size=26).next_to(ax.c2p(1, 1), UR, buff=0.05))
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Create(ax), FadeIn(axl), run_time=0.8)
            self.sync(tr, text, "y equals x squared is")
            self.play(Create(full[0]), FadeIn(cl[0]), run_time=0.8)
            self.sync(tr, text, "x equals y squared is")
            self.play(Create(full[1]), FadeIn(cl[1]), run_time=0.8)
            self.sync(tr, text, "The two curves meet")
            self.play(FadeIn(cl[2]), run_time=0.4)
            self.sync(tr, text, "The region is")
            self.play(FadeIn(reg), Create(bnd[0]), FadeIn(bnd[1]), run_time=1.0)
        self.rest()
        xt = ValueTracker(0.2)
        st = strip(ax, xt, bot, top, w=0.025)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(st), run_time=0.4)
            self.play(xt.animate.set_value(0.8), run_time=2.0)
            self.nb_add(MathTex(r"\int_0^1\!\!\int_{x^2}^{\sqrt x}\dots\,dy\,dx", font_size=36))
        self.rest()

        lines = [
            (3, MathTex(r"M_x=y,\ \ M_y=x+2y,\ \ N_x=1,\ \ N_y=-1", font_size=32), 0, True),
            (4, MathTex(r"N_x-M_y=1-x-2y", font_size=36, color=C_CURL), 1, False),
            (5, MathTex(r"\int_{x^2}^{\sqrt x}(1-x-2y)\,dy=\big[(1-x)y-y^2\big]_{x^2}^{\sqrt x}", font_size=32), 2, True),
            (6, MathTex(r"\text{top: }(1-x)\sqrt x-x,\quad\text{bottom: }(1-x)x^2-x^4", font_size=30), None, True),
            (7, MathTex(r"=\sqrt x-x^{3/2}-x-x^2+x^3+x^4", font_size=34), None, True),
        ]
        for i, m, k, g in lines:
            with self.voiceover(text=vo[i]) as tr:
                if k is not None:
                    self.check_step(k)
                self.nb_add(m, gray=g)
            self.rest()
        terms = MathTex(r"\tfrac23", r",\ -\tfrac25", r",\ -\tfrac12", r",\ -\tfrac13", r",\ \tfrac14", r",\ \tfrac15",
                        font_size=36)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.nb_add(terms, anim=FadeIn(terms[0]))
            for j, ph in enumerate(["Minus x to the three halves gives", "Minus x gives", "Minus x squared gives",
                                    "x cubed gives", "And x to the fourth gives"]):
                self.sync(tr, text, ph)
                self.play(FadeIn(terms[j + 1]), run_time=0.4)
            settle(self, terms)
        self.rest()
        c9 = MathTex(r"\tfrac13-\tfrac15-\tfrac14=\tfrac{20-12-15}{60}=-\tfrac{7}{60}", font_size=36)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.play(Indicate(terms[0]), Indicate(terms[3]), run_time=0.6)
            self.sync(tr, text, "Minus two fifths plus one fifth")
            self.play(Indicate(terms[1]), Indicate(terms[5]), run_time=0.6)
            self.sync(tr, text, "Minus one half plus one quarter")
            self.play(Indicate(terms[2]), Indicate(terms[4]), run_time=0.6)
            self.sync(tr, text, "In sixtieths")
            self.nb_add(c9, buff=0.4, gray=False)
            boxed(self, c9)
        self.rest()

        self.nb_clear()
        self.nb_add(MathTex(r"\text{circulation}=-\tfrac{7}{60}", font_size=34, color=C_CURL), gray=False, run_time=0.6)
        lines2 = [
            (10, MathTex(r"M_x+N_y=y-1", font_size=36, color=C_DIV), 1, False),
            (11, MathTex(r"\Big[\tfrac{y^2}{2}-y\Big]_{x^2}^{\sqrt x}:\ \text{top }\tfrac x2-\sqrt x,\ "
                         r"\text{bottom }\tfrac{x^4}{2}-x^2", font_size=30), 2, True),
            (12, MathTex(r"=\tfrac x2-\sqrt x-\tfrac{x^4}{2}+x^2", font_size=34), None, True),
        ]
        for i, m, k, g in lines2:
            with self.voiceover(text=vo[i]) as tr:
                if k is not None:
                    self.check_step(k)
                self.nb_add(m, gray=g)
            self.rest()
        c13 = MathTex(r"\tfrac14-\tfrac23-\tfrac1{10}+\tfrac13=\tfrac{15-40-6+20}{60}=-\tfrac{11}{60}", font_size=34)
        text = vo[13]
        with self.voiceover(text=text) as tr:
            self.nb_add(c13, buff=0.4, gray=False)
            boxed(self, c13)
        self.rest()
        st.clear_updaters()
        sw = card_left(self, Tex(r"slight clockwise swirl $\cdot$ slight net inflow", font_size=36, color=YELLOW))
        text = vo[14]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.play(FadeIn(sw), run_time=0.6)
        self.rest()

        self.summary(vo[15],
                     [r"Find where the curves meet: that gives the outer limits.",
                      r"Inner integral: top curve minus bottom curve, then expand in powers of $x$.",
                      r"Integrate term by term; common denominator only at the very end."],
                     ["One:", "Two:", "Three:"])


VO["ex22"] = [
    "Exercise twenty two. Use Green's theorem to evaluate the integral around C of three y d x plus two x d y, where C is the boundary of the region where x runs from zero to pi, and y runs from zero to sin x.",
    "The region lies under one arch of the sine curve, above the x axis. Its boundary C has two pieces: the x axis from zero to pi, and the sine curve back from pi to zero. That is counterclockwise, as Green's theorem requires.",
    "The integral has the form M d x plus N d y, so this is the circulation form. M is three y, and N is two x.",
    "The curl: N x is two, and M y is three. So N x minus M y equals two minus three, which is minus one.",
    "Pause and think: the integrand is a constant. What does that mean for the double integral?",
    "The double integral of a constant is that constant times the area of the region. So the line integral equals minus one times the area under the sine arch.",
    "The area is the integral from zero to pi of sin x, d x. That is minus cos x, from zero to pi: minus cos pi, plus cos zero, which is one plus one, so two.",
    "So the line integral equals minus two.",
    "Compare with the long way. You would need two line integrals: one along the x axis, and one along the sine curve, with x equals t and y equals sin t, including a product like t cos t that requires integration by parts. Green's theorem avoids all of that.",
    "Summary. One: recognise the form: M d x plus N d y means the circulation form. Two: when N x minus M y is a constant, the answer is that constant times the area. Three: Green's theorem is especially useful when the boundary consists of several pieces.",
]


class Ex16_4_22(FlatScene):
    def construct(self):
        vo = VO["ex22"]
        self.start("16.4 — Exercise 22",
                   VGroup(MathTex(r"\oint_C 3y\,dx+2x\,dy", font_size=32),
                          MathTex(r"C:\ \text{boundary of }0\le x\le\pi,\ 0\le y\le\sin x", font_size=28)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                   checklist=CHECK_GREEN)
        self.intro(vo[0])
        ax = Axes(x_range=[0, 3.5, 1], y_range=[0, 1.4, 1], x_length=6.2, y_length=2.5, tips=False,
                  axis_config={"stroke_color": GRAY_B, "include_numbers": True, "font_size": 22}).move_to([-3.5, -0.4, 0])
        axl = VGroup(MathTex("x", font_size=30).next_to(ax.x_axis, RIGHT, buff=0.1),
                     MathTex("y", font_size=30).next_to(ax.y_axis, UP, buff=0.1))
        bot, top = (lambda x: 0.0), (lambda x: np.sin(x))
        reg = region_between(ax, bot, top, 0, PI)
        bnd = boundary_between(ax, bot, top, 0, PI)
        pil = MathTex(r"\pi", font_size=30).next_to(ax.c2p(PI, 0), DOWN, buff=0.35)
        sl = MathTex(r"y=\sin x", font_size=28).next_to(ax.c2p(PI / 2, 1), UP, buff=0.12)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Create(ax), FadeIn(axl), FadeIn(pil), run_time=0.8)
            self.play(FadeIn(reg), FadeIn(sl), run_time=0.6)
            self.sync(tr, text, "the x axis from zero")
            self.play(Create(bnd[0]), run_time=1.5)
            self.sync(tr, text, "That is counterclockwise")
            self.play(FadeIn(bnd[1]), run_time=0.5)
        self.rest()

        form = Tex(r"$M\,dx+N\,dy$ $\to$ circulation form", font_size=32, color=C_CURL)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.nb_add(form, gray=False)
            self.sync(tr, text, "M is three y")
            self.nb_add(MathTex(r"M=3y,\ \ N=2x", font_size=36))
        self.rest()
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.nb_add(MathTex(r"N_x=2,\ \ M_y=3", font_size=34))
            self.check_step(1)
            self.nb_add(MathTex(r"N_x-M_y=2-3=-1", font_size=36, color=C_CURL), gray=False)
        self.rest()
        self.pause(vo[4], "Constant integrand — what does that mean?")
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.nb_add(MathTex(r"\iint_R(-1)\,dA=-\text{area}(R)", font_size=36))
            self.play(Indicate(reg, color=YELLOW), run_time=0.8)
        self.rest()
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_add(MathTex(r"\text{area}=\int_0^\pi\sin x\,dx=\big[-\cos x\big]_0^\pi=2", font_size=34))
        self.rest()
        f7 = MathTex(r"\oint_C 3y\,dx+2x\,dy=-2", font_size=38)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.nb_add(f7, buff=0.4, gray=False)
            boxed(self, f7)
        self.rest()
        lw = VGroup(Tex(r"long way: 2 line integrals,", font_size=30, color=GRAY_B),
                    Tex(r"incl.\ $\int t\cos t\,dt$ (by parts)", font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.15)
        card = card_left(self, lw, color=GRAY)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.play(FadeIn(card), run_time=0.6)
            self.sync(tr, text, "Green's theorem avoids")
            self.strike(lw[0], owner=card)
            self.strike(lw[1], owner=card)
        self.rest()

        self.summary(vo[9],
                     [r"$M\,dx+N\,dy$ means the circulation form.",
                      r"$N_x-M_y$ constant $\Rightarrow$ answer $=$ constant $\times$ area.",
                      r"Especially useful when the boundary has several pieces."],
                     ["One:", "Two:", "Three:"])


VO["ex26"] = [
    "Exercise twenty six. Use the Green's theorem area formula to find the area of the region enclosed by the ellipse r of t equals a cos t i plus b sin t j, for t from zero to two pi.",
    "The area formula: the area of R equals one half times the integral around C of x d y minus y d x. Recall where it comes from: Green's theorem with M equals minus y over two and N equals x over two, whose curl is exactly one.",
    "The ellipse has semi axes a and b. As t goes from zero to two pi, the point goes around once, counterclockwise. Exactly the orientation we need.",
    "Step one: x equals a cos t, and y equals b sin t. Their differentials: d x equals minus a sin t d t, and d y equals b cos t d t.",
    "Step two: x d y equals a cos t times b cos t d t, which is a b cos squared t, d t. And y d x equals b sin t times minus a sin t d t, which is minus a b sin squared t, d t.",
    "Step three: x d y minus y d x equals a b cos squared t, plus a b sin squared t, all times d t. Since cos squared plus sin squared is one, this is simply a b d t.",
    "Step four: the area is one half times the integral from zero to two pi of a b d t. That is one half, times a b, times two pi, which is pi a b.",
    "Check: for a circle, a equals b equals r, and we get pi r squared. Correct.",
    "Notice what happened: we found an area by only walking around the boundary. No double integral was needed. For curves given in parametric form, this is often the easiest way to compute an area.",
    "Summary. One: the area formula is one half times the integral of x d y minus y d x around C. Two: substitute the parametrisation, and simplify before integrating; often a Pythagorean identity appears. Three: check the result with a special case, like a circle.",
]


class Ex16_4_26(FlatScene):
    def construct(self):
        vo = VO["ex26"]
        self.start("16.4 — Exercise 26",
                   r"\text{Area inside }\mathbf r(t)=a\cos t\,\mathbf i+b\sin t\,\mathbf j,\ 0\le t\le2\pi",
                   checklist=[r"1 $x, y, dx, dy$", r"2 $x\,dy,\ y\,dx$", "3 simplify", "4 integrate"])
        self.intro(vo[0])
        f1 = MathTex(r"\text{Area}=\tfrac12\oint_C x\,dy-y\,dx", font_size=40)
        f1b = MathTex(r"M=-\tfrac y2,\ N=\tfrac x2,\ \ \text{curl}=1", font_size=32, color=GRAY_B)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.nb_add(f1, gray=False)
            boxed(self, f1, color=YELLOW)
            self.sync(tr, text, "Recall where it comes from")
            self.nb_add(f1b, gray=False)
        self.rest()

        EC, sc = np.array([-3.4, -0.3, 0]), 1.4
        a_t, b_t = ValueTracker(2.0), ValueTracker(1.0)

        def E(t):
            return EC + sc * np.array([a_t.get_value() * np.cos(t), b_t.get_value() * np.sin(t), 0])
        ell = always_redraw(lambda: ParametricFunction(E, t_range=[0, 2 * PI], color=C_BND, stroke_width=5,
                                                       fill_color=C_REG, fill_opacity=0.3))
        axes = VGroup(Line(EC + LEFT * 3.3, EC + RIGHT * 3.3, color=GRAY, stroke_width=1.5),
                      Line(EC + DOWN * 2.0, EC + UP * 2.0, color=GRAY, stroke_width=1.5))
        al = always_redraw(lambda: VGroup(
            Brace(Line(EC, E(0)), DOWN, buff=0.08, color=YELLOW),
            MathTex("a", font_size=32, color=YELLOW).next_to(Line(EC, E(0)), DOWN, buff=0.45),
            Brace(Line(EC, E(PI / 2)), LEFT, buff=0.08, color=YELLOW),
            MathTex("b", font_size=32, color=YELLOW).next_to(Line(EC, E(PI / 2)), LEFT, buff=0.45)))
        tt = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(E(tt.get_value()), radius=0.1, color=WHITE))
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(axes), FadeIn(ell), run_time=0.8)
            self.play(FadeIn(al), run_time=0.5)
            self.sync(tr, text, "As t goes")
            self.add(dot)
            self.play(tt.animate.set_value(2 * PI), run_time=3.0, rate_func=linear)
            etips = VGroup(tip_at(E, PI / 4), tip_at(E, 5 * PI / 4))
            self.play(FadeIn(etips), run_time=0.4)
        self.rest()

        steps = [(3, r"x=a\cos t,\ y=b\sin t,\ dx=-a\sin t\,dt,\ dy=b\cos t\,dt", 0, 32),
                 (4, r"x\,dy=ab\cos^2t\,dt,\quad y\,dx=-ab\sin^2t\,dt", 1, 34),
                 (5, r"x\,dy-y\,dx=ab(\cos^2t+\sin^2t)\,dt=ab\,dt", 2, 34)]
        for i, tex, k, fs in steps:
            with self.voiceover(text=vo[i]) as tr:
                self.check_step(k)
                self.nb_add(MathTex(tex, font_size=fs))
            self.rest()
        f6 = MathTex(r"\tfrac12\int_0^{2\pi}ab\,dt=\tfrac12\cdot ab\cdot2\pi=\pi ab", font_size=38)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(f6, buff=0.4, gray=False)
            boxed(self, f6)
        self.rest()
        f7 = MathTex(r"a=b=r\ \Rightarrow\ \pi r^2\ \checkmark", font_size=38, color=C_ANSWER)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(etips), run_time=0.3)
            self.play(a_t.animate.set_value(1.4), b_t.animate.set_value(1.4), run_time=1.5)
            self.nb_add(f7, gray=False)
        self.rest()
        ell.clear_updaters()
        al.clear_updaters()
        dot.clear_updaters()
        card = card_left(self, Tex(r"area by walking around the boundary", font_size=40, color=YELLOW))
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "we found an area")
            self.play(FadeIn(card), run_time=0.6)
        self.rest()

        self.summary(vo[9],
                     [r"Area $=\tfrac12\oint_C x\,dy-y\,dx$.",
                      r"Substitute the parametrisation and simplify first (Pythagorean identity).",
                      r"Check with a special case: a circle gives $\pi r^2$."],
                     ["One:", "Two:", "Three:"])
