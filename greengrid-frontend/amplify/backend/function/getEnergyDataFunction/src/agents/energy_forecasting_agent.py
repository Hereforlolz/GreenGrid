class EnergyForecastingAgent:
    def __init__(self, sagemaker_client):
        self.sagemaker_client = sagemaker_client

    def forecast_power(self, input_data):
        # Example dummy forecast: add 1 kW to input power, or fixed if not present
        base_power = input_data.get("power_kW", 2.5)
        return base_power + 1.0
