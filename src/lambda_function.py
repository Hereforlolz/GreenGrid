import json
import random
from datetime import datetime, timedelta

def simulate_forecast(num_days=3):
    forecast = []
    today = datetime.utcnow()
    for i in range(num_days):
        day = today + timedelta(days=i)
        # simulate hourly energy forecast in kWh for 24 hours
        hourly_forecast = [round(random.uniform(0.5, 3.0), 2) for _ in range(24)]
        forecast.append({
            "date": day.strftime("%Y-%m-%d"),
            "hourly_forecast_kWh": hourly_forecast
        })
    return forecast

def lambda_handler(event, context):
    # Log event for debugging
    print("Event:", json.dumps(event))
    
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    
    if method == "GET":
        # Return simulated forecast for next 3 days
        data = simulate_forecast()
        response = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"forecast": data})
        }
        return response
    
    elif method == "POST":
        # If POST, expect JSON payload to specify parameters (optional)
        try:
            body = json.loads(event.get("body") or "{}")
            days = int(body.get("days", 3))
        except Exception as e:
            days = 3
        
        data = simulate_forecast(num_days=days)
        response = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"forecast": data})
        }
        return response

    else:
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Method not allowed"})
        }
