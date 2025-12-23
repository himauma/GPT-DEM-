"""
Simple visualization test (non-interactive)
Creates a static plot of the initial state
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from particle import Particle
from dem_simulation import DEMSimulation


def test_visualization():
    """Test that visualization code works"""
    print("Testing visualization setup...")
    
    # Create simulation
    sim = DEMSimulation(width=10.0, height=10.0, gravity=-9.81)
    
    # Add some particles
    radius = 0.3
    mass = 1.0
    for i in range(3):
        for j in range(2):
            x = 3.0 + i * 1.0
            y = 5.0 + j * 1.0
            particle = Particle(x, y, radius, mass, 0, 0)
            sim.add_particle(particle)
    
    # Setup figure
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, sim.width)
    ax.set_ylim(0, sim.height)
    ax.set_aspect('equal')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_title('DEM Simulation - Initial State')
    ax.grid(True, alpha=0.3)
    
    # Draw particles
    positions, radii = sim.get_particle_data()
    for pos, r in zip(positions, radii):
        circle = plt.Circle(pos, r, color='blue', alpha=0.7, ec='black', linewidth=1)
        ax.add_patch(circle)
    
    # Save figure
    plt.tight_layout()
    plt.savefig('/tmp/dem_test_visualization.png', dpi=100)
    plt.close()
    
    print("✓ Visualization test passed - saved to /tmp/dem_test_visualization.png")
    
    # Run a few steps and create another visualization
    print("\nRunning simulation steps...")
    for i in range(100):
        sim.step(0.01)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, sim.width)
    ax.set_ylim(0, sim.height)
    ax.set_aspect('equal')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_title('DEM Simulation - After 1 second')
    ax.grid(True, alpha=0.3)
    
    positions, radii = sim.get_particle_data()
    for pos, r in zip(positions, radii):
        circle = plt.Circle(pos, r, color='blue', alpha=0.7, ec='black', linewidth=1)
        ax.add_patch(circle)
    
    plt.tight_layout()
    plt.savefig('/tmp/dem_test_after_simulation.png', dpi=100)
    plt.close()
    
    print("✓ Simulation ran successfully - saved to /tmp/dem_test_after_simulation.png")
    print("\nVisualization test complete!")


if __name__ == "__main__":
    test_visualization()
