# 16.4 Green's theorem in the plane

_HW2 · due 20-11-2026_

## Kernformules

| Begrip | Formule |
|---|---|
| Double integral | $\iint_R f\,dA \approx \sum f(x_k,y_k)\,\Delta x\,\Delta y$; $\iint_R 1\,dA = $ area of $R$ |
| Verticale strips | $\iint_R f\,dA = \int_a^b\!\int_{g_1(x)}^{g_2(x)} f\,dy\,dx$ (binnengrenzen mogen van $x$ afhangen, buitengrenzen zijn getallen) |
| Curl (circulation density) | $(\text{curl}\,\mathbf F)\cdot\mathbf k = \dfrac{\partial N}{\partial x} - \dfrac{\partial M}{\partial y}$ — spin per oppervlakte (schoepenrad; $>0$ CCW) |
| Divergence (flux density) | $\text{div}\,\mathbf F = \dfrac{\partial M}{\partial x} + \dfrac{\partial N}{\partial y}$ — uitstroom per oppervlakte ($>0$ bron, $<0$ put) |
| Green — circulation (tangential) form | $\oint_C M\,dx + N\,dy = \iint_R (N_x - M_y)\,dx\,dy$ |
| Green — flux (normal) form | $\oint_C M\,dy - N\,dx = \iint_R (M_x + N_y)\,dx\,dy$ |
| Area formula | Area$(R) = \tfrac12\oint_C x\,dy - y\,dx$ (uit $M=-\tfrac y2$, $N=\tfrac x2$, curl $=1$) |

Onthouden: curl = **min**, **kruis**-afgeleiden ($N_x - M_y$); div = **plus**, **rechte** afgeleiden ($M_x + N_y$).

## Voorwaarden
- $C$ gesloten, enkelvoudig (simple), **tegen de klok in** (gebied links van je).
- $M, N$ en hun afgeleiden continu op heel $R$ (geen gat! vgl. whirlpool-veld: curl $=0$ maar $\oint = 2\pi$).

## Waarom het werkt
Bedek $R$ met kleine rechthoekjes: circulatie van elk ≈ curl·ΔA. Gedeelde binnenranden worden in tegengestelde
richting doorlopen en heffen elkaar op → alleen de buitenrand $C$ blijft over.

## Recept
1. Gesloten kromme? Gebied tekenen, oriëntatie checken (tegen de klok in).
2. Vier partiële afgeleiden $M_x, M_y, N_x, N_y$.
3. Circulation: $\iint (N_x-M_y)$, flux: $\iint (M_x+N_y)$ — met verticale strips.
4. Constante integrand ⇒ constante × oppervlakte.

## Video's
`videos/16.4 Green's theorem/`

| Video | Scene | Inhoud |
|---|---|---|
| Concept/0 - Double integrals refresher | `DoubleIntegralRefresher` | rechthoekjes, iterated integrals, strips, oppervlakte $\tfrac13$ |
| Concept/1 - Curl & divergence | `CurlDivergence` | schoepenrad, afleiding $N_x-M_y$, vier velden, div, bron/put |
| Concept/2 - Green's theorem | `GreensTheorem` | oriëntatie, binnenranden heffen op, beide vormen, check $2\pi$/$\pi$, area formula |
| Exercises/Ex 05 | `Ex16_4_05` | vierkant: circulation $0$, flux $2$ (+ controle langs 4 zijden) |
| Exercises/Ex 07 | `Ex16_4_07` | driehoek: circulation $9$, flux $-9$ |
| Exercises/Ex 09 | `Ex16_4_09` | lens $y=x^2$, $y=\sqrt x$: circulation $-\tfrac{7}{60}$, flux $-\tfrac{11}{60}$ |
| Exercises/Ex 22 | `Ex16_4_22` | $\oint 3y\,dx+2x\,dy$ onder $\sin x$: $-2$ |
| Exercises/Ex 26 | `Ex16_4_26` | ellips: $\pi ab$ |

HW2 16.4 (zelf maken): opgaven 6, 8, 11, 23, 27.
