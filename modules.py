# importing built-in library
import json
# importing installed library
import requests
# importing other packages
from exceptions import RateLimitExceededError, NoModelProvidedError

def get_content(response):
    if response.status_code == 200:
        return response.json().get("choices", {})[0].get("message", {}).get("content")
    elif response.status_code == 400:
        raise NoModelProvidedError("No model provided, please provide one in .env file.")
    elif response.status_code == 429:
        raise RateLimitExceededError("Daily rate limit exceeded, limit is 50, you have 0 remaining. Try again tomorrow.")
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")

def get_response(prompt, api_key, model):
    return requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
    })
)

def data_clean(raw):
    if isinstance(raw, str):
        cleared_string = raw.replace("json\n", "")
        cleared_string = cleared_string.replace("`","")
        cleared_string = cleared_string.replace("\\n", "")
        cleared_string = cleared_string.replace("\n", "").strip()
    return cleared_string