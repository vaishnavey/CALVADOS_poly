# Installation Guide for CALVADOS Polymer Simulations

## System Requirements

- **Operating System**: Linux or macOS (Windows via WSL2)
- **Python**: 3.10 (recommended) or 3.11
- **RAM**: Minimum 4 GB, 8+ GB recommended
- **Disk Space**: ~2 GB for installation, additional space for simulation outputs

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/vaishnavey/CALVADOS_poly.git
cd CALVADOS_poly
```

### Step 2: Install Dependencies

#### Option A: Conda (Recommended)

Conda provides the best compatibility, especially for OpenMM with GPU support.

```bash
# Create conda environment with Python 3.10
conda create -n calvados python=3.10
conda activate calvados

# Install OpenMM via conda-forge (required)
conda install -c conda-forge openmm=8.2.0

# For GPU support (optional, if you have CUDA-capable GPU):
# conda install -c conda-forge openmm=8.2.0 cudatoolkit=11.8

# Install CALVADOS and remaining dependencies
pip install -e .
```

#### Option B: pip only

If you don't have conda, you can use pip (but OpenMM GPU support may be limited):

```bash
# Create virtual environment
python3.10 -m venv calvados_env
source calvados_env/bin/activate  # On Windows: calvados_env\Scripts\activate

# Install CALVADOS and all dependencies
pip install -e .
```

### Step 3: Verify Installation

```bash
# Check if all dependencies are installed
python check_dependencies.py
```

Expected output:
```
✓ OpenMM is installed
✓ numpy is installed
✓ pandas is installed
...
✓ All dependencies are installed!
```

### Step 4: Test Basic Functionality

```bash
# Test that CALVADOS can be imported
python -c "import calvados; print('CALVADOS imported successfully!')"

# Test that OpenMM works
python -c "import openmm; print('OpenMM version:', openmm.version.version)"
```

## Troubleshooting

### Issue: "No module named 'openmm'"

**Solution**: Install OpenMM via conda:
```bash
conda install -c conda-forge openmm=8.2.0
```

### Issue: "No module named 'calvados'"

**Solution**: Make sure you're in the repository root and run:
```bash
pip install -e .
```

### Issue: Python version incompatibility

Some dependencies may not work with Python 3.12+. Use Python 3.10:
```bash
conda create -n calvados python=3.10
conda activate calvados
```

### Issue: OpenMM GPU not working

**Check CUDA availability**:
```python
import openmm
platform = openmm.Platform.getPlatformByName('CUDA')
print("CUDA available:", platform is not None)
```

If CUDA is not available:
- Verify you have an NVIDIA GPU
- Check CUDA installation: `nvidia-smi`
- Reinstall OpenMM with CUDA support via conda

### Issue: Installation fails with "wheel" errors

**Solution**: Upgrade pip and setuptools:
```bash
pip install --upgrade pip setuptools wheel
pip install -e .
```

### Issue: "localcider" installation fails

**Solution**: Install dependencies first:
```bash
pip install numpy scipy matplotlib
pip install localcider
```

## Verifying GPU Support (Optional)

If you installed OpenMM with GPU support, verify it works:

```python
import openmm

# List available platforms
print("Available platforms:")
for i in range(openmm.Platform.getNumPlatforms()):
    platform = openmm.Platform.getPlatform(i)
    print(f"  {i}: {platform.getName()}")

# Try to get CUDA platform
try:
    cuda = openmm.Platform.getPlatformByName('CUDA')
    print("\n✓ CUDA platform is available!")
    print(f"  Number of devices: {cuda.getPropertyDefaultValue('DeviceIndex')}")
except:
    print("\n✗ CUDA platform not available - using CPU")
```

## Environment Management

### Activate environment before each session

**Conda**:
```bash
conda activate calvados
```

**venv**:
```bash
source calvados_env/bin/activate  # Linux/Mac
calvados_env\Scripts\activate     # Windows
```

### Deactivate when done

**Conda**:
```bash
conda deactivate
```

**venv**:
```bash
deactivate
```

## Next Steps

After successful installation:

1. **Check the polymer simulation setup**:
   ```bash
   cd polymer_simulations
   cat README.md
   ```

2. **Test the setup scripts** (doesn't run simulations):
   ```bash
   python run_all.py --setup-only
   ```

3. **Read the documentation**:
   - `polymer_simulations/README.md` - Detailed simulation guide
   - `README.polymer.md` - Overview of polymer simulations

4. **Run simulations** (see polymer_simulations/README.md for details)

## Uninstalling

To remove the environment:

**Conda**:
```bash
conda deactivate
conda env remove -n calvados
```

**venv**:
```bash
deactivate
rm -rf calvados_env
```

## Getting Help

- **Check dependency status**: `python check_dependencies.py`
- **OpenMM documentation**: http://docs.openmm.org/
- **CALVADOS documentation**: https://calvados.readthedocs.io/
- **GitHub Issues**: https://github.com/vaishnavey/CALVADOS_poly/issues

## Hardware Recommendations

### Minimum (CPU-only)
- 4 CPU cores
- 4 GB RAM
- 10 GB disk space
- Time per 100 ns simulation: 10-50 hours

### Recommended (GPU)
- 4+ CPU cores
- 8+ GB RAM
- NVIDIA GPU with CUDA support
- 20 GB disk space
- Time per 100 ns simulation: 1-5 hours

### For Production Use
- 8+ CPU cores or GPU
- 16+ GB RAM
- 50+ GB disk space
- Consider HPC cluster for multiple long simulations
