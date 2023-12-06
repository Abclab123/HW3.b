#https://colab.research.google.com/drive/1Q7Tlsw5DDeuG50A9veu89Yl4pZgMgxeK

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from PIL import Image
import requests

class ImageGenerator:
    def __init__(self, model_name: str, online: bool):
        self.pipeline = None
        if online:
            self.pipeline = StableDiffusionPipeline.from_pretrained(model_name)
        else:
            # If the model is not online, you might want to load it from a local path.
            # Replace 'local_model_path' with the actual path to your model.
            local_model_path = '/path/to/your/local/model'
            self.pipeline = StableDiffusionPipeline.from_pretrained(local_model_path)

        # Move the model to the GPU if available
        if torch.cuda.is_available():
            self.pipeline.to('cuda')

    def generate_image(self, prompt: str, output_file_id: int):
        # Use autocast from the torch library for faster inference
        with autocast("cuda"):
            # Generate an image from the prompt
            generated_image = self.pipeline(prompt).images[0]

        # Save the generated image
        output_file_path = f"{output_file_id}.png"
        generated_image.save(output_file_path)

        return output_file_path

def main():
    model_name = "CompVis/stable-diffusion-v1-4"  # Replace with your model's name
    online_model = True  # Set to False if you want to use a local model

    # Create an instance of the ImageGenerator
    image_generator = ImageGenerator(model_name, online_model)

    # Define a prompt for image generation
    prompt = "A landscape of mountains under a starry sky"  # Replace with your desired prompt

    # Generate an image
    output_file = image_generator.generate_image(prompt, 1)

    print(f"Generated image saved as: {output_file}")

if __name__ == "__main__":
    main()