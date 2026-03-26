import math
from dataclasses import dataclass
from enum import Enum
from .radar import RadarContact

class ThreatLevel(str, Enum):
    CRITICAL = 'critical'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

@dataclass
class ThreatAssessment:
    contact_id: int
    threat_level: ThreatLevel
    score: float
    distance_to_base: float
    closing_speed: float
    predicted_eta: float
    classification: str
    recommended_action: str

class ThreatAssessor:
    def __init__(self, base_x=0, base_y=0, critical_radius=500, warning_radius=2000, detection_radius=5000):
        self.base_x = base_x
        self.base_y = base_y
        self.critical_radius = critical_radius
        self.warning_radius = warning_radius
        self.detection_radius = detection_radius

    def assess(self, contact):
        distance = math.sqrt((contact.x - self.base_x)**2 + (contact.y - self.base_y)**2)
        heading_rad = math.radians(contact.heading)
        to_base_x = self.base_x - contact.x
        to_base_y = self.base_y - contact.y
        closing = contact.speed * ((to_base_x * math.cos(heading_rad) + to_base_y * math.sin(heading_rad)) / max(distance, 0.1))
        eta = distance / max(closing, 0.1) if closing > 0 else float('inf')

        score = max(0, (1 - distance / self.detection_radius)) * 30
        score += min(contact.speed / 40, 1.0) * 20
        score += max(0, closing / 20) * 25
        score += (1 if contact.altitude < 200 else 0.3) * 15
        score += contact.rcs * 100

        if distance < self.critical_radius:
            level, action = ThreatLevel.CRITICAL, 'ENGAGE'
        elif distance < self.warning_radius:
            level, action = ThreatLevel.HIGH, 'PREPARE'
        elif closing > 5:
            level, action = ThreatLevel.MEDIUM, 'MONITOR'
        else:
            level, action = ThreatLevel.LOW, 'OBSERVE'

        classification = 'Nano UAV' if contact.rcs < 0.02 else 'Small Quadcopter' if contact.rcs < 0.06 and contact.speed < 25 else 'Fixed-Wing UAV' if contact.speed > 30 else 'Medium UAV'

        return ThreatAssessment(contact.contact_id, level, min(score, 100), distance, closing, eta, classification, action)
