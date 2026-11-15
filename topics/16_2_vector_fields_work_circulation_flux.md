# 16.2 Vector fields, work, circulation, flux

_HW2 · due 20-11-2026_

## Kernformules

| Begrip | Formule |
|---|---|
| Vector field | $\mathbf F = M\,\mathbf i + N\,\mathbf j + P\,\mathbf k$ (pijl met **staart** in het punt) |
| Gradient field | $\nabla f = f_x\,\mathbf i + f_y\,\mathbf j + f_z\,\mathbf k$ — wijst bergop, $\perp$ niveaulijnen |
| Work / flow | $\displaystyle\int_C \mathbf F\cdot\mathbf T\,ds = \int_C \mathbf F\cdot d\mathbf r = \int_a^b \mathbf F(\mathbf r(t))\cdot\mathbf r'(t)\,dt$ |
| Waarom geen $\lvert\mathbf r'\rvert$ | $\mathbf T\,ds = \dfrac{\mathbf r'}{\lvert\mathbf r'\rvert}\,\lvert\mathbf r'\rvert\,dt = \mathbf r'(t)\,dt = d\mathbf r$ |
| Andere notatie | $\mathbf F\cdot d\mathbf r = M\,dx + N\,dy + P\,dz$, met $dx = x'(t)\,dt$ enz. |
| Richting | $\displaystyle\int_{-C} \mathbf F\cdot d\mathbf r = -\int_C \mathbf F\cdot d\mathbf r$ (anders dan bij 16.1!) |
| Circulation | $\displaystyle\oint_C \mathbf F\cdot\mathbf T\,ds$ (gesloten kromme) |
| Flux (vlak, tegen de klok in) | $\displaystyle\oint_C \mathbf F\cdot\mathbf n\,ds = \oint_C M\,dy - N\,dx$, met $\mathbf n = \mathbf T\times\mathbf k$ |

## Methode (work)
1. $\mathbf F(\mathbf r(t))$ — kromme invullen in $\mathbf F$
2. $\mathbf r'(t)$
3. dot product $\mathbf F(\mathbf r(t))\cdot\mathbf r'(t)$
4. integreren van $a$ naar $b$ **in de looprichting** (grenzen mogen van groot naar klein lopen)

Pad in stukken: per stuk een eigen parametrisatie, integralen optellen.
Horizontaal stuk: $dy = 0$; verticaal stuk: $dx = 0$.

## Lopend voorbeeld (intro-video's 2 en 3)
$\mathbf F = (x-y)\,\mathbf i + x\,\mathbf j$, $\mathbf r(t) = \cos t\,\mathbf i + \sin t\,\mathbf j$:
$\mathbf F\cdot\mathbf r' = 1 - \sin t\cos t$.
- Kwartcirkel $0\le t\le\pi/2$: work $= \tfrac\pi2 - \tfrac12 \approx 1.07$
- Volle cirkel: circulation $= 2\pi$, flux $= \int_0^{2\pi}\cos^2 t\,dt = \pi$

## Video's
`videos/16.2 Vector fields, work, circulation, flux/`

| Video | Scene | Inhoud |
|---|---|---|
| Concept/1 - Vector fields & gradient fields | `VectorFieldsIntro` | wat/hoe tekenen, radial/spin, $\nabla T$ op heatmap |
| Concept/2 - Work (F dot dr) | `WorkLineIntegral` | Riemann-som → $\int\mathbf F\cdot\mathbf T\,ds$ → $\int\mathbf F\cdot d\mathbf r$, richting, $M\,dx+N\,dy$ |
| Concept/3 - Flow, circulation, flux | `FlowCirculationFlux` | flow, circulation $2\pi$, flux $\oint M\,dy-N\,dx = \pi$ |
| Exercises/Ex 01 | `Ex16_2_01` | $\nabla(x^2+y^2+z^2)^{-1/2} = -\dfrac{x\mathbf i+y\mathbf j+z\mathbf k}{(x^2+y^2+z^2)^{3/2}}$ |
| Exercises/Ex 04 | `Ex16_2_04` | $\nabla(xy+yz+xz) = (y+z)\mathbf i+(x+z)\mathbf j+(x+y)\mathbf k$ |
| Exercises/Ex 12 | `Ex16_2_12` | zelfde veld langs 3 paden → steeds $3$ (gradient field, teaser 16.3) |
| Exercises/Ex 25 | `Ex16_2_25` | $x=y^2$ van $(4,2)$ naar $(1,-1)$: $-\tfrac{39}{2}$ (grenzen $2\to-1$) |
| Exercises/Ex 15 | `Ex16_2_15` | $\int_C(x^2+y^2)\,dy$ over $(0,0)\to(3,0)\to(3,3)$: $36$ |

HW2 16.2 (zelf maken): opgaven 2, 3, 11, 23, 24.
