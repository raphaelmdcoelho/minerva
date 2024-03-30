from flask import Blueprint, request, Response
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('articles', __name__)

@bp.route('/content', methods=['POST'])
def content():
    if request.is_json:

        data = request.get_json()
        prompt = data.get('message')

        print(os.getenv("OPENAI_API_KEY"))
    
        client = OpenAI(
            api_key=os.environ.get(os.getenv("OPENAI_API_KEY")),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        return Response(chat_completion.choices[0].message.content, status=200, mimetype='application/json')