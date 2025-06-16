class ResourceOptimizationAgent:
    def __init__(self, config=None):
        self.config = config or {}

    def optimize(self, forecasted_data, constraints=None):
        """
        Dummy optimization: enforce max_power_kW limit.
        Real optimization would consider grid constraints, etc.
        """
        max_power = None
        if constraints:
            max_power = constraints.get("max_power_kW")
        optimized = []
        for row in forecasted_data:
            power = row.get("power_kW", 0)
            if max_power is not None and power > max_power:
                power = max_power
            optimized.append({
                "timestamp": row.get("timestamp"),
                "household_id": row.get("household_id"),
                "power_kW": power
            })
        return optimized
