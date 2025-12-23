"""
DEM Simulation Engine
Implements the Discrete Element Method for particle simulation
"""
import numpy as np
from particle import Particle


class DEMSimulation:
    """
    Main DEM simulation engine that handles particle interactions and physics.
    """
    
    def __init__(self, width=10.0, height=10.0, gravity=9.81):
        """
        Initialize the DEM simulation.
        
        Args:
            width (float): Width of the simulation domain
            height (float): Height of the simulation domain
            gravity (float): Gravitational acceleration (m/s^2)
        """
        self.width = width
        self.height = height
        self.gravity = gravity
        self.particles = []
        self.time = 0.0
        
        # Material properties
        self.restitution_coeff = 0.8  # Coefficient of restitution
        self.friction_coeff = 0.3      # Coefficient of friction
        self.stiffness = 1e5           # Contact stiffness (N/m)
        self.damping = 0.3             # Damping coefficient
        
    def add_particle(self, x, y, radius, mass):
        """
        Add a particle to the simulation.
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            radius (float): Particle radius
            mass (float): Particle mass
            
        Returns:
            Particle: The created particle
        """
        particle_id = len(self.particles)
        particle = Particle(x, y, radius, mass, particle_id)
        self.particles.append(particle)
        return particle
        
    def apply_gravity(self):
        """Apply gravitational force to all particles."""
        for particle in self.particles:
            gravity_force = np.array([0.0, -particle.mass * self.gravity])
            particle.add_force(gravity_force)
            
    def check_particle_collision(self, p1, p2):
        """
        Check if two particles are colliding and compute contact force.
        
        Args:
            p1 (Particle): First particle
            p2 (Particle): Second particle
        """
        # Vector from p1 to p2
        delta = p2.position - p1.position
        distance = np.linalg.norm(delta)
        
        # Check if particles overlap
        overlap = (p1.radius + p2.radius) - distance
        if overlap > 0:
            # Normal direction
            normal = delta / distance if distance > 0 else np.array([1.0, 0.0])
            
            # Relative velocity
            relative_velocity = p2.velocity - p1.velocity
            
            # Normal component of relative velocity
            vn = np.dot(relative_velocity, normal)
            
            # Normal force (spring-damper model)
            normal_force_magnitude = self.stiffness * overlap - self.damping * vn
            normal_force = normal_force_magnitude * normal
            
            # Tangential component of relative velocity
            tangent = np.array([-normal[1], normal[0]])
            vt = np.dot(relative_velocity, tangent)
            
            # Tangential force (friction)
            tangent_force_magnitude = -self.friction_coeff * abs(normal_force_magnitude) * np.sign(vt)
            tangent_force = tangent_force_magnitude * tangent
            
            # Total contact force
            contact_force = normal_force + tangent_force
            
            # Apply equal and opposite forces
            p1.add_force(-contact_force)
            p2.add_force(contact_force)
            
    def check_wall_collision(self, particle):
        """
        Check and handle collision with walls.
        
        Args:
            particle (Particle): The particle to check
        """
        # Left wall
        if particle.position[0] - particle.radius < 0:
            overlap = particle.radius - particle.position[0]
            normal_force = self.stiffness * overlap - self.damping * particle.velocity[0]
            particle.add_force(np.array([normal_force, 0.0]))
            
        # Right wall
        if particle.position[0] + particle.radius > self.width:
            overlap = (particle.position[0] + particle.radius) - self.width
            normal_force = -self.stiffness * overlap - self.damping * particle.velocity[0]
            particle.add_force(np.array([normal_force, 0.0]))
            
        # Bottom wall
        if particle.position[1] - particle.radius < 0:
            overlap = particle.radius - particle.position[1]
            normal_force = self.stiffness * overlap - self.damping * particle.velocity[1]
            particle.add_force(np.array([0.0, normal_force]))
            
            # Add friction when in contact with bottom wall
            if overlap > 0:
                friction_force = -self.friction_coeff * abs(normal_force) * np.sign(particle.velocity[0])
                particle.add_force(np.array([friction_force, 0.0]))
                
        # Top wall
        if particle.position[1] + particle.radius > self.height:
            overlap = (particle.position[1] + particle.radius) - self.height
            normal_force = -self.stiffness * overlap - self.damping * particle.velocity[1]
            particle.add_force(np.array([0.0, normal_force]))
            
    def step(self, dt):
        """
        Perform one simulation step.
        
        Args:
            dt (float): Time step size
        """
        # Reset forces
        for particle in self.particles:
            particle.reset_force()
            
        # Apply gravity
        self.apply_gravity()
        
        # Check particle-particle collisions
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                self.check_particle_collision(self.particles[i], self.particles[j])
                
        # Check wall collisions
        for particle in self.particles:
            self.check_wall_collision(particle)
            
        # Update particles
        for particle in self.particles:
            particle.update_acceleration()
            particle.update_velocity(dt)
            particle.update_position(dt)
            
        self.time += dt
        
    def get_total_energy(self):
        """
        Calculate total energy (kinetic + potential) in the system.
        
        Returns:
            tuple: (kinetic_energy, potential_energy, total_energy)
        """
        kinetic = 0.0
        potential = 0.0
        
        for particle in self.particles:
            # Kinetic energy: 0.5 * m * v^2
            v_squared = np.dot(particle.velocity, particle.velocity)
            kinetic += 0.5 * particle.mass * v_squared
            
            # Potential energy: m * g * h
            potential += particle.mass * self.gravity * particle.position[1]
            
        return kinetic, potential, kinetic + potential
