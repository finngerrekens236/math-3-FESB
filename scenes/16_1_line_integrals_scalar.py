"""16.1 Line integrals of scalar functions (Thomas' Calculus, 13e ed.)

Running example:  C: r(t) = (2 cos t, 2 sin t), 0 <= t <= pi/2  (quarter circle)
                  f(x, y) = x y
                  int_C f ds = 4

Scenes (all with English voiceover, Kokoro af_heart):
  LineIntegralIdea         Riemann sum  sum f(P_k) ds_k  along the curve -> integral
  LineIntegralFence        3D: int_C f ds = area of the "fence" with height f above C
  LineIntegralComputation  step-by-step evaluation via parametrisation
  Ex16_1_09                Exercise 9: int_C (x+y) ds along (0,1) -> (1,0) = sqrt(2)

Voiceover text: edit the VO dict below.

Render (from repo root):
  .venv/Scripts/manim -ql scenes/16_1_line_integrals_scalar.py LineIntegralIdea
"""
from manim import *
from manim_voiceover import VoiceoverScene
from _tts import kokoro
import numpy as np

# --- render targets (python render.py <this file> <Scene>) -> videos/<path>.mp4
OUTPUT = {
    "LineIntegralIdea": "16.1 Line integrals (scalar)/Concept/1 - Idea (Riemann sum)",
    "LineIntegralFence": "16.1 Line integrals (scalar)/Concept/2 - Fence (area)",
    "LineIntegralComputation": "16.1 Line integrals (scalar)/Concept/3 - Computation",
    "Ex16_1_09": "16.1 Line integrals (scalar)/Exercises/Ex 09",
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
# Exercise 9:  int_C (x+y) ds,  C: x = t, y = 1 - t, z = 0,  0 <= t <= 1
#              f = 1 on C  ->  integral = length of C = sqrt(2)
# ===========================================================================
C_F = YELLOW      # f-values
C_DT = ORANGE     # delta t
# 3D view for the fence. theta = -115 deg looks almost straight at the fence;
# theta = -50 deg would look along the segment (fence edge-on).
PHI3, THETA3 = 65 * DEGREES, -115 * DEGREES
RX = 0.3          # left edge of the right-hand formula column

VO_EX09 = [
    "Exercise nine. We integrate f equals x plus y along the straight line segment C, "
    "from the point zero, one, to the point one, zero.",
    "Here is the segment. As t runs from zero to one, the point moves from zero, one, down to one, zero.",
    "Before any formula, look at the function on the curve. At every point of this segment, "
    "x plus y equals one. So on C, f is simply one.",
    "Now picture the fence above the curve. Its height is f, which is one everywhere. "
    "So the fence is just a rectangle.",
    "The area of a rectangle is height times length. The length of the segment follows from "
    "Pythagoras: the square root of one squared plus one squared, which is the square root of two. "
    "So we expect the answer: square root of two.",
    "Here is the key idea. The parameter t only runs from zero to one, but the curve is longer than that. "
    "Every step of a quarter in t moves the point about zero point three five along the curve. "
    "That stretch factor is the square root of two: the speed, the length of r prime of t. "
    "That is why d s equals square root of two, times d t.",
    "Now the formal method. Step one: parametrise the curve. r of t equals t i, plus one minus t, j.",
    "Step two: differentiate. r prime of t equals i minus j. Its length is the square root of two.",
    "Step three: substitute the curve into f. x plus y becomes t plus one minus t, which is one.",
    "Step four: integrate. The integral from zero to one of one times square root of two, d t, "
    "gives square root of two.",
    "The same answer as the fence. When f equals one, the line integral is simply the length of the curve.",
]


def cam_matrix(phi, theta, gamma=0.0):
    """World -> camera rotation, identical to ManimCE ThreeDCamera.generate_rotation_matrix."""
    return rotation_about_z(gamma) @ rotation_matrix(-phi, RIGHT) @ rotation_about_z(-theta - PI / 2)


class Ex16_1_09(VoiceoverScene, ThreeDScene):
    def fixed(self, *mobs):
        """Register as fixed-in-frame but keep invisible until animated in."""
        self.add_fixed_in_frame_mobjects(*mobs)
        self.remove(*mobs)

    def column(self, mobs, top, buff=0.35):
        grp = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=buff)
        grp.shift(np.array([RX - grp.get_left()[0], top - grp.get_top()[1], 0]))
        return grp

    def construct(self):
        self.set_speech_service(kokoro())
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        vo = VO_EX09
        M3 = cam_matrix(PHI3, THETA3)

        def to_world(v):
            """Screen offset in the 3D view -> world vector."""
            return M3.T @ np.array(v, dtype=float)

        # ---- drawing (left) ------------------------------------------------
        axes = ThreeDAxes(
            x_range=[0, 1.5, 0.5], y_range=[0, 1.5, 0.5], z_range=[0, 1.5, 0.5],
            x_length=3.6, y_length=3.6, z_length=3.6, tips=False,
        )
        axes.shift(np.array([-5.0, -1.7, 0]) - axes.c2p(0, 0, 0))

        def P(x, y, z=0):
            return axes.c2p(x, y, z)

        z_axis = axes.z_axis          # only shown in 3D (perspective draws it as a stray line from above)
        axes_grp = VGroup(
            axes.x_axis, axes.y_axis,
            MathTex("x", font_size=30).next_to(P(1.5, 0), RIGHT, buff=0.15),
            MathTex("y", font_size=30).next_to(P(0, 1.5), UP, buff=0.15),
            MathTex("1", font_size=24).next_to(P(1, 0), DOWN, buff=0.15),
            MathTex("1", font_size=24).next_to(P(0, 1), LEFT, buff=0.15),
        )
        seg = Line(P(0, 1), P(1, 0), color=C_CURVE, stroke_width=6)

        # ---- header + checklist (fixed) --------------------------------------
        title = Text("16.1 — Exercise 9", font_size=34)
        prob1 = MathTex(r"\int_C (x+y)\,ds", font_size=38)
        prob2 = MathTex(r"C:\ x=t,\ y=1-t,\ z=0,\quad (0,1,0)\to(1,0,0)", font_size=30)
        header = self.column([title, prob1, prob2], top=3.7, buff=0.2)

        items = ["parametrise", r"$\lvert\mathbf r'(t)\rvert$", r"$f(\mathbf r(t))$", "integrate"]
        checklist = VGroup(*[Tex(f"{i + 1}\\ \\ {s}", font_size=26) for i, s in enumerate(items)])
        checklist.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.3).set_color(GRAY_B)
        self.fixed(header, checklist)

        # ---- 0: title + exercise ---------------------------------------------
        with self.voiceover(text=vo[0]) as tr:
            d = tr.duration
            self.play(Write(title), run_time=d * 0.25)
            self.play(Write(prob1), Write(prob2), run_time=d * 0.5)
            self.play(FadeIn(checklist), run_time=tr.get_remaining_duration())

        # ---- 1: the segment, moving point --------------------------------------
        t = ValueTracker(0.0)
        dot = Dot(P(0, 1), color=WHITE)
        dot.add_updater(lambda m: m.move_to(P(t.get_value(), 1 - t.get_value())))
        t_num = DecimalNumber(0, num_decimal_places=2, font_size=30)
        t_lab = VGroup(MathTex("t =", font_size=30), t_num).arrange(RIGHT, buff=0.12)
        t_lab.move_to(P(1.2, 1.4))
        t_num.add_updater(lambda m: m.set_value(t.get_value()))

        with self.voiceover(text=vo[1]) as tr:
            d = tr.duration
            self.play(Create(axes_grp), run_time=d * 0.3)
            self.play(Create(seg), FadeIn(dot), FadeIn(t_lab), run_time=d * 0.2)
            self.play(t.animate.set_value(1), run_time=tr.get_remaining_duration(), rate_func=linear)
        self.wait(1)

        # ---- 2: f on the curve is 1 -------------------------------------------
        vals = [(0, "0", "1"), (0.25, "0.25", "0.75"), (0.5, "0.5", "0.5"), (0.75, "0.75", "0.25"), (1, "1", "0")]
        marks = VGroup(*[Dot(P(a, 1 - a), radius=0.06, color=C_F) for a, _, _ in vals])
        vlabels = VGroup(*[
            MathTex(f"{xs} + {ys} = 1", font_size=24, color=C_F).next_to(P(a, 1 - a), UR, buff=0.08)
            for a, xs, ys in vals
        ])
        f_on_C = MathTex(r"f\big|_C = x + y = 1", font_size=36, color=C_F)
        self.column([f_on_C], top=1.35)
        self.fixed(f_on_C)

        with self.voiceover(text=vo[2]) as tr:
            d = tr.duration
            self.play(FadeOut(dot), FadeOut(t_lab), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(VGroup(m, l)) for m, l in zip(marks, vlabels)], lag_ratio=0.3),
                      run_time=d * 0.55)
            self.play(Write(f_on_C), run_time=tr.get_remaining_duration())
        self.wait(1)

        # ---- 3: the fence (3D) -------------------------------------------------
        h = ValueTracker(0.001)
        fence = always_redraw(lambda: Polygon(
            P(0, 1, 0), P(1, 0, 0), P(1, 0, h.get_value()), P(0, 1, h.get_value()),
            color=C_F, fill_color=C_F, fill_opacity=0.5, stroke_width=2,
        ))

        def face_camera(mob):
            return mob.rotate(PI / 2, RIGHT).rotate(THETA3 + PI / 2, OUT)

        h_lab = face_camera(Tex("height = 1", font_size=30, color=C_F))
        h_lab.move_to(P(1, 0, 0.5) + to_world([1.1, 0, 0]))
        b_lab = face_camera(Tex("base = $C$", font_size=30, color=C_CURVE))
        b_lab.move_to(P(0.5, 0.5, 0) + to_world([0.5, -0.5, 0]))

        d_world = P(0.5, 0.5, 0.4)
        center3 = d_world - to_world([-3.6, -0.9, 0])   # drawing appears at screen (-3.6, -0.9)

        with self.voiceover(text=vo[3]) as tr:
            d = tr.duration
            self.move_camera(phi=PHI3, theta=THETA3, frame_center=center3,
                             added_anims=[FadeOut(marks), FadeOut(vlabels), FadeIn(z_axis)], run_time=d * 0.35)
            self.add(fence)
            self.play(h.animate.set_value(1), run_time=d * 0.35)
            self.play(FadeIn(h_lab), FadeIn(b_lab), run_time=tr.get_remaining_duration())
        fence.clear_updaters()
        self.wait(1)
        self.move_camera(phi=0, theta=-PI / 2, frame_center=ORIGIN,
                         added_anims=[FadeOut(fence), FadeOut(h_lab), FadeOut(b_lab), FadeOut(z_axis)], run_time=1.5)

        # ---- 4: Pythagoras -> expected answer ---------------------------------
        corner = P(1, 1)
        hline = DashedLine(P(0, 1), corner, color=WHITE)
        vline = DashedLine(corner, P(1, 0), color=WHITE)
        sq = Square(side_length=0.18, stroke_width=2, color=WHITE).move_to(corner + np.array([-0.09, -0.09, 0]))
        l1 = MathTex("1", font_size=28).next_to(hline, UP, buff=0.1)
        l2 = MathTex("1", font_size=28).next_to(vline, RIGHT, buff=0.1)
        L_lab = MathTex("L", font_size=32, color=C_CURVE).next_to(seg.get_center(), DL, buff=0.15)

        area = MathTex(r"\text{area} = \text{height}\times\text{length} = 1\cdot L", font_size=32)
        L_eq = MathTex(r"L = \sqrt{1^2+1^2} = \sqrt{2}", font_size=32)
        expect = Tex(r"Expected answer: $\sqrt{2}$", font_size=32, color=GREEN)
        insight = self.column([f_on_C.copy(), area, L_eq, expect], top=1.35)[1:]
        self.fixed(*insight)

        with self.voiceover(text=vo[4]) as tr:
            d = tr.duration
            self.play(Write(area), run_time=d * 0.25)
            self.play(Create(hline), Create(vline), Create(sq), FadeIn(l1), FadeIn(l2), FadeIn(L_lab),
                      run_time=d * 0.2)
            self.play(Write(L_eq), run_time=d * 0.3)
            self.play(FadeIn(expect), run_time=tr.get_remaining_duration())
        self.wait(1)

        # ---- 5: WHY |r'(t)|: delta s vs delta t -------------------------------
        unit = axes.x_axis.get_unit_size()
        nl = NumberLine(x_range=[0, 1, 0.25], length=unit, include_numbers=False, tick_size=0.08)
        nl.shift(np.array([P(0, 0)[0], -3.2, 0]) - nl.n2p(0))
        nl_nums = VGroup(*[MathTex(s, font_size=20).next_to(nl.n2p(v), DOWN, buff=0.12)
                           for v, s in [(0, "0"), (0.25, "0.25"), (0.5, "0.5"), (0.75, "0.75"), (1, "1")]])
        nl_name = MathTex("t", font_size=30).next_to(nl, LEFT, buff=0.3)
        t.set_value(0)
        nl_dot = Dot(nl.n2p(0), color=C_DT)
        nl_dot.add_updater(lambda m: m.move_to(nl.n2p(t.get_value())))
        dot.clear_updaters()
        dot.move_to(P(0, 1))
        dot.add_updater(lambda m: m.move_to(P(t.get_value(), 1 - t.get_value())))

        def piece(a, b):
            ln = Line(P(a, 1 - a), P(b, 1 - b))
            hl = Line(P(a, 1 - a), P(b, 1 - b), color=C_DS, stroke_width=10)
            sb = Brace(ln, direction=normalize(UR), color=C_DS, buff=0.05)
            tb = Brace(Line(nl.n2p(a), nl.n2p(b)), direction=UP, color=C_DT, buff=0.05)
            return hl, sb, tb

        hl, sb, tb = piece(0, 0.25)
        hls = VGroup(hl)
        s_txt = MathTex(r"\Delta s", font_size=28, color=C_DS)
        t_txt = MathTex(r"\Delta t", font_size=28, color=C_DT)
        s_txt.add_updater(lambda m: m.next_to(sb, UR, buff=0.02))
        t_txt.add_updater(lambda m: m.next_to(tb, UP, buff=0.05))

        cmp = MathTex(r"\Delta s = \tfrac{\sqrt2}{4} \approx 0.354", r"\quad\text{vs}\quad",
                      r"\Delta t = 0.25", font_size=32)
        cmp[0].set_color(C_DS)
        cmp[2].set_color(C_DT)
        ratio = MathTex(r"\frac{\Delta s}{\Delta t} = \sqrt{2} = \lvert\mathbf r'(t)\rvert"
                        r"\;\Rightarrow\; ds = \sqrt{2}\,dt", font_size=32)
        why = VGroup(cmp, ratio).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        why.shift(np.array([RX - why.get_left()[0], expect.get_bottom()[1] - 0.45 - why.get_top()[1], 0]))
        ratio_box = SurroundingRectangle(ratio, color=YELLOW, buff=0.12)
        self.fixed(cmp, ratio, ratio_box)

        with self.voiceover(text=vo[5]) as tr:
            d = tr.duration
            self.play(Create(nl), FadeIn(nl_nums), FadeIn(nl_name), FadeIn(dot), FadeIn(nl_dot),
                      run_time=d * 0.1)
            for k in range(4):
                a, b = k / 4, (k + 1) / 4
                if k == 0:
                    self.play(FadeIn(sb), FadeIn(tb), FadeIn(s_txt), FadeIn(t_txt), Create(hl),
                              t.animate.set_value(b), run_time=d * 0.13, rate_func=linear)
                    self.play(Write(cmp), run_time=d * 0.17)
                else:
                    new_hl, new_sb, new_tb = piece(a, b)
                    self.play(Transform(sb, new_sb), Transform(tb, new_tb), Create(new_hl),
                              t.animate.set_value(b), run_time=d * 0.1, rate_func=linear)
                    hls.add(new_hl)
            self.play(Write(ratio), run_time=d * 0.18)
            self.play(Create(ratio_box), run_time=tr.get_remaining_duration())
        self.wait(1)

        # ---- 6-9: the 4-step method -------------------------------------------
        s_tex = [
            r"1.\ \ \mathbf r(t) = t\,\mathbf i + (1-t)\,\mathbf j,\quad 0\le t\le 1",
            r"2.\ \ \mathbf r'(t) = \mathbf i - \mathbf j,\quad \lvert\mathbf r'(t)\rvert = \sqrt{1^2+(-1)^2} = \sqrt{2}",
            r"3.\ \ f(\mathbf r(t)) = t + (1-t) = 1",
            r"4.\ \ \int_C (x+y)\,ds = \int_0^1 1\cdot\sqrt{2}\,dt = \sqrt{2}",
        ]
        steps = self.column([MathTex(s, font_size=30) for s in s_tex], top=1.35, buff=0.45)
        ans_box = SurroundingRectangle(steps[3], color=GREEN, buff=0.12)
        self.fixed(*steps, ans_box)

        old = VGroup(f_on_C, *insight, cmp, ratio, ratio_box)
        self.play(FadeOut(old), FadeOut(sb), FadeOut(tb), FadeOut(s_txt), FadeOut(t_txt), FadeOut(hls),
                  run_time=0.8)
        for k in range(4):
            anims = [checklist[k].animate.set_color(YELLOW)]
            if k > 0:
                anims.append(checklist[k - 1].animate.set_color(WHITE))
            with self.voiceover(text=vo[6 + k]) as tr:
                self.play(*anims, run_time=0.5)
                if k == 3:
                    self.play(Write(steps[k]), run_time=tr.get_remaining_duration() * 0.7)
                    self.play(Create(ans_box), run_time=max(tr.get_remaining_duration(), 0.5))
                else:
                    self.play(Write(steps[k]), run_time=tr.get_remaining_duration())
            self.wait(1)

        # ---- 10: same answer as the fence ----------------------------------------
        final = MathTex(r"\text{fence area} = \sqrt2 \;=\; \int_C f\,ds \;\checkmark", font_size=36)
        final_txt = Tex(r"$f = 1 \;\Rightarrow\; \displaystyle\int_C ds = $ length of $C$", font_size=34,
                        color=C_F)
        end = self.column([final, final_txt], top=1.2, buff=0.5)
        self.fixed(*end)
        fence_final = Polygon(P(0, 1, 0), P(1, 0, 0), P(1, 0, 1), P(0, 1, 1),
                              color=C_F, fill_color=C_F, fill_opacity=0.5, stroke_width=2)
        dot.clear_updaters()
        nl_dot.clear_updaters()

        with self.voiceover(text=vo[10]) as tr:
            d = tr.duration
            self.move_camera(
                phi=PHI3, theta=THETA3, frame_center=center3, run_time=d * 0.4,
                added_anims=[FadeOut(VGroup(*steps, ans_box)),
                             FadeOut(VGroup(nl, nl_nums, nl_name, nl_dot, dot)),
                             FadeIn(fence_final), FadeIn(h_lab), FadeIn(b_lab), FadeIn(z_axis),
                             checklist.animate.set_color(WHITE)],
            )
            self.play(Write(final), run_time=d * 0.35)
            self.play(FadeIn(final_txt), run_time=tr.get_remaining_duration())
        self.wait(2)
