"""Tests for RL module"""

import pytest
import numpy as np
from helios.rl.env import ProcurementEnv

def test_env_creation():
    env = ProcurementEnv({}, n_skus=3, n_suppliers=3)
    obs, info = env.reset()
    assert 'inventory' in obs
    assert obs['inventory'].shape == (3,)

def test_env_step():
    env = ProcurementEnv({}, n_skus=3, n_suppliers=3)
    obs, _ = env.reset()
    action = np.array([0.5, 0.5, 0.5])
    obs, reward, terminated, truncated, info = env.step(action)
    assert isinstance(reward, float)
    assert not terminated
