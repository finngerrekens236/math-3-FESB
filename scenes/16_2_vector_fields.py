"""16.2 Vector fields, work, circulation, flux (Thomas' Calculus, 13e ed.)

Concept videos (2D, FlatScene):
  VectorFieldsIntro     vector fields, drawing them, gradient fields
  WorkLineIntegral      work = int F.T ds = int F(r(t)).r'(t) dt   (running example: pi/2 - 1/2)
  FlowCirculationFlux   flow, circulation (2 pi), flux = oint M dy - N dx  (pi)

Exercises:
  Ex16_2_01  gradient of (x^2+y^2+z^2)^(-1/2)       (3D parts)
  Ex16_2_04  gradient of xy + yz + xz                (3D cube at the end)
  Ex16_2_12  F = grad(xy+yz+xz) along 3 paths -> 3  (3D)
  Ex16_2_25  int F.T ds, F = x^2 i - y j, x = y^2 from (4,2) to (1,-1) -> -39/2  (2D)
  Ex16_2_15  int (x^2+y^2) dy, (0,0)->(3,0)->(3,3) -> 36  (2D)

Voiceover text: VO dict below (literal from the task blocks).
Render: .venv/Scripts/python render.py scenes/16_2_vector_fields.py <Scene> [--low]
"""
from manim import *
import numpy as np

from _exercise import (FlatScene, ExerciseScene, center_for, face_camera, cam_matrix,
                       C_CURVE, C_F, C_NEG, C_DS, C_DT, C_ANSWER, C_WRONG, NB_LEFT, NB_RIGHT, NB_W,
                       LEFT_CENTER)

OUTPUT = {
    "VectorFieldsIntro": "16.2 Vector fields, work, circulation, flux/Concept/1 - Vector fields & gradient fields",
    "WorkLineIntegral": "16.2 Vector fields, work, circulation, flux/Concept/2 - Work (F dot dr)",
    "FlowCirculationFlux": "16.2 Vector fields, work, circulation, flux/Concept/3 - Flow, circulation, flux",
    "Ex16_2_01": "16.2 Vector fields, work, circulation, flux/Exercises/Ex 01",
    "Ex16_2_04": "16.2 Vector fields, work, circulation, flux/Exercises/Ex 04",
    "Ex16_2_12": "16.2 Vector fields, work, circulation, flux/Exercises/Ex 12",
    "Ex16_2_25": "16.2 Vector fields, work, circulation, flux/Exercises/Ex 25",
    "Ex16_2_15": "16.2 Vector fields, work, circulation, flux/Exercises/Ex 15",
}

C_T = YELLOW        # unit tangent T
C_FORCE = RED       # force arrows F_k
C_PROJ = GREEN      # tangential part F.T
C_NORMAL = PURPLE   # normal n, F.n
C_TEAL = TEAL

O = np.array([-3.3, 0.0, 0.0])     # origin of the 2D drawing area (1 unit = 1 scene unit)


def P2(x, y):
    return O + np.array([x, y, 0.0])


def field(func, length_func, step=0.75, half=2.625, **kw):
    """ArrowVectorField of a math field func(x, y) -> (u, v) on the left drawing area.
    Grid is offset from the origin (no zero/singular vector at O)."""
    def f(p):
        x, y = p[0] - O[0], p[1] - O[1]
        u, v = func(x, y)
        return np.array([u, v, 0.0])
    return ArrowVectorField(f, x_range=[O[0] - half, O[0] + half + 1e-3, step],
                            y_range=[-half, half + 1e-3, step], length_func=length_func, **kw)


def plane2d(rng=3):
    return NumberPlane(x_range=[-rng, rng, 1], y_range=[-rng, rng, 1], x_length=2 * rng, y_length=2 * rng,
                       background_line_style={"stroke_color": GRAY_D, "stroke_width": 1, "stroke_opacity": 0.6},
                       axis_config={"stroke_color": GRAY_B}).move_to(O)


def card_left(scene, content, color=YELLOW):
    """Rounded card over the drawing area (notebook stays visible)."""
    if content.width > 6.8:
        content.scale_to_fit_width(6.8)
    content.move_to(LEFT_CENTER)
    bg = RoundedRectangle(corner_radius=0.2, width=7.4, height=min(max(content.height + 1.0, 3.0), 7.6),
                          fill_color="#141414", fill_opacity=0.97, stroke_color=color, stroke_width=2)
    bg.move_to(LEFT_CENTER)
    grp = VGroup(bg, content)
    scene.fixed(grp)
    return grp


VO = {}

VO["intro1"] = [
    "Section sixteen point two is about vector fields, and about line integrals of vector fields. In this first video, we look at vector fields themselves: what they are, how to draw them, and one very important type, the gradient field.",
    "In section sixteen point one, we worked with a scalar function f. At every point, f gives one number, like a temperature. A vector field gives something richer at every point: a vector, with a direction and a magnitude.",
    "Think of the wind. At every point in the air, the wind has a direction and a speed. Or think of a force field, like gravity, or the magnetic field around a coil. In each case, every point gets its own arrow.",
    "We write a vector field in components. In the plane: F equals M of x y, i, plus N of x y, j. In space, a third component, P times k, is added. M, N and P are ordinary scalar functions.",
    "How do we draw a field? Pick a point, evaluate F there, and draw the arrow with its tail at that point. Take F equals x i plus y j. At the point one, two, F equals i plus two j. So we draw that arrow, starting at one, two.",
    "Repeat this on a grid of points, and the picture appears. This is the radial field: every arrow points away from the origin, and the arrows get longer further out.",
    "A different field: minus y i plus x j, divided by the distance to the origin. Every arrow now has length one, and the arrows circle around the origin, counterclockwise. This is a spin field, like water swirling around a drain.",
    "Pause and think: what happens if we swap the signs, and take y i minus x j?",
    "The arrows now circle clockwise. A single minus sign reverses the direction of rotation.",
    "Now a very important type of vector field. In section fourteen point five, you met the gradient of a function. The gradient points in the direction in which the function increases fastest. If we draw the gradient at every point, we get a vector field: the gradient field.",
    "Take a temperature T equals one hundred minus x squared minus y squared. It is hottest at the origin. The gradient is minus two x i, minus two y j. At every point, the arrow points towards the origin: the direction in which it gets warmer fastest.",
    "Notice two things. First, every arrow is perpendicular to the level curve through its point. Second, the arrows are longer where the level curves are closer together, where the temperature changes faster.",
    "In space it works the same way. For T equals one hundred minus x squared minus y squared minus z squared, the gradient field is minus two x i, minus two y j, minus two z k.",
    "So, to find a gradient field, you only need partial derivatives. For example, for f equals x y plus z squared: the x derivative is y, the y derivative is x, and the z derivative is two z. So the gradient field is y i plus x j plus two z k.",
    "This shows up everywhere in engineering. Heat flows from hot to cold, so opposite to the temperature gradient. And the electric field is minus the gradient of the voltage. Later in this chapter, gradient fields will turn out to be special: they are the conservative fields.",
    "Summary. One: a vector field assigns an arrow to every point, written as M i plus N j plus P k. Two: to draw it, evaluate F at a point and put the tail of the arrow there. Three: the gradient field of f is made of partial derivatives; it points uphill, and it is perpendicular to the level curves.",
]

CONCEPT_CHECK = ["1 vector fields", "2 gradient fields"]


# =============================================================================
class VectorFieldsIntro(FlatScene):
    def construct(self):
        vo = VO["intro1"]
        self.start("16.2 — Vector fields",
                   Tex(r"1 Vector fields $\cdot$ 2 Gradient fields", font_size=30, color=GRAY_B))

        # 0 — overview card
        boxes = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.15, width=3.2, height=1.4,
                                                 stroke_color=c, stroke_width=2), Tex(s, font_size=34))
                         for s, c in [("1 Vector fields", BLUE), ("2 Gradient fields", ORANGE)]])
        for b in boxes:
            b[1].move_to(b[0])
        boxes.arrange(RIGHT, buff=0.4).move_to(LEFT_CENTER)
        with self.voiceover(text=vo[0]) as tr:
            self.play(Write(self.title_mob), run_time=1.2)
            self.play(Write(self.problem_mob), run_time=1.5)
            self.sync(tr, vo[0], "In this first video")
            self.play(FadeIn(boxes[0], shift=UP * 0.2), run_time=0.8)
            self.sync(tr, vo[0], "the gradient field")
            self.play(FadeIn(boxes[1], shift=UP * 0.2), run_time=0.8)
        self.rest()
        self.play(FadeOut(boxes), run_time=0.5)

        # 1 — numbers morph into arrows
        self.chapter(1, "What is a vector field?")
        wind = lambda x, y: (1.0, 0.5 * np.sin(1.3 * x))
        pts = [(x, y) for x in np.arange(-2.25, 2.3, 1.5) for y in np.arange(-2.25, 2.3, 1.5)]
        nums, arrows = VGroup(), VGroup()
        for x, y in pts:
            val = 20 + 2 * x - y
            col = interpolate_color(BLUE, RED, (val - 14) / 12)
            nums.add(MathTex(f"{val:.0f}", font_size=30, color=col).move_to(P2(x, y)))
            u, v = wind(x, y)
            arrows.add(Arrow(P2(x, y), P2(x + 0.7 * u, y + 0.7 * v), buff=0, color=col,
                             stroke_width=4, max_tip_length_to_length_ratio=0.3))
        lab_f = Tex("scalar $f$: a number per point", font_size=30, color=GRAY_B).move_to(P2(0, 3.3))
        lab_F = Tex(r"vector field $\mathbf F$: an arrow per point", font_size=30, color=GRAY_B).move_to(P2(0, 3.3))
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "At every point, f")
            self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.03), FadeIn(lab_f), run_time=1.5)
            self.sync(tr, text, "A vector field")
            self.play(*[ReplacementTransform(n, a) for n, a in zip(nums, arrows)],
                      ReplacementTransform(lab_f, lab_F), run_time=2.0)
        self.rest()

        # 2 — wind: stream lines
        sl = StreamLines(lambda p: np.array([1.0, 0.5 * np.sin(1.3 * (p[0] - O[0])), 0.0]),
                         x_range=[O[0] - 3, O[0] + 3, 0.4], y_range=[-3, 3, 0.4],
                         stroke_width=2, max_anchors_per_line=20, padding=0.5, virtual_time=2.5,
                         colors=[BLUE_D, BLUE_B, WHITE])
        tags = VGroup(*[Tex(s, font_size=30).add_background_rectangle(opacity=0.8, buff=0.08)
                        for s in ["wind", "gravity", "magnetic field"]]).arrange(RIGHT, buff=0.5)
        tags.move_to(P2(0, -3.35))
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(arrows), FadeOut(lab_F), run_time=0.6)
            self.add(sl)
            sl.start_animation(warm_up=False, flow_speed=1.2, time_width=0.5)
            self.play(FadeIn(tags[0]), run_time=0.5)
            self.sync(tr, text, "Or think of a force")
            self.play(FadeIn(tags[1]), run_time=0.5)
            self.sync(tr, text, "or the magnetic")
            self.play(FadeIn(tags[2]), run_time=0.5)
            self.wait(tr.get_remaining_duration())
        self.wait(0.8)
        self.play(sl.end_animation(), FadeOut(tags), run_time=1.0)
        self.remove(sl)

        # 3 — components
        text = vo[3]
        f2 = MathTex(r"\mathbf F(x,y)=M(x,y)\,\mathbf i+N(x,y)\,\mathbf j", font_size=34)
        f3 = MathTex(r"\mathbf F(x,y,z)=M\,\mathbf i+N\,\mathbf j+P\,\mathbf k", font_size=34)
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "In the plane")
            self.nb_add(f2)
            self.sync(tr, text, "In space")
            self.nb_add(f3)
        self.rest()

        # 4 — draw one arrow: F = x i + y j at (1,2)
        plane = plane2d()
        p12 = P2(1, 2)
        dot = Dot(p12, color=WHITE, radius=0.07)
        dlab = MathTex("(1,2)", font_size=28).next_to(dot, LEFT, buff=0.12)
        K = 0.22
        arr = Arrow(p12, p12 + K * np.array([1, 2, 0]) * 1.6, buff=0, color=YELLOW, stroke_width=5,
                    max_tip_length_to_length_ratio=0.3)
        alab = MathTex(r"\mathbf F(1,2)", font_size=28, color=YELLOW).next_to(arr.get_end(), RIGHT, buff=0.1)
        ex = MathTex(r"\mathbf F=x\,\mathbf i+y\,\mathbf j,\quad \mathbf F(1,2)=\mathbf i+2\mathbf j", font_size=34)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.play(Create(plane), run_time=1.2)
            self.sync(tr, text, "Take F equals")
            self.nb_add(ex)
            self.sync(tr, text, "At the point one, two")
            self.play(FadeIn(dot), FadeIn(dlab), run_time=0.5)
            self.sync(tr, text, "So we draw")
            self.play(GrowArrow(arr), FadeIn(alab), run_time=1.0)
            self.play(Flash(p12, color=WHITE, line_length=0.2, flash_radius=0.2), run_time=0.8)
        self.rest()

        # 5 — radial field
        radial = field(lambda x, y: (x, y), lambda n: K * n)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(alab), FadeOut(dlab), FadeOut(dot), FadeOut(arr), run_time=0.4)
            self.play(LaggedStart(*[GrowArrow(a) for a in radial], lag_ratio=0.01), run_time=2.5)
            self.sync(tr, text, "This is the radial")
            self.nb_add(Tex("radial field: away from $O$, longer further out", font_size=30, color=GRAY_B),
                        gray=False)
        self.rest()

        # 6 — spin field
        spin = field(lambda x, y: (-y / np.hypot(x, y), x / np.hypot(x, y)), lambda n: 0.5)
        f_spin = MathTex(r"\mathbf F=\dfrac{-y\,\mathbf i+x\,\mathbf j}{\sqrt{x^2+y^2}}", font_size=34)
        ang = ValueTracker(0.0)
        parts = VGroup()
        for r0, a0 in [(1.0, 0), (1.0, PI), (2.0, PI / 2), (2.0, 3 * PI / 2), (2.8, PI / 4)]:
            d = Dot(color=WHITE, radius=0.08)
            d.add_updater(lambda m, r0=r0, a0=a0: m.move_to(P2(r0 * np.cos(a0 + ang.get_value() / r0),
                                                                r0 * np.sin(a0 + ang.get_value() / r0))))
            parts.add(d)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_add(f_spin)
            self.play(ReplacementTransform(radial, spin), run_time=1.5)
            self.sync(tr, text, "and the arrows circle")
            self.add(parts)
            self.play(ang.animate.set_value(4.0), run_time=max(tr.get_remaining_duration(), 1.0), rate_func=linear)
        self.rest(0.6)

        # 7 — pause
        self.pause(vo[7], r"$\mathbf F=y\,\mathbf i-x\,\mathbf j$: which way does it rotate?")

        # 8 — clockwise
        cw = field(lambda x, y: (y, -x), lambda n: K * n)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.play(ReplacementTransform(spin, cw), run_time=1.5)
            self.play(ang.animate.set_value(0.0), run_time=2.5, rate_func=linear)
            self.sync(tr, text, "A single minus")
            self.nb_add(MathTex(r"\mathbf F=y\,\mathbf i-x\,\mathbf j:\ \text{one minus sign}\to\text{reversed}",
                                font_size=32, color=YELLOW), gray=False)
        self.rest()
        for d in parts:
            d.clear_updaters()
        self.play(FadeOut(parts), FadeOut(cw), FadeOut(plane), run_time=0.6)

        # 9 — gradient fields: heat map + level curves of T = 100 - x^2 - y^2
        self.nb_clear()
        self.chapter(2, "Gradient fields")
        heat = VGroup()
        for r in np.linspace(3.0, 0.1, 30):
            T = 100 - r * r
            heat.add(Circle(radius=r, stroke_width=0, fill_opacity=1,
                            fill_color=interpolate_color(ManimColor("#1c2a5a"), ManimColor("#c0392b"),
                                                         (T - 91) / 9)).move_to(O))
        levels = VGroup(*[Circle(radius=np.sqrt(k), color=WHITE, stroke_width=1.5, stroke_opacity=0.7).move_to(O)
                          for k in range(1, 10)])
        grad_def = MathTex(r"\nabla f=\frac{\partial f}{\partial x}\mathbf i+\frac{\partial f}{\partial y}\mathbf j"
                           r"+\frac{\partial f}{\partial z}\mathbf k", font_size=34)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "The gradient points")
            self.nb_add(grad_def)
            self.sync(tr, text, "If we draw")
            self.play(FadeIn(heat), run_time=1.0)
            self.play(Create(levels), run_time=1.5)
        self.rest()

        # 10 — gradient arrows towards the origin
        gfield = VGroup()
        for x in np.arange(-2.625, 2.7, 0.75):
            for y in np.arange(-2.625, 2.7, 0.75):
                if np.hypot(x, y) < 2.9:
                    v = 0.09 * np.array([-2 * x, -2 * y, 0])
                    gfield.add(Arrow(P2(x, y), P2(x, y) + v, buff=0, color=WHITE, stroke_width=3,
                                     max_tip_length_to_length_ratio=0.3))
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.nb_add(MathTex(r"T=100-x^2-y^2,\quad \nabla T=-2x\,\mathbf i-2y\,\mathbf j", font_size=34))
            self.sync(tr, text, "At every point")
            self.play(LaggedStart(*[GrowArrow(a) for a in gfield], lag_ratio=0.01), run_time=2.5)
        self.rest()

        # 11 — perpendicular + longer where denser
        q = np.array([1.875, 1.125])
        rq = np.linalg.norm(q)
        Q = P2(*q)
        inward = -q / rq
        tang = np.array([-q[1], q[0]]) / rq
        l_in = Line(Q, Q + 0.7 * np.array([*inward, 0]))
        l_tan = Line(Q - 0.7 * np.array([*tang, 0]), Q + 0.7 * np.array([*tang, 0]), color=YELLOW, stroke_width=4)
        l_tan2 = Line(Q, Q + 0.7 * np.array([*tang, 0]))
        ra = RightAngle(l_in, l_tan2, length=0.22, color=YELLOW, quadrant=(1, 1))
        lvl = Circle(radius=rq, color=YELLOW, stroke_width=3).move_to(O)
        inner = [a for a in gfield if np.linalg.norm(a.get_start() - O) < 0.8]
        outer = [a for a in gfield if np.linalg.norm(a.get_start() - O) > 2.4]
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "First")
            self.play(Create(lvl), Create(l_tan), run_time=1.0)
            self.play(Create(ra), run_time=0.6)
            self.nb_add(Tex(r"$\nabla T\perp$ level curve", font_size=32, color=YELLOW), gray=False)
            self.sync(tr, text, "Second")
            self.play(FadeOut(lvl), FadeOut(l_tan), FadeOut(ra), run_time=0.4)
            self.play(*[Indicate(a, color=BLUE, scale_factor=1.1) for a in inner], run_time=1.0)
            self.play(*[Indicate(a, color=YELLOW, scale_factor=1.1) for a in outer], run_time=1.0)
            self.nb_add(Tex("level curves closer $\\Rightarrow$ longer arrows", font_size=32, color=YELLOW),
                        gray=False)
        self.rest()

        # 12 — 3D version (formula only)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "For T equals")
            self.nb_add(MathTex(r"T=100-x^2-y^2-z^2,\quad \nabla T=-2x\,\mathbf i-2y\,\mathbf j-2z\,\mathbf k",
                                font_size=34))
        self.rest()

        # 13 — recipe card
        head = Tex("gradient = three partial derivatives", font_size=38, color=YELLOW)
        exf = MathTex(r"f=xy+z^2", font_size=40)
        ders = MathTex(r"f_x=y", r",\quad f_y=x", r",\quad f_z=2z", font_size=40)
        res = MathTex(r"\Rightarrow\ \nabla f=y\,\mathbf i+x\,\mathbf j+2z\,\mathbf k", font_size=40)
        body = VGroup(head, exf, ders, res).arrange(DOWN, buff=0.45)
        card = card_left(self, body)
        text = vo[13]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(card[0]), FadeIn(head), run_time=0.6)
            self.sync(tr, text, "For example")
            self.play(Write(exf), run_time=0.8)
            for k, ph in enumerate(["the x derivative", "the y derivative", "the z derivative"]):
                self.sync(tr, text, ph)
                self.play(FadeIn(ders[k], shift=UP * 0.1), run_time=0.6)
            self.sync(tr, text, "So the gradient field")
            self.play(Write(res), run_time=1.0)
        self.rest()

        # 14 — engineering card
        e_head = Tex("Engineering", font_size=40, color=YELLOW)
        e1 = VGroup(MathTex(r"\mathbf q=-k\,\nabla T", font_size=40), Tex("heat flow: hot $\\to$ cold", font_size=30,
                                                                         color=GRAY_B)).arrange(DOWN, buff=0.15)
        e2 = VGroup(MathTex(r"\mathbf E=-\nabla V", font_size=40), Tex("electric field", font_size=30,
                                                                       color=GRAY_B)).arrange(DOWN, buff=0.15)
        e3 = Tex(r"gradient fields $=$ conservative fields (16.3)", font_size=30, color=ORANGE)
        ebody = VGroup(e_head, e1, e2, e3).arrange(DOWN, buff=0.45)
        ecard = card_left(self, ebody)
        text = vo[14]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(card), FadeIn(ecard[0]), FadeIn(e_head), run_time=0.6)
            self.sync(tr, text, "Heat flows")
            self.play(FadeIn(e1), run_time=0.8)
            self.sync(tr, text, "And the electric")
            self.play(FadeIn(e2), run_time=0.8)
            self.sync(tr, text, "Later in this chapter")
            self.play(FadeIn(e3), run_time=0.8)
        self.rest()

        # 15 — summary
        self.summary(vo[15],
                     [r"A vector field gives an arrow at every point: $M\,\mathbf i+N\,\mathbf j+P\,\mathbf k$.",
                      r"To draw it: evaluate $\mathbf F$ at a point, put the tail of the arrow there.",
                      r"$\nabla f$ = partial derivatives; points uphill, $\perp$ level curves."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
VO["intro2"] = [
    "In this second video, we combine vector fields with curves. The question is: if an object moves along a curve through a force field, how much work does the force do?",
    "Start with what you know from physics. A constant force F moves an object along a straight displacement d. The work is F dot d: the magnitude of F, times the distance, times the cosine of the angle between them. Only the part of the force along the motion does work.",
    "Split the force into two parts: a part along the direction of motion, and a part perpendicular to it. The perpendicular part does no work at all. Think of carrying a box horizontally: gravity pulls down, but it does no work.",
    "Now the path is curved, and the force changes from point to point. Here is the field F equals x minus y, i, plus x, j, and our curve C: a quarter of the unit circle, from one, zero, to zero, one.",
    "We do the same as in section sixteen point one. Cut the curve into small pieces. On each piece, the path is almost straight, and the force is almost constant. The unit tangent vector T gives the direction of motion. The work on one piece is about F dot T, times the length of the piece, delta s.",
    "Add the work on all pieces, and let the pieces get smaller. The sum becomes an integral: the work is the integral over C of F dot T, d s. With more and more pieces, the sum approaches about one point zero seven.",
    "This is nothing new. F dot T is just a number at every point of the curve: a scalar function. So the work is a line integral of a scalar function, exactly like in section sixteen point one.",
    "Now the key simplification. T is r prime divided by its length. And d s is the length of r prime, times d t. Multiply them, and the lengths cancel. T d s is simply r prime of t, d t, which we call d r. So for a vector field, you never need the length of r prime!",
    "This gives the formula we actually use: the integral over C of F dot d r equals the integral from a to b of F of r of t, dot r prime of t, d t.",
    "The method, in three steps. Step one: substitute the curve into F. With x equals cos t and y equals sin t, F becomes cos t minus sin t, i, plus cos t, j.",
    "Step two: differentiate the curve. r prime of t equals minus sin t, i, plus cos t, j.",
    "Step three: take the dot product. Cos t minus sin t, times minus sin t, plus cos t times cos t. That is minus sin t cos t, plus sin squared t, plus cos squared t. And sin squared plus cos squared is one. So we get one minus sin t cos t.",
    "Now integrate from zero to pi over two. One gives t. Sin t cos t integrates to sin squared t over two. The result is pi over two minus one half, about one point zero seven. Exactly what the sum of the pieces was approaching.",
    "Unlike in section sixteen point one, the direction now matters. If we walk the curve backwards, T flips, F dot T changes sign, and the work becomes negative. Moving with the force gives positive work; moving against it gives negative work.",
    "You will often see the same integral written differently. Since d r equals d x i, plus d y j, plus d z k, the dot product F dot d r equals M d x plus N d y plus P d z. To compute it, substitute x, y and z as functions of t, and replace d x by x prime of t, d t, and so on.",
    "For our example: x minus y, d x, plus x, d y. With x equals cos t and y equals sin t, d x is minus sin t d t, and d y is cos t d t. Substituting gives exactly the same integrand: one minus sin t cos t. Same integral, same answer.",
    "In mechatronics, this is about energy. If a robot arm moves its tool along a path through a force field, for example against gravity or a spring, this line integral gives the work done by that field. The motor has to supply the opposite.",
    "Summary. One: work along a curve is the integral of F dot T, d s; only the tangential part of F counts. Two: since T d s equals d r, you compute it as the integral of F of r of t, dot r prime of t, d t, without the length of r prime. Three: the direction matters; reversing the curve changes the sign.",
]

O2 = np.array([-5.7, -2.7, 0.0])   # origin for the unit-circle drawings
U2 = 4.5                            # scene units per math unit


def Q2(x, y):
    return O2 + U2 * np.array([x, y, 0.0])


def F_ex(x, y):
    return np.array([x - y, x])


def ex_field(lf=lambda n: 0.32 * n, opacity=0.55):
    def f(p):
        x, y = (p[0] - O2[0]) / U2, (p[1] - O2[1]) / U2
        u, v = F_ex(x, y)
        return np.array([u, v, 0.0])
    vf = ArrowVectorField(f, x_range=[O2[0] - 0.1 * U2, O2[0] + 1.2 * U2, 0.25 * U2],
                          y_range=[O2[1] - 0.1 * U2, O2[1] + 1.25 * U2, 0.25 * U2], length_func=lf)
    vf.set_opacity(opacity)
    return vf


def quarter_arc(color=C_CURVE, t0=0.0, t1=PI / 2, width=6):
    return ParametricFunction(lambda t: Q2(np.cos(t), np.sin(t)), t_range=[t0, t1], color=color,
                              stroke_width=width)


def dir_tips(ts, color=C_CURVE, reverse=False, func=lambda t: (np.cos(t), np.sin(t)), size=0.28, to=Q2):
    tips = VGroup()
    for t in ts:
        a, b = (t + 0.03, t - 0.03) if reverse else (t - 0.03, t + 0.03)
        p, q = to(*func(a)), to(*func(b))
        tri = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(size / 2)
        tri.rotate(np.arctan2(q[1] - p[1], q[0] - p[0]) - PI / 2).move_to((p + q) / 2)
        tips.add(tri)
    return tips


def midpoint_sum(n):
    ts = (np.arange(n) + 0.5) * (PI / 2) / n
    return float(np.sum(1 - np.sin(ts) * np.cos(ts)) * (PI / 2) / n)


CANCEL_TPL = TexTemplate()
CANCEL_TPL.add_to_preamble(r"\usepackage{xcolor}\usepackage{cancel}\renewcommand{\CancelColor}{\color{red}}")


class WorkLineIntegral(FlatScene):
    def construct(self):
        vo = VO["intro2"]
        self.start("16.2 — Work along a curve",
                   r"\mathbf F=(x-y)\,\mathbf i+x\,\mathbf j,\ \ C:\ \mathbf r(t)=\cos t\,\mathbf i+\sin t\,\mathbf j,"
                   r"\ 0\le t\le\tfrac{\pi}{2}",
                   checklist=[r"1 $\mathbf F(\mathbf r(t))$", r"2 $\mathbf r'(t)$", r"3 dot \& integrate"])
        with self.voiceover(text=vo[0]) as tr:
            self.play(Write(self.title_mob), run_time=1.2)
            self.play(Write(self.problem_mob), run_time=2.0)
            self.sync(tr, vo[0], "The question is")
            q = Tex(r"How much work does a force do\\along a curved path?", font_size=44, color=YELLOW)
            qc = card_left(self, q)
            self.play(FadeIn(qc), run_time=0.6)
        self.rest()
        self.play(FadeOut(qc), run_time=0.5)

        # 1 — straight line work
        self.chapter(1, "Work along a straight line")
        ground = Line([-6.6, -1.0, 0], [0.4, -1.0, 0], color=GRAY)
        box = Square(0.9, color=WHITE, fill_color=GRAY_D, fill_opacity=1).move_to([-5.6, -0.55, 0])
        th = 35 * DEGREES
        Fv = 2.2 * np.array([np.cos(th), np.sin(th), 0])
        fa = Arrow(box.get_center(), box.get_center() + Fv, buff=0, color=C_FORCE, stroke_width=6)
        f_lab = MathTex(r"\mathbf F", color=C_FORCE, font_size=36).next_to(fa.get_end(), UP, buff=0.1)
        darr = Arrow([-5.6, -1.6, 0], [-1.4, -1.6, 0], buff=0, color=WHITE, stroke_width=4)
        d_lab = MathTex(r"\mathbf d", font_size=36).next_to(darr, DOWN, buff=0.1)
        arc_th = Arc(radius=0.6, start_angle=0, angle=th, arc_center=box.get_center(), color=YELLOW)
        th_lab = MathTex(r"\theta", font_size=30, color=YELLOW).move_to(box.get_center() + 0.85 * np.array(
            [np.cos(th / 2), np.sin(th / 2), 0]))
        w = MathTex(r"W=\mathbf F\cdot\mathbf d=|\mathbf F|\,|\mathbf d|\cos\theta", font_size=36)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Create(ground), FadeIn(box), run_time=0.8)
            self.sync(tr, text, "A constant force")
            self.play(GrowArrow(fa), FadeIn(f_lab), run_time=0.8)
            self.play(GrowArrow(darr), FadeIn(d_lab), run_time=0.8)
            self.play(Create(arc_th), FadeIn(th_lab), run_time=0.5)
            self.sync(tr, text, "The work is")
            self.nb_add(w)
            self.play(Indicate(w), run_time=0.8)
        self.rest()

        # 2 — split into parallel / perpendicular parts
        c0 = box.get_center()
        par = Arrow(c0, c0 + np.array([Fv[0], 0, 0]), buff=0, color=C_PROJ, stroke_width=6)
        perp = Arrow(c0, c0 + np.array([0, Fv[1], 0]), buff=0, color=GRAY, stroke_width=6)
        dsh = VGroup(DashedLine(fa.get_end(), par.get_end(), color=GRAY_B),
                     DashedLine(fa.get_end(), perp.get_end(), color=GRAY_B))
        par_lab = Tex("does work", font_size=28, color=C_PROJ).next_to(par, DOWN, buff=0.1)
        perp_lab = Tex("no work", font_size=28, color=GRAY).next_to(perp, LEFT, buff=0.1)
        b2 = Square(0.6, color=WHITE, fill_color=GRAY_D, fill_opacity=1).move_to([-3.4, 2.3, 0])
        g_arr = Arrow(b2.get_center(), b2.get_center() + DOWN * 1.1, buff=0, color=C_FORCE, stroke_width=5)
        m_arr = Arrow(b2.get_right() + RIGHT * 0.1, b2.get_right() + RIGHT * 1.6, buff=0, color=WHITE, stroke_width=4)
        sk_lab = Tex(r"carrying a box: gravity $\perp$ motion $\Rightarrow W=0$", font_size=28).move_to([-3.2, 3.35, 0])
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(Create(dsh), GrowArrow(par), GrowArrow(perp), run_time=1.2)
            self.play(FadeIn(par_lab), run_time=0.4)
            self.sync(tr, text, "The perpendicular part")
            self.play(FadeIn(perp_lab), run_time=0.4)
            self.sync(tr, text, "Think of carrying")
            self.play(FadeIn(b2), GrowArrow(g_arr), GrowArrow(m_arr), FadeIn(sk_lab), run_time=1.0)
        self.rest()
        self.play(*[FadeOut(m) for m in [ground, box, fa, f_lab, darr, d_lab, arc_th, th_lab, par, perp, dsh,
                                         par_lab, perp_lab, b2, g_arr, m_arr, sk_lab]], run_time=0.6)

        # 3 — curved path in the field
        self.nb_clear()
        self.chapter(2, "A curved path")
        axes = VGroup(Arrow(Q2(-0.1, 0), Q2(1.25, 0), buff=0, stroke_width=2, color=GRAY_B, tip_length=0.18),
                      Arrow(Q2(0, -0.1), Q2(0, 1.25), buff=0, stroke_width=2, color=GRAY_B, tip_length=0.18))
        ax_lab = VGroup(MathTex("x", font_size=28).next_to(Q2(1.25, 0), DOWN, buff=0.1),
                        MathTex("y", font_size=28).next_to(Q2(0, 1.25), LEFT, buff=0.1))
        vf = ex_field()
        arc = quarter_arc()
        tips = dir_tips([PI / 4])
        pl = VGroup(MathTex("(1,0)", font_size=26).next_to(Q2(1, 0), DOWN + RIGHT, buff=0.08),
                    MathTex("(0,1)", font_size=26).next_to(Q2(0, 1), LEFT, buff=0.1))
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(axes), FadeIn(ax_lab), run_time=0.6)
            self.sync(tr, text, "Here is the field")
            self.play(LaggedStart(*[GrowArrow(a) for a in vf], lag_ratio=0.02), run_time=1.8)
            self.sync(tr, text, "and our curve")
            self.play(Create(arc), FadeIn(pl), run_time=1.5)
            self.play(FadeIn(tips), run_time=0.4)
        self.rest()

        # 4 — four pieces with T, F, projection
        n = 4
        cuts = VGroup(*[Dot(Q2(np.cos(t), np.sin(t)), radius=0.06, color=WHITE)
                        for t in np.linspace(0, PI / 2, n + 1)])
        piece_grp = VGroup()
        for k in range(n):
            tm = (k + 0.5) * (PI / 2) / n
            pm = Q2(np.cos(tm), np.sin(tm))
            T = np.array([-np.sin(tm), np.cos(tm), 0])
            Fm = np.array([*F_ex(np.cos(tm), np.sin(tm)), 0])
            s = 0.9
            Ta = Arrow(pm, pm + s * T, buff=0, color=C_T, stroke_width=4, max_tip_length_to_length_ratio=0.25)
            Fa = Arrow(pm, pm + s * Fm, buff=0, color=C_FORCE, stroke_width=4, max_tip_length_to_length_ratio=0.25)
            proj = Arrow(pm, pm + s * np.dot(Fm, T) * T, buff=0, color=C_PROJ, stroke_width=6,
                         max_tip_length_to_length_ratio=0.25)
            dl = DashedLine(Fa.get_end(), proj.get_end(), color=GRAY_B, stroke_width=2)
            piece_grp.add(VGroup(Ta, Fa, dl, proj))
        legend = VGroup(*[Tex(s, font_size=28, color=c) for s, c in
                          [(r"$\mathbf T_k$", C_T), (r"$\mathbf F_k$", C_FORCE),
                           (r"$\mathbf F_k\cdot\mathbf T_k$", C_PROJ)]]).arrange(RIGHT, buff=0.4)
        legend.move_to([-2.0, -3.4, 0])
        wk = MathTex(r"W_k\approx \mathbf F_k\cdot\mathbf T_k\,\Delta s_k", font_size=36)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.play(vf.animate.set_opacity(0.2), run_time=0.5)
            self.sync(tr, text, "Cut the curve")
            self.play(FadeIn(cuts), run_time=0.6)
            self.sync(tr, text, "The unit tangent")
            self.play(*[GrowArrow(g[0]) for g in piece_grp], FadeIn(legend[0]), run_time=1.0)
            self.play(*[GrowArrow(g[1]) for g in piece_grp], FadeIn(legend[1]), run_time=1.0)
            self.sync(tr, text, "The work on one piece")
            self.play(*[Create(g[2]) for g in piece_grp], *[GrowArrow(g[3]) for g in piece_grp],
                      FadeIn(legend[2]), run_time=1.0)
            self.nb_add(wk)
        self.rest()

        # 5 — sum -> integral, live counter
        sm = MathTex(r"W\approx\sum \mathbf F_k\cdot\mathbf T_k\,\Delta s_k\ \to\ W=\int_C \mathbf F\cdot\mathbf T\,ds",
                     font_size=34)
        rows = VGroup(*[MathTex(f"n={k}:", f"\\ \\ {midpoint_sum(k):.4f}", font_size=30) for k in (4, 8, 16, 64)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-1.2, 1.6, 0])
        for r in rows:
            r[1].set_color(C_PROJ)
        approx = MathTex(r"\approx 1.07", font_size=34, color=C_PROJ).next_to(rows, DOWN, buff=0.25)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "The sum becomes")
            self.nb_add(sm)
            self.sync(tr, text, "With more and more")
            for r in rows:
                self.play(FadeIn(r, shift=LEFT * 0.2), run_time=0.5)
            self.play(Write(approx), run_time=0.6)
        self.rest()

        # 6 — card: F.T is a scalar
        c6 = card_left(self, Tex(r"$\mathbf F\cdot\mathbf T$ is a scalar\\$\Rightarrow$ this is a 16.1 line integral",
                                 font_size=42, color=YELLOW))
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "F dot T is just")
            self.play(FadeIn(c6), run_time=0.6)
        self.rest()
        self.play(FadeOut(c6), FadeOut(piece_grp), FadeOut(legend), FadeOut(cuts), run_time=0.5)

        # 7 — T ds = r' dt
        self.nb_clear()
        self.chapter(3, r"The shortcut: $\mathbf F\cdot d\mathbf r$")
        l1 = MathTex(r"\mathbf T=\frac{\mathbf r'(t)}{|\mathbf r'(t)|},\quad ds=|\mathbf r'(t)|\,dt", font_size=36)
        l2 = MathTex(r"\mathbf T\,ds=\frac{\mathbf r'(t)}{|\mathbf r'(t)|}\,|\mathbf r'(t)|\,dt", font_size=36)
        l2c = MathTex(r"\mathbf T\,ds=\frac{\mathbf r'(t)}{\cancel{|\mathbf r'(t)|}}\,\cancel{|\mathbf r'(t)|}\,dt",
                      r"=\mathbf r'(t)\,dt=d\mathbf r", font_size=36, tex_template=CANCEL_TPL)
        k_sc = min(1.0, NB_W / l2c.width)
        l2.scale(k_sc)
        l2c.scale(k_sc)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.nb_add(l1)
            self.sync(tr, text, "Multiply them")
            self.nb_add(l2, gray=False)
            l2c.shift(l2.get_left() - l2c[0].get_left() + (l2.get_center()[1] - l2c[0].get_center()[1]) * UP)
            self.sync(tr, text, "the lengths cancel")
            self.play(FadeOut(l2), FadeIn(l2c[0]), run_time=0.8)
            self.nb_items[-1] = l2c
            self.sync(tr, text, "T d s is simply")
            self.play(Write(l2c[1]), run_time=0.8)
            self.play(Indicate(l2c[1]), run_time=0.8)
        self.rest()

        # 8 — boxed formula
        main = MathTex(r"\int_C\mathbf F\cdot\mathbf T\,ds=\int_C\mathbf F\cdot d\mathbf r=\int_a^b "
                       r"\mathbf F(\mathbf r(t))\cdot\mathbf r'(t)\,dt", font_size=34)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.nb_add(main, buff=0.4)
            box8 = SurroundingRectangle(main, color=YELLOW, buff=0.12)
            self.play(Create(box8), run_time=0.6)
            main.add(box8)
        self.rest()

        # 9a-9d — the method
        self.nb_clear()
        self.chapter(4, "The method")
        self.show_checklist()
        dot9 = Dot(Q2(1, 0), color=WHITE, radius=0.08)
        s9a = MathTex(r"\mathbf F(\mathbf r(t))=(\cos t-\sin t)\,\mathbf i+\cos t\,\mathbf j", font_size=34)
        s9b = MathTex(r"\mathbf r'(t)=-\sin t\,\mathbf i+\cos t\,\mathbf j", font_size=34)
        s9c = MathTex(r"\mathbf F\cdot\mathbf r'=-\sin t\cos t+\sin^2t+\cos^2t=", r"1-\sin t\cos t", font_size=34)
        s9c[1].set_color(YELLOW)
        s9d = MathTex(r"\int_0^{\pi/2}(1-\sin t\cos t)\,dt=\Big[t-\tfrac{\sin^2t}{2}\Big]_0^{\pi/2}"
                      r"=\tfrac{\pi}{2}-\tfrac12\approx1.07", font_size=34)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.play(FadeIn(dot9), run_time=0.4)
            self.sync(tr, text, "With x equals")
            self.nb_add(s9a)
        self.rest()
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            self.nb_add(s9b)
        self.rest()
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.nb_add(s9c)
            self.sync(tr, text, "So we get")
            self.play(Indicate(s9c[1]), run_time=0.8)
        self.rest()
        tick = MathTex(r"\checkmark", color=C_ANSWER, font_size=44).next_to(approx, RIGHT, buff=0.2)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.nb_add(s9d, buff=0.4)
            self.sync(tr, text, "The result is")
            b9 = SurroundingRectangle(s9d, color=C_ANSWER, buff=0.12)
            self.play(Create(b9), run_time=0.6)
            s9d.add(b9)
            self.sync(tr, text, "Exactly what")
            self.play(Indicate(rows[-1]), Indicate(approx), run_time=1.0)
            self.play(FadeIn(tick), run_time=0.4)
        self.rest()
        self.play(FadeOut(rows), FadeOut(approx), FadeOut(tick), FadeOut(dot9), run_time=0.5)

        # 10 — direction matters
        self.chapter(5, "Direction matters")
        tips_r = dir_tips([PI / 4], reverse=True)
        rev = VGroup()
        for k in range(n):
            tm = (k + 0.5) * (PI / 2) / n
            pm = Q2(np.cos(tm), np.sin(tm))
            T = -np.array([-np.sin(tm), np.cos(tm), 0])
            Fm = np.array([*F_ex(np.cos(tm), np.sin(tm)), 0])
            s = 0.9
            rev.add(VGroup(Arrow(pm, pm + s * T, buff=0, color=C_T, stroke_width=4, max_tip_length_to_length_ratio=0.25),
                           Arrow(pm, pm + s * np.dot(Fm, T) * T, buff=0, color=C_NEG, stroke_width=6,
                                 max_tip_length_to_length_ratio=0.25)))
        neg_lab = Tex(r"$\mathbf F\cdot\mathbf T<0$", font_size=32, color=C_NEG).move_to([-1.3, 1.8, 0])
        text = vo[13]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "If we walk")
            self.play(Transform(tips, tips_r), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(g[0]) for g in rev], lag_ratio=0.1), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(g[1]) for g in rev], lag_ratio=0.1), FadeIn(neg_lab), run_time=0.8)
            self.sync(tr, text, "and the work becomes")
            self.nb_add(MathTex(r"-C:\ W=-\big(\tfrac{\pi}{2}-\tfrac12\big)", font_size=36, color=C_NEG), gray=False)
        self.rest()
        self.play(FadeOut(rev), FadeOut(neg_lab), Transform(tips, dir_tips([PI / 4])), run_time=0.6)

        # 11 — other notation
        self.nb_clear()
        self.chapter(6, "Another notation")
        n1 = MathTex(r"d\mathbf r=dx\,\mathbf i+dy\,\mathbf j+dz\,\mathbf k\ \Rightarrow\ "
                     r"\mathbf F\cdot d\mathbf r=M\,dx+N\,dy+P\,dz", font_size=34)
        n2 = MathTex(r"dx=x'(t)\,dt,\quad dy=y'(t)\,dt,\quad dz=z'(t)\,dt", font_size=34)
        text = vo[14]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Since d r equals")
            self.nb_add(n1)
            self.sync(tr, text, "To compute it")
            self.nb_add(n2)
        self.rest()

        # 12 — example in this notation
        e1 = MathTex(r"\int_C (x-y)\,dx+x\,dy", font_size=36)
        e2 = MathTex(r"x=\cos t,\ dx=-\sin t\,dt,\quad y=\sin t,\ dy=\cos t\,dt", font_size=32)
        e3 = MathTex(r"(\cos t-\sin t)(-\sin t)+\cos t\cdot\cos t=", r"1-\sin t\cos t", font_size=32)
        e3[1].set_color(YELLOW)
        text = vo[15]
        with self.voiceover(text=text) as tr:
            self.nb_add(e1)
            self.sync(tr, text, "With x equals")
            self.nb_add(e2)
            self.sync(tr, text, "Substituting gives")
            self.nb_add(e3)
            self.play(Indicate(e3[1]), run_time=0.8)
        self.rest()

        # 13 — mechatronics: robot arm
        self.play(*[FadeOut(m) for m in [vf, arc, tips, pl, axes, ax_lab]], run_time=0.5)
        base = np.array([-5.4, -2.6, 0])
        L1 = L2 = 2.3
        s_tr = ValueTracker(0.0)

        def tool(s):
            a = PI * (0.15 + 0.7 * s)
            return np.array([-3.0 + 2.0 * np.cos(a), -0.2 + 1.6 * np.sin(a), 0])

        def arm():
            p = tool(s_tr.get_value())
            d = p - base
            dist = min(np.linalg.norm(d), L1 + L2 - 1e-3)
            a = np.arctan2(d[1], d[0]) + np.arccos((L1 ** 2 + dist ** 2 - L2 ** 2) / (2 * L1 * dist))
            elbow = base + L1 * np.array([np.cos(a), np.sin(a), 0])
            return VGroup(Line(base, elbow, stroke_width=10, color=GRAY_B),
                          Line(elbow, p, stroke_width=8, color=GRAY_B),
                          Dot(elbow, radius=0.1, color=WHITE), Dot(p, radius=0.1, color=YELLOW))
        robot = always_redraw(arm)
        foot = Rectangle(width=1.2, height=0.3, fill_color=GRAY_D, fill_opacity=1, stroke_color=GRAY).move_to(
            base + DOWN * 0.15)
        path = ParametricFunction(tool, t_range=[0, 1], color=C_CURVE, stroke_width=4)
        grav = VGroup(*[Arrow([x, 3.0, 0], [x, 2.3, 0], buff=0, color=C_FORCE, stroke_width=3)
                        for x in np.arange(-6.4, 0.2, 0.9)])
        mt = Tex("Mechatronics", font_size=38, color=YELLOW).move_to([-3.2, 3.6, 0])
        mt2 = Tex(r"work by the field $=-$(energy the motor supplies)", font_size=28).move_to([-3.2, -3.4, 0])
        text = vo[16]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(mt), FadeIn(foot), FadeIn(robot), run_time=0.8)
            self.sync(tr, text, "If a robot arm")
            self.play(Create(path), run_time=1.0)
            self.play(FadeIn(grav), run_time=0.5)
            self.play(s_tr.animate.set_value(1.0), run_time=3.0)
            self.sync(tr, text, "The motor has")
            self.play(FadeIn(mt2), run_time=0.6)
        self.rest()
        robot.clear_updaters()

        # 14 — summary
        self.summary(vo[17],
                     [r"Work $=\int_C\mathbf F\cdot\mathbf T\,ds$: only the tangential part of $\mathbf F$ counts.",
                      r"$\mathbf T\,ds=d\mathbf r$: compute $\int_a^b\mathbf F(\mathbf r(t))\cdot\mathbf r'(t)\,dt$ "
                      r"(no $|\mathbf r'|$).",
                      r"Direction matters: reversing the curve changes the sign."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
VO["intro3"] = [
    "In this third video, the vector field is a velocity field, like flowing water. We ask two questions: how much does the fluid flow along a curve, and how much flows across it?",
    "If F is the velocity of a fluid, the same integral, F dot T d s, measures how much the fluid moves along the curve. We call it the flow along C. The calculation is exactly the same as for work.",
    "If the curve is closed, so it starts and ends at the same point, the flow is called the circulation around the curve. We write a small circle on the integral sign. Circulation tells you whether the fluid tends to swirl around the curve.",
    "Compare two fields on the unit circle. In the radial field, every arrow is perpendicular to the circle, so F dot T is zero everywhere, and the circulation is zero. In the spin field, every arrow points along the circle, so the circulation is positive.",
    "Pause and think: for the field x minus y, i, plus x, j, counterclockwise around the unit circle, is the circulation positive, negative or zero?",
    "On the circle, F dot r prime is one minus sin t cos t, the same as in the previous video. Now we integrate over the full circle, from zero to two pi. The sine cosine part integrates to zero, so the circulation is two pi. Positive: the fluid swirls counterclockwise.",
    "Now the second question: how much fluid crosses the curve? For that we need the component of F perpendicular to the curve, along the outward normal vector n. The flux of F across C is the integral of F dot n, d s. Positive flux means net outflow; negative flux means net inflow.",
    "So circulation uses the tangential component, F dot T. Flux uses the normal component, F dot n. Same field, same curve, two different questions.",
    "For a curve traversed counterclockwise, the outward normal is T cross k. In components, n equals d y over d s, i, minus d x over d s, j. Then F dot n d s becomes M d y minus N d x. The d s disappears again, so we never need the normal vector itself.",
    "This gives the flux formula: the integral around C of M d y minus N d x, with C traversed counterclockwise exactly once.",
    "Example: the same field across the unit circle. M is cos t minus sin t, N is cos t, d y is cos t d t, and d x is minus sin t d t. M d y minus N d x simplifies to cos squared t, d t. Integrating over the full circle gives pi. Positive, so the net flow is outward.",
    "In engineering: the circulation of the magnetic field around a wire is proportional to the current through it. That is Ampère's law. And flux describes how much coolant or air flows out through a boundary. In section sixteen point four, Green's theorem will connect circulation and flux to what happens inside the curve.",
    "Summary. One: flow along a curve is the integral of F dot T d s, the same calculation as work. Two: for a closed curve this is the circulation; it measures swirling. Three: flux across a closed curve is the integral of M d y minus N d x, counterclockwise; it measures net outflow.",
]

C3 = np.array([-3.3, -0.1, 0.0])   # centre of the unit circle
U3 = 2.3


def Q3(x, y, c=C3, u=U3):
    return c + u * np.array([x, y, 0.0])


def circle_arrows(c, u, vec, n=12, s=0.55, color=YELLOW):
    g = VGroup()
    for k in range(n):
        t = 2 * PI * k / n
        p = Q3(np.cos(t), np.sin(t), c, u)
        v = np.array([*vec(np.cos(t), np.sin(t)), 0])
        g.add(Arrow(p, p + s * v, buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.3))
    return g


class FlowCirculationFlux(FlatScene):
    def construct(self):
        vo = VO["intro3"]
        self.start("16.2 — Flow, circulation, flux",
                   r"\mathbf F=(x-y)\,\mathbf i+x\,\mathbf j\ \text{ on the unit circle}")

        # 0 — two questions
        qs = VGroup()
        for s, c in [("along the curve?", YELLOW), ("across the curve?", C_NORMAL)]:
            r = RoundedRectangle(corner_radius=0.15, width=3.3, height=1.6, stroke_color=c, stroke_width=2)
            qs.add(VGroup(r, Tex(s, font_size=34, color=c).move_to(r)))
        qs.arrange(RIGHT, buff=0.3).move_to(LEFT_CENTER)
        with self.voiceover(text=vo[0]) as tr:
            self.play(Write(self.title_mob), run_time=1.2)
            self.play(Write(self.problem_mob), run_time=1.5)
            self.sync(tr, vo[0], "how much does the fluid flow along")
            self.play(FadeIn(qs[0], shift=UP * 0.2), run_time=0.6)
            self.sync(tr, vo[0], "how much flows across")
            self.play(FadeIn(qs[1], shift=UP * 0.2), run_time=0.6)
        self.rest()
        self.play(FadeOut(qs), run_time=0.5)

        # 1 — flow along an open curve
        self.chapter(1, "Flow")

        def vel(p):
            x, y = (p[0] - C3[0]) / U3, (p[1] - C3[1]) / U3
            return np.array([*(0.6 * F_ex(x, y)), 0.0])
        sl = StreamLines(vel, x_range=[C3[0] - 3.4, C3[0] + 3.4, 0.45], y_range=[-3.6, 3.6, 0.45],
                         stroke_width=1.5, max_anchors_per_line=25, padding=0.3, virtual_time=3,
                         colors=[BLUE_E, BLUE_C, BLUE_A])
        open_c = ParametricFunction(lambda t: Q3(np.cos(t), np.sin(t)), t_range=[-PI / 4, 2 * PI / 3],
                                    color=YELLOW, stroke_width=6)
        oc_lab = MathTex("C", color=YELLOW, font_size=36).move_to(Q3(1.15 * np.cos(PI / 3), 1.15 * np.sin(PI / 3)))
        flow = MathTex(r"\text{Flow}=\int_C\mathbf F\cdot\mathbf T\,ds", font_size=36)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.add(sl)
            sl.start_animation(warm_up=False, flow_speed=1.0, time_width=0.5)
            self.wait(1.0)
            self.sync(tr, text, "measures how much")
            self.play(Create(open_c), FadeIn(oc_lab), run_time=1.2)
            self.sync(tr, text, "We call it")
            self.nb_add(flow)
            self.wait(tr.get_remaining_duration())
        self.rest()

        # 2 — closed curve: circulation
        circ = Circle(radius=U3, color=YELLOW, stroke_width=6).move_to(C3)
        circ_tips = dir_tips([PI / 4, 5 * PI / 4], color=YELLOW, to=Q3)
        cmt = MathTex(r"\text{Circulation}=", r"\oint_C", r"\mathbf F\cdot\mathbf T\,ds", font_size=36)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(ReplacementTransform(open_c, circ), oc_lab.animate.move_to(Q3(0.78, 0.78)), run_time=1.2)
            self.play(FadeIn(circ_tips), run_time=0.4)
            self.sync(tr, text, "is called the circulation")
            self.nb_add(cmt)
            self.sync(tr, text, "We write a small circle")
            self.play(Indicate(cmt[1], scale_factor=1.4), run_time=1.0)
            self.wait(tr.get_remaining_duration())
        self.play(sl.end_animation(), run_time=1.0)
        self.remove(sl)
        self.play(FadeOut(circ), FadeOut(circ_tips), FadeOut(oc_lab), run_time=0.5)

        # 3 — radial vs spin on the unit circle
        cl, cr = np.array([-5.0, 0.4, 0]), np.array([-1.55, 0.4, 0])
        ul = 1.25
        pan = VGroup()
        for c, vec, lab, col in [(cl, lambda x, y: (x, y), r"$\mathbf F\cdot\mathbf T=0\to$ circulation $0$", GRAY_B),
                                 (cr, lambda x, y: (-y, x), r"circulation $>0$", C_PROJ)]:
            ring = Circle(radius=ul, color=WHITE, stroke_width=3).move_to(c)
            arr = circle_arrows(c, ul, vec, n=10, s=0.55, color=col)
            t = Tex(lab, font_size=26, color=col).next_to(ring, DOWN, buff=0.75)
            pan.add(VGroup(ring, arr, t))
        names = VGroup(Tex("radial", font_size=30).next_to(pan[0][0], UP, buff=0.75),
                       Tex("spin", font_size=30).next_to(pan[1][0], UP, buff=0.75))
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.play(Create(pan[0][0]), Create(pan[1][0]), FadeIn(names), run_time=0.8)
            self.sync(tr, text, "In the radial field")
            self.play(LaggedStart(*[GrowArrow(a) for a in pan[0][1]], lag_ratio=0.05), run_time=1.0)
            self.sync(tr, text, "and the circulation is zero")
            self.play(FadeIn(pan[0][2]), run_time=0.5)
            self.sync(tr, text, "In the spin field")
            self.play(LaggedStart(*[GrowArrow(a) for a in pan[1][1]], lag_ratio=0.05), run_time=1.0)
            self.sync(tr, text, "so the circulation is positive")
            self.play(FadeIn(pan[1][2]), run_time=0.5)
        self.rest()
        self.play(FadeOut(pan), FadeOut(names), run_time=0.5)

        # 4 — pause
        self.pause(vo[4], r"$\mathbf F=(x-y)\,\mathbf i+x\,\mathbf j$, counterclockwise around the unit circle:\\"
                          r"circulation positive, negative or zero?")

        # 5 — compute circulation = 2 pi
        vf = VGroup()
        for x in np.arange(-1.25, 1.3, 0.5):
            for y in np.arange(-1.25, 1.3, 0.5):
                p = Q3(x, y)
                v = np.array([*F_ex(x, y), 0])
                vf.add(Arrow(p, p + 0.35 * v, buff=0, color=GRAY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3))
        vf.set_opacity(0.5)
        circ = Circle(radius=U3, color=YELLOW, stroke_width=5).move_to(C3)
        circ_tips = dir_tips([PI / 4, 5 * PI / 4], color=YELLOW, to=Q3)
        ang = ValueTracker(0.0)
        parts = VGroup()
        for a0 in np.linspace(0, 2 * PI, 6, endpoint=False):
            d = Dot(radius=0.08, color=WHITE)
            d.add_updater(lambda m, a0=a0: m.move_to(Q3(np.cos(a0 + ang.get_value()), np.sin(a0 + ang.get_value()))))
            parts.add(d)
        c1 = MathTex(r"\mathbf F\cdot\mathbf r'=1-\sin t\cos t\quad(\text{same as video 2})", font_size=34)
        c2 = MathTex(r"\oint_C\mathbf F\cdot\mathbf T\,ds=\int_0^{2\pi}(1-\sin t\cos t)\,dt=2\pi", font_size=34)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(vf), Create(circ), FadeIn(circ_tips), run_time=1.0)
            self.nb_add(c1)
            self.sync(tr, text, "Now we integrate")
            self.nb_add(c2, buff=0.4)
            self.sync(tr, text, "so the circulation is two pi")
            bx = SurroundingRectangle(c2, color=C_ANSWER, buff=0.12)
            self.play(Create(bx), run_time=0.6)
            c2.add(bx)
            self.sync(tr, text, "Positive")
            self.add(parts)
            self.play(ang.animate.set_value(2 * PI), run_time=max(tr.get_remaining_duration(), 2.0), rate_func=linear)
        self.rest()
        for d in parts:
            d.clear_updaters()
        self.play(FadeOut(parts), run_time=0.4)

        # 6 — flux: normal vectors, crossing particles
        self.nb_clear()
        self.chapter(2, "Flux")
        normals = VGroup()
        for k in range(8):
            t = 2 * PI * k / 8 + PI / 8
            p = Q3(np.cos(t), np.sin(t))
            normals.add(Arrow(p, p + 0.7 * np.array([np.cos(t), np.sin(t), 0]), buff=0, color=C_NORMAL,
                              stroke_width=4, max_tip_length_to_length_ratio=0.3))
        n_lab = MathTex(r"\mathbf n", color=C_NORMAL, font_size=34).next_to(normals[1].get_end(), UP, buff=0.05)
        tq = PI / 3
        pq = Q3(np.cos(tq), np.sin(tq))
        Fq = np.array([*F_ex(np.cos(tq), np.sin(tq)), 0])
        nq = np.array([np.cos(tq), np.sin(tq), 0])
        Tq = np.array([-np.sin(tq), np.cos(tq), 0])
        sF = 0.9
        Fa = Arrow(pq, pq + sF * Fq, buff=0, color=WHITE, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        Fn = Arrow(pq, pq + sF * np.dot(Fq, nq) * nq, buff=0, color=C_NORMAL, stroke_width=6,
                   max_tip_length_to_length_ratio=0.3)
        Ft = Arrow(pq, pq + sF * np.dot(Fq, Tq) * Tq, buff=0, color=YELLOW, stroke_width=6,
                   max_tip_length_to_length_ratio=0.3)
        lab_n = MathTex(r"\mathbf F\cdot\mathbf n", color=C_NORMAL, font_size=30).next_to(Fn.get_end(), RIGHT, buff=0.08)
        lab_t = MathTex(r"\mathbf F\cdot\mathbf T", color=YELLOW, font_size=30).next_to(Ft.get_end(), UP, buff=0.08)
        sl2 = StreamLines(vel, x_range=[C3[0] - 3.4, C3[0] + 3.4, 0.5], y_range=[-3.6, 3.6, 0.5],
                          stroke_width=1.5, max_anchors_per_line=25, padding=0.3, virtual_time=3,
                          colors=[BLUE_E, BLUE_C, BLUE_A])
        fl = MathTex(r"\text{Flux}=\oint_C\mathbf F\cdot\mathbf n\,ds", font_size=36)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(vf), run_time=0.4)
            self.add(sl2)
            sl2.start_animation(warm_up=False, flow_speed=1.0, time_width=0.5)
            self.sync(tr, text, "along the outward normal")
            self.play(LaggedStart(*[GrowArrow(a) for a in normals], lag_ratio=0.05), FadeIn(n_lab), run_time=1.0)
            self.play(GrowArrow(Fa), run_time=0.6)
            self.play(GrowArrow(Fn), GrowArrow(Ft), FadeIn(lab_n), FadeIn(lab_t), run_time=0.8)
            self.sync(tr, text, "The flux of F")
            self.nb_add(fl)
            self.sync(tr, text, "Positive flux")
            self.nb_add(Tex("positive: net outflow $\\cdot$ negative: net inflow", font_size=30, color=GRAY_B),
                        gray=False)
            self.wait(tr.get_remaining_duration())
        self.play(sl2.end_animation(), run_time=1.0)
        self.remove(sl2)

        # 7 — two columns
        col = VGroup(VGroup(Tex("circulation", font_size=32, color=YELLOW),
                            Tex(r"$\mathbf F\cdot\mathbf T$ (tangential)", font_size=30)).arrange(DOWN, buff=0.15),
                     VGroup(Tex("flux", font_size=32, color=C_NORMAL),
                            Tex(r"$\mathbf F\cdot\mathbf n$ (normal)", font_size=30)).arrange(DOWN, buff=0.15))
        col.arrange(RIGHT, buff=0.8)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.nb_add(col, gray=False)
            self.play(Indicate(Ft), Indicate(col[0]), run_time=0.8)
            self.sync(tr, text, "Flux uses")
            self.play(Indicate(Fn), Indicate(col[1]), run_time=0.8)
        self.rest()
        self.play(FadeOut(VGroup(Fa, Fn, Ft, lab_n, lab_t)), run_time=0.4)

        # 8 — n = T x k, F.n ds = M dy - N dx
        self.nb_clear()
        m1 = MathTex(r"\mathbf n=\mathbf T\times\mathbf k=\frac{dy}{ds}\,\mathbf i-\frac{dx}{ds}\,\mathbf j", font_size=34)
        m2 = MathTex(r"\mathbf F\cdot\mathbf n\,ds=\Big(M\frac{dy}{ds}-N\frac{dx}{ds}\Big)ds", font_size=34)
        m2c = MathTex(r"\mathbf F\cdot\mathbf n\,ds=\Big(M\frac{dy}{\cancel{ds}}-N\frac{dx}{\cancel{ds}}\Big)\cancel{ds}",
                      r"=M\,dy-N\,dx", font_size=34, tex_template=CANCEL_TPL)
        k_sc = min(1.0, NB_W / m2c.width)
        m2.scale(k_sc)
        m2c.scale(k_sc)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "the outward normal is")
            self.nb_add(m1)
            self.sync(tr, text, "Then F dot n d s")
            self.nb_add(m2, gray=False)
            m2c.shift(m2.get_left() - m2c[0].get_left() + (m2.get_center()[1] - m2c[0].get_center()[1]) * UP)
            self.sync(tr, text, "The d s disappears")
            self.play(FadeOut(m2), FadeIn(m2c[0]), run_time=0.8)
            self.nb_items[-1] = m2c
            self.play(Write(m2c[1]), run_time=0.8)
        self.rest()

        # 9 — boxed flux formula
        ff = MathTex(r"\text{Flux of }\mathbf F\text{ across }C=\oint_C M\,dy-N\,dx\quad(\text{counterclockwise})",
                     font_size=34)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.nb_add(ff, buff=0.4)
            b = SurroundingRectangle(ff, color=YELLOW, buff=0.12)
            self.play(Create(b), run_time=0.6)
            ff.add(b)
        self.rest()

        # 10 — example flux = pi
        x1 = MathTex(r"M=\cos t-\sin t,\ N=\cos t,\ dy=\cos t\,dt,\ dx=-\sin t\,dt", font_size=32)
        x2 = MathTex(r"M\,dy-N\,dx=(\cos^2t-\sin t\cos t+\sin t\cos t)\,dt=\cos^2t\,dt", font_size=32)
        x3 = MathTex(r"\int_0^{2\pi}\cos^2t\,dt=\pi", font_size=36)
        x3b = Tex(r"positive $\to$ net outflow", font_size=30, color=C_ANSWER)
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "M is cos t")
            self.nb_add(x1)
            self.sync(tr, text, "M d y minus N d x simplifies")
            self.nb_add(x2)
            self.sync(tr, text, "Integrating over")
            self.nb_add(x3, buff=0.4)
            bx = SurroundingRectangle(x3, color=C_ANSWER, buff=0.12)
            self.play(Create(bx), run_time=0.6)
            x3.add(bx)
            self.sync(tr, text, "Positive, so")
            self.nb_add(x3b, gray=False)
            self.play(LaggedStart(*[Indicate(a, color=C_NORMAL) for a in normals], lag_ratio=0.05), run_time=1.0)
        self.rest()

        # 11 — engineering card
        eh = Tex("Engineering", font_size=40, color=YELLOW)
        ea = VGroup(MathTex(r"\oint\mathbf B\cdot d\mathbf r=\mu_0 I", font_size=40),
                    Tex(r"Amp\`ere's law (circulation)", font_size=28, color=GRAY_B)).arrange(DOWN, buff=0.15)
        eb = Tex(r"flux $=$ coolant / air leaving\\through a boundary", font_size=32)
        ec = Tex(r"next: 16.4 Green's theorem", font_size=30, color=ORANGE)
        ecard = card_left(self, VGroup(eh, ea, eb, ec).arrange(DOWN, buff=0.45))
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(ecard[0]), FadeIn(eh), run_time=0.6)
            self.play(FadeIn(ea), run_time=0.8)
            self.sync(tr, text, "And flux describes")
            self.play(FadeIn(eb), run_time=0.8)
            self.sync(tr, text, "In section sixteen point four")
            self.play(FadeIn(ec), run_time=0.8)
        self.rest()

        # 12 — summary
        self.summary(vo[12],
                     [r"Flow along $C$: $\int_C\mathbf F\cdot\mathbf T\,ds$ (same calculation as work).",
                      r"Closed curve: circulation $\oint_C\mathbf F\cdot\mathbf T\,ds$ measures swirling.",
                      r"Flux across a closed curve: $\oint_C M\,dy-N\,dx$ (counterclockwise), net outflow."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
#  Exercises — gradient fields (Ex 1, Ex 4)
# =============================================================================
VO["ex01"] = [
    "Exercise one from section sixteen point two. Find the gradient field of f equals x squared plus y squared plus z squared, to the power minus one half.",
    "First, understand the function. x squared plus y squared plus z squared is the squared distance to the origin, rho squared. To the power minus one half, that is one over rho. So f is one over the distance to the origin. It is large close to the origin, and small far away.",
    "The level surfaces of f are spheres around the origin. On each sphere the distance is constant, so f is constant.",
    "Pause and think: will the gradient point towards the origin, or away from it?",
    "f increases when we move towards the origin. The gradient points in the direction of fastest increase, so we expect arrows pointing inward, perpendicular to the spheres.",
    "Now the partial derivative with respect to x. Treat y and z as constants, and use the chain rule. The outer function is u to the power minus one half, with derivative minus one half, u to the power minus three halves. The inner function is x squared plus y squared plus z squared, and its x derivative is two x.",
    "Multiply: minus one half, times two x, times the bracket to the power minus three halves. The one half and the two cancel. So the x derivative is minus x, divided by x squared plus y squared plus z squared, to the power three halves.",
    "By symmetry, the y and z derivatives look exactly the same, with y and z on top. Nothing new to compute: just swap the letters.",
    "So the gradient field is minus, x i plus y j plus z k, divided by x squared plus y squared plus z squared, to the power three halves.",
    "Check our prediction. The vector x i plus y j plus z k points away from the origin, and the minus sign turns it around. So the arrows point inward. Prediction confirmed.",
    "How long are the arrows? The top has length rho, and the bottom is rho cubed. So the length is one over rho squared. This is an inverse square law.",
    "This is exactly the shape of gravity around a planet, and of the electric field around a point charge. The gravitational force of a point mass is a constant times this gradient field. Remember exercise fourteen of section sixteen point one: there, an inverse square function along a ray gave a finite result.",
    "Summary. One: to find a gradient field, take the three partial derivatives. Two: use the chain rule for a power of a bracket, and use symmetry to save work. Three: predict the direction first, and check it at the end.",
]

GRAD_CHECK = [r"1 $\partial f/\partial x$", r"2 $\partial f/\partial y$", r"3 $\partial f/\partial z$",
              r"4 $\nabla f$"]


def axes3d(U, rng=(-1.6, 1.6)):
    a, b = rng
    return ThreeDAxes(x_range=[a, b, 0.5], y_range=[a, b, 0.5], z_range=[a, b, 0.5],
                      x_length=(b - a) * U, y_length=(b - a) * U, z_length=(b - a) * U, tips=False,
                      axis_config={"stroke_color": GRAY_B, "stroke_width": 2})


def arrow3(p, q, color, width=4):
    return Arrow(p, q, buff=0, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.3)


class Ex16_2_01(ExerciseScene):
    PHI, THETA = 70 * DEGREES, -40 * DEGREES

    def construct(self):
        vo = VO["ex01"]
        PHI, THETA = self.PHI, self.THETA
        U = 1.5
        axes = axes3d(U)

        def P(x, y, z):
            return axes.c2p(x, y, z)

        fc = center_for(PHI, THETA, P(0, 0, 0), np.array([-3.4, -0.3, 0]))
        self.start("16.2 — Exercise 1", r"f(x,y,z)=(x^2+y^2+z^2)^{-1/2},\qquad \nabla f=\ ?",
                   phi=PHI, theta=THETA, frame_center=fc, checklist=GRAD_CHECK)
        ax_labels = VGroup(*[face_camera(MathTex(s, font_size=34), PHI, THETA).move_to(p) for s, p in
                             [("x", P(1.85, 0, 0)), ("y", P(0, 1.85, 0)), ("z", P(0, 0, 1.85))]])

        # 0
        self.intro(vo[0])

        # 1 — f = 1/rho, small graph (fixed in frame)
        g_ax = Axes(x_range=[0, 3, 1], y_range=[0, 3, 1], x_length=4.2, y_length=3.2, tips=False,
                    axis_config={"stroke_color": GRAY_B}).move_to([-3.4, 0.2, 0])
        g = g_ax.plot(lambda r: 1 / r, x_range=[1 / 3, 3], color=C_F, stroke_width=4)
        g_lab = MathTex(r"f=\tfrac1\rho", color=C_F, font_size=34).move_to(g_ax.c2p(1.1, 2.3))
        g_x = MathTex(r"\rho", font_size=30).next_to(g_ax.x_axis, RIGHT, buff=0.1)
        hi = Tex("large near $O$", font_size=26, color=GRAY_B).move_to(g_ax.c2p(1.0, 3.1))
        lo = Tex("small far away", font_size=26, color=GRAY_B).move_to(g_ax.c2p(2.4, 0.75))
        self.fixed(g_ax, g, g_lab, g_x, hi, lo)
        s1 = MathTex(r"x^2+y^2+z^2=\rho^2\ \Rightarrow\ f=(\rho^2)^{-1/2}=\dfrac1\rho", font_size=34)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "is the squared distance")
            self.nb_add(s1)
            self.sync(tr, text, "So f is one over")
            self.play(Create(g_ax), FadeIn(g_x), run_time=0.8)
            self.play(Create(g), FadeIn(g_lab), run_time=1.0)
            self.sync(tr, text, "It is large")
            self.play(FadeIn(hi), run_time=0.4)
            self.sync(tr, text, "and small far")
            self.play(FadeIn(lo), run_time=0.4)
        self.rest()
        self.play(FadeOut(VGroup(g_ax, g, g_lab, g_x, hi, lo)), run_time=0.5)

        # 2 — level spheres
        radii = [0.5, 1.0, 1.5]
        spheres = VGroup(*[Sphere(center=P(0, 0, 0), radius=r * U, resolution=(10, 20), fill_opacity=0.12,
                                  checkerboard_colors=[BLUE_D, BLUE_D], stroke_width=0.3, stroke_color=BLUE_B)
                           for r in radii])
        sph_lab = Tex(r"$f=$ constant", font_size=32, color=BLUE_B).move_to([-1.3, 2.6, 0])
        self.fixed(sph_lab)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(Create(axes), FadeIn(ax_labels), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(s) for s in spheres], lag_ratio=0.3), run_time=1.5)
            self.sync(tr, text, "so f is constant")
            self.play(FadeIn(sph_lab), run_time=0.5)
        self.rest()

        # 3 — pause
        self.pause(vo[3], r"Will $\nabla f$ point towards the origin, or away from it?")

        # 4 — prediction: inward arrows
        dirs = [np.array(d) / np.linalg.norm(d) for d in
                [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (1, 1, 1), (-1, 1, 1), (1, -1, 1)]]
        pred = VGroup(*[arrow3(P(*(1.5 * d)), P(*(1.05 * d)), YELLOW) for d in dirs])
        pred_lab = Tex("prediction", font_size=32, color=YELLOW).move_to([-1.3, 2.1, 0])
        self.fixed(pred_lab)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "so we expect")
            self.play(LaggedStart(*[GrowArrow(a) for a in pred], lag_ratio=0.1), FadeIn(pred_lab), run_time=1.5)
        self.rest()

        # 5 — chain rule set-up
        self.nb_clear()
        self.chapter(1, "Computation")
        self.show_checklist()
        c1 = MathTex(r"\frac{\partial f}{\partial x}=\frac{\partial}{\partial x}\big(u^{-1/2}\big),\quad u=x^2+y^2+z^2",
                     font_size=34)
        c2 = MathTex(r"\frac{d}{du}u^{-1/2}=-\tfrac12u^{-3/2},\qquad \frac{\partial u}{\partial x}=2x", font_size=34)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.nb_add(c1)
            self.sync(tr, text, "The outer function")
            self.nb_add(c2)
        self.rest()

        # 6 — multiply, cancel 1/2 and 2
        c3 = MathTex(r"\frac{\partial f}{\partial x}=-", r"\tfrac12", r"\cdot", r"2", r"x\cdot(x^2+y^2+z^2)^{-3/2}",
                     font_size=34)
        c4 = MathTex(r"\frac{\partial f}{\partial x}=-\frac{x}{(x^2+y^2+z^2)^{3/2}}", font_size=36)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_add(c3)
            self.sync(tr, text, "The one half and the two")
            self.play(Indicate(c3[1]), Indicate(c3[3]), run_time=0.8)
            self.strike(c3[1], owner=c3)
            self.strike(c3[3], owner=c3)
            self.sync(tr, text, "So the x derivative")
            self.nb_add(c4, buff=0.4)
            self.play(Indicate(c4), run_time=0.8)
        self.rest()

        # 7 — symmetry: swap the letters
        gy = MathTex(r"\frac{\partial f}{\partial y}=-\frac{y}{(\dots)^{3/2}}", font_size=36)
        gz = MathTex(r"\frac{\partial f}{\partial z}=-\frac{z}{(\dots)^{3/2}}", font_size=36)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            gx_copy = MathTex(r"\frac{\partial f}{\partial x}=-\frac{x}{(\dots)^{3/2}}", font_size=36)
            self.nb_add(gx_copy, gray=False, anim=FadeIn(gx_copy))
            gy.move_to(gx_copy, aligned_edge=LEFT)
            self.fixed(gy)
            self.play(ReplacementTransform(gx_copy, gy), run_time=1.0)
            self.nb_items[-1] = gy
            self.check_step(2)
            gz_copy = gy.copy()
            self.nb_add(gz_copy, gray=False, anim=FadeIn(gz_copy))
            gz.move_to(gz_copy, aligned_edge=LEFT)
            self.fixed(gz)
            self.play(ReplacementTransform(gz_copy, gz), run_time=1.0)
            self.nb_items[-1] = gz
            self.sync(tr, text, "just swap")
            swap = Tex("swap the letters", font_size=30, color=YELLOW)
            self.nb_add(swap, gray=False)
        self.rest()

        # 8 — answer
        ans = MathTex(r"\nabla f=-\dfrac{x\,\mathbf i+y\,\mathbf j+z\,\mathbf k}{(x^2+y^2+z^2)^{3/2}}", font_size=38)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(ans, buff=0.4)
            box = SurroundingRectangle(ans, color=C_ANSWER, buff=0.15)
            self.play(Create(box), run_time=0.6)
            ans.add(box)
        self.rest()

        # 9 — check: r points outward, minus sign flips
        p0 = np.array([0.75, 0.55, 0.65])
        out = arrow3(P(*p0), P(*(1.6 * p0)), GRAY, width=6)
        inw = arrow3(P(*p0), P(*(0.4 * p0)), C_NEG, width=6)
        o_lab = MathTex(r"x\,\mathbf i+y\,\mathbf j+z\,\mathbf k", font_size=28, color=GRAY_B)
        i_lab = MathTex(r"-(x\,\mathbf i+y\,\mathbf j+z\,\mathbf k)", font_size=28, color=C_NEG)
        tick = MathTex(r"\checkmark", font_size=46, color=C_ANSWER).next_to(pred_lab, RIGHT, buff=0.2)
        self.fixed(tick)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(pred), FadeOut(spheres[2]), run_time=0.5)
            o_lab.move_to(self.to_screen(P(*(1.7 * p0))) + np.array([0.3, 0.3, 0]))
            i_lab.move_to(self.to_screen(P(*(0.3 * p0))) + np.array([0.9, -0.5, 0]))
            self.fixed(o_lab, i_lab)
            self.play(GrowArrow(out), FadeIn(o_lab), run_time=1.0)
            self.sync(tr, text, "and the minus sign")
            self.play(ReplacementTransform(out.copy(), inw), FadeIn(i_lab), out.animate.set_opacity(0.3), run_time=1.2)
            self.sync(tr, text, "Prediction confirmed")
            self.play(FadeIn(tick, scale=1.5), run_time=0.5)
        self.rest()
        self.play(FadeOut(VGroup(out, inw, o_lab, i_lab)), run_time=0.5)

        # 10 — length 1/rho^2
        ln = MathTex(r"|\nabla f|=\frac{\rho}{\rho^3}=\frac{1}{\rho^2}", font_size=38)
        lens = VGroup()
        for d in dirs[:5]:
            for r in (0.7, 1.0, 1.5):
                L = 0.22 / r ** 2
                lens.add(arrow3(P(*(r * d)), P(*((r - L) * d)), C_NEG, width=4))
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.nb_add(ln)
            self.sync(tr, text, "So the length")
            self.play(LaggedStart(*[GrowArrow(a) for a in lens], lag_ratio=0.05), run_time=2.0)
            self.sync(tr, text, "inverse square")
            self.nb_add(Tex("inverse square law", font_size=30, color=YELLOW), gray=False)
        self.rest()

        # 11 — physics card
        planet = Circle(radius=0.8, fill_color=BLUE_E, fill_opacity=1, stroke_color=BLUE_B)
        inn = VGroup(*[Arrow(1.9 * np.array([np.cos(a), np.sin(a), 0]), 1.0 * np.array([np.cos(a), np.sin(a), 0]),
                             buff=0, color=C_NEG, stroke_width=4) for a in np.linspace(0, 2 * PI, 10, endpoint=False)])
        pic = VGroup(planet, inn)
        ph = Tex("Physics", font_size=40, color=YELLOW)
        pt = Tex(r"gravity of a point mass $=$ constant $\cdot\ \nabla(1/\rho)$", font_size=30)
        pr = Tex(r"cf.\ 16.1 Ex 14: inverse square along a ray $\to$ finite", font_size=26, color=GRAY_B)
        card = card_left(self, VGroup(ph, pic, pt, pr).arrange(DOWN, buff=0.35))
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(card), run_time=0.8)
            self.sync(tr, text, "Remember exercise")
            self.play(Indicate(pr), run_time=0.8)
        self.rest()

        # 12 — summary
        self.summary(vo[12],
                     [r"Gradient field: take the three partial derivatives.",
                      r"Chain rule for a power of a bracket; use symmetry to save work.",
                      r"Predict the direction first, check it at the end."],
                     ["One:", "Two:", "Three:"])


VO["ex04"] = [
    "Exercise four. Find the gradient field of g equals x y plus y z plus x z.",
    "This function has three terms, each a product of two coordinates. When we take a partial derivative, the other two coordinates are treated as constants.",
    "Partial derivative with respect to x. In x y, the y is a constant factor, so we get y. y z contains no x, so it gives zero. x z gives z. Together: y plus z.",
    "With respect to y: x y gives x, y z gives z, and x z gives zero. So we get x plus z.",
    "With respect to z: x y gives zero, y z gives y, and x z gives x. So we get x plus y.",
    "The gradient field is y plus z, i, plus x plus z, j, plus x plus y, k.",
    "Notice the pattern: each component is the sum of the other two coordinates. A quick check: at the point one, one, one, the gradient is two i plus two j plus two k, pointing along the diagonal.",
    "Here is the field at a few points of the unit cube.",
    "Keep this field in mind. In exercise twelve, we integrate exactly this field along three different paths, and something surprising happens.",
    "Summary. One: in a partial derivative, all other variables are constants. Two: terms without that variable give zero. Three: always check your result at one simple point.",
]

C_XY, C_YZ, C_XZ = BLUE, ORANGE, PINK


class Ex16_2_04(ExerciseScene):
    PHI, THETA = 70 * DEGREES, -50 * DEGREES

    def construct(self):
        vo = VO["ex04"]
        PHI, THETA = self.PHI, self.THETA
        U = 2.6
        axes = ThreeDAxes(x_range=[0, 1.4, 0.5], y_range=[0, 1.4, 0.5], z_range=[0, 1.4, 0.5],
                          x_length=1.4 * U, y_length=1.4 * U, z_length=1.4 * U, tips=False,
                          axis_config={"stroke_color": GRAY_B, "stroke_width": 2})

        def P(x, y, z):
            return axes.c2p(x, y, z)

        fc = center_for(PHI, THETA, P(0.5, 0.5, 0.5), np.array([-3.4, -0.2, 0]))
        prob = MathTex(r"g(x,y,z)=", "xy", "+", "yz", "+", "xz", r",\qquad \nabla g=\ ?", font_size=34)
        for i, c in [(1, C_XY), (3, C_YZ), (5, C_XZ)]:
            prob[i].set_color(c)
        self.start("16.2 — Exercise 4", prob, phi=PHI, theta=THETA, frame_center=fc, checklist=GRAD_CHECK)

        # 0
        self.intro(vo[0])

        # left: big g with coloured terms
        big = MathTex(r"g=", "xy", "+", "yz", "+", "xz", font_size=72).move_to([-3.3, 1.8, 0])
        for i, c in [(1, C_XY), (3, C_YZ), (5, C_XZ)]:
            big[i].set_color(c)
        self.fixed(big)

        # 1 — card: other variables constant
        rule = Tex(r"partial derivative:\\other variables $=$ constants", font_size=38, color=YELLOW)
        rule.move_to([-3.3, -0.6, 0])
        rbox = SurroundingRectangle(rule, color=YELLOW, buff=0.25, corner_radius=0.15)
        self.fixed(rule, rbox)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Write(big), run_time=1.2)
            self.sync(tr, text, "When we take")
            self.play(FadeIn(rule), Create(rbox), run_time=0.8)
        self.rest()
        self.play(FadeOut(rule), FadeOut(rbox), run_time=0.4)

        self.chapter(1, "Partial derivatives")
        self.show_checklist()

        def row(var, outs, res):
            # outs: list of (latex, colour) for the three terms
            parts = []
            for (term, col), o in zip([("xy", C_XY), ("yz", C_YZ), ("xz", C_XZ)], outs):
                parts.append((rf"\frac{{\partial}}{{\partial {var}}}({term})={o}", col if o != "0" else GRAY))
            m = MathTex(*[p for p, _ in parts], rf"\ \Rightarrow\ g_{var}={res}", font_size=30,
                        arg_separator=r",\ \ ")
            for k, (_, col) in enumerate(parts):
                m[k].set_color(col)
            return m

        specs = [("x", ["y", "0", "z"], "y+z", vo[2], ["In x y", "y z contains", "x z gives", "Together"]),
                 ("y", ["x", "z", "0"], "x+z", vo[3], ["x y gives", "y z gives", "and x z", "So we get"]),
                 ("z", ["0", "y", "x"], "x+y", vo[4], ["x y gives", "y z gives", "and x z", "So we get"])]
        results = []
        for k, (var, outs, res, text, phrases) in enumerate(specs):
            m = row(var, outs, res)
            if m.width > NB_W:
                m.scale_to_fit_width(NB_W)
            with self.voiceover(text=text) as tr:
                self.check_step(k)
                self.nb_add(m, anim=FadeIn(m[0]), gray=True)
                for j in range(3):
                    if j > 0:
                        self.sync(tr, text, phrases[j])
                        self.play(FadeIn(m[j]), run_time=0.5)
                    self.play(Indicate(big[2 * j + 1], color=m[j].get_color()), run_time=0.6)
                self.sync(tr, text, phrases[3])
                self.play(Write(m[3]), run_time=0.6)
            results.append(m)
            self.rest()

        # 5 — answer
        ans = MathTex(r"\nabla g=(y+z)\,\mathbf i+(x+z)\,\mathbf j+(x+y)\,\mathbf k", font_size=36)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(ans, buff=0.4)
            box = SurroundingRectangle(ans, color=C_ANSWER, buff=0.15)
            self.play(Create(box), run_time=0.6)
            ans.add(box)
        self.rest()

        # 6 — pattern + check at (1,1,1)
        patt = Tex("each component $=$ sum of the other two coordinates", font_size=30, color=YELLOW)
        chk = MathTex(r"\nabla g(1,1,1)=2\,\mathbf i+2\,\mathbf j+2\,\mathbf k", font_size=34)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_add(patt, gray=False)
            self.play(Indicate(ans), run_time=0.8)
            self.sync(tr, text, "A quick check")
            self.nb_add(chk, gray=False)
        self.rest()

        # 7 — the field on the unit cube (3D)
        cube = VGroup(*[Line(P(*a), P(*b), color=GRAY, stroke_width=2) for a, b in [
            ((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 1, 0)), ((1, 0, 0), (1, 1, 0)), ((0, 1, 0), (1, 1, 0)),
            ((0, 0, 1), (1, 0, 1)), ((0, 0, 1), (0, 1, 1)), ((1, 0, 1), (1, 1, 1)), ((0, 1, 1), (1, 1, 1)),
            ((0, 0, 0), (0, 0, 1)), ((1, 0, 0), (1, 0, 1)), ((0, 1, 0), (0, 1, 1)), ((1, 1, 0), (1, 1, 1))]])
        ax_labels = VGroup(*[face_camera(MathTex(s, font_size=34), PHI, THETA).move_to(p) for s, p in
                             [("x", P(1.55, 0, 0)), ("y", P(0, 1.55, 0)), ("z", P(0, 0, 1.55))]])
        pts = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (0.5, 0.5, 0.5), (0.5, 0, 0.5),
               (0, 0.5, 0.5), (0.5, 0.5, 0), (1, 1, 1)]
        K = 0.16
        arrs = VGroup()
        for p in pts:
            x, y, z = p
            v = np.array([y + z, x + z, x + y])
            col = YELLOW if p == (1, 1, 1) else BLUE_B
            arrs.add(arrow3(P(*p), P(*(np.array(p) + K * v)), col, width=5 if p == (1, 1, 1) else 3))
        diag = DashedLine(P(0, 0, 0), P(1.35, 1.35, 1.35), color=YELLOW, stroke_width=2, stroke_opacity=0.6)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(big), run_time=0.4)
            self.play(Create(axes), FadeIn(ax_labels), Create(cube), run_time=1.2)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.08), run_time=2.0)
            self.play(Create(diag), Indicate(arrs[-1]), run_time=1.0)
        self.rest()
        for th in (THETA + 25 * DEGREES, THETA):
            self.move_camera(theta=th, frame_center=center_for(PHI, th, P(0.5, 0.5, 0.5), np.array([-3.4, -0.2, 0])),
                             run_time=2.5)

        # 8 — teaser
        tz = Tex(r"Exercise 12: integrate this field\\along three different paths\dots", font_size=38, color=YELLOW)
        card = card_left(self, tz)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "In exercise twelve")
            self.play(FadeIn(card), run_time=0.6)
        self.rest()

        # 9 — summary
        self.summary(vo[9],
                     [r"In a partial derivative, all other variables are constants.",
                      r"Terms without that variable give $0$.",
                      r"Always check your result at one simple point."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
#  Exercise 12 — one field, three paths
# =============================================================================
VO["ex12"] = [
    "Exercise twelve. Find the line integral of F equals y plus z, i, plus z plus x, j, plus x plus y, k, from the origin to the point one, one, one, along three different paths.",
    "Path a, C one: the straight line r of t equals t i plus t j plus t k. Path b, C two: the curve r of t equals t i plus t squared j plus t to the fourth k. Path c: first from the origin to one, one, zero, and then straight up to one, one, one.",
    "Think of F as a force, and of the integral as the work done when an object moves from the start to the end point. For each path we use the same method: substitute the path into F, compute r prime, take the dot product, and integrate.",
    "Pause and think: will the three paths give the same work?",
    "Path a. On C one, x, y and z are all equal to t. So every component of F becomes t plus t, which is two t. F of r of t equals two t i, plus two t j, plus two t k.",
    "r prime of t equals i plus j plus k.",
    "The dot product: two t plus two t plus two t, which is six t.",
    "Integrate from zero to one: six t gives three t squared, which is three. The work along path a is three.",
    "Path b. Now x equals t, y equals t squared, and z equals t to the fourth. Substitute carefully. The i component, y plus z, becomes t squared plus t to the fourth. The j component, z plus x, becomes t to the fourth plus t. The k component, x plus y, becomes t plus t squared.",
    "r prime of t equals i plus two t j plus four t cubed k.",
    "The dot product, term by term. The first term is t squared plus t to the fourth. The second is two t, times t to the fourth plus t, which is two t to the fifth plus two t squared. The third is four t cubed, times t plus t squared, which is four t to the fourth plus four t to the fifth.",
    "Collect equal powers. The t squared terms give three t squared. The t to the fourth terms give five t to the fourth. And the t to the fifth terms give six t to the fifth.",
    "Integrate from zero to one. Three t squared gives one. Five t to the fourth gives one. Six t to the fifth gives one. Total: three. The same as path a!",
    "Path c has two pieces, so we split the integral. C three goes from the origin to one, one, zero: r of t equals t i plus t j, with z equal to zero. Then F becomes t i plus t j plus two t k, and r prime is i plus j. The dot product is t plus t, which is two t. Integrating from zero to one gives one.",
    "C four goes straight up, from one, one, zero to one, one, one: r of t equals i plus j plus t k. Here r prime is just k, so only the k component of F counts. That is x plus y, which equals two. Integrating two from zero to one gives two.",
    "Add the pieces: one plus two is three. Again three!",
    "Three different paths, three times the same answer. That is no coincidence. In exercise four, we found that this F is the gradient of g equals x y plus y z plus x z. For a gradient field, the work only depends on the start and end points: g at one, one, one, minus g at zero, zero, zero, which is three minus zero.",
    "This is called path independence, and fields like this are called conservative. It is the main topic of section sixteen point three. For a field that is not a gradient, different paths usually give different answers. You will see that in homework exercise eleven.",
    "Summary. One: for each path, substitute, differentiate, take the dot product, and integrate. Two: for a path in pieces, add the integrals; on a vertical piece, only the k component counts. Three: if F is a gradient field, the work depends only on the end points.",
]

WORK_CHECK = [r"1 $\mathbf F(\mathbf r(t))$", r"2 $\mathbf r'(t)$", r"3 $\mathbf F\cdot\mathbf r'$", "4 integrate"]
C_I, C_J, C_K = TEAL, ORANGE, PINK


class Ex16_2_12(ExerciseScene):
    PHI, THETA = 65 * DEGREES, -50 * DEGREES

    def construct(self):
        vo = VO["ex12"]
        PHI, THETA = self.PHI, self.THETA
        U = 2.6
        axes = ThreeDAxes(x_range=[0, 1.4, 0.5], y_range=[0, 1.4, 0.5], z_range=[0, 1.4, 0.5],
                          x_length=1.4 * U, y_length=1.4 * U, z_length=1.4 * U, tips=False,
                          axis_config={"stroke_color": GRAY_B, "stroke_width": 2})

        def P(x, y, z):
            return axes.c2p(x, y, z)

        SCR = np.array([-3.4, -0.3, 0])
        fc = center_for(PHI, THETA, P(0.5, 0.5, 0.5), SCR)
        prob = VGroup(MathTex(r"\mathbf F=(y+z)\,\mathbf i+(z+x)\,\mathbf j+(x+y)\,\mathbf k", font_size=30),
                      MathTex(r"\text{from }(0,0,0)\text{ to }(1,1,1)\text{ along three paths}", font_size=28)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        self.start("16.2 — Exercise 12", prob, phi=PHI, theta=THETA, frame_center=fc, checklist=WORK_CHECK)
        ax_labels = VGroup(*[face_camera(MathTex(s, font_size=34), PHI, THETA).move_to(p) for s, p in
                             [("x", P(1.55, 0, 0)), ("y", P(0, 1.55, 0)), ("z", P(0, 0, 1.55))]])

        # scoreboard at the bottom of the notebook
        self.nb_bottom = -2.55
        heads = ["path a", "path b", "path c"]
        sb_cells = VGroup()
        sb = VGroup()
        for k, h in enumerate(heads):
            col = VGroup(Tex(h, font_size=28, color=[YELLOW, C_CURVE, C_NEG][k]),
                         MathTex("?", font_size=36, color=GRAY_B)).arrange(DOWN, buff=0.15)
            sb.add(col)
        sb.arrange(RIGHT, buff=0.9)
        sb_frame = SurroundingRectangle(sb, color=GRAY_B, buff=0.2, corner_radius=0.1)
        board = VGroup(sb_frame, sb).move_to([(NB_LEFT + NB_RIGHT) / 2, -3.15, 0])
        self.fixed(board)

        def score(k):
            new = MathTex("3", font_size=40, color=C_ANSWER).move_to(sb[k][1])
            self.fixed(new)
            self.play(Transform(sb[k][1], new), run_time=0.6)
            self.play(Indicate(sb[k]), run_time=0.6)

        # 0
        self.add(axes, ax_labels)
        with self.voiceover(text=vo[0]) as tr:
            self.play(Write(self.title_mob), run_time=1.2)
            self.play(Write(self.problem_mob), run_time=2.5)
            self.play(FadeIn(board), run_time=0.6)
        self.rest()

        # 1 — three paths
        C1 = Line(P(0, 0, 0), P(1, 1, 1), color=YELLOW, stroke_width=6)
        C2 = ParametricFunction(lambda t: P(t, t * t, t ** 4), t_range=[0, 1], color=C_CURVE, stroke_width=6)
        C3 = Line(P(0, 0, 0), P(1, 1, 0), color=C_NEG, stroke_width=6)
        C4 = DashedLine(P(1, 1, 0), P(1, 1, 1), color=C_NEG, stroke_width=6)
        labs = [MathTex(s, font_size=32, color=c) for s, c in
                [("C_1", YELLOW), ("C_2", C_CURVE), ("C_3", C_NEG), ("C_4", C_NEG)]]
        anchor = [P(0.45, 0.45, 0.62), P(0.75, 0.42, 0.18), P(0.6, 0.6, 0), P(1, 1, 0.5)]
        offs = [np.array([-0.35, 0.2, 0]), np.array([0.35, -0.2, 0]), np.array([0.1, -0.35, 0]),
                np.array([0.35, 0, 0])]
        f1 = MathTex(r"C_1:\ \mathbf r=t\,\mathbf i+t\,\mathbf j+t\,\mathbf k", font_size=32, color=YELLOW)
        f2 = MathTex(r"C_2:\ \mathbf r=t\,\mathbf i+t^2\,\mathbf j+t^4\,\mathbf k", font_size=32, color=C_CURVE)
        f3 = MathTex(r"C_3\cup C_4:\ (0,0,0)\to(1,1,0)\to(1,1,1)", font_size=32, color=C_NEG)
        f0 = MathTex(r"0\le t\le 1", font_size=30, color=GRAY_B)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            for i, (c, f, ph) in enumerate([(C1, f1, "Path a"), (C2, f2, "Path b"), (None, f3, "Path c")]):
                self.sync(tr, text, ph)
                self.nb_add(f, gray=False)
                if c is not None:
                    labs[i].move_to(self.to_screen(anchor[i]) + offs[i])
                    self.fixed(labs[i])
                    self.play(Create(c), FadeIn(labs[i]), run_time=1.5)
                else:
                    for j in (2, 3):
                        labs[j].move_to(self.to_screen(anchor[j]) + offs[j])
                        self.fixed(labs[j])
                    self.play(Create(C3), FadeIn(labs[2]), run_time=1.0)
                    self.play(Create(C4), FadeIn(labs[3]), run_time=1.0)
            self.nb_add(f0, gray=False)
        self.rest()

        # 2 — a few field arrows, checklist
        K = 0.13
        arrs = VGroup()
        for p in [(0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5), (1, 0, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 0.5),
                  (0.5, 1, 1), (1, 0.5, 1)]:
            x, y, z = p
            v = np.array([y + z, z + x, x + y])
            arrs.add(arrow3(P(*p), P(*(np.array(p) + K * v)), GRAY_B, width=3))
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.08), run_time=1.5)
            self.sync(tr, text, "For each path")
            self.show_checklist()
            for k in range(4):
                self.play(Indicate(self.checklist[k], color=YELLOW), run_time=0.5)
        self.rest()
        self.play(arrs.animate.set_opacity(0.25), run_time=0.4)

        # 3 — pause
        self.pause(vo[3], "Will the three paths give the same work?")

        def run_dot(func, color, rt=2.0):
            u = ValueTracker(0.0)
            d = Dot(func(0), radius=0.1, color=WHITE)
            d.add_updater(lambda m: m.move_to(func(u.get_value())))
            self.add(d)
            self.play(u.animate.set_value(1.0), run_time=rt, rate_func=smooth)
            d.clear_updaters()
            return d

        def step(text, mob, k=None, buff=0.3, gray=True):
            with self.voiceover(text=text) as tr:
                if k is not None:
                    self.check_step(k)
                self.nb_add(mob, buff=buff, gray=gray)
            self.rest()

        # 4-7 — path a
        self.nb_clear()
        self.chapter(1, "Path a")
        a4 = MathTex(r"x=y=z=t\ \Rightarrow\ \mathbf F(\mathbf r(t))=2t\,\mathbf i+2t\,\mathbf j+2t\,\mathbf k",
                     font_size=32)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.play(C2.animate.set_stroke(opacity=0.25), C3.animate.set_stroke(opacity=0.25),
                      C4.animate.set_stroke(opacity=0.25), run_time=0.4)
            dot = run_dot(lambda s: P(s, s, s), YELLOW)
            self.sync(tr, text, "So every component")
            self.nb_add(a4)
        self.rest()
        step(vo[5], MathTex(r"\mathbf r'(t)=\mathbf i+\mathbf j+\mathbf k", font_size=34), k=1)
        step(vo[6], MathTex(r"\mathbf F\cdot\mathbf r'=2t+2t+2t=6t", font_size=34), k=2)
        a7 = MathTex(r"\int_0^1 6t\,dt=\big[3t^2\big]_0^1=3", font_size=36)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(a7, buff=0.4)
            bx = SurroundingRectangle(a7, color=C_ANSWER, buff=0.12)
            self.play(Create(bx), run_time=0.5)
            a7.add(bx)
            self.sync(tr, text, "The work along path a")
            score(0)
        self.rest()
        self.play(FadeOut(dot), run_time=0.3)

        # 8-12 — path b
        self.nb_clear()
        self.chapter(2, "Path b")
        self.play(C1.animate.set_stroke(opacity=0.25), C2.animate.set_stroke(opacity=1), run_time=0.4)
        for c in self.checklist:
            c.set_color(GRAY_B)
        b8 = VGroup(MathTex(r"y+z=t^2+t^4", font_size=32, color=C_I),
                    MathTex(r"z+x=t^4+t", font_size=32, color=C_J),
                    MathTex(r"x+y=t+t^2", font_size=32, color=C_K)).arrange(RIGHT, buff=0.45)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            dot = run_dot(lambda s: P(s, s * s, s ** 4), C_CURVE)
            self.sync(tr, text, "The i component")
            self.nb_add(b8, anim=FadeIn(b8[0]), gray=False)
            self.sync(tr, text, "The j component")
            self.play(FadeIn(b8[1]), run_time=0.6)
            self.sync(tr, text, "The k component")
            self.play(FadeIn(b8[2]), run_time=0.6)
        self.rest()
        b9 = MathTex(r"\mathbf r'(t)=", r"\mathbf i", "+", r"2t\,\mathbf j", "+", r"4t^3\,\mathbf k", font_size=34)
        b9[1].set_color(C_I)
        b9[3].set_color(C_J)
        b9[5].set_color(C_K)
        step(vo[9], b9, k=1)
        b10a = MathTex(r"\mathbf F\cdot\mathbf r'=", r"(t^2+t^4)", "+", r"2t(t^4+t)", "+", r"4t^3(t+t^2)",
                       font_size=32)
        b10b = MathTex(r"=", r"t^2", r"+t^4", r"+2t^5", r"+2t^2", r"+4t^4", r"+4t^5", font_size=34)
        for m, idx in [(b10a, [(1, C_I), (3, C_J), (5, C_K)]),
                       (b10b, [(1, C_I), (2, C_I), (3, C_J), (4, C_J), (5, C_K), (6, C_K)])]:
            for i, c in idx:
                m[i].set_color(c)
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.nb_add(b10a, anim=FadeIn(b10a[0]))
            for i, ph in [(1, "The first term"), (3, "The second is"), (5, "The third is")]:
                self.sync(tr, text, ph)
                if i > 1:
                    self.play(FadeIn(b10a[i - 1]), run_time=0.2)
                self.play(FadeIn(b10a[i]), run_time=0.5)
            self.nb_add(b10b, anim=FadeIn(VGroup(b10b[0], b10b[1], b10b[2])), gray=False)
            self.sync(tr, text, "which is two t to the fifth")
            self.play(FadeIn(b10b[3]), FadeIn(b10b[4]), run_time=0.6)
            self.sync(tr, text, "which is four t to the fourth")
            self.play(FadeIn(b10b[5]), FadeIn(b10b[6]), run_time=0.6)
        self.rest()
        b11 = MathTex(r"=", r"3t^2", r"+5t^4", r"+6t^5", font_size=36)
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.nb_add(b11, anim=FadeIn(b11[0]))
            for j, (src, ph) in enumerate([((1, 4), "The t squared"), ((2, 5), "The t to the fourth terms"),
                                          ((3, 6), "And the t to the fifth")]):
                self.sync(tr, text, ph)
                self.play(*[Indicate(b10b[i]) for i in src], run_time=0.6)
                cps = [b10b[i].copy() for i in src]
                self.fixed(*cps)
                self.play(*[Transform(c, b11[j + 1].copy()) for c in cps], run_time=0.9)
                self.remove(*cps)
                self.add(b11[j + 1])
        self.rest()
        b12 = MathTex(r"\int_0^1(3t^2+5t^4+6t^5)\,dt=\big[t^3+t^5+t^6\big]_0^1=1+1+1=3", font_size=32)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(b12, buff=0.4)
            self.sync(tr, text, "Total: three")
            bx = SurroundingRectangle(b12, color=C_ANSWER, buff=0.12)
            self.play(Create(bx), run_time=0.5)
            b12.add(bx)
            score(1)
        self.rest()
        self.play(FadeOut(dot), run_time=0.3)

        # 13-15 — path c
        self.nb_clear()
        self.chapter(3, "Path c")
        self.play(C2.animate.set_stroke(opacity=0.25), C3.animate.set_stroke(opacity=1),
                  C4.animate.set_stroke(opacity=1), run_time=0.4)
        for c in self.checklist:
            c.set_color(GRAY_B)
        c13a = MathTex(r"C_3:\ \mathbf r=t\,\mathbf i+t\,\mathbf j,\ \ \mathbf F=t\,\mathbf i+t\,\mathbf j+2t\,\mathbf k,"
                       r"\ \ \mathbf r'=\mathbf i+\mathbf j", font_size=30)
        c13b = MathTex(r"\mathbf F\cdot\mathbf r'=2t,\quad \int_0^1 2t\,dt=1", font_size=34)
        text = vo[13]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "C three goes")
            dot = run_dot(lambda s: P(s, s, 0), C_NEG, rt=1.5)
            self.check_step(0)
            self.nb_add(c13a)
            self.sync(tr, text, "The dot product")
            self.check_step(2)
            self.nb_add(c13b)
        self.rest()
        c14a = MathTex(r"C_4:\ \mathbf r=\mathbf i+\mathbf j+t\,\mathbf k,\ \ \mathbf r'=\mathbf k", font_size=32)
        c14b = MathTex(r"\mathbf F=", r"(y+z)\,\mathbf i", "+", r"(z+x)\,\mathbf j", "+", r"(x+y)\,\mathbf k",
                       font_size=32)
        c14c = MathTex(r"\mathbf F\cdot\mathbf r'=x+y=2,\quad \int_0^1 2\,dt=2", font_size=34)
        dnc = Tex(r"do not count: $\mathbf r'=\mathbf k$", font_size=26, color=GRAY)
        text = vo[14]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(dot), run_time=0.2)
            dot = run_dot(lambda s: P(1, 1, s), C_NEG, rt=1.5)
            self.nb_add(c14a)
            self.sync(tr, text, "so only the k component")
            self.nb_add(c14b, gray=False)
            self.play(c14b[1].animate.set_color(GRAY), c14b[3].animate.set_color(GRAY),
                      c14b[5].animate.set_color(C_K), run_time=0.6)
            dnc.next_to(c14b, DOWN, aligned_edge=LEFT, buff=0.1)
            self.fixed(dnc)
            self.play(FadeIn(dnc), run_time=0.4)
            c14b.add(dnc)
            self.sync(tr, text, "That is x plus y")
            self.nb_add(c14c)
        self.rest()
        c15 = MathTex(r"\int_{C_3\cup C_4}=1+2=3", font_size=38)
        text = vo[15]
        with self.voiceover(text=text) as tr:
            self.nb_add(c15, buff=0.4)
            bx = SurroundingRectangle(c15, color=C_ANSWER, buff=0.12)
            self.play(Create(bx), run_time=0.5)
            c15.add(bx)
            score(2)
            self.play(Indicate(board, color=C_ANSWER), run_time=1.0)
        self.rest()
        self.play(FadeOut(dot), C1.animate.set_stroke(opacity=1), C2.animate.set_stroke(opacity=1), run_time=0.5)

        # 16 — why always three
        self.nb_clear()
        self.chapter(4, "Why always three?")
        w1 = MathTex(r"\mathbf F=\nabla g,\ \ g=xy+yz+xz\quad(\text{Exercise 4})", font_size=34)
        w2 = MathTex(r"\int_C\mathbf F\cdot d\mathbf r=g(1,1,1)-g(0,0,0)=3-0=3", font_size=34)
        text = vo[16]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "In exercise four")
            self.nb_add(w1)
            self.sync(tr, text, "For a gradient field")
            self.nb_add(w2, buff=0.4)
            bx = SurroundingRectangle(w2, color=YELLOW, buff=0.12)
            self.play(Create(bx), run_time=0.5)
            w2.add(bx)
        self.rest()

        # 17 — teaser card
        t1 = Tex(r"path independence $\cdot$ conservative fields $\to$ 16.3", font_size=36, color=YELLOW)
        t2 = Tex(r"not a gradient field $\to$ paths usually differ (try HW 11)", font_size=28, color=GRAY_B)
        card = card_left(self, VGroup(t1, t2).arrange(DOWN, buff=0.4))
        text = vo[17]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(card[0]), FadeIn(t1), run_time=0.6)
            self.sync(tr, text, "For a field that is not")
            self.play(FadeIn(t2), run_time=0.6)
        self.rest()

        # 18 — summary
        self.summary(vo[18],
                     [r"Each path: substitute, differentiate, dot product, integrate.",
                      r"Path in pieces: add the integrals; vertical piece: only the $\mathbf k$ component counts.",
                      r"$\mathbf F$ a gradient field $\Rightarrow$ the work depends only on the end points."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
#  Exercises 25 and 15 — line integrals in the plane (2D)
# =============================================================================
VO["ex25"] = [
    "Exercise twenty five. Evaluate the integral of F dot T, d s, for the vector field F equals x squared i minus y j, along the curve x equals y squared, from the point four, two, to the point one, minus one.",
    "First, the curve. x equals y squared is a parabola that opens to the right. We start at four, two, at the top, move through the origin, and end at one, minus one. The direction matters, so we draw arrows.",
    "Next, the field. F equals x squared i minus y j. Here are the arrows along the curve. Green means the field points along our direction of motion and helps us. Red means it points against the motion.",
    "Remember from the intro: F dot T d s is the same as F dot d r. So we need neither T, nor the length of r prime.",
    "Since x is given as a function of y, the easiest parameter is y itself. Let y equal t. Then x equals t squared. So r of t equals t squared i plus t j.",
    "Pause and think: what are the limits for t?",
    "We start at y equals two and end at y equals minus one. So t runs from two down to minus one, and the integral goes from two to minus one. The lower limit is larger than the upper limit, and that is fine: it encodes the direction of motion.",
    "Step one: F of r of t. x squared becomes t to the fourth, and minus y becomes minus t. So F of r of t equals t to the fourth i minus t j.",
    "Step two: r prime of t equals two t i plus j.",
    "Step three: the dot product. t to the fourth times two t is two t to the fifth. Minus t times one is minus t. So F dot r prime equals two t to the fifth minus t.",
    "In the other notation, this is the integral of x squared d x minus y d y. With x equals t squared, d x equals two t d t, and d y equals d t. Substituting gives the same integrand.",
    "Step four: integrate from two to minus one. The antiderivative is t to the sixth over three, minus t squared over two.",
    "At t equals minus one: one third minus one half, which is minus one sixth. At t equals two: sixty four thirds minus two, which is fifty eight thirds.",
    "Upper limit minus lower limit: minus one sixth, minus fifty eight thirds. In sixths: minus one sixth minus one hundred sixteen sixths, which is minus one hundred seventeen sixths. That simplifies to minus thirty nine halves.",
    "The answer is negative. Overall, the field works against the motion along this path, just as the many red arrows suggested.",
    "The most common mistake: integrating from minus one to two instead of from two to minus one. That traces the curve in the opposite direction, and gives plus thirty nine halves. Wrong sign.",
    "If you prefer increasing limits, use t equals minus y instead. Then t runs from minus two to one, and you get the same answer, minus thirty nine halves. A good way to check your work.",
    "Summary. One: F dot T d s equals F dot d r, so you only need r prime of t. Two: if x is given as a function of y, use y as the parameter. Three: the limits follow the direction of motion, even when they run from large to small.",
]


class Ex16_2_25(FlatScene):
    def construct(self):
        vo = VO["ex25"]
        ax = Axes(x_range=[-0.5, 4.5, 1], y_range=[-1.5, 2.5, 1], x_length=6.5, y_length=5.2, tips=False,
                  axis_config={"stroke_color": GRAY_B, "include_numbers": True, "font_size": 22}).move_to([-3.4, -0.4, 0])
        ax_l = VGroup(MathTex("x", font_size=30).next_to(ax.x_axis, RIGHT, buff=0.1),
                      MathTex("y", font_size=30).next_to(ax.y_axis, UP, buff=0.1))

        def A(x, y):
            return ax.c2p(x, y)

        self.start("16.2 — Exercise 25",
                   VGroup(MathTex(r"\int_C\mathbf F\cdot\mathbf T\,ds,\quad \mathbf F=x^2\,\mathbf i-y\,\mathbf j",
                                  font_size=30),
                          MathTex(r"C:\ x=y^2\ \text{ from }(4,2)\text{ to }(1,-1)", font_size=30)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
                   checklist=WORK_CHECK)

        # 0
        self.intro(vo[0])

        # 1 — the curve with direction
        full = ParametricFunction(lambda s: A(s * s, s), t_range=[-1.5, 2.1], color=GRAY, stroke_width=2,
                                  stroke_opacity=0.6)
        piece = ParametricFunction(lambda u: A((2 - 3 * u) ** 2, 2 - 3 * u), t_range=[0, 1], color=C_CURVE,
                                   stroke_width=6)
        tips = dir_tips([1.5, 0.5, -0.5], reverse=True, func=lambda s: (s * s, s), to=A)
        pts = VGroup(Dot(A(4, 2), color=WHITE), Dot(A(1, -1), color=WHITE))
        plab = VGroup(MathTex("(4,2)", font_size=28).next_to(A(4, 2), LEFT, buff=0.15),
                      MathTex("(1,-1)", font_size=28).next_to(A(1, -1), RIGHT, buff=0.15))
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Create(ax), FadeIn(ax_l), run_time=1.0)
            self.sync(tr, text, "is a parabola")
            self.play(Create(full), run_time=1.0)
            self.sync(tr, text, "We start at")
            self.play(FadeIn(pts[0]), FadeIn(plab[0]), run_time=0.4)
            self.play(Create(piece), run_time=2.0)
            self.play(FadeIn(pts[1]), FadeIn(plab[1]), run_time=0.4)
            self.sync(tr, text, "so we draw arrows")
            self.play(FadeIn(tips), run_time=0.5)
        self.rest()

        # 2 — the field, arrows on the curve coloured by F.T
        def fsc(p):
            x, y = ax.p2c(p)
            return np.array([x * x, -y, 0.0])
        bg = ArrowVectorField(fsc, x_range=[ax.c2p(-0.25, 0)[0], ax.c2p(4.3, 0)[0], 0.65],
                              y_range=[ax.c2p(0, -1.3)[1], ax.c2p(0, 2.3)[1], 0.65],
                              length_func=lambda n: 0.5 * n / (n + 2.0))
        bg.set_opacity(0.25)
        on = VGroup()
        for s in [2.0, 1.6, 1.2, 0.8, 0.4, -0.4, -0.8]:
            x, y = s * s, s
            Fv = np.array([x * x, -y])
            mv = -np.array([2 * s, 1.0])          # direction of motion (t decreasing)
            good = np.dot(Fv, mv) > 0
            L = 0.75 * np.linalg.norm(Fv) / (np.linalg.norm(Fv) + 2.0)
            d = Fv / np.linalg.norm(Fv)
            on.add(Arrow(A(x, y), A(x, y) + L * np.array([*d, 0]) * 1.3, buff=0, stroke_width=5,
                         color=C_PROJ if good else C_NEG, max_tip_length_to_length_ratio=0.3))
        leg = VGroup(Tex("green: helps the motion", font_size=26, color=C_PROJ),
                     Tex("red: against the motion", font_size=26, color=C_NEG)).arrange(DOWN, aligned_edge=LEFT)
        leg.move_to([-1.8, 2.9, 0])
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(bg), run_time=0.8)
            self.sync(tr, text, "Here are the arrows")
            self.play(LaggedStart(*[GrowArrow(a) for a in on], lag_ratio=0.1), run_time=1.5)
            self.sync(tr, text, "Green means")
            self.play(FadeIn(leg[0]), run_time=0.4)
            self.sync(tr, text, "Red means")
            self.play(FadeIn(leg[1]), run_time=0.4)
        self.rest()

        # 3 — F.T ds = F.dr
        step3 = MathTex(r"\mathbf F\cdot\mathbf T\,ds=\mathbf F\cdot d\mathbf r\quad(\text{intro video 2})", font_size=34)
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.nb_add(step3)
        self.rest()

        # 4 — parametrise
        self.chapter(1, "Parametrise")
        self.show_checklist()
        s4 = MathTex(r"y=t,\ x=t^2\ \Rightarrow\ \mathbf r(t)=t^2\,\mathbf i+t\,\mathbf j", font_size=34)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Let y equal t")
            self.nb_add(s4)
        self.rest()

        # 5 — pause
        self.pause(vo[5], "What are the limits for $t$?")

        # 6 — t: 2 -> -1, live label
        tt = ValueTracker(2.0)
        dot = Dot(A(4, 2), radius=0.09, color=YELLOW)
        dot.add_updater(lambda m: m.move_to(A(tt.get_value() ** 2, tt.get_value())))
        tnum = DecimalNumber(2.0, num_decimal_places=2, font_size=30, color=YELLOW)
        tlab = VGroup(MathTex("t=", font_size=30, color=YELLOW), tnum).arrange(RIGHT, buff=0.08)
        tlab.add_updater(lambda m: m.next_to(dot, LEFT, buff=0.2))
        tnum.add_updater(lambda m: m.set_value(tt.get_value()))
        s6 = MathTex(r"t:\ ", r"2", r"\ \to\ ", r"-1", r"\qquad \int_{2}^{-1}\dots\,dt", font_size=36)
        st_lab = Tex("start", font_size=26, color=YELLOW)
        en_lab = Tex("end", font_size=26, color=YELLOW)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(dot), FadeIn(tlab), run_time=0.4)
            self.play(tt.animate.set_value(-1.0), run_time=3.0, rate_func=linear)
            self.sync(tr, text, "So t runs")
            self.nb_add(s6, gray=False)
            st_lab.next_to(s6[1], DOWN, buff=0.12)
            en_lab.next_to(s6[3], DOWN, buff=0.12)
            self.play(Indicate(s6[1]), FadeIn(st_lab), run_time=0.7)
            self.play(Indicate(s6[3]), FadeIn(en_lab), run_time=0.7)
            s6.add(st_lab, en_lab)
            self.sync(tr, text, "it encodes the direction")
            self.play(Indicate(tips), run_time=0.8)
        self.rest()
        tlab.clear_updaters()
        tnum.clear_updaters()
        self.play(FadeOut(tlab), run_time=0.3)

        # 7-9 — the three steps
        s7 = MathTex(r"\mathbf F(\mathbf r(t))=t^4\,\mathbf i-t\,\mathbf j", font_size=34)
        s8 = MathTex(r"\mathbf r'(t)=2t\,\mathbf i+\mathbf j", font_size=34)
        s9 = MathTex(r"\mathbf F\cdot\mathbf r'=t^4\cdot2t+(-t)\cdot1=", r"2t^5-t", font_size=34)
        s9[1].set_color(YELLOW)
        for k, (txt, m) in enumerate([(vo[7], s7), (vo[8], s8), (vo[9], s9)]):
            with self.voiceover(text=txt) as tr:
                self.check_step(k)
                self.nb_add(m)
            self.rest()

        # 9b — other notation
        s9b = MathTex(r"\int_C x^2\,dx-y\,dy,\ \ dx=2t\,dt,\ dy=dt\ \Rightarrow\ ", r"(t^4\cdot2t-t)", r"\,dt",
                      font_size=32)
        s9b[1].set_color(YELLOW)
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.nb_add(s9b)
            self.sync(tr, text, "Substituting gives")
            self.play(Indicate(s9b[1]), Indicate(s9[1]), run_time=1.0)
        self.rest()

        # 10-12 — integrate
        self.nb_clear()
        s10 = MathTex(r"\int_{2}^{-1}(2t^5-t)\,dt=\Big[\tfrac{t^6}{3}-\tfrac{t^2}{2}\Big]_{2}^{-1}", font_size=36)
        s11 = MathTex(r"t=-1:\ \tfrac13-\tfrac12=-\tfrac16\qquad t=2:\ \tfrac{64}{3}-2=\tfrac{58}{3}", font_size=34)
        s12 = MathTex(r"-\tfrac16-\tfrac{58}{3}=-\tfrac16-\tfrac{116}{6}=-\tfrac{117}{6}=-\tfrac{39}{2}", font_size=36)
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(s10)
        self.rest()
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.nb_add(s11)
        self.rest()
        text = vo[13]
        with self.voiceover(text=text) as tr:
            self.nb_add(s12, buff=0.4)
            self.sync(tr, text, "That simplifies")
            bx = SurroundingRectangle(s12, color=C_ANSWER, buff=0.12)
            self.play(Create(bx), run_time=0.6)
            s12.add(bx)
        self.rest()

        # 13 — interpretation
        neg = Tex("negative: the field works against the motion", font_size=30, color=C_NEG)
        text = vo[14]
        with self.voiceover(text=text) as tr:
            self.play(LaggedStart(*[Indicate(a, color=a.get_color()) for a in on], lag_ratio=0.1), run_time=1.5)
            self.nb_add(neg, gray=False)
        self.rest()

        # 14 — common mistake
        self.chapter(2, "Common mistake")
        wrong = MathTex(r"\int_{-1}^{2}(2t^5-t)\,dt=+\tfrac{39}{2}", font_size=36, color=C_WRONG)
        opp = Tex("opposite direction", font_size=28, color=C_WRONG)
        text = vo[15]
        with self.voiceover(text=text) as tr:
            self.nb_add(wrong, gray=False)
            self.sync(tr, text, "That traces the curve")
            self.play(Transform(tips, dir_tips([1.5, 0.5, -0.5], func=lambda s: (s * s, s), to=A, color=C_WRONG)),
                      run_time=0.8)
            self.nb_add(opp, gray=False)
            self.sync(tr, text, "Wrong sign")
            self.strike(wrong, owner=wrong)
        self.rest()
        self.play(Transform(tips, dir_tips([1.5, 0.5, -0.5], reverse=True, func=lambda s: (s * s, s), to=A)),
                  run_time=0.6)

        # 15 — check card
        ch = VGroup(Tex("Check", font_size=40, color=YELLOW),
                    MathTex(r"t=-y:\quad t:\ -2\to1", font_size=38),
                    MathTex(r"\int_{-2}^{1}(2u^5-u)\,du=-\tfrac{39}{2}\ \checkmark", font_size=38)).arrange(DOWN, buff=0.4)
        card = card_left(self, ch)
        text = vo[16]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(card[0]), FadeIn(ch[0]), run_time=0.5)
            self.sync(tr, text, "use t equals minus y")
            self.play(FadeIn(ch[1]), run_time=0.6)
            self.sync(tr, text, "and you get")
            self.play(FadeIn(ch[2]), run_time=0.6)
        self.rest()

        # 16 — summary
        self.summary(vo[17],
                     [r"$\mathbf F\cdot\mathbf T\,ds=\mathbf F\cdot d\mathbf r$: you only need $\mathbf r'(t)$.",
                      r"$x$ given as a function of $y$ $\Rightarrow$ use $y$ as the parameter.",
                      r"The limits follow the direction of motion, even from large to small."],
                     ["One:", "Two:", "Three:"])


VO["ex15"] = [
    "Exercise fifteen. Evaluate the integral over C of x squared plus y squared, d y. The path C goes from the origin to the point three, zero, and then up to three, three.",
    "Note: this is a d y integral, not a d s integral. It is the line integral of the vector field F equals zero i, plus x squared plus y squared, j. Only the motion in the y direction counts.",
    "The path has two straight pieces: C one, horizontal, along the x axis, and C two, vertical, along the line x equals three. We split the integral into two parts.",
    "Pause and think: what is the integral over the horizontal piece C one?",
    "On C one, y stays zero, so y does not change, and d y equals zero. Whatever the integrand is, multiplied by zero it gives zero. The integral over C one is zero, without any calculation.",
    "Let's still check it with a parametrisation. On C one: x equals t, y equals zero, for t from zero to three. Then d y equals y prime of t, d t, which is zero. So the integral is zero. Confirmed.",
    "On C two, x stays three, and y goes from zero to three. Take x equals three and y equals t, for t from zero to three. Then d y equals d t.",
    "Substitute into the integrand: x squared plus y squared becomes nine plus t squared.",
    "The integral over C two is the integral from zero to three of nine plus t squared, d t. Nine t gives twenty seven. t cubed over three gives twenty seven over three, which is nine. Together: thirty six.",
    "The total is zero plus thirty six, which is thirty six.",
    "Why does only C two count? Picture the vector field: all arrows point straight up. Moving horizontally, we move perpendicular to the arrows, so the field does no work. Moving up, we move with the arrows, and they get longer as y grows.",
    "A rule you will use often: on a horizontal piece, d y equals zero. On a vertical piece, d x equals zero. For a closed path made of straight pieces, like a triangle or a rectangle, handle each piece separately with its own parametrisation, and check the direction on each piece.",
    "Summary. One: split a path into pieces, and add the integrals. Two: d x and d y integrals only see motion in the x or y direction; on a horizontal piece, the d y integral is zero. Three: for straight pieces, parametrise each one with its own simple formula.",
]


class Ex16_2_15(FlatScene):
    def construct(self):
        vo = VO["ex15"]
        ax = Axes(x_range=[-0.5, 3.5, 1], y_range=[-0.5, 3.5, 1], x_length=6.0, y_length=6.0, tips=False,
                  axis_config={"stroke_color": GRAY_B, "include_numbers": True, "font_size": 22}).move_to([-3.4, -0.3, 0])
        ax_l = VGroup(MathTex("x", font_size=30).next_to(ax.x_axis, RIGHT, buff=0.1),
                      MathTex("y", font_size=30).next_to(ax.y_axis, UP, buff=0.1))

        def A(x, y):
            return ax.c2p(x, y)

        self.start("16.2 — Exercise 15",
                   r"\int_C (x^2+y^2)\,dy,\qquad C:\ (0,0)\to(3,0)\to(3,3)",
                   checklist=["1 split", "2 parametrise", "3 substitute", "4 integrate"])

        # 0
        self.intro(vo[0])

        # 1 — a dy integral
        s1 = MathTex(r"\int_C N\,dy\ \text{ with }\ \mathbf F=0\,\mathbf i+(x^2+y^2)\,\mathbf j", font_size=34)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(Create(ax), FadeIn(ax_l), run_time=1.0)
            self.sync(tr, text, "It is the line integral")
            self.nb_add(s1)
            self.sync(tr, text, "Only the motion")
            self.nb_add(Tex("only motion in the $y$ direction counts", font_size=30, color=GRAY_B), gray=False)
        self.rest()

        # 2 — the path
        C1 = Line(A(0, 0), A(3, 0), color=C_CURVE, stroke_width=7)
        C2 = Line(A(3, 0), A(3, 3), color=C_TEAL, stroke_width=7)
        l1 = MathTex("C_1", color=C_CURVE, font_size=34).next_to(C1, UP, buff=0.15)
        l2 = MathTex("C_2", color=C_TEAL, font_size=34).next_to(C2, LEFT, buff=0.15)
        tips = VGroup(dir_tips([1.5], color=C_CURVE, func=lambda s: (s, 0), to=A),
                      dir_tips([1.5], color=C_TEAL, func=lambda s: (3, s), to=A))
        s2 = MathTex(r"\int_C=\int_{C_1}+\int_{C_2}", font_size=36)
        uu = ValueTracker(0.0)

        def path(u):
            return A(u, 0) if u <= 3 else A(3, u - 3)
        dot = Dot(A(0, 0), radius=0.09, color=WHITE)
        dot.add_updater(lambda m: m.move_to(path(uu.get_value())))
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.add(dot)
            self.play(Create(C1), uu.animate.set_value(3), run_time=1.5, rate_func=linear)
            self.play(FadeIn(l1), FadeIn(tips[0]), run_time=0.4)
            self.sync(tr, text, "and C two")
            self.play(Create(C2), uu.animate.set_value(6), run_time=1.5, rate_func=linear)
            self.play(FadeIn(l2), FadeIn(tips[1]), run_time=0.4)
            self.sync(tr, text, "We split")
            self.nb_add(s2)
        self.rest()

        # 3 — pause
        self.pause(vo[3], r"What is the integral over the horizontal piece $C_1$?")

        # 4 — dy = 0 on C1
        yl = VGroup(MathTex("y=0", font_size=30, color=YELLOW), MathTex("dy=0", font_size=30, color=YELLOW)
                    ).arrange(DOWN, buff=0.1)
        yl.add_updater(lambda m: m.next_to(dot, UP, buff=0.25))
        s4 = MathTex(r"C_1:\ dy=0\ \Rightarrow\ \int_{C_1}=0", font_size=36)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            uu.set_value(0)
            self.play(FadeIn(yl), run_time=0.4)
            self.play(uu.animate.set_value(3), run_time=2.5, rate_func=linear)
            self.sync(tr, text, "The integral over C one is zero")
            self.nb_add(s4)
        self.rest()
        yl.clear_updaters()
        self.play(FadeOut(yl), run_time=0.3)

        # 5 — check with a parametrisation
        s5 = MathTex(r"C_1:\ x=t,\ y=0,\ 0\le t\le3,\ dy=y'(t)\,dt=0\,dt\ \Rightarrow\ 0\ \checkmark", font_size=32)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            self.nb_add(s5)
        self.rest()

        # 6-9 — piece C2
        self.nb_clear()
        self.chapter(1, r"Piece $C_2$")
        s6 = MathTex(r"C_2:\ x=3,\ y=t,\ 0\le t\le3,\ dy=dt", font_size=34)
        s7 = MathTex(r"x^2+y^2=9+t^2", font_size=36)
        s8 = MathTex(r"\int_0^3(9+t^2)\,dt=\Big[9t+\tfrac{t^3}{3}\Big]_0^3=27+9=36", font_size=34)
        s9 = MathTex(r"\int_C=0+36=36", font_size=40)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.play(uu.animate.set_value(6), run_time=2.0, rate_func=linear)
            self.check_step(1)
            self.nb_add(s6)
        self.rest()
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.nb_add(s7)
        self.rest()
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(s8)
        self.rest()
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.nb_add(s9, buff=0.4)
            bx = SurroundingRectangle(s9, color=C_ANSWER, buff=0.15)
            self.play(Create(bx), run_time=0.6)
            s9.add(bx)
        self.rest()

        # 10 — the field: arrows straight up
        def fsc(p):
            x, y = ax.p2c(p)
            return np.array([0.0, x * x + y * y, 0.0])
        vf = ArrowVectorField(fsc, x_range=[A(0.25, 0)[0], A(3.3, 0)[0], 0.75], y_range=[A(0, 0.1)[1], A(0, 3.2)[1], 0.75],
                              length_func=lambda n: min(0.72, 0.05 * n + 0.08))
        vf.set_opacity(0.6)
        t1 = Tex(r"$\perp$ arrows $\to$ nothing", font_size=28, color=C_CURVE).move_to(A(1.5, -0.35) + DOWN * 0.15)
        t2 = Tex(r"with the arrows, growing", font_size=28, color=C_TEAL).next_to(C2, RIGHT, buff=0.1).shift(UP * 0.6)
        t2.rotate(PI / 2)
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(vf), run_time=1.0)
            self.sync(tr, text, "Moving horizontally")
            uu.set_value(0)
            self.play(uu.animate.set_value(3), FadeIn(t1), run_time=2.0, rate_func=linear)
            self.sync(tr, text, "Moving up")
            self.play(uu.animate.set_value(6), FadeIn(t2), run_time=2.0, rate_func=linear)
        self.rest()
        dot.clear_updaters()

        # 11 — useful rule
        self.chapter(2, "Useful rule")
        rule = VGroup(Tex("horizontal piece: $dy=0$", font_size=34),
                      Tex("vertical piece: $dx=0$", font_size=34),
                      Tex(r"closed path of straight pieces (triangle, rectangle):\\each piece its own parametrisation,\\"
                          r"check the direction of each piece", font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.4)
        card = card_left(self, VGroup(Tex("Useful rule", font_size=40, color=YELLOW), rule).arrange(DOWN, buff=0.5))
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), run_time=0.5)
            self.play(FadeIn(rule[0]), run_time=0.5)
            self.sync(tr, text, "On a vertical piece")
            self.play(FadeIn(rule[1]), run_time=0.5)
            self.sync(tr, text, "For a closed path")
            self.play(FadeIn(rule[2]), run_time=0.6)
        self.rest()

        # 12 — summary
        self.summary(vo[12],
                     [r"Split a path into pieces and add the integrals.",
                      r"$dx$/$dy$ integrals only see motion in $x$/$y$; horizontal piece: $\int\dots dy=0$.",
                      r"Straight pieces: parametrise each one with its own simple formula."],
                     ["One:", "Two:", "Three:"])
