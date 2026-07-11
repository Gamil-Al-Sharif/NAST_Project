<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>N.A.S.T. — README</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,600;14..32,700;14..32,800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet" />

    <!-- Font Awesome 6 (Free) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />

    <style>
        /* ── Reset & Variables ── */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0b1120;
            --bg-secondary: #1e293b;
            --bg-card: #162032;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-purple: #a78bfa;
            --accent-blue: #60a5fa;
            --accent-green: #34d399;
            --accent-yellow: #fbbf24;
            --border-color: #334155;
            --radius: 12px;
            --shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
            --transition: 0.25s ease;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.7;
            padding: 30px 20px;
        }

        a {
            color: var(--accent-blue);
            text-decoration: none;
            transition: color var(--transition);
        }
        a:hover {
            color: var(--accent-purple);
            text-decoration: underline;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            background: var(--bg-secondary);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 40px 48px;
            border: 1px solid var(--border-color);
        }

        /* ── Typography ── */
        h1,
        h2,
        h3,
        h4 {
            font-weight: 700;
            line-height: 1.25;
        }

        h1 {
            font-size: 3.2rem;
            color: var(--accent-purple);
            letter-spacing: -0.02em;
        }
        h1 i {
            color: var(--accent-blue);
            margin-right: 8px;
        }

        h2 {
            font-size: 2rem;
            color: var(--accent-purple);
            margin-top: 48px;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        h2 i {
            color: var(--accent-blue);
            font-size: 1.6rem;
        }

        h3 {
            font-size: 1.3rem;
            color: var(--accent-blue);
            margin-top: 28px;
            margin-bottom: 12px;
        }

        p {
            margin-bottom: 16px;
            color: var(--text-secondary);
        }
        strong {
            color: var(--text-primary);
        }

        /* ── Hero ── */
        .hero {
            text-align: center;
            margin-bottom: 32px;
        }
        .hero .subtitle {
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 20px;
        }
        .hero .banner {
            width: 100%;
            max-height: 260px;
            object-fit: cover;
            border-radius: var(--radius);
            border: 1px solid var(--border-color);
            background: var(--bg-primary);
            box-shadow: var(--shadow);
            margin-bottom: 20px;
        }

        .badges {
            display: flex;
            justify-content: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .badges a {
            display: inline-block;
            transition: transform 0.2s ease;
        }
        .badges a:hover {
            transform: translateY(-2px);
            text-decoration: none;
        }
        .badges img {
            height: 32px;
            border-radius: 6px;
        }

        /* ── ASCII Art ── */
        .ascii-art {
            background: var(--bg-primary);
            color: #4ec9b0;
            padding: 16px 18px;
            border-radius: var(--radius);
            font-family: 'Fira Code', monospace;
            font-size: 0.72rem;
            line-height: 1.3;
            text-align: center;
            overflow-x: auto;
            white-space: pre;
            border: 1px solid var(--border-color);
            margin-bottom: 32px;
        }
        .ascii-art .white {
            color: #d4d4d4;
        }
        .ascii-art .dim {
            color: #6a9955;
        }

        /* ── Grids & Cards ── */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }

        .card {
            background: var(--bg-card);
            padding: 22px 24px;
            border-radius: var(--radius);
            border-left: 4px solid var(--accent-blue);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            transition: transform var(--transition), box-shadow var(--transition);
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        .card h4 {
            font-size: 1.05rem;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card p {
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-bottom: 0;
        }

        .card-warning {
            border-left-color: var(--accent-yellow);
        }
        .card-warning h4 {
            color: var(--accent-yellow);
        }
        .card-danger {
            border-left-color: #f87171;
        }
        .card-danger h4 {
            color: #f87171;
        }
        .card-success {
            border-left-color: var(--accent-green);
        }
        .card-success h4 {
            color: var(--accent-green);
        }
        .card-purple {
            border-left-color: var(--accent-purple);
        }
        .card-purple h4 {
            color: var(--accent-purple);
        }

        .card-highlight {
            background: var(--bg-card);
            border: 1px solid var(--accent-green);
            border-radius: var(--radius);
            padding: 18px 24px;
            margin-bottom: 20px;
            color: var(--text-secondary);
        }
        .card-highlight i {
            color: var(--accent-green);
            margin-right: 8px;
        }

        /* ── Code ── */
        pre {
            background: var(--bg-primary);
            color: #d4d4d4;
            padding: 18px 22px;
            border-radius: var(--radius);
            font-family: 'Fira Code', monospace;
            font-size: 0.88rem;
            line-height: 1.6;
            overflow-x: auto;
            border: 1px solid var(--border-color);
            margin-bottom: 20px;
        }
        pre code {
            background: transparent;
            color: inherit;
            padding: 0;
        }
        code {
            font-family: 'Fira Code', monospace;
            background: var(--bg-primary);
            color: #f472b6;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.9em;
        }
        pre code .folder {
            color: #9cdcfe;
            font-weight: 600;
        }
        pre code .file {
            color: #ce9178;
        }
        pre code .file-exe {
            color: #4ec9b0;
            font-weight: 600;
        }
        pre code .file-json {
            color: #dcdcaa;
        }
        pre code .comment {
            color: #6a9955;
            font-style: italic;
        }

        /* ── Doc list ── */
        .doc-list {
            list-style: none;
        }
        .doc-list li {
            background: var(--bg-card);
            margin-bottom: 12px;
            padding: 16px 20px;
            border-radius: var(--radius);
            border: 1px solid var(--border-color);
            display: flex;
            align-items: flex-start;
            gap: 16px;
            transition: background var(--transition), border-color var(--transition);
        }
        .doc-list li:hover {
            background: var(--bg-secondary);
            border-color: var(--accent-purple);
        }
        .doc-list li i {
            font-size: 1.4rem;
            flex-shrink: 0;
            margin-top: 2px;
            width: 28px;
            text-align: center;
        }
        .doc-list li .doc-content {
            flex: 1;
        }
        .doc-list li .doc-content strong {
            display: block;
            color: var(--text-primary);
            font-size: 1rem;
        }
        .doc-list li .doc-content .doc-desc {
            color: var(--text-secondary);
            font-size: 0.92rem;
        }
        .doc-list li .doc-content .doc-link {
            font-weight: 600;
            font-size: 0.88rem;
            display: inline-block;
            margin-top: 4px;
        }
        .doc-list li .doc-content .doc-link i {
            font-size: 0.75rem;
            width: auto;
            margin-left: 4px;
        }

        /* ── Developer Cards ── */
        .dev-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-top: 16px;
        }
        .dev-card {
            background: var(--bg-card);
            padding: 24px 28px;
            border-radius: var(--radius);
            border: 1px solid var(--border-color);
            transition: all var(--transition);
        }
        .dev-card:hover {
            border-color: var(--accent-purple);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            transform: translateY(-3px);
        }
        .dev-card h3 {
            margin-top: 0;
            color: var(--text-primary);
            font-size: 1.15rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .dev-card h3 i {
            color: var(--accent-purple);
        }
        .dev-card .title {
            color: var(--text-muted);
            font-style: italic;
            font-size: 0.95rem;
            margin-bottom: 12px;
        }
        .dev-contact {
            margin-bottom: 4px;
            font-size: 0.92rem;
        }
        .dev-contact i {
            width: 20px;
            color: var(--text-muted);
            text-align: center;
        }

        /* ── Table of Contents ── */
        .toc {
            background: var(--bg-card);
            padding: 16px 22px;
            border-radius: var(--radius);
            border: 1px solid var(--border-color);
            margin-bottom: 32px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px 28px;
        }
        .toc a {
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.95rem;
            transition: color var(--transition);
        }
        .toc a:hover {
            color: var(--accent-purple);
            text-decoration: none;
        }
        .toc i {
            margin-right: 6px;
            color: var(--accent-blue);
        }

        /* ── Footer ── */
        footer {
            text-align: center;
            margin-top: 48px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 0.92rem;
        }
        footer .footer-links {
            display: flex;
            justify-content: center;
            gap: 24px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }
        footer .footer-links a {
            color: var(--text-muted);
        }
        footer .footer-links a:hover {
            color: var(--accent-purple);
            text-decoration: none;
        }
        footer .star-link {
            font-weight: 600;
            color: var(--accent-yellow);
        }

        /* ── Responsive ── */
        @media (max-width: 820px) {
            .container {
                padding: 24px 18px;
            }
            .grid-2,
            .dev-grid {
                grid-template-columns: 1fr;
            }
            h1 {
                font-size: 2.4rem;
            }
            .hero .banner {
                max-height: 180px;
            }
            .ascii-art {
                font-size: 0.58rem;
                padding: 12px 10px;
            }
            .doc-list li {
                flex-direction: column;
                gap: 6px;
            }
        }

        @media (max-width: 480px) {
            h1 {
                font-size: 1.8rem;
            }
            .badges img {
                height: 26px;
            }
            pre {
                font-size: 0.75rem;
                padding: 14px 16px;
            }
        }
    </style>
</head>
<body>
    <div class="container">

        <!-- ════════════════════════════════════════════ -->
        <!-- HERO                                        -->
        <!-- ════════════════════════════════════════════ -->
        <header class="hero">
            <h1><i class="fa-solid fa-network-wired"></i> N.A.S.T.</h1>
            <p class="subtitle">Neural Aerodynamic Shape Transformation Framework</p>

            <img src="docs/images/nast_banner.png"
            alt="NAST Framework Banner"
            class="banner"
            onerror="this.src='https://via.placeholder.com/1100x260/0b1120/a78bfa?text=N.A.S.T.+—+Neural+Aerodynamic+Shape+Transformation'"
            />

            <div class="badges">
                <a href="https://www.python.org/" target="_blank">
                    <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
                </a>
                <a href="https://pytorch.org/" target="_blank">
                    <img src="https://img.shields.io/badge/PyTorch-Deep_Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" />
                </a>
                <a href="https://onnxruntime.ai/" target="_blank">
                    <img src="https://img.shields.io/badge/ONNX_Runtime-Enabled-005CED?style=for-the-badge&logo=onnx&logoColor=white" alt="ONNX" />
                </a>
                <a href="https://scipy.org/" target="_blank">
                    <img src="https://img.shields.io/badge/Math-SciPy_Brentq-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white" alt="SciPy" />
                </a>
                <a href="https://github.com/Gamil-Al-Sharif/NAST_Project/blob/main/LICENSE" target="_blank">
                    <img src="https://img.shields.io/badge/License-MIT-success?style=for-the-badge" alt="MIT License" />
                </a>
                <a href="https://github.com/Gamil-Al-Sharif/NAST_Project" target="_blank">
                    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
                </a>
            </div>
        </header>

        <!-- ════════════════════════════════════════════ -->
        <!-- ASCII ART                                   -->
        <!-- ════════════════════════════════════════════ -->
        <div class="ascii-art">
            ════════════════════════════════════════════════════════════════════
               ███╗   ██╗    █████╗    ███████╗   ████████╗
               ████╗  ██║   ██╔══██╗   ██╔════╝   ╚══██╔══╝
            ██╔██╗ ██║   ███████║   ███████╗      ██║
            ██║╚██╗██║   ██╔══██║   ╚════██║      ██║
            ██║ ╚████║   ██║  ██║   ███████║      ██║
            ╚═╝  ╚═══╝   ╚═╝  ╚═╝   ╚══════╝      ╚═╝
            ════════════════════════════════════════════════════════════════════
            <span class="white">Neural Aerodynamic Shape Transformation &bull; Latent Space Z-Routing</span>
            <span class="white">Disentangled β-cVAE Engine &bull; Sobolev Physics-Informed Math</span>
            <span class="dim">Developers: Gamil Abdullah Al-Sharif &amp; Yhya Abdullah Al-Wazir</span>
            <span class="dim">Contact: <a href="mailto:mely104haja@gmail.com" style="color:#4ec9b0;">mely104haja@gmail.com</a></span>
            ════════════════════════════════════════════════════════════════════
        </div>

        <!-- ════════════════════════════════════════════ -->
        <!-- TABLE OF CONTENTS                           -->
        <!-- ════════════════════════════════════════════ -->
        <div class="toc">
            <a href="#crisis"><i class="fa-solid fa-triangle-exclamation"></i> Crisis</a>
            <a href="#solution"><i class="fa-solid fa-brain"></i> Solution</a>
            <a href="#architecture"><i class="fa-solid fa-folder-tree"></i> Architecture</a>
            <a href="#quickstart"><i class="fa-solid fa-rocket"></i> Quick Start</a>
            <a href="#docs"><i class="fa-solid fa-book"></i> Documentation</a>
            <a href="#developers"><i class="fa-solid fa-user-astronaut"></i> Developers</a>
        </div>

        <!-- ════════════════════════════════════════════ -->
        <!-- 1. CRISIS                                   -->
        <!-- ════════════════════════════════════════════ -->
        <section id="crisis">
            <h2><i class="fa-solid fa-triangle-exclamation"></i> 1. The Crisis of Traditional Parameterization</h2>
            <p>
                Historically, aerodynamicists have relied on mathematical polynomials like
                <strong>PARSEC</strong>, <strong>Hicks–Henne</strong>, or
                <strong>Class Shape Transformation (CST)</strong> to define airfoils.
                Yet polynomials are <strong>mathematically blind to fluid dynamics</strong>.
            </p>

            <div class="grid-2">
                <div class="card card-warning">
                    <h4><i class="fa-solid fa-chart-area"></i> The Exploitation of Polynomials</h4>
                    <p>
                        When optimisation algorithms manipulate polynomial variables to maximise
                        Lift-to-Drag (<em>L/D</em>) ratios, they relentlessly exploit mathematical
                        blind spots. The result: <strong>jagged leading edges, crossed boundary
                        lines, and microscopically rippled surfaces</strong> — shapes polynomials
                        allow, but physics forbid.
                    </p>
                </div>
                <div class="card card-danger">
                    <h4><i class="fa-solid fa-bomb"></i> The CFD Crash Cascade</h4>
                    <p>
                        These &ldquo;broken&rdquo; geometries are passed to strict CFD solvers
                        like <strong>XFOIL</strong> or <strong>OpenFOAM</strong>. Meshing
                        algorithms catastrophically fail, returning <code>NaN</code> matrices
                        and destroying the entire optimisation loop.
                    </p>
                </div>
            </div>
        </section>

        <!-- ════════════════════════════════════════════ -->
        <!-- 2. SOLUTION                                 -->
        <!-- ════════════════════════════════════════════ -->
        <section id="solution">
            <h2><i class="fa-solid fa-brain"></i> 2. The N.A.S.T. Solution</h2>
            <p>
                <strong>N.A.S.T. abandons polynomials entirely.</strong><br />
                Powered by a <strong>Physics-Informed Deep Neural Network</strong> trained on
                a mathematically &ldquo;healed&rdquo; database of over 700,000 real-world
                aerodynamic topologies, the engine <em>only</em> knows how to generate viable,
                aerodynamically sound airfoils.
            </p>
            <p>
                Aerodynamicists gain explicit, deterministic control over the wing via a
                revolutionary <strong>32‑Dimensional Parameterisation Matrix</strong>:
            </p>

            <div class="grid-2">
                <div class="card card-purple">
                    <h4><i class="fa-solid fa-bone"></i> The Skeleton (20 C‑Features)</h4>
                    <p>
                        Explicit, real‑world physical constraints mapped to direct aeronautical
                        requirements: Max Thickness, Leading‑Edge Radii, Upper/Lower Crest
                        Locations, Trailing‑Edge Gaps, and Camber profiles.
                    </p>
                </div>
                <div class="card card-purple">
                    <h4><i class="fa-solid fa-palette"></i> The Style (12 Z‑Features)</h4>
                    <p>
                        Abstract, multi‑dimensional &ldquo;Latent&rdquo; variables governing
                        the internal Neural Manifold. They control curve tension, mass
                        distribution, and subtle aerodynamic styling <em>between</em> the
                        rigid structural constraints of the Skeleton.
                    </p>
                </div>
            </div>

            <div class="card-highlight">
                <i class="fa-solid fa-check-double"></i>
                <strong>The Ultimate Output:</strong> A mathematically flawless,
                C²‑continuous coordinate array, generated in milliseconds and strictly
                prepared for high‑performance CFD mesh generation and CNC manufacturing.
            </div>
        </section>

        <!-- ════════════════════════════════════════════ -->
        <!-- 3. ARCHITECTURE                             -->
        <!-- ════════════════════════════════════════════ -->
        <section id="architecture">
            <h2><i class="fa-solid fa-folder-tree"></i> 3. Repository Architecture</h2>
            <p>
                The N.A.S.T. framework is organised into a clean, modular hierarchy,
                strictly isolating the core mathematical inference engine from the
                documentation and global datasets.
            </p>

            <pre><code><span class="folder">NAST_Project/</span>
            │
            ├── <span class="folder">NAST_Scr/</span>                       <span class="comment"># Core AI &amp; Mathematical Engine</span>
            │   ├── <span class="file">nast_advanced_gen.py</span>        <span class="comment"># Macro/Micro Synthesis Engine CLI</span>
            │   ├── <span class="file">nast_master_cli.py</span>          <span class="comment"># Unified Inversion &amp; Generation Router</span>
            │   ├── <span class="file">train_nast_infinite.py</span>      <span class="comment"># Automated AI Training Pipeline</span>
            │   ├── <span class="file-exe">nast_decoder.onnx</span>           <span class="comment"># Compiled Neural Network Brain</span>
            │   ├── <span class="file-exe">nast_decoder.onnx.data</span>      <span class="comment"># Extended ONNX weight tensors</span>
            │   ├── <span class="file-json">nast_normalization.npz</span>      <span class="comment"># Mathematical normalisation matrices</span>
            │   └── <span class="file-json">NAST_Global_DNA_Library.json</span> <span class="comment"># 32‑D Math Dictionary of 700k airfoils</span>
            │
            ├── <span class="folder">Foil_Folder/</span>                    <span class="comment"># Reference Aerodynamic Data</span>
            │   └── <span class="file">NACA0012.dat</span>                <span class="comment"># Sample target file for AI Inversion</span>
            │
            ├── <span class="folder">docs/</span>                           <span class="comment"># Comprehensive Documentation Library</span>
            │   ├── <span class="file">01_Introduction.md</span>          <span class="comment"># Framework Overview &amp; Paradigm shift</span>
            │   ├── <span class="file">02_Advanced_Gen_Examples.md</span> <span class="comment"># Parametric Manipulation CLI guides</span>
            │   ├── <span class="file">03_Master_CLI_Examples.md</span>   <span class="comment"># L‑BFGS‑B Inversion algorithms</span>
            │   ├── <span class="file">04_Data_Outputs.md</span>          <span class="comment"># XFOIL .dat, CAD .dxf, and CSV exporting</span>
            │   └── <span class="file">05_Theory_and_Math.md</span>       <span class="comment"># The Calculus behind the β‑VAE</span>
            │
            ├── <span class="file">test_cli_suite.py</span>               <span class="comment"># Automated QA Testing Suite</span>
            └── <span class="file-json">requirements.txt</span>                <span class="comment"># Python Dependency Blueprint</span></code></pre>

            <div class="card-highlight">
                <i class="fa-solid fa-shield-check"></i>
                <strong>Automated System Verification:</strong> Run
                <code>python test_cli_suite.py</code> at any time to trigger the automated
                QA engineer. It executes 10 complex operations to guarantee parameter
                overrides, interpolation splines, and export formats function flawlessly
                on your local hardware.
            </div>
        </section>

        <!-- ════════════════════════════════════════════ -->
        <!-- 4. QUICK START                              -->
        <!-- ════════════════════════════════════════════ -->
        <section id="quickstart">
            <h2><i class="fa-solid fa-rocket"></i> 4. Quick Start: Hello World</h2>
            <p>
                Get N.A.S.T. running locally and generate your first AI‑driven airfoil in
                under 60 seconds.
            </p>

            <h3><i class="fa-solid fa-download"></i> Step 1: Installation</h3>
            <p>
                Clone the repository and install the highly optimised scientific computing
                dependencies. <em>(Using a virtual environment is highly recommended.)</em>
            </p>
            <pre><code>git clone https://github.com/Gamil-Al-Sharif/NAST_Project.git
                cd NAST_Project
                pip install -r requirements.txt</code></pre>

            <h3><i class="fa-solid fa-terminal"></i> Step 2: Synthesise Your First Airfoil</h3>
            <p>
                Use the Advanced Generator CLI to synthesise a completely novel airfoil.
                In this command, we instruct the AI to generate a <strong>15% thick,
                4% cambered</strong> wing, mapped onto a <strong>200‑point Half‑Cosine
                grid</strong>, instantly exporting it to an XFOIL <code>.dat</code> format
                and a <code>.png</code> plot.
            </p>
            <!-- Single-line command as requested -->
            <pre><code>python NAST_Scr/nast_advanced_gen.py --name "Hello_NAST" --output_dir NAST_Output --t_max 0.15 --c_max 0.04 --points 200 --spacing half-cosine --export_selig --export_plot</code></pre>
        </section>

        <!-- ════════════════════════════════════════════ -->
        <!-- 5. DOCUMENTATION                            -->
        <!-- ════════════════════════════════════════════ -->
        <section id="docs">
            <h2><i class="fa-solid fa-book"></i> 5. Deep Dive Documentation</h2>
            <p>
                To truly master the N.A.S.T. framework, explore our comprehensive Markdown
                documentation located in the <code>docs/</code> folder. It contains over
                40 copy‑and‑paste CLI examples and deep theoretical explanations.
            </p>

            <ul class="doc-list">
                <!-- 02_Advanced_Gen_Examples -->
                <li>
                    <i class="fa-solid fa-code" style="color: #60a5fa;"></i>
                    <div class="doc-content">
                        <strong>20+ Examples for <code>nast_advanced_gen.py</code></strong>
                        <div class="doc-desc">
                            Learn how to synthesise Supersonic Needle‑Noses, Thick Heavy‑Lifters,
                            and explicitly control Z‑Space Latent styling.
                        </div>
                        <a href="https://github.com/Gamil-Al-Sharif/NAST_Project/blob/main/docs/02_Advanced_Gen_Examples.md"
                        target="_blank"
                        class="doc-link">
                        <i class="fa-regular fa-file-lines"></i> View on GitHub
                        <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                </div>
            </li>

            <!-- 03_Master_CLI_Examples -->
            <li>
                <i class="fa-solid fa-copy" style="color: #34d399;"></i>
                <div class="doc-content">
                    <strong>20+ Examples for <code>nast_master_cli.py</code></strong>
                    <div class="doc-desc">
                        Learn how to use the L‑BFGS‑B optimizer to &ldquo;Clone&rdquo;
                        real‑world airfoils, extract their JSON DNA, and mathematically
                        heal noisy wind‑tunnel data.
                    </div>
                    <a href="https://github.com/Gamil-Al-Sharif/NAST_Project/blob/main/docs/03_Master_CLI_Examples.md"
                    target="_blank"
                    class="doc-link">
                    <i class="fa-regular fa-file-lines"></i> View on GitHub
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
            </div>
        </li>

        <!-- 04_Data_Outputs -->
        <li>
            <i class="fa-solid fa-floppy-disk" style="color: #fbbf24;"></i>
            <div class="doc-content">
                <strong>Data Outputs &amp; Formats Guide</strong>
                <div class="doc-desc">
                    A technical guide to exporting airfoils directly into XFOIL (<code>.dat</code>),
                    Pandas Machine Learning DataFrames (<code>.csv</code>), and
                    SolidWorks/AutoCAD (<code>.dxf</code>).
                </div>
                <a href="https://github.com/Gamil-Al-Sharif/NAST_Project/blob/main/docs/04_Data_Outputs.md"
                target="_blank"
                class="doc-link">
                <i class="fa-regular fa-file-lines"></i> View on GitHub
                <i class="fa-solid fa-arrow-up-right-from-square"></i>
            </a>
        </div>
    </li>

    <!-- 05_Theory_and_Math -->
    <li>
        <i class="fa-solid fa-square-root-variable" style="color: #f472b6;"></i>
        <div class="doc-content">
            <strong>Math Format &amp; β‑VAE Theory</strong>
            <div class="doc-desc">
                The rigorous analytical calculus behind the 20‑Feature Extractor, and the
                deep‑learning mathematics of the Disentangled KL Divergence loss functions.
            </div>
            <a href="https://github.com/Gamil-Al-Sharif/NAST_Project/blob/main/docs/05_Theory_and_Math.md"
            target="_blank"
            class="doc-link">
            <i class="fa-regular fa-file-lines"></i> View on GitHub
            <i class="fa-solid fa-arrow-up-right-from-square"></i>
        </a>
    </div>
</li>
</ul>
</section>

<!-- ════════════════════════════════════════════ -->
<!-- 6. DEVELOPERS                              -->
<!-- ════════════════════════════════════════════ -->
<section id="developers">
    <h2><i class="fa-solid fa-user-astronaut"></i> 6. About the Developers</h2>

    <div class="dev-grid">
        <!-- Gamil -->
        <div class="dev-card">
            <h3><i class="fa-solid fa-id-badge"></i> Gamil Abdullah Al‑Sharif</h3>
            <p class="title">Mechanical Engineer &amp; AI R&D Specialist &bull; Sana&rsquo;a, Yemen</p>
            <div class="dev-contact">
                <i class="fa-solid fa-envelope"></i>
                <a href="mailto:mely104haja@gmail.com">mely104haja@gmail.com</a>
            </div>
            <div class="dev-contact">
                <i class="fa-brands fa-linkedin"></i>
                <a href="https://linkedin.com/in/gamil-alsharif" target="_blank">linkedin.com/in/gamil-alsharif</a>
            </div>
            <div class="dev-contact">
                <i class="fa-brands fa-github"></i>
                <a href="https://github.com/Gamil-Al-Sharif" target="_blank">github.com/Gamil-Al-Sharif</a>
            </div>
        </div>

        <!-- Yhya -->
        <div class="dev-card">
            <h3><i class="fa-solid fa-id-badge"></i> Yhya Abdullah Al‑Wazir</h3>
            <p class="title">Mechanical Engineer &amp; AI R&D Specialist &bull; Sana&rsquo;a, Yemen</p>
            <div class="dev-contact">
                <i class="fa-solid fa-envelope"></i>
                <a href="mailto:abdullahyhya141@gmail.com">abdullahyhya141@gmail.com</a>
            </div>
            <div class="dev-contact">
                <i class="fa-brands fa-researchgate"></i>
                <a href="https://www.researchgate.net/profile/Yhya-Al-Wazir" target="_blank">ResearchGate Profile</a>
            </div>
            <div class="dev-contact">
                <i class="fa-brands fa-github"></i>
                <a href="https://github.com/Yhya-Al-Wazir" target="_blank">github.com/Yhya-Al-Wazir</a>
            </div>
        </div>
    </div>
</section>

<!-- ════════════════════════════════════════════ -->
<!-- FOOTER                                      -->
<!-- ════════════════════════════════════════════ -->
<footer>
    <div class="footer-links">
        <a href="https://github.com/Gamil-Al-Sharif/NAST_Project" target="_blank">
            <i class="fa-brands fa-github"></i> Repository
        </a>
        <a href="https://github.com/Gamil-Al-Sharif/NAST_Project/issues" target="_blank">
            <i class="fa-regular fa-circle-exclamation"></i> Issues
        </a>
        <a href="https://github.com/Gamil-Al-Sharif/NAST_Project/blob/main/LICENSE" target="_blank">
            <i class="fa-regular fa-scale-balanced"></i> License
        </a>
        <a href="mailto:mely104haja@gmail.com">
            <i class="fa-regular fa-envelope"></i> Contact
        </a>
    </div>
    <p>
        Built with passion for the advancement of computational fluid dynamics and
        deep generative architectures.
    </p>
    <p style="margin-top: 4px;">
        <a href="https://github.com/Gamil-Al-Sharif/NAST_Project" target="_blank" class="star-link">
            ⭐ If you find N.A.S.T. useful, please consider giving it a star!
        </a>
    </p>
</footer>

</div>
<!-- end .container -->
</body>
</html>
