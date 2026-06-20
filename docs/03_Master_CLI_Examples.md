

***

# 📗 Section 5: The Master CLI (`nast_master_cli.py`)

The `nast_master_cli.py` script is the production-grade pipeline tool. While `nast_advanced_gen.py` is used to create *new* airfoils from scratch, the Master CLI is designed to operate on **existing data**. 

It has three primary operational modes:
1.  **`invert`**: Reads a `.dat` file, extracts its physical constraints, and uses an AI optimizer to "clone" the airfoil's style, returning the exact 32-D mathematical DNA.
2.  **`generate`**: Reads a `.json` DNA file and reconstructs the airfoil, perfectly converting the math back into physical coordinates.
3.  **`repanel`**: Bypasses the AI entirely. Uses pure B-Spline mathematics to clean up messy, jagged `.dat` files downloaded from the internet.

Below are 21 examples demonstrating how to master the CLI for reverse engineering and data sanitization.

---

### 🟢 Part 1: AI Inversion (Cloning Airfoils)
These commands demonstrate how to feed a raw `.dat` file to the Neural Network, forcing the AI to hunt through its Latent Space to find the exact DNA required to clone the shape.

**1. Basic AI Cloning**
Reads the classic NACA 0012, clones it using the AI, and outputs a high-resolution comparison plot to verify the clone's accuracy.
```bash
python NAST_Scr/nast_master_cli.py --mode invert --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --export_plot
```

**2. Extracting Neural DNA (JSON Export)**
Clones an airfoil and exports the 32-Dimensional DNA (The 20 $C$-Features and 12 $Z$-Features) to a `.json` file. This is crucial for building custom optimization datasets.
```bash
python NAST_Scr/nast_master_cli.py --mode invert --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --export_json
```

**3. Reverse Engineering to CAD (DXF Export)**
Takes a raw `.dat` file, smooths it through the Neural Manifold, and instantly exports it to a `.dxf` file so you can extrude a physical 3D wing in AutoCAD, SolidWorks, or Fusion360.
```bash
python NAST_Scr/nast_master_cli.py --mode invert --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --export_dxf
```

**4. High-Resolution CFD Cloning (300 points)**
Clones an airfoil and forces the AI's output to be perfectly distributed across 300 points. Useful when transferring a low-resolution wind-tunnel file into a high-resolution Navier-Stokes solver.
```bash
python NAST_Scr/nast_master_cli.py --mode invert --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --points 300 --export_selig
```

**5. Acoustic Distribution Cloning**
Clones the airfoil but redistributes the newly generated points using **Sine Spacing** (packing the points densely at the trailing edge) for acoustic wake simulations.
```bash
python NAST_Scr/nast_master_cli.py --mode invert --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --spacing sine --export_csv
```

---

### 🔵 Part 2: Generative Rebuilding (The JSON Pipeline)
Once you have extracted the `.json` DNA from an airfoil using the `invert` command, you can use the `generate` command to summon that airfoil back into physical reality at any time, on any grid density.

*(Note: These examples assume you ran Example #2 and have a `NACA0012.json` file in your `NAST_Output` folder).*

**6. Basic Rebuilding**
Reads the 32-variable DNA from the JSON file and mathematically generates the physical $X/Y$ coordinates.
```bash
python NAST_Scr/nast_master_cli.py --mode generate --vector NAST_Output/NACA0012.json --name "NACA_Reborn" --output_dir NAST_Output --export_plot
```

**7. Rebuilding for XFOIL (Half-Cosine)**
Reads the JSON DNA and forces the rebuilt airfoil onto a 160-point Half-Cosine grid, which guarantees high convergence rates in XFOIL.
```bash
python NAST_Scr/nast_master_cli.py --mode generate --vector NAST_Output/NACA0012.json --name "NACA_Xfoil" --output_dir NAST_Output --points 160 --spacing half-cosine --export_selig
```

**8. Rebuilding for Data Science (Linear CSV)**
Reads the JSON DNA and rebuilds the airfoil onto an evenly-spaced Linear grid, exporting it to CSV for easy ingestion into Pandas or Excel databases.
```bash
python NAST_Scr/nast_master_cli.py --mode generate --vector NAST_Output/NACA0012.json --name "NACA_Data" --output_dir NAST_Output --spacing linear --export_csv
```

**9. The Automated Pipeline Loop**
You can chain these commands in Python scripts. Invert an airfoil to get the JSON, modify the JSON slightly in Python (e.g., increase the `t_max` value inside the file), and then run the `generate` command to instantly render the modified wing!
```bash
python NAST_Scr/nast_master_cli.py --mode generate --vector NAST_Output/Modified_NACA.json --name "Mutated_Wing" --output_dir NAST_Output --export_dxf
```

---

### 🟡 Part 3: Mathematical Repaneling (Data Sanitization)
The `repanel` mode is arguably the most powerful data-cleaning tool in the suite. It completely bypasses the Neural Network and uses pure analytical B-Spline mathematics to "heal" jagged, noisy `.dat` files downloaded from the internet (e.g., the UIUC database).

**10. Basic Data Cleaning**
Takes a noisy `.dat` file, fits a parametric B-Spline through it, and re-exports it as a perfectly smooth, clean `.dat` file.
```bash
python NAST_Scr/nast_master_cli.py --mode repanel --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --export_selig
```

**11. Visualizing the Mathematical Fix**
Runs the repaneling algorithm and generates a plot, allowing you to visually verify that the new points perfectly trace the original geometry without any jagged artifacts.
```bash
python NAST_Scr/nast_master_cli.py --mode repanel --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --export_plot
```

**12. Heavy-Duty Grid Up-Sampling**
Takes a terrible 30-point `.dat` file from a 1940s wind-tunnel report and mathematically up-samples it into a flawless, continuous 250-point array.
```bash
python NAST_Scr/nast_master_cli.py --mode repanel --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --points 250 --export_selig
```

**13. Fixing the Leading Edge Singularity**
If your input `.dat` file has a jagged leading edge (causing XFOIL to crash), this command forces a `half-cosine` re-distribution, wrapping dozens of points elegantly around the nose to mathematically stabilize it.
```bash
python NAST_Scr/nast_master_cli.py --mode repanel --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --spacing half-cosine --export_selig
```

**14. Preparing Old Airfoils for 3D Printing**
Takes an old coordinate file, smooths it, evenly distributes the points using linear spacing, and exports it directly to DXF for laser cutting or 3D printing.
```bash
python NAST_Scr/nast_master_cli.py --mode repanel --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --spacing linear --export_dxf
```

---

### 🟠 Part 4: Advanced Cross-Format Exporting
The Master CLI acts as a universal Rosetta Stone, capable of instantly translating a single geometry into every major engineering format simultaneously.

**15. The Complete Data Dump**
Whether you are using `invert` or `repanel`, you can stack the export flags to generate every format at once.
```bash
python NAST_Scr/nast_master_cli.py --mode repanel --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --export_selig --export_lednicer --export_csv --export_dxf --export_plot
```

**16. Generating Lednicer Formats**
Some highly specialized 3D CFD panel codes (like VSPAero) refuse to read the standard wrap-around Selig `.dat` files. They require the "Lednicer" format (where the upper and lower surfaces are physically separated in the text file). N.A.S.T. handles this natively.
```bash
python NAST_Scr/nast_master_cli.py --mode repanel --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --export_lednicer
```

**17. Generating CSV for Machine Learning**
If you are building an ML database, raw `.dat` files are hard to parse. Use this to convert them to clean, column-header CSVs.
```bash
python NAST_Scr/nast_master_cli.py --mode repanel --input Foil_Folder/NACA0012.dat --output_dir NAST_Output --export_csv
```

---

### 🔴 Part 5: Error Handling & Edge Cases
The Master CLI is built for production environments. It is designed to catch bad user inputs safely without crashing the Python interpreter.

**18. Missing File Protection**
If you accidentally mistype a filename during an inversion, the CLI will catch the error and safely terminate, printing a warning rather than throwing a raw Python traceback.
```bash
python NAST_Scr/nast_master_cli.py --mode invert --input Foil_Folder/Does_Not_Exist.dat
```

**19. Missing Mode Protection**
If you forget to specify whether you want to `invert`, `repanel`, or `generate`, the argparse system will immediately reject the command and present the help menu.
```bash
python NAST_Scr/nast_master_cli.py --input Foil_Folder/NACA0012.dat
```

**20. Missing JSON Vector Protection**
If you attempt to use the `generate` mode without providing the `--vector` JSON file, the CLI will refuse to execute, preventing mathematically empty arrays from breaking the AI.
```bash
python NAST_Scr/nast_master_cli.py --mode generate --name "Blank_Wing" --export_selig
```

**21. Missing Export Flags**
If you successfully run a complex AI inversion but forget to tell the script what formats to save, it will still execute the math but safely warn you that no files were written to the hard drive.
```bash
python NAST_Scr/nast_master_cli.py --mode invert --input Foil_Folder/NACA0012.dat --output_dir NAST_Output
```


---
