# importing built-in library
import os
import json
# importing installed library
from dotenv import load_dotenv
from jinja2 import Template
# importing other packages
from modules import get_content, get_response, data_clean
from exceptions import RateLimitExceededError, NoModelProvidedError

load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
FILENAME = 'output.json'

if __name__ == '__main__':
    use_emoji = True
    emoji_text = "use emoji" if use_emoji else "don't use emoji"
    template = Template('Write a {{ tone }} post to {{ audience }} target audience, {{ emoji }} ,with the next campaign message: "{{ message }}", and the response should be only a format like this: {"facebook": "<text + recomended hashtags>", "instagram": "<tags + hashtags + 2 recomended picture ideas>","linkedin": "<text>", "x": "<text + hashtags>"}. Please only and only write that nothing else only the json and the syntax needs to be perfect.')
    prompt = template.render(tone="friendly", audience="20-30 age gamer", emoji=emoji_text, message="Find out our new chair!")

    try:
        response = get_response(prompt, API_KEY, MODEL)
        raw_content_data = get_content(response)
        print(data_clean(raw_content_data))
        cleaned_data = json.loads(data_clean(raw_content_data))
        with open(FILENAME, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False)
        print("Data has been written to " + FILENAME)
    except NoModelProvidedError as e:
        print(e)
    except RateLimitExceededError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")
    