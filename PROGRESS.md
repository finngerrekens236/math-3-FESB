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
| 2026-11-13 | 16.1 Line integrals (scalar) | `Ex16_1_10` (HW, stopt bij opgestelde integraal) | ⏳ code klaar, nog niet gerenderd (render afgebroken: geheugen) |
| 2026-11-13 | 16.1 Line integrals (scalar) | `Ex16_1_14` (volledig uitgewerkt, improper integral) | ⏳ code klaar, nog niet gerenderd |
| 2026-11-13 | 16.1 Line integrals (scalar) | `Ex16_1_15` (HW, stopt bij twee opgestelde integralen) | ⏳ code klaar, nog niet gerenderd |

## Begrip per topic

| Topic | Snap ik | Snap ik nog niet | Scene(s) |
|---|---|---|---|
| 13.1 Curves in space | ja | | — |
| 13.3 Arc length in space | ja | | — |
| 14.3 Partial derivatives | ja| | — |
| 14.5 Directional derivatives & gradient | ja | | — |
| 16.1 Line integrals of scalar functions | | idee ∫f ds en waarom ds = \|r'(t)\| dt klikt nog niet (eerste video's te snel) | `LineIntegralIdea`, `LineIntegralFence`, `LineIntegralComputation`, `Ex16_1_09`, `Ex16_1_10` (HW), `Ex16_1_14`, `Ex16_1_15` (HW) |
| 16.2 Vector fields, work, circulation, flux | | | — |
| 16.3 Path independence, conservative fields, potential functions | | | — |
| 16.4 Green's theorem in the plane | | | — |
