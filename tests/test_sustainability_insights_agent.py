import pytest
from src.agents.sustainability_insights_agent import SustainabilityInsightsAgent

def test_generate_insights():
    dummy_config = {"some_config": True}
    agent = SustainabilityInsightsAgent(config=dummy_config)
    usage_data = [
        {"timestamp": "2025-06-15T08:00:00", "household_id": 1, "power_kW": 4.5},
        {"timestamp": "2025-06-15T09:00:00", "household_id": 1, "power_kW": 2.1},
    ]
    insights = agent.generate_insights(usage_data)
    assert isinstance(insights, dict)
    assert "recommendations" in insights
    assert isinstance(insights["recommendations"], list)
    assert len(insights["recommendations"]) > 0
