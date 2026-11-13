"""Shared TTS helper: Kokoro (local, free) via kokoro-manim-voiceover.

Model files (~355 MB) are downloaded once to <repo>/models/kokoro/ (git-ignored).
Usage in a scene file (scenes/ is on sys.path when manim loads a scene):

    from _tts import kokoro
    self.set_speech_service(kokoro())               # default voice, speed 1.0
    self.set_speech_service(kokoro(speed=0.95))     # exercise videos
"""
from pathlib import Path

from kokoro_mv import KokoroService

MODEL_DIR = Path(__file__).resolve().parents[2] / "models" / "kokoro"
BASE_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
MODEL_FILE = "kokoro-v1.0.onnx"
VOICES_FILE = "voices-v1.0.bin"

VOICE = "af_heart"  # chosen by Finn (2026-11-13), American English female


def _ensure(name: str) -> Path:
    """Download a model file once (own downloader: the package's progress
    output uses emoji, which crashes on a cp1252 Windows console)."""
    path = MODEL_DIR / name
    if not path.exists():
        import urllib.request
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".part")
        print(f"Downloading {name} -> {path} ...")
        urllib.request.urlretrieve(BASE_URL + name, tmp)
        tmp.replace(path)
    return path


def kokoro(voice: str = VOICE, speed: float = 1.0) -> KokoroService:
    kwargs = {}
    if speed != 1.0:
        # The package's cache key ignores speed -> separate cache dir per speed,
        # otherwise old audio at another speed would be reused.
        from manim import config
        kwargs["cache_dir"] = str(Path(config.media_dir) / "voiceovers" / f"kokoro_{voice}_{speed:g}")
    return KokoroService(
        model_path=str(_ensure(MODEL_FILE)),
        voices_path=str(_ensure(VOICES_FILE)),
        voice=voice,
        speed=speed,
        lang="en-us",
        **kwargs,
    )
