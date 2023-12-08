import random
import streamlit as st
from time import sleep
# TODO: remember to import the real PineconeInterface
# from somewhere import PineconeInterface

# NOTE: this is just a dummy; should be removed latter
class PineconeInterface:
    def __init__(self, api_key, index_name):
        pass
    def search_vectors(self, query_vector, top_k=5):
        return ['Dummy Bookname'] * top_k

# the UI for searching the vector store
class UI_search:
    def __init__(self):
        self.query = None
        self.result = []

        # TODO: should fill in pinecone api key and index name here
        self.pinecone = PineconeInterface('dummy api key', 'dummy index name')

    def UI(self):
        placeholder = f'  {self.random_placeholder()}'
        with st.chat_message('ai'):
            st.write('Please tell me what kind of story would you like to read?')
            st.write(f'For example: "{placeholder}"')

        if query := st.chat_input():
            st.chat_message('user').write(query)

            with st.chat_message('ai'):
                with st.spinner('Finding...'):
                    self.search(query)

                st.write('These stories are probably what you want.')
                sleep(1)
                for i, book in enumerate(self.result):
                    # TODO: the following button should take the user to the story content
                    st.button(f'Story {i+1}: {book}')

    def random_placeholder(self) -> str:
        placeholders = [
            'A story long after the heros defeated the evil villain...',
            'A story if Snow White never wakes up after eating the poisoned apple...',
            'A story of a brave guy who save the world from World War III with his trumpet...',
        ]
        return random.choice(placeholders)

    def search(self, keyword: str):
        if keyword == '':
            return
        self.result = self.pinecone.search_vectors(keyword)

# the followings won't be executed if this file is imported as a module
if __name__ == '__main__':
    ui = UI_search()
    ui.UI()
