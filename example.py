#!/usr/bin/env python3
"""
Example script demonstrating the FluidSim API
"""
import numpy as np
import sys
import os

# Add the fluid simulation to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fluid_core import FluidSim
from colormaps import dye_colormap, viridis_colormap, divergence_colormap


def demonstrate_api():
    """Demonstrate the FluidSim API with various scenarios."""
    print("FluidSim API Demonstration")
    print("=" * 50)
    
    # 1. Basic usage
    print("\n1. Basic FluidSim Usage")
    sim = FluidSim(N=128, dt=0.06, vel_diss=0.05, dye_diss=0.1)
    print(f"Created simulation: {sim.N}x{sim.N} grid")
    
    # 2. Adding splats
    print("\n2. Adding Different Types of Splats")
    
    # Dye only
    sim.add_splat(0.2, 0.2, dye_amount=1.0, radius=0.08)
    print("Added dye-only splat")
    
    # Velocity only  
    sim.add_splat(0.8, 0.2, fx=0.7, fy=0.3, radius=0.06)
    print("Added velocity-only splat")
    
    # Combined dye and velocity
    sim.add_splat(0.5, 0.8, dye_amount=0.8, fx=-0.4, fy=-0.6, radius=0.1)
    print("Added combined dye+velocity splat")
    
    # 3. Simulation loop
    print("\n3. Running Simulation")
    for step in range(20):
        sim.step()
        if step % 5 == 0:
            stats = sim.get_stats()
            print(f"Step {stats['step']:2d}: "
                  f"L2(div)={stats['divergence_l2']:.6f}, "
                  f"max|v|={stats['max_velocity']:.3f}")
    
    # 4. Field analysis
    print("\n4. Field Analysis")
    fields = sim.get_fields()
    
    for name, field in fields.items():
        print(f"{name:12s}: min={np.min(field):7.3f}, "
              f"max={np.max(field):7.3f}, "
              f"mean={np.mean(field):7.3f}")
    
    # 5. Parameter adjustment
    print("\n5. Parameter Adjustment")
    original_vort = sim.vort_strength
    sim.set_params(vort_strength=12.0, vel_diss=0.02)
    print(f"Changed vorticity strength: {original_vort} → {sim.vort_strength}")
    print(f"Changed velocity dissipation: 0.05 → {sim.vel_diss}")
    
    # Run a few more steps to see the effect
    for _ in range(5):
        sim.step()
    
    stats = sim.get_stats()
    print(f"After parameter change: max|v|={stats['max_velocity']:.3f}")
    
    # 6. Visualization preparation
    print("\n6. Visualization Data")
    fields = sim.get_fields()
    
    # Generate RGB data for different visualizations
    dye_rgb = dye_colormap(fields['dye'])
    vort_rgb = viridis_colormap(fields['vorticity'])
    div_rgb = divergence_colormap(fields['divergence'])
    
    print(f"Generated visualization data:")
    print(f"  Dye colormap: {dye_rgb.shape}")
    print(f"  Vorticity colormap: {vort_rgb.shape}")
    print(f"  Divergence colormap: {div_rgb.shape}")
    
    # 7. Reset and new scenario
    print("\n7. Reset and New Scenario")
    sim.reset()
    print("Reset simulation")
    
    # Create a vortex ring
    center_x, center_y = 0.5, 0.5
    radius = 0.15
    n_points = 8
    
    for i in range(n_points):
        angle = 2 * np.pi * i / n_points
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)
        
        # Tangential velocity for circulation
        fx = -np.sin(angle) * 0.6
        fy = np.cos(angle) * 0.6
        
        sim.add_splat(x, y, dye_amount=0.7, fx=fx, fy=fy, radius=0.04)
    
    print(f"Created vortex ring with {n_points} splats")
    
    # Run the vortex simulation
    for step in range(15):
        sim.step()
        if step % 5 == 0:
            stats = sim.get_stats()
            print(f"Vortex step {stats['step']:2d}: "
                  f"L2(div)={stats['divergence_l2']:.6f}")
    
    print("\n" + "=" * 50)
    print("API demonstration complete!")
    print("For interactive use, run: python fluid_gui.py")


def demonstrate_educational_concepts():
    """Demonstrate key educational concepts."""
    print("\n\nEducational Concepts Demonstration")
    print("=" * 50)
    
    # Concept 1: Effect of projection on divergence
    print("\n1. Pressure Projection Effect")
    sim = FluidSim(N=64, iters=80)
    
    # Add some divergent velocity
    sim.add_splat(0.3, 0.5, fx=1.0, fy=0.0, radius=0.1)  # Right flow
    sim.add_splat(0.7, 0.5, fx=-1.0, fy=0.0, radius=0.1)  # Left flow
    
    # Measure divergence before and after a step
    fields_before = sim.get_fields()
    div_before = np.linalg.norm(fields_before['divergence'])
    
    sim.step()  # This includes projection
    
    fields_after = sim.get_fields()
    div_after = np.linalg.norm(fields_after['divergence'])
    
    print(f"Divergence before projection: {div_before:.6f}")
    print(f"Divergence after projection:  {div_after:.6f}")
    print(f"Reduction factor: {div_after/div_before:.3f}")
    
    # Concept 2: Vorticity confinement effect
    print("\n2. Vorticity Confinement Effect")
    sim_no_vort = FluidSim(N=64, vort_strength=0.0)
    sim_with_vort = FluidSim(N=64, vort_strength=8.0)
    
    # Add same initial conditions
    for sim in [sim_no_vort, sim_with_vort]:
        sim.add_splat(0.5, 0.5, fx=0.5, fy=0.3, radius=0.08)
    
    # Run simulations
    for _ in range(10):
        sim_no_vort.step()
        sim_with_vort.step()
    
    fields_no_vort = sim_no_vort.get_fields()
    fields_with_vort = sim_with_vort.get_fields()
    
    max_vort_no = np.max(fields_no_vort['vorticity'])
    max_vort_with = np.max(fields_with_vort['vorticity'])
    
    print(f"Max vorticity without confinement: {max_vort_no:.3f}")
    print(f"Max vorticity with confinement:    {max_vort_with:.3f}")
    print(f"Enhancement factor: {max_vort_with/max_vort_no:.2f}")
    
    # Concept 3: Dissipation effects
    print("\n3. Dissipation Effects")
    sim_low_diss = FluidSim(N=64, vel_diss=0.01, dye_diss=0.01)
    sim_high_diss = FluidSim(N=64, vel_diss=0.15, dye_diss=0.15)
    
    # Add same initial conditions
    for sim in [sim_low_diss, sim_high_diss]:
        sim.add_splat(0.5, 0.5, dye_amount=1.0, fx=0.8, fy=0.0, radius=0.1)
    
    # Run for many steps
    for _ in range(30):
        sim_low_diss.step()
        sim_high_diss.step()
    
    stats_low = sim_low_diss.get_stats()
    stats_high = sim_high_diss.get_stats()
    
    print(f"Low dissipation:  max|v|={stats_low['max_velocity']:.3f}, "
          f"max_dye={stats_low['max_dye']:.3f}")
    print(f"High dissipation: max|v|={stats_high['max_velocity']:.3f}, "
          f"max_dye={stats_high['max_dye']:.3f}")
    
    print("\n" + "=" * 50)
    print("Educational concepts demonstration complete!")


if __name__ == "__main__":
    demonstrate_api()
    demonstrate_educational_concepts()
    
    print("\n\nNext steps:")
    print("1. Run the interactive GUI: python fluid_gui.py")
    print("2. Try different grid sizes: python fluid_gui.py 256")
    print("3. Compare with original: python fluid_langrangians.py")