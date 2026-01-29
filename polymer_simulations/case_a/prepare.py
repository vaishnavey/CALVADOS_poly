#!/usr/bin/env python3
"""
Setup script for Case A: 100% Polyallylamine System
Simulates a 5 nm cubic box with polyallylamine chains
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
sysname = 'case_a_polyallylamine'

# Set the side length of the cubic box (5 nm = 50 Angstroms)
L = 5.0  # nm

# Simulation parameters for 100 ns
# With timestep of 10 fs, 100 ns = 10^7 steps
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

# Define components - polyallylamine chains
# Create 10 chains of 50 monomers each for reasonable density
components = Components(
    molecule_type = 'protein',  # treat as protein-like polymer
    nmol = 10,  # 10 chains
    restraint = False,
    charge_termini = 'both',
    periodic = True,
    
    # INPUT
    fresidues = residues_file,
    ffasta = os.path.join(input_dir, 'polyallylamine.fasta'),
)

components.add(name='polyallylamine_chain')

# Write components file to all directories
components.write(path_min, name='components.yaml')
components.write(path_eq, name='components.yaml')
components.write(path_prod, name='components.yaml')

print(f"Setup complete for Case A: 100% Polyallylamine")
print(f"Box size: {L} nm")
print(f"Total simulation time: {simulation_time_ns} ns")
print(f"Equilibration time: {equil_steps/1e5} ns")
print(f"Number of chains: 10")
print(f"Monomers per chain: 50")
print(f"\nTo run simulations:")
print(f"1. Minimization: python {path_min}/run.py --path {path_min}")
print(f"2. Equilibration: python {path_eq}/run.py --path {path_eq}")
print(f"3. Production: python {path_prod}/run.py --path {path_prod}")
