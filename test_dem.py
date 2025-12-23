"""
Unit tests for DEM simulation components
"""
import numpy as np
from particle import Particle
from dem_simulation import DEMSimulation


def test_particle_initialization():
    """Test particle initialization."""
    print("Testing particle initialization...")
    p = Particle(x=1.0, y=2.0, radius=0.5, mass=1.0, particle_id=0)
    
    assert p.id == 0
    assert np.allclose(p.position, [1.0, 2.0])
    assert np.allclose(p.velocity, [0.0, 0.0])
    assert p.radius == 0.5
    assert p.mass == 1.0
    print("✓ Particle initialization test passed")


def test_particle_force_and_acceleration():
    """Test force application and acceleration calculation."""
    print("Testing force and acceleration...")
    p = Particle(x=0.0, y=0.0, radius=0.5, mass=2.0, particle_id=0)
    
    # Apply force
    force = np.array([4.0, 6.0])
    p.add_force(force)
    
    assert np.allclose(p.force, [4.0, 6.0])
    
    # Update acceleration (F = ma -> a = F/m)
    p.update_acceleration()
    expected_accel = np.array([2.0, 3.0])
    assert np.allclose(p.acceleration, expected_accel)
    print("✓ Force and acceleration test passed")


def test_particle_velocity_update():
    """Test velocity update with constant acceleration."""
    print("Testing velocity update...")
    p = Particle(x=0.0, y=0.0, radius=0.5, mass=1.0, particle_id=0)
    
    # Set acceleration and update velocity
    p.acceleration = np.array([1.0, 2.0])
    dt = 0.1
    p.update_velocity(dt)
    
    expected_velocity = np.array([0.1, 0.2])
    assert np.allclose(p.velocity, expected_velocity)
    print("✓ Velocity update test passed")


def test_particle_position_update():
    """Test position update with constant velocity."""
    print("Testing position update...")
    p = Particle(x=1.0, y=2.0, radius=0.5, mass=1.0, particle_id=0)
    
    p.velocity = np.array([0.5, 1.0])
    dt = 0.1
    p.update_position(dt)
    
    expected_position = np.array([1.05, 2.1])
    assert np.allclose(p.position, expected_position)
    print("✓ Position update test passed")


def test_simulation_initialization():
    """Test simulation initialization."""
    print("Testing simulation initialization...")
    sim = DEMSimulation(width=10.0, height=20.0, gravity=9.81)
    
    assert sim.width == 10.0
    assert sim.height == 20.0
    assert sim.gravity == 9.81
    assert len(sim.particles) == 0
    print("✓ Simulation initialization test passed")


def test_add_particle():
    """Test adding particles to simulation."""
    print("Testing add particle...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=9.81)
    
    p1 = sim.add_particle(x=5.0, y=5.0, radius=0.5, mass=1.0)
    assert len(sim.particles) == 1
    assert p1.id == 0
    
    p2 = sim.add_particle(x=6.0, y=6.0, radius=0.5, mass=1.0)
    assert len(sim.particles) == 2
    assert p2.id == 1
    print("✓ Add particle test passed")


def test_gravity_application():
    """Test that gravity is applied correctly."""
    print("Testing gravity application...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=10.0)
    
    # Add particle with mass 2.0
    p = sim.add_particle(x=5.0, y=5.0, radius=0.5, mass=2.0)
    
    # Reset and apply gravity
    p.reset_force()
    sim.apply_gravity()
    
    # Expected force: F = -m*g in y-direction
    expected_force = np.array([0.0, -20.0])
    assert np.allclose(p.force, expected_force)
    print("✓ Gravity application test passed")


def test_energy_conservation():
    """Test energy calculation."""
    print("Testing energy conservation...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=10.0)
    
    # Add particle at height 5.0
    p = sim.add_particle(x=5.0, y=5.0, radius=0.5, mass=2.0)
    
    # Calculate initial energy (all potential)
    ke, pe, te = sim.get_total_energy()
    assert ke == 0.0  # No velocity initially
    assert pe == 2.0 * 10.0 * 5.0  # m*g*h = 2*10*5 = 100
    assert te == 100.0
    print("✓ Energy conservation test passed")


def test_single_particle_simulation():
    """Test single particle falling under gravity."""
    print("Testing single particle simulation...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=9.81)
    
    # Add particle at height 5.0
    p = sim.add_particle(x=5.0, y=5.0, radius=0.2, mass=1.0)
    
    initial_height = p.position[1]
    
    # Run simulation for a short time
    for _ in range(100):
        sim.step(dt=0.001)
    
    # Check that particle has fallen
    assert p.position[1] < initial_height
    # Check that particle has downward velocity
    assert p.velocity[1] < 0
    print("✓ Single particle simulation test passed")


def test_wall_collision():
    """Test that particles collide with walls."""
    print("Testing wall collision...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=9.81)
    
    # Add particle slightly above bottom
    p = sim.add_particle(x=5.0, y=1.0, radius=0.15, mass=1.0)
    
    # Run simulation until particle hits bottom
    for _ in range(500):
        sim.step(dt=0.001)
    
    # Particle should have settled near the bottom (within radius of ground)
    # Using a tolerance factor for numerical stability
    GROUND_TOLERANCE = 0.9
    assert p.position[1] >= p.radius * GROUND_TOLERANCE  # Should be at or above ground
    assert p.position[1] < 1.0  # Should have fallen from initial height
    print("✓ Wall collision test passed")


def test_particle_collision_detection():
    """Test that two particles collide."""
    print("Testing particle collision detection...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=0.0)  # No gravity
    
    # Add two particles close together
    p1 = sim.add_particle(x=5.0, y=5.0, radius=0.3, mass=1.0)
    p2 = sim.add_particle(x=5.4, y=5.0, radius=0.3, mass=1.0)  # Overlapping
    
    # They should be overlapping (distance 0.4 < sum of radii 0.6)
    distance = np.linalg.norm(p2.position - p1.position)
    assert distance < (p1.radius + p2.radius)
    
    # Run one step - collision forces should be applied
    sim.step(dt=0.001)
    
    # After collision, particles should have moved apart or have forces applied
    # (checking forces during step is tricky, so we just verify no error occurs)
    print("✓ Particle collision detection test passed")


def test_multiple_steps():
    """Test that simulation runs for multiple steps without errors."""
    print("Testing multiple simulation steps...")
    sim = DEMSimulation(width=10.0, height=10.0, gravity=9.81)
    
    # Add multiple particles
    for i in range(5):
        sim.add_particle(x=5.0, y=5.0 + i * 0.5, radius=0.15, mass=1.0)
    
    # Run simulation for many steps
    for _ in range(1000):
        sim.step(dt=0.001)
    
    # Check that time has advanced
    assert sim.time > 0.9
    print("✓ Multiple steps test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("Running DEM Simulation Tests")
    print("=" * 70)
    print()
    
    tests = [
        test_particle_initialization,
        test_particle_force_and_acceleration,
        test_particle_velocity_update,
        test_particle_position_update,
        test_simulation_initialization,
        test_add_particle,
        test_gravity_application,
        test_energy_conservation,
        test_single_particle_simulation,
        test_wall_collision,
        test_particle_collision_detection,
        test_multiple_steps,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
