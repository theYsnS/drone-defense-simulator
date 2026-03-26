# Anti-Drone Defense Simulator

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![PyGame](https://img.shields.io/badge/PyGame-2.5+-green.svg)](https://pygame.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)](https://opencv.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Simulation framework for counter-unmanned aerial system (C-UAS) defense strategies. Models drone detection, classification, tracking, and neutralization using radar simulation, computer vision, and electronic warfare concepts. Developed based on military defense research background.

## Features

- **Radar Simulation**: Simulated radar sweeps with configurable range, resolution, and noise
- **Drone Classification**: ML-based classification of drone types (quadcopter, fixed-wing, hybrid)
- **Threat Assessment**: Real-time threat scoring based on speed, altitude, trajectory, and proximity
- **Defense Zones**: Configurable multi-layer defense perimeters (detection, warning, engagement)
- **Electronic Warfare Sim**: RF jamming and GPS spoofing simulation modules
- **Trajectory Prediction**: Kalman filter-based flight path prediction
- **2D Visualization**: Real-time tactical display with PyGame
- **Scenario Engine**: Customizable attack scenarios for training and evaluation

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│ Scenario     │────▶│ Radar Sim    │────▶│ Detector &    │
│ Generator    │     │ (Range/Noise)│     │ Classifier    │
└─────────────┘     └──────────────┘     └───────┬───────┘
                                                  │
┌─────────────┐     ┌──────────────┐     ┌────────▼──────┐
│ Tactical     │◀───│ Defense      │◀───│ Threat        │
│ Display      │     │ Controller   │     │ Assessor      │
└─────────────┘     └──────────────┘     └───────────────┘
                           │
                    ┌──────▼───────┐
                    │ EW / Jammer  │
                    │ Simulation   │
                    └──────────────┘
```

## Installation

```bash
git clone https://github.com/theYsnS/drone-defense-simulator.git
cd drone-defense-simulator
pip install -r requirements.txt
```

## Usage

```bash
# Run simulation with default scenario
python main.py

# Custom scenario
python main.py --scenario config/scenarios/swarm_attack.yaml

# Headless mode (no visualization)
python main.py --headless --log results.json
```

## Scenarios

- `single_recon.yaml` — Single reconnaissance drone approach
- `swarm_attack.yaml` — Coordinated multi-drone swarm attack
- `high_altitude.yaml` — High-altitude surveillance drone
- `evasive_maneuver.yaml` — Drone with evasive flight patterns

## License

MIT License - see [LICENSE](LICENSE) for details.
