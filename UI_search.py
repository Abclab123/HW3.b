import random
from sentence_transformers import SentenceTransformer
import streamlit as st
from time import sleep
# from somewhere import PineconeInterface

# NOTE: dummy PineconeInterface
class PineconeInterface:
    def __init__(self, api_key, index_name):
        pass
    def search_vectors(self, query_vector, top_k=5):
        return [
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eros tellus, scelerisque eu rhoncus nec, mollis a mi. Sed sit amet aliquam diam, et semper augue. Ut vel feugiat ante. Nulla dictum nulla elementum, laoreet erat quis, vulputate elit. Phasellus in consectetur neque. Cras facilisis aliquet mauris sed hendrerit. Fusce erat neque, rhoncus ut consectetur ac, aliquam id urna.',
            'Etiam posuere purus et tortor luctus, vitae interdum metus pharetra. Sed quis ante non est placerat pharetra. Curabitur non hendrerit nisl. Praesent sit amet ipsum vitae urna suscipit varius sed ac sem. Suspendisse diam nunc, eleifend lobortis eleifend ut, pellentesque id justo.',
            'Aenean suscipit sed velit ac blandit. In nisl odio, aliquet vel velit id, tempus blandit tellus. Vestibulum scelerisque molestie lectus, ut laoreet erat maximus pharetra. In et augue orci. Aliquam bibendum quis ipsum ac dapibus. Vestibulum et elementum quam. Phasellus semper rutrum leo ac tincidunt. In lacus mauris, interdum iaculis mollis in, ultrices et diam.',
            'Cras elementum, mauris nec convallis aliquam, eros magna bibendum neque, a maximus elit purus eget justo. Phasellus viverra accumsan quam, a blandit sem blandit laoreet. Fusce tempor sollicitudin auctor. Nam vitae ex vehicula, euismod lorem et, mollis orci. Nunc gravida leo ut pulvinar accumsan. Pellentesque sollicitudin justo eget eros hendrerit, quis consectetur mi elementum.',
            'Nulla id mauris neque. Nam eleifend ullamcorper sagittis. Nullam ac lorem est. Suspendisse ornare aliquet mollis. Sed sollicitudin viverra quam, varius pulvinar libero viverra ut. In magna orci, vehicula non fermentum quis, consequat lacinia nibh. Maecenas ac iaculis turpis.',
        ]

# the UI for searching the vector store
class UI_search:
    def __init__(self):
        self.query = None
        self.result = []

        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
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
                for i, story in enumerate(self.result):
                    st.info(f'#### Story {i+1}\n{story}')

    def random_placeholder(self) -> str:
        placeholders = [
            'A story long after the heros defeated the evil villain...',
            'A story if Snow White never wakes up after eating the poisoned apple...',
            'A story of a brave guy who save the world from World War III with his trumpet...',
        ]
        return random.choice(placeholders)

    def search(self, keyword: str) -> list:
        if keyword == '':
            return
        embedding = self.model.encode(keyword)
        self.result = self.pinecone.search_vectors(embedding)

# the followings won't be executed if this file is imported as a module
if __name__ == '__main__':
    ui = UI_search()
    ui.UI()
