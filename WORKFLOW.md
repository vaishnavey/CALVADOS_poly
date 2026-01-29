# Simulation Workflow Summary

## Project Goal
Simulate polyallylamine and glutaraldehyde polymer systems to study crosslinking dynamics using the CALVADOS coarse-grained force field.

## Simulation Systems

### Case A: 100% Polyallylamine (Control)
- **Purpose**: Baseline behavior of polyallylamine without crosslinker
- **Composition**: 10 polyallylamine chains, 50 monomers each
- **Expected behavior**: Chain dynamics without inter-chain crosslinking

### Case B: 50% Polyallylamine + 50% Glutaraldehyde (Crosslinking Study)
- **Purpose**: Study crosslinking between polyallylamine and glutaraldehyde
- **Composition**: 5 PAA chains + 5 GTA chains, 50 monomers each
- **Expected behavior**: Formation of PAA-GTA contacts/crosslinks

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SIMULATION WORKFLOW                       │
└─────────────────────────────────────────────────────────────┘

1. SETUP PHASE
   │
   ├── Define Polymers
   │   ├── Polyallylamine (PAA): P residue
   │   │   • MW: 73.14 g/mol, Charge: +1
   │   │   • λ: 0.4, σ: 0.55 nm
   │   │
   │   └── Glutaraldehyde (GTA): G residue
   │       • MW: 100.12 g/mol, Charge: 0
   │       • λ: 0.3, σ: 0.50 nm
   │
   ├── Create FASTA Sequences
   │   ├── 50 P's for PAA chain
   │   └── 50 G's for GTA chain
   │
   └── Run prepare.py
       ├── Case A: 10 PAA chains
       └── Case B: 5 PAA + 5 GTA chains
       
       ↓

2. MINIMIZATION PHASE (~1-5 minutes)
   │
   ├── Remove bad contacts
   ├── 1000 minimization steps
   └── Output: minimized structure
   
       ↓

3. EQUILIBRATION PHASE (~10-30 minutes CPU, 2-5 min GPU)
   │
   ├── Heat system to 293.15 K
   ├── 1 ns simulation (100,000 steps)
   └── Output: equilibrated trajectory
   
       ↓

4. PRODUCTION PHASE (~10-50 hours CPU, 1-5 hours GPU)
   │
   ├── 100 ns simulation (10,000,000 steps)
   ├── Save every 10 ps (1000 steps)
   ├── Output: 10,000 frames
   └── Files: *.dcd trajectory, *.pdb structure
   
       ↓

5. ANALYSIS PHASE (~5-10 minutes)
   │
   └── Case B Only: Crosslinking Analysis
       ├── Calculate PAA-GTA contacts (< 0.6 nm)
       ├── Compute contact statistics
       ├── Generate time series plots
       └── Create summary report
       
       ↓

6. RESULTS
   │
   ├── Case A Results
   │   ├── PAA chain dynamics
   │   ├── Self-interaction behavior
   │   └── Baseline for comparison
   │
   └── Case B Results
       ├── Crosslinking extent
       ├── Contact formation dynamics
       ├── Spatial distribution
       └── Comparison with Case A
```

## Key Files and Directories

```
CALVADOS_poly/
│
├── check_dependencies.py          # Verify installation
├── INSTALL.md                      # Installation guide
├── QUICKSTART.md                   # Quick start guide
├── README.polymer.md               # Polymer project overview
│
├── polymer_simulations/            # Main simulation directory
│   │
│   ├── README.md                   # Detailed documentation
│   ├── run_all.py                  # Main execution script
│   │
│   ├── input/                      # Polymer definitions
│   │   ├── polymer_residues.csv    # Force field parameters
│   │   ├── polyallylamine.fasta    # PAA sequence (50 P's)
│   │   └── glutaraldehyde.fasta    # GTA sequence (50 G's)
│   │
│   ├── case_a/                     # 100% PAA system
│   │   ├── prepare.py              # Setup script
│   │   ├── minimization/           # Min phase (auto-generated)
│   │   ├── equilibration/          # Equil phase (auto-generated)
│   │   └── production/             # Prod phase (auto-generated)
│   │
│   ├── case_b/                     # 50/50 PAA/GTA system
│   │   ├── prepare.py              # Setup script
│   │   ├── minimization/           # Min phase (auto-generated)
│   │   ├── equilibration/          # Equil phase (auto-generated)
│   │   └── production/             # Prod phase (auto-generated)
│   │
│   └── analysis/                   # Analysis tools
│       └── analyze_crosslinking.py # Crosslinking analysis
│
├── calvados/                       # CALVADOS force field
└── examples/                       # Original CALVADOS examples
```

## Force Field Parameters

### CALVADOS Coarse-Grained Model

Each residue represented by single bead with:

| Parameter | Description | PAA Value | GTA Value |
|-----------|-------------|-----------|-----------|
| MW | Molecular weight (g/mol) | 73.14 | 100.12 |
| λ (lambda) | Hydrophobicity scale (0-1) | 0.4 | 0.3 |
| σ (sigma) | Bead size (nm) | 0.55 | 0.50 |
| q | Charge (e) | +1 | 0 |
| Bond length | Distance between beads (nm) | 0.38 | 0.38 |

### Interaction Potentials

1. **Electrostatics**: Debye-Hückel (screened Coulomb)
2. **Hydrophobic**: λ-dependent attractive interactions
3. **Excluded volume**: Lennard-Jones repulsion
4. **Bonded**: Harmonic potential between consecutive beads

## Running Simulations

### Complete Workflow
```bash
cd polymer_simulations
python run_all.py
```

### Step-by-Step
```bash
# 1. Setup
python run_all.py --setup-only

# 2. Run Case A
cd case_a/minimization && python run.py --path .
cd ../equilibration && python run.py --path .
cd ../production && python run.py --path .

# 3. Run Case B
cd ../../case_b/minimization && python run.py --path .
cd ../equilibration && python run.py --path .
cd ../production && python run.py --path .

# 4. Analyze Case B
cd ../../analysis
python analyze_crosslinking.py \
    --traj ../case_b/production/*.dcd \
    --top ../case_b/production/*.pdb \
    --output ../case_b/production/crosslinking
```

## Expected Outputs

### Simulation Outputs (per case)
- `*.pdb` - Initial structure (~1 MB)
- `*.dcd` - Trajectory (~500 MB - 2 GB)
- `*.log` - Simulation log (~1-10 MB)
- `*.chk` - Checkpoint for restart (~10 MB)

### Analysis Outputs (Case B)
- `crosslinking_analysis_contacts.png` - Time series
- `crosslinking_analysis_contact_histogram.png` - Distribution
- `crosslinking_analysis_summary.txt` - Statistics

## Analysis Metrics

### Crosslinking Quantification

1. **Contact Count**: Number of PAA-GTA atom pairs within 0.6 nm
2. **Contact Fraction**: Percentage of possible contacts formed
3. **Temporal Dynamics**: How contacts evolve over time
4. **Equilibrium Value**: Steady-state crosslinking density

### Expected Results

**Case A (Control)**:
- No inter-chain crosslinking (PAA-PAA only)
- Self-interaction dynamics
- Chain flexibility and radius of gyration

**Case B (Crosslinked)**:
- PAA-GTA contacts indicating crosslinks
- Network formation over time
- Comparison: Case B crosslinking > Case A self-interaction

## Performance Notes

| System | Steps | CPU Time | GPU Time |
|--------|-------|----------|----------|
| Minimization | 1,000 | 1-5 min | <1 min |
| Equilibration | 100,000 | 10-30 min | 2-5 min |
| Production | 10,000,000 | 10-50 hrs | 1-5 hrs |
| Analysis | N/A | 5-10 min | N/A |

**Total per case**: 10-50 hours (CPU) or 1-5 hours (GPU)
**Both cases**: 20-100 hours (CPU) or 2-10 hours (GPU)

## Customization Options

### Change Polymer Length
Edit FASTA files (add/remove P or G characters)

### Change Number of Chains
Edit `nmol` in prepare.py scripts

### Change Box Size
Edit `L` variable in prepare.py

### Change Simulation Time
Edit `simulation_time_ns` in prepare.py

### Change Force Field Parameters
Edit `polymer_residues.csv`

## Scientific Interpretation

### Crosslinking Analysis

- **High contact fraction** → Strong crosslinking
- **Low contact fraction** → Weak crosslinking
- **Increasing over time** → Crosslink formation
- **Stable over time** → Equilibrated network

### Comparison with Experiment

Simulation results can be compared to:
- Experimental crosslinking density (e.g., from gel analysis)
- Network formation kinetics
- Mechanical properties of crosslinked hydrogels

## References

1. CALVADOS force field papers (see main README.md)
2. Polyallylamine: Polycation for layer-by-layer assembly
3. Glutaraldehyde: Common bifunctional crosslinker

## Support and Documentation

- **Installation**: `INSTALL.md`
- **Quick start**: `QUICKSTART.md`
- **Detailed guide**: `polymer_simulations/README.md`
- **Overview**: `README.polymer.md`
- **Check dependencies**: `python check_dependencies.py`

## Contact

For issues or questions:
- GitHub Issues: https://github.com/vaishnavey/CALVADOS_poly/issues
- CALVADOS Documentation: https://calvados.readthedocs.io/
