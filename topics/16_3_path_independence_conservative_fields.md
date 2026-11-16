# 16.3 Path independence, conservative fields, potential functions

_HW2 · due 20-11-2026_

## Kernformules

| Begrip | Formule |
|---|---|
| Conservative (path independent) | $\int_C \mathbf F\cdot d\mathbf r$ hetzelfde voor elk pad $C$ van $A$ naar $B$ → notatie $\int_A^B \mathbf F\cdot d\mathbf r$ |
| Potential function | $\mathbf F = \nabla f$ |
| Fundamental theorem of line integrals | $\displaystyle\int_C \nabla f\cdot d\mathbf r = f(B) - f(A)$ (vgl. $\int_a^b f'(x)\,dx = f(b)-f(a)$) |
| Waarom (kettingregel) | $\frac{d}{dt} f(\mathbf r(t)) = \nabla f(\mathbf r(t))\cdot\mathbf r'(t)$ |
| Gesloten lus | $\mathbf F$ conservative $\iff \oint_C \mathbf F\cdot d\mathbf r = 0$ voor elke lus |
| Equivalent | $\mathbf F=\nabla f \iff$ conservative $\iff \oint = 0$ (stuksgewijs gladde krommen, samenhangend domein) |
| Component test | $P_y = N_z,\quad M_z = P_x,\quad N_x = M_y$ (gemengde afgeleiden, 14.3) |
| Exact form | $M\,dx + N\,dy + P\,dz = df$ ⇒ $\int_A^B = f(B) - f(A)$ |
| Mechanica | $\mathbf F = -\nabla U$, $U = -f$; $U_\text{gravity} = mgz$, $U_\text{spring} = \tfrac12 kx^2$ |

## Component test = symmetrische tabel
Rijen $M, N, P$ · kolommen $\partial/\partial x, \partial/\partial y, \partial/\partial z$. Diagonaal doet niet mee;
de drie spiegelparen moeten gelijk zijn: $M_y \leftrightarrow N_x$, $M_z \leftrightarrow P_x$, $N_z \leftrightarrow P_y$.
Eén paar dat niet klopt ⇒ **niet** conservative.

**Valkuil — gaten:** de test werkt alleen op een *simply connected* domein (elke lus kan tot een punt krimpen).
Voorbeeld: $\mathbf F = \dfrac{-y\,\mathbf i + x\,\mathbf j}{x^2+y^2}$ voldoet aan de test, maar $\oint_{\text{eenheidscirkel}} = 2\pi \neq 0$
(domein = ruimte zonder de $z$-as).

## Recept
1. **Component test** + domein zonder gaten?
2. Nee → niet conservative → lijnintegraal "de lange weg" (16.2).
   Ja → **vind $f$**: $f = \int M\,dx + g(y,z)$ → $f_y \overset!= N$ geeft $g$ → $f_z \overset!= P$ geeft $h(z)$ (+ $C$).
3. Lijnintegraal van $A$ naar $B$: **$f(B) - f(A)$**. Altijd controleren: $\nabla f = \mathbf F$.

## Video's
`videos/16.3 Path independence, conservative fields, potentials/`

| Video | Scene | Inhoud |
|---|---|---|
| Concept/1 - Path independence & potential functions | `ConservativeIntro` | path independence, $\mathbf F=\nabla f$, fundamental theorem, lussen, mechanica |
| Concept/2 - Component test & finding potentials | `TestAndPotential` | tabel-test, gaten, $f$ vinden (voorbeeld 3), exact forms, recept |
| Exercises/Ex 01 | `Ex16_3_01` | $yz\,\mathbf i+xz\,\mathbf j+xy\,\mathbf k$: conservative, $f=xyz$ |
| Exercises/Ex 03 | `Ex16_3_03` | $y\,\mathbf i+(x+z)\,\mathbf j-y\,\mathbf k$: niet ($N_z=1\ne P_y=-1$), lus $=-2$ |
| Exercises/Ex 07 | `Ex16_3_07` | $f = x^2+\tfrac32y^2+2z^2+C$ |
| Exercises/Ex 11 | `Ex16_3_11` | $f = x\ln x - x + \tan(x+y) + \tfrac12\ln(y^2+z^2) + C$ |
| Exercises/Ex 18 | `Ex16_3_18` | exact form, $f = 2x\cos y+\ln y+\ln z$: $\ln\tfrac\pi2\approx0.45$ |
| Exercises/Ex 20 | `Ex16_3_20` | exact form, $f = x^2\ln y - xyz$: $-\ln 2\approx-0.69$ |

HW2 16.3 (zelf maken): opgaven 2, 6, 8, 9, 19, 21.
