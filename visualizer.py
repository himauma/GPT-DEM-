"""
Visualization module for DEM simulation
Provides functions to visualize particles and create animations
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import numpy as np


class DEMVisualizer:
    """
    Visualizer for DEM simulation using matplotlib.
    """
    
    def __init__(self, simulation):
        """
        Initialize the visualizer.
        
        Args:
            simulation (DEMSimulation): The DEM simulation instance
        """
        self.simulation = simulation
        self.fig = None
        self.ax = None
        self.particle_patches = []
        
    def setup_plot(self):
        """Set up the matplotlib figure and axis."""
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_xlim(0, self.simulation.width)
        self.ax.set_ylim(0, self.simulation.height)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X Position (m)')
        self.ax.set_ylabel('Y Position (m)')
        self.ax.set_title('DEM Simulation')
        self.ax.grid(True, alpha=0.3)
        
    def draw_particles(self):
        """Draw all particles on the current axis."""
        # Clear previous patches
        for patch in self.particle_patches:
            patch.remove()
        self.particle_patches = []
        
        # Draw each particle
        for particle in self.simulation.particles:
            circle = Circle(
                particle.position, 
                particle.radius, 
                facecolor='blue', 
                edgecolor='black',
                alpha=0.7
            )
            self.ax.add_patch(circle)
            self.particle_patches.append(circle)
            
    def show_static(self):
        """Show a static snapshot of the current simulation state."""
        self.setup_plot()
        self.draw_particles()
        
        # Display simulation info
        ke, pe, te = self.simulation.get_total_energy()
        info_text = f'Time: {self.simulation.time:.2f}s\n'
        info_text += f'Particles: {len(self.simulation.particles)}\n'
        info_text += f'Kinetic Energy: {ke:.2f} J\n'
        info_text += f'Potential Energy: {pe:.2f} J\n'
        info_text += f'Total Energy: {te:.2f} J'
        
        self.ax.text(0.02, 0.98, info_text, 
                    transform=self.ax.transAxes,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.show()
        
    def animate(self, dt=0.001, steps_per_frame=10, frames=500, interval=20):
        """
        Create an animation of the simulation.
        
        Args:
            dt (float): Time step for simulation
            steps_per_frame (int): Number of simulation steps per animation frame
            frames (int): Total number of animation frames
            interval (int): Delay between frames in milliseconds
            
        Returns:
            matplotlib.animation.FuncAnimation: The animation object
        """
        self.setup_plot()
        
        # Initialize particles
        self.draw_particles()
        
        # Text for displaying info
        info_text = self.ax.text(0.02, 0.98, '', 
                                transform=self.ax.transAxes,
                                verticalalignment='top',
                                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        def update(frame):
            # Perform multiple simulation steps per frame for stability
            for _ in range(steps_per_frame):
                self.simulation.step(dt)
                
            # Update particle positions
            for i, particle in enumerate(self.simulation.particles):
                self.particle_patches[i].center = particle.position
                
            # Update info text
            ke, pe, te = self.simulation.get_total_energy()
            info_str = f'Time: {self.simulation.time:.2f}s\n'
            info_str += f'Particles: {len(self.simulation.particles)}\n'
            info_str += f'Kinetic Energy: {ke:.2f} J\n'
            info_str += f'Potential Energy: {pe:.2f} J\n'
            info_str += f'Total Energy: {te:.2f} J'
            info_text.set_text(info_str)
            
            return self.particle_patches + [info_text]
        
        anim = animation.FuncAnimation(
            self.fig, update, frames=frames, 
            interval=interval, blit=True, repeat=False
        )
        
        return anim
    
    def save_animation(self, filename='dem_simulation.gif', dt=0.001, 
                      steps_per_frame=10, frames=500, interval=20, dpi=80):
        """
        Save the simulation animation to a file.
        
        Args:
            filename (str): Output filename
            dt (float): Time step for simulation
            steps_per_frame (int): Number of simulation steps per animation frame
            frames (int): Total number of animation frames
            interval (int): Delay between frames in milliseconds
            dpi (int): Resolution of the output
        """
        anim = self.animate(dt, steps_per_frame, frames, interval)
        anim.save(filename, writer='pillow', dpi=dpi)
        print(f"Animation saved to {filename}")
