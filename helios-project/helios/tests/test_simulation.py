"""Tests for simulation module"""

import pytest
from helios.simulation.stress_tests import MonteCarloStressTester, DisruptionScenario
from helios.simulation.game_theory import SupplierGameSimulator
from helios.data_generator.synthetic_supply_chain import SupplyChainDataGenerator

def test_stress_tester():
    tester = MonteCarloStressTester(n_simulations=100)
    scenario = DisruptionScenario("Test", 5, 0.5, 0.1)
    policy = {'order_qty': 1000, 'safety_stock': 500}

    impacts = tester.simulate_impact(scenario, policy)
    assert len(impacts) == 100
    assert impacts.mean() > 0

def test_game_theory():
    gen = SupplyChainDataGenerator(n_skus=2, n_suppliers=3, years=1)
    game = SupplierGameSimulator(gen.suppliers, demand_forecast=10000)
    equilibrium = game.find_equilibrium(max_iter=5)
    assert len(equilibrium) == 3
