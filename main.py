# importing built-in library
import os
import json
# importing installed library
import requests
from dotenv import load_dotenv
from jinja2 import Template


load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_content(response):
    return response.json().get("choices", {})[0].get("message", {}).get("content")

def get_response(prompt):
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
                "content": prompt
            }
        ],
    })
)

if __name__ == '__main__':
    use_emoji = True
    emoji_text = "use emoji" if use_emoji else "don't use emoji"
    template = Template("Write a {{ tone }} post to {{ audience }} target audience, {{ emoji }} ,with the next campaign message: '{{ message }}', and the response should be in json like this: {'facebook': '<text + recomended hashtags>', 'instagram': '<tags + hashtags + 2 recomended picture ideas>','linkedin': '<text>', 'x': '<text + hashtags>'}")
    prompt = template.render(tone="friendly", audience="20-30 age gamer", emoji=emoji_text, message="Find out our new chair!")
    response = get_response(prompt)
    print(get_content(response))
