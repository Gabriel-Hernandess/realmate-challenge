import requests
import os
from groq import Groq

def generate_summary(messages_text):
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY não definido no ambiente")
    
    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Resuma de forma clara e concisa as conversas abaixo:\n\n{messages_text}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content