import boto3
import json

class SustainabilityInsightsAgent:
    def __init__(self, bedrock_client, config): # Added bedrock_client to init
        self.bedrock_client = bedrock_client
        self.config = config
        self.target_languages = config.get("target_languages", ["English", "Spanish", "Bosnian"]) # Default languages

    def generate_insights(self, optimized_data, current_context=None):
        """
        Generates human-friendly, localized insights using Amazon Bedrock.
        Assumes optimized_data contains household-level adjusted power readings.
        current_context can provide additional info like neighborhood peak status.
        """
        if not optimized_data:
            return {"recommendations": {lang: "No usage data to analyze." for lang in self.target_languages}}

        # For a hackathon, let's focus on one example where optimization occurred
        # In a real system, you'd iterate or aggregate this more intelligently
        example_household_data = None
        for item in optimized_data:
            # Dummy logic: If adjusted power is notably less than a hypothetical 'original' high forecast
            # In a real scenario, you'd compare optimized_data with original forecasted_data for each household
            if item["adjusted_power_kW"] < self.config.get("threshold", 5.0): # Using threshold as a proxy for 'reduction'
                example_household_data = item
                break
        
        if example_household_data is None:
            # If no significant optimization was applied (e.g., all below threshold), give general advice
            prompt_text = "Generate a general, encouraging tip about saving energy at home. Keep it simple and actionable. Provide the tip in English, Spanish, and Bosnian."
        else:
            # Example where optimization was applied (household_id: 6 in your example output)
            household_id = example_household_data["household_id"]
            adjusted_power = example_household_data["adjusted_power_kW"]
            
            # This is where you'd ideally compare to the *original* forecasted_power_kW for that household
            # For this example, let's assume the context implies a reduction was needed.
            # You could pass the original forecasted value as part of current_context in main_pipeline
            
            # Crafting the prompt for Bedrock
            prompt_text = f"""
            You are an AI assistant providing helpful energy-saving advice to residents in St. Louis.
            A household (ID: {household_id}) has adjusted its power usage to {adjusted_power:.2f} kW during a recent peak demand period, helping the neighborhood grid.
            Please generate a concise, actionable, and encouraging energy-saving tip for this household.
            The tip should be easy to understand, avoid jargon, and be culturally sensitive for an urban/suburban St. Louis audience.
            Consider common household energy uses like lighting, appliances, or heating/cooling.
            
            Crucially, provide the same tip translated into the following languages:
            1. English
            2. Spanish
            3. Bosnian
            
            Format your response as a JSON object with a key for each language. For example:
            {{
              "English": "...",
              "Spanish": "...",
              "Bosnian": "..."
            }}
            """
            
        # Select the Bedrock model
        # You can choose other models like 'anthropic.claude-v2' or 'ai21.j2-mid'
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0" 
        
        # Prepare the request payload based on model requirements
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        }
                    ]
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7,
        })

        try:
            response = self.bedrock_client.invoke_model(
                body=body,
                modelId=model_id,
                accept="application/json",
                contentType="application/json"
            )
            
            response_body = json.loads(response.get('body').read())
            
            # Claude 3 response structure
            if 'content' in response_body and response_body['content']:
                generated_text = response_body['content'][0]['text']
                
                # Attempt to parse as JSON (as requested in prompt)
                try:
                    insights_json = json.loads(generated_text)
                    return {"recommendations": insights_json}
                except json.JSONDecodeError:
                    print(f"Warning: Bedrock did not return perfect JSON. Raw output: {generated_text}")
                    # Fallback if Bedrock doesn't strictly follow JSON format
                    return {"recommendations": {lang: generated_text for lang in self.target_languages}}
            else:
                return {"recommendations": {lang: "Could not generate insights." for lang in self.target_languages}}

        except Exception as e:
            print(f"Error invoking Bedrock: {e}")
            return {"recommendations": {lang: f"Error generating insights: {str(e)}" for lang in self.target_languages}}