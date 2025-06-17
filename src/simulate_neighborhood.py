import random
from datetime import datetime, timedelta

def simulate_neighborhood_data(num_households=5, days=1, readings_per_day=24):
    """
    Simulate energy usage data for multiple households over a number of days.
    Returns a list of dicts with:
    - household_id
    - timestamp
    - energy_kWh
    """
    data = []
    start_time = datetime.now() - timedelta(days=days)

    for household_id in range(1, num_households + 1):
        for hour in range(readings_per_day * days):
            timestamp = start_time + timedelta(hours=hour)
            base_usage = random.uniform(0.5, 2.0)
            if 18 <= timestamp.hour <= 22:
                usage = base_usage + random.uniform(1.5, 3.0)
            else:
                usage = base_usage + random.uniform(0, 1.0)
            record = {
                "household_id": str(household_id),
                "timestamp": timestamp.isoformat(),
                "energy_kWh": round(usage, 3)
            }
            data.append(record)
    return data
