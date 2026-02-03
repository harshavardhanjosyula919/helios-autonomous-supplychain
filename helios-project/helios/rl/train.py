"""RL training using Ray RLlib"""

import ray
from ray.rllib.algorithms.ppo import PPOConfig
from typing import Dict

def train_procurement_agent(env_class, config: Dict, iterations: int = 100):
    """Train PPO agent for procurement optimization"""
    ray.init(ignore_reinit_error=True)

    rllib_config = (
        PPOConfig()
        .environment(env_class, env_config=config)
        .framework('torch')
        .rollouts(num_rollout_workers=2)
        .training(model={'fcnet_hiddens': [128, 128]})
    )

    algo = rllib_config.build()

    for i in range(iterations):
        result = algo.train()
        if i % 10 == 0:
            print(f"Iteration {i}: reward = {result['episode_reward_mean']:.2f}")

    checkpoint = algo.save("models/procurement_agent")
    ray.shutdown()
    return algo
