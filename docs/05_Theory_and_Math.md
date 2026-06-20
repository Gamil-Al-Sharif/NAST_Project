

***

# 📕 Section 7: The Mathematics of the 20 $C$-Features

The core innovation of the N.A.S.T. framework is its rejection of geometric approximations. When N.A.S.T. evaluates an airfoil (either during the training Crucible or during a CLI `invert` operation), it does not simply search for the highest discrete point in an array. 

Raw coordinate arrays are inherently flawed because the true mathematical crest of an airfoil may exist *between* two discrete points. To solve this, N.A.S.T. builds a **Continuous Parametric Polynomial Manifold** for every airfoil, allowing us to use exact differential calculus to extract the 20 $C$-Features.

---

### 1. Parametric B-Spline Healing & Interpolation
Given a raw set of discrete airfoil coordinates $(X_{raw}, Y_{raw})$, we first parameterize the curve by its cumulative arc-length ($S$) to eliminate infinite vertical slopes ($dy/dx \rightarrow \infty$) at the leading edge.

$$ S_i = \sum_{j=1}^{i} \sqrt{(X_j - X_{j-1})^2 + (Y_j - Y_{j-1})^2} $$

We then fit $C^2$-continuous Cubic Splines to map the coordinates back to the arc-length:
$$ X(s) = \text{CubicSpline}(S, X_{raw}) $$
$$ Y(s) = \text{CubicSpline}(S, Y_{raw}) $$

To evaluate the exact $Y$ coordinate at *any* continuous chord position $X_{target}$, we use the **Scipy Brentq** root-finding algorithm to find the exact arc-length root $s^*$ that satisfies:
$$ f(s) = X(s) - X_{target} = 0 $$
Once $s^*$ is found, the true vertical coordinate is evaluated as $Y(s^*)$.

---

### 2. Macro-Structure (F0 - F3)
With the continuous splines defined for the upper surface ($Y_{up}(x)$) and lower surface ($Y_{lo}(x)$), we mathematically define continuous functions for Thickness $T(x)$ and Camber $C(x)$:

$$ T(x) = Y_{up}(x) - Y_{lo}(x) $$
$$ C(x) = \frac{Y_{up}(x) + Y_{lo}(x)}{2} $$

To find the **Maximum Thickness (F0)** and its **X-Location (F1)**, we use Scipy's `minimize_scalar` bounded optimization to find the exact global maximum of the continuous thickness function between $0.005c$ and $0.995c$:

$$ \text{F1} = \text{arg}\min_{x \in [0.005, 0.995]} (-T(x)) $$
$$ \text{F0} = T(\text{F1}) $$

The **Maximum Camber (F2)** and its **X-Location (F3)** are found identically:
$$ \text{F3} = \text{arg}\min_{x \in [0.005, 0.995]} (-|C(x)|) $$
$$ \text{F2} = C(\text{F3}) $$

---

### 3. Aerodynamic Crests (F4 - F9)
The upper and lower crests represent the absolute physical extremes of the airfoil volume. They are independent of thickness and camber maximums.

**Upper Crest Location (F5) and Height (F4):**
$$ \text{F5} = \text{arg}\min_{x \in [0.005, 0.995]} (-Y_{up}(x)) $$
$$ \text{F4} = Y_{up}(\text{F5}) $$

**Lower Crest Location (F8) and Depth (F7):**
$$ \text{F8} = \text{arg}\min_{x \in [0.005, 0.995]} (Y_{lo}(x)) $$
$$ \text{F7} = Y_{lo}(\text{F8}) $$

**Crest Curvatures (F6 & F9):**
Because we parameterized the curves by arc-length $s$, we can extract the exact analytical curvature $\kappa(s)$ at the crest locations without suffering from vertical asymptote errors. The analytical curvature formula is:

$$ \kappa(s) = \frac{X'(s)Y''(s) - Y'(s)X''(s)}{(X'(s)^2 + Y'(s)^2)^{3/2}} $$
where $X'$ and $Y'$ are the first derivatives (velocity) and $X''$, $Y''$ are the second derivatives (acceleration) of the splines evaluated at the crest arc-length $s_{crest}$.

---

### 4. Leading Edge Constraints (F10 - F13)
The Leading Edge is highly volatile. If we measure properties at exactly $X=0.0$, the math becomes undefined. Therefore, N.A.S.T. evaluates all Leading Edge phenomena at a microscopic setback of $X = 0.005$ (0.5% chord).

**Leading Edge Radii (F10 & F11):**
Using Brentq, we find the arc-length $s_{0.005}$ corresponding to $X=0.005$ for both top and bottom surfaces. We calculate the analytical curvature $\kappa(s)$ at this point. The radius of the osculating circle is exactly:
$$ \text{Radius} = \left| \frac{1}{\kappa(s_{0.005})} \right| $$

**Leading Edge Entry Angles (F12 & F13):**
The true geometric slope of a parametrically defined curve is given by the chain rule: $\frac{dy}{dx} = \frac{dy/ds}{dx/ds}$. The entry wedge angles (in degrees) are therefore:
$$ \theta_{LE} = \left| \frac{180}{\pi} \arctan \left( \frac{Y'(s_{0.005})}{X'(s_{0.005})} \right) \right| $$

---

### 5. Trailing Edge Constraints (F14 - F17)
The trailing edge constraints are evaluated exactly at the terminal arc-length ($s_{max}$), which corresponds to $X=1.0$.

**TE Gap (F14) & Camber Offset (F15):**
$$ \text{F14} = \max(0.0, Y_{up}(1.0) - Y_{lo}(1.0)) $$
$$ \text{F15} = \frac{Y_{up}(1.0) + Y_{lo}(1.0)}{2} $$

**TE Exit Angles (F16 & F17):**
Using the identical chain-rule derivation from the leading edge, but evaluated at $s_{max}$:
$$ \theta_{TE\_Upper} = \frac{180}{\pi} \arctan \left( \frac{Y'_{up}(s_{max})}{X'_{up}(s_{max})} \right) $$
$$ \theta_{TE\_Lower} = \frac{180}{\pi} \arctan \left( \frac{Y'_{lo}(s_{max})}{X'_{lo}(s_{max})} \right) $$

---

### 6. Curvature Inflections (F18 - F19)
An inflection point occurs where the surface transitions from convex to concave, indicating an Adverse Pressure Gradient. Mathematically, this is the exact X-coordinate where the curvature $\kappa(s)$ crosses zero. 

Because curvature naturally approaches zero near the trailing edge, N.A.S.T. bounds the search window between $X=0.05$ and $X=0.95$ to avoid false positives.

We evaluate the curvature array $\kappa_i$ across the bounded grid. We detect the first inflection point by searching for a sign-change multiplier:
$$ \text{If } (\kappa_i \cdot \kappa_{i-1} < 0) \rightarrow \text{Inflection exists at } X_i $$

If no sign change occurs, the value defaults to $0.0$, indicating a perfectly monotonic, non-reflexed surface.

---

Here is the highly detailed **Section 8: The $\beta$-VAE Neural Architecture**. 

This section is targeted toward machine learning engineers, data scientists, and AI researchers. It explains the exact neural topography of the N.A.S.T. engine, why a standard Autoencoder fails at aerospace geometries, and the deep mathematical theory behind the $\beta$-VAE framework and the Kullback-Leibler (KL) Divergence that makes this project possible.

This should be saved inside your `docs/01_Theory_and_Math.md` file, directly beneath Section 7.

***

# 📕 Section 8: The $\beta$-cVAE Neural Architecture

While Section 7 defines the rigid, 20-dimensional physical skeleton of the airfoil (the $C$-Vector), it does not explain how the curves are actually drawn between those 20 nodes. In traditional systems (like CST), the curves are drawn using Bernstein polynomials. In the N.A.S.T. framework, the curves are generated by a **Conditional $\beta$-Variational Autoencoder ($\beta$-cVAE)**.

This section explains how the AI learned to understand fluid-dynamic styling, and how it mathematically organizes that knowledge into the 12-dimensional $Z$-Vector.

---

### 1. Why Standard Autoencoders Fail in Aerospace
A standard Autoencoder consists of an Encoder (which compresses a 256-point airfoil down into 12 numbers) and a Decoder (which decompresses those 12 numbers back into 256 points). 

While standard Autoencoders are good at memorizing shapes, they suffer from a fatal flaw known as a **Discontinuous Latent Space**. If you train a standard Autoencoder on a NACA 0012 and a supercritical airliner wing, it will memorize both. However, if you ask it to generate a shape located *mathematically halfway* between them, it will likely output a corrupted, jagged line. 

In aerospace optimization, Genetic Algorithms must explore the spaces *between* known airfoils to find novel solutions. If the Latent Space is discontinuous, the optimizer will crash the CFD solver.

### 2. The Variational Solution (VAE)
To solve this, N.A.S.T. utilizes a **Variational Autoencoder (VAE)**. Instead of compressing an airfoil into a single discrete point in the 12-D space, the Encoder compresses the airfoil into a **Probability Distribution**. 

For every airfoil, the Encoder outputs two vectors:
*   $\mu$ (Mean)
*   $\sigma^2$ (Variance, logged as $\log(\sigma^2)$ for numerical stability)

During training, we use the **Reparameterization Trick** to sample a specific $Z$-Vector from this distribution:
$$ Z = \mu + \sigma \odot \epsilon $$
*(where $\epsilon \sim \mathcal{N}(0, I)$ is a random noise tensor).*

Because the network is constantly injected with random Gaussian noise during training, it is forced to learn that points located *close to each other* in the 12-D space must decode into similar aerodynamic shapes. This mathematically guarantees a perfectly smooth, continuous Latent Space.

---

### 3. The $\beta$-VAE Framework: Forcing Orthogonal Disentanglement
In a standard VAE, the 12 $Z$-variables are often "entangled." For example, changing $Z_1$ might simultaneously make the trailing edge thicker, shift the camber forward, and sharpen the nose. This entanglement makes it nearly impossible for an optimizer to isolate and tune a specific aerodynamic phenomenon.

N.A.S.T. relies on the **$\beta$-VAE theory** (introduced by Higgins et al., DeepMind, 2017: *"$\beta$-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework"*). 

The $\beta$-VAE modifies the standard loss function by adding an aggressive scalar multiplier ($\beta$) to the **Kullback-Leibler (KL) Divergence** term.

#### The N.A.S.T. Loss Function:
$$ \mathcal{L} = \mathcal{L}_{Recon} + \beta \cdot D_{KL}(q(Z|X,C) || p(Z)) + \lambda \cdot \mathcal{L}_{Physics} $$

1.  **Reconstruction Loss ($\mathcal{L}_{Recon}$):** The Mean Squared Error (MSE) between the AI's generated airfoil and the true target airfoil. N.A.S.T. utilizes an *Adaptive Hunter-Seeker Focal Weighting* here to heavily penalize errors at the leading edge.
2.  **KL Divergence ($D_{KL}$):** This term measures how far the AI's learned probability distribution $q(Z)$ has strayed from a perfect, standard Normal Gaussian sphere $p(Z) \sim \mathcal{N}(0, I)$. 
3.  **Physics Loss ($\mathcal{L}_{Physics}$):** A 2nd-derivative penalty that forces the AI to output $C^2$-continuous curves.

#### The Power of the $\beta$ Multiplier
By setting $\beta > 1$ (N.A.S.T. heavily tunes this parameter), we artificially constrict the information bottleneck. We mathematically force the neural network to align its learned features with the independent, orthogonal axes of the 12-D $Z$-space. 

**The Result:** The 12 $Z$-variables become **disentangled**. 
*   $Z_0$ might learn to control purely the tension of the upper aft reflex.
*   $Z_1$ might learn to control purely the "fatness" of the nose geometry behind the LE radius.

Because the variables are orthogonal, a Genetic Algorithm can easily tune them independently to achieve maximum $L/D$ ratios without accidentally triggering secondary geometric collapses.

---

### 4. Conditioning (The cVAE Component)
If N.A.S.T. were purely a $\beta$-VAE, it would be a fascinating toy, but useless for aerospace engineering, because you couldn't explicitly tell it to generate a "15% thick" wing.

N.A.S.T. is a **Conditional** $\beta$-VAE. 

During training and inference, the 20-dimensional physical $C$-Vector is concatenated directly into both the Encoder and the Decoder.
$$ \text{Input} = [Z_0, Z_1, ... Z_{11}, C_0, C_1, ... C_{19}] $$

Because the network *always* receives the absolute physical truth (the $C$-Vector) alongside the abstract style (the $Z$-Vector), the neural network learns to offload all macro-structural responsibility to the $C$-Vector. 

The $Z$-Vector stops trying to control thickness or camber, and instead dedicates $100\%$ of its massive computational capacity to learning the microscopic, fluid-dynamic "tension" and styling of the curves that bridge the physical $C$-nodes. 

This hybrid architecture gives N.A.S.T. the explicit control of a mathematical polynomial (CST), combined with the infinite, fluid-dynamic adaptability of a Deep Neural Network.