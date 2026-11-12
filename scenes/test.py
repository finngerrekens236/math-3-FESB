"""Test-scene: controleert dat Manim + ffmpeg werken (geen LaTeX nodig)."""
from manim import *


class TestScene(Scene):
    def construct(self):
        title = Text("Math 3 — FESB", font_size=56)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        axes = Axes(x_range=[-3, 3, 1], y_range=[-1.5, 1.5, 1], x_length=8, y_length=4)
        graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        label = Text("y = sin(x)", font_size=32, color=BLUE).next_to(axes, DOWN)

        self.play(Create(axes))
        self.play(Create(graph), FadeIn(label))
        self.wait(1)
