"""Simulated radar system for drone detection."""

import math
import random
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class RadarContact:
    contact_id: int
    x: float
    y: float
    altitude: float
    speed: float
    heading: float
    rcs: float  # radar cross section
    signal_strength: float
    timestamp: float


class RadarSimulator:
    """Simulate a surveillance radar with configurable parameters."""

    def __init__(
        self,
        range_km: float = 10.0,
        resolution_m: float = 5.0,
        rotation_speed: float = 12.0,  # RPM
        noise_factor: float = 0.1,
        min_rcs: float = 0.01,
    ):
        self.range_km = range_km
        self.resolution_m = resolution_m
        self.rotation_speed = rotation_speed
        self.noise_factor = noise_factor
        self.min_rcs = min_rcs
        self._scan_angle = 0.0
        self._contacts: dict[int, RadarContact] = {}
        self._next_id = 0

    def scan(self, targets: list[dict], timestamp: float) -> list[RadarContact]:
        """Perform radar sweep and detect targets."""
        self._scan_angle = (self._scan_angle + self.rotation_speed * 6) % 360
        detected = []

        for target in targets:
            distance = math.sqrt(target["x"] ** 2 + target["y"] ** 2) / 1000
            if distance > self.range_km:
                continue

            rcs = target.get("rcs", 0.05)
            if rcs < self.min_rcs:
                continue

            detection_prob = self._calculate_detection_probability(distance, rcs)
            if random.random() > detection_prob:
                continue

            noise_x = random.gauss(0, self.noise_factor * self.resolution_m)
            noise_y = random.gauss(0, self.noise_factor * self.resolution_m)

            contact = RadarContact(
                contact_id=self._get_or_assign_id(target),
                x=target["x"] + noise_x,
                y=target["y"] + noise_y,
                altitude=target.get("altitude", 100) + random.gauss(0, 2),
                speed=target.get("speed", 0),
                heading=target.get("heading", 0),
                rcs=rcs,
                signal_strength=self._signal_strength(distance, rcs),
                timestamp=timestamp,
            )
            detected.append(contact)
            self._contacts[contact.contact_id] = contact

        return detected

    def _calculate_detection_probability(self, distance_km: float, rcs: float) -> float:
        base = min(1.0, (rcs / 0.01) * (self.range_km / max(distance_km, 0.1)) ** 2)
        return min(0.99, base * 0.95)

    def _signal_strength(self, distance_km: float, rcs: float) -> float:
        return rcs / (distance_km ** 4 + 0.001)

    def _get_or_assign_id(self, target: dict) -> int:
        tid = target.get("id")
        if tid is not None:
            return tid
        self._next_id += 1
        return self._next_id
