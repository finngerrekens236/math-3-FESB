# PROGRESS

## Log

| Datum | Topic | Scene(s) | Status |
|---|---|---|---|
| 2026-11-12 | Setup | `scenes/test.py` · `TestScene` | ✅ gerenderd (-ql) |
| 2026-11-12 | Setup | MiKTeX 25.12 + `MathTex`-test | ✅ werkt |
| 2026-11-12 | Overzicht | `topics/README.md` + 8 topic-bestanden | ✅ klaar |
| 2026-11-13 | 16.1 Line integrals (scalar) | `scenes/16_1_line_integrals_scalar.py` · 3 scenes | ✅ gerenderd (-ql) |
| 2026-11-13 | Setup | manim-voiceover 0.4.0 + gTTS · `scenes/test_voiceover.py` · `TestVoiceover` | ✅ gerenderd (-ql), audio OK |
| 2026-11-13 | 16.1 Line integrals (scalar) | voiceover toegevoegd aan alle 3 scenes (tekst door Claude, in `VO`) | ✅ gerenderd (-ql), audio synchroon |
| 2026-11-13 | Setup | Kokoro (lokaal) via kokoro-manim-voiceover 0.1.5 · helper `scenes/_tts/` · `TestVoiceover` (af_heart), `TestVoiceoverMale` (am_michael) | ✅ gerenderd (-ql), audio OK |
| 2026-11-13 | 16.1 Line integrals (scalar) | voiceover omgezet gTTS → Kokoro `af_heart` (gekozen stem) | ✅ gerenderd (-ql), audio synchroon |
| 2026-11-13 | Setup | `render.py` + `videos/`-mappen (Concept/Exercises), `videos/` in `.gitignore` | ✅ werkt |
| 2026-11-13 | 16.1 Line integrals (scalar) | 3 conceptscenes opnieuw gerenderd (-qm) naar `videos/16.1 …/Concept/` | ✅ |
| 2026-11-13 | 16.1 Line integrals (scalar) | `Ex16_1_09` — opgave 9, proefvideo opgaven-reeks (Kokoro) | ✅ gerenderd (-qm), wacht op feedback Finn |
| 2026-11-13 | Setup | stijlregels opgaven-video's (`CLAUDE.md`) + gedeelde helpers `scenes/_exercise.py`; Kokoro speed 0.95 | ✅ |
| 2026-11-13 | 16.1 Line integrals (scalar) | `Ex16_1_09` opnieuw: lange versie (7 hoofdstukken, 5:18) | ✅ gerenderd (-ql) + gecontroleerd; -qm nog te doen |
| 2026-11-13 | 16.1 Line integrals (scalar) | `Ex16_1_09` goedgekeurd door Finn (stijl = template voor volgende opgaven) | ✅ |
| 2026-11-13 | Setup | `_exercise.py`: `ShiftCamera` — fix verschoven beeld bij start met `frame_center ≠ 0` + getallen (`DecimalNumber`) blijven fixed-in-frame | ✅ |
| 2026-11-13 | 16.1 Line integrals (scalar) | `Ex16_1_10` (HW, stopt bij opgestelde integraal, 3:54) — HW-check OK | ✅ gerenderd (-qm) |
| 2026-11-13 | 16.1 Line integrals (scalar) | `Ex16_1_14` (volledig uitgewerkt, improper integral, 4:10) | ✅ gerenderd (-ql) mét fixes + gecontroleerd (2026-11-16) |
| 2026-11-13 | 16.1 Line integrals (scalar) | `Ex16_1_15` (HW, stopt bij twee opgestelde integralen, 3:49) — HW-check OK | ✅ gerenderd (-ql) + gecontroleerd |
| 2026-11-15 | 16.1 Line integrals (scalar) | HW2 16.1-opgaven af (Finn) | ✅ |
| 2026-11-15 | Setup | `_exercise.py`: `_Notebook`-mixin + `FlatScene` (2D, minder geheugen) naast `ExerciseScene` (3D); `render.py --no_latex_cleanup` + `TTS_CACHE_TAG` → parallel renderen in aparte terminals | ✅ |
| 2026-11-15 | 16.2 Vector fields, work, circulation, flux | `VectorFieldsIntro` (4:16) | ✅ gerenderd (-ql) + gecontroleerd |
| 2026-11-15 | 16.2 Vector fields, work, circulation, flux | `WorkLineIntegral` (5:24) | ✅ gerenderd (-ql) + gecontroleerd |
| 2026-11-15 | 16.2 Vector fields, work, circulation, flux | `FlowCirculationFlux` (3:56) | ✅ gerenderd (-ql) + gecontroleerd |
| 2026-11-15 | 16.2 Vector fields, work, circulation, flux | `Ex16_2_04` (gradient, 1:48) | ✅ gerenderd (-ql) + gecontroleerd |
| 2026-11-15 | 16.2 Vector fields, work, circulation, flux | `Ex16_2_01` (3:08), `Ex16_2_12` (4:47), `Ex16_2_25` (3:59), `Ex16_2_15` (3:01) | ✅ gerenderd (-ql) + gecontroleerd |
| 2026-11-15 | 16.2 Vector fields, work, circulation, flux | 720p (-qm) van alle 16.2-video's | ⏳ nog te doen (480p eerst voor feedback) |
| 2026-11-16 | 16.3 Path independence, conservative fields, potentials | `ConservativeIntro` (4:55), `TestAndPotential` (5:44), `Ex16_3_01` (2:02), `Ex16_3_03` (2:21), `Ex16_3_07` (2:01), `Ex16_3_11` (3:18), `Ex16_3_18` (2:42), `Ex16_3_20` (2:38) | ✅ gerenderd (-ql) + gecontroleerd (fix: kaders bleven staan na nb_clear) |
| 2026-11-16 | 16.1 Line integrals (scalar) | `Ex16_1_09` lange versie (5:18) + `Ex16_1_14` opnieuw → `videos/16.1 …/Exercises/` | ✅ gerenderd (-ql) + gecontroleerd — 16.1 compleet |
| 2026-11-16 | 16.4 Green's theorem | `scenes/16_4_greens_theorem.py`: 8 scenes geschreven (`DoubleIntegralRefresher`, `CurlDivergence`, `GreensTheorem`, `Ex16_4_05/07/09/22/26`) | ⏳ NIET gerenderd (Finn rendert zelf); py_compile + import + sync/LaTeX-check OK |

## Begrip per topic

| Topic | Snap ik | Snap ik nog niet | Scene(s) |
|---|---|---|---|
| 13.1 Curves in space | ja | | — |
| 13.3 Arc length in space | ja | | — |
| 14.3 Partial derivatives | ja| | — |
| 14.5 Directional derivatives & gradient | ja | | — |
| 16.1 Line integrals of scalar functions | | idee ∫f ds en waarom ds = \|r'(t)\| dt klikt nog niet (eerste video's te snel) | `LineIntegralIdea`, `LineIntegralFence`, `LineIntegralComputation`, `Ex16_1_09`, `Ex16_1_10` (HW), `Ex16_1_14`, `Ex16_1_15` (HW) |
| 16.2 Vector fields, work, circulation, flux | | | `VectorFieldsIntro`, `WorkLineIntegral`, `FlowCirculationFlux`, `Ex16_2_01`, `Ex16_2_04`, `Ex16_2_12`, `Ex16_2_25`, `Ex16_2_15` |
| 16.3 Path independence, conservative fields, potential functions | | | `ConservativeIntro`, `TestAndPotential`, `Ex16_3_01`, `Ex16_3_03`, `Ex16_3_07`, `Ex16_3_11`, `Ex16_3_18`, `Ex16_3_20` |
| 16.4 Green's theorem in the plane | | | `DoubleIntegralRefresher`, `CurlDivergence`, `GreensTheorem`, `Ex16_4_05`, `Ex16_4_07`, `Ex16_4_09`, `Ex16_4_22`, `Ex16_4_26` |
