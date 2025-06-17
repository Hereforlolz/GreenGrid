from simulate_neighborhood import simulate_neighborhood_data
from dynamo_utils import save_energy_data
import boto3
import json

def main():
    print("Starting main pipeline...")

    # Use the GreenGrid profile and region explicitly for safety
    session = boto3.Session(profile_name='GreenGrid', region_name='us-east-1')
    dynamodb = session.resource('dynamodb')

    # Simulate data
    print("Simulating neighborhood energy data...")
    simulated_data = simulate_neighborhood_data(num_households=10, days=2, readings_per_day=24)
    print(f"Generated {len(simulated_data)} records.")

    # Show a sample
    print(json.dumps(simulated_data[:5], indent=2))

    # Save data to DynamoDB
    print("Saving simulated data to DynamoDB...")
    save_energy_data(simulated_data, table_name="EnergyUsage")

    print("Done.")

if __name__ == "__main__":
    main()
