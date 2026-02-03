"""Gymnasium environment for supply chain RL"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Dict, Tuple

class ProcurementEnv(gym.Env):
    """Multi-period procurement environment"""

    metadata = {'render_modes': ['human']}

    def __init__(self, config: Dict, n_skus: int = 5, n_suppliers: int = 5):
        super().__init__()

        self.n_skus = n_skus
        self.n_suppliers = n_suppliers

        self.action_space = spaces.Box(low=0, high=1, shape=(n_suppliers,), dtype=np.float32)

        self.observation_space = spaces.Dict({
            'inventory': spaces.Box(low=0, high=1e6, shape=(n_skus,), dtype=np.float32),
            'forecast': spaces.Box(low=0, high=1e6, shape=(4,), dtype=np.float32),
        })

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.inventory = np.ones(self.n_skus) * 500
        self.period = 0
        return self._get_obs(), {}

    def _get_obs(self):
        return {
            'inventory': self.inventory.astype(np.float32),
            'forecast': np.ones(4) * 1000
        }

    def step(self, action):
        order_qty = action * 1000
        demand = np.random.normal(1000, 100)

        self.inventory += order_qty.sum() / self.n_skus
        sales = min(self.inventory.sum(), demand)
        self.inventory -= sales / self.n_skus

        reward = sales * 10 - order_qty.sum() * 5 - self.inventory.sum() * 0.1
        self.period += 1

        terminated = self.period >= 52
        truncated = False

        return self._get_obs(), reward, terminated, truncated, {}
