import requests
import os
from dotenv import load_dotenv

load_dotenv()


class OpenRouterChatService:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = 'https://openrouter.ai/api/v1'
        self.model = 'anthropic/claude-3-haiku'

    def chat(self, message, context=None):
        if not self.api_key:
            return {'error': 'OpenRouter API key not configured'}

        try:
            system_prompt = """You are a food safety and storage expert AI assistant. 
            Help users with questions about food storage, safety, and shelf life predictions.
            Provide clear, practical advice based on food safety guidelines.
            Always prioritize safety - when in doubt, recommend discarding food.
            Keep responses concise and actionable."""

            messages = [
                {'role': 'system', 'content': system_prompt}
            ]

            if context:
                messages.append({
                    'role': 'user',
                    'content': f"Context: {context}\n\nQuestion: {message}"
                })
            else:
                messages.append({
                    'role': 'user',
                    'content': message
                })

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:3000',
                'X-Title': 'Food Shelf Life Predictor'
            }

            data = {
                'model': self.model,
                'messages': messages,
                'max_tokens': 500,
                'temperature': 0.7
            }

            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'response': result['choices'][0]['message']['content']
                }
            else:
                return {
                    'error': f'API request failed with status {response.status_code}',
                    'message': response.text
                }

        except Exception as e:
            return {'error': str(e)}

    def get_prediction_explanation(self, prediction_result):
        context = f"""
        Food Type: {prediction_result['food_type']}
        Storage Type: {prediction_result['storage_type']}
        Temperature: {prediction_result['temperature']}°C
        Humidity: {prediction_result['humidity']}%
        Days Stored: {prediction_result['days_stored']}
        Predicted Remaining Days: {prediction_result['predicted_remaining_days']}
        Safety Classification: {prediction_result['safety_classification']}
        """

        questions = [
            "What are the main factors affecting this prediction?",
            "What should I do with this food item?",
            "How can I extend the shelf life of similar items?"
        ]

        explanation = []
        for question in questions:
            response = self.chat(question, context)
            if response.get('success'):
                explanation.append({
                    'question': question,
                    'answer': response['response']
                })

        return explanation

    def get_storage_advice(self, food_type, storage_conditions):
        message = f"What are the best storage practices for {food_type}?"

        context = f"""
        Current storage conditions:
        - Storage type: {storage_conditions.get('storage_type', 'unknown')}
        - Temperature: {storage_conditions.get('temperature', 'unknown')}°C
        - Humidity: {storage_conditions.get('humidity', 'unknown')}%
        """

        return self.chat(message, context)

    def get_safety_guidelines(self, food_type):
        message = f"What are the key safety guidelines for storing {food_type}? How can I tell if it has gone bad?"
        return self.chat(message)
