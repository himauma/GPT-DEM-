"""
Example scenarios for DEM simulation
Demonstrates various use cases of the DEM engine
"""
import numpy as np
import matplotlib.pyplot as plt
from dem_simulation import DEMSimulation
from visualizer import DEMVisualizer


def example_single_particle_drop():
    """
    Simple example: single particle dropping under gravity.
    """
    print("Running: Single Particle Drop")
    
    # Create simulation
    sim = DEMSimulation(width=5.0, height=10.0, gravity=9.81)
    
    # Add a single particle at the top
    sim.add_particle(x=2.5, y=8.0, radius=0.2, mass=1.0)
    
    # Create visualizer
    viz = DEMVisualizer(sim)
    
    # Run simulation
    print("Simulating particle drop...")
    for i in range(1000):
        sim.step(0.001)
        if i % 100 == 0:
            print(f"Step {i}: time={sim.time:.3f}s, position={sim.particles[0].position}")
    
    # Show final state
    viz.show_static()
    

def example_multiple_particles():
    """
    Example with multiple particles falling and colliding.
    """
    print("\nRunning: Multiple Particles Collision")
    
    # Create simulation
    sim = DEMSimulation(width=10.0, height=10.0, gravity=9.81)
    
    # Add multiple particles
    np.random.seed(42)
    for i in range(10):
        x = 2.0 + np.random.random() * 6.0
        y = 5.0 + np.random.random() * 4.0
        radius = 0.15 + np.random.random() * 0.1
        mass = 1.0
        sim.add_particle(x, y, radius, mass)
    
    # Create visualizer
    viz = DEMVisualizer(sim)
    
    # Run simulation
    print("Simulating multiple particle collision...")
    for i in range(2000):
        sim.step(0.001)
        if i % 500 == 0:
            ke, pe, te = sim.get_total_energy()
            print(f"Step {i}: time={sim.time:.2f}s, energy={te:.2f}J")
    
    # Show final state
    viz.show_static()


def example_particle_pile():
    """
    Example: particles forming a pile on the ground.
    """
    print("\nRunning: Particle Pile Formation")
    
    # Create simulation
    sim = DEMSimulation(width=8.0, height=12.0, gravity=9.81)
    
    # Add particles in a column that will fall and form a pile
    np.random.seed(123)
    for i in range(15):
        x = 4.0 + (np.random.random() - 0.5) * 0.5
        y = 2.0 + i * 0.5
        radius = 0.15
        mass = 1.0
        sim.add_particle(x, y, radius, mass)
    
    # Create visualizer
    viz = DEMVisualizer(sim)
    
    # Run simulation with animation
    print("Creating animation of pile formation...")
    anim = viz.animate(dt=0.001, steps_per_frame=10, frames=300, interval=20)
    plt.show()


def example_save_animation():
    """
    Example: save animation to file.
    """
    print("\nRunning: Save Animation Example")
    
    # Create simulation
    sim = DEMSimulation(width=6.0, height=8.0, gravity=9.81)
    
    # Add particles
    np.random.seed(456)
    for i in range(8):
        x = 2.0 + np.random.random() * 2.0
        y = 4.0 + i * 0.4
        radius = 0.12
        mass = 0.5
        sim.add_particle(x, y, radius, mass)
    
    # Create visualizer and save animation
    viz = DEMVisualizer(sim)
    print("Saving animation to file...")
    viz.save_animation('particle_demo.gif', dt=0.001, steps_per_frame=10, 
                      frames=200, interval=20, dpi=80)
    print("Animation saved successfully!")


def example_particle_bounce():
    """
    Example: particles bouncing with different restitution coefficients.
    """
    print("\nRunning: Particle Bounce Test")
    
    # Create simulation with high restitution (bouncy)
    sim = DEMSimulation(width=5.0, height=10.0, gravity=9.81)
    sim.restitution_coeff = 0.9
    sim.damping = 0.1  # Low damping for bouncier behavior
    
    # Add particles at different heights
    for i, x_pos in enumerate([1.5, 2.5, 3.5]):
        sim.add_particle(x=x_pos, y=8.0, radius=0.15, mass=1.0)
    
    # Create visualizer
    viz = DEMVisualizer(sim)
    
    # Run simulation
    print("Simulating bouncing particles...")
    for i in range(3000):
        sim.step(0.001)
        if i % 1000 == 0:
            print(f"Step {i}: time={sim.time:.2f}s")
            for j, p in enumerate(sim.particles):
                print(f"  Particle {j}: pos={p.position}, vel={p.velocity}")
    
    # Show final state
    viz.show_static()


if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for testing
    
    print("=" * 60)
    print("DEM Simulation Examples")
    print("=" * 60)
    
    # Run examples
    example_single_particle_drop()
    example_multiple_particles()
    
    # Uncomment to test animation (requires interactive backend)
    # example_particle_pile()
    # example_save_animation()
    
    example_particle_bounce()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
