# importing built-in library
import json
from typing import Optional
# importing installed library
import requests
# importing other packages
from exceptions import RateLimitExceededError, NoModelProvidedError

# getting response with API call
def get_response(prompt: str, api_key: str, model: str) -> str:
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

# returning the output from the response
def get_content(response: str) -> Optional[str]:
    # in case of status OK the output string will be returned
    if response.status_code == 200:
        return response.json().get("choices", {})[0].get("message", {}).get("content")
    # model was no provided raising error
    elif response.status_code == 400:
        raise NoModelProvidedError("No model provided, please provide one in .env file.")
    # if the limit of the requests are out raising error
    elif response.status_code == 429:
        raise RateLimitExceededError("Daily rate limit exceeded.")
    # raising error on other status codes
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")

# cleaning output from unwanted characters, not always accruate, depends on the output format
def data_clean(raw: str) -> str:
    if isinstance(raw, str):
        cleared_string = raw.replace("json\n", "")
        cleared_string = cleared_string.replace("`","")
        cleared_string = cleared_string.replace("\\n", "")
        cleared_string = cleared_string.replace("\n", "").strip()
    return cleared_string