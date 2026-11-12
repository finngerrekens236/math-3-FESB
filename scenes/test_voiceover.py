"""Test-scene: manim-voiceover + Kokoro (lokaal). Twee stemmen om uit te kiezen."""
from manim import *
from manim_voiceover import VoiceoverScene

from _tts import kokoro

TEXT = "This is a test of the voiceover. The circle appears while I speak."


class TestVoiceover(VoiceoverScene):
    voice = "af_heart"  # American English, female

    def construct(self):
        self.set_speech_service(kokoro(self.voice))
        with self.voiceover(text=TEXT) as tracker:
            self.play(Create(Circle(color=BLUE)), run_time=tracker.duration)


class TestVoiceoverMale(TestVoiceover):
    voice = "am_michael"  # American English, male
