# importing built-in library
import os
import json
# importing installed library
from dotenv import load_dotenv
from jinja2 import Template
# importing other packages
from modules import get_content, get_response, data_clean
from exceptions import RateLimitExceededError, NoModelProvidedError

# declaring every global variable
load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
FILENAME = 'output.json'

if __name__ == '__main__':
    # getting from input what should be the output
    tone_input = input("Please write in what tone should be the posts (friendly, encouraging, ...): ")
    audience_input = input("Who is the target audience of the posts (20-25 aged men, gamers, powerlifters)")
    message_input = input("Please write a campaign message: ")
    while True:
        emoji_input = input("Emojis should be used? (y/n)").lower()
        if emoji_input in ('y', 'n'):
            emoji_text = "use emoji" if emoji_input == 'y' else "don't use emoji"
            break
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    # Creating the prompt
    template = Template('Write a {{ tone }} post to {{ audience }} target audience, {{ emoji }} ,with the next campaign message: "{{ message }}", and the response should be only a format like this: {"facebook": "<text + recomended hashtags>", "instagram": "<tags + hashtags + 2 recomended picture ideas>","linkedin": "<text>", "x": "<text + hashtags>"}. Please only and only write that nothing else only the json and the syntax needs to be perfect.')
    prompt = template.render(tone=tone_input, audience=audience_input, emoji=emoji_text, message=message_input)

    # getting response
    try:
        # getting response through API call
        response = get_response(prompt, API_KEY, MODEL)
        raw_content_data = get_content(response)
        print(data_clean(raw_content_data))
        # refining the output, writing output to a json file
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
    