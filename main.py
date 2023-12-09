import streamlit as st
from sentence_transformers import SentenceTransformer


class PineconeInterface:
    def __init__(self, api_key, index_name):
        pass
    def search_vectors(self, query_vector, top_k):
        # return the name of books
        return [
            'a',
            'b',
            'c',
            'd',
            'e',
        ]

    


class UI_search:
    def __init__(self):
        self.result = []
        self.pinecone_interface = PineconeInterface('api_key', 'index_name')
        self.story2vector = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    def UI(self):
        st.title("Book Search")

        # Input keyword and select the number of books to display
        keyword = st.text_input("Enter your keyword:")
        #num_books = st.slider("Select number of books to display", 1, 5, 5)
        num_books = st.selectbox("Select number of books to display:", [1,2,3,4,5])
        
        # Search button
        if st.button("Search"):
            if keyword == "":
                return st.write("Enter a Keyword to Begin")
            # Call the search function with the keyword and get results
            self.result = self.search(keyword, num_books)
            
            if num_books==1:
                st.write(f"This story are likely to be of interest to you.")
            else:
                st.write(f"These {num_books} stories are likely to be of interest to you.")
                
            st.write("Click on any book to read more!")      

            # Display search results as buttons
            for i, name in enumerate(self.result):
                if st.button(f":notebook: Story {i + 1}: {name}"):
                    # next UI do
                    pass
                
                



    def search(self, keyword, num_books):
        # Call Pinecone's search_vectors function with the keyword
        query_vector = self.story2vector.encode(keyword)
        search_results = self.pinecone_interface.search_vectors(query_vector, top_k=num_books)
        return search_results
 

    
if __name__ == '__main__':
    ui = UI_search()
    ui.UI()