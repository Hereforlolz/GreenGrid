import pytest
from src.agents.resource_optimization_agent import ResourceOptimizationAgent

def test_optimize_resources():
    dummy_config = {"some_config": True}
    agent = ResourceOptimizationAgent(config=dummy_config)
    forecasted_data = [
        {"timestamp": "2025-06-15T08:00:00", "household_id": 1, "power_kW": 3.2},
        {"timestamp": "2025-06-15T08:10:00", "household_id": 1, "power_kW": 2.8},
    ]
    constraints = {"max_power_kW": 5.0}
    plan = agent.optimize(forecasted_data, constraints)
    assert isinstance(plan, list)
    assert all("adjusted_power_kW" in item for item in plan)
    assert all(item["adjusted_power_kW"] <= constraints["max_power_kW"] for item in plan)
