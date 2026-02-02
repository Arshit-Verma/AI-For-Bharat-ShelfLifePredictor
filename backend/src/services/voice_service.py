import requests
import os
from dotenv import load_dotenv

load_dotenv()


class ElevenLabsVoiceService:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.base_url = 'https://api.elevenlabs.io/v1'
        self.voice_id = '21m00Tcm4TlvDq8ikWAM'

    def text_to_speech(self, text, voice_id=None):
        if not self.api_key:
            return {'error': 'ElevenLabs API key not configured'}

        try:
            url = f'{self.base_url}/text-to-speech/{voice_id or self.voice_id}'
            headers = {
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json',
                'xi-api-key': self.api_key
            }
            data = {
                'text': text,
                'model_id': 'eleven_monolingual_v1',
                'voice_settings': {
                    'stability': 0.5,
                    'similarity_boost': 0.75
                }
            }

            response = requests.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                return {
                    'success': True,
                    'audio_data': response.content
                }
            else:
                return {
                    'error': f'API request failed with status {response.status_code}',
                    'message': response.text
                }

        except Exception as e:
            return {'error': str(e)}

    def generate_explanation_audio(self, prediction_result):
        explanation_text = self._format_explanation(prediction_result)
        return self.text_to_speech(explanation_text)

    def _format_explanation(self, result):
        text = f"For your {result['food_type']} stored in the {result['storage_type']}, "
        text += f"at {result['temperature']} degrees Celsius and {result['humidity']} percent humidity, "
        text += f"after {result['days_stored']} days, "
        text += f"the predicted remaining shelf life is {result['predicted_remaining_days']} days. "

        if result['safety_classification'] == 'Safe':
            text += "The food is safe to consume. "
        elif result['safety_classification'] == 'Consume Soon':
            text += "You should consume this food soon. "
        else:
            text += "This food has likely expired and should be discarded. "

        if result['issues']:
            text += f"I've detected {len(result['issues'])} issues: "
            for issue in result['issues'][:2]:
                text += f"{issue}. "

        if result['recommendations']:
            text += "My recommendations are: "
            for rec in result['recommendations'][:2]:
                text += f"{rec}. "

        return text

    def get_available_voices(self):
        if not self.api_key:
            return {'error': 'ElevenLabs API key not configured'}

        try:
            url = f'{self.base_url}/voices'
            headers = {
                'xi-api-key': self.api_key
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return {'voices': response.json().get('voices', [])}
            else:
                return {'error': f'Failed to fetch voices: {response.text}'}

        except Exception as e:
            return {'error': str(e)}
