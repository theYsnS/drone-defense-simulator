import math
from dataclasses import dataclass
from enum import Enum


class DroneType(str, Enum):
    QUADCOPTER = 'quadcopter'
    FIXED_WING = 'fixed_wing'
    HYBRID = 'hybrid'
    NANO = 'nano'


@dataclass
class DroneSpec:
    drone_type: DroneType
    max_speed: float
    max_altitude: float
    rcs: float
    weight_kg: float

DRONE_SPECS = {
    DroneType.QUADCOPTER: DroneSpec(DroneType.QUADCOPTER, 20, 500, 0.05, 2.5),
    DroneType.FIXED_WING: DroneSpec(DroneType.FIXED_WING, 40, 3000, 0.08, 5.0),
    DroneType.HYBRID: DroneSpec(DroneType.HYBRID, 30, 1500, 0.06, 3.5),
    DroneType.NANO: DroneSpec(DroneType.NANO, 10, 150, 0.01, 0.3),
}


class Drone:
    def __init__(self, drone_id, drone_type, start_x, start_y, start_alt=100):
        self.drone_id = drone_id
        self.spec = DRONE_SPECS[drone_type]
        self.x = start_x
        self.y = start_y
        self.altitude = start_alt
        self.speed = 0.0
        self.heading = 0.0
        self.is_active = True
        self._waypoints = []
        self._wp_index = 0

    def set_waypoints(self, waypoints):
        self._waypoints = waypoints
        self._wp_index = 0

    def update(self, dt):
        if not self.is_active or not self._waypoints:
            return self.state
        target = self._waypoints[self._wp_index]
        dx = target[0] - self.x
        dy = target[1] - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist < 5.0:
            self._wp_index = (self._wp_index + 1) % len(self._waypoints)
            return self.state
        self.heading = math.degrees(math.atan2(dy, dx))
        self.speed = min(self.spec.max_speed, dist / max(dt, 0.01))
        move = min(self.speed * dt, dist)
        self.x += (dx / dist) * move
        self.y += (dy / dist) * move
        return self.state

    @property
    def state(self):
        return {'id': self.drone_id, 'x': self.x, 'y': self.y, 'altitude': self.altitude,
                'speed': self.speed, 'heading': self.heading, 'rcs': self.spec.rcs,
                'type': self.spec.drone_type.value, 'active': self.is_active}

    def neutralize(self):
        self.is_active = False
        self.speed = 0
