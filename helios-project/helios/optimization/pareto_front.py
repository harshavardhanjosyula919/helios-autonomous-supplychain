"""Pareto frontier analysis for multi-objective optimization"""

import numpy as np
import pandas as pd
from typing import Dict, List

class ParetoFrontierAnalyzer:
    def __init__(self, optimizer):
        self.optimizer = optimizer
        self.frontier_points = []

    def compute_frontier(self, state, n_points: int = 10) -> pd.DataFrame:
        """Compute Pareto frontier by varying weights"""
        results = []

        for w_cost in np.linspace(0.1, 0.9, n_points):
            w_carbon = 1 - w_cost
            result = self.optimizer.optimize(state, {'cost': w_cost, 'carbon': w_carbon})
            result['weights'] = {'cost': w_cost, 'carbon': w_carbon}
            results.append(result)

        return pd.DataFrame(results)
