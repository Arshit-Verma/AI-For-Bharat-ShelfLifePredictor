from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
import traceback
import io

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

load_dotenv('../../config/.env')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.preprocessing.preprocessor import DataPreprocessor
from src.feature_engineering.engineer import FeatureEngineer
from src.models.predictor import ShelfLifePredictor
from src.inference.pipeline import InferencePipeline
from src.rules.interpreter import RuleBasedInterpreter
from src.services.voice_service import ElevenLabsVoiceService
from src.services.chat_service import OpenRouterChatService

app = Flask(__name__)
CORS(app)

pipeline = None
voice_service = None
chat_service = None


def load_pipeline():
    global pipeline, voice_service, chat_service
    try:
        preprocessor = DataPreprocessor().load('models/preprocessor.pkl')
        model = ShelfLifePredictor().load('models/shelf_life_predictor.pkl')
        feature_engineer = FeatureEngineer()
        rule_interpreter = RuleBasedInterpreter()

        pipeline = InferencePipeline(preprocessor, feature_engineer, model, rule_interpreter)
        print("Pipeline loaded successfully!")
    except Exception as e:
        print(f"Error loading pipeline: {e}")
        traceback.print_exc()

    try:
        voice_service = ElevenLabsVoiceService()
        chat_service = OpenRouterChatService()
        print("Services loaded successfully!")
    except Exception as e:
        print(f"Error loading services: {e}")
        traceback.print_exc()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'pipeline_loaded': pipeline is not None})


@app.route('/predict', methods=['POST'])
def predict():
    if pipeline is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()

        result = pipeline.predict_single(
            food_type=data['food_type'],
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            storage_type=data['storage_type'],
            days_stored=float(data['days_stored'])
        )

        return jsonify(result)
    except Exception as e:
        print(f"Prediction error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/explain', methods=['POST'])
def explain():
    if pipeline is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()

        result = pipeline.predict_single(
            food_type=data['food_type'],
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            storage_type=data['storage_type'],
            days_stored=float(data['days_stored'])
        )

        explanation = pipeline.explain_prediction(result)

        return jsonify({
            'explanation': explanation,
            'result': result
        })
    except Exception as e:
        print(f"Explanation error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    if pipeline is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        items = data.get('items', [])

        results = pipeline.predict(items)

        return jsonify({'results': results})
    except Exception as e:
        print(f"Batch prediction error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/voice/explain', methods=['POST'])
def voice_explain():
    if pipeline is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()

        result = pipeline.predict_single(
            food_type=data['food_type'],
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            storage_type=data['storage_type'],
            days_stored=float(data['days_stored'])
        )

        audio_result = voice_service.generate_explanation_audio(result)

        if 'error' in audio_result:
            return jsonify(audio_result), 500

        return send_file(
            io.BytesIO(audio_result['audio_data']),
            mimetype='audio/mpeg',
            as_attachment=False
        )

    except Exception as e:
        print(f"Voice explanation error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    if chat_service is None:
        return jsonify({'error': 'Chat service not loaded'}), 500

    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context')

        response = chat_service.chat(message, context)

        if 'error' in response:
            return jsonify(response), 500

        return jsonify(response)

    except Exception as e:
        print(f"Chat error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/chat/prediction_explanation', methods=['POST'])
def prediction_explanation():
    if pipeline is None or chat_service is None:
        return jsonify({'error': 'Services not loaded'}), 500

    try:
        data = request.get_json()

        result = pipeline.predict_single(
            food_type=data['food_type'],
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            storage_type=data['storage_type'],
            days_stored=float(data['days_stored'])
        )

        explanation = chat_service.get_prediction_explanation(result)

        return jsonify({'explanation': explanation})

    except Exception as e:
        print(f"Prediction explanation error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/chat/storage_advice', methods=['POST'])
def storage_advice():
    if chat_service is None:
        return jsonify({'error': 'Chat service not loaded'}), 500

    try:
        data = request.get_json()
        food_type = data['food_type']
        storage_conditions = data.get('storage_conditions', {})

        response = chat_service.get_storage_advice(food_type, storage_conditions)

        if 'error' in response:
            return jsonify(response), 500

        return jsonify(response)

    except Exception as e:
        print(f"Storage advice error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    load_pipeline()
    app.run(host='0.0.0.0', port=5001, debug=True)
