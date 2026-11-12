# CLAUDE.md — Math 3 (FESB) Manim-animaties

Repo met Manim Community-animaties bij het vak Math 3 (FESB).

## Structuur
- `topics/` — notities/uitleg per onderwerp (Markdown), één bestand per topic.
- `scenes/` — Manim-scenes (`.py`), één bestand per topic, bv. `scenes/fourier_series.py`.
- `PROGRESS.md` — wat af is (scene, topic, datum, commit).
- `TODO.md` — openstaande taken.
- `media/` — renderoutput, staat in `.gitignore`, nooit committen.

## Omgeving
- Python 3.12, virtualenv in `.venv/` (`.venv\Scripts\activate` of `.venv/Scripts/manim`).
- Manim Community (`from manim import *`) — **niet** ManimGL / 3b1b-manim.
- ffmpeg: aanwezig. LaTeX: MiKTeX 25.12 (user-install, AutoInstall=1 voor ontbrekende pakketten),
  `C:\Users\Gebruiker\AppData\Local\Programs\MiKTeX\miktex\bin\x64` staat in user-PATH.
- Altijd renderen vanuit de repo-root met de standaard (relatieve) `media/`-map. Een absolute
  `--media_dir` met 8.3-kort pad (`GEBRUI~1`) laat `MathTex` falen ("latex failed but did not produce a log file").

## Werkwijze voor "TAAK VOOR CLAUDE CODE"-blokken
Als de gebruiker een blok met kop **TAAK VOOR CLAUDE CODE** plakt:

1. **Lezen** — lees het hele blok; check `TODO.md`/`PROGRESS.md` en bestaande scenes op overlap.
2. **Scene schrijven** — Manim Community, in `scenes/<topic>.py`.
   - Eén `Scene`-klasse per deelanimatie, duidelijke CamelCase-naam.
   - Formules met `MathTex`; kleuren/constanten bovenaan het bestand.
   - Optioneel: korte uitleg in `topics/<topic>.md`.
3. **Testrender (lage kwaliteit)** — vanuit de repo-root:
   `.venv/Scripts/manim -ql scenes/<topic>.py <SceneNaam>`
   Fouten oplossen tot de render slaagt. Geen hoge kwaliteit renderen tenzij gevraagd
   (`-qh` / `-qk` alleen op verzoek).
4. **Bijwerken** — `PROGRESS.md`: regel toevoegen (datum, topic, scene(s), status).
   `TODO.md`: taak afvinken/verwijderen, nieuwe vervolgtaken toevoegen.
5. **Commit + push** — Conventional Commit, bv. `feat(scenes): add FourierSeries scene`,
   daarna `git push`. `media/` nooit committen.

## Conventies
- Bestandsnamen: snake_case. Scene-klassen: CamelCase.
- Houd scenes kort (< ~60 s) en per concept opgesplitst.
- Taal in animaties: Engels (vak FESB), tenzij de taak anders zegt.
