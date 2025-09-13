# Fermi Fluids Introduction

A pure Python NumPy-based 2D incompressible fluid simulation with semi-Lagrangian advection, vorticity confinement, and Jacobi projection. This is a computational physics research project demonstrating fluid dynamics algorithms.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

- **CRITICAL**: Python 3.12.3 is required and available at `/usr/bin/python3`
- **CRITICAL**: pip3 is available at `/usr/bin/pip3` for package management
- Bootstrap and run the simulation:
  - `pip3 install numpy` -- takes 10-30 seconds. Install NumPy dependency (user installation)
  - `python3 fluid_langrangians.py` -- takes ~1 second. Runs complete fluid simulation
- Verify installation and code integrity:
  - `python3 -c "import numpy; print('NumPy version:', numpy.__version__)"` -- verify NumPy is available
  - `python3 -c "import fluid_langrangians; print('Module imports successfully')"` -- verify module imports
  - `python3 -m py_compile fluid_langrangians.py` -- compile check, takes <1 second
  - `python3 -c "import ast; ast.parse(open('fluid_langrangians.py').read()); print('Syntax check passed')"` -- syntax validation

## Repository Structure

The repository contains:
- `README.md` -- minimal project description (1 line)
- `fluid_langrangians.py` -- main fluid simulation script (145 lines)
- `.gitignore` -- excludes Python cache and build artifacts

No build system, test framework, or CI/CD pipelines are present. This is a standalone research script.

## Validation

- **MANUAL VALIDATION REQUIREMENT**: After making changes, always run the full simulation to ensure it produces expected output
- Run complete simulation: `python3 fluid_langrangians.py`
- Expected output includes:
  - Projection test showing divergence reduction: `[projection test] L2(div) before=X.XXXXXX, after=Y.YYYYYY`
  - 13 simulation steps showing divergence values: `step XXX  L2(div)≈ Z.ZZZZZZ`
  - Total execution time: ~1 second
- The simulation should complete without errors and show physically reasonable divergence values
- Verify module can be imported: `python3 -c "import fluid_langrangians"`
- **No testing framework** is available - validation must be done by running the script and observing output

## Dependencies and Environment

- **Python 3.12.3** (system installation at `/usr/bin/python3`)
- **pip3** for package management (user installation to `/home/runner/.local/`)
- **NumPy 2.3.3+** (install with `pip3 install numpy`)
- **No virtual environment setup** - uses system Python with user packages
- **No requirements.txt** - single dependency on NumPy

## Development Tools

- **No linting tools** (flake8, black, mypy not available)
- **No testing framework** (pytest not available) 
- **No formatting tools** installed
- Use built-in Python tools for validation:
  - `python3 -m py_compile` for compilation check
  - `python3 -c "import ast; ast.parse(...)"` for syntax validation
  - `python3 -m pydoc fluid_langrangians` for documentation

## Code Understanding

The main script implements:
- **Boundary enforcement**: `enforce_no_through()` - sets velocity to zero at boundaries
- **Fluid operators**: `divergence()`, `jacobi_pressure()`, `project()` - core fluid mechanics
- **Vorticity handling**: `curl_scalar()`, `vorticity_confinement()` - maintains fluid rotation
- **Advection**: `advect_scalar()`, `advect_vector()` - semi-Lagrangian transport
- **Initial conditions**: Seeded with random velocity splats and dye injection
- **Main simulation loop**: 120 time steps with divergence monitoring

Key files to modify when working on fluid dynamics:
- `fluid_langrangians.py` - contains all simulation logic
- Check `README.md` for project context updates

## Common Tasks

### Running the simulation
```bash
cd /home/runner/work/fermi-fluids-intro/fermi-fluids-intro
pip3 install numpy
python3 fluid_langrangians.py
```

### Checking code integrity
```bash
python3 -m py_compile fluid_langrangians.py
python3 -c "import fluid_langrangians; print('Import successful')"
```

### Understanding the module structure
```bash
python3 -c "import fluid_langrangians; help(fluid_langrangians)" | head -20
```

## Repository Contents Reference

### ls -la [repo-root]
```
total 24
drwxr-xr-x 3 runner runner 4096 Sep 13 04:57 .
drwxr-xr-x 3 runner runner 4096 Sep 13 04:57 ..
drwxrwxr-x 7 runner runner 4096 Sep 13 04:57 .git
drwxrwxr-x 2 runner runner 4096 Sep 13 04:57 .github
-rw-rw-r-- 1 runner runner  222 Sep 13 04:57 .gitignore
-rw-rw-r-- 1 runner runner   20 Sep 13 04:57 README.md
-rw-rw-r-- 1 runner runner 5202 Sep 13 04:57 fluid_langrangians.py
```

### cat README.md
```
# fermi-fluids-intro
```

### Expected simulation output
```
[projection test] L2(div) before=12.713231, after=8.351003
step 000  L2(div)≈ 1.948369
step 010  L2(div)≈ 6.264033
step 020  L2(div)≈ 11.077718
step 030  L2(div)≈ 12.653949
step 040  L2(div)≈ 12.890569
step 050  L2(div)≈ 14.410472
step 060  L2(div)≈ 15.107371
step 070  L2(div)≈ 16.761661
step 080  L2(div)≈ 17.022193
step 090  L2(div)≈ 18.253327
step 100  L2(div)≈ 18.782842
step 110  L2(div)≈ 19.605656
step 119  L2(div)≈ 19.784135
```

## Git Workflow

- Repository is on branch `copilot/fix-3`
- Standard git hooks available (samples only)
- Use `.gitignore` to exclude `__pycache__/` and build artifacts
- No CI/CD or automated testing workflows