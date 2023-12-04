import streamlit as st

# the UI for searching the vector store
class UI_search:
    def __init__(self):
        self.result = []

    def UI(self):
        prev_query = ''
        cols = st.columns([4, 1])
        query = cols[0].text_input(
            '',
            placeholder='',
            label_visibility='collapsed',
        )
        cols[1].button(
            ':mag:',
            on_click=self.search(query),
        )

    def search(self, keyword: str) -> list:
        pass

# the followings won't be executed if this file is imported as a module
if __name__ == '__main__':
    ui = UI_search()
    ui.UI()
