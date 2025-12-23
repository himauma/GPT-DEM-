"""
Main entry point for DEM simulation
Run this file to execute the simulation
"""
import numpy as np

from dem_simulation import DEMSimulation
from visualizer import DEMVisualizer


def main():
    """
    Main function to run DEM simulation demonstration.
    """
    # Set matplotlib backend for non-interactive use
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    print("=" * 70)
    print("GPT-DEM Simulation - Discrete Element Method")
    print("=" * 70)
    print("\nInitializing DEM simulation...")
    
    # Create simulation with reasonable domain size
    sim = DEMSimulation(width=10.0, height=15.0, gravity=9.81)
    
    # Configure material properties
    sim.restitution_coeff = 0.7  # Slightly bouncy
    sim.friction_coeff = 0.3     # Moderate friction
    sim.stiffness = 1e5          # Contact stiffness
    sim.damping = 0.3            # Damping coefficient
    
    print(f"\nSimulation domain: {sim.width}m x {sim.height}m")
    print(f"Gravity: {sim.gravity} m/s²")
    print(f"Material properties:")
    print(f"  - Restitution coefficient: {sim.restitution_coeff}")
    print(f"  - Friction coefficient: {sim.friction_coeff}")
    print(f"  - Stiffness: {sim.stiffness} N/m")
    print(f"  - Damping: {sim.damping}")
    
    # Add particles - create a stack that will fall and form a pile
    print("\nAdding particles to simulation...")
    np.random.seed(42)
    
    num_particles = 20
    for i in range(num_particles):
        # Create particles in layers
        layer = i // 4
        position_in_layer = i % 4
        
        x = 3.0 + position_in_layer * 1.2 + (np.random.random() - 0.5) * 0.2
        y = 8.0 + layer * 0.6
        radius = 0.2
        mass = 1.0
        
        sim.add_particle(x, y, radius, mass)
    
    print(f"Added {len(sim.particles)} particles")
    
    # Run simulation
    print("\nRunning DEM simulation...")
    print("-" * 70)
    
    dt = 0.0005  # Time step (seconds)
    total_steps = 5000
    report_interval = 1000
    
    for step in range(total_steps):
        sim.step(dt)
        
        if step % report_interval == 0:
            ke, pe, te = sim.get_total_energy()
            print(f"Step {step:5d} | Time: {sim.time:6.3f}s | "
                  f"KE: {ke:8.2f}J | PE: {pe:8.2f}J | Total: {te:8.2f}J")
    
    print("-" * 70)
    print(f"Simulation completed at t = {sim.time:.3f}s")
    
    # Calculate final statistics
    ke, pe, te = sim.get_total_energy()
    print("\nFinal Energy State:")
    print(f"  Kinetic Energy:   {ke:8.2f} J")
    print(f"  Potential Energy: {pe:8.2f} J")
    print(f"  Total Energy:     {te:8.2f} J")
    
    # Calculate average particle height
    avg_height = np.mean([p.position[1] for p in sim.particles])
    print(f"\nAverage particle height: {avg_height:.2f} m")
    
    # Particle velocity statistics
    velocities = [np.linalg.norm(p.velocity) for p in sim.particles]
    print(f"Velocity statistics:")
    print(f"  Mean:   {np.mean(velocities):.3f} m/s")
    print(f"  Max:    {np.max(velocities):.3f} m/s")
    print(f"  Min:    {np.min(velocities):.3f} m/s")
    
    # Create visualization
    print("\nCreating visualization...")
    viz = DEMVisualizer(sim)
    viz.setup_plot()
    viz.draw_particles()
    
    # Add final state information to plot
    ke, pe, te = sim.get_total_energy()
    info_text = f'Final State (t = {sim.time:.2f}s)\n'
    info_text += f'Particles: {len(sim.particles)}\n'
    info_text += f'Kinetic Energy: {ke:.2f} J\n'
    info_text += f'Potential Energy: {pe:.2f} J\n'
    info_text += f'Total Energy: {te:.2f} J\n'
    info_text += f'Avg Height: {avg_height:.2f} m'
    
    viz.ax.text(0.02, 0.98, info_text, 
                transform=viz.ax.transAxes,
                verticalalignment='top',
                fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Save the figure
    output_file = 'dem_simulation_result.png'
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to {output_file}")
    
    print("\n" + "=" * 70)
    print("DEM Simulation completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
