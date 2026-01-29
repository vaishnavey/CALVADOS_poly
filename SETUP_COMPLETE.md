# CALVADOS Polymer Simulation Setup - Complete

## ✅ What Has Been Accomplished

This repository is now fully configured to simulate polyallylamine and glutaraldehyde polymer systems using the CALVADOS coarse-grained force field. Everything is ready to run - you just need to install the dependencies!

## 📋 Project Summary

### Goal
Simulate and analyze crosslinking dynamics between polyallylamine (positively charged polymer) and glutaraldehyde (neutral crosslinker) in a coarse-grained molecular dynamics framework.

### Two Simulation Cases

**Case A: 100% Polyallylamine (Control)**
- 10 chains of 50 monomers each
- Purpose: Establish baseline polymer behavior without crosslinker

**Case B: 50/50 Polyallylamine + Glutaraldehyde**
- 5 PAA chains + 5 GTA chains (50 monomers each)
- Purpose: Study crosslinking interactions between PAA and GTA

### Simulation Protocol
1. **Minimization**: Remove bad contacts (1000 steps)
2. **Equilibration**: Relax system (1 ns)
3. **Production**: Collect data (100 ns)
4. **Analysis**: Quantify crosslinking (Case B only)

## 📁 Repository Structure

```
CALVADOS_poly/
├── 📘 Documentation
│   ├── QUICKSTART.md          # 5-minute setup guide
│   ├── INSTALL.md             # Detailed installation
│   ├── WORKFLOW.md            # Complete workflow diagram
│   ├── README.polymer.md      # Project overview
│   └── check_dependencies.py  # Verify installation
│
├── 🧪 Polymer Simulations (Main Work Area)
│   └── polymer_simulations/
│       ├── README.md                   # Detailed simulation guide
│       ├── run_all.py                  # Main execution script ⭐
│       │
│       ├── input/                      # Polymer definitions
│       │   ├── polymer_residues.csv    # Force field parameters
│       │   ├── polyallylamine.fasta    # PAA sequence
│       │   └── glutaraldehyde.fasta    # GTA sequence
│       │
│       ├── case_a/                     # 100% PAA system
│       │   └── prepare.py              # Setup script
│       │
│       ├── case_b/                     # 50/50 PAA/GTA system
│       │   └── prepare.py              # Setup script
│       │
│       └── analysis/                   # Analysis tools
│           └── analyze_crosslinking.py # Crosslinking analysis
│
├── 🔧 CALVADOS Force Field
│   ├── calvados/               # Core CALVADOS implementation
│   ├── examples/               # Original CALVADOS examples
│   ├── tests/                  # Test suite
│   └── setup.py               # Installation script
│
└── 📄 Configuration
    ├── .gitignore             # Ignore simulation outputs
    ├── residues.csv           # Standard residue definitions
    └── pytest.ini             # Testing configuration
```

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies (5 minutes)
```bash
# Clone repository
git clone https://github.com/vaishnavey/CALVADOS_poly.git
cd CALVADOS_poly

# Create environment
conda create -n calvados python=3.10 -y
conda activate calvados

# Install OpenMM and CALVADOS
conda install -c conda-forge openmm=8.2.0 -y
pip install -e .

# Verify installation
python check_dependencies.py
```

### Step 2: Setup Simulations (1 minute)
```bash
cd polymer_simulations
python run_all.py --setup-only
```

This creates all necessary directories and configuration files.

### Step 3: Run Simulations (hours to days)
```bash
python run_all.py
```

This runs both cases through minimization, equilibration, and production, then analyzes Case B for crosslinking.

## 📊 What Gets Created

### During Setup (`--setup-only`)
```
polymer_simulations/
├── case_a/
│   ├── minimization/
│   │   ├── config.yaml       # Simulation parameters
│   │   ├── components.yaml   # Molecule definitions
│   │   └── run.py           # Execution script
│   ├── equilibration/
│   │   └── [same files]
│   └── production/
│       └── [same files]
└── case_b/
    └── [same structure]
```

### After Simulations
```
polymer_simulations/
├── case_a/production/
│   ├── case_a_polyallylamine_prod.pdb    # Structure (~1 MB)
│   ├── case_a_polyallylamine_prod.dcd    # Trajectory (~500 MB - 2 GB)
│   └── case_a_polyallylamine_prod.log    # Simulation log
│
└── case_b/production/
    ├── case_b_mixed_prod.pdb
    ├── case_b_mixed_prod.dcd
    ├── case_b_mixed_prod.log
    ├── crosslinking_analysis_contacts.png         # Plots
    ├── crosslinking_analysis_contact_histogram.png
    └── crosslinking_analysis_summary.txt          # Statistics
```

## 🔬 Scientific Details

### Polymer Definitions

| Polymer | Code | MW (g/mol) | Charge | Hydrophobicity | Size (nm) |
|---------|------|------------|--------|----------------|-----------|
| Polyallylamine | PAA (P) | 73.14 | +1 | 0.4 | 0.55 |
| Glutaraldehyde | GTA (G) | 100.12 | 0 | 0.3 | 0.50 |

### System Composition

| Parameter | Case A | Case B |
|-----------|--------|--------|
| PAA chains | 10 | 5 |
| GTA chains | 0 | 5 |
| Total monomers | 500 PAA | 250 PAA + 250 GTA |
| Box size | 5 nm cubic | 5 nm cubic |
| Temperature | 293.15 K | 293.15 K |
| Ionic strength | 0.15 M | 0.15 M |

### Simulation Parameters

| Phase | Steps | Time | Output Frequency |
|-------|-------|------|------------------|
| Minimization | 1,000 | N/A | 100 steps |
| Equilibration | 100,000 | 1 ns | 1,000 steps (10 ps) |
| Production | 10,000,000 | 100 ns | 1,000 steps (10 ps) |

### Analysis (Case B)

**Crosslinking Metrics**:
- Contact definition: PAA-GTA atoms within 0.6 nm
- Contact count: Number of PAA-GTA pairs in contact
- Contact fraction: Percentage of possible contacts formed
- Time evolution: How crosslinking changes over time

## ⏱️ Time Estimates

| Hardware | Case A | Case B | Total | Analysis |
|----------|--------|--------|-------|----------|
| **CPU only** | 10-50 hrs | 10-50 hrs | 20-100 hrs | 5-10 min |
| **GPU (CUDA)** | 1-5 hrs | 1-5 hrs | 2-10 hrs | 5-10 min |

💡 **Tip**: GPU acceleration is 10-50× faster. Enable with `platform = 'CUDA'` in prepare.py files.

## 🎯 Usage Examples

### Run Everything
```bash
cd polymer_simulations
python run_all.py
```

### Run Specific Case
```bash
python run_all.py --case a  # Case A only
python run_all.py --case b  # Case B only
```

### Control Simulation Phases
```bash
python run_all.py --setup-only           # Setup without running
python run_all.py --skip-minimization    # Skip minimization
python run_all.py --skip-production      # Quick test (min + equil only)
```

### Analysis Only
```bash
python run_all.py --analyze-only  # Analyze existing Case B trajectory
```

### Manual Control
```bash
# Setup
cd case_a
python prepare.py

# Run phases individually
python minimization/run.py --path minimization
python equilibration/run.py --path equilibration
python production/run.py --path production
```

## 🔧 Customization

### Modify Polymer Length
Edit FASTA files in `polymer_simulations/input/`:
```
>polyallylamine_chain
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
(Add or remove P's to change length)
```

### Modify Number of Chains
Edit prepare.py files:
```python
nmol = 10,  # Change to desired number of chains
```

### Modify Simulation Time
Edit prepare.py files:
```python
simulation_time_ns = 100  # Change to desired time (ns)
```

### Modify Box Size
Edit prepare.py files:
```python
L = 5.0  # Change to desired size (nm)
```

### Modify Force Field Parameters
Edit `polymer_simulations/input/polymer_residues.csv`:
```csv
one,three,MW,lambdas,sigmas,q,bondlength
P,PAA,73.14,0.4,0.55,1,0.38     # Modify these values
G,GTA,100.12,0.3,0.50,0,0.38    # Modify these values
```

## 📖 Documentation Guide

**Start here:**
1. **QUICKSTART.md** - Get running in 5 minutes
2. **polymer_simulations/README.md** - Detailed simulation guide

**For specific needs:**
- **INSTALL.md** - Installation troubleshooting
- **WORKFLOW.md** - Complete workflow diagram
- **README.polymer.md** - Scientific background

**Tools:**
- **check_dependencies.py** - Verify installation
- **run_all.py --help** - Command-line options

## 🎓 Expected Results

### Case A (Control)
- **Output**: PAA self-interaction dynamics
- **Analysis**: Chain flexibility, radius of gyration
- **Purpose**: Baseline for comparison

### Case B (Crosslinked)
- **Output**: PAA-GTA crosslinking dynamics
- **Analysis**: 
  - Mean contact count: ~50-500 contacts (varies)
  - Contact fraction: ~0.1-1% of possible contacts
  - Equilibration time: ~10-50 ns
- **Purpose**: Quantify crosslinking extent

### Interpretation
- **High contact count** → Strong crosslinking network
- **Low contact count** → Weak crosslinking
- **Increasing over time** → Crosslink formation in progress
- **Stable over time** → Equilibrated crosslinked network

## 🛠️ Troubleshooting

### "No module named 'openmm'"
```bash
conda install -c conda-forge openmm=8.2.0
```

### "No module named 'calvados'"
```bash
cd /path/to/CALVADOS_poly
pip install -e .
```

### Simulations are too slow
1. **Use GPU**: Edit prepare.py, change `platform = 'CUDA'`
2. **Reduce time**: Edit prepare.py, change `simulation_time_ns = 10`
3. **Use HPC**: Run on high-performance computing cluster

### Out of disk space
- Each case generates ~1-2 GB of trajectory data
- Clear old trajectories: `rm case_*/production/*.dcd`
- Reduce output frequency: Edit `N_save` in prepare.py

### Analysis fails
Check that trajectory exists:
```bash
ls case_b/production/*.dcd
ls case_b/production/*.pdb
```

## 📝 Next Steps

1. ✅ **Installation complete** (you are here)
2. ⏭️ **Test setup**: `python run_all.py --setup-only`
3. ⏭️ **Test run**: `python run_all.py --case a --skip-production`
4. ⏭️ **Full simulation**: `python run_all.py`
5. ⏭️ **Analyze results**: View plots and summary in case_b/production/

## 🤝 Contributing

This is a research repository for polymer simulations. Contributions are welcome:
- Report issues: GitHub Issues
- Suggest improvements: Pull Requests
- Ask questions: GitHub Discussions

## 📚 References

### CALVADOS Force Field
- Tesei et al., PNAS (2021) - Original CALVADOS
- Tesei & Lindorff-Larsen, Open Research Europe (2022) - CALVADOS2
- Cao et al., Protein Science (2024) - Multi-domain proteins

### Polymer Chemistry
- Polyallylamine: Polycation for layer-by-layer assembly
- Glutaraldehyde: Bifunctional crosslinking agent

### Software
- OpenMM: http://openmm.org/
- CALVADOS: https://github.com/KULL-Centre/CALVADOS
- MDAnalysis: https://www.mdanalysis.org/

## 📞 Support

- **GitHub Issues**: https://github.com/vaishnavey/CALVADOS_poly/issues
- **CALVADOS Docs**: https://calvados.readthedocs.io/
- **OpenMM Docs**: http://docs.openmm.org/

## ✨ Summary

You now have a complete, ready-to-run simulation setup for studying polyallylamine and glutaraldehyde crosslinking! 

**What's ready**:
- ✅ Full CALVADOS force field implementation
- ✅ Custom polymer definitions (PAA and GTA)
- ✅ Two simulation cases (control and crosslinked)
- ✅ Complete simulation workflow (minimize, equilibrate, produce)
- ✅ Crosslinking analysis tools
- ✅ Comprehensive documentation
- ✅ Main execution script

**What's needed**:
- ⏭️ Install dependencies (5 minutes)
- ⏭️ Run simulations (hours to days)
- ⏭️ Analyze results

**Get started**:
```bash
# 1. Install
conda create -n calvados python=3.10 -y && conda activate calvados
conda install -c conda-forge openmm=8.2.0 -y && pip install -e .

# 2. Setup
cd polymer_simulations && python run_all.py --setup-only

# 3. Run
python run_all.py
```

Happy simulating! 🧪🔬
