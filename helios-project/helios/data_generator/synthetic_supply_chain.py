"""Synthetic supply chain data generator with regime switching"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List
from enum import Enum

class DemandRegime(Enum):
    NORMAL = "normal"
    PEAK = "peak"
    RECESSION = "recession"
    DISRUPTION = "disruption"

@dataclass
class SKU:
    id: str
    category: str
    base_demand: float
    demand_volatility: float

@dataclass  
class Supplier:
    id: str
    region: str
    base_price: float
    capacity: float
    reliability: float
    carbon_intensity: float

class SupplyChainDataGenerator:
    def __init__(self, n_skus: int = 50, n_suppliers: int = 20, years: int = 3):
        self.n_skus = n_skus
        self.n_suppliers = n_suppliers
        self.years = years
        self.n_periods = years * 52
        self.skus: Dict[str, SKU] = {}
        self.suppliers: Dict[str, Supplier] = {}
        self._initialize()

    def _initialize(self):
        categories = ['electronics', 'apparel', 'food', 'industrial']
        for i in range(self.n_skus):
            self.skus[f"SKU_{i:03d}"] = SKU(
                id=f"SKU_{i:03d}",
                category=np.random.choice(categories),
                base_demand=np.random.lognormal(8, 1.5),
                demand_volatility=np.random.uniform(0.1, 0.4)
            )

        regions = ['NA', 'EU', 'APAC', 'LATAM']
        for i in range(self.n_suppliers):
            reliability = np.clip(np.random.beta(7, 2), 0.7, 0.99)
            self.suppliers[f"SUP_{i:03d}"] = Supplier(
                id=f"SUP_{i:03d}",
                region=np.random.choice(regions),
                base_price=np.random.lognormal(2, 0.5) * (1 + (reliability - 0.8) * 2),
                capacity=np.random.lognormal(10, 1),
                reliability=reliability,
                carbon_intensity=np.random.lognormal(0, 0.5)
            )

    def generate_demand(self) -> pd.DataFrame:
        demands = []
        for t in range(self.n_periods):
            for sku_id, sku in self.skus.items():
                base = sku.base_demand
                noise = np.random.gamma(1/sku.demand_volatility**2, sku.demand_volatility**2)
                demands.append({
                    'period': t,
                    'sku_id': sku_id,
                    'category': sku.category,
                    'demand': max(0, base * noise),
                    'regime': DemandRegime.NORMAL.value
                })
        return pd.DataFrame(demands)

    def generate_full_dataset(self) -> Dict:
        return {
            'demand': self.generate_demand(),
            'skus': self.skus,
            'suppliers': self.suppliers
        }
