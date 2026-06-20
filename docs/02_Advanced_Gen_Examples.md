

***

# 📘 Section 4: Advanced Synthesis (`nast_advanced_gen.py`)

The `nast_advanced_gen.py` script is the core generative engine of the N.A.S.T. framework. It allows aerodynamicists to explicitly dictate the physical boundaries of an airfoil via the command line, while relying on the Neural Engine to intelligently bridge those boundaries with optimal fluid-dynamic styling.

Below are 24 examples demonstrating the vast capabilities of the engine, ranging from basic symmetric generation to extreme, high-resolution asymmetrical synthesis.

---

### 🟢 Part 1: Basic Aerodynamic Generation
These commands demonstrate how to control the fundamental macro-geometry of the wing. If you do not specify a parameter, the engine automatically defaults to the mathematical "Universal Average" derived from the 700,000+ airfoil training set.

**1. The Universal Default Airfoil**
Generates the baseline neural shape (roughly 12% thick, 2% camber).
```bash
python NAST_Scr/nast_advanced_gen.py --name "Basic_Default" --output_dir NAST_Output --export_plot --export_selig
```

**2. Standard Symmetric (NACA 0012 Style)**
Forces the airfoil to be exactly 12% thick with zero camber.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Symmetric_12" --output_dir NAST_Output --t_max 0.12 --c_max 0.0 --export_plot --export_selig
```

**3. Thick Heavy-Lifter (Cargo / UAV)**
Pushes the thickness to 20% and adds significant camber to generate massive lift at low speeds.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Thick_Cargo" --output_dir NAST_Output --t_max 0.20 --c_max 0.05 --export_plot --export_selig
```

**4. Thin Supersonic Interceptor**
Generates a razor-thin 5% airfoil. The Smart Sieve will automatically scale down the leading-edge radius to prevent mathematical ballooning.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Thin_Supersonic" --output_dir NAST_Output --t_max 0.05 --c_max 0.0 --export_plot --export_selig
```

**5. Aft-Loaded Laminar Flow (P-51 Mustang Style)**
Shifts the maximum thickness far back (to 50% chord) to encourage a favorable pressure gradient and extend laminar flow.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Aft_Loaded" --output_dir NAST_Output --t_max 0.14 --x_tmax 0.50 --c_max 0.02 --export_plot
```

---

### 🔵 Part 2: Grid Density & Distribution Control
CFD solvers and meshing software require highly specific coordinate distributions. N.A.S.T. uses a purely analytical `CubicSpline + Scipy Brentq` engine to perfectly resample the AI's output without compromising $C^2$ continuity.

**6. High-Density CFD Mesh (300 points)**
Generates an ultra-dense array required for high-Reynolds Navier-Stokes solvers like OpenFOAM.
```bash
python NAST_Scr/nast_advanced_gen.py --name "High_Density" --output_dir NAST_Output --points 300 --export_csv
```

**7. Half-Cosine Spacing (XFOIL Standard)**
Packs points extremely densely at the Leading Edge to resolve the suction peak, while spreading them out over the Trailing Edge. Highly recommended for 2D panel codes.
```bash
python NAST_Scr/nast_advanced_gen.py --name "XFOIL_Ready" --output_dir NAST_Output --spacing half-cosine --export_selig
```

**8. Sine Spacing (Acoustic / Wake Meshing)**
Packs points densely at the *Trailing Edge* instead of the Leading Edge. Useful for resolving trailing edge vortex shedding and acoustic noise simulations.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Acoustic_TE" --output_dir NAST_Output --spacing sine --export_csv
```

**9. Pure Linear Spacing (Structural Slicing)**
Distributes points evenly across the X-axis. Useful if you are exporting cross-sections to slice into physical ribs for a laser cutter.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Linear_Ribs" --output_dir NAST_Output --spacing linear --export_dxf
```

---

### 🟡 Part 3: Leading & Trailing Edge Micro-Management
Control the absolute geometric limits of the airfoil to ensure manufacturability and specific stall characteristics.

**10. Razor-Sharp Trailing Edge (Theoretical CFD)**
Forces the Trailing Edge gap to be exactly $0.0000$. Ideal for inviscid 2D CFD analysis to perfectly satisfy the Kutta condition.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Sharp_TE" --output_dir NAST_Output --te_gap 0.0 --export_plot
```

**11. Blunt Trailing Edge (CNC / Foam Manufacturability)**
Forces a $1\%$ (0.01) gap at the trailing edge so a CNC router bit doesn't snap the trailing edge off during manufacturing.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Blunt_TE" --output_dir NAST_Output --te_gap 0.01 --export_plot
```

**12. Massive Leading Edge Radius (Soft Stall)**
Forces a massive leading-edge radius to prevent abrupt boundary-layer separation at high angles of attack.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Fat_Nose" --output_dir NAST_Output --r_le_up 0.15 --r_le_lo 0.15 --export_plot
```

**13. Needle Nose (Supersonic Shock Delay)**
Forces a microscopic radius and a shallow wedge angle to easily pierce the sound barrier.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Needle_Nose" --output_dir NAST_Output --r_le_up 0.005 --r_le_lo 0.005 --theta_le_up 15.0 --theta_le_lo 15.0 --export_plot
```

**14. Reflexed Trailing Edge (Tailless Flying Wing)**
Pushes the trailing edge exit angles upwards, and shifts the inflection points to the aft, creating a natural pitch-up moment for stability without a tail.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Reflex_Wing" --output_dir NAST_Output --c_max 0.03 --theta_te_up 15.0 --theta_te_lo 10.0 --x_infl_up 0.85 --export_plot
```

---

### 🟠 Part 4: The Abstract Z-Space (Styling & Tension)
While the $C$-features define the rigid structural box, the 12-Dimensional $Z$-Vector controls the internal volume and "style" of the curve. Sweeping these variables (from $-3.0$ to $+3.0$) dramatically alters the aerodynamics without breaking the physical thickness constraints.

**15. Z-Vector Injection (The "Plump" Wing)**
By pushing specific Z-variables high, the Neural Network increases the internal volume (the "meat") of the airfoil without making it technically thicker.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Z_Plump" --output_dir NAST_Output --z_vector "2.0,1.5,0.0,0.5,1.1,-1.1,0.0,0.0,0.0,0.0,2.0,2.0" --export_plot
```

**16. Z-Vector Injection (The "Pinched" Wing)**
By driving Z-variables into the negative, the Neural Network pulls the curves tightly against the centerline, creating a "hollow" or pinched aerodynamic style.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Z_Pinched" --output_dir NAST_Output --z_vector "-2.0,-2.5,-1.0,-0.5,-1.1,1.1,0.0,0.0,0.0,0.0,-2.0,-2.0" --export_plot
```

---

### 🔴 Part 5: The Master Overrides (Extreme Constraints)
These examples demonstrate pushing the `nast_advanced_gen.py` script to its absolute limits by explicitly providing almost every single variable to create highly unorthodox, yet mathematically stable, geometries.

**17. The Flat-Bottomed Trainer**
Forces the lower crest to remain completely flat, making the wing easy to build on a flat workbench (similar to a Clark Y).
```bash
python NAST_Scr/nast_advanced_gen.py --name "Flat_Bottom" --output_dir NAST_Output --t_max 0.12 --c_max 0.06 --y_lo_crest 0.0 --k_lo_crest 0.0 --export_plot
```

**18. The Deep Under-Camber (Slow-Flyer / Turbine)**
Forces the lower surface to curve aggressively inwards, trapping high pressure for massive lift at slow speeds.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Under_Camber" --output_dir NAST_Output --t_max 0.08 --c_max 0.08 --y_lo_crest 0.04 --export_plot
```



---

### 🟣 Part 6: Multi-Export & Pipeline Integration
Generate an airfoil and instantly format it for every department in your engineering pipeline.

**19. The "All-In-One" Engineering Export**
Generates a standard 12% wing and saves it as Selig DAT (for XFOIL), CSV (for Excel/Pandas), DXF (for SolidWorks/AutoCAD), JSON (for Python/Web-Apps), and PNG (for visual inspection).
```bash
python NAST_Scr/nast_advanced_gen.py --name "Pipeline_Wing" --output_dir NAST_Output --t_max 0.12 --export_selig --export_csv --export_dxf --export_json --export_plot
```

**20. Extracting the DNA (JSON Export)**
Generates an airfoil and exports *only* the JSON file. The JSON contains the explicit 32-D mathematical vector required to summon this exact shape later.
```bash
python NAST_Scr/nast_advanced_gen.py --name "DNA_Only" --output_dir NAST_Output --t_max 0.18 --export_json
```

**21. Lednicer Format (Specific CFD Codes)**
Exports the geometry in the classic "Lednicer" format (where the upper and lower surfaces are split into two distinct arrays), which is required by certain legacy 3D panel codes (e.g., VSPAero).
```bash
python NAST_Scr/nast_advanced_gen.py --name "Legacy_CFD" --output_dir NAST_Output --t_max 0.15 --spacing half-cosine --export_lednicer
```


### 🧬 Part 7: Global DNA Library Mutations (The `--base_dna` command)
Instead of building an airfoil from the universal average, you can load the exact 32-D mathematical DNA of a classic airfoil directly from the `NAST_Global_DNA_Library.json`, and then inject modifications to instantly mutate it!

**22. Summoning a Classic Airfoil**
Pulls the mathematical DNA of the Eppler 423 from the library and instantly generates it on a high-resolution CFD grid.
```bash
python NAST_Scr/nast_advanced_gen.py --name "Eppler_Clone" --output_dir NAST_Output --base_dna "e423" --points 200 --export_plot
```

**23. Mutating a Classic Airfoil (Thickening)**
Pulls the Eppler 423 DNA, but intercepts the 32-D array and physically forces the maximum thickness to 18%, while perfectly scaling the leading edge radius to prevent ballooning!
```bash
python NAST_Scr/nast_advanced_gen.py --name "Eppler_Fat" --output_dir NAST_Output --base_dna "e423" --t_max 0.18 --export_plot
```

**24. Mutating a Classic Airfoil (Aero-Tuning)**
Pulls a NACA 4412, and mutates its performance by shifting the maximum camber rearward to $50\%$ chord (`--x_cmax 0.50`) and tightening the trailing edge gap to exactly zero.
```bash
python NAST_Scr/nast_advanced_gen.py --name "NACA4412_Mutant" --output_dir NAST_Output --base_dna "naca4412" --x_cmax 0.50 --te_gap 0.0 --export_plot
```


---