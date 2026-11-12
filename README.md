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
manim -ql scenes/test.py TestScene   # lage kwaliteit (test)
manim -qh scenes/test.py TestScene   # hoge kwaliteit
```
Output komt in `media/` (niet in git).

## Structuur
- `scenes/` — Manim-scenes
- `topics/` — uitleg per onderwerp
- `PROGRESS.md` / `TODO.md` — voortgang en taken
