# 16.1 Line integrals of scalar functions

_HW2 · due 20-11-2026_ · Scene: [`scenes/16_1_line_integrals_scalar.py`](../scenes/16_1_line_integrals_scalar.py)

## Idee
Hak de kromme $C$ in stukjes met lengte $\Delta s_k$, kies in elk stukje een punt $P_k$,
en tel op: $\sum f(P_k)\,\Delta s_k$. De limiet voor $n\to\infty$ is

$$\int_C f\,ds = \lim_{n\to\infty}\sum_{k=1}^{n} f(P_k)\,\Delta s_k .$$

Meetkundig (als $f \ge 0$): de oppervlakte van een "hek" met basis $C$ en hoogte $f(x,y)$.

## Berekenen
Met een parametrisatie $\mathbf r(t)$, $a \le t \le b$:

$$\int_C f\,ds = \int_a^b f(\mathbf r(t))\,\lvert\mathbf r'(t)\rvert\,dt .$$

Stappen: parametriseer $C$ → bereken $\lvert\mathbf r'(t)\rvert$ → $ds = \lvert\mathbf r'(t)\rvert\,dt$ → substitueer → integreer.

## Voorbeeld (in de scene)
$f(x,y)=xy$, $C$: $\mathbf r(t)=(2\cos t, 2\sin t)$, $0\le t\le \pi/2$.
$\lvert\mathbf r'(t)\rvert = 2$, dus
$\int_C xy\,ds = \int_0^{\pi/2} 4\cos t\sin t\cdot 2\,dt = 8\cdot\tfrac12 = 4$.

## Valkuilen
- $\lvert\mathbf r'(t)\rvert$ vergeten (dan reken je met $dt$ i.p.v. $ds$).
- Het resultaat hangt **niet** af van de oriëntatie of de gekozen parametrisatie van $C$.

## Scenes
| Klasse | Inhoud |
|---|---|
| `LineIntegralIdea` | Riemann-som langs de kromme, $n = 4 \to 40$, convergeert naar 4 |
| `LineIntegralFence` | 3D: integraal = oppervlakte van het hek |
| `LineIntegralComputation` | stap-voor-stap berekening |

## Voiceover
Alle drie de scenes hebben Engelse voiceover (Kokoro, stem `af_heart`). De tekst staat in de dict `VO`
bovenaan `scenes/16_1_line_integrals_scalar.py` — daar aanpassen en opnieuw renderen.
Duur (-ql): Idea ±40 s, Fence ±27 s, Computation ±44 s.
