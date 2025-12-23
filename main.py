"""
Main script to run DEM simulation
Creates particles, runs simulation, and visualizes results
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from particle import Particle
from dem_simulation import DEMSimulation


def create_falling_particles_simulation():
    """Create a simulation with falling particles"""
    # Create simulation
    sim = DEMSimulation(width=10.0, height=10.0, gravity=-9.81)
    
    # Add particles in a grid pattern at the top
    radius = 0.3
    mass = 1.0
    spacing = 2 * radius + 0.1
    
    for i in range(5):
        for j in range(3):
            x = 2.0 + i * spacing
            y = 7.0 + j * spacing
            # Add small random velocity
            vx = np.random.uniform(-0.5, 0.5)
            vy = np.random.uniform(-0.5, 0.5)
            particle = Particle(x, y, radius, mass, vx, vy)
            sim.add_particle(particle)
    
    return sim


def create_pile_simulation():
    """Create a simulation with particles forming a pile"""
    # Create simulation
    sim = DEMSimulation(width=10.0, height=10.0, gravity=-9.81)
    
    # Add particles randomly at the top
    radius = 0.25
    mass = 1.0
    
    np.random.seed(42)  # For reproducibility
    for i in range(30):
        x = np.random.uniform(radius, 10.0 - radius)
        y = np.random.uniform(7.0, 9.5)
        vx = np.random.uniform(-0.2, 0.2)
        vy = 0
        particle = Particle(x, y, radius, mass, vx, vy)
        sim.add_particle(particle)
    
    return sim


def animate_simulation(sim, duration=10.0, dt=0.01, fps=30):
    """
    Animate the DEM simulation
    
    Args:
        sim (DEMSimulation): The simulation to animate
        duration (float): Simulation duration in seconds
        dt (float): Time step for simulation
        fps (int): Frames per second for animation
    """
    # Setup figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, sim.width)
    ax.set_ylim(0, sim.height)
    ax.set_aspect('equal')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_title('DEM Simulation - Particle Dynamics')
    ax.grid(True, alpha=0.3)
    
    # Initialize particle circles
    circles = []
    positions, radii = sim.get_particle_data()
    for pos, radius in zip(positions, radii):
        circle = plt.Circle(pos, radius, color='blue', alpha=0.7, ec='black', linewidth=1)
        ax.add_patch(circle)
        circles.append(circle)
    
    # Simulation parameters
    steps_per_frame = int(1.0 / (fps * dt))
    total_frames = int(duration * fps)
    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                        verticalalignment='top', fontsize=10,
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def update(frame):
        """Update function for animation"""
        # Run multiple simulation steps per frame for smoother physics
        for _ in range(steps_per_frame):
            sim.step(dt)
        
        # Update circle positions
        positions, _ = sim.get_particle_data()
        for circle, pos in zip(circles, positions):
            circle.center = pos
        
        # Update time display
        current_time = frame / fps
        time_text.set_text(f'Time: {current_time:.2f}s')
        
        return circles + [time_text]
    
    # Create animation
    anim = animation.FuncAnimation(fig, update, frames=total_frames,
                                   interval=1000/fps, blit=True, repeat=False)
    
    plt.tight_layout()
    return anim


def run_simulation():
    """Run the DEM simulation"""
    print("DEM (Discrete Element Method) Simulation")
    print("=" * 50)
    print("\nSimulation types:")
    print("1. Falling particles")
    print("2. Forming a pile")
    
    choice = input("\nSelect simulation type (1 or 2, default=2): ").strip()
    
    if choice == "1":
        print("\nCreating falling particles simulation...")
        sim = create_falling_particles_simulation()
    else:
        print("\nCreating pile formation simulation...")
        sim = create_pile_simulation()
    
    print(f"Number of particles: {len(sim.particles)}")
    print(f"Domain size: {sim.width} x {sim.height} m")
    print(f"Gravity: {sim.gravity} m/s^2")
    print("\nStarting simulation...")
    
    # Run and animate
    anim = animate_simulation(sim, duration=10.0, dt=0.01, fps=30)
    
    # Save animation (optional)
    save = input("\nSave animation as GIF? (y/n, default=n): ").strip().lower()
    if save == 'y':
        print("Saving animation... (this may take a while)")
        anim.save('dem_simulation.gif', writer='pillow', fps=30)
        print("Animation saved as 'dem_simulation.gif'")
    
    plt.show()
    print("\nSimulation complete!")


if __name__ == "__main__":
    run_simulation()
