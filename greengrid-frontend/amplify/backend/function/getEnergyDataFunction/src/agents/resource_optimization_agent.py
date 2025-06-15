class ResourceOptimizationAgent:
    def __init__(self, config):
        self.config = config

    def optimize(self, forecasted_data, constraints):
        """
        Dummy optimizer: limit each forecasted power to max_power_kW in constraints.
        """
        max_power = constraints.get("max_power_kW", 5.0)
        optimized = []
        for item in forecasted_data:
            adjusted = {
                "timestamp": item["timestamp"],
                "household_id": item["household_id"],
                "adjusted_power_kW": min(item["power_kW"], max_power)
            }
            optimized.append(adjusted)
        return optimized
