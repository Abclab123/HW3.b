## Usage 
In this module, I have created a abstract class for you to build the UI for AI story telling.

##### You have to inherit the class `StorytellingAppBase` and fill in 2 extra method.
1. `create_text_to_display` and 
2. `create_image_to_display`
---
### Notice 
1. In the abstract class, user input history has already been handle,
You can use `self.user_history` in your own class directly 

2. The stremlit module have specify the what format of image can be display, you might have to look into that. Function `create_image_to_display` have comment on that.

### Here is a simple example of how to use the class

#### 1. Inherit the class and import other module, overwrite the 2 method mention before
```python
# my UI module
from UI_module import StorytellingAppBase
# the 2 module of other team 
from ai import OpenAIGenerator, ImageGenerator

# *********************************************
# please inherit the class StorytellingAppBase*
# *********************************************
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
```

#### 2. Run this command in terminal
`streamlit run [your_file_name].py `
