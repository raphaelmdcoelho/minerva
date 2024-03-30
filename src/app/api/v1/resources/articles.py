from flask import Blueprint, jsonify, request
import requests

OPENAI_API_KEY = 'your_api_key_here'

bp = Blueprint('articles', __name__)

@bp.route('/content', methods=['POST'])
def content():
    if request.is_json:

        data = request.get_json()
        prompt = data.get('message')

        if prompt:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}'
            }

            payload = {
                'model': 'text-davinci-003',
                'prompt': prompt,
                'temperature': 0.5,
                'max_tokens': 100
            }

            response = requests.post('https://api.openai.com/v1/completions', json=payload, headers=headers)

            if response.status_code == 200:
                return jsonify(response.json()), 200
            else:
                return jsonify({"error": "Failed to get response from OpenAI API"}), response.status_code
        else:
            return jsonify({"error": "No message provided"}), 400
    else:
        return jsonify({"error": "Request must be in JSON format"}), 400
    
