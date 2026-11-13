# Math 3 — FESB · Manim-animaties

Animaties bij Math 3 (FESB), gemaakt met [Manim Community](https://www.manim.community/).

## Setup (Windows)
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Vereist ook **ffmpeg** en **LaTeX** (MiKTeX):
```powershell
winget install Gyan.FFmpeg
winget install MiKTeX.MiKTeX
```

## Renderen
```powershell
python render.py scenes/16_1_line_integrals_scalar.py Ex16_1_09         # 720p (standaard)
python render.py scenes/16_1_line_integrals_scalar.py Ex16_1_09 --low   # 480p (test)
python render.py scenes/16_1_line_integrals_scalar.py                   # alle scenes uit OUTPUT
```
Video's (+ ondertitels) komen in `videos/<topic>/Concept|Exercises/` (niet in git).
`render.py` gebruikt automatisch de Python uit `.venv`.

## Structuur
- `scenes/` — Manim-scenes
- `topics/` — uitleg per onderwerp
- `PROGRESS.md` / `TODO.md` — voortgang en taken
