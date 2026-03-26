import logging
from dataclasses import dataclass
from enum import Enum
from .threat_assessor import ThreatAssessment, ThreatLevel

logger = logging.getLogger(__name__)

class CountermeasureType(str, Enum):
    RF_JAMMER = 'rf_jammer'
    GPS_SPOOFER = 'gps_spoofer'
    NET_CAPTURE = 'net_capture'

@dataclass
class CMStatus:
    cm_type: CountermeasureType
    is_active: bool
    target_id: int | None
    effective_range: float
    cooldown: float

class DefenseController:
    def __init__(self):
        self.countermeasures = {
            CountermeasureType.RF_JAMMER: CMStatus(CountermeasureType.RF_JAMMER, False, None, 2000, 0),
            CountermeasureType.GPS_SPOOFER: CMStatus(CountermeasureType.GPS_SPOOFER, False, None, 3000, 0),
            CountermeasureType.NET_CAPTURE: CMStatus(CountermeasureType.NET_CAPTURE, False, None, 200, 0),
        }
        self._log = []

    def respond(self, assessments):
        actions = []
        for t in sorted(assessments, key=lambda a: a.score, reverse=True):
            if t.threat_level == ThreatLevel.CRITICAL:
                a = self._engage(t, CountermeasureType.RF_JAMMER)
                if a: actions.append(a)
            elif t.threat_level == ThreatLevel.HIGH:
                a = self._engage(t, CountermeasureType.GPS_SPOOFER)
                if a: actions.append(a)
        return actions

    def _engage(self, threat, cm_type):
        cm = self.countermeasures.get(cm_type)
        if not cm or cm.is_active or cm.cooldown > 0 or threat.distance_to_base > cm.effective_range:
            return None
        cm.is_active = True
        cm.target_id = threat.contact_id
        action = {'action': 'ENGAGE', 'countermeasure': cm_type.value, 'target_id': threat.contact_id, 'threat_level': threat.threat_level.value}
        self._log.append(action)
        logger.warning('ENGAGING target %d with %s', threat.contact_id, cm_type.value)
        return action

    def release(self, cm_type, cooldown=10.0):
        cm = self.countermeasures.get(cm_type)
        if cm:
            cm.is_active = False
            cm.target_id = None
            cm.cooldown = cooldown
