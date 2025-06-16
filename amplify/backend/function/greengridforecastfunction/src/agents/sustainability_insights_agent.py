import json

class SustainabilityInsightsAgent:
    def __init__(self, bedrock_client=None, config=None):
        self.bedrock_client = bedrock_client
        self.config = config or {}
        self.threshold = self.config.get("threshold", 5.0)
        self.target_languages = self.config.get("target_languages", ["English"])

    def generate_insights(self, optimized_data):
        """
        Generates sustainability insights based on optimized data.
        Uses Bedrock LLM if available, else returns dummy recommendations.
        """
        try:
            if self.bedrock_client:
                # Build prompt with optimized data (summarized)
                prompt = self._build_prompt(optimized_data)
                response = self._call_bedrock_model(prompt)
                insights = json.loads(response)
            else:
                insights = self._dummy_insights()
        except Exception as e:
            print(f"Error generating insights: {e}")
            insights = self._dummy_insights()
        return insights

    def _build_prompt(self, optimized_data):
        # Simplified prompt; you can make this richer
        avg_power = sum(d["power_kW"] for d in optimized_data) / max(len(optimized_data), 1)
        return f"Generate sustainability advice for average power usage: {avg_power} kW."

    def _call_bedrock_model(self, prompt):
        # Placeholder: your Bedrock client call to the model goes here
        # For now, return dummy JSON string
        return '{"recommendations": {"English": "Reduce energy consumption during peak hours."}}'

    def _dummy_insights(self):
        return {
            "recommendations": {
                "English": "Consider reducing your energy consumption during peak hours to improve sustainability.",
                "Spanish": "Considere reducir su consumo de energía durante las horas pico para mejorar la sostenibilidad.",
                "Bosnian": "Razmislite o smanjenju potrošnje energije tijekom vršnih sati za poboljšanje održivosti."
            }
        }
