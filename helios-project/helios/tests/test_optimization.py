"""Tests for optimization module"""

import pytest
import numpy as np
from helios.optimization.stochastic_mip import StochasticProcurementOptimizer, ProcurementState
from helios.data_generator.synthetic_supply_chain import SupplyChainDataGenerator

def test_data_generator():
    gen = SupplyChainDataGenerator(n_skus=5, n_suppliers=5, years=1)
    data = gen.generate_full_dataset()
    assert 'demand' in data
    assert len(data['skus']) == 5

def test_optimizer():
    gen = SupplyChainDataGenerator(n_skus=3, n_suppliers=3, years=1)
    opt = StochasticProcurementOptimizer(gen.skus, gen.suppliers, n_scenarios=10)

    state = ProcurementState(
        inventory={f"SKU_{i:03d}": 100 for i in range(3)},
        demand_forecast={f"SKU_{i:03d}": np.array([1000]*10) for i in range(3)}
    )

    result = opt.optimize(state, {'cost': 0.5, 'carbon': 0.3})
    assert 'orders' in result
