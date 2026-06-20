#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# FILE: nast_master_cli.py
# PROJECT: Neural Aerodynamic Shape Transformation (N.A.S.T.)
# PHASE: Master Unified Production-Grade CLI Tool
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
import time
import argparse
import numpy as np
import scipy.optimize as opt
from scipy.interpolate import CubicSpline, splprep, splev
import onnxruntime as ort
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings

warnings.filterwarnings("ignore")
ort.set_default_logger_severity(3)

# =============================================================================
# 1. BULLETPROOF MATHEMATICAL SPLINE ENGINES & PRECISION LOCK
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
            current_c_max, current_c_min = np.max(camber), np.min(camber)
            if target_c > 0 and current_c_max > 1e-6:
                camber = camber * (target_c / current_c_max)
            elif target_c < 0 and current_c_min < -1e-6:
                camber = camber * (target_c / current_c_min)
                
    camber_shift = y_te_offset - camber[-1]
    camber = camber + (camber_shift * (X / np.max(X)))
    camber[0], thickness[0] = 0.0, 0.0
    
    return camber + (thickness / 2.0), camber - (thickness / 2.0)

def heal_and_repanel(x_ai, y_ai, n_points, strategy='cosine'):
    x_ai, y_ai = np.array(x_ai), np.array(y_ai)
    keep = np.insert(np.sqrt(np.diff(x_ai)**2 + np.diff(y_ai)**2) > 1e-6, 0, True)
    x_clean, y_clean = x_ai[keep], y_ai[keep]

    tck, _ = splprep([x_clean, y_clean], s=1e-5, k=3)
    x_dense, y_dense = splev(np.linspace(0, 1, 3000), tck)
    
    # Mathematical preservation of exact radius (Zero flat-spots)
    x_dense -= np.min(x_dense)
    x_dense /= np.max(x_dense)
    
    s_dense = get_arc_length(x_dense, y_dense)
    spline_x = CubicSpline(s_dense, x_dense, bc_type='not-a-knot')
    spline_y = CubicSpline(s_dense, y_dense, bc_type='not-a-knot')

    x_target = generate_spacing(strategy, n_points)
    y_out, s_out = np.zeros(n_points), np.zeros(n_points)
    
    for i, xt in enumerate(x_target):
        if i == 0: y_out[i], s_out[i] = y_dense[0], 0.0; continue
        if i == n_points - 1: y_out[i], s_out[i] = y_dense[-1], s_dense[-1]; continue
        try: 
            s_root = opt.brentq(lambda s: spline_x(s) - xt, 0, s_dense[-1], xtol=1e-12)
            y_out[i], s_out[i] = spline_y(s_root), s_root
        except: 
            idx = np.argmin(np.abs(x_dense - xt))
            y_out[i], s_out[i] = spline_y(s_dense[idx]), s_dense[idx]
            
    return x_target, y_out, s_out, spline_x, spline_y

def calculate_curvature(s_eval, spline_x, spline_y):
    dx, ddx = spline_x(s_eval, 1), spline_x(s_eval, 2)
    dy, ddy = spline_y(s_eval, 1), spline_y(s_eval, 2)
    den = (dx**2 + dy**2)**1.5
    curv = np.zeros_like(s_eval)
    valid = den > 1e-12
    curv[valid] = (dx[valid]*ddy[valid] - dy[valid]*ddx[valid]) / den[valid]
    return curv

def get_continuous_y_at_x(x_val, s_max, spline_x, spline_y):
    try: return spline_y(opt.brentq(lambda s: spline_x(s) - x_val, 0, s_max, xtol=1e-12))
    except: return 0.0

def get_s_at_x(x_val, s_max, spline_x):
    try: return opt.brentq(lambda s: spline_x(s) - x_val, 0, s_max, xtol=1e-12)
    except: return 0.0

def exact_feature_extraction(x_f, yt, yb, st, sb, sx_t, sy_t, sx_b, sy_b):
    F = np.zeros(20, dtype=np.float64)
    s_t_max, s_b_max = st[-1], sb[-1]

    def continuous_thickness(x_val): return get_continuous_y_at_x(x_val, s_t_max, sx_t, sy_t) - get_continuous_y_at_x(x_val, s_b_max, sx_b, sy_b)
    def continuous_camber(x_val): return (get_continuous_y_at_x(x_val, s_t_max, sx_t, sy_t) + get_continuous_y_at_x(x_val, s_b_max, sx_b, sy_b)) / 2.0

    res_thick = opt.minimize_scalar(lambda x: -continuous_thickness(x), bounds=(0.005, 0.995), method='bounded')
    res_camb  = opt.minimize_scalar(lambda x: -abs(continuous_camber(x)), bounds=(0.005, 0.995), method='bounded')
    F[0], F[1] = -res_thick.fun, res_thick.x
    F[2], F[3] = -res_camb.fun, res_camb.x

    res_crest_u = opt.minimize_scalar(lambda x: -get_continuous_y_at_x(x, s_t_max, sx_t, sy_t), bounds=(0.005, 0.995), method='bounded')
    res_crest_l = opt.minimize_scalar(lambda x: get_continuous_y_at_x(x, s_b_max, sx_b, sy_b), bounds=(0.005, 0.995), method='bounded')
    F[4], F[5] = -res_crest_u.fun, res_crest_u.x
    F[7], F[8] = res_crest_l.fun, res_crest_l.x

    s_crest_u, s_crest_l = get_s_at_x(F[5], s_t_max, sx_t), get_s_at_x(F[8], s_b_max, sx_b)
    F[6] = calculate_curvature(np.array([s_crest_u]), sx_t, sy_t)[0]
    F[9] = calculate_curvature(np.array([s_crest_l]), sx_b, sy_b)[0]

    s_le_u, s_le_l = get_s_at_x(0.005, s_t_max, sx_t), get_s_at_x(0.005, s_b_max, sx_b)
    ku, kl = calculate_curvature(np.array([s_le_u]), sx_t, sy_t)[0], calculate_curvature(np.array([s_le_l]), sx_b, sy_b)[0]
    F[10] = abs(1.0/ku) if abs(ku) > 1e-6 else 0.0
    F[11] = abs(1.0/kl) if abs(kl) > 1e-6 else 0.0
    F[12] = np.degrees(np.arctan(sy_t(s_le_u, 1) / (sx_t(s_le_u, 1) + 1e-12)))
    F[13] = abs(np.degrees(np.arctan(sy_b(s_le_l, 1) / (sx_b(s_le_l, 1) + 1e-12))))

    F[14] = max(0.0, yt[-1] - yb[-1])
    F[15] = (yt[-1] + yb[-1]) / 2.0
    F[16] = np.degrees(np.arctan(sy_t(s_t_max, 1) / (sx_t(s_t_max, 1) + 1e-12)))
    F[17] = np.degrees(np.arctan(sy_b(s_b_max, 1) / (sx_b(s_b_max, 1) + 1e-12)))

    return F

# =============================================================================
# 2. N.A.S.T. INFERENCE ENGINE
# =============================================================================
class NASTEngine:
    def __init__(self, onnx_path="nast_decoder.onnx", norm_path="nast_normalization.npz"):
        self.session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
        norm = np.load(norm_path)
        self.mu_C, self.sig_C = norm['mu_C'].astype(np.float32), norm['sig_C'].astype(np.float32)
        self.mu_Y, self.sig_Y = norm['mu_Y'].astype(np.float32), norm['sig_Y'].astype(np.float32)
        self.X_grid_native = norm['X_grid'].astype(np.float32)
        self.input_name = self.session.get_inputs()[0].name
        
    def generate_native(self, Z, C_phys):
        C_norm = (C_phys - self.mu_C) / self.sig_C
        X_in = np.concatenate((Z, C_norm)).astype(np.float32).reshape(1, 32)
        Y_norm = self.session.run(None, {self.input_name: X_in})[0].flatten()
        Y_phys = (Y_norm * self.sig_Y) + self.mu_Y
        
        yt_native, yb_native = Y_phys[:128], Y_phys[128:]
        
        # PURE ALIGNMENT
        yt_native[0], yb_native[0] = 0.0, 0.0
        te_gap, y_te_offset = C_phys[14], C_phys[15]
        tgt_yt = y_te_offset + (te_gap / 2.0)
        tgt_yb = y_te_offset - (te_gap / 2.0)
        yt_native[-1], yb_native[-1] = tgt_yt, tgt_yb

        return yt_native, yb_native

    def invert_airfoil(self, x_raw, y_raw):
        idx_le = np.argmin(x_raw)
        x_norm = (x_raw - x_raw[idx_le]) / (np.max(x_raw) - x_raw[idx_le])
        y_norm = (y_raw - y_raw[idx_le]) / (np.max(x_raw) - x_raw[idx_le])
        
        if y_norm[0] > y_norm[-1]: 
            xt, yt = x_norm[:idx_le+1][::-1], y_norm[:idx_le+1][::-1]
            xb, yb = x_norm[idx_le:], y_norm[idx_le:]
        else:
            xt, yt = x_norm[:idx_le+1], y_norm[:idx_le+1]
            xb, yb = x_norm[idx_le:], y_norm[idx_le:]

        xf, yt_new, st, sxt, syt = heal_and_repanel(xt, yt, 128, 'cosine')
        _, yb_new, sb, sxb, syb = heal_and_repanel(xb, yb, 128, 'cosine')
        yt_new[0], yb_new[0] = 0.0, 0.0
        
        if yt_new[-1] < yb_new[-1]:
            avg_te = (yt_new[-1] + yb_new[-1]) / 2.0
            yt_new[-1], yb_new[-1] = avg_te, avg_te

        C_target = exact_feature_extraction(xf, yt_new, yb_new, st, sb, sxt, syt, sxb, syb)
        Y_target = np.concatenate([yt_new, yb_new])

        def objective(Z):
            yt_pred, yb_pred = self.generate_native(Z, C_target)
            pred_Y = np.concatenate([yt_pred, yb_pred])
            weights = 1.0 + 9.0 * np.exp(-30.0 * self.X_grid_native)
            w_full = np.concatenate([weights, weights])
            return np.mean(((pred_Y - Y_target)**2) * w_full)

        best_Z = np.zeros(12)
        best_loss = float('inf')
        for Z0 in [np.zeros(12)] + [np.random.randn(12)*0.5 for _ in range(3)]:
            res = opt.minimize(objective, Z0, method='L-BFGS-B', bounds=[(-3.0, 3.0)]*12)
            if res.fun < best_loss: best_loss, best_Z = res.fun, res.x

        rmse = np.sqrt(best_loss)
        return best_Z, C_target, rmse, xf, yt_new, yb_new

# =============================================================================
# 3. UNIVERSAL EXPORTER
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
        data = {"name": name, "latent_vector_Z": Z.tolist() if Z is not None else [], "physics_vector_C": C.tolist() if C is not None else [], "coordinates": {"x": x.tolist(), "y_top": yt.tolist(), "y_bot": yb.tolist()}}
        with open(filename, 'w') as f: json.dump(data, f, indent=4)
        
    @staticmethod
    def to_plot(filename, name, x, yt, yb):
        """Standard plot for generic Synthesis & Generation."""
        plt.figure(figsize=(12, 4), facecolor='white')
        xs, ys = Exporter._format_selig(x, yt, yb)
        plt.plot(xs, ys, color='#2C3E50', lw=2)
        plt.fill(xs, ys, color='#3498DB', alpha=0.2)
        plt.title(f"N.A.S.T. Geometry Plot: {name}", fontsize=14, fontweight='bold')
        plt.axis('equal'); plt.grid(True, ls='--', alpha=0.5)
        plt.gca().spines['top'].set_visible(False); plt.gca().spines['right'].set_visible(False)
        plt.savefig(filename, dpi=200, bbox_inches='tight')
        plt.close()

    @staticmethod
    def to_inversion_plot(filename, name, X_tar, YT_tar, YB_tar, X_pred, YT_pred, YB_pred, rmse, elapsed, C_target, mu_C, sig_C, best_Z):
        """Advanced 3-Panel plot specifically for validating Inversion Mode."""
        fig = plt.figure(figsize=(18, 6), facecolor='#F8F9FA')
        gs = gridspec.GridSpec(1, 3, width_ratios=[4, 1.2, 1.2], figure=fig)
        gs.update(left=0.05, right=0.96, top=0.85, bottom=0.15, wspace=0.25)
        TEXT, GRID = '#2C3E50', '#E0E4E8'

        # Overlay Graph
        ax1 = fig.add_subplot(gs[0])
        ax1.set_facecolor('#FFFFFF')
        ax1.fill(np.concatenate([X_tar, X_tar[::-1]]), np.concatenate([YT_tar, YB_tar[::-1]]), color='#E9ECEF', label='_nolegend_')
        
        ax1.plot(np.concatenate([X_tar, X_tar[::-1]]), np.concatenate([YT_tar, YB_tar[::-1]]), color='#34495E', lw=3, label=f'Target: {name}')
        ax1.plot(np.concatenate([X_pred, X_pred[::-1]]), np.concatenate([YT_pred, YB_pred[::-1]]), color='#E74C3C', lw=2, ls='--', dashes=(4,2), label='N.A.S.T. AI Reconstruction')
        
        ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)
        ax1.set_title('Absolute Aerodynamic Reconstruction', color=TEXT, fontsize=15, fontweight='bold', loc='left')
        ax1.grid(True, ls='-', lw=0.7, color=GRID); ax1.legend(loc='upper right')
        ax1.set_aspect('equal', adjustable='datalim'); ax1.set_ylim(-0.25, 0.25)
        
        clr = '#27AE60' if rmse < 0.003 else ('#F39C12' if rmse < 0.01 else '#C0392B')
        ax1.text(0.02, 0.95, f" RMSE: {rmse:.6f} \n Z-Search Time: {elapsed:.2f}s ", transform=ax1.transAxes, color='white', 
                fontsize=12, fontweight='bold', va='top', bbox=dict(boxstyle='square,pad=0.5', facecolor=clr, edgecolor='none'))

        # C-Physics (20 Features) Bar Chart
        ax2 = fig.add_subplot(gs[1]); ax2.set_facecolor('#FFFFFF')
        c_labels = ["t_max", "x_tmax", "c_max", "x_cmax", "y_up_crest", "x_up_crest", "k_up_crest", "y_lo_crest", "x_lo_crest", "k_lo_crest", 
                    "r_le_up", "r_le_lo", "theta_le_up", "theta_le_lo", "te_gap", "y_te_offset", "theta_te_up", "theta_te_lo", "x_infl_up", "x_infl_lo"]
        
        C_vis = (C_target - mu_C) / sig_C 
        clrs_c = ['#4682B4' if v >= 0 else '#CD5C5C' for v in C_vis]
        ax2.barh(range(20), C_vis, color=clrs_c, height=0.6)
        ax2.set_yticks(range(20)); ax2.set_yticklabels(c_labels, fontsize=8)
        ax2.set_title('20-D C-Physics Vector', fontsize=12, fontweight='bold')
        ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
        ax2.grid(True, axis='x', ls='--', alpha=0.5)

        # Z-Latent (12 Variables) Bar Chart
        ax3 = fig.add_subplot(gs[2]); ax3.set_facecolor('#FFFFFF')
        clrs_z = ['#4682B4' if v >= 0 else '#CD5C5C' for v in best_Z]
        ax3.barh(range(12), best_Z, color=clrs_z, height=0.6)
        ax3.set_yticks(range(12)); ax3.set_yticklabels([f"Z{i}" for i in range(12)], fontsize=8)
        ax3.set_xlim(-3.2, 3.2); ax3.axvline(0, color='#34495E', lw=1)
        ax3.set_title('Optimized 12-D Z-Style', fontsize=12, fontweight='bold')
        ax3.spines['top'].set_visible(False); ax3.spines['right'].set_visible(False)
        ax3.grid(True, axis='x', ls='--', alpha=0.5)

        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()

# =============================================================================
# 4. CLI ORCHESTRATOR
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="N.A.S.T. Universal Output & Geometry CLI")
    
    parser.add_argument('--mode', choices=['invert', 'repanel', 'generate'], required=True)
    parser.add_argument('--input', help="Path to target .dat airfoil.")
    parser.add_argument('--vector', help="Path to target .json vector file.")
    parser.add_argument('--base_dna', help="Name of airfoil in NAST_Global_DNA_Library.json")
    parser.add_argument('--name', default="nast_output", help="Name for output")
    parser.add_argument('--output_dir', default='NAST_Output', help="Directory to save exports.")
    
    parser.add_argument('--points', type=int, default=128, help="Number of points PER SURFACE.")
    parser.add_argument('--spacing', choices=['cosine', 'half-cosine', 'sine', 'linear'], default='cosine')
    
    parser.add_argument('--export_selig', action='store_true')
    parser.add_argument('--export_lednicer', action='store_true')
    parser.add_argument('--export_csv', action='store_true')
    parser.add_argument('--export_dxf', action='store_true')
    parser.add_argument('--export_json', action='store_true')
    parser.add_argument('--export_plot', action='store_true') 

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    
    # STRICT INPUT VALIDATION
    if args.mode in ['repanel', 'invert']:
        if not args.input:
            sys.exit(f"[ERROR] '--input' argument required for '{args.mode}' mode.")
        if not os.path.exists(args.input):
            sys.exit(f"[ERROR] Input file not found: '{args.input}'")
            
    if args.mode == 'generate':
        if not args.vector and not args.base_dna:
            sys.exit(f"[ERROR] Must provide either '--vector' or '--base_dna' for generate mode.")
        if args.vector and not os.path.exists(args.vector):
            sys.exit(f"[ERROR] Vector JSON file not found: '{args.vector}'")

    base_name = args.name if args.mode == 'generate' else os.path.basename(args.input).replace('.dat', '')
    Z_final, C_final = None, None
    x_tar, yt_tar, yb_tar = None, None, None
    rmse, elapsed = None, None

    if args.mode == 'repanel':
        print(f"[*] Repaneling {base_name} strictly via Parametric Math (No AI)...")
        data = np.loadtxt(args.input, skiprows=1)
        idx_le = np.argmin(data[:,0])
        x_raw, y_raw = data[:,0], data[:,1]
        if y_raw[0] > y_raw[-1]: 
            xt, yt = x_raw[:idx_le+1][::-1], y_raw[:idx_le+1][::-1]
            xb, yb = x_raw[idx_le:], y_raw[idx_le:]
        else:
            xt, yt = x_raw[:idx_le+1], y_raw[:idx_le+1]
            xb, yb = x_raw[idx_le:], y_raw[idx_le:]

        x_out, yt_out, _, _, _ = heal_and_repanel(xt, yt, args.points, args.spacing) 
        _, yb_out, _, _, _ = heal_and_repanel(xb, yb, args.points, args.spacing)

    elif args.mode == 'invert':
        print(f"[*] AI Inversion: Cloning {base_name} through the Neural Manifold...")
        data = np.loadtxt(args.input, skiprows=1)
        engine = NASTEngine()
        
        t0 = time.time()
        Z_final, C_final, rmse, x_tar, yt_tar, yb_tar = engine.invert_airfoil(data[:,0], data[:,1])
        elapsed = time.time() - t0
        
        yt_native, yb_native = engine.generate_native(Z_final, C_final)
        
        print(f"[*] Enforcing 100.0% Absolute Precision Limits...")
        yt_native, yb_native = enforce_absolute_precision(
            engine.X_grid_native, yt_native, yb_native, 
            target_t=C_final[0], target_c=C_final[2], 
            te_gap=C_final[14], y_te_offset=C_final[15]
        )
        
        print(f"[*] Translating AI Geometry to {args.points}-point {args.spacing.capitalize()} distribution...")
        x_out, yt_out, _, _, _ = heal_and_repanel(engine.X_grid_native, yt_native, args.points, args.spacing)
        _, yb_out, _, _, _ = heal_and_repanel(engine.X_grid_native, yb_native, args.points, args.spacing)

    elif args.mode == 'generate':
        if args.base_dna:
            print(f"[*] AI Synthesis: Generating '{base_name}' from Global DNA Library template '{args.base_dna}'...")
            
            dna_path = os.path.join("NAST_Scr", "NAST_Global_DNA_Library.json")
            if not os.path.exists(dna_path):
                sys.exit(f"[ERROR] Global DNA library '{dna_path}' not found.")
            with open(dna_path, 'r') as f: dna_lib = json.load(f)
            if args.base_dna not in dna_lib:
                sys.exit(f"[ERROR] Airfoil '{args.base_dna}' not found in the global library.")
                
            Z_final = np.array(dna_lib[args.base_dna]["Z"], dtype=np.float64)
            C_final = np.array(dna_lib[args.base_dna]["C"], dtype=np.float64)
        else:
            print(f"[*] AI Synthesis: Generating '{base_name}' from input vector file '{args.vector}'...")
            with open(args.vector, 'r') as f: vec_data = json.load(f)
            Z_final = np.array(vec_data["latent_vector_Z"], dtype=np.float64)
            C_final = np.array(vec_data["physics_vector_C"], dtype=np.float64)

        engine = NASTEngine()
        yt_native, yb_native = engine.generate_native(Z_final, C_final)
        
        print(f"[*] Enforcing 100.0% Absolute Precision Limits...")
        yt_native, yb_native = enforce_absolute_precision(
            engine.X_grid_native, yt_native, yb_native, 
            target_t=C_final[0], target_c=C_final[2], 
            te_gap=C_final[14], y_te_offset=C_final[15]
        )
        
        print(f"[*] Smoothing and Translating AI Synthesis to {args.points}-point {args.spacing.capitalize()} distribution...")
        x_out, yt_out, _, _, _ = heal_and_repanel(engine.X_grid_native, yt_native, args.points, args.spacing)
        _, yb_out, _, _, _ = heal_and_repanel(engine.X_grid_native, yb_native, args.points, args.spacing)

    print(f"[*] Generating requested export formats...")
    if args.export_selig: Exporter.to_dat(os.path.join(args.output_dir, f"{base_name}_selig.dat"), base_name, x_out, yt_out, yb_out, 'selig')
    if args.export_lednicer: Exporter.to_dat(os.path.join(args.output_dir, f"{base_name}_lednicer.dat"), base_name, x_out, yt_out, yb_out, 'lednicer')
    if args.export_csv: Exporter.to_csv(os.path.join(args.output_dir, f"{base_name}.csv"), x_out, yt_out, yb_out)
    if args.export_dxf: Exporter.to_dxf(os.path.join(args.output_dir, f"{base_name}.dxf"), x_out, yt_out, yb_out)
    if args.export_json: Exporter.to_json(os.path.join(args.output_dir, f"{base_name}.json"), base_name, x_out, yt_out, yb_out, Z_final, C_final)
    
    if args.export_plot:
        # Context-Aware Plot Routing
        if args.mode == 'invert':
            plot_file = os.path.join(args.output_dir, f"{base_name}_inversion.png")
            Exporter.to_inversion_plot(plot_file, base_name, x_tar, yt_tar, yb_tar, engine.X_grid_native, yt_native, yb_native, rmse, elapsed, C_final, engine.mu_C, engine.sig_C, Z_final)
        else:
            plot_file = os.path.join(args.output_dir, f"{base_name}.png")
            Exporter.to_plot(plot_file, base_name, x_out, yt_out, yb_out)
            
    print("[SUCCESS] Processing and Export Complete!")

if __name__ == "__main__":
    main()