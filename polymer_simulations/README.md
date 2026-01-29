# Polymer Simulations with CALVADOS

This directory contains setup and analysis scripts for simulating polyallylamine and glutaraldehyde polymer systems using the CALVADOS coarse-grained force field.

## Overview

The simulations consist of two cases:
- **Case A**: 100% polyallylamine chains in a 5 nm cubic box
- **Case B**: 50% polyallylamine + 50% glutaraldehyde chains in a 5 nm cubic box

Each case includes:
1. Energy minimization
2. 1 ns equilibration
3. 100 ns production simulation
4. Crosslinking analysis (Case B only)

## Installation

### Prerequisites

- Python 3.10 (recommended; Python 3.12 may have compatibility issues with some dependencies)
- Conda or pip package manager

### Setting up the environment

#### Option 1: Using Conda (Recommended)

```bash
# Create and activate conda environment
conda create -n calvados python=3.10
conda activate calvados

# Install OpenMM (required for GPU support)
conda install -c conda-forge openmm=8.2.0

# For GPU support (optional):
# conda install -c conda-forge openmm=8.2.0 cudatoolkit=11.8

# Install CALVADOS and dependencies
cd /path/to/CALVADOS_poly
pip install -e .
```

#### Option 2: Using pip only

```bash
# Create virtual environment
python3.10 -m venv calvados_env
source calvados_env/bin/activate

# Install CALVADOS and dependencies
cd /path/to/CALVADOS_poly
pip install -e .
```

### Verifying Installation

```bash
python -c "import calvados; import openmm; print('Installation successful!')"
```

## Directory Structure

```
polymer_simulations/
├── input/
│   ├── polymer_residues.csv      # Residue definitions for PAA and GTA
│   ├── polyallylamine.fasta      # Polyallylamine sequence
│   └── glutaraldehyde.fasta      # Glutaraldehyde sequence
├── case_a/
│   ├── prepare.py                # Setup script for Case A
│   ├── minimization/             # Created by prepare.py
│   ├── equilibration/            # Created by prepare.py
│   └── production/               # Created by prepare.py
├── case_b/
│   ├── prepare.py                # Setup script for Case B
│   ├── minimization/             # Created by prepare.py
│   ├── equilibration/            # Created by prepare.py
│   └── production/               # Created by prepare.py
├── analysis/
│   └── analyze_crosslinking.py   # Crosslinking analysis script
├── run_all.py                    # Main execution script
└── README.md                     # This file
```

## Usage

### Quick Start - Run Everything

To set up and run all simulations:

```bash
cd polymer_simulations
python run_all.py
```

This will:
1. Set up both Case A and Case B
2. Run minimization, equilibration, and production for both cases
3. Analyze crosslinking for Case B

### Running Individual Cases

**Case A only:**
```bash
python run_all.py --case a
```

**Case B only:**
```bash
python run_all.py --case b
```

### Running Specific Phases

**Setup only (no simulation):**
```bash
python run_all.py --setup-only
```

**Skip certain phases:**
```bash
python run_all.py --skip-minimization
python run_all.py --skip-equilibration
python run_all.py --skip-production
```

### Manual Execution

You can also run simulations manually:

```bash
# Setup Case A
cd case_a
python prepare.py

# Run minimization
python minimization/run.py --path minimization

# Run equilibration
python equilibration/run.py --path equilibration

# Run production
python production/run.py --path production
```

### Crosslinking Analysis

To analyze crosslinking in Case B (after production run completes):

```bash
python run_all.py --analyze-only
```

Or manually:

```bash
cd analysis
python analyze_crosslinking.py \
    --traj ../case_b/production/case_b_mixed_prod.dcd \
    --top ../case_b/production/case_b_mixed_prod.pdb \
    --cutoff 0.6 \
    --output ../case_b/production/crosslinking_analysis
```

This generates:
- `crosslinking_analysis_contacts.png` - Time series of contacts
- `crosslinking_analysis_contact_histogram.png` - Distribution of contacts
- `crosslinking_analysis_summary.txt` - Summary statistics

## System Parameters

### Simulation Box
- Size: 5 nm × 5 nm × 5 nm cubic box
- Periodic boundary conditions: enabled

### Polymer Chains
- Polyallylamine (PAA): 50 monomers per chain
- Glutaraldehyde (GTA): 50 monomers per chain
- Case A: 10 PAA chains
- Case B: 5 PAA chains + 5 GTA chains

### Simulation Parameters
- Temperature: 293.15 K (20°C)
- Ionic strength: 0.15 M
- pH: 7.0
- Timestep: 10 fs
- Minimization: 1000 steps
- Equilibration: 1 ns (100,000 steps)
- Production: 100 ns (10,000,000 steps)
- Output frequency: 1000 steps (10 ps)

### Force Field Parameters

Residue definitions in `input/polymer_residues.csv`:

| Residue | MW (g/mol) | λ (hydrophobicity) | σ (nm) | q (charge) | Bond length (nm) |
|---------|------------|-------------------|--------|------------|-----------------|
| PAA     | 73.14      | 0.4               | 0.55   | +1         | 0.38           |
| GTA     | 100.12     | 0.3               | 0.50   | 0          | 0.38           |

## Output Files

Each simulation phase generates:
- `*.pdb` - Initial structure
- `*.dcd` - Trajectory file
- `*.log` - Simulation log
- `*.chk` - Checkpoint file (for restarts)
- `config.yaml` - Configuration file
- `components.yaml` - Component definitions

## Analysis Results

The crosslinking analysis provides:
1. **Mean number of contacts** between PAA and GTA chains
2. **Contact fraction** (percentage of possible contacts formed)
3. **Time series** showing evolution of crosslinking
4. **Distribution** of contact counts

A contact is defined as any PAA-GTA atom pair within 0.6 nm (adjustable).

## Customization

### Changing Box Size

Edit the `L` variable in `prepare.py`:
```python
L = 5.0  # nm (change to desired size)
```

### Changing Simulation Time

Edit the `simulation_time_ns` variable:
```python
simulation_time_ns = 100  # ns (change to desired time)
```

### Changing Number of Chains

Edit the `nmol` parameter in `prepare.py`:
```python
nmol = 10,  # number of chains
```

### Changing Polymer Length

Edit the FASTA files in `input/`:
- Add or remove `P` characters for polyallylamine
- Add or remove `G` characters for glutaraldehyde

### Modifying Force Field Parameters

Edit `input/polymer_residues.csv` to adjust:
- Hydrophobicity (lambdas)
- Size (sigmas)
- Charge (q)
- Bond length

## Troubleshooting

### OpenMM Import Error
```
ImportError: No module named 'openmm'
```
**Solution**: Install OpenMM via conda:
```bash
conda install -c conda-forge openmm=8.2.0
```

### Memory Issues
If simulations run out of memory, try:
- Reducing box size
- Reducing number of chains
- Using GPU platform instead of CPU

### GPU Support
To use GPU acceleration, edit `platform = 'CPU'` to `platform = 'CUDA'` in prepare.py files.

### Simulation Too Slow
For faster simulations:
1. Use GPU platform (if available)
2. Increase output frequency (`N_save`)
3. Reduce simulation time initially for testing

## Performance Notes

Approximate simulation times (CPU-only, varies by hardware):
- Minimization: ~1-5 minutes
- Equilibration (1 ns): ~10-30 minutes
- Production (100 ns): ~10-50 hours

GPU acceleration can provide 10-50x speedup depending on the GPU.

## References

CALVADOS force field:
- Tesei et al., PNAS (2021), 118(44):e2111696118
- Tesei & Lindorff-Larsen, Open Research Europe (2022), 2(94)
- Cao et al., Protein Science (2024), 33(11):e5172

## Support

For CALVADOS-specific issues, see:
- GitHub: https://github.com/KULL-Centre/CALVADOS
- Documentation: https://calvados.readthedocs.io/

For simulation setup issues in this repository, please open an issue on the GitHub repository.
