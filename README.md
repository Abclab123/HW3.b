# Pinecone Interface
## Getting started
Create a [Pinecone](https://www.pinecone.io/) account first. Get your API key and modify `API_KEY` variable in main.py.
```
# insert API key here 
API_KEY = ""
```

Create conda or venv, and install requirements.txt
```
conda create -n cone python=3.11
conda activate cone 
pip install -r requirements.txt
```

## Running the code 
```
python main.py
```

--- 

```
# Project Name: GenAI Toolbox

## 1: Generative AI, aka GenAI
Invoke #6 and #7 to generate texts and images respectively.

UI_gen

## 2: UI for reading aloud the generated text.

UI_read

## 3: Search the vector store

UI_search

## 4: UI for login.

UI login

## 5

class speech_to_text:
    def __init__(self, online: bool, language: str):
        self.online = online
        self.language = language

    def record(self, output_file_id: int) -> str:
        if self.online:
            pass
        else:
            pass

## 6
# In this module, your input arguments are user's prompt and the chat history, and the goal is to generate good stories by using openai api.
# Utilize the system prompt to ingeniously guide your GPT in crafting a creative narrative with a compelling plot twist.

class OpenAIGenerator:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate(self, user_input: str, history: list = []) -> str:
        pass

## 7

from torch import autocast
from diffusers import StableDiffusionPipeline

class ImageGenerator:
    def __init__(self, model_name: str, online: bool):
        pass

    def generate_image(self, prompt, output_file_id: int):
        pass

## 8

class TextToSpeech:
    def __init__(self, language: str):
        self.language = language

    def convert_to_audio(self, text, file_id: int):
        pass

## 9
# In this module, you need to use mongoDB to create a database for books.
# Each book has its corresponding table.
# The format of the elements of the collections are : {page : page_number, content : the text content of this page, picture_idx : the index of the picture corresponding to the story in this page.}
# MongoDB
import pymongo

class BooksDB:
    def __init__(self, myclient: str):
        self.myclient = myclient
        self.mydb = myclient["mydatabase"]

    def create_book(self, bookname: str):
        pass

    def append(bookname: str, picture_idx: int, content: str):
        pass

## 10

class PineconeInterface:
    def __init__(self, api_key, index_name):
        pinecone.init(api_key=api_key)
        self.index = pinecone.Index(index_name)

    def insert_vector(self, vector_id, vector_data):
        self.index.upsert(items=[(vector_id, vector_data)])

    def search_vectors(self, query_vector, top_k=5):
        pass

## 11: Putting it all together.

## 12: Fine-tune

## 13: Prepare data
```
