"""
Particle class for DEM simulation
Represents a single particle with physical properties
"""
import numpy as np


class Particle:
    """
    A particle in the DEM simulation with position, velocity, and physical properties.
    """
    
    def __init__(self, x, y, radius, mass, particle_id):
        """
        Initialize a particle.
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            radius (float): Particle radius
            mass (float): Particle mass
            particle_id (int): Unique identifier for the particle
        """
        self.id = particle_id
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0], dtype=float)
        self.acceleration = np.array([0.0, 0.0], dtype=float)
        self.force = np.array([0.0, 0.0], dtype=float)
        self.radius = radius
        self.mass = mass
        
    def reset_force(self):
        """Reset the force acting on the particle to zero."""
        self.force = np.array([0.0, 0.0], dtype=float)
        
    def add_force(self, force):
        """
        Add a force to the particle.
        
        Args:
            force (numpy.ndarray): Force vector to add
        """
        self.force += force
        
    def update_acceleration(self):
        """Update acceleration based on current force (F = ma)."""
        self.acceleration = self.force / self.mass
        
    def update_velocity(self, dt):
        """
        Update velocity using current acceleration.
        
        Args:
            dt (float): Time step
        """
        self.velocity += self.acceleration * dt
        
    def update_position(self, dt):
        """
        Update position using current velocity.
        
        Args:
            dt (float): Time step
        """
        self.position += self.velocity * dt
