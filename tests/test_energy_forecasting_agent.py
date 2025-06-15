import pytest
from src.agents.energy_forecasting_agent import EnergyForecastingAgent

class DummySagemakerClient:
    def invoke_endpoint(self, *args, **kwargs):
        return {"prediction": 3.5}

def test_forecast_output():
    agent = EnergyForecastingAgent(sagemaker_client=DummySagemakerClient())
    sample_input = {
        "timestamp": "2025-06-15T08:00:00",
        "household_id": 1,
        "appliance": "HVAC",
        "power_kW": 2.5
    }
    prediction = agent.forecast_power(sample_input)
    assert isinstance(prediction, float)
    assert prediction >= 0
