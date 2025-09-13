# Interactive Fermi Fluids Introduction

An educational tool for exploring 2D incompressible fluid dynamics with interactive visualization. This repository provides both a pure numerical implementation and an interactive GUI for real-time experimentation with semi-Lagrangian fluid simulation.

## Features

### Interactive GUI
- **Real-time Visualization**: Multiple view modes including dye transport, vorticity magnitude, divergence heatmap, and velocity vectors
- **Mouse Interaction**: Add dye and velocity splats by dragging and clicking
- **Live Parameter Control**: Adjust simulation parameters in real-time
- **Educational Overlays**: Built-in help explaining fluid dynamics concepts
- **Performance Monitoring**: Live FPS, divergence tracking, and simulation statistics

### Numerical Methods
- **Semi-Lagrangian Advection**: Unconditionally stable advection scheme
- **Pressure Projection**: Helmholtz-Hodge decomposition for incompressibility
- **Vorticity Confinement**: Restores small-scale turbulent features
- **Jacobi Iteration**: Efficient pressure solve with configurable iterations

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Running the Interactive GUI
```bash
python fluid_gui.py [grid_size]
```

Example with 256x256 grid:
```bash
python fluid_gui.py 256
```

### Running the Original Script
```bash
python fluid_langrangians.py
```

## Controls

### Mouse Controls
- **Left Drag**: Add dye and velocity along motion direction
- **Right Click**: Add velocity vortex at cursor position
- **Shift + Click**: Larger splat radius (planned feature)

### Keyboard Shortcuts
- **Space**: Pause/Resume simulation
- **S**: Single step when paused
- **R**: Reset simulation to initial state
- **C**: Clear dye field only
- **H**: Toggle help overlay
- **1-4**: Switch visualization modes (Dye/Vorticity/Divergence/Velocity)

### GUI Controls
- **Mode Button**: Cycle through visualization modes
- **Pause/Resume**: Control simulation playback
- **Step**: Advance one timestep when paused
- **Reset**: Restart with random initial conditions
- **Clear Dye**: Remove dye while keeping velocity field

## Visualization Modes

1. **Dye Mode**: Shows scalar tracer transport (red coloring)
2. **Vorticity Mode**: Displays magnitude of fluid rotation (viridis colormap)  
3. **Divergence Mode**: Shows velocity field divergence (blue=negative, red=positive)
4. **Velocity Mode**: Vector field with arrow overlay showing flow direction

## Educational Concepts

### Semi-Lagrangian Advection
The simulation uses semi-Lagrangian advection, which:
- Is **unconditionally stable** regardless of time step size
- Traces particles backward in time to find source values
- Introduces **numerical diffusion** that smooths sharp features
- Allows larger time steps than explicit methods

### Pressure Projection
The pressure projection step:
- Enforces the **incompressibility constraint** (∇·v = 0)
- Uses the **Helmholtz-Hodge decomposition** to separate velocity into divergence-free and gradient components
- Solves a Poisson equation for pressure using **Jacobi iteration**
- Is crucial for realistic fluid behavior

### Vorticity Confinement
Vorticity confinement:
- **Restores small-scale turbulence** lost to numerical diffusion
- Adds energy back into rotational motion
- Is controlled by the `vort_strength` parameter
- Helps maintain visual interest in long simulations

### Dissipation
- **Velocity dissipation** (`vel_diss`) simulates viscosity effects
- **Dye dissipation** (`dye_diss`) simulates mixing and diffusion
- Both use exponential decay: `field *= exp(-dissipation * dt)`

## File Structure

```
fluid_core.py       # Core simulation class and numerical methods
fluid_gui.py        # Interactive pygame-based GUI
colormaps.py        # Visualization utilities and color mapping
fluid_langrangians.py  # Original headless simulation script
requirements.txt    # Python dependencies
README.md          # This documentation
```

## API Reference

### FluidSim Class

```python
from fluid_core import FluidSim

# Create simulation
sim = FluidSim(N=128, dt=0.08, vel_diss=0.08, dye_diss=0.12, 
               vort_strength=6.0, iters=60)

# Add splats
sim.add_splat(x=0.5, y=0.5, dye_amount=1.0, fx=0.5, fy=0.0, radius=0.1)

# Advance simulation
sim.step()

# Get fields
fields = sim.get_fields()  # Returns dict with 'dye', 'u', 'v', etc.

# Get statistics  
stats = sim.get_stats()   # Returns step count, divergence, etc.
```

### Parameters

- `N`: Grid resolution (default: 128)
- `dt`: Time step size (default: 0.08)
- `vel_diss`: Velocity dissipation rate (default: 0.08)
- `dye_diss`: Dye dissipation rate (default: 0.12)  
- `vort_strength`: Vorticity confinement strength (default: 6.0)
- `iters`: Pressure projection iterations (default: 60)

## Performance Notes

- **Grid Size**: Computational cost scales as O(N²) per timestep
- **Projection Iterations**: More iterations improve incompressibility but cost more
- **Visualization**: GUI rendering may be the bottleneck for large grids
- **Recommended Sizes**: 
  - Interactive use: 128-256
  - High quality: 512
  - Real-time demos: 64-128

## Educational Use

This tool is designed for:
- **Computational Fluid Dynamics courses** - visualizing numerical methods
- **Physics education** - understanding fluid behavior
- **Computer graphics** - learning simulation techniques
- **Research** - prototyping new fluid algorithms

The clear separation between numerical core (`fluid_core.py`) and visualization (`fluid_gui.py`) makes it easy to:
- Modify numerical methods without touching GUI code
- Implement new visualization modes
- Use the simulation in other projects
- Understand the mathematical foundations

## Implementation Details

### Boundary Conditions
- **No-slip walls** on all boundaries
- Velocity components normal to walls are set to zero
- Pressure uses Neumann boundary conditions

### Numerical Stability
- Semi-Lagrangian advection is unconditionally stable
- CFL condition is monitored but not enforced
- Simulation remains stable even with large time steps

### Memory Layout
- All fields use `float32` for efficiency
- Fields are stored in row-major order (y, x indexing)
- GUI handles coordinate system conversions

## Future Enhancements

Potential improvements for educational impact:
- **Multi-resolution grids** for performance scaling
- **Save/load simulation states** for sharing interesting configurations
- **Animation export** for creating educational videos
- **Side-by-side comparisons** of different numerical methods
- **3D visualization** mode for advanced courses
- **Interactive obstacles** that can be placed and moved

## License

This educational tool is provided for learning and research purposes. See the original repository for licensing details.

## Contributing

Contributions that enhance the educational value are welcome:
- Additional visualization modes
- Better educational explanations
- Performance optimizations
- Bug fixes and stability improvements

Focus should remain on clarity and educational impact rather than production performance.