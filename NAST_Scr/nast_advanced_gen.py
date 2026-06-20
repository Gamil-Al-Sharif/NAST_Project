#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# FILE: nast_advanced_gen.py
# PROJECT: Neural Aerodynamic Shape Transformation (N.A.S.T.)
# PHASE: Advanced Macro/Micro Synthesis & Export Engine
#
# ==============================================================================
# ABOUT THE DEVELOPERS:
# ------------------------------------------------------------------------------
# Gamil Abdullah Al-Sharif
# Mechanical Engineer & R&D Specialist | Sana'a, Yemen
# ✉️ Email: mely104haja@gmail.com
# 💼 LinkedIn: linkedin.com/in/gamil-alsharif
#
# Yhya Abdullah Al-Wazir
# Mechanical Engineer & R&D Specialist | Sana'a, Yemen
# ✉️ Email: abdullahyhya141@gmail.com
# 🔬 ResearchGate: profile/Yhya-Abdullah-Al-Waze
# ==============================================================================

import os
import sys
import json
import argparse
import numpy as np
import scipy.optimize as opt
from scipy.interpolate import CubicSpline, splprep, splev
import onnxruntime as ort
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")
ort.set_default_logger_severity(3)

# =============================================================================
# 1. ABSOLUTE PRECISION GEOMETRY ENGINE (Post-Processing & Healing)
# =============================================================================
def generate_spacing(strategy, n_points):
    if strategy == 'cosine': return 0.5 * (1.0 - np.cos(np.linspace(0.0, np.pi, n_points)))
    elif strategy == 'half-cosine': return 1.0 - np.cos(np.linspace(0.0, np.pi/2, n_points))
    elif strategy == 'sine': return np.sin(np.linspace(0.0, np.pi/2, n_points))
    elif strategy == 'linear': return np.linspace(0.0, 1.0, n_points)
    else: raise ValueError(f"Unknown strategy: {strategy}")

def get_arc_length(x, y):
    return np.concatenate(([0], np.cumsum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))))

def enforce_absolute_precision(X, yt, yb, target_t, target_c, te_gap, y_te_offset):
    camber = (yt + yb) / 2.0
    thickness = yt - yb
    
    t_delta = np.maximum(thickness - te_gap, 0.0) 
    
    if target_t is not None:
        max_td = np.max(t_delta)
        target_td = target_t - te_gap
        if max_td > 1e-6 and target_td > 0:
            t_delta = t_delta * (target_td / max_td)
            
    thickness = t_delta + te_gap
    
    if target_c is not None:
        if abs(target_c) < 1e-6:
            camber = camber * 0.0 
        else:
            current_c_max = np.max(camber)
            current_c_min = np.min(camber)
            if target_c > 0 and current_c_max > 1e-6:
                camber = camber * (target_c / current_c_max)
            elif target_c < 0 and current_c_min < -1e-6:
                camber = camber * (target_c / current_c_min)
                
    camber_shift = y_te_offset - camber[-1]
    blend = X / np.max(X)
    camber = camber + (camber_shift * blend)
    
    camber[0], thickness[0] = 0.0, 0.0
    
    yt_new = camber + (thickness / 2.0)
    yb_new = camber - (thickness / 2.0)
    return yt_new, yb_new

def heal_and_repanel(x_ai, y_ai, n_points, strategy):
    x_ai, y_ai = np.array(x_ai), np.array(y_ai)
    
    keep = np.insert(np.sqrt(np.diff(x_ai)**2 + np.diff(y_ai)**2) > 1e-6, 0, True)
    x_clean, y_clean = x_ai[keep], y_ai[keep]

    tck, _ = splprep([x_clean, y_clean], s=1e-5, k=3)
    x_dense, y_dense = splev(np.linspace(0, 1, 3000), tck)
    
    # MAGIC FIX FOR FLAT NOSES & PINCHES:
    # Instead of clipping negative X (which flattens the nose), 
    # we perfectly shift and re-normalize the curve to preserve the exact radius.
    x_dense -= np.min(x_dense)
    x_dense /= np.max(x_dense)
    
    s_dense = get_arc_length(x_dense, y_dense)
    spline_x = CubicSpline(s_dense, x_dense, bc_type='not-a-knot')
    spline_y = CubicSpline(s_dense, y_dense, bc_type='not-a-knot')

    x_target = generate_spacing(strategy, n_points)
    y_out = np.zeros(n_points)
    
    for i, xt in enumerate(x_target):
        if i == 0: y_out[i] = y_dense[0]; continue
        if i == n_points - 1: y_out[i] = y_dense[-1]; continue
        try: 
            s_root = opt.brentq(lambda s: spline_x(s) - xt, 0, s_dense[-1], xtol=1e-12)
            y_out[i] = spline_y(s_root)
        except: 
            y_out[i] = spline_y(s_dense[np.argmin(np.abs(x_dense - xt))])
            
    return x_target, y_out

# =============================================================================
# 2. UNIVERSAL EXPORTER
# =============================================================================
class Exporter:
    @staticmethod
    def _format_selig(x, yt, yb): return np.concatenate([x[::-1], x[1:]]), np.concatenate([yt[::-1], yb[1:]])
    @staticmethod
    def to_dat(filename, name, x, yt, yb, format_type='selig'):
        with open(filename, 'w') as f:
            f.write(f"{name}\n")
            if format_type == 'selig':
                xs, ys = Exporter._format_selig(x, yt, yb)
                for i in range(len(xs)): f.write(f"{xs[i]:.6f} {ys[i]:.6f}\n")
            else:
                f.write(f"  {len(x)}.  {len(x)}.\n\n")
                for i in range(len(x)): f.write(f"{x[i]:.6f} {yt[i]:.6f}\n")
                f.write("\n")
                for i in range(len(x)): f.write(f"{x[i]:.6f} {yb[i]:.6f}\n")
    @staticmethod
    def to_csv(filename, x, yt, yb):
        with open(filename, 'w') as f:
            f.write("X,Y,Surface\n")
            for i in range(len(x)): f.write(f"{x[i]:.6f},{yt[i]:.6f},Top\n")
            for i in range(len(x)): f.write(f"{x[i]:.6f},{yb[i]:.6f},Bottom\n")
    @staticmethod
    def to_dxf(filename, x, yt, yb):
        xs, ys = Exporter._format_selig(x, yt, yb)
        with open(filename, 'w') as f:
            f.write("0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n8\n0\n90\n")
            f.write(f"{len(xs)}\n70\n1\n") 
            for i in range(len(xs)): f.write(f"10\n{xs[i]:.6f}\n20\n{ys[i]:.6f}\n")
            f.write("0\nSEQEND\n0\nENDSEC\n0\nEOF\n")
    @staticmethod
    def to_json(filename, name, x, yt, yb, Z, C):
        with open(filename, 'w') as f: json.dump({"name": name, "latent_vector_Z": Z.tolist(), "physics_vector_C": C.tolist(), "coordinates": {"x": x.tolist(), "y_top": yt.tolist(), "y_bot": yb.tolist()}}, f, indent=4)
    @staticmethod
    def to_plot(filename, name, x, yt, yb):
        plt.figure(figsize=(12, 4), facecolor='white')
        xs, ys = Exporter._format_selig(x, yt, yb)
        plt.plot(xs, ys, color='#2C3E50', lw=2)
        plt.fill(xs, ys, color='#3498DB', alpha=0.2)
        plt.title(f"N.A.S.T. Synthesized Airfoil: {name}", fontsize=14, fontweight='bold')
        plt.axis('equal'); plt.grid(True, ls='--', alpha=0.5)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.savefig(filename, dpi=200, bbox_inches='tight')
        plt.close()

# =============================================================================
# 3. MAIN SYNTHESIS ORCHESTRATOR
# =============================================================================
def main():
    z_vec_str = None
    args_to_remove = []
    for i in range(len(sys.argv)):
        if sys.argv[i].startswith('--z_vector='):
            z_vec_str = sys.argv[i].split('=', 1)[1]
            args_to_remove.append(i)
        elif sys.argv[i] == '--z_vector':
            if i + 1 < len(sys.argv):
                z_vec_str = sys.argv[i+1]
                args_to_remove.extend([i, i+1])
    for i in sorted(args_to_remove, reverse=True): sys.argv.pop(i)

    parser = argparse.ArgumentParser(description="N.A.S.T. Advanced Synthesis Engine")
    parser.add_argument('--name', default="custom_airfoil", help="Name of the output airfoil.")
    parser.add_argument('--output_dir', default="NAST_Output", help="Folder to save outputs.")
    parser.add_argument('--base_dna', type=str, help="Name of airfoil in NAST_Global_DNA_Library.json")
    
    parser.add_argument('--points', type=int, default=128)
    parser.add_argument('--spacing', choices=['cosine', 'half-cosine', 'sine', 'linear'], default='cosine')
    
    parser.add_argument('--export_selig', action='store_true')
    parser.add_argument('--export_lednicer', action='store_true')
    parser.add_argument('--export_csv', action='store_true')
    parser.add_argument('--export_dxf', action='store_true')
    parser.add_argument('--export_json', action='store_true')
    parser.add_argument('--export_plot', action='store_true')

    parser.add_argument('--t_max', type=float); parser.add_argument('--x_tmax', type=float)
    parser.add_argument('--c_max', type=float); parser.add_argument('--x_cmax', type=float)
    parser.add_argument('--y_up_crest', type=float); parser.add_argument('--x_up_crest', type=float)
    parser.add_argument('--k_up_crest', type=float); parser.add_argument('--y_lo_crest', type=float)
    parser.add_argument('--x_lo_crest', type=float); parser.add_argument('--k_lo_crest', type=float)
    parser.add_argument('--r_le_up', type=float); parser.add_argument('--r_le_lo', type=float)
    parser.add_argument('--theta_le_up', type=float); parser.add_argument('--theta_le_lo', type=float)
    parser.add_argument('--te_gap', type=float); parser.add_argument('--y_te_offset', type=float)
    parser.add_argument('--theta_te_up', type=float); parser.add_argument('--theta_te_lo', type=float)
    parser.add_argument('--x_infl_up', type=float); parser.add_argument('--x_infl_lo', type=float)

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 80)
    print(f" N.A.S.T. - ADVANCED SYNTHESIS ENGINE (WITH 100.0% PRECISION)")
    print("=" * 80)

    session = ort.InferenceSession("nast_decoder.onnx", providers=['CPUExecutionProvider'])
    norm = np.load("nast_normalization.npz")
    mu_C, sig_C = norm['mu_C'].astype(np.float32), norm['sig_C'].astype(np.float32)
    mu_Y, sig_Y = norm['mu_Y'].astype(np.float32), norm['sig_Y'].astype(np.float32)
    X_grid_native = norm['X_grid'].astype(np.float32)

    Z_final = np.zeros(12, dtype=np.float32)
    C_phys = np.copy(mu_C)
    
    if args.base_dna:
        dna_path = os.path.join("NAST_Scr", "NAST_Global_DNA_Library.json")
        if not os.path.exists(dna_path):
            sys.exit(f"[ERROR] Global DNA library '{dna_path}' not found. ")
        else:
            try:
                with open(dna_path, 'r') as f: dna_lib = json.load(f)
                if args.base_dna in dna_lib:
                    print(f"[*] Successfully loaded template DNA for: {args.base_dna}")
                    Z_final = np.array(dna_lib[args.base_dna]["Z"], dtype=np.float32)
                    C_phys = np.array(dna_lib[args.base_dna]["C"], dtype=np.float32)
                else: print(f"[WARNING] Airfoil '{args.base_dna}' not found in library.")
            except Exception as e: print(f"[ERROR] Failed to read DNA library: {e}")

    if z_vec_str:
        try: Z_final = np.array([float(x) for x in z_vec_str.split(',')], dtype=np.float32)
        except: sys.exit("[ERROR] --z_vector must contain exactly 12 comma-separated floats.")

    cli_mapping = {
        0: args.t_max, 1: args.x_tmax, 2: args.c_max, 3: args.x_cmax,
        4: args.y_up_crest, 5: args.x_up_crest, 6: args.k_up_crest,
        7: args.y_lo_crest, 8: args.x_lo_crest, 9: args.k_lo_crest,
        10: args.r_le_up, 11: args.r_le_lo, 12: args.theta_le_up, 13: args.theta_le_lo,
        14: args.te_gap, 15: args.y_te_offset, 16: args.theta_te_up, 17: args.theta_te_lo,
        18: args.x_infl_up, 19: args.x_infl_lo
    }
    for idx, val in cli_mapping.items():
        if val is not None: C_phys[idx] = val

    mu_t, mu_c = mu_C[0], mu_C[2]
    delta_t, delta_c = C_phys[0] - mu_t, C_phys[2] - mu_c
    t_ratio = C_phys[0] / mu_t if mu_t > 0 else 1.0

    if args.y_up_crest is None: C_phys[4] = mu_C[4] + delta_c + (delta_t / 2.0)
    if args.y_lo_crest is None: C_phys[7] = mu_C[7] + delta_c - (delta_t / 2.0)
    if args.r_le_up is None: C_phys[10] = mu_C[10] * (t_ratio**2)
    if args.r_le_lo is None: C_phys[11] = mu_C[11] * (t_ratio**2)
    if args.theta_le_up is None: C_phys[12] = mu_C[12] * t_ratio + (delta_c * 40.0)
    if args.theta_le_lo is None: C_phys[13] = mu_C[13] * t_ratio - (delta_c * 40.0)
    if args.theta_te_up is None: C_phys[16] = mu_C[16] * t_ratio - (delta_c * 15.0)
    if args.theta_te_lo is None: C_phys[17] = mu_C[17] * t_ratio - (delta_c * 15.0)
    
    if args.theta_te_up is not None and abs(args.theta_te_up - mu_C[16]) > 10.0:
        if args.x_infl_up is None: C_phys[18] = 0.85
    if args.theta_te_lo is not None and abs(args.theta_te_lo - mu_C[17]) > 10.0:
        if args.x_infl_lo is None: C_phys[19] = 0.85

    theoretical_r_max = 1.20 * (C_phys[0]**2)
    C_phys[10] = min(C_phys[10], theoretical_r_max)
    C_phys[11] = min(C_phys[11], theoretical_r_max)

    print(f"[*] AI Network Synthesizing '{args.name}'...")
    C_norm = (C_phys - mu_C) / sig_C
    X_in = np.concatenate((Z_final, C_norm)).astype(np.float32).reshape(1, 32)
    
    Y_norm_out = session.run(None, {session.get_inputs()[0].name: X_in})[0].flatten()
    Y_phys = (Y_norm_out * sig_Y) + mu_Y
    yt_native, yb_native = Y_phys[:128], Y_phys[128:]

    print(f"[*] Applying Absolute Precision Enforcements (100.0% Scaling & Anti-Crossover)...")
    yt_native, yb_native = enforce_absolute_precision(
        X_grid_native, yt_native, yb_native, 
        target_t=args.t_max, target_c=args.c_max, 
        te_gap=C_phys[14], y_te_offset=C_phys[15]
    )

    print(f"[*] Mathematical B-Spline Healing to {args.points} points ({args.spacing})...")
    x_out, yt_out = heal_and_repanel(X_grid_native, yt_native, args.points, args.spacing)
    _, yb_out = heal_and_repanel(X_grid_native, yb_native, args.points, args.spacing)

    print(f"[*] Exporting files to '{args.output_dir}'...")
    if args.export_selig: Exporter.to_dat(os.path.join(args.output_dir, f"{args.name}_selig.dat"), args.name, x_out, yt_out, yb_out, 'selig')
    if args.export_lednicer: Exporter.to_dat(os.path.join(args.output_dir, f"{args.name}_lednicer.dat"), args.name, x_out, yt_out, yb_out, 'lednicer')
    if args.export_csv: Exporter.to_csv(os.path.join(args.output_dir, f"{args.name}.csv"), x_out, yt_out, yb_out)
    if args.export_dxf: Exporter.to_dxf(os.path.join(args.output_dir, f"{args.name}.dxf"), x_out, yt_out, yb_out)
    if args.export_json: Exporter.to_json(os.path.join(args.output_dir, f"{args.name}.json"), args.name, x_out, yt_out, yb_out, Z_final, C_phys)
    if args.export_plot: Exporter.to_plot(os.path.join(args.output_dir, f"{args.name}.png"), args.name, x_out, yt_out, yb_out)
    print("[SUCCESS] Synthesis and Export Complete!")

if __name__ == "__main__":
    main()