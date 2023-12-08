from UI_module import StorytellingAppBase
from ai import OpenAIGenerator, ImageGenerator

class StorytellingApp(StorytellingAppBase):
    # Implement the methods to create text and image to display
    # You can also add any other methods that you may need
    def __init__(self, _text_generator=None, _image_generator=None):
        # Call the base class constructor
        super().__init__(_text_generator, _image_generator)

    def create_image_to_display( self, image):
        # Implement the logic to process and return text for display
        
        # image = self.image_generator.generate_image(prompt, output_file_id)
        # return image

        return "https://via.placeholder.com/300"
    
    def create_text_to_display(self, text ):
        # Implement the logic to create and return an image for display

        # text = self.text_generator.generate(user_input, self.user_history)
        # return text
        return "Open ai genetrated text "

def main():
    # Create an instance of the StorytellingApp class and run it
    app = StorytellingApp(_text_generator = OpenAIGenerator("OpenAI API Key"), 
                          _image_generator = ImageGenerator("Image Generator Model Name", True)
                        )
    app.run()

if __name__ == "__main__":
    main()