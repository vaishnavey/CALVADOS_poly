#!/usr/bin/env python3
"""
Main execution script for polymer simulations
Runs both Case A and Case B simulations with minimization, equilibration, and production
"""
import os
import sys
import subprocess
import argparse

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {cmd}")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode != 0:
        print(f"Error: Command failed with return code {result.returncode}")
        return False
    return True

def setup_case(case_dir):
    """Run prepare.py for a case"""
    prepare_script = os.path.join(case_dir, 'prepare.py')
    if not os.path.exists(prepare_script):
        print(f"Error: prepare.py not found in {case_dir}")
        return False
    
    cmd = f"cd {case_dir} && python prepare.py"
    return run_command(cmd, f"Setting up {os.path.basename(case_dir)}")

def run_simulation(sim_dir, phase_name):
    """Run a single simulation phase"""
    run_script = os.path.join(sim_dir, 'run.py')
    if not os.path.exists(run_script):
        print(f"Error: run.py not found in {sim_dir}")
        return False
    
    cmd = f"cd {sim_dir} && python run.py --path ."
    return run_command(cmd, f"Running {phase_name} in {os.path.basename(os.path.dirname(sim_dir))}")

def run_case_simulations(case_dir, skip_minimization=False, skip_equilibration=False, skip_production=False):
    """Run all simulation phases for a case"""
    case_name = os.path.basename(case_dir)
    
    print(f"\n{'#'*60}")
    print(f"# RUNNING {case_name.upper()}")
    print(f"{'#'*60}\n")
    
    # Minimization
    if not skip_minimization:
        min_dir = os.path.join(case_dir, 'minimization')
        if not run_simulation(min_dir, "Minimization"):
            print(f"Failed to complete minimization for {case_name}")
            return False
    
    # Equilibration
    if not skip_equilibration:
        eq_dir = os.path.join(case_dir, 'equilibration')
        if not run_simulation(eq_dir, "Equilibration"):
            print(f"Failed to complete equilibration for {case_name}")
            return False
    
    # Production
    if not skip_production:
        prod_dir = os.path.join(case_dir, 'production')
        if not run_simulation(prod_dir, "Production (100 ns)"):
            print(f"Failed to complete production for {case_name}")
            return False
    
    print(f"\n✓ Completed all simulations for {case_name}")
    return True

def analyze_crosslinking(case_b_dir):
    """Run crosslinking analysis for Case B"""
    print(f"\n{'#'*60}")
    print(f"# ANALYZING CROSSLINKING (CASE B)")
    print(f"{'#'*60}\n")
    
    prod_dir = os.path.join(case_b_dir, 'production')
    analysis_script = os.path.join(os.path.dirname(case_b_dir), 'analysis', 'analyze_crosslinking.py')
    
    # Find trajectory and topology files
    traj_file = None
    top_file = None
    
    for f in os.listdir(prod_dir):
        if f.endswith('.dcd'):
            traj_file = os.path.join(prod_dir, f)
        elif f.endswith('.pdb'):
            top_file = os.path.join(prod_dir, f)
    
    if not traj_file or not top_file:
        print("Warning: Could not find trajectory (.dcd) or topology (.pdb) files")
        print("Skipping crosslinking analysis")
        return False
    
    output_prefix = os.path.join(prod_dir, 'crosslinking_analysis')
    cmd = f"python {analysis_script} --traj {traj_file} --top {top_file} --output {output_prefix}"
    
    return run_command(cmd, "Analyzing crosslinking extent")

def main():
    parser = argparse.ArgumentParser(description='Run polymer simulations')
    parser.add_argument('--case', choices=['a', 'b', 'both'], default='both',
                       help='Which case to run: a (polyallylamine only), b (mixed), or both (default: both)')
    parser.add_argument('--skip-minimization', action='store_true',
                       help='Skip minimization phase')
    parser.add_argument('--skip-equilibration', action='store_true',
                       help='Skip equilibration phase')
    parser.add_argument('--skip-production', action='store_true',
                       help='Skip production phase')
    parser.add_argument('--analyze-only', action='store_true',
                       help='Only run crosslinking analysis (requires completed Case B simulation)')
    parser.add_argument('--setup-only', action='store_true',
                       help='Only run setup scripts, do not run simulations')
    
    args = parser.parse_args()
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    case_a_dir = os.path.join(script_dir, 'case_a')
    case_b_dir = os.path.join(script_dir, 'case_b')
    
    print("\n" + "="*60)
    print("POLYMER SIMULATION RUNNER")
    print("="*60)
    
    # Analysis only mode
    if args.analyze_only:
        analyze_crosslinking(case_b_dir)
        return
    
    # Setup phase
    if args.case in ['a', 'both']:
        if not setup_case(case_a_dir):
            print("Failed to setup Case A")
            return
    
    if args.case in ['b', 'both']:
        if not setup_case(case_b_dir):
            print("Failed to setup Case B")
            return
    
    if args.setup_only:
        print("\n✓ Setup complete. Run without --setup-only to start simulations.")
        return
    
    # Run simulations
    success = True
    
    if args.case in ['a', 'both']:
        if not run_case_simulations(case_a_dir, 
                                   args.skip_minimization, 
                                   args.skip_equilibration, 
                                   args.skip_production):
            success = False
    
    if args.case in ['b', 'both']:
        if not run_case_simulations(case_b_dir,
                                   args.skip_minimization,
                                   args.skip_equilibration,
                                   args.skip_production):
            success = False
    
    # Analyze crosslinking for Case B
    if args.case in ['b', 'both'] and not args.skip_production:
        analyze_crosslinking(case_b_dir)
    
    # Final summary
    print("\n" + "="*60)
    if success:
        print("✓ ALL SIMULATIONS COMPLETED SUCCESSFULLY")
    else:
        print("✗ SOME SIMULATIONS FAILED")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
