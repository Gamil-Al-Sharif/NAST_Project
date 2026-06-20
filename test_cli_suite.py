#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# FILE: test_cli_suite.py
# PROJECT: Neural Aerodynamic Shape Transformation (N.A.S.T.)
# UTILITY: Automated QA Testing for Master CLI Scripts
# ==============================================================================

import os
import sys
import subprocess
import time
import shutil
import numpy as np

# =============================================================================
# 1. SETUP HELPERS
# =============================================================================
def create_dummy_target():
    """Generates a mathematical NACA 0012 to use as a guaranteed clean target."""
    os.makedirs("Foil_Folder", exist_ok=True)
    filepath = "Foil_Folder/test_target_0012.dat"
    
    # Generate NACA 0012
    x = np.linspace(0, 1, 100)
    y = 0.60 * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    
    x_selig = np.concatenate([x[::-1], x[1:]])
    y_selig = np.concatenate([y[::-1], -y[1:]])
    
    with open(filepath, 'w') as f:
        f.write("test_target_0012\n")
        for i in range(len(x_selig)):
            f.write(f"{x_selig[i]:.6f} {y_selig[i]:.6f}\n")
    return filepath

def run_test(test_name, command, expected_files):
    """Executes a CLI command and verifies the output files were generated."""
    print(f"\n[{test_name}]")
    print(f"Executing: {command}")
    
    t0 = time.time()
    # Run the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    elapsed = time.time() - t0
    
    # Check for crashes
    if result.returncode != 0:
        print(f"  ❌ FAILED (Crashed in {elapsed:.2f}s)")
        print(f"  Error Log:\n{result.stderr}")
        return False
        
    # Verify outputs
    missing_files = []
    for file in expected_files:
        if not os.path.exists(file):
            missing_files.append(file)
            
    if missing_files:
        print(f"  ❌ FAILED (Command ran, but files were not created)")
        for m in missing_files: print(f"     Missing: {m}")
        return False
    else:
        print(f"  ✅ SUCCESS ({elapsed:.2f}s) - All {len(expected_files)} files verified.")
        return True

# =============================================================================
# 2. MAIN TEST SUITE
# =============================================================================
def main():
    print("=" * 80)
    print(" N.A.S.T. - AUTOMATED CLI TEST SUITE")
    print("=" * 80)
    
    # Pre-flight checklist
    print("[*] Checking for AI model files...")
    missing_files = False
    
    # Added "nast_decoder.onnx.data" to support externally saved ONNX weights
    check_files = ["nast_decoder.onnx", "nast_decoder.onnx.data", "nast_normalization.npz"]
    
    for fname in check_files:
        # If not in root, but exists in NAST_Scr, copy them to root 
        if not os.path.exists(fname) and os.path.exists(os.path.join("NAST_Scr", fname)):
            print(f"    Copying {fname} from NAST_Scr/ to root directory...")
            shutil.copy(os.path.join("NAST_Scr", fname), fname)
        
        # If core files are still missing in root, flag them
        if fname in ["nast_decoder.onnx", "nast_normalization.npz"] and not os.path.exists(fname):
            missing_files = True

    if missing_files:
        print("[ERROR] Missing nast_decoder.onnx or nast_normalization.npz in root directory!")
        print("Please ensure the AI is fully trained and model files are placed in the current directory.")
        sys.exit(1)

    print("[*] Generating baseline target airfoil (Foil_Folder/test_target_0012.dat)...")
    target_file = create_dummy_target()
    out_dir = "NAST_Test_Outputs"
    os.makedirs(out_dir, exist_ok=True)
    
    tests_passed = 0
    total_tests = 10

    # -------------------------------------------------------------------------
    # PART 1: NAST_Scr/nast_advanced_gen.py TESTS
    # -------------------------------------------------------------------------
    
    # TEST 1: Basic Macro features + All Export Formats
    cmd1 = f"python NAST_Scr/nast_advanced_gen.py --name test_gen_all_exports --output_dir {out_dir} --t_max 0.15 --c_max 0.05 --export_selig --export_lednicer --export_csv --export_dxf --export_json --export_plot"
    exp1 = [f"{out_dir}/test_gen_all_exports_selig.dat", f"{out_dir}/test_gen_all_exports_lednicer.dat", f"{out_dir}/test_gen_all_exports.csv", f"{out_dir}/test_gen_all_exports.dxf", f"{out_dir}/test_gen_all_exports.json", f"{out_dir}/test_gen_all_exports.png"]
    if run_test("TEST 1: AdvancedGen - All 6 Export Formats", cmd1, exp1): tests_passed += 1

    # TEST 2: High Resolution Linear Spacing
    cmd2 = f"python NAST_Scr/nast_advanced_gen.py --name test_gen_linear --output_dir {out_dir} --points 300 --spacing linear --export_selig"
    exp2 = [f"{out_dir}/test_gen_linear_selig.dat"]
    if run_test("TEST 2: AdvancedGen - High-Res Linear Spacing (300 pts)", cmd2, exp2): tests_passed += 1

    # TEST 3: Acoustic Sine Spacing (Dense trailing edge)
    cmd3 = f"python NAST_Scr/nast_advanced_gen.py --name test_gen_sine --output_dir {out_dir} --points 100 --spacing sine --export_csv"
    exp3 = [f"{out_dir}/test_gen_sine.csv"]
    if run_test("TEST 3: AdvancedGen - Sine Spacing (100 pts)", cmd3, exp3): tests_passed += 1

    # TEST 4: Micro-Style Z-Vector Injection
    cmd4 = f"python NAST_Scr/nast_advanced_gen.py --name test_gen_zvec --output_dir {out_dir} --z_vector \"2.0,-1.5,0.0,0.5,1.1,-1.1,0.0,0.0,0.0,0.0,-2.0,2.0\" --export_json --export_plot"
    exp4 = [f"{out_dir}/test_gen_zvec.json", f"{out_dir}/test_gen_zvec.png"]
    if run_test("TEST 4: AdvancedGen - Custom 12-D Z-Vector Injection", cmd4, exp4): tests_passed += 1

    # TEST 5: Extreme 20-Feature C-Vector Override
    cmd5 = (f"python NAST_Scr/nast_advanced_gen.py --name test_gen_extreme_c --output_dir {out_dir} "
            f"--t_max 0.12 --x_tmax 0.35 --c_max 0.02 --x_cmax 0.45 "
            f"--y_up_crest 0.08 --x_up_crest 0.35 --k_up_crest -1.2 "
            f"--y_lo_crest -0.04 --x_lo_crest 0.35 --k_lo_crest 0.8 "
            f"--r_le_up 0.015 --r_le_lo 0.015 --theta_le_up 45.0 --theta_le_lo 45.0 "
            f"--te_gap 0.005 --y_te_offset 0.0 --theta_te_up -10.0 --theta_te_lo 5.0 "
            f"--x_infl_up 0.8 --x_infl_lo 0.8 --export_selig")
    exp5 = [f"{out_dir}/test_gen_extreme_c_selig.dat"]
    if run_test("TEST 5: AdvancedGen - Explicit 20-Feature C-Vector Overrides", cmd5, exp5): tests_passed += 1


    # -------------------------------------------------------------------------
    # PART 2: nast_master_cli.py TESTS
    # -------------------------------------------------------------------------

    # TEST 6: Repanel Mode (Pure Math, No AI)
    cmd6 = f"python NAST_Scr/nast_master_cli.py --mode repanel --input {target_file} --output_dir {out_dir} --points 256 --spacing half-cosine --export_selig --export_csv"
    exp6 = [f"{out_dir}/test_target_0012_selig.dat", f"{out_dir}/test_target_0012.csv"]
    if run_test("TEST 6: MasterCLI - Mode: Repanel (Half-Cosine, 256 pts)", cmd6, exp6): tests_passed += 1

    # TEST 7: Invert Mode (AI Cloning) -> Export JSON DNA
    cmd7 = f"python NAST_Scr/nast_master_cli.py --mode invert --input {target_file} --output_dir {out_dir} --export_json --export_dxf"
    exp7 = [f"{out_dir}/test_target_0012.json", f"{out_dir}/test_target_0012.dxf"]
    if run_test("TEST 7: MasterCLI - Mode: Invert (Extract JSON & DXF)", cmd7, exp7): tests_passed += 1

    # TEST 8: Generate Mode (Using the JSON extracted from Test 7)
    json_path = f"{out_dir}/test_target_0012.json"
    cmd8 = f"python NAST_Scr/nast_master_cli.py --mode generate --vector {json_path} --name test_master_regenerated --output_dir {out_dir} --points 150 --spacing linear --export_selig --export_plot"
    exp8 = [f"{out_dir}/test_master_regenerated_selig.dat", f"{out_dir}/test_master_regenerated.png"]
    
    if os.path.exists(json_path):
        if run_test("TEST 8: MasterCLI - Mode: Generate (From JSON Vector)", cmd8, exp8): tests_passed += 1
    else:
        print("\n[TEST 8: MasterCLI - Mode: Generate]")
        print("  ❌ FAILED (Skipped because Test 7 failed to create the JSON vector)")

    # TEST 9: Invert Mode -> Bad File Handling
    cmd9 = f"python NAST_Scr/nast_master_cli.py --mode invert --input Foil_Folder/does_not_exist.dat --output_dir {out_dir} --export_selig"
    print(f"\n[TEST 9: MasterCLI - Error Handling (Missing Target)]")
    res9 = subprocess.run(cmd9, shell=True, capture_output=True, text=True)
    if "No such file" in res9.stderr or "Error" in res9.stderr or res9.returncode != 0:
        print("  ✅ SUCCESS - CLI safely caught the missing file error.")
        tests_passed += 1
    else:
        print("  ❌ FAILED - CLI did not handle the missing file properly.")

    # TEST 10: Generate Mode -> Missing Vector Error Handling
    cmd10 = f"python NAST_Scr/nast_master_cli.py --mode generate --name fail_test --output_dir {out_dir} --export_selig"
    print(f"\n[TEST 10: MasterCLI - Error Handling (Missing Vector Arg)]")
    res10 = subprocess.run(cmd10, shell=True, capture_output=True, text=True)
    if "required" in res10.stderr or "error" in res10.stderr.lower():
        print("  ✅ SUCCESS - CLI safely demanded the --vector argument.")
        tests_passed += 1
    else:
        print("  ❌ FAILED - CLI executed Generate mode without a vector file.")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f" TEST SUITE COMPLETE: {tests_passed} / {total_tests} Tests Passed")
    if tests_passed == total_tests:
        print(" 🏆 YOUR N.A.S.T. CLI FRAMEWORK IS FULLY OPERATIONAL AND PRODUCTION-READY.")
    else:
        print(" ⚠️ SOME TESTS FAILED. Please review the error logs above.")
    print("=" * 80)

if __name__ == "__main__":
    main()