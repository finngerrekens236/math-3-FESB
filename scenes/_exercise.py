"""Shared building blocks for exercise videos — see CLAUDE.md "Opgaven-video's (stijl)".

    from _exercise import *

    class Ex16_1_09(ExerciseScene):
        def construct(self):
            self.start("16.1 — Exercise 9", r"\\int_C (x+y)\\,ds")
            ...

Layout: drawing on the left (x < 0.7), "notebook" panel on the right with header
(title + problem), checklist row and a scrolling column of formulas.
"""
from manim import *
from manim_voiceover import VoiceoverScene
import numpy as np

from _tts import kokoro

# --- fixed colours (CLAUDE.md) ---------------------------------------------
C_CURVE = BLUE
C_F = YELLOW
C_NEG = RED
C_DS = GREEN
C_DT = ORANGE
C_ANSWER = GREEN
C_WRONG = RED

SPEED = 0.95
REST = 1.2            # pause after a new formula

# --- notebook geometry (screen coordinates) --------------------------------
NB_LEFT, NB_RIGHT = 1.05, 6.85
NB_W = NB_RIGHT - NB_LEFT
NB_BOTTOM = -3.7
HEADER_TOP = 3.8
LEFT_CENTER = np.array([-3.2, 0.0, 0.0])   # centre of the drawing area


def cam_matrix(phi, theta, gamma=0.0):
    """World -> camera rotation, identical to ManimCE ThreeDCamera.generate_rotation_matrix."""
    return rotation_about_z(gamma) @ rotation_matrix(-phi, RIGHT) @ rotation_about_z(-theta - PI / 2)


def center_for(phi, theta, world_point, screen_point):
    """frame_center such that world_point appears at screen_point in the (phi, theta) view."""
    M = cam_matrix(phi, theta)
    return np.array(world_point, dtype=float) - M.T @ np.array(screen_point, dtype=float)


def face_camera(mob, phi, theta):
    """Rotate a flat mobject (made in the xy-plane) so it faces a camera at (phi, theta)."""
    return mob.rotate(phi, RIGHT, about_point=mob.get_center()).rotate(
        theta + PI / 2, OUT, about_point=mob.get_center())


class ShiftCamera(ThreeDCamera):
    """ThreeDCamera whose frame_center only shifts the 3D projection.

    Stock ManimCE also subtracts frame_center from fixed-in-frame mobjects, and
    caches the cairo transform with the frame_center of the first frame — so a
    scene that *starts* off-centre gets its notebook shifted for ever. Here the
    drawing code always sees ORIGIN; the real centre lives in `_frame_center`.
    """

    @property
    def frame_center(self):
        return ORIGIN

    @frame_center.setter
    def frame_center(self, point):
        self._frame_center.move_to(point)

    def project_points(self, points):
        return super().project_points(np.asarray(points) - self._frame_center.points[0])

    # Submobjects created later (DecimalNumber.set_value, become, ...) are not
    # in fixed_in_frame_mobjects; re-collect the families of the fixed roots
    # before every frame.
    def add_fixed_in_frame_mobjects(self, *mobjects):
        super().add_fixed_in_frame_mobjects(*mobjects)
        self.__dict__.setdefault("_fixed_roots", []).extend(mobjects)

    def remove_fixed_in_frame_mobjects(self, *mobjects):
        super().remove_fixed_in_frame_mobjects(*mobjects)
        roots = self.__dict__.get("_fixed_roots", [])
        self._fixed_roots = [m for m in roots if all(m is not x for x in mobjects)]

    def capture_mobjects(self, mobjects, **kwargs):
        for root in self.__dict__.get("_fixed_roots", []):
            self.fixed_in_frame_mobjects.update(root.get_family())
        super().capture_mobjects(mobjects, **kwargs)


class ExerciseScene(VoiceoverScene, ThreeDScene):
    def __init__(self, **kwargs):
        kwargs.setdefault("camera_class", ShiftCamera)
        super().__init__(**kwargs)

    # ------------------------------------------------------------------ basics
    def fixed(self, *mobs):
        """Register as fixed-in-frame, but keep invisible until animated in."""
        self.add_fixed_in_frame_mobjects(*mobs)
        self.remove(*mobs)
        return mobs[0] if len(mobs) == 1 else mobs

    def rest(self, t=REST):
        self.wait(t)

    def sync(self, tr, text, phrase, lead=0.0):
        """Wait until (approximately) `phrase` is spoken — estimated from its
        character position in the voiceover text."""
        i = text.find(phrase)
        if i < 0:
            raise ValueError(f"phrase not in voiceover text: {phrase!r}")
        target = tr.duration * i / len(text) - lead
        elapsed = tr.duration - tr.get_remaining_duration()
        if target - elapsed > 0.03:
            self.wait(target - elapsed)

    def to_screen(self, p):
        """Screen position (fixed-in-frame coordinates) of world point p, current camera."""
        cam = self.camera
        v = cam.generate_rotation_matrix() @ (np.array(p, dtype=float) - cam._frame_center.points[0])
        fd, zoom = cam.get_focal_distance(), cam.get_zoom()
        factor = fd / (fd - v[2]) if fd - v[2] > 0 else 1.0
        return np.array([v[0] * factor * zoom, v[1] * factor * zoom, 0.0])

    # --------------------------------------------------------- header/notebook
    def start(self, title, problem, phi=0.0, theta=-PI / 2, frame_center=ORIGIN, problem_size=30):
        self.set_speech_service(kokoro(speed=SPEED))
        self.set_camera_orientation(phi=phi, theta=theta, frame_center=frame_center)

        panel = RoundedRectangle(corner_radius=0.15, width=NB_W + 0.4, height=7.8,
                                 stroke_color=GRAY_D, stroke_width=1.5,
                                 fill_color="#0e0e0e", fill_opacity=1)
        panel.move_to([(NB_LEFT + NB_RIGHT) / 2, 0, 0])
        self.add_fixed_in_frame_mobjects(panel)

        self.title_mob = Text(title, font_size=30)
        self.problem_mob = problem if isinstance(problem, Mobject) else MathTex(problem, font_size=problem_size)
        hdr = VGroup(self.title_mob, self.problem_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        if hdr.width > NB_W:
            hdr.scale_to_fit_width(NB_W)
        hdr.shift([NB_LEFT - hdr.get_left()[0], HEADER_TOP - hdr.get_top()[1], 0])

        items = ["1 parametrise", r"2 $\lvert\mathbf r'(t)\rvert$", r"3 $f(\mathbf r(t))$", "4 integrate"]
        self.checklist = VGroup(*[Tex(s, font_size=24) for s in items]).arrange(RIGHT, buff=0.35)
        self.checklist.set_color(GRAY_B)
        self.checklist.shift([NB_LEFT - self.checklist.get_left()[0],
                              hdr.get_bottom()[1] - 0.3 - self.checklist.get_center()[1], 0])
        self.fixed(self.title_mob, self.problem_mob, self.checklist)

        self.nb_top = self.checklist.get_bottom()[1] - 0.3
        self.nb_cursor = self.nb_top
        self.nb_items = []
        self.parked = VGroup()

    def intro(self, text):
        with self.voiceover(text=text) as tr:
            self.play(Write(self.title_mob), run_time=min(1.5, tr.duration * 0.25))
            self.play(Write(self.problem_mob), run_time=min(3.0, tr.duration * 0.5))
        self.rest()

    def nb_add(self, mob, run_time=1.2, buff=0.3, gray=True, anim=None):
        """Add a line to the notebook. Older lines turn GRAY; when the column is
        full everything scrolls up and the top lines fade out."""
        if mob.width > NB_W:
            mob.scale_to_fit_width(NB_W)
        mob.shift([NB_LEFT - mob.get_left()[0], self.nb_cursor - mob.get_top()[1], 0])
        over = max(0.0, NB_BOTTOM - mob.get_bottom()[1])
        shift = UP * over
        mob.shift(shift)

        anims, keep = [], []
        for it in self.nb_items:
            if it.get_top()[1] + over > self.nb_top + 0.05:
                anims.append(FadeOut(it, shift=shift))
                continue
            keep.append(it)
            if over > 0 or gray:
                a = it.animate
                if over > 0:
                    a = a.shift(shift)
                if gray:
                    a = a.set_color(GRAY)
                anims.append(a)
        self.nb_items = keep + [mob]
        self.fixed(mob)
        self.play(*anims, anim if anim is not None else Write(mob), run_time=run_time)
        self.nb_cursor = mob.get_bottom()[1] - buff
        return mob

    def nb_clear(self, run_time=0.6):
        if self.nb_items:
            self.play(FadeOut(VGroup(*self.nb_items)), run_time=run_time)
        self.nb_items = []
        self.nb_cursor = self.nb_top

    def nb_park(self, mob, run_time=1.2, scale=0.8):
        """Move a result to a 'parking spot' at the top of the notebook; the rest is cleared."""
        target = mob.copy().scale(scale)
        if len(self.parked):
            target.next_to(self.parked, DOWN, aligned_edge=LEFT, buff=0.15)
        else:
            target.shift([NB_LEFT - target.get_left()[0], self.nb_top - target.get_top()[1], 0])
        others = [i for i in self.nb_items if i is not mob]
        anims = [Transform(mob, target)]
        if others:
            anims.append(FadeOut(VGroup(*others)))
        self.play(*anims, run_time=run_time)
        self.parked.add(mob)
        self.nb_items = []
        self.nb_cursor = self.parked.get_bottom()[1] - 0.35

    def strike(self, mob, run_time=0.6, owner=None):
        """Red strike-through. `owner` (a notebook line) carries the strike when it scrolls."""
        line = Line(mob.get_left() + LEFT * 0.05, mob.get_right() + RIGHT * 0.05,
                    color=C_WRONG, stroke_width=5)
        self.fixed(line)
        self.play(Create(line), run_time=run_time)
        if owner is not None:
            owner.add(line)
        return line

    # ---------------------------------------------------------------- checklist
    def show_checklist(self):
        self.play(FadeIn(self.checklist), run_time=0.6)

    def check_step(self, k):
        anims = [self.checklist[k].animate.set_color(YELLOW)]
        anims += [self.checklist[j].animate.set_color(WHITE) for j in range(k)]
        self.play(*anims, run_time=0.5)

    # -------------------------------------------------------------------- cards
    def _card(self, content, opacity=0.95, region=None):
        if region is None:
            bg = Rectangle(width=config.frame_width + 1, height=config.frame_height + 1,
                           fill_color=BLACK, fill_opacity=opacity, stroke_width=0)
        else:
            bg = region
        grp = VGroup(bg, content)
        self.fixed(grp)
        return grp

    def chapter(self, n, name):
        """Title card (~2 s) before every part."""
        txt = Tex(f"Chapter {n} — {name}", font_size=52)
        line = Line(LEFT * 3, RIGHT * 3, color=YELLOW, stroke_width=3).next_to(txt, DOWN, buff=0.3)
        card = self._card(VGroup(txt, line))
        self.play(FadeIn(card), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(card), run_time=0.4)

    def pause(self, text, question, seconds=4.0, phrase="Pause", before=None):
        """Voiceover block that ends in a 'Pause and think' card + silent countdown."""
        icon = VGroup(Rectangle(width=0.16, height=0.6), Rectangle(width=0.16, height=0.6))
        icon.arrange(RIGHT, buff=0.14).set_fill(WHITE, 1).set_stroke(width=0)
        head = VGroup(icon, Text("Pause and think", font_size=46)).arrange(RIGHT, buff=0.3)
        q = Tex(question, font_size=46, color=YELLOW)
        bar_bg = Rectangle(width=4, height=0.14, stroke_color=GRAY, stroke_width=1)
        prog = ValueTracker(1.0)
        bar = Rectangle(width=4, height=0.14, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
        content = VGroup(head, q, bar_bg).arrange(DOWN, buff=0.6)
        bar.move_to(bar_bg)
        bar.add_updater(lambda m: m.stretch_to_fit_width(max(4 * prog.get_value(), 1e-3)).align_to(bar_bg, LEFT))
        card = self._card(VGroup(content, bar))
        with self.voiceover(text=text) as tr:
            if before is not None:
                before(tr)
            self.sync(tr, text, phrase)
            self.play(FadeIn(card), run_time=0.6)
        self.play(prog.animate.set_value(0), run_time=seconds, rate_func=linear)
        bar.clear_updaters()
        self.play(FadeOut(card), run_time=0.5)

    def your_turn(self, lines, run_time=1.0):
        """'Your turn' card over the drawing area (notebook stays visible). HW only."""
        title = Text("Your turn", font_size=44, color=YELLOW)
        body = VGroup(*[Tex(s, font_size=32) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        content = VGroup(title, body).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        if content.width > 6.6:
            content.scale_to_fit_width(6.6)
        content.move_to(LEFT_CENTER)
        bg = RoundedRectangle(corner_radius=0.2, width=7.4, height=max(content.height + 1.0, 3.5),
                              fill_color="#141414", fill_opacity=0.97, stroke_color=YELLOW, stroke_width=2)
        bg.move_to(LEFT_CENTER)
        card = self._card(content, region=bg)
        self.play(FadeIn(card), run_time=run_time)
        return card

    def summary(self, text, items, phrases, extra=None, extra_phrase=None):
        """Summary card: 3 numbered takeaways, shown in sync with the voiceover."""
        head = Text("Summary", font_size=48, color=YELLOW)
        rows = VGroup(*[Tex(f"{i + 1}.\\ \\ {s}", font_size=34) for i, s in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        parts = [head, rows]
        foot = None
        if extra:
            foot = Tex(extra, font_size=28, color=GRAY_B)
            parts.append(foot)
        content = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        if content.width > config.frame_width - 1.2:
            content.scale_to_fit_width(config.frame_width - 1.2)
        content.move_to(ORIGIN)
        bg = Rectangle(width=config.frame_width + 1, height=config.frame_height + 1,
                       fill_color=BLACK, fill_opacity=1, stroke_width=0)
        self.fixed(bg, head, *rows, *([foot] if foot else []))
        with self.voiceover(text=text) as tr:
            self.play(FadeIn(bg), Write(head), run_time=1.0)
            for row, ph in zip(rows, phrases):
                self.sync(tr, text, ph)
                self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.8)
            if foot is not None:
                self.sync(tr, text, extra_phrase)
                self.play(FadeIn(foot), run_time=0.8)
        self.wait(2.5)

    def left_overlay(self):
        """Opaque panel over the drawing area, for 2D graphs on top of a 3D drawing."""
        bg = Rectangle(width=7.9, height=config.frame_height + 0.2, fill_color=BLACK, fill_opacity=1,
                       stroke_width=0).move_to([-3.2, 0, 0])
        self.fixed(bg)
        return bg

    def question_card(self, text, question, phrase):
        """Card with a question, shown from `phrase` until the end of the voiceover block."""
        q = Tex(question, font_size=50, color=YELLOW)
        card = self._card(q)
        with self.voiceover(text=text) as tr:
            self.sync(tr, text, phrase)
            self.play(FadeIn(card), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(card), run_time=0.5)

    def table_row(self, cells, colors, col_x=(0, 0.9, 2.5, 4.1), size=32):
        g = VGroup()
        for x, c, col in zip(col_x, cells, colors):
            m = MathTex(c, font_size=size, color=col)
            m.move_to([x, 0, 0], aligned_edge=LEFT)
            g.add(m)
        return g
