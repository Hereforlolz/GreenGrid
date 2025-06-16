class EnergyForecastingAgent:
    def __init__(self, sagemaker_client=None):
        self.sagemaker_client = sagemaker_client

    def forecast_power(self, usage_record):
        """
        Dummy forecast: Just return the current power_kW with a small random adjustment.
        Replace with ML model inference in production.
        """
        power = usage_record.get("power_kW", 0)
        # For example, a trivial forecast (could be improved)
        return power * 1.05  # +5% forecast bump for demo
