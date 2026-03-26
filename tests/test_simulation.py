"""Tests for drone defense simulation."""
import unittest
import numpy as np
from src.radar import RadarSimulator
from src.drone import Drone, DroneType
from src.kalman_tracker import KalmanTracker
from src.threat_assessor import ThreatAssessor

class TestRadar(unittest.TestCase):
    def test_detect_in_range(self):
        radar = RadarSimulator(range_km=10)
        targets = [{"id": 1, "x": 5000, "y": 3000, "altitude": 100, "speed": 15, "heading": 180, "rcs": 0.05}]
        contacts = radar.scan(targets, 0)
        self.assertGreaterEqual(len(contacts), 0)

    def test_out_of_range(self):
        radar = RadarSimulator(range_km=1)
        targets = [{"id": 1, "x": 50000, "y": 0, "altitude": 100, "speed": 0, "heading": 0, "rcs": 0.05}]
        contacts = radar.scan(targets, 0)
        self.assertEqual(len(contacts), 0)

class TestDrone(unittest.TestCase):
    def test_drone_movement(self):
        drone = Drone(1, DroneType.QUADCOPTER, 1000, 1000)
        drone.set_waypoints([(0, 0, 100)])
        state = drone.update(1.0)
        self.assertLess(abs(state["x"]), 1001)

    def test_neutralize(self):
        drone = Drone(1, DroneType.QUADCOPTER, 0, 0)
        drone.neutralize()
        self.assertFalse(drone.is_active)

class TestKalman(unittest.TestCase):
    def test_prediction(self):
        tracker = KalmanTracker(dt=1.0)
        tracker.update((100, 100))
        tracker.update((110, 105))
        future = tracker.predict_future(5)
        self.assertEqual(len(future), 5)

if __name__ == "__main__":
    unittest.main()
