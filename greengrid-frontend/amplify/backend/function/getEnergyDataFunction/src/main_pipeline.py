import csv
import boto3 # Import boto3 for AWS services
import json # Import json for working with JSON data in Bedrock responses and Lambda output

# Import your agent classes
from agents.energy_forecasting_agent import EnergyForecastingAgent
from agents.resource_optimization_agent import ResourceOptimizationAgent
from agents.sustainability_insights_agent import SustainabilityInsightsAgent


def load_usage_data(file_path="data/sample_energy_usage.csv"):
    """
    Loads energy usage data from a CSV file.
    Args:
        file_path (str): The path to the CSV data file.
    Returns:
        list: A list of dictionaries, each representing a row of usage data.
    """
    data = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure power_kW is converted to float for calculations
                data.append({
                    "timestamp": row["timestamp"],
                    "household_id": row["household_id"],
                    "power_kW": float(row["power_kW"])
                })
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}. Please ensure 'data/sample_energy_usage.csv' exists.")
        return []
    except Exception as e:
        print(f"Error loading usage data: {e}")
        return []
    return data


def main():
    """
    Orchestrates the energy data processing pipeline:
    1. Initializes AWS Bedrock client.
    2. Loads simulated usage data.
    3. Forecasts energy usage.
    4. Optimizes resource allocation.
    5. Generates sustainability insights using Bedrock.
    6. Returns all processed data.
    """
    # --- AWS Boto3 Client Initialization for Bedrock ---
    # The Lambda's IAM role must have 'bedrock:InvokeModel' permissions
    bedrock_client = None
    try:
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1" # Ensure this matches the region where Bedrock is enabled
        )
        print("Bedrock client initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize Bedrock client: {e}. Please ensure AWS credentials are set up and Bedrock is available in your region. Insights generation might fail.")
        # If bedrock client fails, the insights agent will handle it gracefully.


    # === 1️⃣ Load raw usage data ===
    # For the hackathon, we're using a local CSV.
    # In a real system, this would come from an IoT data stream (e.g., Kinesis, S3).
    usage_data = load_usage_data("data/sample_energy_usage.csv")
    if not usage_data:
        # Return empty data if loading failed to prevent further errors
        return {
            "forecasted_data": [],
            "optimized_data": [],
            "sustainability_insights": {"recommendations": {"English": "No data loaded.", "Spanish": "No hay datos cargados.", "Bosnian": "Nema učitanih podataka."}}
        }

    # === 2️⃣ Forecast Energy Usage ===
    # Using a dummy agent. In production, this would use ML models (e.g., from SageMaker).
    forecast_agent = EnergyForecastingAgent(sagemaker_client=None) # sagemaker_client is a placeholder for now
    forecasted_data = []
    for item in usage_data:
        forecast = forecast_agent.forecast_power(item)
        forecasted_data.append({
            "timestamp": item["timestamp"],
            "household_id": item["household_id"],
            "power_kW": forecast
        })
    print("=== Forecasted Data ===")
    for row in forecasted_data[:5]: # Print first 5 rows for logs
        print(row)


    # === 3️⃣ Optimize Resource Allocation ===
    # Dummy optimizer applying a max power constraint.
    # Real optimization would be complex, considering grid conditions, incentives, etc.
    optimization_agent = ResourceOptimizationAgent(config={"max_power_kW": 5.0})
    # The constraint should typically come from configuration or a real-time signal
    optimized_data = optimization_agent.optimize(forecasted_data, constraints={"max_power_kW": 5.0})
    print("\n=== Optimized Data ===")
    for row in optimized_data[:5]: # Print first 5 rows for logs
        print(row)


    # === 4️⃣ Generate Sustainability Insights ===
    # Uses Bedrock (Claude 3 Sonnet) to generate human-friendly advice.
    insights_agent = SustainabilityInsightsAgent(
        bedrock_client=bedrock_client,
        config={
            "threshold": 5.0, # Used in dummy logic to determine if optimization occurred
            "target_languages": ["English", "Spanish", "Bosnian"]
        }
    )
    # Pass optimized_data for insights generation. You could also pass forecasted_data for richer context.
    insights = insights_agent.generate_insights(optimized_data)
    print("\n=== Sustainability Insights ===")
    print(json.dumps(insights, indent=2, ensure_ascii=False))


    # Return all processed data for the Lambda response
    return {
        "forecasted_data": forecasted_data,
        "optimized_data": optimized_data,
        "sustainability_insights": insights
    }


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    This is the entry point for your Lambda.
    It calls the main pipeline and formats the output for API Gateway.
    """
    print("Lambda function invoked!")
    
    try:
        # Call the main pipeline function to get all processed data
        result_data = main()
        print("Lambda execution finished.")
        
        # Return the data as a JSON string for API Gateway
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result_data) # Convert dictionary to JSON string
        }
    except Exception as e:
        # Catch any unexpected errors in the pipeline and return a 500 response
        print(f"Error during Lambda execution: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"message": "Internal Server Error", "error": str(e)})
        }


if __name__ == "__main__":
    # This block allows you to run main() locally for testing
    print("Running main() locally...")
    local_results = main()
    # You can print or process local_results here if needed
    # print("\nLocal Run Results:")
    # print(json.dumps(local_results, indent=2, ensure_ascii=False))