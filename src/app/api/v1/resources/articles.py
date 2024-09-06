from flask import Blueprint, request, Response
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

bp = Blueprint('articles', __name__)

@bp.route('/content', methods=['POST'])
def content():
    if request.is_json:
        try:
            prompt = get_prompt(request)
            file_type = get_type(request).lower()  # Get the file type and make it lowercase for consistency

            client = create_client()

            # Auto-GPT iterative refinement
            refined_content = auto_gpt_refine_content(client, prompt, file_type)
            print("Refined content:", refined_content)

            # Set the mimetype based on the file type
            mimetype = 'text/markdown' if file_type == 'markdown' else 'text/html' if file_type == 'html' else 'application/json'

            return Response(refined_content, status=200, mimetype=mimetype)
        except Exception as e:
            print(f"Error processing request: {e}")
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')
    else:
        return Response(json.dumps({"error": "Invalid JSON input"}), status=400, mimetype='application/json')


def get_prompt(request):
    data = request.get_json()
    return data.get('message', 'No prompt provided')


def get_type(request):
    data = request.get_json()
    return data.get('type', 'Markdown')  # Default to Markdown if type is not provided


def create_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


def create_completion(client, prompt, temperature=0.7):
    try:
        return client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o",
            temperature=temperature,
        )
    except Exception as e:
        print(f"Error creating completion: {e}")
        raise


def auto_gpt_refine_content(client, prompt, file_type):
    # Step 1: Generate initial content
    initial_content = generate_content(client, prompt)

    # Step 2: Iteratively refine content using AI feedback
    refined_content = initial_content
    for _ in range(3):  # Set the number of iterations based on quality needs
        # Ask GPT to review and improve its own output
        review_prompt = (
            f"Review the following article for clarity, coherence, and content quality. "
            f"Suggest improvements and rewrite sections as necessary: {refined_content}"
        )
        review_response = create_completion(client, review_prompt, temperature=0.5)
        refined_content = review_response.choices[0].message.content

        # Check if the refined content meets quality standards
        validation_prompt = (
            f"Evaluate the quality of the following content. Does it meet the standards of a professional blog post? "
            f"Is it informative, well-structured, and engaging? Provide a rating from 1 to 5 and suggest further improvements if necessary: {refined_content}"
        )
        validation_response = create_completion(client, validation_prompt, temperature=0.3)
        validation_feedback = validation_response.choices[0].message.content
        print(f"Validation feedback: {validation_feedback}")

        # Optional: Stop refinement early based on feedback quality
        if "5" in validation_feedback:
            break

    # Step 3: Final format conversion
    final_content = format_content(client, refined_content, file_type)
    return clean_format(final_content)


def generate_content(client, prompt):
    response = create_completion(
        client,
        f"Write a detailed blog post on the topic: {prompt}. The article should be informative, provide clear insights, and be suitable for publication on a blog, without sounding promotional.",
    )
    return response.choices[0].message.content


def format_content(client, content, file_type):
    response = create_completion(
        client,
        f"Act as a {file_type} formatting expert. Format the following text into {file_type}, including titles, subtitles, bullet points, and ensuring it is properly formatted without special characters or escape sequences: {content}",
        temperature=0.5,
    )
    return response.choices[0].message.content


def clean_format(text):
    # Basic cleanup to remove unwanted special characters and escape sequences
    return text.replace("\\n", "\n").replace("\\", "")
