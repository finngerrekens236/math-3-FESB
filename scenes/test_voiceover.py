"""Test-scene: controleert manim-voiceover + gTTS (Engelse stem)."""
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class TestVoiceover(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))

        circle = Circle(color=BLUE)
        with self.voiceover(
            text="This is a test of the voiceover. The circle appears while I speak."
        ) as tracker:
            self.play(Create(circle), run_time=tracker.duration)
