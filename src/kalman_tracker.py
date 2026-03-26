import numpy as np

class KalmanTracker:
    def __init__(self, dt=1.0):
        self.dt = dt
        self.state = np.zeros(4)
        self.P = np.eye(4) * 1000
        self.F = np.array([[1,0,dt,0],[0,1,0,dt],[0,0,1,0],[0,0,0,1]])
        self.H = np.array([[1,0,0,0],[0,1,0,0]])
        self.R = np.eye(2) * 10
        self.Q = np.eye(4) * 0.1
        self._init = False

    def update(self, measurement):
        z = np.array(measurement)
        if not self._init:
            self.state[:2] = z
            self._init = True
            return self.state.copy()
        self.state = self.F @ self.state
        self.P = self.F @ self.P @ self.F.T + self.Q
        y = z - self.H @ self.state
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.state += K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P
        return self.state.copy()

    def predict_future(self, steps=10):
        positions = []
        state = self.state.copy()
        for _ in range(steps):
            state = self.F @ state
            positions.append((float(state[0]), float(state[1])))
        return positions
