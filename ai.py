from openai import OpenAI
from torch import autocast
from diffusers import StableDiffusionPipeline
import torch


class OpenAIGenerator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = (
            "We are going to play a game called Story Chain. "
            "The user starts by telling the beginning of a story, and then you "
            "and the user take turns continuing the story until it reaches a "
            "suitable conclusion."
        )

    def generate(self, user_input: str, history: list = []) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        for i, message in enumerate(history):
            if i % 2 == 0:
                messages.append({"role": "user", "content": message})
            else:
                messages.append({"role": "assistant", "content": message})
        messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106", messages=messages
        )
        return response.choices[0].message.content


class ImageGenerator:
    def __init__(self, model_name: str, online: bool):
        if online:
            # Load model from Hugging Face Hub.
            self.pipeline = StableDiffusionPipeline.from_pretrained(model_name)
        else:
            # Load model from local path.
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_name, local_files_only=True
            )

        # Move the model to the GPU if available.
        self.pipeline = self.pipeline.to("cuda" if torch.cuda.is_available() else "cpu")

    def generate_image(self, prompt, output_file_id: int):
        with autocast("cuda" if torch.cuda.is_available() else "cpu"):
            # Generate an image from the prompt.
            image = self.pipeline(prompt).images[0]

        # Save the image to a file.
        image.save(f"{output_file_id}.png")
