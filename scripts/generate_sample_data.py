import csv
import random
import os
from pathlib import Path
from datetime import datetime, timedelta

def generate_data(file_path, num_rows=1000):
    # Ensure parent folder exists
    os.makedirs(file_path.parent, exist_ok=True)

    start_time = datetime.now()
    appliances = ["HVAC", "Washer", "Dryer", "Refrigerator", "Lighting"]

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'household_id', 'appliance', 'power_kW'])
        for i in range(num_rows):
            ts = start_time + timedelta(minutes=i)
            household_id = random.randint(1, 10)
            appliance = random.choice(appliances)
            power = round(random.uniform(0.1, 5.0), 2)
            writer.writerow([ts.isoformat(), household_id, appliance, power])

    print(f"✅ Generated {num_rows} rows in {file_path}")

if __name__ == "__main__":
    # This always resolves relative to this script’s folder
    script_dir = Path(__file__).parent.resolve()
    output_file = script_dir.parent / "data" / "sample_energy_usage.csv"

    print(f"Generating sample data at: {output_file}")
    generate_data(output_file)
    print(f"✅ Done generating data at: {output_file}")
