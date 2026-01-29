#!/usr/bin/env python3
"""
Check if required dependencies are installed for CALVADOS polymer simulations
"""
import sys

def check_module(module_name, package_name=None):
    """Check if a module can be imported"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name} is NOT installed")
        return False

def main():
    print("Checking CALVADOS dependencies...\n")
    
    required = [
        ('openmm', 'OpenMM'),
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
        ('MDAnalysis', 'MDAnalysis'),
        ('Bio', 'biopython'),
        ('jinja2', 'Jinja2'),
        ('tqdm', 'tqdm'),
        ('matplotlib', 'matplotlib'),
        ('yaml', 'PyYAML'),
        ('statsmodels', 'statsmodels'),
        ('localcider', 'localcider'),
        ('pytest', 'pytest'),
        ('numba', 'numba'),
        ('scipy', 'scipy'),
        ('mdtraj', 'mdtraj'),
    ]
    
    all_installed = True
    for module, package in required:
        if not check_module(module, package):
            all_installed = False
    
    print("\n" + "="*60)
    if all_installed:
        print("✓ All dependencies are installed!")
        print("\nYou can now run simulations:")
        print("  cd polymer_simulations")
        print("  python run_all.py --setup-only")
    else:
        print("✗ Some dependencies are missing!")
        print("\nTo install dependencies:")
        print("\nOption 1 (Recommended - using conda):")
        print("  conda create -n calvados python=3.10")
        print("  conda activate calvados")
        print("  conda install -c conda-forge openmm=8.2.0")
        print("  pip install -e .")
        print("\nOption 2 (Using pip only):")
        print("  pip install -e .")
        print("\nNote: OpenMM installation via pip may not support GPU.")
        print("      Use conda for best results.")
    print("="*60)
    
    return 0 if all_installed else 1

if __name__ == '__main__':
    sys.exit(main())
