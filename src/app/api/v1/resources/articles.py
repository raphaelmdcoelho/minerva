# from flask import Blueprint, request, Response
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# import json
# import time

# load_dotenv()

# bp = Blueprint('articles', __name__)

# @bp.route('/content', methods=['POST'])
# def content():
#     if request.is_json:

#         prompt = get_prompt(request)         
    
#         client = create_client()   

#         chat_completion = create_completition(client, prompt)
#         initial_content = chat_completion.choices[0].message.content

#         print("Initial Content:", initial_content)

#         grammar_check_assistant = create_assistant(
#             client,
#             "Grammar Assistant",
#             "Grammar and spelling check assistant",
#             "You are a specialized AI trained to check grammar and spelling errors.",
#             "gpt-3.5-turbo"
#         )

#         check_grammar_assistant_thread = create_thread(client) 
#         message1 = create_message(client, check_grammar_assistant_thread, initial_content)
#         grammar_checked_response = run_message(client, check_grammar_assistant_thread, grammar_check_assistant, "Please check text for grammar and spelling errors and apply the corrections to the text as a result.")
#         time.sleep(10)

#         # Get the updated message from the grammar check assistant
#         while grammar_checked_response.status == "queued":
#             print(grammar_checked_response.status)
#             print("Waiting for answer...")
#             print(check_grammar_assistant_thread.id)
#             print(grammar_checked_response.id)
#             run = client.beta.threads.runs.retrieve(
#                 thread_id=check_grammar_assistant_thread.id,
#                 run_id=grammar_checked_response.id
#             )
#             time.sleep(20)

#         grammar_messages = client.beta.threads.messages.list(
#             thread_id=check_grammar_assistant_thread.id
#         )

#         grammar_checked_content = extract_text_content(grammar_messages)
#         print("Grammar Checked Response Messages:", grammar_messages)
#         print("Grammar Checked Content:", grammar_checked_content)

#         md_assistant = create_assistant(
#             client,
#             "MD Extension Format Assistant",
#             "Specialized AI trained to convert text to .md format",
#             "You are a specialized AI trained to convert text to .md format.",
#             "gpt-3.5-turbo"
#         )
        
#         md_assistant_thread = create_thread(client) 
#         create_message(client, md_assistant_thread, grammar_checked_content)
#         md_response = run_message(client, md_assistant_thread, md_assistant, "Make this text as a markdown file with title and subtitles and add a word end at the end of the text. I want a header level 1 being added as a result")
#         time.sleep(10)

#         # Get the updated message from the markdown assistant
#         md_messages = client.beta.threads.messages.list(
#             thread_id=md_assistant_thread.id
#         )

#         md_content = extract_text_content(md_messages)
#         print("Markdown Response Messages:", md_messages)
#         print("Markdown Content:", md_content)

#         return Response(md_content, status=200, mimetype='application/json')

# def get_prompt(request):
#     data = request.get_json()
#     return data.get('message')

# def create_client():
#     return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def create_completition(client, prompt):
#     return client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt,
#             }
#         ],
#         model="gpt-3.5-turbo",
#         temperature=0.7,
#     )

# def create_assistant(client, name, description, instructions, model):
#     return client.beta.assistants.create(
#         name=name,
#         #description=description,
#         instructions=instructions,
#         model=model,
#     )

# def create_thread(client):
#     return client.beta.threads.create()

# def create_message(client, thread, content):
#     return client.beta.threads.messages.create(
#         thread_id=thread.id, 
#         role="user", 
#         content=content
#     )

# def run_message(client, thread, assistant, action):
#     return client.beta.threads.runs.create(
#         thread_id=thread.id, 
#         assistant_id=assistant.id, 
#         instructions=action
#     )

# def extract_text_content(messages):
#     try:
#         text_blocks = messages.data[0].content
#         # text_content = " ".join([block.text.value for block in text_blocks if block.type == 'text'])
#         # return text_content
#         return text_blocks[0].text.value
#     except (KeyError, IndexError, TypeError) as e:
#         print(f"Error extracting text content from messages: {e}")
#         return None



from flask import Blueprint, request, Response
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

bp = Blueprint('articles', __name__)

@bp.route('/content', methods=['POST'])
def content():
    if request.is_json:

        prompt = get_prompt(request)         
    
        client = create_client()   

        # ask chat gpt to write the prompt for the steps:
        chat_completion = create_completition(client, 
            f"Write a post about {prompt} with up to 1000 words at maximum with. The post should be informative and engaging and not sound like a sales pitch.")
        initial_content = chat_completion.choices[0].message.content

        print(chat_completion)

        chat_completion_grammar_check = create_completition(client, 
            f"Act as a grammar english expert and check the following text for grammar and spelling errors and apply the corrections to the text as a result: {initial_content}")
        grammar_check_content = chat_completion_grammar_check.choices[0].message.content

        print(chat_completion_grammar_check)

        md_transformation_completion = create_completition(client, 
            f"Act as a markdown file format expert and make this text as a markdown format. If necessary add title, subtitles and enumerations for the text: {grammar_check_content}")
        result_content = md_transformation_completion.choices[0].message.content     

        return Response(result_content, status=200, mimetype='application/json')

def get_prompt(request):
    data = request.get_json()
    return data.get('message')

def create_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_completition(client, prompt):
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
        temperature=0.7,
    )

def create_assistant(client, name, description, instructions, model):
    return client.beta.assistants.create(
        name=name,
        #description=description,
        instructions=instructions,
        model=model,
    )

def create_thread(client):
    return client.beta.threads.create()

def create_message(client, thread, content):
    return client.beta.threads.messages.create(
        thread_id=thread.id, 
        role="user", 
        content=content
    )

def run_message(client, thread, assistant, action):
    return client.beta.threads.runs.create(
        thread_id=thread.id, 
        assistant_id=assistant.id, 
        instructions=action
    )

def extract_text_content(messages):
    try:
        text_blocks = messages.data[0].content
        # text_content = " ".join([block.text.value for block in text_blocks if block.type == 'text'])
        # return text_content
        return text_blocks[0].text.value
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error extracting text content from messages: {e}")
        return None
