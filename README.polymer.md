# CALVADOS Polymer Simulations

This repository extends the CALVADOS coarse-grained force field to simulate polymer systems, specifically for studying polyallylamine and glutaraldehyde crosslinking dynamics.

## Project Overview

**Goal**: Simulate and analyze crosslinking behavior between polyallylamine (PAA) and glutaraldehyde (GTA) polymers in a coarse-grained framework.

**Simulation Cases**:
1. **Case A**: 100% polyallylamine system (baseline/control)
2. **Case B**: 50% polyallylamine + 50% glutaraldehyde (crosslinking study)

**Simulation Protocol**:
- Box size: 5 nm × 5 nm × 5 nm
- Energy minimization (1000 steps)
- Equilibration (1 ns)
- Production simulation (100 ns)
- Crosslinking analysis

## Quick Start

See [polymer_simulations/README.md](polymer_simulations/README.md) for detailed instructions.

```bash
# 1. Install CALVADOS
conda create -n calvados python=3.10
conda activate calvados
conda install -c conda-forge openmm=8.2.0
pip install -e .

# 2. Run simulations
cd polymer_simulations
python run_all.py

# 3. View results
# Trajectories and analysis in case_a/ and case_b/ subdirectories
```

## Repository Structure

```
CALVADOS_poly/
├── calvados/                    # CALVADOS force field code
├── polymer_simulations/         # Polymer simulation setup
│   ├── input/                   # Polymer definitions
│   │   ├── polymer_residues.csv # PAA and GTA parameters
│   │   ├── polyallylamine.fasta # PAA sequence
│   │   └── glutaraldehyde.fasta # GTA sequence
│   ├── case_a/                  # 100% PAA system
│   │   └── prepare.py           # Setup script
│   ├── case_b/                  # 50/50 PAA/GTA system
│   │   └── prepare.py           # Setup script
│   ├── analysis/                # Analysis tools
│   │   └── analyze_crosslinking.py
│   ├── run_all.py              # Main execution script
│   └── README.md               # Detailed documentation
├── examples/                    # Original CALVADOS examples
├── tests/                       # Test suite
└── README.md                    # This file (CALVADOS overview)
```

## Polymer Definitions

### Polyallylamine (PAA)
- Molecular weight: 73.14 g/mol per monomer
- Charge: +1 (positively charged amine group)
- Hydrophobicity (λ): 0.4
- Size (σ): 0.55 nm

### Glutaraldehyde (GTA)
- Molecular weight: 100.12 g/mol per monomer
- Charge: 0 (neutral aldehyde)
- Hydrophobicity (λ): 0.3
- Size (σ): 0.50 nm

Both polymers are modeled as chains of 50 monomers.

## Simulation Details

### System Composition

**Case A (100% PAA)**:
- 10 polyallylamine chains
- 50 monomers per chain
- Total: 500 PAA monomers

**Case B (50/50 PAA/GTA)**:
- 5 polyallylamine chains
- 5 glutaraldehyde chains
- 50 monomers per chain
- Total: 250 PAA + 250 GTA monomers

### Simulation Parameters

- **Temperature**: 293.15 K (20°C)
- **Ionic strength**: 0.15 M
- **pH**: 7.0
- **Timestep**: 10 fs
- **Box**: 5 nm cubic with periodic boundaries
- **Platform**: CPU (can be changed to CUDA for GPU)

### Simulation Phases

1. **Minimization**: 1000 steps to remove bad contacts
2. **Equilibration**: 1 ns (100,000 steps) to relax the system
3. **Production**: 100 ns (10,000,000 steps) for analysis
4. **Output frequency**: Every 10 ps (1000 steps)

## Analysis

### Crosslinking Analysis (Case B)

The `analyze_crosslinking.py` script quantifies interactions between PAA and GTA chains:

- **Contact definition**: PAA-GTA atom pairs within 0.6 nm
- **Metrics**:
  - Mean number of contacts
  - Contact fraction (% of possible contacts)
  - Time evolution of crosslinking
  - Distribution of contact counts

**Output files**:
- `crosslinking_analysis_contacts.png` - Time series plots
- `crosslinking_analysis_contact_histogram.png` - Distribution
- `crosslinking_analysis_summary.txt` - Statistical summary

### Expected Results

The analysis will reveal:
1. Extent of crosslinking between PAA and GTA
2. Temporal dynamics of crosslink formation
3. Equilibrium crosslinking density
4. Spatial distribution of crosslinks

## Usage Examples

### Run everything at once
```bash
cd polymer_simulations
python run_all.py
```

### Run specific case
```bash
python run_all.py --case a  # Only Case A
python run_all.py --case b  # Only Case B
```

### Run specific phases
```bash
python run_all.py --setup-only              # Setup only
python run_all.py --skip-minimization       # Skip minimization
python run_all.py --skip-production         # Quick test run
```

### Run analysis only
```bash
python run_all.py --analyze-only  # Analyze existing Case B trajectory
```

### Manual control
```bash
# Setup
cd case_a
python prepare.py

# Run phases individually
python minimization/run.py --path minimization
python equilibration/run.py --path equilibration
python production/run.py --path production
```

## Performance

**CPU-only** (approximate, varies by hardware):
- Minimization: 1-5 minutes
- Equilibration (1 ns): 10-30 minutes
- Production (100 ns): 10-50 hours per case

**GPU** (CUDA platform):
- 10-50x faster depending on GPU

For faster testing, reduce simulation time in prepare.py:
```python
simulation_time_ns = 10  # Instead of 100
```

## Customization

### Modify polymer length
Edit FASTA files in `polymer_simulations/input/`:
```
>polyallylamine_chain
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```
Add or remove P/G characters for desired length.

### Modify force field parameters
Edit `polymer_simulations/input/polymer_residues.csv`:
```csv
one,three,MW,lambdas,sigmas,q,bondlength
P,PAA,73.14,0.4,0.55,1,0.38
G,GTA,100.12,0.3,0.50,0,0.38
```

### Modify simulation parameters
Edit prepare.py scripts:
```python
L = 5.0  # Box size (nm)
simulation_time_ns = 100  # Simulation time
N_save = 1000  # Output frequency
```

## Troubleshooting

### Installation issues
```bash
# If OpenMM fails to import
conda install -c conda-forge openmm=8.2.0

# If dependencies fail
pip install --upgrade pip
pip install -e .
```

### Memory issues
- Reduce box size: `L = 4.0` instead of `5.0`
- Reduce number of chains
- Increase output frequency: `N_save = 5000`

### Slow simulations
- Use GPU: Change `platform = 'CUDA'` in prepare.py
- Reduce simulation time for testing
- Run on HPC cluster if available

### Analysis fails
Check that trajectory files exist:
```bash
ls case_b/production/*.dcd
ls case_b/production/*.pdb
```

## Scientific Background

### CALVADOS Force Field

CALVADOS is a coarse-grained force field originally designed for intrinsically disordered proteins (IDPs). Each residue is represented by a single bead, with interactions based on:

- **Electrostatics**: Debye-Hückel potential
- **Hydrophobic**: λ-dependent attraction
- **Excluded volume**: Lennard-Jones repulsion
- **Bonded**: Harmonic bonds between consecutive residues

### Polymer Adaptation

For polymer simulations, we:
1. Define custom residue types (PAA, GTA)
2. Represent polymers as linear chains
3. Use protein-like topology for bonding
4. Analyze crosslinking through inter-chain contacts

### Crosslinking Mechanism

In polymer chemistry, glutaraldehyde acts as a crosslinker:
- Two aldehyde groups can form covalent bonds
- Reacts with amine groups (PAA)
- Creates three-dimensional networks

Our coarse-grained model captures:
- Spatial proximity (contact analysis)
- Dynamic formation/breaking
- Equilibrium crosslink density

Note: Explicit covalent bonds are not modeled; crosslinking is inferred from persistent contacts.

## References

### CALVADOS
- Tesei et al., PNAS (2021) - Original CALVADOS model
- Tesei & Lindorff-Larsen, Open Research Europe (2022) - CALVADOS2
- Cao et al., Protein Science (2024) - Multi-domain extensions

### Polymer Chemistry
- Polyallylamine: Common polycation used in layer-by-layer assembly
- Glutaraldehyde: Bifunctional crosslinker widely used in bioconjugation

## Support

- **CALVADOS documentation**: https://calvados.readthedocs.io/
- **CALVADOS GitHub**: https://github.com/KULL-Centre/CALVADOS
- **Issues**: Open an issue on this repository

## License

This project uses CALVADOS which is licensed under GNU GPL3. See LICENSE file for details.
