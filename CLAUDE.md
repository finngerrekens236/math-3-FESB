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
3. **Testrender (lage kwaliteit)** — via `render.py` (zie "Video's"):
   `.venv/Scripts/python render.py scenes/<topic>.py <SceneNaam> --low`
   Fouten oplossen tot de render slaagt; frames controleren op layout.
   Daarna de eindversie op standaardkwaliteit (`-qm`, 720p): zelfde commando zonder `--low`.
   `--high` (1080p) alleen op verzoek.
4. **Bijwerken** — `PROGRESS.md`: regel toevoegen (datum, topic, scene(s), status).
   `TODO.md`: taak afvinken/verwijderen, nieuwe vervolgtaken toevoegen.
5. **Commit + push** — Conventional Commit, bv. `feat(scenes): add FourierSeries scene`,
   daarna `git push`. `media/` nooit committen.

## Video's
- **Altijd renderen via `render.py`** (repo-root), nooit los met `manim`:
  `.venv/Scripts/python render.py scenes/<file>.py [Scene ...] [--low|--high]`
  Zonder scenenaam: alle scenes uit `OUTPUT`. Standaard `-qm` (720p30).
- `render.py` rendert naar `media/` en kopieert `.mp4` + `.srt` naar `videos/<pad>`.
  `videos/` staat in `.gitignore` — nooit committen.
- **Elke nieuwe scene krijgt een regel in de dict `OUTPUT`** bovenaan het scenebestand:
  `"Ex16_1_09": "16.1 Line integrals (scalar)/Exercises/Ex 09"` (pad zonder extensie).
- Structuur: `videos/<§> <Topic>/Concept/<n> - <Naam>` en `videos/<§> <Topic>/Exercises/Ex <nn>`.
- Opgave-scenes: klasse `Ex<hoofdstuk>_<paragraaf>_<nn>`, bv. `Ex16_1_09`.

## Conventies
- Bestandsnamen: snake_case. Scene-klassen: CamelCase (opgaven: `Ex16_1_09`).
- Houd scenes kort (< ~60 s) en per concept opgesplitst. Uitzondering: opgave-video's
  die een "klik" moeten geven mogen ~90 s+ zijn als de taak dat zegt.
- Taal in animaties: Engels (vak FESB), tenzij de taak anders zegt.

## Voiceover
Scenes krijgen Engelse gesproken uitleg via `manim-voiceover` + **Kokoro** (lokaal, gratis, offline).
- Elke scene erft van `VoiceoverScene` (niet `Scene`/`ThreeDScene`); 3D-scenes:
  `class X(VoiceoverScene, ThreeDScene)`.
- Speech service via de gedeelde helper `scenes/_tts/` (`scenes/` staat op `sys.path` bij renderen):
  ```python
  from manim_voiceover import VoiceoverScene
  from _tts import kokoro
  ...
  self.set_speech_service(kokoro())   # gekozen stem = _tts.VOICE
  ```
  Stem wisselen: `VOICE` in `scenes/_tts/__init__.py` aanpassen (niet per scene).
  Gekozen stem: `af_heart` (vrouw, VS). Alternatief getest: `am_michael` (man, VS).
- De gesproken tekst komt uit het veld **"Voiceover"** in het taakblok — niet zelf verzinnen.
  Ontbreekt het veld: vragen, of (na akkoord) zelf schrijven in een `VO`-dict bovenaan het scenebestand.
- Kort per stap: één `with self.voiceover(text="...") as tracker:`-blok per animatiestap,
  animaties met `run_time=tracker.duration` (meerdere animaties: duur verdelen,
  laatste met `tracker.get_remaining_duration()`).
- Modelbestanden (±355 MB) worden bij het eerste gebruik gedownload naar `models/kokoro/`;
  gecachte audio staat in `media/voiceovers/`. Beide staan in `.gitignore` — nooit committen.
- Waarschuwing "SoX could not be found!" kan geen kwaad. Ondertitels (`.srt`) komen naast de video.
