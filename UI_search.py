import random
import streamlit as st

# the UI for searching the vector store
class UI_search:
    def __init__(self):
        self.result = []

    def UI(self):
        st.write('What kind of story would you like to read? Please tell me in the below text input.')

        cols = st.columns([9, 1])
        query = cols[0].text_input(
            '',
            placeholder=f'    {self.random_placeholder()}',
            label_visibility='collapsed',
        )
        cols[1].button(
            ':mag:',
            on_click=self.search(query),
        )

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

# the followings won't be executed if this file is imported as a module
if __name__ == '__main__':
    ui = UI_search()
    ui.UI()
