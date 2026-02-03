"""Monte Carlo stress testing for supply chain resilience"""

import numpy as np
import pandas as pd
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class DisruptionScenario:
    name: str
    duration: int
    severity: float
    probability: float

class MonteCarloStressTester:
    """CVaR calculation and tail risk analysis"""

    def __init__(self, n_simulations: int = 10000):
        self.n_simulations = n_simulations

    def simulate_impact(self, scenario: DisruptionScenario, policy: Dict) -> np.ndarray:
        """Simulate financial impact over 52 weeks"""
        impacts = np.zeros(self.n_simulations)

        for sim in range(self.n_simulations):
            cost = 0
            inventory = policy.get('safety_stock', 500)

            for week in range(52):
                if week < scenario.duration:
                    capacity = 1 - scenario.severity
                else:
                    capacity = 1.0

                demand = np.random.lognormal(7, 0.5)
                available = policy.get('order_qty', 1000) * capacity

                fulfilled = min(demand, inventory + available)
                lost = demand - fulfilled

                cost += available * 25 + inventory * 0.1 + lost * 50
                inventory = max(0, inventory + available - demand)

            impacts[sim] = cost

        return impacts

    def calculate_cvar(self, losses: np.ndarray, alpha: float = 0.95) -> float:
        """Calculate Conditional Value at Risk"""
        var = np.percentile(losses, alpha * 100)
        return np.mean(losses[losses >= var])

    def run_stress_test(self, scenarios: List[DisruptionScenario], policy: Dict) -> pd.DataFrame:
        """Run comprehensive stress test"""
        results = []

        for scenario in scenarios:
            impacts = self.simulate_impact(scenario, policy)
            results.append({
                'scenario': scenario.name,
                'expected_cost': np.mean(impacts),
                'cvar_95': self.calculate_cvar(impacts, 0.95),
                'worst_case': np.max(impacts)
            })

        return pd.DataFrame(results)
