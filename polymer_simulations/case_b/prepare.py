#!/usr/bin/env python3
"""
Setup script for Case B: 50% Polyallylamine + 50% Glutaraldehyde System
Simulates a 5 nm cubic box with mixed polymer chains
"""
import os
import sys
import subprocess

# Add parent directory to path to import calvados
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from calvados.cfg import Config, Components

# Get current working directory
cwd = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(os.path.dirname(cwd), 'input')

# System name
sysname = 'case_b_mixed'

# Set the side length of the cubic box (5 nm = 50 Angstroms)
L = 5.0  # nm

# Simulation parameters for 100 ns
timestep_fs = 10  # fs
simulation_time_ns = 100  # ns
total_steps = int(simulation_time_ns * 1e6)  # 100 ns = 10^7 steps

# Saving interval (save every 10 ps = 1000 steps)
N_save = 1000  
N_frames = total_steps // N_save  # 10000 frames for 100 ns

# Equilibration steps (1 ns = 100000 steps)
equil_steps = 100000

residues_file = os.path.join(input_dir, 'polymer_residues.csv')

# MINIMIZATION CONFIG
config_min = Config(
    # GENERAL
    sysname = sysname + '_min',
    box = [L, L, L],  # nm
    temp = 293.15,  # K
    ionic = 0.15,  # M
    pH = 7.0,
    
    # MINIMIZATION SETTINGS
    minimize = True,
    minimize_steps = 1000,
    
    # RUNTIME SETTINGS
    wfreq = 100,
    steps = 100,  # minimal steps after minimization
    platform = 'CPU',
    verbose = True,
)

# EQUILIBRATION CONFIG
config_eq = Config(
    # GENERAL
    sysname = sysname + '_eq',
    box = [L, L, L],  # nm
    temp = 293.15,  # K
    ionic = 0.15,  # M
    pH = 7.0,
    
    # RUNTIME SETTINGS
    wfreq = N_save,
    steps = equil_steps,  # 1 ns equilibration
    platform = 'CPU',
    restart = 'checkpoint',
    frestart = 'restart.chk',
    verbose = True,
)

# PRODUCTION CONFIG
config_prod = Config(
    # GENERAL
    sysname = sysname + '_prod',
    box = [L, L, L],  # nm
    temp = 293.15,  # K
    ionic = 0.15,  # M
    pH = 7.0,
    
    # RUNTIME SETTINGS
    wfreq = N_save,  # save every 10 ps
    steps = total_steps,  # 100 ns production
    platform = 'CPU',
    restart = 'checkpoint',
    frestart = 'restart.chk',
    verbose = True,
)

# Create output directories
path_min = os.path.join(cwd, 'minimization')
path_eq = os.path.join(cwd, 'equilibration')
path_prod = os.path.join(cwd, 'production')

for path in [path_min, path_eq, path_prod]:
    os.makedirs(path, exist_ok=True)

# Write config files
config_min.write(path_min, name='config.yaml')
config_eq.write(path_eq, name='config.yaml')
config_prod.write(path_prod, name='config.yaml')

# Define components - 50% polyallylamine, 50% glutaraldehyde
# 5 chains of each type
components_paa = Components(
    molecule_type = 'protein',  # treat as protein-like polymer
    nmol = 5,  # 5 chains of polyallylamine
    restraint = False,
    charge_termini = 'both',
    periodic = True,
    
    # INPUT
    fresidues = residues_file,
    ffasta = os.path.join(input_dir, 'polyallylamine.fasta'),
)

components_paa.add(name='polyallylamine_chain')

# Now add glutaraldehyde chains
components_gta = Components(
    molecule_type = 'protein',  # treat as protein-like polymer
    nmol = 5,  # 5 chains of glutaraldehyde
    restraint = False,
    charge_termini = 'both',
    periodic = True,
    
    # INPUT
    fresidues = residues_file,
    ffasta = os.path.join(input_dir, 'glutaraldehyde.fasta'),
)

components_gta.add(name='glutaraldehyde_chain')

# Merge the component systems
# We need to manually create a combined components structure
combined_components = {
    'defaults': components_paa.components['defaults'],
    'system': {
        'polyallylamine_chain': components_paa.components['system']['polyallylamine_chain'],
        'glutaraldehyde_chain': {
            'fresidues': residues_file,
            'ffasta': os.path.join(input_dir, 'glutaraldehyde.fasta'),
        }
    }
}

# Update nmol for each component
combined_components['system']['polyallylamine_chain']['nmol'] = 5
combined_components['system']['glutaraldehyde_chain']['nmol'] = 5

# Write combined components to all directories
import yaml
for path in [path_min, path_eq, path_prod]:
    with open(os.path.join(path, 'components.yaml'), 'w') as f:
        yaml.dump(combined_components, f, sort_keys=False)

print(f"Setup complete for Case B: 50% Polyallylamine + 50% Glutaraldehyde")
print(f"Box size: {L} nm")
print(f"Total simulation time: {simulation_time_ns} ns")
print(f"Equilibration time: {equil_steps/1e5} ns")
print(f"Number of polyallylamine chains: 5")
print(f"Number of glutaraldehyde chains: 5")
print(f"Monomers per chain: 50")
print(f"\nTo run simulations:")
print(f"1. Minimization: python {path_min}/run.py --path {path_min}")
print(f"2. Equilibration: python {path_eq}/run.py --path {path_eq}")
print(f"3. Production: python {path_prod}/run.py --path {path_prod}")
