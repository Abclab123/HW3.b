from torch import autocast
from diffusers import StableDiffusionPipeline
import torch

class ImageGenerator:
    def __init__(self, model_name: str, online: bool):
    
        if online:
            # Load model from Hugging Face Hub.
            self.pipeline = StableDiffusionPipeline.from_pretrained(model_name)
        else:
            # Load model from local path.
            self.pipeline = StableDiffusionPipeline.from_pretrained(model_name, local_files_only=True)
        
        # Move the model to the GPU if available.
        self.pipeline = self.pipeline.to("cuda" if torch.cuda.is_available() else "cpu")

    def generate_image(self, prompt, output_file_id: int):
        
        with autocast("cuda" if torch.cuda.is_available() else "cpu"):
            # Generate an image from the prompt.
            image = self.pipeline(prompt).images[0]
        
        # Save the image to a file.
        image.save(f"{output_file_id}.png")

# Example usage
if __name__ == "__main__":
    model_name = "CompVis/stable-diffusion-v1-4"  # Example model name
    image_generator = ImageGenerator(model_name, online=True)
    image_generator.generate_image("A beautiful landscape", 1)
    image_generator.generate_image("a red ball on the beach", 2)
    image_generator.generate_image("A puffin on the rock", 3)
