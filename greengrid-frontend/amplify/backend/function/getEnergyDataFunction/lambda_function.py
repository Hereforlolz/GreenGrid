import boto3
import json
import os # To get AWS_REGION if needed, though 'us-east-1' is a common default

# === EnergyForecastingAgent Class ===
# This class was originally in energy_forecasting_agent.py
class EnergyForecastingAgent:
    def __init__(self, sagemaker_client):
        self.sagemaker_client = sagemaker_client

    def forecast_power(self, input_data):
        # Example dummy forecast: add 1 kW to input power, or fixed if not present
        base_power = input_data.get("power_kW", 2.5)
        return base_power + 1.0

# === ResourceOptimizationAgent Class ===
# This class was originally in resource_optimization_agent.py
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

# === SustainabilityInsightsAgent Class ===
# This class was originally in sustainability_insights_agent.py
class SustainabilityInsightsAgent:
    def __init__(self, bedrock_client, config): # Added bedrock_client to init
        self.bedrock_client = bedrock_client
        self.config = config

    def generate_insights(self, usage_data):
        """
        Dummy insights: check average adjusted power vs threshold.
        For Bedrock integration, you'd make an API call here.
        """
        if not usage_data:
            return {"recommendations": []}

        avg_power = sum(d["adjusted_power_kW"] for d in usage_data) / len(usage_data)
        threshold = self.config.get("threshold", 3.0)

        recommendations = []
        if avg_power > threshold:
            recommendations.append("Reduce peak usage")
            recommendations.append("Use smart thermostat")

        # Example of how you would use bedrock_client if you were generating insights with LLM
        # For hackathon, we're keeping it simple for now, as the dummy logic covers it.
        # This part is commented out for simplicity in this example
        # try:
        #     # Example bedrock call (replace with your actual prompt and model)
        #     model_id = "anthropic.claude-v2" # or "amazon.titan-text-express-v1"
        #     body = json.dumps({
        #         "prompt": f"\n\nHuman: Given the average power usage is {avg_power} kW, suggest sustainability insights. \n\nAssistant:",
        #         "max_tokens_to_sample": 200
        #     })
        #     response = self.bedrock_client.invoke_model(
        #         body=body,
        #         modelId=model_id,
        #         accept="application/json",
        #         contentType="application/json"
        #     )
        #     response_body = json.loads(response.get("body").read())
        #     llm_insight = response_body.get("completion") # For Claude
        #     recommendations.append(f"AI Insight: {llm_insight}")
        # except Exception as e:
        #     print(f"Bedrock call failed: {e}")
        #     recommendations.append("Failed to get AI insights due to an error.")


        return {"recommendations": recommendations}


# === Lambda Handler Function ===
def lambda_handler(event, context):
    try:
        # Initialize Bedrock client (will be passed to SustainabilityInsightsAgent)
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.environ.get('AWS_REGION', 'us-east-1') # Use Lambda's region or default
        )

        # --- HARDCODED SAMPLE USAGE DATA ---
        # This replaces loading from a CSV file.
        usage_data = [
            {"timestamp": "2025-06-15T08:55:00.000Z", "household_id": "10", "power_kW": 2.5},
            {"timestamp": "2025-06-15T08:56:00.000Z", "household_id": "4", "power_kW": 2.8},
            {"timestamp": "2025-06-15T08:57:00.000Z", "household_id": "7", "power_kW": 3.1},
            {"timestamp": "2025-06-15T08:58:00.000Z", "household_id": "12", "power_kW": 2.9},
            {"timestamp": "2025-06-15T08:59:00.000Z", "household_id": "5", "power_kW": 3.5},
            {"timestamp": "2025-06-15T09:00:00.000Z", "household_id": "9", "power_kW": 4.0},
            {"timestamp": "2025-06-15T09:01:00.000Z", "household_id": "1", "power_kW": 2.7},
            {"timestamp": "2025-06-15T09:02:00.000Z", "household_id": "3", "power_kW": 3.2},
        ]

        # === 1️⃣ Forecast ===
        forecast_agent = EnergyForecastingAgent(sagemaker_client=None)
        forecasted_data = []
        for item in usage_data:
            forecast = forecast_agent.forecast_power(item)
            forecasted_data.append({
                "timestamp": item["timestamp"],
                "household_id": item["household_id"],
                "power_kW": forecast # This is the forecasted value
            })

        # === 2️⃣ Optimize ===
        optimization_agent = ResourceOptimizationAgent(config={"max_power_kW": 5.0})
        optimized_data = optimization_agent.optimize(forecasted_data, constraints={"max_power_kW": 5.0})

        # === 3️⃣ Generate Insights ===
        insights_agent = SustainabilityInsightsAgent(
            bedrock_client=bedrock_client, # Pass the initialized bedrock client
            config={"threshold": 3.0}
        )
        insights = insights_agent.generate_insights(optimized_data)

        # === Return results in API Gateway format ===
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # Essential for your frontend to call this API
            },
            'body': json.dumps({
                "message": "Energy data processed successfully!",
                "forecastedData": forecasted_data,
                "optimizedData": optimized_data,
                "insights": insights
            }, indent=2, ensure_ascii=False) # indent for readability, ensure_ascii for non-English chars
        }

    except Exception as e:
        print(f"Error in Lambda function: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "error": str(e),
                "message": "Failed to process energy data. Check Lambda logs for details."
            })
        }