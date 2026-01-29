# Quick Start Guide - CALVADOS Polymer Simulations

This guide will help you run polyallylamine and glutaraldehyde simulations in 5 minutes (setup only - actual simulations take longer).

## Prerequisites

Before starting, make sure you have:
- [ ] Git installed
- [ ] Python 3.10 installed
- [ ] Conda (recommended) or pip

## 5-Minute Setup

### 1. Clone and Enter Repository (30 seconds)

```bash
git clone https://github.com/vaishnavey/CALVADOS_poly.git
cd CALVADOS_poly
```

### 2. Create Environment (2 minutes)

```bash
# Using conda (recommended)
conda create -n calvados python=3.10 -y
conda activate calvados
conda install -c conda-forge openmm=8.2.0 -y
```

### 3. Install CALVADOS (2 minutes)

```bash
pip install -e .
```

### 4. Verify Installation (30 seconds)

```bash
python check_dependencies.py
```

You should see all green checkmarks (✓).

### 5. Test Setup Scripts (1 minute)

```bash
cd polymer_simulations
python run_all.py --setup-only
```

This creates the simulation directories without running the actual simulations.

## What Was Created?

```
polymer_simulations/
├── case_a/                    # 100% polyallylamine
│   ├── minimization/          # Energy minimization setup
│   ├── equilibration/         # 1 ns equilibration setup
│   └── production/            # 100 ns production setup
└── case_b/                    # 50/50 polyallylamine/glutaraldehyde
    ├── minimization/
    ├── equilibration/
    └── production/
```

Each directory contains:
- `config.yaml` - Simulation parameters
- `components.yaml` - Molecule definitions
- `run.py` - Execution script

## Running Simulations

### Quick Test Run (5-10 minutes)

To test that everything works, run just the minimization:

```bash
# Run Case A minimization only
cd case_a/minimization
python run.py --path .
```

This should complete in a few minutes.

### Full Simulation (10-50 hours per case)

To run complete simulations (minimize, equilibrate, 100 ns production):

```bash
cd polymer_simulations
python run_all.py
```

**Warning**: This will take a long time on CPU (10-50 hours per case). Consider:
- Using GPU if available (see below)
- Running overnight
- Starting with just one case: `python run_all.py --case a`

### With GPU Acceleration (1-5 hours per case)

If you have a CUDA-capable GPU:

1. Install with GPU support:
```bash
conda install -c conda-forge openmm=8.2.0 cudatoolkit=11.8
```

2. Edit prepare.py files to use CUDA:
```python
# Change this line in case_a/prepare.py and case_b/prepare.py
platform = 'CUDA',  # was 'CPU'
```

3. Run simulations:
```bash
python run_all.py
```

## Viewing Results

After simulations complete, you'll have:

### Trajectory Files
- `*.dcd` - Molecular dynamics trajectory
- `*.pdb` - Initial structure

### Analysis (Case B only)
```bash
cd case_b/production
ls *crosslinking*
```

Output files:
- `crosslinking_analysis_contacts.png` - Contact time series
- `crosslinking_analysis_contact_histogram.png` - Distribution
- `crosslinking_analysis_summary.txt` - Statistics

## Common Commands

```bash
# Check what's installed
python check_dependencies.py

# Setup only (no simulation)
python run_all.py --setup-only

# Run specific case
python run_all.py --case a     # Only Case A
python run_all.py --case b     # Only Case B

# Skip certain phases
python run_all.py --skip-minimization
python run_all.py --skip-production

# Analyze existing results
python run_all.py --analyze-only
```

## File Locations

- **Setup scripts**: `polymer_simulations/case_*/prepare.py`
- **Simulation output**: `polymer_simulations/case_*/production/`
- **Analysis tools**: `polymer_simulations/analysis/`
- **Documentation**: 
  - `polymer_simulations/README.md` (detailed)
  - `README.polymer.md` (overview)
  - `INSTALL.md` (installation help)

## Troubleshooting

### "No module named 'openmm'"
```bash
conda install -c conda-forge openmm=8.2.0
```

### "No module named 'calvados'"
```bash
pip install -e .
```

### Simulation is too slow
- Use GPU (see above)
- Reduce simulation time for testing (edit prepare.py)
- Run on a more powerful computer

### Not enough disk space
Simulations generate ~1-2 GB of data per case. Make sure you have at least 5 GB free.

## Next Steps

1. **Read detailed documentation**:
   ```bash
   cat polymer_simulations/README.md
   ```

2. **Modify simulation parameters** (optional):
   - Edit `case_a/prepare.py` or `case_b/prepare.py`
   - Change box size, simulation time, number of chains, etc.

3. **Run simulations**:
   - Start with a test: `python run_all.py --case a --skip-production`
   - Then full run: `python run_all.py`

4. **Analyze results**:
   - Crosslinking analysis runs automatically for Case B
   - Create custom analysis using MDAnalysis

## Time Estimates

| Phase | CPU Time | GPU Time |
|-------|----------|----------|
| Setup | 1 min | 1 min |
| Minimization | 2-5 min | 1 min |
| Equilibration | 10-30 min | 2-5 min |
| Production (100 ns) | 10-50 hours | 1-5 hours |
| Analysis | 5-10 min | 5-10 min |
| **Total per case** | **10-50 hours** | **1-5 hours** |
| **Both cases** | **20-100 hours** | **2-10 hours** |

## Support

- **Issues**: https://github.com/vaishnavey/CALVADOS_poly/issues
- **CALVADOS Docs**: https://calvados.readthedocs.io/
- **OpenMM Docs**: http://docs.openmm.org/

## Summary

You've successfully set up CALVADOS polymer simulations! 

**What you can do now**:
- ✓ Setup scripts are ready
- ✓ Run test minimization
- ✓ Launch full simulations
- ✓ Analyze crosslinking

**Remember**:
- Full simulations take time (hours to days on CPU)
- GPU acceleration highly recommended
- Start with one case for testing
- Monitor disk space

Happy simulating! 🧪
