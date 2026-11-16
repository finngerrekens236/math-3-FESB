"""16.3 Path independence, conservative fields, potential functions (Thomas' Calculus, 13e ed.)

Concept videos (2D, FlatScene):
  ConservativeIntro   path independence, F = grad f, fundamental theorem of line integrals, loops
  TestAndPotential    component test (symmetric table), holes, finding f in 3 steps, exact forms

Exercises (fully worked):
  Ex16_3_01  yz i + xz j + xy k            -> conservative, f = xyz
  Ex16_3_03  y i + (x+z) j - y k           -> not conservative (loop gives -2)
  Ex16_3_07  2x i + 3y j + 4z k            -> f = x^2 + 3/2 y^2 + 2 z^2 + C
  Ex16_3_11  ln x + sec^2(x+y), ...        -> f = x ln x - x + tan(x+y) + 1/2 ln(y^2+z^2) + C
  Ex16_3_18  exact form, (0,2,1)->(1,pi/2,2) -> ln(pi/2)
  Ex16_3_20  exact form, (1,2,1)->(2,1,1)    -> -ln 2

Fixed visual: the component-test table (rows M, N, P; columns d/dx, d/dy, d/dz), diagonal GRAY,
mirror pairs M_y-N_x YELLOW, M_z-P_x TEAL, N_z-P_y PURPLE; match GREEN check, mismatch RED cross.

Voiceover text: VO dict (literal from the task block).
Render (one at a time): .\\.venv\\Scripts\\python.exe render.py scenes\\16_3_conservative_fields.py <Scene> --low
"""
from manim import *
import numpy as np

from _exercise import (FlatScene, C_CURVE, C_F, C_NEG, C_DS, C_DT, C_ANSWER, C_WRONG, NB_LEFT, NB_RIGHT, NB_W,
                       LEFT_CENTER)

OUTPUT = {
    "ConservativeIntro": "16.3 Path independence, conservative fields, potentials/Concept/1 - Path independence & potential functions",
    "TestAndPotential": "16.3 Path independence, conservative fields, potentials/Concept/2 - Component test & finding potentials",
    "Ex16_3_01": "16.3 Path independence, conservative fields, potentials/Exercises/Ex 01",
    "Ex16_3_03": "16.3 Path independence, conservative fields, potentials/Exercises/Ex 03",
    "Ex16_3_07": "16.3 Path independence, conservative fields, potentials/Exercises/Ex 07",
    "Ex16_3_11": "16.3 Path independence, conservative fields, potentials/Exercises/Ex 11",
    "Ex16_3_18": "16.3 Path independence, conservative fields, potentials/Exercises/Ex 18",
    "Ex16_3_20": "16.3 Path independence, conservative fields, potentials/Exercises/Ex 20",
}

C_M, C_N, C_P = BLUE, ORANGE, PINK          # components M, N, P
C_GRAD = YELLOW                              # grad f / f' (same colour)
PAIRS = [((0, 1), (1, 0), YELLOW, "M_y", "N_x"),
         ((0, 2), (2, 0), TEAL, "M_z", "P_x"),
         ((1, 2), (2, 1), PURPLE, "N_z", "P_y")]

CHECK_TEST = ["1 domain", "2 table", "3 pairs", "4 verdict"]
CHECK_POT = [r"1 $\int M\,dx$", r"2 match $N$", r"3 match $P$", "4 check"]
CHECK_EXACT = ["1 test", r"2 find $f$", r"3 $f(B)-f(A)$"]

CANCEL_TPL = TexTemplate()
CANCEL_TPL.add_to_preamble(r"\usepackage{xcolor}\usepackage{cancel}\renewcommand{\CancelColor}{\color{red}}")


# ----------------------------------------------------------------------------- helpers
def card_left(scene, content, color=YELLOW, center=LEFT_CENTER, width=7.4):
    """Rounded card over the drawing area (notebook stays visible)."""
    if content.width > width - 0.6:
        content.scale_to_fit_width(width - 0.6)
    content.move_to(center)
    bg = RoundedRectangle(corner_radius=0.2, width=width, height=min(max(content.height + 1.0, 2.2), 7.6),
                          fill_color="#141414", fill_opacity=0.97, stroke_color=color, stroke_width=2)
    bg.move_to(center)
    return VGroup(bg, content)


def boxed(scene, mob, color=C_ANSWER, buff=0.12):
    """Draw a frame around a notebook line; the frame becomes part of the line."""
    b = SurroundingRectangle(mob, color=color, buff=buff)
    scene.play(Create(b), run_time=0.6)
    put_in(scene, mob, b)      # frame lives only inside mob (else it stays behind after nb_clear)
    return b


def put_in(scene, owner, *mobs):
    """Mobjects that were animated in separately become part of `owner` (so they scroll/fade with it)."""
    scene.remove(*mobs)
    owner.add(*mobs)


def tip(func, t, color, reverse=False, size=0.26):
    a, b = (t + 0.01, t - 0.01) if reverse else (t - 0.01, t + 0.01)
    p, q = func(a), func(b)
    tri = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(size / 2)
    tri.rotate(np.arctan2(q[1] - p[1], q[0] - p[0]) - PI / 2).move_to((p + q) / 2)
    return tri


def check_mark(ok, size=40):
    return MathTex(r"\checkmark" if ok else r"\times", font_size=size, color=C_ANSWER if ok else C_WRONG)


class CompTable(VGroup):
    """3x3 table of partial derivatives (rows M, N, P; columns d/dx, d/dy, d/dz)."""

    # table spans x from center-2.5*cw to center+1.5*cw (header column on the left), legend to the right
    def __init__(self, center=np.array([-3.85, 0.2, 0]), cw=1.15, ch=0.85, size=30, legend=True):
        super().__init__()
        self.center_cell, self.cw, self.ch, self.size = np.array(center, dtype=float), cw, ch, size
        diag = VGroup(*[Rectangle(width=cw * 0.95, height=ch * 0.9, stroke_width=0, fill_color=GRAY_D,
                                  fill_opacity=0.45).move_to(self.pos(i, i)) for i in range(3)])
        heads_c = VGroup(*[MathTex(s, font_size=size) for s in
                           [r"\partial/\partial x", r"\partial/\partial y", r"\partial/\partial z"]])
        for c, h in enumerate(heads_c):
            h.move_to(self.pos(-1, c))
        heads_r = VGroup(*[MathTex(s, font_size=size + 6, color=col) for s, col in
                           [("M", C_M), ("N", C_N), ("P", C_P)]])
        for r, h in enumerate(heads_r):
            h.move_to(self.pos(r, -1))
        left, right = self.pos(0, -1)[0] - cw / 2, self.pos(0, 2)[0] + cw / 2
        top, bottom = self.pos(-1, 0)[1] + ch / 2, self.pos(2, 0)[1] - ch / 2
        grid = VGroup(Line([left, top - ch, 0], [right, top - ch, 0], color=GRAY, stroke_width=2),
                      Line([left + cw, top, 0], [left + cw, bottom, 0], color=GRAY, stroke_width=2))
        self.cells = [[MathTex("MNP"[r] + "_" + "xyz"[c], font_size=size, color=GRAY if r == c else GRAY_B)
                       .move_to(self.pos(r, c)) for c in range(3)] for r in range(3)]
        self.arcs = VGroup()
        for a, b, col, _, _ in PAIRS:
            pa, pb = self.pos(*a), self.pos(*b)
            u = (pb - pa) / np.linalg.norm(pb - pa)
            self.arcs.add(ArcBetweenPoints(pa + 0.32 * u, pb - 0.32 * u, angle=-PI / 3, color=col, stroke_width=3))
        self.legend = VGroup()
        if legend:
            for k, (_, _, col, n1, n2) in enumerate(PAIRS):
                self.legend.add(MathTex(n1 + r"\leftrightarrow " + n2, font_size=size, color=col))
            self.legend.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            self.legend.next_to(VGroup(*[self.cells[r][2] for r in range(3)]), RIGHT, buff=0.6)
        self.marks = [None, None, None]
        self.add(diag, grid, heads_c, heads_r, *[m for row in self.cells for m in row], self.arcs, self.legend)
        self.frame_parts = VGroup(diag, grid, heads_c, heads_r)

    def pos(self, r, c):
        return self.center_cell + np.array([(c - 1) * self.cw, -(r - 1) * self.ch, 0])

    def fill(self, r, c, tex, color=WHITE):
        new = MathTex(tex, font_size=self.size, color=GRAY if r == c else color).move_to(self.pos(r, c))
        if new.width > self.cw * 0.95:
            new.scale_to_fit_width(self.cw * 0.95)
        return Transform(self.cells[r][c], new)


def settle(scene, mob):
    """After animating parts of `mob` in separately: keep only `mob` itself in the scene
    (otherwise the parts stay behind when `mob` later fades out or scrolls)."""
    scene.remove(*mob.get_family()[1:])
    scene.add(mob)


def show_table(scene, tbl, run_time=1.2, with_arcs=True):
    """Fade the table in. with_arcs=False: arcs + legend are left out (add them later with show_arcs)."""
    cells = [m for row in tbl.cells for m in row]
    anims = [FadeIn(tbl.frame_parts), *[FadeIn(m) for m in cells]]
    if with_arcs:
        anims += [Create(tbl.arcs), FadeIn(tbl.legend)]
    else:
        tbl.remove(tbl.arcs, tbl.legend)
    scene.play(*anims, run_time=run_time)
    scene.remove(tbl.frame_parts, *cells, tbl.arcs, tbl.legend)
    scene.add(tbl)


def show_arcs(scene, tbl, *extra, run_time=1.2):
    scene.play(Create(tbl.arcs), FadeIn(tbl.legend), *[FadeIn(m) for m in extra], run_time=run_time)
    scene.remove(tbl.arcs, tbl.legend)
    tbl.add(tbl.arcs, tbl.legend)


def fill_row(scene, tbl, r, vals, run_time=0.5):
    for c, v in enumerate(vals):
        scene.play(tbl.fill(r, c, v), run_time=run_time)


def judge_pair(scene, tbl, k, ok, run_time=0.6):
    """Colour mirror pair k GREEN/RED and put a check/cross next to its legend row."""
    a, b, _, _, _ = PAIRS[k]
    col = C_ANSWER if ok else C_WRONG
    mark = check_mark(ok, size=tbl.size + 8)
    if len(tbl.legend):
        mark.next_to(tbl.legend[k], RIGHT, buff=0.2)
    else:
        mark.move_to(tbl.arcs[k].point_from_proportion(0.5)).shift(0.25 * DOWN + 0.25 * RIGHT)
    scene.play(tbl.arcs[k].animate.set_color(col), tbl.cells[a[0]][a[1]].animate.set_color(col),
               tbl.cells[b[0]][b[1]].animate.set_color(col), FadeIn(mark, scale=1.4), run_time=run_time)
    put_in(scene, tbl, mark)
    tbl.marks[k] = mark


def big_components(comps, size=40, buff=0.35):
    """Left-area display of M, N, P in their colours."""
    g = VGroup(*[MathTex(s, font_size=size, color=c) for s, c in zip(comps, [C_M, C_N, C_P])])
    g.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    if g.width > 6.8:
        g.scale_to_fit_width(6.8)
    return g.move_to(LEFT_CENTER)


VO = {}

# =============================================================================
VO["intro1"] = [
    "Section sixteen point three: path independence, conservative fields, and potential functions. Remember exercise twelve from the previous section: three completely different paths, and every time the work was three. In this video we find out why, and why it saves us a lot of work.",
    "For most vector fields, the work from A to B depends on the path you take. But for some special fields, every path from A to B gives the same answer. We then say the line integral is path independent, and the field is called conservative. Because only the end points matter, we can write the integral simply as the integral from A to B.",
    "You know this from physics. Lifting a box to the second floor takes the same work against gravity, whether you take the stairs, a ladder, or a winding ramp. Only the height difference matters. Gravity is a conservative force. Friction is not: a longer route costs more energy.",
    "Where does path independence come from? From gradient fields. If F is the gradient of a scalar function f, then f is called a potential function for F. In exercise four of the previous section, we found exactly such a function: g equals x y plus y z plus x z, whose gradient is the field of exercise twelve.",
    "Here is the key theorem: the fundamental theorem of line integrals. If F is the gradient of f, then the line integral of F along any curve from A to B equals f at B minus f at A. Compare it with the ordinary fundamental theorem of calculus: the integral of f prime from a to b is f of b minus f of a. The gradient plays the role of the derivative.",
    "Why does it work? Walk along the curve, and watch the value of f. By the chain rule from chapter fourteen, the rate at which f changes as you walk is the gradient of f, dot r prime of t. That is exactly the integrand F dot r prime. So the line integral just adds up all the small changes of f along the way, and the total change is f at the end minus f at the start. The path in between does not matter.",
    "Check it with exercise twelve: g at one, one, one is three, and g at the origin is zero. Three minus zero is three. No parametrisation, no dot products, no integrals.",
    "Another example from the book. Suppose F is the gradient of f equals minus one over x squared plus y squared plus z squared. Find the work from one, zero, zero, to zero, zero, two. With the theorem, it takes one line. f at the end point is minus one quarter, and f at the start is minus one. The work is minus one quarter plus one, which is three quarters.",
    "What if the curve is a closed loop, ending where it started? Then the end point equals the start point, and f at A minus f at A is zero. So for a conservative field, the work around every closed loop is zero. And the reverse also holds: if the work around every loop is zero, the field is conservative.",
    "So three statements are equivalent. F is a gradient field. F is conservative, meaning path independent. And the work around every closed loop is zero. If you know one, you know all three.",
    "These results hold under mild conditions: the curves are piecewise smooth, and the domain is connected, so it is in one piece. In the next video, we will see that one test also needs the domain to have no holes.",
    "In mechanics, a potential function is closely related to potential energy. Physicists write the force as minus the gradient of the potential energy U, so U is just minus f. For gravity near the ground, U equals m g z. For a spring, U equals one half k x squared. For a robot arm, this means that the energy needed to lift a payload against gravity depends only on the height difference, not on the trajectory. But friction and motor losses do depend on the path.",
    "Summary. One: a field is conservative if the line integral depends only on the end points. Two: if F is the gradient of a potential function f, the line integral equals f at B minus f at A. Three: for a conservative field, the work around every closed loop is zero.",
]


def scoreboard(vals=("3", "3", "3"), q=True):
    cols = VGroup()
    for name, v, c in zip(["path a", "path b", "path c"], vals, [YELLOW, C_CURVE, C_NEG]):
        cols.add(VGroup(Tex(name, font_size=30, color=c), MathTex(v, font_size=44, color=C_ANSWER)
                        ).arrange(DOWN, buff=0.15))
    cols.arrange(RIGHT, buff=0.8)
    frame = SurroundingRectangle(cols, color=GRAY_B, buff=0.25, corner_radius=0.1)
    head = Tex("16.2 Exercise 12", font_size=28, color=GRAY_B).next_to(frame, UP, buff=0.15)
    g = VGroup(head, frame, cols)
    if q:
        g.add(Tex("why?", font_size=44, color=YELLOW).next_to(frame, DOWN, buff=0.35))
    return g


class ConservativeIntro(FlatScene):
    def construct(self):
        vo = VO["intro1"]
        self.start("16.3 — Conservative fields",
                   Tex(r"path independence $\cdot$ potential functions $\cdot$ loops", font_size=30, color=GRAY_B))

        # 0 — scoreboard of 16.2 Ex 12
        sb = scoreboard().move_to(LEFT_CENTER)
        text = vo[0]
        with self.voiceover(text=text) as tr:
            self.play(Write(self.title_mob), run_time=1.2)
            self.play(Write(self.problem_mob), run_time=1.2)
            self.sync(tr, text, "Remember exercise twelve")
            self.play(FadeIn(sb[:3]), run_time=0.8)
            self.sync(tr, text, "In this video")
            self.play(FadeIn(sb[3], scale=1.3), run_time=0.6)
        self.rest()
        self.play(FadeOut(sb), run_time=0.5)

        # 1 — path independence: A, B, three paths
        self.chapter(1, "Path independence")
        A, B = np.array([-6.0, -2.3, 0]), np.array([-1.3, 1.9, 0])
        AB = B - A
        nrm = np.array([-AB[1], AB[0], 0]) / np.linalg.norm(AB)
        p1 = Line(A, B, color=YELLOW, stroke_width=5)
        p2 = ArcBetweenPoints(A, B, angle=-PI / 2, color=C_CURVE, stroke_width=5)
        p3 = ParametricFunction(lambda t: A + t * AB + 0.55 * np.sin(3 * PI * t) * nrm, t_range=[0, 1],
                                color=C_NEG, stroke_width=5)
        dots = VGroup(Dot(A, radius=0.09), Dot(B, radius=0.09))
        labs = VGroup(MathTex("A", font_size=38).next_to(A, DL, buff=0.1), MathTex("B", font_size=38).next_to(B, UR, buff=0.1))
        anchors = [p1.point_from_proportion(0.62) + np.array([0.35, -0.25, 0]),
                   p2.point_from_proportion(0.5) + np.array([0.55, -0.1, 0]),
                   p3.point_from_proportion(0.3) + np.array([-0.7, 0.35, 0])]
        cols = [YELLOW, C_CURVE, C_NEG]
        w_any = VGroup(*[MathTex(rf"W={v}", font_size=30, color=c).move_to(p) for v, c, p in
                         zip(["1.4", "0.6", "-0.3"], cols, anchors)])
        w_same = VGroup(*[MathTex(r"W=2", font_size=30, color=c).move_to(p) for c, p in zip(cols, anchors)])
        tag_any = Tex("an arbitrary field", font_size=30, color=GRAY_B).move_to([-3.4, 3.2, 0])
        tag_sp = Tex("a special field", font_size=30, color=C_ANSWER).move_to([-3.4, 3.2, 0])
        defn = MathTex(r"\mathbf F\text{ conservative}\iff\int_C\mathbf F\cdot d\mathbf r\text{ same for all }C"
                       r"\text{ from }A\text{ to }B", font_size=32)
        defn2 = MathTex(r"\text{notation: }\int_A^B\mathbf F\cdot d\mathbf r", font_size=34)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(dots), FadeIn(labs), run_time=0.5)
            self.play(Create(p1), Create(p2), Create(p3), run_time=1.5)
            self.sync(tr, text, "depends on the path")
            self.play(FadeIn(tag_any), FadeIn(w_any), run_time=0.8)
            self.sync(tr, text, "But for some special")
            self.play(ReplacementTransform(tag_any, tag_sp), ReplacementTransform(w_any, w_same), run_time=1.0)
            self.sync(tr, text, "and the field is called conservative")
            self.nb_add(defn, gray=False)
            boxed(self, defn, color=YELLOW)
            self.sync(tr, text, "Because only the end points")
            self.nb_add(defn2)
        self.rest()
        self.play(FadeOut(VGroup(p1, p2, p3, dots, labs, w_same, tag_sp)), run_time=0.5)

        # 2 — physics: stairs, ladder, ramp
        g0, g1 = -2.5, 1.0
        floors = VGroup(Line([-6.9, g0, 0], [-0.2, g0, 0], color=GRAY, stroke_width=3),
                        DashedLine([-6.9, g1, 0], [-0.2, g1, 0], color=GRAY, stroke_width=2))
        fl_lab = Tex("2nd floor", font_size=26, color=GRAY_B).next_to(floors[1], UP, buff=0.08).align_to(floors[1], RIGHT)
        steps = [[-6.4 + 0.3 * k, g0 + 0.35 * k, 0] for k in range(11)]
        stairs = VMobject(color=YELLOW, stroke_width=4)
        pts = []
        for k in range(10):
            pts += [steps[k], [steps[k][0] + 0.3, steps[k][1], 0]]
        pts.append([steps[10][0], g1, 0])
        stairs.set_points_as_corners(pts)
        ladder = VGroup(Line([-3.7, g0, 0], [-3.7, g1, 0]), Line([-3.3, g0, 0], [-3.3, g1, 0]),
                        *[Line([-3.7, y, 0], [-3.3, y, 0]) for y in np.linspace(g0 + 0.3, g1 - 0.2, 8)])
        ladder.set_color(C_CURVE).set_stroke(width=3)
        ramp = ParametricFunction(lambda t: np.array([-1.9 + 0.9 * np.sin(4 * PI * t), g0 + (g1 - g0) * t, 0]),
                                  t_range=[0, 1], color=C_NEG, stroke_width=4)
        box = Square(0.4, fill_color=GRAY_B, fill_opacity=1, stroke_color=WHITE).move_to([-5.1, g0 + 0.2, 0])
        mgh = VGroup(*[MathTex("W=mgh", font_size=28, color=c).move_to([x, g1 + 0.75, 0])
                       for x, c in [(-5.2, YELLOW), (-3.5, C_CURVE), (-1.9, C_NEG)]])
        h_ar = DoubleArrow([-0.55, g0, 0], [-0.55, g1, 0], buff=0, color=WHITE, stroke_width=3, tip_length=0.18)
        h_lab = MathTex("h", font_size=32).next_to(h_ar, LEFT, buff=0.08)
        fric = Tex(r"friction: longer path $\to$ more work", font_size=30, color=C_WRONG).move_to([-3.5, -3.2, 0])
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.play(Create(floors), FadeIn(fl_lab), FadeIn(box), GrowFromCenter(h_ar), FadeIn(h_lab), run_time=1.0)
            self.sync(tr, text, "whether you take the stairs")
            self.play(Create(stairs), run_time=0.8)
            self.sync(tr, text, "a ladder")
            self.play(Create(ladder), run_time=0.6)
            self.sync(tr, text, "or a winding ramp")
            self.play(Create(ramp), run_time=0.8)
            self.sync(tr, text, "Only the height")
            self.play(LaggedStart(*[FadeIn(m) for m in mgh], lag_ratio=0.3), run_time=1.0)
            self.sync(tr, text, "Friction is not")
            self.play(FadeIn(fric), run_time=0.6)
        self.rest()
        self.play(FadeOut(VGroup(floors, fl_lab, stairs, ladder, ramp, box, mgh, h_ar, h_lab, fric)), run_time=0.5)

        # 3 — potential functions
        self.nb_clear()
        self.chapter(2, "Potential functions")
        pot = MathTex(r"\mathbf F=\nabla f\quad(f=\text{potential function})", font_size=36)
        ref = MathTex(r"g=xy+yz+xz,\ \ \nabla g=(y+z)\,\mathbf i+(z+x)\,\mathbf j+(x+y)\,\mathbf k", font_size=30)
        ref2 = Tex("(16.2 Ex 4, 12)", font_size=28, color=GRAY_B)
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "If F is the gradient")
            self.nb_add(pot, gray=False)
            boxed(self, pot, color=YELLOW)
            self.sync(tr, text, "In exercise four")
            self.nb_add(ref)
            self.nb_add(ref2, gray=False)
        self.rest()

        # 4 — fundamental theorem of line integrals
        self.nb_clear()
        self.chapter(3, "Fundamental theorem of line integrals")
        ft1 = MathTex(r"\int_C", r"\nabla f", r"\cdot d\mathbf r=f(B)-f(A)", font_size=40)
        ft2 = MathTex(r"\int_a^b", r"f'(x)", r"\,dx=f(b)-f(a)", font_size=40)
        ft1[1].set_color(C_GRAD)
        ft2[1].set_color(C_GRAD)
        lr = MathTex(r"\Updownarrow", font_size=44, color=GRAY_B)
        cmp_grp = VGroup(ft1, lr, ft2).arrange(DOWN, buff=0.4).move_to(LEFT_CENTER)
        cap1 = Tex("line integrals", font_size=28, color=GRAY_B).next_to(ft1, UP, buff=0.2)
        cap2 = Tex("Calculus 1", font_size=28, color=GRAY_B).next_to(ft2, DOWN, buff=0.2)
        nb_ft = MathTex(r"\int_C\nabla f\cdot d\mathbf r=f(B)-f(A)", font_size=38)
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "If F is the gradient")
            self.nb_add(nb_ft, gray=False)
            boxed(self, nb_ft, color=YELLOW)
            self.play(Write(ft1), FadeIn(cap1), run_time=1.2)
            self.sync(tr, text, "Compare it")
            self.play(FadeIn(lr), Write(ft2), FadeIn(cap2), run_time=1.2)
            self.sync(tr, text, "The gradient plays")
            self.play(Indicate(ft1[1]), Indicate(ft2[1]), run_time=1.0)
        self.rest()
        self.play(FadeOut(VGroup(cmp_grp, cap1, cap2)), run_time=0.5)

        # 5 — why: walk through a contour plot, meter f(r(t))
        OC = np.array([-3.4, -0.2, 0])

        def fval(x, y):
            return 0.4 * x * x + 0.8 * y

        def S(x, y):
            return OC + np.array([x, y, 0])
        contours = VGroup()
        for c in np.arange(-2.4, 4.81, 0.6):
            xs = np.linspace(-3.0, 3.0, 121)
            ys = (c - 0.4 * xs * xs) / 0.8
            ok = (ys > -3.0) & (ys < 3.0)
            if ok.sum() < 3:
                continue
            col = interpolate_color(ManimColor("#2c5aa0"), ManimColor("#e06c3a"), (c + 2.4) / 7.2)
            m = VMobject(stroke_color=col, stroke_width=2.5, stroke_opacity=0.85)
            m.set_points_smoothly([S(x, y) for x, y in zip(xs[ok], ys[ok])])
            contours.add(m)
        cl = Tex("level curves of $f$", font_size=26, color=GRAY_B).move_to(S(1.9, -2.7))
        Am, Bm = np.array([-2.0, -1.5]), np.array([2.0, 1.5])
        paths = [lambda s: Am + s * (Bm - Am),
                 lambda s: Am + s * (Bm - Am) + 1.6 * np.sin(PI * s) * np.array([-0.6, 0.8]),
                 lambda s: Am + s * (Bm - Am) + 1.4 * np.sin(PI * s) * np.array([0.6, -0.8])]
        pcols = [YELLOW, C_CURVE, C_NEG]
        curves = [ParametricFunction(lambda s, f=f: S(*f(s)), t_range=[0, 1], color=c, stroke_width=5)
                  for f, c in zip(paths, pcols)]
        ab = VGroup(Dot(S(*Am), radius=0.09), Dot(S(*Bm), radius=0.09),
                    MathTex("A", font_size=34).next_to(S(*Am), DOWN, buff=0.12),
                    MathTex("B", font_size=34).next_to(S(*Bm), UP, buff=0.12))
        s_tr = ValueTracker(0.0)
        cur = {"f": paths[0]}
        dot = Dot(S(*Am), radius=0.1, color=WHITE)
        dot.add_updater(lambda m: m.move_to(S(*cur["f"](s_tr.get_value()))))
        meter_num = DecimalNumber(fval(*Am), num_decimal_places=2, font_size=34, color=C_GRAD)
        meter_num.add_updater(lambda m: m.set_value(fval(*cur["f"](s_tr.get_value()))))
        meter = VGroup(MathTex(r"f(\mathbf r(t))=", font_size=34, color=C_GRAD), meter_num).arrange(RIGHT, buff=0.12)
        meter.move_to([-5.0, 3.3, 0])
        meter.add_background_rectangle(opacity=0.85, buff=0.1)
        cr = MathTex(r"\frac{d}{dt}f(\mathbf r(t))=\nabla f(\mathbf r(t))\cdot\mathbf r'(t)", font_size=34)
        ft = MathTex(r"\int_a^b\nabla f\cdot\mathbf r'\,dt=\int_a^b\frac{d}{dt}f(\mathbf r(t))\,dt"
                     r"=f(\mathbf r(b))-f(\mathbf r(a))", font_size=32)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.play(Create(contours), FadeIn(cl), run_time=1.2)
            self.play(FadeIn(ab), Create(curves[0]), run_time=0.8)
            self.add(dot)
            self.play(FadeIn(meter), run_time=0.4)
            self.sync(tr, text, "Walk along the curve")
            self.play(s_tr.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
            self.sync(tr, text, "By the chain rule")
            self.nb_add(cr)
            self.sync(tr, text, "So the line integral")
            self.nb_add(ft, gray=False)
            self.sync(tr, text, "The path in between")
            for k in (1, 2):
                cur["f"] = paths[k]
                s_tr.set_value(0.0)
                self.play(Create(curves[k]), run_time=0.6)
                self.play(s_tr.animate.set_value(1.0), run_time=2.0, rate_func=smooth)
            self.play(Indicate(meter), run_time=0.8)
        self.rest()
        dot.clear_updaters()
        meter_num.clear_updaters()

        # 6 — exercise twelve again
        sb2 = scoreboard(q=False).scale(0.8).move_to([-3.4, 2.4, 0])
        e12 = MathTex(r"g(1,1,1)-g(0,0,0)=3-0=3", font_size=36)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.play(FadeOut(VGroup(contours, cl, ab, dot, meter, *curves)), run_time=0.5)
            self.play(FadeIn(sb2), run_time=0.5)
            self.nb_add(e12, gray=False)
            self.sync(tr, text, "Three minus zero")
            self.play(Indicate(sb2[2], color=C_ANSWER), run_time=1.0)
            self.sync(tr, text, "No parametrisation")
            nope = Tex(r"no parametrisation $\cdot$ no dot products $\cdot$ no integrals", font_size=28,
                       color=GRAY_B).move_to([-3.4, 0.6, 0])
            self.play(FadeIn(nope), run_time=0.6)
        self.rest()
        self.play(FadeOut(sb2), FadeOut(nope), run_time=0.4)

        # 7 — book example: 3/4
        ex1 = MathTex(r"f=-\frac{1}{x^2+y^2+z^2}", font_size=36)
        ex2 = MathTex(r"W=f(0,0,2)-f(1,0,0)=-\tfrac14-(-1)=\tfrac34", font_size=36)
        pts7 = VGroup(MathTex(r"A=(1,0,0)", font_size=34), MathTex(r"B=(0,0,2)", font_size=34),
                      MathTex(r"f(A)=-1,\qquad f(B)=-\tfrac14", font_size=34, color=C_GRAD)
                      ).arrange(DOWN, buff=0.35).move_to(LEFT_CENTER)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Suppose F is the gradient")
            self.nb_add(ex1)
            self.sync(tr, text, "Find the work")
            self.play(FadeIn(pts7[0]), FadeIn(pts7[1]), run_time=0.6)
            self.sync(tr, text, "f at the end point")
            self.play(FadeIn(pts7[2]), run_time=0.6)
            self.sync(tr, text, "The work is")
            self.nb_add(ex2, buff=0.4)
            boxed(self, ex2)
        self.rest()
        self.play(FadeOut(pts7), run_time=0.4)

        # 8 — closed loops
        self.nb_clear()
        self.chapter(4, "Closed loops")
        EC, ea, eb = np.array([-3.4, -0.1, 0]), 2.4, 1.6

        def E(t):
            return EC + np.array([ea * np.cos(t), eb * np.sin(t), 0])
        loop = ParametricFunction(E, t_range=[0, 2 * PI], color=YELLOW, stroke_width=5)
        lt = VGroup(tip(E, PI / 2, YELLOW), tip(E, 3 * PI / 2, YELLOW))
        Apt = Dot(E(PI), radius=0.1)
        Alab = MathTex("A=B", font_size=34).next_to(Apt, LEFT, buff=0.12)
        z1 = MathTex(r"\oint_C\mathbf F\cdot d\mathbf r=f(A)-f(A)=0", font_size=38)
        upper = ParametricFunction(E, t_range=[0, PI], color=C_CURVE, stroke_width=6)        # B -> A? (see below)
        lower = ParametricFunction(E, t_range=[PI, 2 * PI], color=C_NEG, stroke_width=6)
        Bpt = Dot(E(0), radius=0.1)
        lab_c = VGroup(MathTex("A", font_size=34).next_to(E(PI), LEFT, buff=0.12),
                       MathTex("B", font_size=34).next_to(E(0), RIGHT, buff=0.12),
                       MathTex("C_1", font_size=34, color=C_NEG).next_to(E(3 * PI / 2), DOWN, buff=0.12),
                       MathTex("C_2", font_size=34, color=C_CURVE).next_to(E(PI / 2), UP, buff=0.12))
        t_c1 = tip(E, 3 * PI / 2, C_NEG)            # lower arc A -> B (counterclockwise)
        t_c2 = tip(E, PI / 2, C_CURVE)              # upper arc B -> A
        t_c2r = tip(E, PI / 2, C_CURVE, reverse=True)
        mc2 = MathTex("-C_2", font_size=34, color=C_CURVE).next_to(E(PI / 2), UP, buff=0.12)
        z2 = MathTex(r"\int_{C_1}\mathbf F\cdot d\mathbf r=\int_{-C_2}\mathbf F\cdot d\mathbf r", font_size=36)
        z3 = Tex(r"loops give $0$ $\Rightarrow$ two paths $A\to B$ give the same", font_size=30, color=GRAY_B)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.play(Create(loop), FadeIn(lt), FadeIn(Apt), FadeIn(Alab), run_time=1.2)
            self.sync(tr, text, "Then the end point")
            self.nb_add(z1, gray=False)
            boxed(self, z1, color=YELLOW)
            self.sync(tr, text, "And the reverse")
            self.play(FadeOut(loop), FadeOut(lt), FadeOut(Alab), run_time=0.4)
            self.play(Create(lower), Create(upper), FadeIn(Bpt), FadeIn(lab_c), FadeIn(t_c1), FadeIn(t_c2), run_time=1.0)
            self.play(Transform(t_c2, t_c2r), Transform(lab_c[3], mc2), run_time=1.0)
            self.nb_add(z2)
            self.nb_add(z3, gray=False)
        self.rest()
        self.play(FadeOut(VGroup(upper, lower, Apt, Bpt, lab_c, t_c1, t_c2)), run_time=0.5)

        # 9 — three equivalent statements
        bx = VGroup()
        for s in [r"$\mathbf F=\nabla f$", r"$\mathbf F$ conservative", r"$\oint_C\mathbf F\cdot d\mathbf r=0$ for every loop"]:
            t = Tex(s, font_size=34)
            r = RoundedRectangle(corner_radius=0.15, width=t.width + 0.5, height=t.height + 0.45, stroke_color=YELLOW,
                                 stroke_width=2)
            bx.add(VGroup(r, t.move_to(r)))
        iffs = [MathTex(r"\Updownarrow", font_size=44, color=GRAY_B) for _ in range(2)]
        schema = VGroup(bx[0], iffs[0], bx[1], iffs[1], bx[2]).arrange(DOWN, buff=0.3).move_to(LEFT_CENTER)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "F is a gradient")
            self.play(FadeIn(bx[0]), run_time=0.5)
            self.sync(tr, text, "F is conservative")
            self.play(FadeIn(iffs[0]), FadeIn(bx[1]), run_time=0.5)
            self.sync(tr, text, "And the work around")
            self.play(FadeIn(iffs[1]), FadeIn(bx[2]), run_time=0.5)
            self.sync(tr, text, "If you know one")
            self.nb_add(MathTex(r"\mathbf F=\nabla f\iff\mathbf F\text{ conservative}\iff\oint_C\mathbf F\cdot d\mathbf r=0",
                                font_size=32), gray=False)
        self.rest()
        self.play(FadeOut(schema), run_time=0.4)

        # 10 — assumptions
        asm = VGroup(Tex("assumptions", font_size=36, color=YELLOW),
                     Tex(r"piecewise smooth curves\\connected domain (one piece)", font_size=32),
                     Tex(r"next video: no holes", font_size=30, color=ORANGE)).arrange(DOWN, buff=0.35)
        acard = card_left(self, asm)
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(acard[0]), FadeIn(asm[0]), FadeIn(asm[1]), run_time=0.8)
            self.sync(tr, text, "In the next video")
            self.play(FadeIn(asm[2]), run_time=0.6)
        self.rest()
        self.play(FadeOut(acard), run_time=0.4)

        # 11 — mechanics
        mh = Tex("Mechanics", font_size=38, color=YELLOW)
        mf = MathTex(r"\mathbf F=-\nabla U\ \ (U=-f),\qquad U_{\text{gravity}}=mgz,\quad U_{\text{spring}}=\tfrac12kx^2",
                     font_size=30)
        base = np.array([-1.6, -1.6, 0])
        arm = VGroup(Rectangle(width=1.0, height=0.25, fill_color=GRAY_D, fill_opacity=1, stroke_color=GRAY
                               ).move_to(base + DOWN * 0.12),
                     Line(base, base + np.array([-0.9, 1.3, 0]), stroke_width=9, color=GRAY_B),
                     Line(base + np.array([-0.9, 1.3, 0]), base + np.array([-2.3, 1.6, 0]), stroke_width=7, color=GRAY_B),
                     Square(0.35, fill_color=ORANGE, fill_opacity=1, stroke_width=0).move_to(base + np.array([-2.3, 1.35, 0])))
        traj = VGroup(DashedLine(base + np.array([-2.3, -0.9, 0]), base + np.array([-2.3, 1.2, 0]), color=YELLOW),
                      ArcBetweenPoints(base + np.array([-2.3, -0.9, 0]), base + np.array([-2.3, 1.2, 0]), angle=PI / 1.5,
                                       color=C_CURVE, stroke_width=3))
        m1 = Tex(r"energy $=mg\,\Delta h$, any trajectory", font_size=28, color=C_ANSWER)
        m2 = Tex(r"friction / motor losses: path dependent", font_size=28, color=C_WRONG)
        pic = VGroup(arm, traj)
        mbody = VGroup(mh, mf, pic, m1, m2).arrange(DOWN, buff=0.3)
        mcard = card_left(self, mbody)
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(mcard[0]), FadeIn(mh), run_time=0.5)
            self.sync(tr, text, "Physicists write")
            self.play(FadeIn(mf), run_time=0.8)
            self.sync(tr, text, "For a robot arm")
            self.play(FadeIn(pic), run_time=0.8)
            self.play(FadeIn(m1), run_time=0.5)
            self.sync(tr, text, "But friction")
            self.play(FadeIn(m2), run_time=0.5)
        self.rest()

        # 12 — summary
        self.summary(vo[12],
                     [r"Conservative: the line integral depends only on the end points.",
                      r"$\mathbf F=\nabla f$ $\Rightarrow$ $\int_A^B\mathbf F\cdot d\mathbf r=f(B)-f(A)$.",
                      r"Conservative $\Rightarrow$ the work around every closed loop is $0$."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
VO["intro2"] = [
    "In the previous video we saw how useful a potential function is. Two questions remain. How can you tell whether a field is conservative? And if it is, how do you find the potential function f? This video answers both, and ends with a recipe you can use for every exercise.",
    "Suppose F is the gradient of f. Then M is f x, N is f y, and P is f z. Now take the y derivative of M: that is the mixed derivative f x y. And the x derivative of N is f y x. By the mixed derivative theorem from section fourteen point three, these two are equal. So for a conservative field, the y derivative of M must equal the x derivative of N.",
    "The same argument works for every pair of components. This gives three conditions: P y equals N z, M z equals P x, and N x equals M y. Together they are called the component test for conservative fields.",
    "Here is an easy way to remember it. Put all nine partial derivatives in a table: one row for each component, and one column for each variable. The diagonal does not matter. The test says the table must be symmetric: each entry must equal its mirror image across the diagonal. That gives three pairs to check.",
    "Pause and think: is the field two x minus three, i, minus z, j, plus cos z, k, conservative?",
    "Check the first pair. P is cos z, which contains no y, so P y is zero. N is minus z, so N z is minus one. Zero is not minus one. One failing pair is enough: the field is not conservative, and we can stop.",
    "Now a trap. The field minus y i plus x j, divided by x squared plus y squared, passes the test: all three pairs match. But around the unit circle, its circulation is two pi, not zero. So it is not conservative. How is that possible?",
    "The field is not defined at the origin; in space, it is not defined on the whole z axis. The domain has a hole. The test only works on a simply connected domain: one in which every loop can be shrunk to a point without leaving the domain. A loop around the hole cannot be shrunk, and that is exactly where the test fails. So always check the domain as well.",
    "Now the second question: finding f. We need a function whose three partial derivatives are M, N and P. Take example three from the book. M equals e to the x cos y, plus y z. N equals x z minus e to the x sin y. And P equals x y plus z. You can check that it passes the test.",
    "Step one: integrate M with respect to x, holding y and z fixed. That gives e to the x cos y, plus x y z. But the constant of integration may still depend on y and z, so we add g of y and z. This is the most important detail.",
    "Step two: take the y derivative of this f, and set it equal to N. We get minus e to the x sin y, plus x z, plus g y. That must equal x z minus e to the x sin y. Everything cancels except g y, which must be zero. So g depends only on z, and we write h of z.",
    "Step three: take the z derivative, and set it equal to P. We get x y plus h prime of z, which must equal x y plus z. So h prime is z, and h is z squared over two, plus a constant C. The potential function is e to the x cos y, plus x y z, plus z squared over two, plus C.",
    "Always check: take the three partial derivatives of f, and you get M, N and P back.",
    "In the exercises you will also meet this idea in differential form notation. The expression M d x plus N d y plus P d z is called exact if it equals d f, the total differential of some function f. The test is exactly the same component test. Then the integral from A to B is simply f of B minus f of A. For example, y d x plus x d y plus four d z is exact, with f equals x y plus four z. From one, one, one, to two, three, minus one, the integral is two minus five, which is minus three.",
    "Here is the recipe for every exercise in this section. One: apply the component test, and check the domain. Two: if the test fails, the field is not conservative, and you compute line integrals the long way, as in section sixteen point two. If it passes, find f in three steps: integrate M with respect to x, match N, and match P. Three: for a line integral from A to B, the answer is f of B minus f of A.",
    "Summary. One: the component test says the table of partial derivatives must be symmetric; that comes from the mixed derivative theorem. Two: the test only works on a domain without holes. Three: to find f, integrate one component, and determine the unknown function step by step by matching the others.",
]


def flow_box(text, color, w=None, size=28):
    t = Tex(text, font_size=size)
    r = RoundedRectangle(corner_radius=0.12, width=(w or t.width + 0.4), height=t.height + 0.35,
                         stroke_color=color, stroke_width=2)
    return VGroup(r, t.move_to(r))


class TestAndPotential(FlatScene):
    def construct(self):
        vo = VO["intro2"]
        self.start("16.3 — Component test & potentials",
                   Tex(r"is $\mathbf F$ conservative? $\cdot$ how do we find $f$?", font_size=30, color=GRAY_B),
                   checklist=CHECK_POT)

        # 0 — two questions
        qs = VGroup()
        for s, c in [(r"Is $\mathbf F$ conservative?", YELLOW), (r"How do we find $f$?", C_ANSWER)]:
            r = RoundedRectangle(corner_radius=0.15, width=3.3, height=1.6, stroke_color=c, stroke_width=2)
            qs.add(VGroup(r, Tex(s, font_size=32, color=c).move_to(r)))
        qs.arrange(RIGHT, buff=0.3).move_to(LEFT_CENTER)
        text = vo[0]
        with self.voiceover(text=text) as tr:
            self.play(Write(self.title_mob), run_time=1.2)
            self.play(Write(self.problem_mob), run_time=1.2)
            self.sync(tr, text, "How can you tell")
            self.play(FadeIn(qs[0], shift=UP * 0.2), run_time=0.6)
            self.sync(tr, text, "And if it is")
            self.play(FadeIn(qs[1], shift=UP * 0.2), run_time=0.6)
        self.rest()
        self.play(FadeOut(qs), run_time=0.4)

        # 1 — mixed derivatives
        self.chapter(1, "The component test")
        a1 = MathTex(r"\mathbf F=\nabla f\Rightarrow M=f_x,\ N=f_y,\ P=f_z", font_size=36)
        a2 = MathTex(r"M_y=f_{xy},\quad N_x=f_{yx},\quad f_{xy}=f_{yx}\ (\text{14.3})\Rightarrow M_y=N_x", font_size=32)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Then M is f x")
            self.nb_add(a1)
            self.sync(tr, text, "Now take the y derivative")
            self.nb_add(a2, gray=False)
            self.sync(tr, text, "So for a conservative")
            self.play(Indicate(a2), run_time=0.8)
        self.rest()

        # 2 — the three conditions
        a3 = MathTex(r"\frac{\partial P}{\partial y}=\frac{\partial N}{\partial z},\quad "
                     r"\frac{\partial M}{\partial z}=\frac{\partial P}{\partial x},\quad "
                     r"\frac{\partial N}{\partial x}=\frac{\partial M}{\partial y}", font_size=34)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "This gives three")
            self.nb_add(a3, buff=0.4)
            boxed(self, a3, color=YELLOW)
        self.rest()

        # 3 — the table
        tbl = CompTable()
        sym = Tex("table must be symmetric", font_size=32, color=YELLOW).move_to([-3.4, -2.4, 0])
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Put all nine")
            show_table(self, tbl, with_arcs=False)
            self.sync(tr, text, "The diagonal does not")
            self.play(*[Indicate(tbl.cells[i][i], color=GRAY) for i in range(3)], run_time=0.8)
            self.sync(tr, text, "The test says")
            show_arcs(self, tbl, sym)
        self.rest()

        # 4 — pause
        self.pause(vo[4], r"$\mathbf F=(2x-3)\,\mathbf i-z\,\mathbf j+(\cos z)\,\mathbf k$ — conservative?")

        # 5 — first pair fails
        f5 = MathTex(r"M=2x-3,\ \ N=-z,\ \ P=\cos z", font_size=34)
        one = Tex("one failing pair is enough", font_size=30, color=C_WRONG)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.nb_add(f5)
            self.sync(tr, text, "so P y is zero")
            self.play(tbl.fill(2, 1, "0"), run_time=0.5)
            self.sync(tr, text, "so N z is minus one")
            self.play(tbl.fill(1, 2, "-1"), run_time=0.5)
            self.sync(tr, text, "Zero is not")
            judge_pair(self, tbl, 2, False)
            self.nb_add(MathTex(r"P_y=0\neq N_z=-1", font_size=36, color=C_WRONG), gray=False)
            self.sync(tr, text, "One failing pair")
            self.nb_add(one, gray=False)
        self.rest()
        self.play(FadeOut(tbl), FadeOut(sym), run_time=0.5)

        # 6 — the trap: spin field with a hole
        self.nb_clear()
        self.chapter(2, "A trap: holes")
        OC = np.array([-3.4, -0.2, 0])

        def spin(p):
            x, y = p[0] - OC[0], p[1] - OC[1]
            r2 = x * x + y * y
            return np.array([-y / r2, x / r2, 0.0])
        vf = ArrowVectorField(spin, x_range=[OC[0] - 2.85, OC[0] + 2.9, 0.6], y_range=[OC[1] - 2.85, OC[1] + 2.9, 0.6],
                              length_func=lambda n: 0.45 * np.tanh(n))
        hole = VGroup(Circle(radius=0.18, fill_color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=3).move_to(OC),
                      Tex("hole", font_size=26, color=WHITE).next_to(OC, DOWN, buff=0.25))
        f6 = MathTex(r"\mathbf F=\frac{-y\,\mathbf i+x\,\mathbf j}{x^2+y^2}", font_size=36)
        f6b = MathTex(r"N_x=M_y=\frac{y^2-x^2}{(x^2+y^2)^2}", font_size=34)
        circ = Circle(radius=1.6, color=YELLOW, stroke_width=5).move_to(OC)
        f6c = MathTex(r"\oint_{\text{unit circle}}\mathbf F\cdot d\mathbf r=2\pi\neq0", font_size=36, color=C_WRONG)
        tbl2 = CompTable()
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_add(f6)
            self.play(LaggedStart(*[GrowArrow(a) for a in vf], lag_ratio=0.005), FadeIn(hole), run_time=1.5)
            self.sync(tr, text, "passes the test")
            self.play(FadeOut(vf), FadeOut(hole), run_time=0.4)
            show_table(self, tbl2, run_time=0.8)
            self.nb_add(f6b)
            for k in range(3):
                judge_pair(self, tbl2, k, True, run_time=0.4)
            self.sync(tr, text, "But around the unit circle")
            self.play(FadeOut(tbl2), FadeIn(vf), FadeIn(hole), run_time=0.6)
            self.play(Create(circ), run_time=1.0)
            self.nb_add(f6c, gray=False)
        self.rest()
        self.play(FadeOut(VGroup(vf, circ)), FadeOut(hole), run_time=0.5)

        # 7 — simply connected: two panels
        cl, cr = np.array([-5.1, 0.4, 0]), np.array([-1.7, 0.4, 0])
        holes = VGroup(*[Circle(radius=0.15, fill_color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=3
                                ).move_to(c) for c in (cl, cr)])
        frames = VGroup(*[RoundedRectangle(corner_radius=0.15, width=3.2, height=3.4, stroke_color=GRAY, stroke_width=1.5
                                           ).move_to(c) for c in (cl, cr)])
        lp_ok = Circle(radius=0.6, color=C_ANSWER, stroke_width=4).move_to(cl + np.array([0.75, 0.75, 0]))
        lp_bad = Circle(radius=1.1, color=C_WRONG, stroke_width=4).move_to(cr)
        t_ok = Tex(r"shrinks to a point", font_size=26, color=C_ANSWER).next_to(frames[0], DOWN, buff=0.15)
        t_bad = Tex(r"stuck at the hole", font_size=26, color=C_WRONG).next_to(frames[1], DOWN, buff=0.15)
        sc = Tex(r"simply connected $=$ every loop can shrink to a point", font_size=28, color=YELLOW).move_to([-3.4, -2.6, 0])
        dom = Tex(r"domain: space minus the $z$-axis", font_size=28, color=GRAY_B).move_to([-3.4, -3.2, 0])
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(frames), FadeIn(holes), run_time=0.5)
            self.sync(tr, text, "in space, it is not")
            self.nb_add(dom.copy().set_color(GRAY_B), gray=False)
            self.sync(tr, text, "The test only works")
            self.play(Create(lp_ok), run_time=0.6)
            self.play(lp_ok.animate.scale(0.02), run_time=1.5)
            self.play(FadeIn(t_ok), FadeIn(sc), run_time=0.5)
            self.sync(tr, text, "A loop around the hole")
            self.play(Create(lp_bad), run_time=0.6)
            self.play(lp_bad.animate.scale(0.2), run_time=1.2)
            self.play(Indicate(lp_bad, color=C_WRONG), FadeIn(t_bad), run_time=0.8)
            self.sync(tr, text, "So always check")
            self.nb_add(Tex("always check the domain", font_size=30, color=YELLOW), gray=False)
        self.rest()
        self.play(FadeOut(VGroup(frames, holes, lp_ok, lp_bad, t_ok, t_bad, sc)), run_time=0.5)

        # 8 — finding f: example 3
        self.nb_clear()
        self.chapter(3, "Finding a potential")
        self.show_checklist()
        comps = big_components([r"M=e^x\cos y+yz", r"N=xz-e^x\sin y", r"P=xy+z"], size=44)
        g8 = MathTex(r"M=e^x\cos y+yz,\ \ N=xz-e^x\sin y,\ \ P=xy+z", font_size=30)
        g8b = MathTex(r"f_x=M,\quad f_y=N,\quad f_z=P", font_size=36)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "We need a function")
            self.nb_add(g8b, gray=False)
            self.sync(tr, text, "M equals e")
            self.play(FadeIn(comps[0]), run_time=0.5)
            self.sync(tr, text, "N equals")
            self.play(FadeIn(comps[1]), run_time=0.5)
            self.sync(tr, text, "And P equals")
            self.play(FadeIn(comps[2]), run_time=0.5)
            self.nb_add(g8)
        self.rest()

        # 9 — step 1
        s1 = MathTex(r"f=\int M\,dx=e^x\cos y+xyz+", r"g(y,z)", font_size=36)
        s1[1].set_color(YELLOW)
        nc = Tex(r"not just $C$!", font_size=28, color=YELLOW)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.play(Indicate(comps[0]), run_time=0.6)
            self.nb_add(s1, anim=FadeIn(s1[0]))
            self.sync(tr, text, "so we add g")
            gb = SurroundingRectangle(s1[1], color=YELLOW, buff=0.08)
            nc.next_to(gb, DOWN, buff=0.1).align_to(gb, RIGHT)
            self.play(FadeIn(s1[1]), Create(gb), FadeIn(nc), run_time=0.8)
            s1.add(gb, nc)
            settle(self, s1)
            self.nb_cursor = nc.get_bottom()[1] - 0.3
        self.rest()

        # 10 — step 2 (cancel equal terms)
        s2 = MathTex(r"f_y=", r"-e^x\sin y", "+", "xz", r"+g_y\overset{!}{=}", "xz", r"-e^x\sin y", font_size=36)
        s2b = MathTex(r"\Rightarrow\ g_y=0\ \Rightarrow\ g=h(z)", font_size=36)
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            self.play(Indicate(comps[1]), run_time=0.6)
            self.nb_add(s2)
            self.sync(tr, text, "Everything cancels")
            for i in (1, 3, 5, 6):
                self.strike(s2[i], run_time=0.3, owner=s2)
            self.nb_add(s2b, gray=False)
        self.rest()

        # 11 — step 3
        s3 = MathTex(r"f_z=xy+h'(z)\overset{!}{=}xy+z\Rightarrow h'=z\Rightarrow h=\tfrac{z^2}{2}+C", font_size=34)
        s3b = MathTex(r"f=e^x\cos y+xyz+\tfrac{z^2}{2}+C", font_size=38)
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.play(Indicate(comps[2]), run_time=0.6)
            self.nb_add(s3)
            self.sync(tr, text, "The potential function is")
            self.nb_add(s3b, buff=0.4, gray=False)
            boxed(self, s3b)
        self.rest()

        # 12 — check
        chk = VGroup(MathTex(r"f_x=e^x\cos y+yz=M", r"\ \checkmark", font_size=32),
                     MathTex(r"f_y=-e^x\sin y+xz=N", r"\ \checkmark", font_size=32),
                     MathTex(r"f_z=xy+z=P", r"\ \checkmark", font_size=32))
        for c in chk:
            c[1].set_color(C_ANSWER)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            for k, c in enumerate(chk):
                self.nb_add(c, gray=False, run_time=0.8)
                self.play(Indicate(comps[k], color=C_ANSWER), run_time=0.5)
        self.rest()
        self.play(FadeOut(comps), run_time=0.4)

        # 13 — exact differential forms
        self.nb_clear()
        self.chapter(4, "Exact differential forms")
        e1 = MathTex(r"M\,dx+N\,dy+P\,dz=df\ \ (\text{exact})\qquad\int_A^B df=f(B)-f(A)", font_size=32)
        e2 = MathTex(r"\int_{(1,1,1)}^{(2,3,-1)}y\,dx+x\,dy+4\,dz", font_size=36)
        e3 = MathTex(r"f=xy+4z:\ \ f(B)-f(A)=2-5=-3", font_size=36)
        text = vo[13]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "The expression")
            self.nb_add(e1, gray=False)
            self.sync(tr, text, "For example")
            self.nb_add(e2)
            self.sync(tr, text, "with f equals")
            self.nb_add(e3, buff=0.4)
            self.sync(tr, text, "which is minus three")
            boxed(self, e3)
        self.rest()

        # 14 — recipe flowchart
        r_head = Tex("Recipe", font_size=40, color=YELLOW)
        b1 = flow_box(r"1 component test $+$ domain without holes?", YELLOW)
        b_no = flow_box(r"not conservative $\to$ compute the long way (16.2)", C_WRONG, size=26)
        b2 = flow_box(r"2 find $f$: $\int M\,dx+g(y,z)$ $\to$ match $N$ $\to$ match $P$", C_ANSWER, size=26)
        b3 = flow_box(r"3 answer: $f(B)-f(A)$", C_ANSWER)
        no_l = Tex("no", font_size=26, color=C_WRONG)
        yes_l = Tex("yes", font_size=26, color=C_ANSWER)
        chart = VGroup(r_head, b1, b_no, b2, b3).arrange(DOWN, buff=0.45)
        b_no.shift(LEFT * 0.0)
        a_no = Arrow(b1.get_bottom(), b_no.get_top(), buff=0.05, color=C_WRONG, stroke_width=3)
        no_l.next_to(a_no, LEFT, buff=0.1)
        a_yes = CurvedArrow(b1.get_right() + RIGHT * 0.05, b2.get_right() + RIGHT * 0.05, angle=-PI / 2,
                            color=C_ANSWER, stroke_width=3)
        yes_l.next_to(a_yes, RIGHT, buff=0.1)
        a_3 = Arrow(b2.get_bottom(), b3.get_top(), buff=0.05, color=C_ANSWER, stroke_width=3)
        body = VGroup(chart, a_no, no_l, a_yes, yes_l, a_3)
        rcard = card_left(self, body)
        text = vo[14]
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(rcard[0]), FadeIn(r_head), run_time=0.5)
            self.sync(tr, text, "One: apply")
            self.play(FadeIn(b1), run_time=0.5)
            self.sync(tr, text, "Two: if the test fails")
            self.play(GrowArrow(a_no), FadeIn(no_l), FadeIn(b_no), run_time=0.7)
            self.sync(tr, text, "If it passes")
            self.play(Create(a_yes), FadeIn(yes_l), FadeIn(b2), run_time=0.7)
            self.sync(tr, text, "Three: for a line integral")
            self.play(GrowArrow(a_3), FadeIn(b3), run_time=0.7)
        self.rest()

        # 15 — summary
        self.summary(vo[15],
                     [r"Component test: the table of partial derivatives must be symmetric.",
                      r"The test only works on a domain without holes.",
                      r"Find $f$: integrate one component, then match the others."],
                     ["One:", "Two:", "Three:"])


# =============================================================================
#  Exercises
# =============================================================================
def say_fill(scene, tr, text, tbl, r, items, run_time=0.45):
    """items: list of (column, tex, phrase); each entry appears when its phrase is spoken."""
    for c, tex, ph in items:
        if ph:
            scene.sync(tr, text, ph)
        scene.play(tbl.fill(r, c, tex), run_time=run_time)


VO["ex01"] = [
    "Exercise one from section sixteen point three. Is the field F equals y z, i, plus x z, j, plus x y, k, conservative?",
    "The field is defined everywhere in space, so the domain has no holes. That means we can use the component test.",
    "First, name the components. M is y z, N is x z, and P is x y.",
    "Now fill in the table of partial derivatives. Row M, for y z: the x derivative is zero, the y derivative is z, and the z derivative is y.",
    "Row N, for x z: the x derivative is z, the y derivative is zero, and the z derivative is x.",
    "Row P, for x y: the x derivative is y, the y derivative is x, and the z derivative is zero.",
    "Now compare the mirror pairs. M y is z, and N x is z: equal. M z is y, and P x is y: equal. N z is x, and P y is x: equal. All three pairs match.",
    "So the table is symmetric, the domain has no holes, and the field is conservative.",
    "Bonus: can we guess the potential? Each component is the product of the other two coordinates. Try f equals x y z. Its x derivative is y z, its y derivative is x z, and its z derivative is x y. That is exactly F.",
    "Because F is conservative, its line integral between two points is simply the difference in x y z. For example, from the origin to the point one, two, three, the work is six.",
    "Summary. One: first check the domain, then apply the component test. Two: a table of nine partial derivatives keeps your work organised; only the three mirror pairs matter. Three: if all three pairs match, the field is conservative.",
]


class Ex16_3_01(FlatScene):
    def construct(self):
        vo = VO["ex01"]
        self.start("16.3 — Exercise 1",
                   r"\mathbf F=yz\,\mathbf i+xz\,\mathbf j+xy\,\mathbf k\quad\text{conservative?}", checklist=CHECK_TEST)
        self.intro(vo[0])

        # 1 — domain
        dom = card_left(self, Tex(r"domain $=$ all of space\\$\to$ no holes $\checkmark$", font_size=40, color=C_ANSWER),
                        color=C_ANSWER)
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.play(FadeIn(dom), run_time=0.6)
        self.rest()
        self.play(FadeOut(dom), run_time=0.4)

        # 2 — components
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.nb_add(MathTex(r"M=yz,\ \ N=xz,\ \ P=xy", font_size=38))
        self.rest()

        # 3-5 — table rows
        tbl = CompTable()
        rows = [(vo[3], 0, [(0, "0", "the x derivative is zero"), (1, "z", "the y derivative is z"),
                            (2, "y", "and the z derivative is y")]),
                (vo[4], 1, [(0, "z", "the x derivative is z"), (1, "0", "the y derivative is zero"),
                            (2, "x", "and the z derivative is x")]),
                (vo[5], 2, [(0, "y", "the x derivative is y"), (1, "x", "the y derivative is x"),
                            (2, "0", "and the z derivative is zero")])]
        for k, (text, r, items) in enumerate(rows):
            with self.voiceover(text=text) as tr:
                if k == 0:
                    self.check_step(1)
                    show_table(self, tbl, run_time=0.8)
                say_fill(self, tr, text, tbl, r, items)
            self.rest(0.6)

        # 6 — the pairs
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            for k, ph in enumerate(["M y is z", "M z is y", "N z is x"]):
                self.sync(tr, text, ph)
                judge_pair(self, tbl, k, True)
        self.rest()

        # 7 — verdict
        v = Tex(r"conservative $\checkmark$", font_size=40, color=C_ANSWER)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(v, gray=False)
            boxed(self, v)
        self.rest()

        # 8 — guess the potential
        g = MathTex(r"f=xyz,\quad \nabla f=yz\,\mathbf i+xz\,\mathbf j+xy\,\mathbf k\ \checkmark", font_size=34)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Try f equals")
            self.nb_add(g, gray=False)
            self.sync(tr, text, "That is exactly F")
            self.play(Indicate(g), run_time=0.8)
        self.rest()

        # 9 — a line integral
        li = MathTex(r"\int_{(0,0,0)}^{(1,2,3)}\mathbf F\cdot d\mathbf r=f(1,2,3)-f(0,0,0)=6", font_size=34)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "For example")
            self.nb_add(li, buff=0.4)
            boxed(self, li)
        self.rest()

        self.summary(vo[10],
                     [r"First check the domain, then apply the component test.",
                      r"A table of nine partial derivatives: only the three mirror pairs matter.",
                      r"All three pairs match $\Rightarrow$ conservative."],
                     ["One:", "Two:", "Three:"])


VO["ex03"] = [
    "Exercise three. Is the field F equals y i, plus x plus z, j, minus y k, conservative?",
    "Again the field is defined everywhere, so we can use the component test. M is y, N is x plus z, and P is minus y.",
    "Pause and think: which pair would you check first?",
    "Let's fill in the table. Row M, for y: zero, one, zero. Row N, for x plus z: one, zero, one. Row P, for minus y: zero, minus one, zero.",
    "Compare the pairs. M y is one, and N x is one: equal. M z is zero, and P x is zero: equal. But N z is one, while P y is minus one. Not equal.",
    "One failing pair is enough. The field is not conservative, so its line integrals depend on the path.",
    "Let's confirm this with a closed loop, because for a conservative field every loop gives zero. Take a unit square in the y z plane, where x is zero. We go from the origin to zero, one, zero, then up to zero, one, one, then back to zero, zero, one, and down to the origin.",
    "In this plane, F dot d r equals z d y minus y d z. On the first side, z is zero and d z is zero, so we get zero. On the second side, y is one and z goes from zero to one: the integral of minus d z gives minus one.",
    "On the third side, z is one and y goes back from one to zero: the integral of d y from one to zero gives minus one. On the last side, y is zero and d y is zero, so we get zero.",
    "The total around the loop is minus two, not zero. That confirms it: the field is not conservative.",
    "Summary. One: a single failing pair proves that the field is not conservative. Two: for such a field, line integrals depend on the path, and loops can give non zero work. Three: a quick loop calculation is a good way to double check.",
]


class Ex16_3_03(FlatScene):
    def construct(self):
        vo = VO["ex03"]
        self.start("16.3 — Exercise 3",
                   r"\mathbf F=y\,\mathbf i+(x+z)\,\mathbf j-y\,\mathbf k\quad\text{conservative?}", checklist=CHECK_TEST)
        self.intro(vo[0])

        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.sync(tr, text, "M is y")
            self.nb_add(MathTex(r"M=y,\ \ N=x+z,\ \ P=-y", font_size=38))
        self.rest()

        self.pause(vo[2], "Which pair would you check first?")

        # 3 — table
        tbl = CompTable()
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            show_table(self, tbl, run_time=0.8)
            self.sync(tr, text, "Row M")
            fill_row(self, tbl, 0, ["0", "1", "0"], run_time=0.3)
            self.sync(tr, text, "Row N")
            fill_row(self, tbl, 1, ["1", "0", "1"], run_time=0.3)
            self.sync(tr, text, "Row P")
            fill_row(self, tbl, 2, ["0", "-1", "0"], run_time=0.3)
        self.rest()

        # 4 — pairs
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            for k, ph, ok in [(0, "M y is one", True), (1, "M z is zero", True), (2, "But N z is one", False)]:
                self.sync(tr, text, ph)
                judge_pair(self, tbl, k, ok)
            self.nb_add(MathTex(r"N_z=1\neq P_y=-1", font_size=36, color=C_WRONG), gray=False)
        self.rest()

        # 5 — verdict
        v = Tex("not conservative", font_size=40, color=C_WRONG)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(v, gray=False)
            boxed(self, v, color=C_WRONG)
        self.rest()
        self.play(FadeOut(tbl), run_time=0.5)

        # 6 — unit square in the yz plane
        self.nb_clear()
        self.chapter(1, "Check with a loop")
        O = np.array([-4.9, -2.1, 0])
        U = 3.2

        def Q(y, z):
            return O + U * np.array([y, z, 0])
        axes = VGroup(Arrow(Q(-0.15, 0), Q(1.35, 0), buff=0, stroke_width=2, color=GRAY_B, tip_length=0.18),
                      Arrow(Q(0, -0.15), Q(0, 1.35), buff=0, stroke_width=2, color=GRAY_B, tip_length=0.18))
        ax_l = VGroup(MathTex("y", font_size=32).next_to(Q(1.35, 0), DOWN, buff=0.1),
                      MathTex("z", font_size=32).next_to(Q(0, 1.35), LEFT, buff=0.1))
        plane = Tex(r"plane $x=0$", font_size=28, color=GRAY_B).move_to(Q(0.95, 1.3))
        corners = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
        sides = VGroup(*[Line(Q(*corners[i]), Q(*corners[i + 1]), color=YELLOW, stroke_width=5) for i in range(4)])
        tips = VGroup(*[tip(lambda s, i=i: Q(*(np.array(corners[i]) + s * (np.array(corners[i + 1]) - np.array(corners[i])))),
                            0.5, YELLOW) for i in range(4)])
        clabs = VGroup(MathTex("(0,0,0)", font_size=26).next_to(Q(0, 0), DL, buff=0.08),
                       MathTex("(0,1,0)", font_size=26).next_to(Q(1, 0), DR, buff=0.08),
                       MathTex("(0,1,1)", font_size=26).next_to(Q(1, 1), UR, buff=0.08),
                       MathTex("(0,0,1)", font_size=26).next_to(Q(0, 1), UL, buff=0.08))
        nums = VGroup(*[MathTex(str(i + 1), font_size=28, color=YELLOW).move_to(
            (Q(*corners[i]) + Q(*corners[i + 1])) / 2 + d) for i, d in
            enumerate([DOWN * 0.3, RIGHT * 0.3, UP * 0.3, LEFT * 0.3])])
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Take a unit square")
            self.play(FadeIn(axes), FadeIn(ax_l), FadeIn(plane), run_time=0.6)
            for i, ph in enumerate(["We go from the origin", "then up to", "then back to", "and down to"]):
                self.sync(tr, text, ph)
                self.play(Create(sides[i]), FadeIn(tips[i]), FadeIn(clabs[i]), FadeIn(nums[i]), run_time=0.7)
        self.rest()

        # 7-9 — the four sides
        dot = Dot(Q(0, 0), radius=0.1, color=WHITE)
        l7a = MathTex(r"x=0:\ \mathbf F\cdot d\mathbf r=z\,dy-y\,dz", font_size=36)
        l7b = MathTex(r"\text{side 1: }0,\qquad\text{side 2: }\int_0^1-1\,dz=-1", font_size=34)
        l8 = MathTex(r"\text{side 3: }\int_1^0 1\,dy=-1,\qquad\text{side 4: }0", font_size=34)
        l9 = MathTex(r"\oint=0-1-1+0=-2\neq0", font_size=40, color=C_WRONG)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.add(dot)
            self.nb_add(l7a)
            self.sync(tr, text, "On the first side")
            self.play(dot.animate.move_to(Q(1, 0)), Indicate(nums[0]), run_time=1.0)
            self.sync(tr, text, "On the second side")
            self.play(dot.animate.move_to(Q(1, 1)), Indicate(nums[1]), run_time=1.0)
            self.nb_add(l7b)
        self.rest()
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "On the third side")
            self.play(dot.animate.move_to(Q(0, 1)), Indicate(nums[2]), run_time=1.0)
            self.sync(tr, text, "On the last side")
            self.play(dot.animate.move_to(Q(0, 0)), Indicate(nums[3]), run_time=1.0)
            self.nb_add(l8)
        self.rest()
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.nb_add(l9, buff=0.4, gray=False)
            boxed(self, l9, color=C_WRONG)
        self.rest()

        self.summary(vo[10],
                     [r"A single failing pair proves: not conservative.",
                      r"Then line integrals depend on the path; loops can give non-zero work.",
                      r"A quick loop calculation is a good double check."],
                     ["One:", "Two:", "Three:"])


VO["ex07"] = [
    "Exercise seven. Find a potential function f for the field F equals two x i, plus three y j, plus four z k.",
    "We need a function f with f x equals two x, f y equals three y, and f z equals four z.",
    "A quick test first. Each component depends only on its own variable, so all mixed partial derivatives are zero. The table is symmetric, and the field is conservative.",
    "Step one: integrate M with respect to x. Two x gives x squared. The constant may depend on y and z, so f equals x squared, plus g of y and z.",
    "Step two: the y derivative of f is g y, because x squared contains no y. Set it equal to N: g y equals three y. Integrate: g equals three halves y squared, plus a function h of z.",
    "Step three: the z derivative of f is now h prime of z. Set it equal to P: h prime equals four z. So h equals two z squared, plus a constant C.",
    "The potential function is x squared, plus three halves y squared, plus two z squared, plus C.",
    "Check: the x derivative is two x, the y derivative is three y, and the z derivative is four z. Correct.",
    "Notice that the constant C can be anything. Every choice gives a valid potential function, because constants disappear when you take the gradient. In line integrals, C cancels in f of B minus f of A.",
    "Summary. One: write down the three equations: f x equals M, f y equals N, and f z equals P. Two: integrate one of them, and keep a function of the remaining variables as the constant. Three: always check by taking the gradient.",
]


class Ex16_3_07(FlatScene):
    def construct(self):
        vo = VO["ex07"]
        self.start("16.3 — Exercise 7",
                   r"\mathbf F=2x\,\mathbf i+3y\,\mathbf j+4z\,\mathbf k,\quad f=\ ?", checklist=CHECK_POT)
        self.intro(vo[0])

        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.nb_add(MathTex(r"f_x=2x,\quad f_y=3y,\quad f_z=4z", font_size=38))
        self.rest()

        # 2 — quick test: only the diagonal
        tbl = CompTable()
        text = vo[2]
        with self.voiceover(text=text) as tr:
            show_table(self, tbl, run_time=0.8)
            self.play(tbl.fill(0, 0, "2"), tbl.fill(1, 1, "3"), tbl.fill(2, 2, "4"), run_time=0.6)
            self.sync(tr, text, "so all mixed")
            self.play(*[tbl.fill(r, c, "0") for r in range(3) for c in range(3) if r != c], run_time=0.8)
            self.sync(tr, text, "The table is symmetric")
            for k in range(3):
                judge_pair(self, tbl, k, True, run_time=0.35)
        self.rest()
        self.play(FadeOut(tbl), run_time=0.4)

        comps = big_components([r"M=2x", r"N=3y", r"P=4z"], size=56, buff=0.5)
        self.play(FadeIn(comps), run_time=0.5)
        s3 = MathTex(r"f=x^2+", r"g(y,z)", font_size=38)
        s3[1].set_color(YELLOW)
        s4 = MathTex(r"f_y=g_y\overset{!}{=}3y\ \Rightarrow\ g=\tfrac32y^2+h(z)", font_size=36)
        s5 = MathTex(r"f_z=h'(z)\overset{!}{=}4z\ \Rightarrow\ h=2z^2+C", font_size=36)
        for k, (txt, m, c) in enumerate([(vo[3], s3, 0), (vo[4], s4, 1), (vo[5], s5, 2)]):
            with self.voiceover(text=txt) as tr:
                self.check_step(k)
                self.play(Indicate(comps[c]), run_time=0.6)
                self.nb_add(m)
            self.rest()

        ans = MathTex(r"f=x^2+\tfrac32y^2+2z^2+C", font_size=40)
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.nb_add(ans, buff=0.4, gray=False)
            boxed(self, ans)
        self.rest()

        chk = MathTex(r"f_x=2x,\ \ f_y=3y,\ \ f_z=4z\ \checkmark", font_size=36, color=C_ANSWER)
        text = vo[7]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(chk, gray=False)
        self.rest()
        self.play(FadeOut(comps), run_time=0.4)

        # 8 — any constant C
        vers = VGroup(*[MathTex(rf"x^2+\tfrac32y^2+2z^2{s}", font_size=36) for s in ["", "+5", "-2"]])
        vers.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.4, 1.9, 0])
        grad = MathTex(r"\text{all: }\nabla f=2x\,\mathbf i+3y\,\mathbf j+4z\,\mathbf k", font_size=36, color=C_GRAD)
        grad.move_to([-3.4, -0.6, 0])
        arrs = VGroup(Arrow(vers.get_bottom(), grad.get_top(), buff=0.2, color=GRAY_B, stroke_width=3))
        cc = MathTex(r"f(B)-f(A):\ C\text{ cancels}", font_size=36, color=YELLOW).move_to([-3.4, -2.2, 0])
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.play(LaggedStart(*[FadeIn(v) for v in vers], lag_ratio=0.3), run_time=1.0)
            self.sync(tr, text, "because constants disappear")
            self.play(*[GrowArrow(a) for a in arrs], FadeIn(grad), run_time=0.8)
            self.sync(tr, text, "In line integrals")
            self.play(FadeIn(cc), run_time=0.6)
        self.rest()

        self.summary(vo[9],
                     [r"Write down $f_x=M$, $f_y=N$, $f_z=P$.",
                      r"Integrate one; the constant is a function of the remaining variables.",
                      r"Always check by taking the gradient."],
                     ["One:", "Two:", "Three:"])


VO["ex11"] = [
    "Exercise eleven. Find a potential function for the field F with these components. M equals ln x plus sec squared of x plus y. N equals sec squared of x plus y, plus y over y squared plus z squared. And P equals z over y squared plus z squared.",
    "This looks complicated, but the method is exactly the same. We do not even need to test first: if we manage to find f, the field is automatically conservative.",
    "Step one: integrate M with respect to x, holding y and z fixed. M has two terms, so we integrate them one at a time.",
    "The integral of ln x is a standard one: integration by parts gives x ln x minus x. The integral of sec squared of x plus y, with respect to x, is tan of x plus y, because the derivative of tan is sec squared.",
    "So f equals x ln x minus x, plus tan of x plus y, plus g of y and z.",
    "Step two: take the y derivative of f. The terms with only x give zero. Tan of x plus y gives sec squared of x plus y. And we add g y.",
    "Set it equal to N. Sec squared of x plus y, plus g y, equals sec squared of x plus y, plus y over y squared plus z squared. The sec squared terms cancel. So g y equals y over y squared plus z squared.",
    "Pause and think: how do you integrate y over y squared plus z squared, with respect to y?",
    "The top is half the derivative of the bottom. Substitute u equals y squared plus z squared, so d u equals two y d y. The integral becomes one half ln u. So g equals one half ln of y squared plus z squared, plus a function h of z.",
    "Step three: take the z derivative of f. Only the logarithm contains z. Its derivative is one half, times two z, over y squared plus z squared, which is z over y squared plus z squared. Plus h prime of z.",
    "Set it equal to P, which is z over y squared plus z squared. Those terms cancel, so h prime is zero, and h is a constant C.",
    "The potential function is x ln x minus x, plus tan of x plus y, plus one half ln of y squared plus z squared, plus C.",
    "Check one component. The x derivative of x ln x minus x is ln x plus one minus one, which is ln x. Plus sec squared of x plus y. That is M. The other two checks work the same way.",
    "Summary. One: the method works even for complicated fields: integrate, match, match. Two: integrate term by term, and use standard integrals like ln x and sec squared. Three: in the matching steps most terms cancel; what is left determines the unknown function.",
]


class Ex16_3_11(FlatScene):
    def construct(self):
        vo = VO["ex11"]
        M_t = r"M=\ln x+\sec^2(x+y)"
        N_t = r"N=\sec^2(x+y)+\frac{y}{y^2+z^2}"
        P_t = r"P=\frac{z}{y^2+z^2}"
        prob = VGroup(MathTex(M_t, font_size=28, color=C_M), MathTex(N_t, font_size=28, color=C_N),
                      MathTex(P_t + r",\qquad f=\ ?", font_size=28, color=C_P)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        self.start("16.3 — Exercise 11", prob, checklist=CHECK_POT)
        text = vo[0]
        with self.voiceover(text=text) as tr:
            self.play(Write(self.title_mob), run_time=1.0)
            for k, ph in enumerate(["M equals", "N equals", "And P equals"]):
                self.sync(tr, text, ph)
                self.play(Write(prob[k]), run_time=1.0)
        self.rest()

        # 1 — card
        c1 = card_left(self, Tex(r"find $f$ $\Rightarrow$ conservative automatically", font_size=38, color=YELLOW))
        text = vo[1]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "We do not even need")
            self.play(FadeIn(c1), run_time=0.6)
        self.rest()
        self.play(FadeOut(c1), run_time=0.4)
        comps = big_components([M_t, N_t, P_t], size=42, buff=0.45)
        self.play(FadeIn(comps), run_time=0.6)

        # 2-4 — step 1
        s2 = MathTex(r"f=\int\ln x\,dx+\int\sec^2(x+y)\,dx", font_size=34)
        s3 = MathTex(r"\int\ln x\,dx=x\ln x-x\ (\text{by parts}),\quad \int\sec^2(x+y)\,dx=\tan(x+y)", font_size=30)
        s4 = MathTex(r"f=x\ln x-x+\tan(x+y)+", r"g(y,z)", font_size=36)
        s4[1].set_color(YELLOW)
        text = vo[2]
        with self.voiceover(text=text) as tr:
            self.check_step(0)
            self.play(Indicate(comps[0]), run_time=0.6)
            self.nb_add(s2)
        self.rest()
        text = vo[3]
        with self.voiceover(text=text) as tr:
            self.nb_add(s3)
        self.rest()
        text = vo[4]
        with self.voiceover(text=text) as tr:
            self.nb_add(s4, gray=False)
            self.play(Indicate(s4[1]), run_time=0.6)
        self.rest()

        # 5-6 — step 2
        s5 = MathTex(r"f_y=\sec^2(x+y)+g_y", font_size=36)
        s6 = MathTex(r"\sec^2(x+y)", r"+g_y\overset{!}{=}", r"\sec^2(x+y)", r"+\frac{y}{y^2+z^2}", font_size=34)
        s6b = MathTex(r"\Rightarrow\ g_y=\frac{y}{y^2+z^2}", font_size=36)
        text = vo[5]
        with self.voiceover(text=text) as tr:
            self.check_step(1)
            self.nb_add(s5)
        self.rest()
        text = vo[6]
        with self.voiceover(text=text) as tr:
            self.play(Indicate(comps[1]), run_time=0.6)
            self.nb_add(s6)
            self.sync(tr, text, "The sec squared terms cancel")
            self.strike(s6[0], run_time=0.4, owner=s6)
            self.strike(s6[2], run_time=0.4, owner=s6)
            self.sync(tr, text, "So g y equals")
            self.nb_add(s6b, gray=False)
        self.rest()

        # 7 — pause
        self.pause(vo[7], r"$\displaystyle\int\frac{y}{y^2+z^2}\,dy=\ ?$")

        # 8 — substitution
        s8 = MathTex(r"u=y^2+z^2,\ du=2y\,dy:\ \int\frac{y}{y^2+z^2}dy=\tfrac12\ln(y^2+z^2)", font_size=32)
        s8b = MathTex(r"\Rightarrow\ g=\tfrac12\ln(y^2+z^2)+h(z)", font_size=36)
        text = vo[8]
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, "Substitute u")
            self.nb_add(s8)
            self.sync(tr, text, "So g equals")
            self.nb_add(s8b, gray=False)
        self.rest()

        # 9-10 — step 3
        s9 = MathTex(r"f_z=\frac{z}{y^2+z^2}+h'(z)", font_size=36)
        s10 = MathTex(r"\overset{!}{=}\frac{z}{y^2+z^2}\ \Rightarrow\ h'=0\ \Rightarrow\ h=C", font_size=36)
        text = vo[9]
        with self.voiceover(text=text) as tr:
            self.check_step(2)
            self.play(Indicate(comps[2]), run_time=0.6)
            self.sync(tr, text, "Its derivative is")
            self.nb_add(s9)
        self.rest()
        text = vo[10]
        with self.voiceover(text=text) as tr:
            self.nb_add(s10)
        self.rest()

        # 11 — answer
        ans = MathTex(r"f=x\ln x-x+\tan(x+y)+\tfrac12\ln(y^2+z^2)+C", font_size=36)
        text = vo[11]
        with self.voiceover(text=text) as tr:
            self.nb_add(ans, buff=0.4, gray=False)
            boxed(self, ans)
        self.rest()

        # 12 — check f_x
        chk = MathTex(r"f_x=\ln x+1-1+\sec^2(x+y)=M\ \checkmark", font_size=34, color=C_ANSWER)
        text = vo[12]
        with self.voiceover(text=text) as tr:
            self.check_step(3)
            self.nb_add(chk, gray=False)
            self.sync(tr, text, "That is M")
            self.play(Indicate(comps[0], color=C_ANSWER), run_time=0.8)
        self.rest()

        self.summary(vo[13],
                     [r"Works even for complicated fields: integrate, match, match.",
                      r"Integrate term by term; use standard integrals ($\ln x$, $\sec^2$).",
                      r"Most terms cancel in the matching steps; the rest gives the unknown function."],
                     ["One:", "Two:", "Three:"])


VO["ex18"] = [
    "Exercise eighteen. Evaluate the integral of two cos y d x, plus, one over y minus two x sin y, d y, plus one over z d z, from the point zero, two, one, to the point one, pi over two, two.",
    "We are not given a path at all. That is a strong hint: the form must be exact, so the answer depends only on the end points. Our plan: test, find f, and compute f of B minus f of A.",
    "The components are: M equals two cos y, N equals one over y minus two x sin y, and P equals one over z.",
    "The test. N x is minus two sin y, and M y is minus two sin y: equal. M z is zero, and P x is zero: equal. P y is zero, and N z is zero: equal. The form is exact on the region where y and z are positive, and that region contains both points.",
    "Step one: integrate M with respect to x. Two cos y does not depend on x, so we get two x cos y, plus g of y and z.",
    "Step two: the y derivative is minus two x sin y, plus g y. This must equal one over y minus two x sin y. So g y equals one over y, and g equals ln y, plus h of z.",
    "Step three: the z derivative is h prime of z. This must equal one over z, so h equals ln z. We choose the constant equal to zero.",
    "So f equals two x cos y, plus ln y, plus ln z.",
    "Now evaluate. At the end point B, one, pi over two, two: two times one times cos of pi over two is zero. Then plus ln of pi over two, plus ln two.",
    "At the start point A, zero, two, one: the first term is zero, because x is zero. Then plus ln two, plus ln one, which is zero. So f of A is ln two.",
    "f of B minus f of A: ln of pi over two, plus ln two, minus ln two. The ln two terms cancel, and the answer is ln of pi over two, about zero point four five.",
    "Summary. One: when no path is given, expect an exact form. Two: test, find f, then compute f of B minus f of A. Three: evaluate carefully: cos of pi over two is zero, and ln one is zero.",
]


def exact_scene(scene, vo, title, problem, comps_tex, table_vals, pair_phrases, domain_tex, domain_phrase,
                steps, f_tex, evals, answer_tex, summary_items, plan_text):
    """Shared layout for Ex 18 / Ex 20: test -> find f -> f(B)-f(A).
    steps: [(vo_index, [tex lines], comp_index)], evals: [(vo_index, tex)]"""
    scene.start(title, problem, checklist=CHECK_EXACT, problem_size=26)
    scene.intro(vo[0])

    plan = card_left(scene, Tex(plan_text, font_size=38, color=YELLOW))
    with scene.voiceover(text=vo[1]) as tr:
        scene.play(FadeIn(plan), run_time=0.6)
    scene.rest()
    scene.play(FadeOut(plan), run_time=0.4)

    with scene.voiceover(text=vo[2]) as tr:
        scene.nb_add(MathTex(comps_tex, font_size=34))
    scene.rest()

    # 3 — test with the table
    tbl = CompTable()
    dom = Tex(domain_tex, font_size=30, color=C_ANSWER).move_to([-3.4, -2.3, 0])
    text = vo[3]
    with scene.voiceover(text=text) as tr:
        scene.check_step(0)
        show_table(scene, tbl, run_time=0.8)
        for k, ph in enumerate(pair_phrases):
            scene.sync(tr, text, ph)
            (a, b, _, _, _) = PAIRS[k]
            scene.play(tbl.fill(*a, table_vals[k][0]), tbl.fill(*b, table_vals[k][1]), run_time=0.6)
            judge_pair(scene, tbl, k, True, run_time=0.4)
        scene.sync(tr, text, domain_phrase)
        scene.play(FadeIn(dom), run_time=0.6)
    scene.rest()
    scene.play(FadeOut(tbl), FadeOut(dom), run_time=0.5)
    comps = big_components(comps_tex.replace(r",\ \ ", "|").split("|"), size=42, buff=0.45)
    scene.play(FadeIn(comps), run_time=0.5)

    # 4-6 — find f
    for n, (i, lines, ci) in enumerate(steps):
        with scene.voiceover(text=vo[i]) as tr:
            if n == 0:
                scene.check_step(1)
            scene.play(Indicate(comps[ci]), run_time=0.6)
            for ln in lines:
                scene.nb_add(MathTex(ln, font_size=34))
        scene.rest()

    f_line = MathTex(f_tex, font_size=38)
    with scene.voiceover(text=vo[7]) as tr:
        scene.nb_add(f_line, buff=0.4, gray=False)
        boxed(scene, f_line)
    scene.rest()
    scene.play(FadeOut(comps), run_time=0.4)

    # 8-10 — evaluate
    scene.nb_clear()
    scene.nb_add(f_line.copy().scale(0.85), gray=False, run_time=0.6)
    for n, (i, tex) in enumerate(evals):
        with scene.voiceover(text=vo[i]) as tr:
            if n == 0:
                scene.check_step(2)
            scene.nb_add(MathTex(tex, font_size=34))
        scene.rest()
    ans = MathTex(answer_tex, font_size=40)
    with scene.voiceover(text=vo[10]) as tr:
        scene.nb_add(ans, buff=0.4, gray=False)
        boxed(scene, ans)
        scene.play(Indicate(ans), run_time=0.8)
    scene.rest()

    scene.summary(vo[11], summary_items, ["One:", "Two:", "Three:"])


class Ex16_3_18(FlatScene):
    def construct(self):
        exact_scene(
            self, VO["ex18"], "16.3 — Exercise 18",
            r"\int_{(0,2,1)}^{(1,\pi/2,2)}2\cos y\,dx+\Big(\frac1y-2x\sin y\Big)dy+\frac1z\,dz",
            r"M=2\cos y,\ \ N=\frac1y-2x\sin y,\ \ P=\frac1z",
            [(r"-2\sin y", r"-2\sin y"), ("0", "0"), ("0", "0")],
            ["The test", "M z is zero", "P y is zero"],
            r"domain $y>0,\ z>0$ contains $A$ and $B$", "The form is exact",
            [(4, [r"f=2x\cos y+g(y,z)"], 0),
             (5, [r"f_y=-2x\sin y+g_y\overset{!}{=}\frac1y-2x\sin y", r"\Rightarrow\ g=\ln y+h(z)"], 1),
             (6, [r"f_z=h'(z)\overset{!}{=}\frac1z\ \Rightarrow\ h=\ln z"], 2)],
            r"f=2x\cos y+\ln y+\ln z",
            [(8, r"f(B)=2\cdot1\cdot\cos\tfrac\pi2+\ln\tfrac\pi2+\ln2=\ln\tfrac\pi2+\ln2"),
             (9, r"f(A)=0+\ln2+\ln1=\ln2")],
            r"f(B)-f(A)=\ln\tfrac\pi2\approx0.45",
            [r"No path given $\Rightarrow$ expect an exact form.",
             r"Test, find $f$, then compute $f(B)-f(A)$.",
             r"Evaluate carefully: $\cos\tfrac\pi2=0$, $\ln1=0$."],
            r"no path given $\to$ expect exact\\$\to$ $f(B)-f(A)$")


VO["ex20"] = [
    "Exercise twenty. Evaluate the integral of, two x ln y minus y z, d x, plus, x squared over y minus x z, d y, minus x y d z, from the point one, two, one, to the point two, one, one.",
    "Again no path is given. So we test whether the form is exact, find f, and compute f of B minus f of A.",
    "The components are: M equals two x ln y minus y z. N equals x squared over y, minus x z. And P equals minus x y.",
    "The test. M y is two x over y minus z, and N x is two x over y minus z: equal. M z is minus y, and P x is minus y: equal. N z is minus x, and P y is minus x: equal. The form is exact for y greater than zero, and both points have a positive y.",
    "Step one: integrate M with respect to x. Two x ln y gives x squared ln y. Minus y z gives minus x y z. Plus g of y and z.",
    "Step two: the y derivative of f is x squared over y, minus x z, plus g y. This must equal N, which is x squared over y minus x z. So g y is zero, and g depends only on z: we write h of z.",
    "Step three: the z derivative of f is minus x y, plus h prime of z. This must equal P, which is minus x y. So h prime is zero, and h is a constant. We take zero.",
    "So f equals x squared ln y, minus x y z.",
    "At B, two, one, one: four times ln one, which is zero, minus two times one times one. So f of B is minus two.",
    "At A, one, two, one: one times ln two, minus one times two times one. So f of A is ln two minus two.",
    "f of B minus f of A: minus two, minus, ln two minus two. The twos cancel, and the answer is minus ln two, about minus zero point six nine.",
    "Summary. One: in the matching steps, it is common that g turns out to be zero, or a constant. Two: watch the minus signs when you subtract f of A. Three: f of B minus f of A replaces the whole parametrisation.",
]


class Ex16_3_20(FlatScene):
    def construct(self):
        exact_scene(
            self, VO["ex20"], "16.3 — Exercise 20",
            r"\int_{(1,2,1)}^{(2,1,1)}(2x\ln y-yz)\,dx+\Big(\frac{x^2}{y}-xz\Big)dy-xy\,dz",
            r"M=2x\ln y-yz,\ \ N=\frac{x^2}{y}-xz,\ \ P=-xy",
            [(r"\tfrac{2x}{y}-z", r"\tfrac{2x}{y}-z"), ("-y", "-y"), ("-x", "-x")],
            ["The test", "M z is minus y", "N z is minus x"],
            r"exact for $y>0$; both points have $y>0$", "The form is exact",
            [(4, [r"f=x^2\ln y-xyz+g(y,z)"], 0),
             (5, [r"f_y=\frac{x^2}{y}-xz+g_y\overset{!}{=}N\ \Rightarrow\ g_y=0\ \Rightarrow\ g=h(z)"], 1),
             (6, [r"f_z=-xy+h'\overset{!}{=}-xy\ \Rightarrow\ h=C\ (=0)"], 2)],
            r"f=x^2\ln y-xyz",
            [(8, r"f(B)=4\ln1-2=-2"),
             (9, r"f(A)=\ln2-2")],
            r"f(B)-f(A)=-2-(\ln2-2)=-\ln2\approx-0.69",
            [r"In the matching steps $g$ often turns out to be $0$ or a constant.",
             r"Watch the minus signs when you subtract $f(A)$.",
             r"$f(B)-f(A)$ replaces the whole parametrisation."],
            r"no path $\to$ test, find $f$,\\$f(B)-f(A)$")
