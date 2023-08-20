import openai
import keyring

openai.api_key = keyring.get_password('openai', 'secret-key')

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'system', 'content': 'You are a smart and helpful assistant.'},
        {'role': 'user', 'content': 'Generate documented Python code for setting up a minimal Flask server.'},
    ]
)

print(response['choices'][0]['message']['content'])