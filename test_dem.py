"""
Test script to verify DEM simulation works correctly
"""

import numpy as np
from particle import Particle
from dem_simulation import DEMSimulation


def test_particle_creation():
    """Test particle creation and basic properties"""
    print("Test 1: Particle creation...")
    p = Particle(5.0, 5.0, 0.5, 1.0, 1.0, -1.0)
    assert p.position[0] == 5.0
    assert p.position[1] == 5.0
    assert p.radius == 0.5
    assert p.mass == 1.0
    assert p.velocity[0] == 1.0
    assert p.velocity[1] == -1.0
    print("✓ Particle creation test passed")


def test_particle_force():
    """Test force application"""
    print("\nTest 2: Force application...")
    p = Particle(0, 0, 0.5, 1.0)
    p.reset_force()
    p.add_force(10.0, -5.0)
    assert p.force[0] == 10.0
    assert p.force[1] == -5.0
    print("✓ Force application test passed")


def test_particle_update():
    """Test particle position and velocity update"""
    print("\nTest 3: Particle update...")
    p = Particle(0, 0, 0.5, 1.0, 0, 0)
    p.add_force(10.0, 0)  # 10N force on 1kg mass = 10 m/s^2
    dt = 0.1
    p.update(dt)
    # After 0.1s with 10 m/s^2 acceleration: v = 1 m/s, x = 0.05 m
    assert abs(p.velocity[0] - 1.0) < 0.001
    assert abs(p.position[0] - 0.1) < 0.001
    print("✓ Particle update test passed")


def test_simulation_creation():
    """Test simulation creation"""
    print("\nTest 4: Simulation creation...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=-9.81)
    assert sim.width == 10.0
    assert sim.height == 10.0
    assert sim.gravity == -9.81
    assert len(sim.particles) == 0
    print("✓ Simulation creation test passed")


def test_add_particle_to_simulation():
    """Test adding particles to simulation"""
    print("\nTest 5: Adding particles to simulation...")
    sim = DEMSimulation()
    p1 = Particle(1, 1, 0.5, 1.0)
    p2 = Particle(2, 2, 0.5, 1.0)
    sim.add_particle(p1)
    sim.add_particle(p2)
    assert len(sim.particles) == 2
    print("✓ Adding particles test passed")


def test_gravity():
    """Test gravity application"""
    print("\nTest 6: Gravity application...")
    sim = DEMSimulation(gravity=-10.0)
    p = Particle(5, 5, 0.5, 2.0)
    sim.add_particle(p)
    p.reset_force()
    sim.apply_gravity()
    # Force should be mass * gravity = 2.0 * -10.0 = -20.0
    assert abs(p.force[1] - (-20.0)) < 0.001
    print("✓ Gravity application test passed")


def test_simulation_step():
    """Test simulation step with a single falling particle"""
    print("\nTest 7: Simulation step...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=-10.0)
    p = Particle(5, 5, 0.5, 1.0, 0, 0)
    sim.add_particle(p)
    
    initial_y = p.position[1]
    initial_vy = p.velocity[1]
    
    # Run one step
    dt = 0.1
    sim.step(dt)
    
    # Particle should have moved down and gained downward velocity
    assert p.position[1] < initial_y
    assert p.velocity[1] < initial_vy
    print("✓ Simulation step test passed")


def test_boundary_collision():
    """Test boundary collision detection"""
    print("\nTest 8: Boundary collision...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=0)
    p = Particle(0.2, 0.2, 0.5, 1.0, -2.0, -2.0)  # Moving towards bottom-left corner
    sim.add_particle(p)
    
    # Run multiple steps
    for _ in range(20):
        sim.step(0.05)
    
    # Particle should stay within bounds
    assert p.position[0] >= p.radius
    assert p.position[0] <= sim.width - p.radius
    assert p.position[1] >= p.radius
    assert p.position[1] <= sim.height - p.radius
    print("✓ Boundary collision test passed")


def test_particle_collision():
    """Test particle-particle collision"""
    print("\nTest 9: Particle-particle collision...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=0)
    # Create two particles that will collide
    p1 = Particle(5, 5, 0.5, 1.0, 1.0, 0)
    p2 = Particle(7, 5, 0.5, 1.0, -1.0, 0)
    sim.add_particle(p1)
    sim.add_particle(p2)
    
    # Run simulation
    for _ in range(50):
        sim.step(0.01)
    
    # Particles should have bounced off each other
    # Check that they're not overlapping significantly
    distance = np.linalg.norm(p2.position - p1.position)
    assert distance >= (p1.radius + p2.radius) * 0.9  # Allow small overlap
    print("✓ Particle collision test passed")


def test_get_particle_data():
    """Test getting particle data for visualization"""
    print("\nTest 10: Get particle data...")
    sim = DEMSimulation()
    p1 = Particle(1, 2, 0.3, 1.0)
    p2 = Particle(3, 4, 0.5, 1.0)
    sim.add_particle(p1)
    sim.add_particle(p2)
    
    positions, radii = sim.get_particle_data()
    assert positions.shape == (2, 2)
    assert radii.shape == (2,)
    assert np.allclose(positions[0], [1, 2])
    assert np.allclose(positions[1], [3, 4])
    assert radii[0] == 0.3
    assert radii[1] == 0.5
    print("✓ Get particle data test passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("DEM Simulation Test Suite")
    print("=" * 60)
    
    try:
        test_particle_creation()
        test_particle_force()
        test_particle_update()
        test_simulation_creation()
        test_add_particle_to_simulation()
        test_gravity()
        test_simulation_step()
        test_boundary_collision()
        test_particle_collision()
        test_get_particle_data()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
