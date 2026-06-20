<div align="center">

# 🦅 N.A.S.T.
### Neural Aerodynamic Shape Transformation

<img src="docs/images/nast_banner.png" alt="NAST Framework Banner" width="100%" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

<br>

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![ONNX](https://img.shields.io/badge/ONNX_Runtime-Enabled-orange?style=for-the-badge&logo=onnx&logoColor=white)](https://onnxruntime.ai/)
[![SciPy](https://img.shields.io/badge/Math-SciPy_Brentq-lightgrey?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org/)
[![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](LICENSE)

> **A high-fidelity, AI-driven parametric engine replacing traditional mathematical airfoil parameterizations (PARSEC, Hicks-Henne, CST) using a Disentangled $\beta$-cVAE Neural Manifold.**

</div>

---

## 📖 Table of Contents
- [🚨 The Crisis of Traditional Parameterization](#-the-crisis-of-traditional-parameterization)
- [💡 The N.A.S.T. Solution](#-the-nast-solution)
- [⚡ Quick Start: Hello World](#-quick-start-hello-world)
- [📂 Repository Architecture](#-repository-architecture)
- [📚 Deep Dive Documentation](#-deep-dive-documentation)
- [👨‍💻 About the Developers](#-about-the-developers)

---

## 🚨 The Crisis of Traditional Parameterization

Historically, aerodynamicists have used mathematical polynomials (like the Class Shape Transformation, or CST) to define airplane wings. However, polynomials are inherently flawed: **they are mathematically blind to fluid dynamics.** 

When optimization algorithms (Genetic Algorithms or Particle Swarm) manipulate these numbers to maximize Lift-to-Drag ($L/D$) ratios, they relentlessly exploit polynomial weaknesses. This results in **jagged leading edges, crossed boundary lines, and microscopically rippled surfaces.** When these "broken" geometries are passed to CFD solvers like **XFOIL** or **OpenFOAM**, the meshes crash, returning `NaN` and destroying the optimization loop.

---

## 💡 The N.A.S.T. Solution

**N.A.S.T. abandons polynomials entirely.** Powered by a **Physics-Informed Deep Neural Network** trained on a mathematically "healed" database of over 700,000 real-world aerodynamic topologies, the engine *only* knows how to generate viable, aerodynamically sound airplane wings.

Aerodynamicists gain explicit, deterministic control over the wing via **32 Parameters**:
*   🦴 **The Skeleton (20 $C$-Features):** Explicit, real-world physical constraints (e.g., Max Thickness, Leading Edge Radii, Upper/Lower Crests, Trailing Edge Gap).
*   🎨 **The Style (12 $Z$-Features):** Abstract, multi-dimensional "Latent" variables controlling curve tension and mass distribution between rigid structural constraints.

The result is a **$C^2$-continuous, mathematically flawless coordinate array** ready for high-performance CFD and immediate CNC manufacturing.

### 🔬 Visualizing the Engine Constraints

<div align="center">
  <img src="docs/images/macro_geometry.png" width="48%" alt="Macro-Structure">
  <img src="docs/images/aerodynamic_crests.png" width="48%" alt="Aerodynamic Crests">
</div>
<div align="center">
  <img src="docs/images/edges.png" width="48%" alt="Leading and Trailing Edges Constraints">
  <img src="docs/images/inflection.png" width="48%" alt="Inflection Limits">
</div>

### 📊 Model Validation Against Real-World Airfoils

<div align="center">
  <img src="docs/images/as6095_validation.png" width="48%" alt="AS6095 Validation">
  <img src="docs/images/ah79k143_validation.png" width="48%" alt="AH79K143 Validation">
</div>
<div align="center">
  <img src="docs/images/fx74modsmrev_validation.png" width="48%" alt="FX74MODSMREV Validation">
  <img src="docs/images/goe570_validation.png" width="48%" alt="GOE570 Validation">
</div>

---

## ⚡ Quick Start: Hello World

Get N.A.S.T. running locally and generate your first AI-driven airfoil in under 60 seconds.

### 1. Installation
Clone the repository and install the highly optimized scientific computing dependencies. *(Virtual environment recommended)*.
```bash
git clone https://github.com/Gamil-Al-Sharif/NAST_Project.git
cd NAST_Project
pip install -r requirements.txt
```

### 2. Generate Your First Airfoil
Use the Advanced Generator CLI to synthesize a completely novel airfoil. We will ask the AI for a **15% thick, 4% cambered** wing, mapped onto a **200-point Half-Cosine grid**, instantly exporting it to an XFOIL `.dat` format and a `.png` plot.

```bash
python NAST_Scr/nast_advanced_gen.py --name "Hello_NAST" --output_dir NAST_Output --t_max 0.15 --c_max 0.04 --points 200 --spacing half-cosine --export_selig --export_plot
```

---

## 📂 Repository Architecture

The N.A.S.T. framework is organized into a clean, modular hierarchy, isolating the core mathematical engine from documentation and data.

```text
📦 NAST_Project
 ┣ 📂 NAST_Scr/                       # Core AI & Mathematical Engine
 ┃ ┣ 📜 nast_advanced_gen.py        # Macro/Micro Synthesis Engine
 ┃ ┣ 📜 nast_master_cli.py          # Unified Inversion & Generation CLI
 ┃ ┣ 🧠 nast_decoder.onnx           # Compiled Neural Network Weights
 ┃ ┣ 🧠 nast_decoder.onnx.data      # Extended weight data
 ┃ ┣ 📐 nast_normalization.npz      # Mathematical normalization tensors
 ┃ ┗ 🧬 NAST_Global_DNA_Library.json# 32-D Math Dictionary of all airfoils
 ┣ 📂 Foil_Folder/                    # Reference Aerodynamic Data
 ┃ ┗ 📊 NACA0012.dat                # Sample target file for AI Inversion
 ┣ 📂 docs/                           # Comprehensive Documentation Library
 ┃ ┣ 📘 01_Introduction & Comprehensive Overview.md       
 ┃ ┣ 📗 02_Advanced_Gen_Examples.md 
 ┃ ┣ 📙 03_Master_CLI_Examples.md   
 ┃ ┣ 📙 04_Data_Outputs.md   
 ┃ ┗ 📕 05_Theory_and_Math.md 
 ┣ 🤖 test_cli_suite.py               # Automated QA Testing Suite
 ┗ ⚙️ requirements.txt                # Python Dependencies
```

> **🛡️ Automated System Verification:** 
> Run `python test_cli_suite.py` at any time to trigger the automated QA engineer. It executes 10 complex operations to guarantee parameter overrides, interpolation splines, and export formats function flawlessly on your hardware.

---

## 📚 Deep Dive Documentation

To truly master the N.A.S.T. framework, explore our comprehensive Markdown documentation located in the `docs/` folder. It contains over 40 copy-and-paste CLI examples and deep theoretical explanations.

| Document | Description |
| :--- | :--- |
| [📘 **20+ Examples for `nast_advanced_gen.py`**](docs/02_Advanced_Gen_Examples.md) | *Learn how to synthesize Supersonic Needle-Noses, Thick Heavy-Lifters, and explicitly control Z-Space Latent styling.* |
| [📗 **20+ Examples for `nast_master_cli.py`**](docs/03_Master_CLI_Examples.md) | *Learn how to use the L-BFGS-B optimizer to "Clone" real-world airfoils, extract their JSON DNA, and mathematically heal noisy wind-tunnel data.* |
| [📙 **Data Outputs & Formats Guide**](docs/04_Data_Outputs.md) | *A technical guide to exporting airfoils directly into XFOIL (.dat), Pandas Machine Learning Dataframes (.csv), and SolidWorks/AutoCAD (.dxf).* |
| [📕 **Math Format & $\beta$-VAE Theory**](docs/05_Theory_and_Math.md) | *The rigorous analytical calculus behind the 20-Feature Extractor, and the deep-learning mathematics of the Disentangled KL Divergence loss functions.* |

---

## 👨‍💻 About the Developers

<div align="center">
  <table style="border-collapse: collapse; border: none; width: 100%;">
    <tr>
      <td align="center" width="50%" style="border: none;">
        <h3>Gamil Abdullah Al-Sharif</h3>
        <b>Mechanical Engineer & R&D Specialist</b><br>
        <i>Sana'a, Yemen</i><br><br>
        ✉️ <a href="mailto:mely104haja@gmail.com">mely104haja@gmail.com</a><br>
        💼 <a href="https://linkedin.com/in/gamil-alsharif">LinkedIn Profile</a>
      </td>
      <td align="center" width="50%" style="border: none;">
        <h3>Yhya Abdullah Al-Wazir</h3>
        <b>Mechanical Engineer & R&D Specialist</b><br>
        <i>Sana'a, Yemen</i><br><br>
        ✉️ <a href="mailto:abdullahyhya141@gmail.com">abdullahyhya141@gmail.com</a><br>
        🔬 <a href="https://researchgate.net/profile/Yhya-Abdullah-Al-Waze">ResearchGate Profile</a>
      </td>
    </tr>
  </table>
</div>

<br>

<div align="center">
  <i>Built with passion for the advancement of computational fluid dynamics and aerospace optimization.</i>
</div>
