

***

# 📙 Section 6: Data Outputs & File Formats

The N.A.S.T. framework is designed to sit at the absolute center of a high-performance aerospace engineering pipeline. Because different departments (Aerodynamics, Data Science, and Manufacturing) use completely different software stacks, N.A.S.T. features a **Universal Translation Engine**. 

Whenever you synthesize, invert, or repanel an airfoil, you can append export flags to your command line to instantly generate the geometry in any (or all) of the formats listed below.

---

### 1. Selig Format (`--export_selig`)
**Command Flag:** `--export_selig`
**File Extension:** `.dat`

**The Engineering Standard for 2D CFD.**
The Selig format is the globally accepted standard for representing airfoil coordinates in 2D panel codes (specifically **XFOIL** and **MSES**). 

**Format Structure:**
1.  **Header:** The first line contains the name of the airfoil.
2.  **Wrap-Around Array:** The coordinates are listed in a continuous, wrapping loop. It begins at the Trailing Edge (Upper Surface), moves forward to the Leading Edge ($0,0$), wraps around the bottom, and travels back to the Trailing Edge (Lower Surface).
3.  **Coordinate Precision:** Formatted as two columns ($X$ and $Y$) separated by spaces, uniformly rounded to 6 decimal places ($10^{-6}$ precision).

*Example Snippet:*
```text
NAST_Synthesized_Wing
1.000000 0.001050  (Upper TE)
0.995000 0.002100
...
0.000000 0.000000  (Leading Edge)
...
0.995000 -0.001900
1.000000 -0.001050 (Lower TE)
```

---

### 2. Lednicer Format (`--export_lednicer`)
**Command Flag:** `--export_lednicer`
**File Extension:** `.dat`

**The Requirement for 3D Panel Codes.**
While XFOIL loves the Selig wrap-around format, many 3D aerodynamic solvers (like **VSPAero** and certain legacy NASA codes) will instantly crash if you feed them a continuous loop. They require the upper and lower surfaces to be mathematically severed at the leading edge.

**Format Structure:**
1.  **Header:** The first line contains the name of the airfoil.
2.  **Point Counters:** The second line explicitly states how many points are on the Upper surface and how many are on the Lower surface (e.g., `128. 128.`).
3.  **Split Arrays:** It lists the Upper coordinates from Leading Edge to Trailing Edge. Then, it leaves a blank line, and lists the Lower coordinates from Leading Edge to Trailing Edge.

*Example Snippet:*
```text
NAST_Synthesized_Wing
  128.  128.

0.000000 0.000000  (Upper LE)
0.005000 0.012000
...
1.000000 0.001050  (Upper TE)

0.000000 0.000000  (Lower LE)
0.005000 -0.011500
...
1.000000 -0.001050 (Lower TE)
```

---

### 3. Data Science Format (`--export_csv`)
**Command Flag:** `--export_csv`
**File Extension:** `.csv`

**The Standard for Machine Learning & Analytics.**
If you are trying to ingest airfoils into a Python `pandas` dataframe, a Jupyter Notebook, or a Microsoft Excel spreadsheet, raw `.dat` files are incredibly frustrating to parse because they lack headers and mix top/bottom data.

**Format Structure:**
1.  **Strict Headers:** The first line is exactly `X,Y,Surface`.
2.  **Comma Separation:** Cleanly delimited for instantaneous ingestion into `pd.read_csv()`.
3.  **Categorical Tagging:** Every single coordinate explicitly tags whether it belongs to the `Top` or `Bottom` surface, allowing data scientists to perform instantaneous filtering operations (`df[df['Surface'] == 'Top']`).

*Example Snippet:*
```text
X,Y,Surface
0.000000,0.000000,Top
0.005000,0.012000,Top
...
0.000000,0.000000,Bottom
0.005000,-0.011500,Bottom
```

---

### 4. CAD & Manufacturing Format (`--export_dxf`)
**Command Flag:** `--export_dxf`
**File Extension:** `.dxf` (Drawing Exchange Format)

**Direct-to-Manufacture Geometric Extraction.**
If you are an aerodynamicist working with a structural engineer, you need to provide them with CAD-ready files. If you give a mechanical engineer a `.dat` file, they have to manually write a macro to import it into SolidWorks. 

By using the `--export_dxf` flag, N.A.S.T. mathematically translates the airfoil into an **AutoCAD native LWPOLYLINE entity**. 

**Operation:**
You can literally drag and drop this `.dxf` file into **SolidWorks**, **CATIA**, **AutoCAD**, or a CNC Laser-Cutter software suite. It will instantly appear as a closed, continuous, perfectly scaled 2D sketch, ready to be extruded into a 3D wing or cut out of balsa wood.

---

### 5. The Neural DNA (`--export_json`)
**Command Flag:** `--export_json`
**File Extension:** `.json`

**The Core of the Optimization Pipeline.**
This is arguably the most important file format in the framework. If you use the `invert` command on a target airfoil, or the `generate` command to synthesize a new one, this JSON file acts as the absolute mathematical "save state" of the geometry.

**Format Structure:**
It is a highly structured dictionary containing:
1.  **`name`**: The string identifier.
2.  **`latent_vector_Z`**: The 12-dimensional array containing the exact Abstract Style nodes that the AI used to tension the curves.
3.  **`physics_vector_C`**: The 20-dimensional array containing the explicit structural constraints (Thickness, Crests, LE Radii, etc.) that you demanded.
4.  **`coordinates`**: Three arrays (`x`, `y_top`, `y_bot`) containing the exact finalized physical geometry.

**Why this is crucial:**
If you ever need to reproduce an airfoil, you do not need to save the thousands of $X/Y$ coordinates. You only need to save the 32 numbers in this JSON file. You can pass this JSON back into `nast_master_cli.py --mode generate` at any point in the future to summon the geometry back into existence.

---

### 6. Visual Inspection (`--export_plot`)
**Command Flag:** `--export_plot`
**File Extension:** `.png`

**The Executive Summary.**
Sometimes you just need to *look* at what the AI generated without opening a CFD solver or CAD program. 

**Format Structure:**
This generates a beautiful, high-resolution (200 DPI) image. It mathematically plots the upper and lower surfaces, fills the internal volume with a semi-transparent blue hue, and removes all distracting graph spines. It forces an **"equal aspect ratio"**, meaning the airfoil is drawn exactly as it would appear in the real world (preventing the optical illusion of extreme thickness caused by auto-scaling graphs).


---