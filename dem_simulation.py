"""
DEM (Discrete Element Method) Simulation Engine
Handles particle interactions, collisions, and physics
"""

import numpy as np
from particle import Particle


class DEMSimulation:
    """DEM simulation engine"""
    
    def __init__(self, width=10.0, height=10.0, gravity=-9.81):
        """
        Initialize the DEM simulation
        
        Args:
            width (float): Simulation domain width
            height (float): Simulation domain height
            gravity (float): Gravitational acceleration (default: -9.81 m/s^2)
        """
        self.width = width
        self.height = height
        self.gravity = gravity
        self.particles = []
        
        # Contact parameters
        self.k_n = 1000.0  # Normal stiffness
        self.k_t = 800.0   # Tangential stiffness
        self.damping = 0.3  # Damping coefficient
        self.friction = 0.5  # Friction coefficient
        self.restitution = 0.8  # Coefficient of restitution
    
    def add_particle(self, particle):
        """Add a particle to the simulation"""
        self.particles.append(particle)
    
    def apply_gravity(self):
        """Apply gravitational force to all particles"""
        for particle in self.particles:
            particle.add_force(0, particle.mass * self.gravity)
    
    def detect_and_resolve_collisions(self):
        """Detect and resolve particle-particle collisions"""
        n = len(self.particles)
        
        # Check all pairs of particles
        for i in range(n):
            for j in range(i + 1, n):
                p1 = self.particles[i]
                p2 = self.particles[j]
                
                # Calculate distance between particles
                delta = p2.position - p1.position
                distance = np.linalg.norm(delta)
                
                # Check if particles overlap
                min_distance = p1.radius + p2.radius
                if distance < min_distance:
                    # Particles are colliding
                    overlap = min_distance - distance
                    
                    # Normal direction
                    if distance > 0:
                        normal = delta / distance
                    else:
                        # If particles are at same position, use random direction
                        normal = np.array([1.0, 0.0])
                    
                    # Calculate normal force (spring-damper model)
                    relative_velocity = p2.velocity - p1.velocity
                    normal_velocity = np.dot(relative_velocity, normal)
                    
                    # Normal force
                    force_magnitude = self.k_n * overlap - self.damping * normal_velocity
                    force = force_magnitude * normal
                    
                    # Apply forces (Newton's third law)
                    p1.add_force(-force[0], -force[1])
                    p2.add_force(force[0], force[1])
    
    def handle_boundary_collisions(self):
        """Handle collisions with domain boundaries"""
        for particle in self.particles:
            # Bottom boundary
            if particle.position[1] - particle.radius < 0:
                overlap = particle.radius - particle.position[1]
                particle.add_force(0, self.k_n * overlap)
                particle.velocity[1] *= -self.restitution
                particle.position[1] = particle.radius
            
            # Top boundary
            if particle.position[1] + particle.radius > self.height:
                overlap = particle.position[1] + particle.radius - self.height
                particle.add_force(0, -self.k_n * overlap)
                particle.velocity[1] *= -self.restitution
                particle.position[1] = self.height - particle.radius
            
            # Left boundary
            if particle.position[0] - particle.radius < 0:
                overlap = particle.radius - particle.position[0]
                particle.add_force(self.k_n * overlap, 0)
                particle.velocity[0] *= -self.restitution
                particle.position[0] = particle.radius
            
            # Right boundary
            if particle.position[0] + particle.radius > self.width:
                overlap = particle.position[0] + particle.radius - self.width
                particle.add_force(-self.k_n * overlap, 0)
                particle.velocity[0] *= -self.restitution
                particle.position[0] = self.width - particle.radius
    
    def step(self, dt):
        """
        Perform one simulation time step
        
        Args:
            dt (float): Time step size
        """
        # Reset forces
        for particle in self.particles:
            particle.reset_force()
        
        # Apply forces
        self.apply_gravity()
        self.detect_and_resolve_collisions()
        self.handle_boundary_collisions()
        
        # Update particle positions and velocities
        for particle in self.particles:
            particle.update(dt)
    
    def get_particle_data(self):
        """
        Get current particle positions and radii for visualization
        
        Returns:
            tuple: (positions, radii) as numpy arrays
        """
        positions = np.array([p.position for p in self.particles])
        radii = np.array([p.radius for p in self.particles])
        return positions, radii
