"""16.1 Line integrals of scalar functions (Thomas' Calculus, 13e ed.)

Running example:  C: r(t) = (2 cos t, 2 sin t), 0 <= t <= pi/2  (quarter circle)
                  f(x, y) = x y
                  int_C f ds = 4

Scenes (all with English voiceover, Kokoro af_heart):
  LineIntegralIdea         Riemann sum  sum f(P_k) ds_k  along the curve -> integral
  LineIntegralFence        3D: int_C f ds = area of the "fence" with height f above C
  LineIntegralComputation  step-by-step evaluation via parametrisation
  Ex16_1_09                Exercise 9  (worked, ~5 min): int_C (x+y) ds = sqrt(2)
  Ex16_1_10                Exercise 10 (HW: stops at the set-up integral)
  Ex16_1_14                Exercise 14 (worked): infinite ray, improper integral = 1
  Ex16_1_15                Exercise 15 (HW: stops at the two set-up integrals)

Voiceover text: edit the VO dict below.

Render (from repo root):
  .venv/Scripts/manim -ql scenes/16_1_line_integrals_scalar.py LineIntegralIdea
"""
from manim import *
from manim_voiceover import VoiceoverScene
from _tts import kokoro
from _exercise import (ExerciseScene, center_for, face_camera, cam_matrix, C_ANSWER, C_WRONG, C_NEG)
import numpy as np

# --- render targets (python render.py <this file> <Scene>) -> videos/<path>.mp4
OUTPUT = {
    "LineIntegralIdea": "16.1 Line integrals (scalar)/Concept/1 - Idea (Riemann sum)",
    "LineIntegralFence": "16.1 Line integrals (scalar)/Concept/2 - Fence (area)",
    "LineIntegralComputation": "16.1 Line integrals (scalar)/Concept/3 - Computation",
    "Ex16_1_09": "16.1 Line integrals (scalar)/Exercises/Ex 09",
    "Ex16_1_10": "16.1 Line integrals (scalar)/Exercises/Ex 10 (HW)",
    "Ex16_1_14": "16.1 Line integrals (scalar)/Exercises/Ex 14",
    "Ex16_1_15": "16.1 Line integrals (scalar)/Exercises/Ex 15 (HW)",
}

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

# --- voiceover text (English, one entry per animation step) ----------------
VO = {
    "idea": [
        "Section sixteen point one: line integrals of scalar functions. "
        "We want to integrate the function f of x y equals x times y "
        "along a curve C: a quarter circle of radius two.",
        "First, we chop the curve into small pieces.",
        "Each piece has a length, delta s k. Inside each piece we pick a point, P k.",
        "We multiply the value of f at P k by the length of the piece, and add everything up. "
        "The colour shows how large f is.",
        "With more and more pieces, the sum settles down to four.",
        "The limit of these sums is the line integral of f over C, "
        "written as the integral of f d s. Here it equals four.",
    ],
    "fence": [
        "There is also a nice picture of this integral.",
        "Here is the curve C, lying in the x y plane.",
        "Above every point of the curve, we raise a wall up to height f of x y.",
        "The top edge follows the function along the curve.",
        "Together, these walls form a fence.",
        "When f is positive, the line integral is exactly the area of this fence. "
        "So this fence has area four.",
        "Notice that the base is measured along the curve itself, not along the x axis.",
    ],
    "computation": [
        "To compute a line integral, we parametrise the curve and use this formula: "
        "the integral of f of r of t, times the length of r prime of t, d t.",
        "Step one: parametrise C. We use two cos t, two sin t, for t from zero to pi over two.",
        "Step two: differentiate. The speed, the length of r prime of t, equals two.",
        "Step three: so d s equals two d t.",
        "Step four: substitute x equals two cos t and y equals two sin t into f.",
        "Step five: evaluate. Eight times the integral of sine times cosine "
        "gives eight times one half, which is four.",
        "The most common mistake: forgetting the factor, the length of r prime of t.",
    ],
}


def f_color(t):
    return interpolate_color(C_LOW, C_HIGH, f(*r(t)) / F_MAX)


def riemann_sum(n):
    """Midpoint sum  sum f(P_k) * |chord_k|."""
    ts = np.linspace(T0, T1, n + 1)
    total = 0.0
    for a, b in zip(ts[:-1], ts[1:]):
        total += f(*r((a + b) / 2)) * np.linalg.norm(r(b) - r(a))
    return total


class LineIntegralIdea(VoiceoverScene):
    def construct(self):
        self.set_speech_service(kokoro())
        vo = VO["idea"]

        title = Text("16.1  Line integral of a scalar function", font_size=36).to_edge(UP)
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

        with self.voiceover(text=vo[0]) as tracker:
            d = tracker.duration / 3
            self.play(Write(title), run_time=d)
            self.play(Create(axes), FadeIn(info), run_time=d)
            self.play(Create(curve), Write(c_label), run_time=d)

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
        with self.voiceover(text=vo[1]) as tracker:
            self.play(FadeOut(curve), Create(cur[0]), FadeIn(cur[1]), run_time=tracker.duration)

        # explain one piece
        seg = cur[0][1]
        ds_brace = BraceLabel(seg, r"\Delta s_k", brace_direction=seg.copy().rotate(-PI / 2).get_unit_vector(),
                              label_constructor=MathTex, font_size=30)
        ds_brace.set_color(C_DS)
        pk = MathTex("P_k", font_size=30).next_to(cur[1][1], DL, buff=0.1)
        with self.voiceover(text=vo[2]) as tracker:
            d = tracker.duration / 2
            self.play(FadeIn(ds_brace), run_time=d)
            self.play(Write(pk), run_time=d)

        hint = Tex(r"colour = value of $f$ at $P_k$", font_size=30, color=GRAY_B)
        hint.next_to(axes, DOWN, buff=0.3)
        with self.voiceover(text=vo[3]) as tracker:
            self.play(Write(readout), run_time=tracker.duration * 0.6)
            self.play(FadeIn(hint), run_time=tracker.get_remaining_duration())
        self.play(FadeOut(ds_brace), FadeOut(pk), run_time=0.5)

        with self.voiceover(text=vo[4]) as tracker:
            ns = [8, 16, 40]
            d = tracker.duration / len(ns)
            for n in ns:
                self.play(
                    Transform(cur, pieces(n)),
                    n_val.animate.set_value(n),
                    s_val.animate.set_value(riemann_sum(n)),
                    run_time=d,
                )

        # --- limit -> integral ---------------------------------------------
        limit = MathTex(
            r"\int_C f\,ds", "=", r"\lim_{n\to\infty}\sum_{k=1}^{n} f(P_k)\,\Delta s_k", "=", "4"
        ).scale(0.8)
        limit.next_to(readout, DOWN, buff=0.45, aligned_edge=LEFT)
        limit.shift(LEFT * max(0, limit.get_right()[0] - (config.frame_width / 2 - 0.3)))
        box = SurroundingRectangle(limit, color=YELLOW, buff=0.15)
        with self.voiceover(text=vo[5]) as tracker:
            self.play(Write(limit), run_time=tracker.duration * 0.75)
            self.play(Create(box), run_time=tracker.get_remaining_duration())
        self.wait(1)


class LineIntegralFence(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.set_speech_service(kokoro())
        vo = VO["fence"]

        axes = ThreeDAxes(
            x_range=[0, 2.5, 1], y_range=[0, 2.5, 1], z_range=[0, 2.5, 1],
            x_length=5, y_length=5, z_length=4, tips=False,
        )
        axes.shift(IN * 1.6)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("y"), MathTex("z"))
        self.set_camera_orientation(phi=68 * DEGREES, theta=-35 * DEGREES, zoom=0.95)

        title = Text("Line integral = area of the fence", font_size=34).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        title.set_opacity(0)

        with self.voiceover(text=vo[0]) as tracker:
            d = tracker.duration / 2
            self.play(title.animate.set_opacity(1), run_time=d)
            self.play(Create(axes), FadeIn(labels), run_time=d)

        curve = ParametricFunction(lambda t: axes.c2p(*r(t), 0), t_range=[T0, T1], color=C_CURVE)
        curve.set_stroke(width=6)
        with self.voiceover(text=vo[1]) as tracker:
            self.play(Create(curve), run_time=tracker.duration)

        top = ParametricFunction(lambda t: axes.c2p(*r(t), f(*r(t))), t_range=[T0, T1], color=C_HIGH)
        top.set_stroke(width=5)

        # height bars rising from the curve
        bars = VGroup(*[
            Line(axes.c2p(*r(t), 0), axes.c2p(*r(t), f(*r(t))), color=f_color(t), stroke_width=4)
            for t in np.linspace(T0, T1, 13)
        ])
        with self.voiceover(text=vo[2]) as tracker:
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.1), run_time=tracker.duration)
        with self.voiceover(text=vo[3]) as tracker:
            self.play(Create(top), run_time=tracker.duration)

        fence = Surface(
            lambda u, v: axes.c2p(*r(u), v * f(*r(u))),
            u_range=[T0, T1], v_range=[0, 1], resolution=(24, 4),
            fill_opacity=0.55, checkerboard_colors=[YELLOW_D, YELLOW_E],
            stroke_width=0.5, stroke_color=YELLOW_A,
        )
        with self.voiceover(text=vo[4]) as tracker:
            self.play(FadeIn(fence), FadeOut(bars), run_time=tracker.duration)

        formula = MathTex(r"\int_C f\,ds", r"=\ \text{area}", r"=\ 4").scale(0.9)
        sub = MathTex(r"\text{height} = f(x,y) = xy,\quad \text{base} = C", font_size=32)
        group = VGroup(formula, sub).arrange(DOWN, aligned_edge=LEFT).to_corner(DR)
        self.add_fixed_in_frame_mobjects(group)
        group.set_opacity(0)
        with self.voiceover(text=vo[5]) as tracker:
            self.play(formula.animate.set_opacity(1), run_time=tracker.duration / 2)
            self.play(sub.animate.set_opacity(1), run_time=tracker.get_remaining_duration())

        self.begin_ambient_camera_rotation(rate=0.25)
        with self.voiceover(text=vo[6]) as tracker:
            self.wait(tracker.duration)
        self.stop_ambient_camera_rotation()
        self.wait(1)


class LineIntegralComputation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(kokoro())
        vo = VO["computation"]

        title = Text("How to compute it", font_size=36).to_edge(UP)
        general = MathTex(
            r"\int_C f\,ds = \int_a^b f\big(\mathbf r(t)\big)\,\lvert\mathbf r'(t)\rvert\,dt"
        )
        general.scale(0.8).next_to(title, DOWN, buff=0.3)
        gbox = SurroundingRectangle(general, color=YELLOW, buff=0.15)
        with self.voiceover(text=vo[0]) as tracker:
            self.play(Write(title), run_time=tracker.duration * 0.2)
            self.play(Write(general), Create(gbox), run_time=tracker.get_remaining_duration())

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
        for step, note, text in zip(steps, notes, vo[1:6]):
            tag = Text(note, font_size=20, color=GRAY_B).to_edge(DOWN, buff=0.25)
            with self.voiceover(text=text) as tracker:
                self.play(Write(step), FadeIn(tag), run_time=tracker.duration * 0.8)
            self.play(FadeOut(tag), run_time=0.3)

        ans = SurroundingRectangle(steps[-1], color=GREEN, buff=0.12)
        warn = Tex(r"Don't forget $\lvert\mathbf r'(t)\rvert$ !", font_size=34, color=RED)
        warn.next_to(steps[2], RIGHT, buff=1.0)
        with self.voiceover(text=vo[6]) as tracker:
            self.play(Create(ans), FadeIn(warn), run_time=tracker.duration * 0.5)
        self.wait(1.5)




# ===========================================================================
# Exercise videos — style: CLAUDE.md "Opgaven-video's (stijl)", helpers: scenes/_exercise.py
# ===========================================================================
C_F = YELLOW
C_DT = ORANGE
C_TEAL = TEAL
# 3D view for planar segments. theta = -115 deg looks almost straight at a fence above
# the segment (0,1)->(1,0); the requested -50 deg looks along it (fence edge-on).
PHI_FENCE, THETA_FENCE = 65 * DEGREES, -115 * DEGREES


def num_tex(x, nd=3):
    return f"{x:.{nd}f}"


# ---------------------------------------------------------------------------
# Exercise 9:  int_C (x+y) ds,  C: x = t, y = 1 - t, z = 0   ->  sqrt(2)
# ---------------------------------------------------------------------------
VO["ex09"] = [
    "Exercise nine from section sixteen point one. We have to evaluate the integral over C of x plus y, d s. "
    "C is the straight line segment from the point zero, one, zero, to the point one, zero, zero.",
    "Before we calculate anything, let's understand what this integral means. We walk along the curve C. "
    "At every point, we take the value of f, multiply it by a tiny piece of length, d s, and add all these "
    "pieces together.",
    "Chapter one: the curve. It is given by x equals t, y equals one minus t, and z equals zero. Since z is zero, "
    "everything happens in the x y plane, so we look at it from above.",
    "Watch what happens as t increases. At t equals zero, we are at zero, one. At t equals one half, we are "
    "halfway, at one half, one half. At t equals one, we arrive at one, zero. The parameter t tells us where we "
    "are on the curve.",
    "Chapter two: the function on the curve. Pause the video and think: what is x plus y on this segment?",
    "Let's check a few points. Zero plus one is one. A quarter plus three quarters is one. One half plus one half "
    "is one. Every point of this segment has x plus y equal to one. That is no coincidence: the segment lies on "
    "the line x plus y equals one.",
    "Chapter three: a picture. Above every point of the curve, we put a wall with height f. Here f equals one "
    "everywhere, so the wall is a rectangle of height one. For a positive f, the line integral is the area of "
    "this wall.",
    "Another way to see it: unroll the curve onto a straight axis, the s axis, where s measures distance along "
    "the curve. The curve becomes an interval from zero to its length, square root of two. Now the line integral "
    "is just an ordinary area under the graph of f. Here it is a rectangle, one high and square root of two wide. "
    "So we expect the answer: square root of two.",
    "Chapter four: the definition, with real numbers. Cut the curve into four equal pieces. Each piece has length "
    "square root of two divided by four, about zero point three five. In the middle of each piece, f equals one. "
    "So each piece contributes one times zero point three five.",
    "Adding the four pieces gives about one point four one, which is the square root of two. With eight or "
    "sixteen pieces we get exactly the same, because f is constant here. For a function that changes along the "
    "curve, more pieces make the sum more accurate.",
    "Chapter five: why the length of r prime of t appears. Below the picture, you see the t axis from zero to "
    "one. When t moves a quarter, the point on the curve moves about zero point three five. The curve is "
    "stretched compared to the t axis.",
    "This stretch factor is d s divided by d t: the speed of the point, which is the length of r prime of t. "
    "Here it equals square root of two. So every d t must be multiplied by square root of two to turn it into a "
    "real length, d s.",
    "Chapter six: the formal method, in four steps. Step one: write the curve as a vector function. r of t "
    "equals t i, plus one minus t, j, with t from zero to one.",
    "Step two: differentiate, and take the length. r prime of t equals i minus j. Its length is the square root "
    "of one squared plus minus one squared, which is square root of two.",
    "Step three: substitute the curve into f. x plus y becomes t plus one minus t, which is one.",
    "Step four: put it together and integrate. The integral from zero to one of one times square root of two, "
    "d t, equals square root of two. This matches the area of the wall.",
    "Chapter seven: the most common mistake. If you forget the length of r prime of t, you compute the integral "
    "of one, d t, from zero to one, and get one. That is the length of the t interval, not the length of the "
    "curve. It is wrong.",
    "Summary. One: a line integral adds f times length along the curve. Two: d s equals the length of r prime of "
    "t, times d t, because the curve is stretched compared to t. Three: when f equals one, the line integral is "
    "the length of the curve. And if f were the density of a wire, this integral would be its mass.",
]


class Ex16_1_09(ExerciseScene):
    def construct(self):
        vo = VO["ex09"]
        self.start("16.1 — Exercise 9", r"\int_C (x+y)\,ds,\qquad C:\ (0,1,0)\to(1,0,0)")

        U = 2.2
        O = np.array([-5.2, 0.2, 0.0])
        axes = ThreeDAxes(x_range=[0, 1.5, 0.5], y_range=[0, 1.5, 0.5], z_range=[0, 1.5, 0.5],
                          x_length=1.5 * U, y_length=1.5 * U, z_length=1.5 * U, tips=False)
        axes.shift(O - axes.c2p(0, 0, 0))

        def P(x, y, z=0):
            return axes.c2p(x, y, z)

        z_axis = axes.z_axis  # only in 3D (from above, perspective draws it as a stray line)
        axes2d = VGroup(
            axes.x_axis, axes.y_axis,
            MathTex("x", font_size=30).next_to(P(1.5, 0), RIGHT, buff=0.15),
            MathTex("y", font_size=30).next_to(P(0, 1.5), UP, buff=0.15),
            MathTex("1", font_size=24).next_to(P(1, 0), DOWN, buff=0.15),
            MathTex("1", font_size=24).next_to(P(0, 1), LEFT, buff=0.15),
        )
        seg = Line(P(0, 1), P(1, 0), color=C_CURVE, stroke_width=6)

        # 0 — exercise
        self.intro(vo[0])

        # 1 — what the integral means
        w = [Tex(r"walk along $C$", font_size=30), Tex(r"value $f$", font_size=30, color=C_F),
             Tex(r"$\times$ tiny length $ds$", font_size=30, color=C_DS), Tex("add up", font_size=30)]
        ar = [MathTex(r"\to", font_size=30) for _ in range(3)]
        row1 = VGroup(w[0], ar[0], w[1], ar[1]).arrange(RIGHT, buff=0.15)
        row2 = VGroup(w[2], ar[2], w[3]).arrange(RIGHT, buff=0.15)
        schema = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "We walk")
            self.nb_add(schema, anim=FadeIn(w[0]), run_time=0.8)
            self.sync(tr, text, "we take the value")
            self.play(FadeIn(ar[0]), FadeIn(w[1]), run_time=0.8)
            self.sync(tr, text, "multiply it")
            self.play(FadeIn(ar[1]), FadeIn(w[2]), run_time=0.8)
            self.sync(tr, text, "add all")
            self.play(FadeIn(ar[2]), FadeIn(w[3]), run_time=0.8)
        self.add(schema)
        self.rest()

        # 2 — chapter 1: the curve
        self.chapter(1, "The curve")
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(Create(axes2d), run_time=1.5)
            self.play(Create(seg), run_time=1.0)
            self.sync(tr, text, "It is given")
            self.nb_add(MathTex(r"x=t,\ \ y=1-t,\ \ z=0", font_size=34))
        self.rest()

        # 3 — moving point
        t = ValueTracker(0.0)
        dot = Dot(P(0, 1), color=WHITE, radius=0.09)
        dot.add_updater(lambda m: m.move_to(P(t.get_value(), 1 - t.get_value())))
        t_num = DecimalNumber(0, num_decimal_places=2, font_size=32)
        t_num.add_updater(lambda m: m.set_value(t.get_value()))
        t_lab = VGroup(MathTex("t =", font_size=32), t_num).arrange(RIGHT, buff=0.12).move_to(P(1.15, 1.45))
        coords = [MathTex(s, font_size=28).next_to(P(a, 1 - a), UR, buff=0.12)
                  for a, s in [(0, r"(0,\,1)"), (0.5, r"(\tfrac12,\,\tfrac12)"), (1, r"(1,\,0)")]]
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(dot), FadeIn(t_lab), run_time=0.6)
            self.sync(tr, text, "At t equals zero")
            self.play(FadeIn(coords[0]), Indicate(dot), run_time=0.8)
            self.sync(tr, text, "At t equals one half")
            self.play(t.animate.set_value(0.5), run_time=1.6)
            self.play(FadeIn(coords[1]), run_time=0.5)
            self.sync(tr, text, "At t equals one, we")
            self.play(t.animate.set_value(1), run_time=1.6)
            self.play(FadeIn(coords[2]), run_time=0.5)
        self.rest()
        self.play(FadeOut(VGroup(*coords)), FadeOut(t_lab), FadeOut(dot), run_time=0.6)

        # 4 — chapter 2 + pause
        self.chapter(2, "The function on the curve")
        self.pause(vo[4], r"What is $x + y$ on this segment?")

        # 5 — x + y = 1 everywhere
        vals = [(0, "0", "1"), (0.25, r"\tfrac14", r"\tfrac34"), (0.5, r"\tfrac12", r"\tfrac12"),
                (0.75, r"\tfrac34", r"\tfrac14"), (1, "1", "0")]
        marks = VGroup(*[Dot(P(a, 1 - a), radius=0.07, color=C_F) for a, _, _ in vals])
        vlabels = VGroup(*[MathTex(f"{xs} + {ys} = 1", font_size=28, color=C_F).next_to(P(a, 1 - a), UR, buff=0.08)
                           for a, xs, ys in vals])
        ext = DashedLine(P(-0.2, 1.2), P(1.25, -0.25), color=C_CURVE, stroke_width=3)
        ext_lab = MathTex("x+y=1", font_size=30, color=C_CURVE).next_to(P(1.25, -0.25), RIGHT, buff=0.1)
        f_C = MathTex(r"f\big|_C = x+y = 1", font_size=36, color=C_F)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            for k, ph in enumerate(["Zero plus one", "A quarter", "One half plus"]):
                self.sync(tr, text, ph)
                self.play(FadeIn(marks[k]), FadeIn(vlabels[k]), run_time=0.6)
            self.sync(tr, text, "Every point")
            self.play(FadeIn(marks[3:]), FadeIn(vlabels[3:]), run_time=0.8)
            self.nb_add(f_C)
            self.sync(tr, text, "the segment lies")
            self.play(Create(ext), FadeIn(ext_lab), run_time=1.2)
        self.play(Indicate(f_C))
        self.rest()

        # 6 — chapter 3: the wall (3D)
        self.chapter(3, "A picture")
        d_world = P(0.5, 0.5, 0.4)
        screen = np.array([-3.6, -0.4, 0])
        c3 = center_for(PHI_FENCE, THETA_FENCE, d_world, screen)
        h = ValueTracker(0.001)
        fence = always_redraw(lambda: Polygon(
            P(0, 1, 0), P(1, 0, 0), P(1, 0, h.get_value()), P(0, 1, h.get_value()),
            color=C_F, fill_color=C_F, fill_opacity=0.5, stroke_width=2))
        h_lab = face_camera(Tex("height $f = 1$", font_size=32, color=C_F), PHI_FENCE, THETA_FENCE)
        h_lab.move_to(P(1, 0, 0.55) + cam_matrix(PHI_FENCE, THETA_FENCE).T @ np.array([1.3, 0, 0]))
        b_lab = face_camera(Tex("base $C$", font_size=32, color=C_CURVE), PHI_FENCE, THETA_FENCE)
        b_lab.move_to(P(0.5, 0.5, 0) + cam_matrix(PHI_FENCE, THETA_FENCE).T @ np.array([0.5, -0.55, 0]))
        flat = VGroup(marks, vlabels, ext, ext_lab)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.move_camera(phi=PHI_FENCE, theta=THETA_FENCE, frame_center=c3,
                             added_anims=[FadeOut(flat), FadeIn(z_axis)], run_time=2.0)
            self.sync(tr, text, "we put a wall")
            self.add(fence)
            self.play(h.animate.set_value(1), run_time=2.0)
            self.sync(tr, text, "so the wall")
            self.play(FadeIn(h_lab), FadeIn(b_lab), run_time=0.8)
            self.sync(tr, text, "For a positive")
            for dth in (20, -20, 0):
                th = THETA_FENCE + dth * DEGREES
                self.move_camera(theta=th, frame_center=center_for(PHI_FENCE, th, d_world, screen),
                                 run_time=2.5 if dth != -20 else 4.0)
        fence.clear_updaters()
        self.rest()
        self.move_camera(phi=0, theta=-PI / 2, frame_center=ORIGIN,
                         added_anims=[FadeOut(fence), FadeOut(h_lab), FadeOut(b_lab), FadeOut(z_axis)],
                         run_time=1.8)

        # 7 — unroll onto the s-axis
        s0 = np.array([O[0], -3.3, 0])
        s1 = s0 + RIGHT * np.sqrt(2) * U
        s_axis = Line(s0 + LEFT * 0.2, s1 + RIGHT * 0.6, stroke_width=2)
        s_name = MathTex("s", font_size=30).next_to(s_axis, RIGHT, buff=0.1)
        s_ticks = VGroup(MathTex("0", font_size=26).next_to(s0, DOWN, buff=0.12),
                         MathTex(r"\sqrt2", font_size=26).next_to(s1, DOWN, buff=0.12))
        unrolled = seg.copy()
        rect = Polygon(s0, s1, s1 + UP * U, s0 + UP * U, color=C_F, fill_color=C_F, fill_opacity=0.45,
                       stroke_width=2)
        rect_labs = VGroup(MathTex("f = 1", font_size=30, color=C_F).move_to(rect),
                           MathTex("1", font_size=26).next_to(rect, LEFT, buff=0.12))
        area_eq = MathTex(r"\int_C f\,ds = \text{area} = 1\cdot\sqrt2", r"\;\;(\text{expected})", font_size=34)
        area_eq[1].set_color(GRAY_B)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "unroll")
            self.play(Create(s_axis), FadeIn(s_name), run_time=0.8)
            self.play(Transform(unrolled, Line(s0, s1, color=C_CURVE, stroke_width=6)), run_time=2.0)
            self.sync(tr, text, "The curve becomes")
            self.play(FadeIn(s_ticks), run_time=0.6)
            self.sync(tr, text, "Now the line integral")
            self.play(FadeIn(rect), FadeIn(rect_labs), run_time=1.2)
            self.sync(tr, text, "So we expect")
            self.nb_add(area_eq)
        self.play(Indicate(area_eq[0]))
        self.rest()
        unroll_grp = VGroup(s_axis, s_name, s_ticks, unrolled, rect, rect_labs)

        # 8 — chapter 4: Riemann sum with numbers
        self.nb_clear()
        self.chapter(4, "The definition with numbers")

        def pieces(n):
            ts = np.linspace(0, 1, n + 1)
            segs = VGroup(*[Line(P(a, 1 - a), P(b, 1 - b), stroke_width=9,
                                 color=GREEN_B if i % 2 == 0 else GREEN_E)
                            for i, (a, b) in enumerate(zip(ts[:-1], ts[1:]))])
            mids = VGroup(*[Dot(P((a + b) / 2, 1 - (a + b) / 2), radius=0.06 if n <= 8 else 0.04, color=WHITE)
                            for a, b in zip(ts[:-1], ts[1:])])
            return segs, mids

        col_x = [0, 0.9, 2.5, 4.1]

        def row(cells, colors, size=32):
            g = VGroup()
            for x, c, col in zip(col_x, cells, colors):
                m = MathTex(c, font_size=size, color=col)
                m.move_to([x, 0, 0], aligned_edge=LEFT)
                g.add(m)
            return g

        header = row(["k", "f(P_k)", r"\Delta s_k", r"f\cdot\Delta s"], [WHITE, C_F, C_DS, WHITE])
        header.add(Line(header.get_corner(DL) + DOWN * 0.12, header.get_corner(DR) + DOWN * 0.12 + RIGHT * 0.3,
                        stroke_width=1.5, color=GRAY))
        rows = [row([str(k), "1", "0.354", "0.354"], [WHITE, C_F, C_DS, WHITE]) for k in range(1, 5)]
        segs, mids = pieces(4)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Cut the curve")
            self.play(Create(segs), run_time=1.5)
            self.sync(tr, text, "Each piece has length")
            self.play(Indicate(segs, color=C_DS), run_time=1.0)
            self.sync(tr, text, "In the middle")
            self.play(FadeIn(mids), run_time=0.8)
            self.nb_add(header, gray=False, run_time=0.8, buff=0.18)
            self.sync(tr, text, "So each piece")
            for k in range(4):
                self.nb_add(rows[k], gray=False, run_time=0.6, buff=0.14, anim=FadeIn(rows[k]))
                self.play(Indicate(segs[k], color=YELLOW), run_time=0.5)
        self.rest()

        # 9 — the sum, n = 8, 16
        sum_eq = MathTex(r"\sum f\,\Delta s = 4\cdot 0.354 \approx 1.414 = \sqrt2", font_size=34)
        n8 = MathTex(r"n = 8:\ \ 8\cdot 0.177 \approx 1.414", font_size=32)
        n16 = MathTex(r"n = 16:\ \ 16\cdot 0.0884 \approx 1.414", font_size=32)
        const = Tex(r"$f$ constant $\Rightarrow$ every $n$ gives $\sqrt2$", font_size=32, color=C_F)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.nb_add(sum_eq, gray=False, buff=0.35)
            self.play(Indicate(sum_eq), run_time=0.8)
            self.sync(tr, text, "With eight")
            s8, m8 = pieces(8)
            self.play(Transform(segs, s8), Transform(mids, m8), run_time=0.8)
            self.nb_add(n8, gray=False, run_time=0.8)
            s16, m16 = pieces(16)
            n16.move_to(n8, aligned_edge=LEFT)
            self.play(Transform(segs, s16), Transform(mids, m16), Transform(n8, n16), run_time=0.8)
            self.sync(tr, text, "because f is constant")
            self.nb_add(const, gray=False)
        self.rest()

        # 10 — chapter 5: why |r'(t)|
        self.play(FadeOut(segs), FadeOut(mids), FadeOut(unroll_grp), run_time=0.6)
        self.nb_clear()
        self.chapter(5, r"Why $\lvert\mathbf r'(t)\rvert$")
        nl = NumberLine(x_range=[0, 1, 0.25], length=U, color=C_DT, tick_size=0.08, include_numbers=False)
        nl.shift(np.array([O[0], -1.6, 0]) - nl.n2p(0))
        nl_nums = VGroup(*[MathTex(s, font_size=24, color=C_DT).next_to(nl.n2p(v), DOWN, buff=0.15)
                           for v, s in [(0, "0"), (0.25, r"\tfrac14"), (0.5, r"\tfrac12"), (0.75, r"\tfrac34"),
                                        (1, "1")]])
        nl_name = MathTex("t", font_size=32, color=C_DT).next_to(nl, LEFT, buff=0.3)
        t.set_value(0)
        dot.move_to(P(0, 1))
        nl_dot = Dot(nl.n2p(0), color=C_DT, radius=0.09)
        nl_dot.add_updater(lambda m: m.move_to(nl.n2p(t.get_value())))

        def braces(a, b):
            sb = Brace(Line(P(a, 1 - a), P(b, 1 - b)), direction=normalize(UR), color=C_DS, buff=0.05)
            tb = Brace(Line(nl.n2p(a), nl.n2p(b)), direction=UP, color=C_DT, buff=0.05)
            return sb, tb

        sb, tb = braces(0, 0.25)
        s_txt = MathTex(r"\Delta s \approx 0.354", font_size=28, color=C_DS)
        t_txt = MathTex(r"\Delta t = 0.25", font_size=28, color=C_DT)
        s_txt.add_updater(lambda m: m.next_to(sb, UR, buff=0.02))
        t_txt.add_updater(lambda m: m.next_to(tb, UP, buff=0.05))
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Below the picture")
            self.play(Create(nl), FadeIn(nl_nums), FadeIn(nl_name), FadeIn(dot), FadeIn(nl_dot), run_time=1.2)
            self.sync(tr, text, "When t moves")
            self.play(FadeIn(sb), FadeIn(tb), FadeIn(s_txt), FadeIn(t_txt), t.animate.set_value(0.25),
                      run_time=1.4, rate_func=linear)
            for k in range(1, 4):
                nsb, ntb = braces(k / 4, (k + 1) / 4)
                self.play(Transform(sb, nsb), Transform(tb, ntb), t.animate.set_value((k + 1) / 4),
                          run_time=1.2, rate_func=linear)
        self.rest(0.6)

        # 11 — stretch factor
        ratio1 = MathTex(r"\frac{\Delta s}{\Delta t} = \frac{0.354}{0.25} = \sqrt2 = \lvert\mathbf r'(t)\rvert",
                         font_size=34)
        ratio2 = MathTex(r"\Rightarrow\ ds = \lvert\mathbf r'(t)\rvert\,dt = \sqrt2\,dt", font_size=34)
        box2 = SurroundingRectangle(ratio2, color=YELLOW, buff=0.12)
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.nb_add(ratio1)
            self.sync(tr, text, "So every d t")
            self.nb_add(VGroup(ratio2, box2))
        self.play(Indicate(ratio2))
        self.rest()
        self.play(FadeOut(VGroup(sb, tb, s_txt, t_txt)), FadeOut(dot), FadeOut(nl_dot), run_time=0.6)

        # 12-15 — chapter 6: the formal method
        self.nb_clear()
        self.chapter(6, "The formal method")
        steps = [
            MathTex(r"1.\ \ \mathbf r(t) = t\,\mathbf i + (1-t)\,\mathbf j,\quad 0\le t\le 1", font_size=32),
            MathTex(r"2.\ \ \mathbf r'(t)=\mathbf i-\mathbf j,\ \ \lvert\mathbf r'(t)\rvert=\sqrt{1^2+(-1)^2}=\sqrt2",
                    font_size=32),
            MathTex(r"3.\ \ f(\mathbf r(t)) = t + (1-t) = 1", font_size=32),
            MathTex(r"4.\ \ \int_C (x+y)\,ds=\int_0^1 1\cdot\sqrt2\,dt=\sqrt2", font_size=32),
        ]
        ans_box = SurroundingRectangle(steps[3], color=C_ANSWER, buff=0.12)
        self.show_checklist()
        for k in range(4):
            text = vo[12 + k]
            with self.voiceover(text=text) as tr:
                self.check_step(k)
                if k == 0:
                    self.sync(tr, text, "Step one")
                if k < 3:
                    self.nb_add(steps[k], buff=0.4)
                else:
                    self.nb_add(VGroup(steps[3], ans_box), buff=0.3)
                    self.sync(tr, text, "This matches")
                    mini = Rectangle(width=np.sqrt(2) * 0.6, height=0.6, color=C_F, fill_color=C_F,
                                     fill_opacity=0.45, stroke_width=2)
                    ml = VGroup(MathTex("1", font_size=22).next_to(mini, LEFT, buff=0.08),
                                MathTex(r"\sqrt2", font_size=22).next_to(mini, DOWN, buff=0.08))
                    ok = Tex(r"$\checkmark$ matches the area", font_size=30, color=C_ANSWER)
                    sketch = VGroup(VGroup(mini, ml), ok).arrange(RIGHT, buff=0.4)
                    self.nb_add(sketch, gray=False, anim=FadeIn(sketch))
            if k in (1, 3):
                self.play(Indicate(steps[k]))
            self.rest()

        # 16 — chapter 7: common mistake
        self.chapter(7, "Common mistake")
        wrong = MathTex(r"\int_0^1 1\,dt = 1", font_size=36, color=C_WRONG)
        note = Tex(r"length of the $t$-interval $\neq$ length of the curve", font_size=30)
        len_t = MathTex(r"\text{length } 1", font_size=26, color=C_WRONG).next_to(nl, RIGHT, buff=0.35)
        len_c = MathTex(r"\text{length } \sqrt2", font_size=26, color=C_ANSWER).next_to(
            seg.get_center(), DL, buff=0.2)
        text = vo[16]
        with self.voiceover(text=text) as tr:
            self.play(*[c.animate.set_color(WHITE) for c in self.checklist], run_time=0.4)
            self.sync(tr, text, "you compute")
            self.nb_add(wrong)
            self.sync(tr, text, "That is the length")
            self.play(nl.animate.set_color(C_WRONG), FadeIn(len_t), run_time=0.8)
            self.play(seg.animate.set_color(C_ANSWER), FadeIn(len_c), run_time=0.8)
            self.nb_add(note, gray=False)
            self.sync(tr, text, "It is wrong")
            self.strike(wrong)
        self.rest()

        # 17 — summary
        self.summary(
            vo[17],
            [r"A line integral adds $f\times$ length along the curve.",
             r"$ds = \lvert\mathbf r'(t)\rvert\,dt$ — the curve is stretched compared to $t$.",
             r"If $f = 1$: $\displaystyle\int_C ds$ = length of $C$."],
            ["One:", "Two:", "Three:"],
            extra=r"($f$ = density of a wire $\Rightarrow$ $\int_C f\,ds$ = its mass)", extra_phrase="And if f",
        )


# ---------------------------------------------------------------------------
# Exercise 10 (HW):  int_C (x - y + z - 2) ds,  C: x = t, y = 1 - t, z = 1
#   HW -> stop at the set-up integral, never show the value.
# ---------------------------------------------------------------------------
VO["ex10"] = [
    "Exercise ten. Evaluate the integral over C of x minus y plus z minus two, d s. C is the straight line "
    "segment from zero, one, one, to one, zero, one.",
    "Compare this with exercise nine. The segment has exactly the same shape, only lifted to height z equals one. "
    "What changes is the function.",
    "Chapter one: the curve. x equals t, y equals one minus t, z equals one. As t goes from zero to one, the point "
    "moves from zero, one, one, to one, zero, one, in the horizontal plane z equals one.",
    "Chapter two: the function on the curve. Pause and think: is f positive or negative on this segment?",
    "Let's check. At the start: zero minus one, plus one, minus two, gives minus two. In the middle: one half "
    "minus one half, plus one, minus two, gives minus one. At the end: one minus zero, plus one, minus two, gives "
    "zero. So f goes from minus two up to zero. It is negative almost everywhere.",
    "In the wall picture, a negative f gives a wall that hangs downward, below the curve. This part counts as "
    "negative area. So we expect a negative answer.",
    "Unrolled onto the s axis, f becomes a straight line from minus two up to zero, over an interval of length "
    "square root of two. The line integral is the signed area between this graph and the s axis.",
    "Chapter three: the definition, with numbers. Cut the curve into four pieces, each of length square root of "
    "two over four. In the middle of the pieces, f equals minus seven quarters, minus five quarters, minus three "
    "quarters, and minus one quarter. Multiply each value by the length of the piece, and add them up. Do this "
    "on paper: it is your first check.",
    "Chapter four: why the length of r prime of t. The speed is the same as in exercise nine. The point moves "
    "square root of two along the curve for every unit of t. So d s equals square root of two, d t.",
    "Chapter five: the formal method. Step one: r of t equals t i, plus one minus t, j, plus k, with t from zero "
    "to one.",
    "Step two: r prime of t equals i minus j. The k component is constant, so its derivative is zero. The length "
    "is square root of two.",
    "Step three: substitute into f. x minus y becomes t minus, between brackets, one minus t. Then plus z, which "
    "is one, and minus two. Remove the brackets carefully: minus one plus t. Everything together gives two t "
    "minus two.",
    "Step four: the line integral becomes the integral from zero to one of two t minus two, times square root of "
    "two, d t. Now it is your turn. Compute this integral. Check that your answer is negative, and that it "
    "agrees with your sum from the table.",
    "Summary. One: a line integral can be negative when f is negative on the curve. Two: a constant component of "
    "r of t disappears in r prime of t. Three: simplify f of r of t carefully, especially the minus signs, before "
    "you integrate.",
]


class Ex16_1_10(ExerciseScene):
    PHI, THETA = 50 * DEGREES, -115 * DEGREES

    def construct(self):
        vo = VO["ex10"]
        PHI, THETA = self.PHI, self.THETA
        U = 2.0
        axes = ThreeDAxes(x_range=[0, 1.5, 0.5], y_range=[0, 1.5, 0.5], z_range=[-1, 1.5, 0.5],
                          x_length=1.5 * U, y_length=1.5 * U, z_length=2.5 * U, tips=False)

        def P(x, y, z=0):
            return axes.c2p(x, y, z)

        d_world, screen = P(0.5, 0.5, 0.3), np.array([-3.6, -0.2, 0])
        self.start("16.1 — Exercise 10 (HW)",
                   r"\int_C (x-y+z-2)\,ds,\quad C:\ (0,1,1)\to(1,0,1)",
                   phi=PHI, theta=THETA, frame_center=center_for(PHI, THETA, d_world, screen))
        ax_labels = VGroup(*[face_camera(MathTex(s, font_size=34), PHI, THETA).move_to(p) for s, p in
                             [("x", P(1.7, 0, 0)), ("y", P(0, 1.7, 0)), ("z", P(0, 0, 1.7))]])
        f = lambda t: 2 * t - 2

        def r(t, z=1.0):
            return P(t, 1 - t, z)

        # 0
        self.add(axes, ax_labels)
        self.intro(vo[0])

        # 1 — same shape as Ex 9, lifted
        ghost = DashedLine(r(0, 0), r(1, 0), color=GRAY, stroke_width=3)
        seg = Line(r(0, 0), r(1, 0), color=GRAY, stroke_width=6)
        lifted = Tex(r"same shape, lifted to $z = 1$", font_size=32, color=C_CURVE)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Create(ghost), run_time=1.0)
            self.add(seg)
            self.sync(tr, text, "only lifted")
            self.play(seg.animate.put_start_and_end_on(r(0), r(1)).set_color(C_CURVE), run_time=2.0)
            self.nb_add(lifted)
        self.rest()

        # 2 — chapter 1: the curve
        self.chapter(1, "The curve")
        plane = Polygon(P(0, 0, 1), P(1.5, 0, 1), P(1.5, 1.5, 1), P(0, 1.5, 1), stroke_color=BLUE_E,
                        stroke_width=1, fill_color=BLUE_E, fill_opacity=0.15)
        t = ValueTracker(0.0)
        dot = Dot3D(r(0), radius=0.07, color=WHITE)
        dot.add_updater(lambda m: m.move_to(r(t.get_value())))
        t_num = DecimalNumber(0, num_decimal_places=2, font_size=32)
        t_num.add_updater(lambda m: m.set_value(t.get_value()))
        t_lab = VGroup(MathTex("t =", font_size=32), t_num).arrange(RIGHT, buff=0.12).move_to([-5.6, 3.4, 0])
        self.fixed(t_lab)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(plane), run_time=0.8)
            self.nb_add(MathTex(r"x=t,\ \ y=1-t,\ \ z=1", font_size=34))
            self.sync(tr, text, "As t goes")
            self.play(FadeIn(dot), FadeIn(t_lab), run_time=0.5)
            self.play(t.animate.set_value(1), run_time=4.0, rate_func=linear)
        self.rest()
        self.play(FadeOut(dot), FadeOut(t_lab), run_time=0.5)

        # 3 — chapter 2 + pause
        self.chapter(2, "The function on the curve")
        self.pause(vo[3], r"Is $f$ positive or negative on $C$?")

        # 4 — values on the curve
        vals = [(0, r"0-1+1-2=-2", C_NEG), (0.5, r"\tfrac12-\tfrac12+1-2=-1", C_NEG), (1, r"1-0+1-2=0", WHITE)]
        marks = VGroup(*[Dot3D(r(a), radius=0.06, color=col) for a, _, col in vals])
        labs = VGroup()
        for a, s, col in vals:
            m = MathTex(s, font_size=28, color=col)
            m.move_to(self.to_screen(r(a)) + np.array([0, 0.45, 0]))
            labs.add(m)
        labs[0].shift(LEFT * 0.4)
        self.fixed(*labs)
        f_range = Tex(r"$f$ goes from $-2$ up to $0$", font_size=32, color=C_NEG)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            for k, ph in enumerate(["At the start", "In the middle", "At the end"]):
                self.sync(tr, text, ph)
                self.play(FadeIn(marks[k]), FadeIn(labs[k]), run_time=0.8)
            self.sync(tr, text, "So f goes")
            self.nb_add(f_range)
        self.rest()

        # 5 — wall hanging downward
        h = ValueTracker(0.001)
        wall = always_redraw(lambda: Polygon(r(0), r(1), r(0, 1 - 2 * h.get_value()),
                                             color=C_NEG, fill_color=C_NEG, fill_opacity=0.5, stroke_width=2))
        neg = Tex(r"negative $f$ $\to$ negative area", font_size=32, color=C_NEG)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(labs), run_time=0.4)
            self.add(wall)
            self.play(h.animate.set_value(1), run_time=2.0)
            self.sync(tr, text, "This part counts")
            self.nb_add(neg)
            for dth in (20, -20, 0):
                th = THETA + dth * DEGREES
                self.move_camera(theta=th, frame_center=center_for(PHI, th, d_world, screen),
                                 run_time=2.5 if dth != -20 else 4.0)
        wall.clear_updaters()
        self.rest()

        # 6 — unrolled: signed area (no number!)
        ov = self.left_overlay()
        ax2 = Axes(x_range=[0, 1.7, 0.5], y_range=[-2.3, 0.7, 1], x_length=5.0, y_length=4.4, tips=False)
        ax2.move_to([-3.4, -0.2, 0])
        graph = ax2.plot(lambda s: 2 * (s / np.sqrt(2)) - 2, x_range=[0, np.sqrt(2)], color=C_NEG, stroke_width=5)
        area = ax2.get_area(graph, x_range=[0, np.sqrt(2)], color=C_NEG, opacity=0.45)
        g_labs = VGroup(MathTex("s", font_size=30).next_to(ax2.x_axis, RIGHT, buff=0.1),
                        MathTex("f", font_size=30, color=C_NEG).next_to(ax2.y_axis, UP, buff=0.1),
                        MathTex(r"\sqrt2", font_size=28).next_to(ax2.c2p(np.sqrt(2), 0), UP, buff=0.15),
                        MathTex("-2", font_size=28).next_to(ax2.c2p(0, -2), LEFT, buff=0.15),
                        Line(ax2.c2p(np.sqrt(2), -0.08), ax2.c2p(np.sqrt(2), 0.08)))
        self.fixed(ax2, graph, area, g_labs)
        signed = Tex(r"line integral = signed area", font_size=32)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(ov), run_time=0.6)
            self.play(Create(ax2), FadeIn(g_labs), run_time=1.0)
            self.sync(tr, text, "f becomes")
            self.play(Create(graph), run_time=1.5)
            self.sync(tr, text, "The line integral")
            self.play(FadeIn(area), run_time=1.0)
            self.nb_add(signed)
        self.rest()
        self.play(FadeOut(VGroup(ov, ax2, graph, area, g_labs)), FadeOut(marks), FadeOut(wall), run_time=0.8)

        # 7 — chapter 3: Riemann sum table, total left open
        self.nb_clear()
        self.chapter(3, "The definition with numbers")
        ts = np.linspace(0, 1, 5)
        segs = VGroup(*[Line(r(a), r(b), stroke_width=9, color=GREEN_B if i % 2 == 0 else GREEN_E)
                        for i, (a, b) in enumerate(zip(ts[:-1], ts[1:]))])
        mids = VGroup(*[Dot3D(r((a + b) / 2), radius=0.06, color=WHITE) for a, b in zip(ts[:-1], ts[1:])])
        header = self.table_row(["k", "f(P_k)", r"\Delta s_k", r"f\cdot\Delta s"], [WHITE, C_NEG, C_DS, WHITE])
        header.add(Line(header.get_corner(DL) + DOWN * 0.12, header.get_corner(DR) + DOWN * 0.12 + RIGHT * 0.3,
                        stroke_width=1.5, color=GRAY))
        fv = [r"-\tfrac74", r"-\tfrac54", r"-\tfrac34", r"-\tfrac14"]
        rows = [self.table_row([str(k + 1), fv[k], r"\tfrac{\sqrt2}{4}", "?"], [WHITE, C_NEG, C_DS, YELLOW])
                for k in range(4)]
        total = MathTex(r"\sum f\,\Delta s = \ ?", font_size=34, color=YELLOW)
        paper = Tex("do this on paper: your first check", font_size=30, color=GRAY_B)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Cut the curve")
            self.play(Create(segs), run_time=1.2)
            self.nb_add(header, gray=False, run_time=0.8, buff=0.18)
            self.sync(tr, text, "In the middle")
            self.play(FadeIn(mids), run_time=0.6)
            for k, ph in enumerate(["minus seven", "minus five", "minus three", "minus one quarter"]):
                self.sync(tr, text, ph)
                self.nb_add(rows[k], gray=False, run_time=0.6, buff=0.14, anim=FadeIn(rows[k]))
            self.sync(tr, text, "and add them up")
            self.nb_add(total, gray=False, buff=0.3)
            self.sync(tr, text, "Do this on paper")
            self.nb_add(paper, gray=False)
        self.rest()

        # 8 — chapter 4: why |r'(t)| (short)
        self.play(FadeOut(segs), FadeOut(mids), run_time=0.5)
        self.nb_clear()
        self.chapter(4, r"Why $\lvert\mathbf r'(t)\rvert$")
        nl = NumberLine(x_range=[0, 1, 0.25], length=U, color=C_DT, tick_size=0.08)
        nl.shift(np.array([-5.4, -3.0, 0]) - nl.n2p(0))
        nl_name = MathTex("t", font_size=32, color=C_DT).next_to(nl, LEFT, buff=0.3)
        nl_nums = VGroup(MathTex("0", font_size=24, color=C_DT).next_to(nl.n2p(0), DOWN, buff=0.15),
                         MathTex("1", font_size=24, color=C_DT).next_to(nl.n2p(1), DOWN, buff=0.15))
        t.set_value(0)
        nl_dot = Dot(nl.n2p(0), color=C_DT, radius=0.09)
        nl_dot.add_updater(lambda m: m.move_to(nl.n2p(t.get_value())))
        self.fixed(nl, nl_name, nl_nums, nl_dot)

        def braces(a, b):
            pa, pb = self.to_screen(r(a)), self.to_screen(r(b))
            perp = rotate_vector(normalize(pb - pa), PI / 2)
            sb = BraceBetweenPoints(pa, pb, direction=perp, color=C_DS)
            tb = Brace(Line(nl.n2p(a), nl.n2p(b)), direction=UP, color=C_DT, buff=0.05)
            self.fixed(sb, tb)
            return sb, tb

        sb, tb = braces(0, 0.25)
        same = MathTex(r"ds = \sqrt2\,dt", r"\quad(\text{same as Ex 9})", font_size=34)
        same[1].set_color(GRAY_B)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.play(Create(nl), FadeIn(nl_name), FadeIn(nl_nums), FadeIn(nl_dot), FadeIn(dot), run_time=1.0)
            self.sync(tr, text, "The point moves")
            self.play(FadeIn(sb), FadeIn(tb), t.animate.set_value(0.25), run_time=0.9, rate_func=linear)
            for k in range(1, 4):
                nsb, ntb = braces(k / 4, (k + 1) / 4)
                self.play(Transform(sb, nsb), Transform(tb, ntb), t.animate.set_value((k + 1) / 4),
                          run_time=0.8, rate_func=linear)
            self.sync(tr, text, "So d s equals")
            self.nb_add(same)
        self.rest()
        self.play(FadeOut(VGroup(sb, tb, nl, nl_name, nl_nums, nl_dot)), FadeOut(dot), run_time=0.6)

        # 9-12 — chapter 5: the formal method
        self.nb_clear()
        self.chapter(5, "The formal method")
        self.show_checklist()
        s1 = MathTex(r"1.\ \ \mathbf r(t)=t\,\mathbf i+(1-t)\,\mathbf j+\mathbf k,\quad 0\le t\le 1", font_size=32)
        s2 = MathTex(r"2.\ \ \mathbf r'(t)=\mathbf i-\mathbf j", r"\ (+\,0\,\mathbf k)",
                     r",\ \ \lvert\mathbf r'(t)\rvert=\sqrt2", font_size=32)
        s3a = MathTex(r"3.\ \ f(\mathbf r(t)) = t", r"-(1-t)", r"+1-2", font_size=32)
        s3b = MathTex(r"\phantom{3.\ \ f(\mathbf r(t))}\ = t", r"-1+t", r"+1-2", font_size=32)
        s3c = MathTex(r"\phantom{3.\ \ f(\mathbf r(t))}\ = 2t-2", font_size=32)
        s4 = MathTex(r"4.\ \ \int_C (x-y+z-2)\,ds=\int_0^1 (2t-2)\sqrt2\,dt", font_size=32)
        s4_box = SurroundingRectangle(s4, color=YELLOW, buff=0.12)

        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.sync(tr, text, "Step one")
            self.nb_add(s1, buff=0.4)
        self.rest()

        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            self.nb_add(s2, buff=0.4)
            self.sync(tr, text, "The k component")
            self.play(Indicate(s2[1], color=C_WRONG), run_time=0.8)
            self.strike(s2[1], owner=s2)
        self.rest()

        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.nb_add(s3a, buff=0.2)
            self.sync(tr, text, "Remove the brackets")
            self.play(Indicate(s3a[1], color=C_WRONG), run_time=0.8)
            self.nb_add(s3b, buff=0.2, gray=False)
            self.play(Indicate(s3b[1], color=C_WRONG), run_time=0.8)
            self.sync(tr, text, "Everything together")
            self.nb_add(s3c, buff=0.4, gray=False)
        self.rest()

        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(VGroup(s4, s4_box))
            self.sync(tr, text, "Now it is your turn")
            self.your_turn([r"1)\ \ compute this integral", r"2)\ \ check: is it negative?",
                            r"3)\ \ compare with your Riemann sum from the table"])
        self.wait(3)

        # 13 — summary
        self.summary(
            vo[13],
            [r"A line integral can be negative when $f < 0$ on the curve.",
             r"A constant component of $\mathbf r(t)$ disappears in $\mathbf r'(t)$.",
             r"Simplify $f(\mathbf r(t))$ carefully — watch the minus signs."],
            ["One:", "Two:", "Three:"],
        )


# ---------------------------------------------------------------------------
# Exercise 14 (worked):  int_C sqrt(3)/(x^2+y^2+z^2) ds,  r(t) = (t, t, t), 1 <= t < inf  ->  1
# ---------------------------------------------------------------------------
VO["ex14"] = [
    "Exercise fourteen. Find the line integral of f equals square root of three, divided by x squared plus y "
    "squared plus z squared, over the curve r of t equals t i plus t j plus t k, for t from one to infinity.",
    "Something new here: the curve is infinitely long. Can an integral over an infinite curve still give a "
    "finite number? Let's find out.",
    "Chapter one: the curve. All three coordinates are equal to t. So the curve is a straight ray. It starts at "
    "the point one, one, one, and runs away from the origin forever, in the diagonal direction one, one, one.",
    "Chapter two: the function. x squared plus y squared plus z squared is the squared distance to the origin. "
    "So f equals square root of three, divided by the distance squared. The further we go, the smaller f "
    "becomes. This is an inverse square law, just like gravity, or the electric field of a point charge.",
    "For a curve in space, the wall picture does not work well. Instead, think of the curve as a wire, and of f "
    "as its density. Bright and thick means a large density. The line integral is then the total mass of the "
    "wire.",
    "Pause and think: the wire is infinitely long. Can its total mass be finite?",
    "Chapter three: the formal method. Step one: the parametrisation is already given. r of t equals t i plus t "
    "j plus t k, for t from one to infinity.",
    "Step two: r prime of t equals i plus j plus k. Its length is the square root of one plus one plus one, "
    "which is square root of three. So d s equals square root of three, d t. Moving one unit in t moves the "
    "point square root of three along the ray.",
    "Step three: on the curve, x squared plus y squared plus z squared equals t squared plus t squared plus t "
    "squared, which is three t squared. So f of r of t equals square root of three, over three t squared.",
    "Step four: multiply by the speed. Square root of three over three t squared, times square root of three, "
    "gives three over three t squared, which is simply one over t squared.",
    "So the line integral becomes the integral from one to infinity of one over t squared, d t. This is an "
    "improper integral, because the upper limit is infinity. We handle it with a limit: integrate up to b, and "
    "then let b go to infinity.",
    "Chapter four: watch the area under one over t squared. From one to two, the area is one half. Up to three, "
    "it is two thirds. Up to four, three quarters. Up to b, it is one minus one over b. However far we go, the "
    "area never passes one.",
    "Formally: the integral from one to b of one over t squared is minus one over t, evaluated from one to b. "
    "That gives one minus one over b. As b goes to infinity, one over b goes to zero. So the line integral "
    "equals one.",
    "Compare this with a function that decays more slowly, like one over t. Its area keeps growing without "
    "bound, like the natural logarithm of b. One over t squared decays fast enough. One over t does not.",
    "Summary. One: a line integral over an infinite curve is an improper integral, computed as a limit. Two: "
    "along this diagonal ray, d s equals square root of three, d t. Three: an infinitely long wire with an "
    "inverse square density can have a finite mass. Here it is exactly one.",
]


class Ex16_1_14(ExerciseScene):
    PHI, THETA = 70 * DEGREES, -45 * DEGREES

    def construct(self):
        vo = VO["ex14"]
        PHI, THETA = self.PHI, self.THETA
        U = 0.8
        axes = ThreeDAxes(x_range=[0, 5, 1], y_range=[0, 5, 1], z_range=[0, 5, 1],
                          x_length=5 * U, y_length=5 * U, z_length=5 * U, tips=False)

        def R(t):
            return axes.c2p(t, t, t)

        d_world, screen = axes.c2p(2.5, 2.5, 2.2), np.array([-3.4, -0.2, 0])
        self.start("16.1 — Exercise 14",
                   r"\int_C \frac{\sqrt3}{x^2+y^2+z^2}\,ds,\quad \mathbf r(t)=t\,\mathbf i+t\,\mathbf j+t\,\mathbf k,"
                   r"\ \ 1\le t<\infty",
                   phi=PHI, theta=THETA, frame_center=center_for(PHI, THETA, d_world, screen))
        ax_labels = VGroup(*[face_camera(MathTex(s, font_size=34), PHI, THETA).move_to(p) for s, p in
                             [("x", axes.c2p(5.5, 0, 0)), ("y", axes.c2p(0, 5.5, 0)), ("z", axes.c2p(0, 0, 5.5))]])
        f = lambda t: np.sqrt(3) / (3 * t * t)

        # 0
        self.add(axes, ax_labels)
        self.intro(vo[0])

        # 1 — question
        self.question_card(vo[1], r"Infinite curve $\to$ finite integral?", "Can an integral")

        # 2 — chapter 1: the ray
        self.chapter(1, "The curve")
        stub = DashedLine(axes.c2p(0, 0, 0), R(1), color=GRAY, stroke_width=3)
        ray = Line(R(1), R(4), color=C_CURVE, stroke_width=6)
        tail = VGroup(*[Line(R(4 + 0.2 * i), R(4.2 + 0.2 * i), color=C_CURVE, stroke_width=6,
                             stroke_opacity=1 - (i + 1) / 7) for i in range(6)])
        inf = MathTex(r"\to\infty", font_size=34, color=C_CURVE)
        start_lab = MathTex("(1,1,1)", font_size=28)
        t = ValueTracker(1.0)
        dot = Dot3D(R(1), radius=0.08, color=WHITE)
        dot.add_updater(lambda m: m.move_to(R(t.get_value())))
        t_num = DecimalNumber(1, num_decimal_places=2, font_size=32)
        t_num.add_updater(lambda m: m.set_value(t.get_value()))
        t_lab = VGroup(MathTex("t =", font_size=32), t_num).arrange(RIGHT, buff=0.12).move_to([-5.8, 3.4, 0])
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.nb_add(MathTex(r"x=y=z=t,\quad 1\le t<\infty", font_size=34))
            self.sync(tr, text, "It starts")
            inf.move_to(self.to_screen(R(5.4)) + np.array([0.3, 0.1, 0]))
            start_lab.move_to(self.to_screen(R(1)) + np.array([0.75, -0.1, 0]))
            self.fixed(inf, start_lab, t_lab)
            self.play(Create(stub), FadeIn(dot), FadeIn(start_lab), FadeIn(t_lab), run_time=1.0)
            self.sync(tr, text, "and runs away")
            self.play(Create(ray), t.animate.set_value(4), run_time=3.0, rate_func=linear)
            self.play(FadeIn(tail), FadeIn(inf), run_time=1.0)
        self.rest()

        # 3 — chapter 2: f = sqrt3 / d^2
        self.chapter(2, "The function")
        dist = always_redraw(lambda: DashedLine(axes.c2p(0, 0, 0), R(t.get_value()), color=C_F, stroke_width=3))
        d_lab = MathTex("d", font_size=34, color=C_F)
        d_lab.add_updater(lambda m: m.move_to(self.to_screen(R(t.get_value() / 2)) + np.array([0.0, 0.3, 0])))
        self.fixed(d_lab)
        eq_d = MathTex(r"x^2+y^2+z^2 = d^2,\qquad f=\frac{\sqrt3}{d^2}", font_size=34)
        law = Tex("inverse square law (gravity, point charge)", font_size=30, color=GRAY_B)
        text = vo[3]
        with self.voiceover(text=text) as tr:
            t.set_value(2.0)
            self.play(Create(dist), FadeIn(d_lab), run_time=1.0)
            self.sync(tr, text, "is the squared distance")
            self.nb_add(eq_d)
            self.sync(tr, text, "The further")
            self.play(t.animate.set_value(4), run_time=2.0)
            self.sync(tr, text, "This is an inverse")
            self.nb_add(law, gray=False)
        self.play(Indicate(eq_d))
        self.rest()
        dist.clear_updaters()
        d_lab.clear_updaters()
        self.play(FadeOut(dist), FadeOut(d_lab), FadeOut(t_lab), run_time=0.5)

        # 4 — the wire with density f
        n = 48
        ts = np.linspace(1, 5.2, n + 1)
        wire = VGroup()
        for a, b in zip(ts[:-1], ts[1:]):
            q = f((a + b) / 2) / f(1)
            wire.add(Line(R(a), R(b), stroke_width=2 + 12 * q,
                          color=interpolate_color(ManimColor("#3a3000"), YELLOW, q ** 0.6)))
        wire_txt = Tex(r"wire with density $f$ $\to$ integral = total mass", font_size=30, color=C_F)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Instead, think")
            self.play(FadeOut(ray), FadeOut(tail), FadeIn(wire), run_time=1.5)
            self.sync(tr, text, "The line integral")
            self.nb_add(wire_txt)
        self.rest()

        # 5 — pause
        self.pause(vo[5], r"Infinitely long wire — can its mass be finite?")

        # 6-9 — chapter 3: the formal method
        self.nb_clear()
        self.chapter(3, "The formal method")
        self.show_checklist()
        s1 = MathTex(r"1.\ \ \mathbf r(t)=t\,\mathbf i+t\,\mathbf j+t\,\mathbf k,\quad 1\le t<\infty", font_size=32)
        s2 = MathTex(r"2.\ \ \mathbf r'(t)=\mathbf i+\mathbf j+\mathbf k,\ \ "
                     r"\lvert\mathbf r'(t)\rvert=\sqrt{1+1+1}=\sqrt3", font_size=32)
        s2b = MathTex(r"ds=\sqrt3\,dt", font_size=34)
        s3 = MathTex(r"3.\ \ x^2+y^2+z^2=t^2+t^2+t^2=3t^2", r"\ \Rightarrow\ f(\mathbf r(t))=\frac{\sqrt3}{3t^2}",
                     font_size=32)
        s4 = MathTex(r"4.\ \ ", r"\frac{\sqrt3}{3t^2}\cdot\sqrt3", r"=\frac{3}{3t^2}=\frac{1}{t^2}", font_size=34)

        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.sync(tr, text, "Step one")
            self.nb_add(s1, buff=0.4)
        self.rest()

        pa, pb = self.to_screen(R(1)), self.to_screen(R(2))
        perp = rotate_vector(normalize(pb - pa), PI / 2)   # away from the (1,1,1) label
        sbr = BraceBetweenPoints(pa, pb, direction=perp, color=C_DS)
        sbr_lab = MathTex(r"\Delta s = \sqrt3 \approx 1.73", font_size=28, color=C_DS)
        sbr_lab.next_to(sbr.get_center(), perp, buff=0.35)
        dt_lab = MathTex(r"\Delta t = 1", font_size=28, color=C_DT).next_to(sbr_lab, UP, buff=0.12)
        self.fixed(sbr, sbr_lab, dt_lab)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            self.nb_add(s2, buff=0.3)
            self.sync(tr, text, "So d s equals")
            self.nb_add(s2b, buff=0.4, gray=False)
            self.sync(tr, text, "Moving one unit")
            self.play(FadeIn(sbr), FadeIn(sbr_lab), FadeIn(dt_lab), run_time=1.0)
        self.play(Indicate(s2b))
        self.rest()

        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.play(FadeOut(VGroup(sbr, sbr_lab, dt_lab)), run_time=0.4)
            self.nb_add(s3, buff=0.4)
        self.rest()

        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(s4, buff=0.4)
            self.sync(tr, text, "times square root")
            self.play(Indicate(s4[1]), run_time=1.0)
        self.rest()

        # 10 — improper integral + switch to a 2D graph
        imp = MathTex(r"\int_C f\,ds=\int_1^\infty \frac{dt}{t^2}=\lim_{b\to\infty}\int_1^b\frac{dt}{t^2}",
                      font_size=34)
        ov = self.left_overlay()
        ax2 = Axes(x_range=[0, 10.5, 1], y_range=[0, 1.15, 0.5], x_length=6.0, y_length=4.2, tips=False,
                   x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5, 10], "font_size": 22},
                   y_axis_config={"numbers_to_include": [0.5, 1], "font_size": 22})
        ax2.move_to([-3.6, 0.3, 0])
        g2 = ax2.plot(lambda x: 1 / x ** 2, x_range=[1, 10], color=C_F, stroke_width=4)
        g_lab = MathTex(r"y=\frac1{t^2}", font_size=30, color=C_F).move_to(ax2.c2p(2.6, 0.55))
        t_ax = MathTex("t", font_size=30).next_to(ax2.x_axis, RIGHT, buff=0.1)
        self.fixed(ax2, g2, g_lab, t_ax)
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.play(*[c.animate.set_color(WHITE) for c in self.checklist], run_time=0.4)
            self.nb_add(imp)
            self.sync(tr, text, "We handle it")
            self.play(FadeIn(ov), run_time=0.6)
            self.play(Create(ax2), FadeIn(t_ax), run_time=1.0)
            self.play(Create(g2), FadeIn(g_lab), run_time=1.2)
        self.rest()

        # 11 — chapter 4: the area creeps up to 1
        self.chapter(4, "The area")
        b = ValueTracker(1.001)
        area = always_redraw(lambda: ax2.get_area(g2, x_range=[1, min(b.get_value(), 10)], color=C_F, opacity=0.4))
        b_line = always_redraw(lambda: DashedLine(ax2.c2p(min(b.get_value(), 10), 0),
                                                  ax2.c2p(min(b.get_value(), 10), 1.05), color=GRAY, stroke_width=2))
        self.fixed(area, b_line)
        frac = MathTex(r"\text{area} = \tfrac12", font_size=34).move_to([-3.6, -2.6, 0])
        b_num = DecimalNumber(4, num_decimal_places=0, font_size=32)
        a_num = DecimalNumber(0.75, num_decimal_places=3, font_size=32)
        b_num.add_updater(lambda m: m.set_value(b.get_value()))
        a_num.add_updater(lambda m: m.set_value(1 - 1 / b.get_value()))
        live = VGroup(MathTex("b =", font_size=32), b_num, MathTex(r",\quad \text{area} = 1-\tfrac1b =", font_size=32),
                      a_num).arrange(RIGHT, buff=0.12).move_to([-3.6, -2.6, 0])
        bar_frame = Rectangle(width=0.35, height=3.0, stroke_color=GRAY, stroke_width=1.5).move_to([0.25, 0.3, 0])
        bar_fill = Rectangle(width=0.35, height=0.01, fill_color=C_F, fill_opacity=0.8, stroke_width=0)
        bar_fill.add_updater(lambda m: m.stretch_to_fit_height(max(3.0 * (1 - 1 / b.get_value()), 1e-3))
                             .align_to(bar_frame, DOWN).set_x(bar_frame.get_x()))
        one_line = DashedLine(bar_frame.get_corner(UL) + LEFT * 0.15, bar_frame.get_corner(UR) + RIGHT * 0.15,
                              color=WHITE, stroke_width=2)
        one_lab = MathTex("1", font_size=28).next_to(one_line, UP, buff=0.08)
        self.fixed(frac, live, bar_frame, bar_fill, one_line, one_lab)
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(bar_frame), FadeIn(one_line), FadeIn(one_lab), FadeIn(bar_fill), FadeIn(area),
                      FadeIn(b_line), run_time=0.6)
            for ph, val, tex in [("From one to two", 2, r"\tfrac12"), ("Up to three", 3, r"\tfrac23"),
                                 ("Up to four", 4, r"\tfrac34")]:
                self.sync(tr, text, ph)
                new = MathTex(r"\text{area}\ \text{from 1 to } %d = %s" % (val, tex), font_size=34).move_to(frac)
                if val == 2:
                    self.fixed(new)
                self.play(b.animate.set_value(val), (FadeIn(new) if val == 2 else Transform(frac, new)),
                          run_time=1.2)
                if val == 2:
                    frac = new
            self.sync(tr, text, "Up to b")
            self.play(FadeOut(frac), FadeIn(live), run_time=0.6)
            self.play(b.animate.set_value(30), run_time=5.0, rate_func=rate_functions.ease_in_out_sine)
        self.rest()

        # 12 — formal evaluation
        ev = MathTex(r"\int_1^b\frac{dt}{t^2}=\Big[-\frac1t\Big]_1^b=1-\frac1b\ \xrightarrow{\,b\to\infty\,}\ 1",
                     font_size=34)
        ans = MathTex(r"\int_C f\,ds = 1", font_size=38)
        ans_box = SurroundingRectangle(ans, color=C_ANSWER, buff=0.15)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.nb_add(ev)
            self.sync(tr, text, "So the line integral")
            self.nb_add(VGroup(ans, ans_box))
        self.play(Indicate(ans))
        self.rest()

        # 13 — compare with 1/t
        g3 = DashedVMobject(ax2.plot(lambda x: 1 / x, x_range=[1, 10], color=C_DT, stroke_width=4), num_dashes=40)
        g3_lab = MathTex(r"y=\frac1t", font_size=30, color=C_DT).move_to(ax2.c2p(6.5, 0.32))
        c = ValueTracker(1.001)
        ln_num = DecimalNumber(0, num_decimal_places=2, font_size=32, color=C_DT)
        ln_num.add_updater(lambda m: m.set_value(np.log(c.get_value())))
        ln_live = VGroup(MathTex(r"\int_1^b\frac{dt}{t} = \ln b =", font_size=32, color=C_DT), ln_num,
                         MathTex(r"\to\infty", font_size=32, color=C_DT)).arrange(RIGHT, buff=0.12)
        ln_live.move_to([-3.6, -3.4, 0])
        cmp_txt = Tex(r"$1/t^2$ decays fast enough — $1/t$ does not", font_size=32)
        self.fixed(g3, g3_lab, *ln_live)
        text = vo[13]
        with self.voiceover(text=text) as tr:
            self.play(Create(g3), FadeIn(g3_lab), run_time=1.5)
            self.sync(tr, text, "Its area keeps")
            self.play(FadeIn(ln_live[0]), FadeIn(ln_num), run_time=0.5)
            self.play(c.animate.set_value(30), run_time=3.0)
            self.play(FadeIn(ln_live[2]), run_time=0.4)
            self.sync(tr, text, "One over t squared decays")
            self.nb_add(cmp_txt, gray=False)
        self.rest()

        # 14 — summary
        self.summary(
            vo[14],
            [r"A line integral over an infinite curve is an improper integral: a limit.",
             r"Along the diagonal ray, $ds = \sqrt3\,dt$.",
             r"Infinite wire, inverse-square density: finite mass (here exactly $1$)."],
            ["One:", "Two:", "Three:"],
        )


# ---------------------------------------------------------------------------
# Exercise 15 (HW):  int_C (x + sqrt(y) - z^2) ds,  C = C1 u C2
#   C1: r = t i + t^2 j,  C2: r = i + j + t k,  0 <= t <= 1
#   HW -> stop at the two set-up integrals, never show values.
# ---------------------------------------------------------------------------
C_C2 = TEAL

VO["ex15"] = [
    "Exercise fifteen. Integrate f equals x plus the square root of y, minus z squared, over the path from zero, "
    "zero, zero, to one, one, one. The path consists of two pieces: C one and C two.",
    "C one is a parabola in the x y plane: r of t equals t i plus t squared j, from the origin to the point one, "
    "one, zero. C two is a vertical segment: r of t equals i plus j plus t k, from one, one, zero, straight up to "
    "one, one, one.",
    "The key rule: a line integral over a path made of pieces is the sum of the line integrals over the pieces. "
    "So we handle C one and C two separately, and add the results.",
    "Chapter one: the parabola. Watch the points for t equals zero, a quarter, a half, three quarters, and one. "
    "The steps in t are equal, but the pieces of curve are not. They get longer as the parabola gets steeper. "
    "The speed is not constant.",
    "r prime of t equals i plus two t j. Its length is the square root of one plus four t squared. At t equals "
    "zero the speed is one. At t equals one it is square root of five, about two point two four. So d s equals "
    "the square root of one plus four t squared, d t.",
    "Chapter two: the function on the parabola. Here x equals t, y equals t squared, and z equals zero. Pause "
    "and think: what is the square root of t squared?",
    "In general, the square root of t squared is the absolute value of t. But on this piece, t runs from zero to "
    "one, so t is never negative. That means the square root of t squared is just t. So f becomes t plus t minus "
    "zero, which is two t.",
    "Putting it together: the integral over C one is the integral from zero to one of two t, times the square "
    "root of one plus four t squared, d t. We park this result for now.",
    "Chapter three: the vertical segment. r prime of t equals k, with length one. Here d s equals d t, because "
    "the point moves at unit speed.",
    "On C two, x equals one, y equals one, and z equals t. So f equals one, plus the square root of one, minus t "
    "squared. That is two minus t squared.",
    "The integral over C two is the integral from zero to one of two minus t squared, d t.",
    "Chapter four: the whole picture. Here is the complete path, unrolled onto the s axis. First the parabola, "
    "then the vertical segment. The line integral is the total shaded area under f.",
    "So the line integral over C equals the integral over C one, plus the integral over C two. Now it is your "
    "turn: compute both integrals, and add them. A tip for C one: look for a substitution that matches the "
    "derivative of what is under the square root.",
    "Summary. One: split a path into pieces, and add the integrals. Two: when the speed is not constant, d s "
    "changes along the curve. Three: the square root of t squared equals t only when t is not negative.",
]


def arc_parabola(t):
    """Arc length of (t, t^2) from 0 to t."""
    return t / 2 * np.sqrt(1 + 4 * t * t) + np.arcsinh(2 * t) / 4


class Ex16_1_15(ExerciseScene):
    PHI, THETA = 65 * DEGREES, -50 * DEGREES

    def construct(self):
        vo = VO["ex15"]
        PHI, THETA = self.PHI, self.THETA
        U = 2.3
        axes = ThreeDAxes(x_range=[0, 1.5, 0.5], y_range=[0, 1.5, 0.5], z_range=[0, 1.5, 0.5],
                          x_length=1.5 * U, y_length=1.5 * U, z_length=1.5 * U, tips=False)

        def P(x, y, z=0):
            return axes.c2p(x, y, z)

        d3, s3 = P(0.6, 0.6, 0.4), np.array([-3.5, -0.4, 0])
        c3 = center_for(PHI, THETA, d3, s3)
        d_top, s_top = P(0.5, 0.5, 0), np.array([-3.9, 0.9, 0])
        c_top = center_for(0, -PI / 2, d_top, s_top)

        problem = VGroup(
            MathTex(r"\int_C (x+\sqrt y - z^2)\,ds,\quad C=C_1\cup C_2", font_size=30),
            MathTex(r"C_1:\ \mathbf r=t\,\mathbf i+t^2\,\mathbf j,\qquad C_2:\ \mathbf r=\mathbf i+\mathbf j+t\,\mathbf k",
                    font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        self.start("16.1 — Exercise 15 (HW)", problem, phi=PHI, theta=THETA, frame_center=c3)
        ax_labels = VGroup(*[face_camera(MathTex(s, font_size=34), PHI, THETA).move_to(p) for s, p in
                             [("x", P(1.7, 0, 0)), ("y", P(0, 1.7, 0)), ("z", P(0, 0, 1.7))]])
        C1 = ParametricFunction(lambda t: P(t, t * t, 0), t_range=[0, 1], color=C_CURVE, stroke_width=6)
        C2 = Line(P(1, 1, 0), P(1, 1, 1), color=C_C2, stroke_width=6)

        def path(u):
            return P(u, u * u, 0) if u <= 1 else P(1, 1, u - 1)

        # 0
        self.add(axes, ax_labels)
        self.intro(vo[0])

        # 1 — the two pieces
        u = ValueTracker(0.0)
        dot = Dot3D(P(0, 0, 0), radius=0.07, color=WHITE)
        dot.add_updater(lambda m: m.move_to(path(u.get_value())))
        l1 = MathTex("C_1", font_size=34, color=C_CURVE).move_to(self.to_screen(P(0.55, 0.3, 0)) + np.array([0.3, -0.3, 0]))
        l2 = MathTex("C_2", font_size=34, color=C_C2).move_to(self.to_screen(P(1, 1, 0.5)) + np.array([0.45, 0, 0]))
        self.fixed(l1, l2)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Create(C1), FadeIn(l1), run_time=1.5)
            self.sync(tr, text, "C two is")
            self.play(Create(C2), FadeIn(l2), run_time=1.2)
            self.add(dot)
            self.play(u.animate.set_value(2), run_time=4.0, rate_func=linear)
        self.rest()
        self.play(FadeOut(dot), run_time=0.4)

        # 2 — split rule
        split = MathTex(r"\int_C f\,ds=", r"\int_{C_1} f\,ds", r"+", r"\int_{C_2} f\,ds", font_size=36)
        split[1].set_color(C_CURVE)
        split[3].set_color(C_C2)
        split_txt = Tex("split the path, add the pieces", font_size=30, color=GRAY_B)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.nb_add(split)
            self.sync(tr, text, "So we handle")
            self.nb_add(split_txt, gray=False)
        self.play(Indicate(split))
        self.rest()

        # 3 — chapter 1: the parabola, from above
        self.nb_clear()
        self.chapter(1, "Piece 1: the parabola")
        self.move_camera(phi=0, theta=-PI / 2, frame_center=c_top,
                         added_anims=[FadeOut(C2), FadeOut(l2), FadeOut(l1), FadeOut(axes.z_axis),
                                      FadeOut(ax_labels[2])], run_time=1.8)
        ax_labels[:2].set_opacity(0)
        top_labels = VGroup(MathTex("x", font_size=30).next_to(P(1.5, 0), RIGHT, buff=0.15),
                            MathTex("y", font_size=30).next_to(P(0, 1.5), UP, buff=0.15),
                            MathTex("1", font_size=24).next_to(P(1, 0), DOWN, buff=0.15),
                            MathTex("1", font_size=24).next_to(P(0, 1), LEFT, buff=0.15))
        self.play(FadeIn(top_labels), run_time=0.4)
        q = [0, 0.25, 0.5, 0.75, 1]
        qdots = VGroup(*[Dot(P(a, a * a), radius=0.07, color=WHITE) for a in q])
        lens = [arc_parabola(b) - arc_parabola(a) for a, b in zip(q[:-1], q[1:])]
        cbraces, clabs = VGroup(), VGroup()
        for (a, b), L in zip(zip(q[:-1], q[1:]), lens):
            pa, pb = P(a, a * a), P(b, b * b)
            perp = rotate_vector(normalize(pb - pa), -PI / 2)
            br = BraceBetweenPoints(pa, pb, direction=perp, color=C_DS)
            cbraces.add(br)
            clabs.add(MathTex(f"{L:.2f}", font_size=26, color=C_DS).next_to(br.get_center(), perp, buff=0.3))
        nl = NumberLine(x_range=[0, 1, 0.25], length=U, color=C_DT, tick_size=0.08)
        nl.shift(np.array([-5.0, -2.75, 0]) - nl.n2p(0))
        nl_name = MathTex("t", font_size=32, color=C_DT).next_to(nl, LEFT, buff=0.3)
        tbraces = VGroup(*[Brace(Line(nl.n2p(a), nl.n2p(b)), direction=UP, color=C_DT, buff=0.04)
                           for a, b in zip(q[:-1], q[1:])])
        tlabs = VGroup(*[MathTex(r"\tfrac14", font_size=22, color=C_DT).next_to(br, UP, buff=0.05)
                         for br in tbraces])
        self.fixed(nl, nl_name, tbraces, tlabs)
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Watch the points")
            self.play(LaggedStart(*[FadeIn(d) for d in qdots], lag_ratio=0.3), run_time=2.0)
            self.play(Create(nl), FadeIn(nl_name), FadeIn(tbraces), FadeIn(tlabs), run_time=1.0)
            self.sync(tr, text, "but the pieces")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b), FadeIn(l)) for b, l in zip(cbraces, clabs)],
                                  lag_ratio=0.4), run_time=2.5)
        self.rest()

        # 4 — speed sqrt(1+4t^2), speedometer
        sp1 = MathTex(r"\mathbf r'(t)=\mathbf i+2t\,\mathbf j,\quad \lvert\mathbf r'(t)\rvert=\sqrt{1+4t^2}",
                      font_size=34)
        sp2 = MathTex(r"ds=\sqrt{1+4t^2}\,dt", font_size=34)
        t = ValueTracker(0.0)
        dot2 = Dot(P(0, 0), radius=0.08, color=WHITE)
        dot2.add_updater(lambda m: m.move_to(P(t.get_value(), t.get_value() ** 2)))
        meter_w = 2.6
        meter_frame = Rectangle(width=meter_w, height=0.25, stroke_color=GRAY, stroke_width=1.5)
        meter_frame.move_to([-4.3 + meter_w / 2 - 1.3 + 1.3, -3.55, 0])
        meter_fill = Rectangle(width=0.01, height=0.25, fill_color=C_DS, fill_opacity=0.85, stroke_width=0)
        meter_fill.add_updater(lambda m: m.stretch_to_fit_width(
            meter_w * np.sqrt(1 + 4 * t.get_value() ** 2) / np.sqrt(5)).align_to(meter_frame, LEFT)
            .set_y(meter_frame.get_y()))
        sp_num = DecimalNumber(1, num_decimal_places=2, font_size=28, color=C_DS)
        sp_num.add_updater(lambda m: m.set_value(np.sqrt(1 + 4 * t.get_value() ** 2)).next_to(meter_frame, RIGHT,
                                                                                               buff=0.15))
        sp_name = Tex("speed", font_size=28).next_to(meter_frame, LEFT, buff=0.2)
        self.fixed(meter_frame, meter_fill, sp_num, sp_name)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.nb_add(sp1)
            self.sync(tr, text, "At t equals zero")
            self.play(FadeIn(meter_frame), FadeIn(meter_fill), FadeIn(sp_num), FadeIn(sp_name), FadeIn(dot2),
                      run_time=0.6)
            self.sync(tr, text, "At t equals one it")
            self.play(t.animate.set_value(1), run_time=2.5)
            self.sync(tr, text, "So d s equals")
            self.nb_add(VGroup(sp2, SurroundingRectangle(sp2, color=YELLOW, buff=0.12)))
        self.play(Indicate(sp2))
        self.rest()

        # 5 — chapter 2: f on piece 1 + pause
        self.play(FadeOut(VGroup(cbraces, clabs, qdots)), run_time=0.5)
        self.nb_clear()
        self.chapter(2, "f on piece 1")
        on_c1 = MathTex(r"x=t,\ \ y=t^2,\ \ z=0", font_size=34)
        self.pause(vo[5], r"What is $\sqrt{t^2}$?",
                   before=lambda tr: (self.sync(tr, vo[5], "Here x equals"), self.nb_add(on_c1)))

        # 6 — sqrt(t^2) = |t| = t
        a1 = MathTex(r"\sqrt{t^2} = \lvert t\rvert", font_size=34)
        a2 = Tex(r"$t \ge 0$ on $C_1$ $\Rightarrow$ $\lvert t\rvert = t$", font_size=32, color=C_F)
        a3 = MathTex(r"f(\mathbf r(t)) = t + t - 0 = 2t", font_size=34)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_add(a1)
            self.sync(tr, text, "But on this piece")
            self.nb_add(a2)
            self.play(Indicate(nl, color=YELLOW), run_time=0.8)
            self.sync(tr, text, "So f becomes")
            self.nb_add(a3)
        self.play(Indicate(a3))
        self.rest()

        # 7 — integral over C1, parked
        i1 = MathTex(r"\int_{C_1} f\,ds=\int_0^1 2t\sqrt{1+4t^2}\,dt", font_size=34, color=C_CURVE)
        i1g = VGroup(i1, SurroundingRectangle(i1, color=C_CURVE, buff=0.12))
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.nb_add(i1g)
            self.sync(tr, text, "We park")
            self.nb_park(i1g)
        self.rest()

        # 8 — chapter 3: the vertical segment, back to 3D
        self.chapter(3, "Piece 2: the vertical segment")
        for m in (meter_fill, sp_num):
            m.clear_updaters()
        dot2.clear_updaters()
        self.move_camera(phi=PHI, theta=THETA, frame_center=c3, run_time=1.8,
                         added_anims=[FadeOut(VGroup(nl, nl_name, tbraces, tlabs, meter_frame, meter_fill, sp_num,
                                                     sp_name)), FadeOut(dot2), FadeOut(top_labels),
                                      FadeIn(axes.z_axis), FadeIn(C2), ax_labels.animate.set_opacity(1)])
        v1 = MathTex(r"\mathbf r'(t)=\mathbf k,\ \ \lvert\mathbf r'(t)\rvert=1,\ \ ds=dt", font_size=34)
        w = ValueTracker(0.0)
        dot3 = Dot3D(P(1, 1, 0), radius=0.07, color=WHITE)
        dot3.add_updater(lambda m: m.move_to(P(1, 1, w.get_value())))
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.add(dot3)
            self.play(w.animate.set_value(1), run_time=2.5, rate_func=linear)
            self.nb_add(v1)
        self.rest()

        # 9 — f on C2
        v2 = MathTex(r"x=1,\ y=1,\ z=t\ \Rightarrow\ f=1+\sqrt1-t^2=2-t^2", font_size=34)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.nb_add(v2)
        self.play(Indicate(v2))
        self.rest()

        # 10 — integral over C2, parked under C1
        i2 = MathTex(r"\int_{C_2} f\,ds=\int_0^1 (2-t^2)\,dt", font_size=34, color=C_C2)
        i2g = VGroup(i2, SurroundingRectangle(i2, color=C_C2, buff=0.12))
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.nb_add(i2g)
        self.rest(0.6)
        self.nb_park(i2g)
        self.play(FadeOut(dot3), run_time=0.3)

        # 11 — chapter 4: the whole path unrolled (no numbers on areas)
        self.chapter(4, "The whole picture")
        L1 = arc_parabola(1)
        ov = self.left_overlay()
        ax2 = Axes(x_range=[0, L1 + 1.15, 10], y_range=[0, 2.3, 10], x_length=6.0, y_length=3.6, tips=False)
        ax2.move_to([-3.6, -0.6, 0])
        ts = np.linspace(0, 1, 60)
        pts1 = [ax2.c2p(arc_parabola(tt), 2 * tt) for tt in ts]
        pts2 = [ax2.c2p(L1 + tt, 2 - tt * tt) for tt in ts]
        g1 = VMobject(color=C_CURVE, stroke_width=4).set_points_as_corners(pts1)
        g2 = VMobject(color=C_C2, stroke_width=4).set_points_as_corners(pts2)
        a1p = Polygon(ax2.c2p(0, 0), *pts1, ax2.c2p(L1, 0), stroke_width=0, fill_color=C_CURVE, fill_opacity=0.4)
        a2p = Polygon(ax2.c2p(L1, 0), *pts2, ax2.c2p(L1 + 1, 0), stroke_width=0, fill_color=C_C2, fill_opacity=0.4)
        sep = DashedLine(ax2.c2p(L1, 0), ax2.c2p(L1, 2.2), color=WHITE, stroke_width=2)
        under = VGroup(
            BraceBetweenPoints(ax2.c2p(0, 0), ax2.c2p(L1, 0), direction=DOWN, color=C_CURVE),
            BraceBetweenPoints(ax2.c2p(L1, 0), ax2.c2p(L1 + 1, 0), direction=DOWN, color=C_C2))
        under_l = VGroup(MathTex("C_1", font_size=30, color=C_CURVE).next_to(under[0], DOWN, buff=0.1),
                         MathTex("C_2", font_size=30, color=C_C2).next_to(under[1], DOWN, buff=0.1))
        names = VGroup(MathTex("s", font_size=30).next_to(ax2.x_axis, RIGHT, buff=0.1),
                       MathTex("f", font_size=30).next_to(ax2.y_axis, UP, buff=0.1))
        self.fixed(ax2, g1, g2, a1p, a2p, sep, under, under_l, names)
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(ov), run_time=0.5)
            self.play(Create(ax2), FadeIn(names), run_time=0.8)
            self.sync(tr, text, "First the parabola")
            self.play(Create(g1), FadeIn(under[0]), FadeIn(under_l[0]), run_time=1.2)
            self.sync(tr, text, "then the vertical")
            self.play(Create(sep), Create(g2), FadeIn(under[1]), FadeIn(under_l[1]), run_time=1.2)
            self.sync(tr, text, "The line integral is")
            self.play(FadeIn(a1p), FadeIn(a2p), run_time=1.2)
        self.rest()

        # 12 — final set-up + your turn
        fin = MathTex(r"\int_C f\,ds=", r"\int_0^1 2t\sqrt{1+4t^2}\,dt", r"+", r"\int_0^1(2-t^2)\,dt", font_size=34)
        fin[1].set_color(C_CURVE)
        fin[3].set_color(C_C2)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.nb_add(VGroup(fin, SurroundingRectangle(fin, color=YELLOW, buff=0.12)))
            self.sync(tr, text, "Now it is your turn")
            self.play(FadeOut(VGroup(ax2, g1, g2, a1p, a2p, sep, under, under_l, names)), run_time=0.5)
            self.your_turn([r"1)\ \ compute both integrals", r"2)\ \ add them",
                            r"Tip for $C_1$: substitution — look at what is under the square root"])
        self.wait(3)

        # 13 — summary
        self.summary(
            vo[13],
            [r"Split a path into pieces and add the integrals.",
             r"Non-constant speed $\Rightarrow$ $ds$ changes along the curve.",
             r"$\sqrt{t^2} = t$ only when $t \ge 0$ (in general $\sqrt{t^2}=\lvert t\rvert$)."],
            ["One:", "Two:", "Three:"],
        )
