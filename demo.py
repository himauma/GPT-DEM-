"""
Simple example: Run a quick DEM simulation and save an animation
This is a non-interactive version suitable for automated testing
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from particle import Particle
from dem_simulation import DEMSimulation


def create_demo_simulation():
    """Create a simple demo simulation"""
    print("Creating DEM simulation...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=-9.81)
    
    # Add particles in a pattern
    radius = 0.25
    mass = 1.0
    
    np.random.seed(42)
    for i in range(20):
        x = np.random.uniform(radius + 1, 9.0 - radius)
        y = np.random.uniform(6.0, 9.0)
        vx = np.random.uniform(-0.1, 0.1)
        particle = Particle(x, y, radius, mass, vx, 0)
        sim.add_particle(particle)
    
    print(f"Created simulation with {len(sim.particles)} particles")
    return sim


def save_animation(sim, filename='dem_demo.gif', duration=5.0, dt=0.01, fps=30):
    """Save an animation of the simulation"""
    print(f"Creating animation ({duration}s at {fps} fps)...")
    
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
    
    steps_per_frame = int(1.0 / (fps * dt))
    total_frames = int(duration * fps)
    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                        verticalalignment='top', fontsize=10,
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def update(frame):
        for _ in range(steps_per_frame):
            sim.step(dt)
        
        positions, _ = sim.get_particle_data()
        for circle, pos in zip(circles, positions):
            circle.center = pos
        
        current_time = frame / fps
        time_text.set_text(f'Time: {current_time:.2f}s')
        
        if frame % 30 == 0:  # Progress every second
            print(f"  Progress: {current_time:.1f}s / {duration:.1f}s")
        
        return circles + [time_text]
    
    anim = animation.FuncAnimation(fig, update, frames=total_frames,
                                   interval=1000/fps, blit=True, repeat=False)
    
    plt.tight_layout()
    print(f"Saving animation to {filename}...")
    anim.save(filename, writer='pillow', fps=fps)
    plt.close()
    print(f"✓ Animation saved successfully!")


def main():
    """Run the demo"""
    print("=" * 60)
    print("DEM Simulation Demo")
    print("=" * 60)
    print()
    
    # Create and run simulation
    sim = create_demo_simulation()
    
    # Save animation
    save_animation(sim, filename='dem_demo.gif', duration=5.0)
    
    print()
    print("=" * 60)
    print("Demo complete!")
    print("View the animation: dem_demo.gif")
    print("=" * 60)


if __name__ == "__main__":
    main()
