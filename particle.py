"""
Particle class for DEM simulation
Represents a single particle with physical properties
"""

import numpy as np


class Particle:
    """A particle in the DEM simulation"""
    
    def __init__(self, x, y, radius, mass, vx=0.0, vy=0.0):
        """
        Initialize a particle
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            radius (float): Particle radius
            mass (float): Particle mass
            vx (float): Initial x velocity
            vy (float): Initial y velocity
        """
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([vx, vy], dtype=float)
        self.radius = radius
        self.mass = mass
        self.force = np.array([0.0, 0.0], dtype=float)
    
    def reset_force(self):
        """Reset forces acting on the particle"""
        self.force = np.array([0.0, 0.0], dtype=float)
    
    def add_force(self, fx, fy):
        """Add force to the particle"""
        self.force[0] += fx
        self.force[1] += fy
    
    def update(self, dt):
        """
        Update particle position and velocity using Euler integration
        
        Args:
            dt (float): Time step
        """
        # Update velocity: v = v + a*dt
        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        
        # Update position: x = x + v*dt
        self.position += self.velocity * dt
