"""16.1 Line integrals of scalar functions (Thomas' Calculus, 13e ed.)

Running example:  C: r(t) = (2 cos t, 2 sin t), 0 <= t <= pi/2  (quarter circle)
                  f(x, y) = x y
                  int_C f ds = 4

Scenes:
  LineIntegralIdea         Riemann sum  sum f(P_k) ds_k  along the curve -> integral
  LineIntegralFence        3D: int_C f ds = area of the "fence" with height f above C
  LineIntegralComputation  step-by-step evaluation via parametrisation

Render (from repo root):
  .venv/Scripts/manim -ql scenes/16_1_line_integrals_scalar.py LineIntegralIdea
"""
from manim import *
import numpy as np

# --- example ---------------------------------------------------------------
R = 2.0
T0, T1 = 0.0, PI / 2


def r(t):
    return np.array([R * np.cos(t), R * np.sin(t)])


def f(x, y):
    return x * y


F_MAX = R * R / 2  # max of xy on the quarter circle (at t = pi/4)
EXACT = 4.0

# --- style -----------------------------------------------------------------
C_CURVE = BLUE
C_LOW, C_HIGH = BLUE, YELLOW  # colour scale for f
C_DS = GREEN


def f_color(t):
    return interpolate_color(C_LOW, C_HIGH, f(*r(t)) / F_MAX)


def riemann_sum(n):
    """Midpoint sum  sum f(P_k) * |chord_k|."""
    ts = np.linspace(T0, T1, n + 1)
    total = 0.0
    for a, b in zip(ts[:-1], ts[1:]):
        total += f(*r((a + b) / 2)) * np.linalg.norm(r(b) - r(a))
    return total


class LineIntegralIdea(Scene):
    def construct(self):
        title = Text("16.1  Line integral of a scalar function", font_size=36).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 2.5, 1], y_range=[0, 2.5, 1],
            x_length=5, y_length=5, tips=False,
            axis_config={"include_numbers": True, "font_size": 24},
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        curve = axes.plot_parametric_curve(r, t_range=[T0, T1], color=C_CURVE)
        c_label = MathTex("C", color=C_CURVE).move_to(axes.c2p(*(1.15 * r(PI / 3))))

        info = VGroup(
            MathTex(r"f(x,y) = xy"),
            MathTex(r"C:\ \mathbf r(t) = (2\cos t,\ 2\sin t)"),
            MathTex(r"0 \le t \le \tfrac{\pi}{2}"),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8)
        info.to_edge(RIGHT, buff=0.6).shift(UP * 1.6)

        self.play(Create(axes), FadeIn(info))
        self.play(Create(curve), Write(c_label))
        self.wait(0.5)

        # --- Riemann sum --------------------------------------------------
        def pieces(n):
            ts = np.linspace(T0, T1, n + 1)
            segs, dots = VGroup(), VGroup()
            for a, b in zip(ts[:-1], ts[1:]):
                m = (a + b) / 2
                segs.add(Line(axes.c2p(*r(a)), axes.c2p(*r(b)),
                              color=f_color(m), stroke_width=8))
                dots.add(Dot(axes.c2p(*r(m)), radius=0.06 if n <= 8 else 0.03, color=WHITE))
            return VGroup(segs, dots)

        sum_tex = MathTex(r"\sum_{k=1}^{n} f(P_k)\,\Delta s_k").scale(0.9)
        n_val = Integer(4)
        s_val = DecimalNumber(riemann_sum(4), num_decimal_places=4)
        n_line = VGroup(MathTex("n ="), n_val).arrange(RIGHT)
        s_line = VGroup(MathTex(r"\text{sum} \approx"), s_val).arrange(RIGHT)
        readout = VGroup(sum_tex, n_line, s_line).arrange(DOWN, aligned_edge=LEFT, buff=0.15).scale(0.85)
        readout.next_to(info, DOWN, buff=0.4, aligned_edge=LEFT)

        cur = pieces(4)
        self.play(FadeOut(curve), Create(cur[0]), FadeIn(cur[1]))

        # explain one piece
        seg = cur[0][1]
        ds_brace = BraceLabel(seg, r"\Delta s_k", brace_direction=seg.copy().rotate(-PI / 2).get_unit_vector(),
                              label_constructor=MathTex, font_size=30)
        ds_brace.set_color(C_DS)
        pk = MathTex("P_k", font_size=30).next_to(cur[1][1], DL, buff=0.1)
        self.play(FadeIn(ds_brace), Write(pk))

        hint = Tex(r"colour = value of $f$ at $P_k$", font_size=30, color=GRAY_B)
        hint.next_to(axes, DOWN, buff=0.3)
        self.play(FadeIn(hint), Write(readout))
        self.wait(1)
        self.play(FadeOut(ds_brace), FadeOut(pk))

        for n in [8, 16, 40]:
            new = pieces(n)
            self.play(
                Transform(cur, new),
                n_val.animate.set_value(n),
                s_val.animate.set_value(riemann_sum(n)),
                run_time=1.2,
            )
            self.wait(0.5)

        # --- limit -> integral ---------------------------------------------
        limit = MathTex(
            r"\int_C f\,ds", "=", r"\lim_{n\to\infty}\sum_{k=1}^{n} f(P_k)\,\Delta s_k", "=", "4"
        ).scale(0.8)
        limit.next_to(readout, DOWN, buff=0.45, aligned_edge=LEFT)
        limit.shift(LEFT * max(0, limit.get_right()[0] - (config.frame_width / 2 - 0.3)))
        box = SurroundingRectangle(limit, color=YELLOW, buff=0.15)
        self.play(Write(limit))
        self.play(Create(box))
        self.wait(2)


class LineIntegralFence(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[0, 2.5, 1], y_range=[0, 2.5, 1], z_range=[0, 2.5, 1],
            x_length=5, y_length=5, z_length=4, tips=False,
        )
        axes.shift(IN * 1.6)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("y"), MathTex("z"))
        self.set_camera_orientation(phi=68 * DEGREES, theta=-35 * DEGREES, zoom=0.95)

        title = Text("Line integral = area of the fence", font_size=34).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        self.play(Create(axes), FadeIn(labels))

        curve = ParametricFunction(lambda t: axes.c2p(*r(t), 0), t_range=[T0, T1], color=C_CURVE)
        curve.set_stroke(width=6)
        self.play(Create(curve))

        top = ParametricFunction(lambda t: axes.c2p(*r(t), f(*r(t))), t_range=[T0, T1], color=C_HIGH)
        top.set_stroke(width=5)

        # height bars rising from the curve
        bars = VGroup(*[
            Line(axes.c2p(*r(t), 0), axes.c2p(*r(t), f(*r(t))), color=f_color(t), stroke_width=4)
            for t in np.linspace(T0, T1, 13)
        ])
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.1))
        self.play(Create(top))

        fence = Surface(
            lambda u, v: axes.c2p(*r(u), v * f(*r(u))),
            u_range=[T0, T1], v_range=[0, 1], resolution=(24, 4),
            fill_opacity=0.55, checkerboard_colors=[YELLOW_D, YELLOW_E],
            stroke_width=0.5, stroke_color=YELLOW_A,
        )
        self.play(FadeIn(fence), FadeOut(bars))

        formula = MathTex(r"\int_C f\,ds", r"=\ \text{area}", r"=\ 4").scale(0.9)
        sub = MathTex(r"\text{height} = f(x,y) = xy,\quad \text{base} = C", font_size=32)
        group = VGroup(formula, sub).arrange(DOWN, aligned_edge=LEFT).to_corner(DR)
        self.add_fixed_in_frame_mobjects(group)
        self.play(Write(formula), FadeIn(sub))

        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(1)


class LineIntegralComputation(Scene):
    def construct(self):
        title = Text("How to compute it", font_size=36).to_edge(UP)
        general = MathTex(
            r"\int_C f\,ds = \int_a^b f\big(\mathbf r(t)\big)\,\lvert\mathbf r'(t)\rvert\,dt"
        )
        general.scale(0.8).next_to(title, DOWN, buff=0.3)
        gbox = SurroundingRectangle(general, color=YELLOW, buff=0.15)
        self.play(Write(title))
        self.play(Write(general), Create(gbox))
        self.wait(1)

        steps = VGroup(
            MathTex(r"1.\ \ \mathbf r(t) = (2\cos t,\ 2\sin t),\quad 0 \le t \le \tfrac{\pi}{2}"),
            MathTex(r"2.\ \ \mathbf r'(t) = (-2\sin t,\ 2\cos t),\quad \lvert\mathbf r'(t)\rvert = \sqrt{4\sin^2 t + 4\cos^2 t} = 2"),
            MathTex(r"3.\ \ ds = \lvert\mathbf r'(t)\rvert\,dt = 2\,dt"),
            MathTex(r"4.\ \ \int_C xy\,ds = \int_0^{\pi/2} (2\cos t)(2\sin t)\cdot 2\,dt"),
            MathTex(r"5.\ \ = 8\int_0^{\pi/2}\sin t\cos t\,dt = 8\cdot\tfrac12 = 4"),
        ).scale(0.62).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        steps.next_to(general, DOWN, buff=0.45)

        notes = [
            "parametrise C",
            "speed of the parametrisation",
            "arc-length element",
            "substitute x = 2cos t, y = 2sin t",
            "evaluate",
        ]
        for step, note in zip(steps, notes):
            tag = Text(note, font_size=20, color=GRAY_B).to_edge(DOWN, buff=0.25)
            self.play(Write(step), FadeIn(tag), run_time=1.2)
            self.wait(0.8)
            self.play(FadeOut(tag), run_time=0.3)

        ans = SurroundingRectangle(steps[-1], color=GREEN, buff=0.12)
        warn = Tex(r"Don't forget $\lvert\mathbf r'(t)\rvert$ !", font_size=34, color=RED)
        warn.next_to(steps[2], RIGHT, buff=1.0)
        self.play(Create(ans), FadeIn(warn))
        self.wait(2)
