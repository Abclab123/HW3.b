import openai
import os
from dotenv import load_dotenv

load_dotenv()


class OpenAIGenerator:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate(self, user_input: str, history: list = []) -> str:
        messages = [{"role": "system", "content": "This is a story solitaire game. Your goal is to collaboratively continue the story, taking turns with the user, until reaches a fantastic ending."}]
        for i, message in enumerate(history):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": message})
        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
        )
        generated_text = response['choices'][0]["message"]["content"]
        return generated_text


# Usage Example:

# Set up API_KEY="" in .env file
api_key = os.getenv('API_KEY')
generator = OpenAIGenerator(api_key)

# Input
user_input = "Once upon a time in a magical land, a brave knight set out on a quest."

# History
history = [
    "The brave knight named Sir Gallant was given a quest to retrieve a precious gem from a tricky goblin.",
    "The journey was long and arduous, leading him through dense forests and treacherous mountains."]

# Generate Story
generated_story = generator.generate(user_input, history)
print(generated_story)
