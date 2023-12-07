import streamlit as st

class TextToSpeech:
    def __init__(self, language: str):
        self.language = language

    def convert_to_audio(self, text, file_id:int):
        pass

class UI_read:
    def __init__(self, stories):
        self.stories = stories
        if 'page' not in st.session_state:
            st.session_state.page = 0

    def UI(self):

        '''
        st.sidebar.content("Select Story")
        selected_story = st.sidebar.selectbox("", [story["content"][:20] + "..." for story in self.stories])

        for idx, story in enumerate(self.stories):
            if selected_story.startswith(story["content"][:20] + "..."):
                st.session_state.page = idx
        '''

        st.title("Story Reader")
        current_story = self.stories[st.session_state.page]

        # Selectbox to jump to a specific page
        page_selector = st.selectbox("Select Page", list(range(1, len(self.stories) + 1)))
        #if st.button("Go to Page") and page_selector:
        st.session_state.page = page_selector - 1


        col1, col2 = st.columns(2)
        # Navigation buttons
        with col1:
            if st.button("Previous Page"):
                if st.session_state.page > 0:
                    st.session_state.page -= 1

        with col2:
            if st.button("Next Page"):
                if st.session_state.page + 1 < len(self.stories):
                    st.session_state.page += 1

        # Button to play audio
        if st.button("Play Audio"):
            self.read(current_story['content'])

        # Display text and image for the current page
        current_story = self.stories[st.session_state.page]
        st.markdown(f"### Page {st.session_state.page + 1}")
        st.write(current_story['content'])
        st.image('images/image' + str(current_story['pic_id']) + '.jpg', caption="Image for the page")


    def read(self, text: str):
        tts = TextToSpeech(language="English")
        # Assume convert_to_audio returns the audio file path
        audio_file_path = tts.convert_to_audio(text, file_id=1)

        # Play audio
        st.audio(audio_file_path, format='audio/wav')


# Example usage
if __name__ == "__main__":
    page1 = 'Snow White and the Seven Dwarfs is a 1937 American animated musical fantasy film produced by Walt Disney Productions and released by RKO Radio Pictures. Based on the 1812 German fairy tale by the Brothers Grimm, it is the first full-length cel animated feature film and the first Disney feature film. The production was supervised by David Hand, and the film\'s sequences were directed by Perce Pearce, William Cottrell, Larry Morey, Wilfred Jackson, and Ben Sharpsteen.'

    page2 = 'Shrek is a 2001 American animated fantasy comedy film loosely based on the 1990 children\'s picture book of the same name by William Steig. Directed by Andrew Adamson and Vicky Jenson (in their feature directorial debuts) and written by Ted Elliott, Terry Rossio, Joe Stillman, and Roger S. H. Schulman, it is the first installment in the Shrek film series. The film stars Mike Myers, Eddie Murphy, Cameron Diaz, and John Lithgow. In the film, an embittered ogre named Shrek (Myers) finds his home in the swamp overrun by fairy tale creatures banished by the obsessive ruler Lord Farquaad (Lithgow). With the help of Donkey (Murphy), Shrek makes a pact with Farquaad to rescue Princess Fiona (Diaz) in exchange for regaining control of his swamp.'

    stories = [
        {'content': page1, 'pic_id': 1},
        {'content': page2, 'pic_id': 2},
        # Add more pages as needed
    ]

    # Create an instance of UI_read
    ui_reader = UI_read(stories)

    # Run the Streamlit app
    ui_reader.UI()

