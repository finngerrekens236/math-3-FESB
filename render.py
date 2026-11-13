"""Render Manim scenes and copy the result into videos/ with a readable name.

Each scene file defines a dict OUTPUT mapping scene class -> target path
(relative to videos/, without extension), e.g.

    OUTPUT = {"Ex16_1_09": "16.1 Line integrals (scalar)/Exercises/Ex 09"}

Usage (from anywhere; paths are relative to the repo root):
    python render.py scenes/16_1_line_integrals_scalar.py Ex16_1_09
    python render.py scenes/16_1_line_integrals_scalar.py            # all scenes in OUTPUT
    python render.py scenes/16_1_line_integrals_scalar.py Ex16_1_09 --low

Quality: -qm (720p30) by default, --low for -ql (480p15), --high for -qh (1080p60).
Renders to the normal media/ folder (no absolute --media_dir: that breaks MathTex
on this machine, see CLAUDE.md) and copies mp4 + srt afterwards.
"""
import argparse
import ast
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEOS = ROOT / "videos"
QUALITY = {"low": ("-ql", "480p15"), "medium": ("-qm", "720p30"), "high": ("-qh", "1080p60")}
MIKTEX = Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"


def read_output(scene_file: Path) -> dict:
    """Read OUTPUT = {...} from the scene file without importing it."""
    tree = ast.parse(scene_file.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "OUTPUT" for t in node.targets
        ):
            return ast.literal_eval(node.value)
    return {}


def python_exe() -> str:
    venv = ROOT / ".venv" / "Scripts" / "python.exe"
    if not venv.exists():
        venv = ROOT / ".venv" / "bin" / "python"
    return str(venv) if venv.exists() else sys.executable


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="scene file, e.g. scenes/16_1_line_integrals_scalar.py")
    ap.add_argument("scenes", nargs="*", help="scene class(es); default: all in OUTPUT")
    q = ap.add_mutually_exclusive_group()
    q.add_argument("--low", action="store_const", dest="quality", const="low")
    q.add_argument("--high", action="store_const", dest="quality", const="high")
    ap.set_defaults(quality="medium")
    args = ap.parse_args()

    scene_file = (Path.cwd() / args.file).resolve()
    if not scene_file.exists():
        scene_file = (ROOT / args.file).resolve()
    if not scene_file.exists():
        print(f"Scene file not found: {args.file}")
        return 1

    output = read_output(scene_file)
    scenes = args.scenes or list(output)
    if not scenes:
        print(f"No scenes given and no OUTPUT dict in {scene_file.name}")
        return 1
    missing = [s for s in scenes if s not in output]
    if missing:
        print(f"No OUTPUT entry for: {', '.join(missing)} — add it to OUTPUT in {scene_file.name}")
        return 1

    env = os.environ.copy()
    if shutil.which("latex", path=env.get("PATH")) is None and MIKTEX.exists():
        env["PATH"] = f"{MIKTEX}{os.pathsep}{env.get('PATH', '')}"
    env.setdefault("PYTHONIOENCODING", "utf-8")

    flag, res = QUALITY[args.quality]
    rel = scene_file.relative_to(ROOT)
    for scene in scenes:
        print(f"\n=== {scene}  ({res}) ===")
        cmd = [python_exe(), "-m", "manim", flag, str(rel), scene]
        if subprocess.run(cmd, cwd=ROOT, env=env).returncode != 0:
            print(f"Render failed: {scene}")
            return 1

        src_dir = ROOT / "media" / "videos" / scene_file.stem / res
        target = VIDEOS / output[scene]
        target.parent.mkdir(parents=True, exist_ok=True)
        for ext in (".mp4", ".srt"):
            src = src_dir / f"{scene}{ext}"
            if src.exists():
                shutil.copy2(src, target.with_suffix(ext))
                print(f"  -> {target.with_suffix(ext).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
