"""Game-theoretic supplier behavior modeling"""

import numpy as np
from typing import Dict
from dataclasses import dataclass

@dataclass
class SupplierStrategy:
    price_markup: float
    capacity_allocation: float

class SupplierGameSimulator:
    """Nash equilibrium computation for supplier competition"""

    def __init__(self, suppliers: Dict, demand_forecast: float):
        self.suppliers = suppliers
        self.demand_forecast = demand_forecast

    def payoff(self, supplier_id: str, strategy: SupplierStrategy, others: Dict) -> float:
        """Calculate supplier payoff given strategies"""
        sup = self.suppliers[supplier_id]
        price = sup.base_price * (1 + strategy.price_markup)
        capacity = sup.capacity * strategy.capacity_allocation

        utilities = {sid: -(s.base_price * (1 + others.get(sid, SupplierStrategy(0.1, 0.8)).price_markup)) 
                    for sid, s in self.suppliers.items()}
        utilities[supplier_id] = -price

        exp_utils = {k: np.exp(u) for k, u in utilities.items()}
        market_share = exp_utils[supplier_id] / sum(exp_utils.values())

        volume = min(self.demand_forecast * market_share, capacity)
        revenue = volume * price
        cost = volume * sup.base_price * 0.7

        return revenue - cost

    def find_equilibrium(self, max_iter: int = 20) -> Dict[str, SupplierStrategy]:
        """Find Nash equilibrium via best response iteration"""
        strategies = {sid: SupplierStrategy(0.1, 0.8) for sid in self.suppliers}

        for _ in range(max_iter):
            for sid in self.suppliers:
                others = {k: v for k, v in strategies.items() if k != sid}
                best_payoff = float('-inf')
                best_strategy = strategies[sid]

                for markup in [0.0, 0.1, 0.2, 0.3]:
                    strategy = SupplierStrategy(markup, 0.8)
                    payoff = self.payoff(sid, strategy, others)
                    if payoff > best_payoff:
                        best_payoff = payoff
                        best_strategy = strategy

                strategies[sid] = best_strategy

        return strategies
