# importing built-in library
import os
import json
import requests
# importing installed library
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_content(response):
    return response.json().get("choices", {})[0].get("message", {}).get("content")

def get_response():
    return requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "messages": [
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
        ],
    })
)

if __name__ == '__main__':
    response = get_response()
    print(get_content(response))