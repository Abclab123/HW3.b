import streamlit as st
from sentence_transformers import SentenceTransformer
from time import sleep


class PineconeInterface:
    def __init__(self, api_key, index_name):
        pass
    def search_vectors(self, query_vector, top_k):
        return [
            'In a distant future, where advanced technology coexists with nature, a lone explorer discovers an ancient artifact that holds the key to restoring balance to the world. As the explorer delves deeper into the mystery, they encounter unexpected allies and formidable challenges that will test their courage and determination.',
            'On a magical island hidden from the mortal world, a young sorcerer embarks on a quest to unlock their latent powers and fulfill their destiny. Along the way, they form bonds with mythical creatures and face trials that reveal the true strength lying within their heart.',
            'In a steampunk city ruled by airships and clockwork marvels, a brilliant inventor stumbles upon a forgotten blueprint that could revolutionize the entire society. As the inventor races against time to build the extraordinary machine, they must navigate political intrigue and industrial espionage to ensure the world-changing invention does not fall into the wrong hands.',
            'In a parallel dimension where dreams come to life, a curious dreamwalker discovers a hidden realm filled with whimsical creatures and surreal landscapes. However, as they explore deeper, they uncover a dark force threatening to engulf the dreamworld in eternal nightmares, and the dreamwalker must confront their fears to save both realms.',
            'In a medieval kingdom plagued by a mysterious curse, a young knight sets out on a quest to find the legendary Sword of Radiance, said to be the only weapon capable of breaking the enchantment. Along the way, they forge alliances with mystical beings and face mythical creatures guarding the sword, testing their loyalty and valor.',
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
            # Call the search function with the keyword and get results
            self.result = self.search(keyword, num_books)
            sleep(1)
                
            
        # Display search results as buttons
        for i, book in enumerate(self.result):
            if st.button(f"Book {i + 1}: {book}"):
                # Call the read function or perform other actions with the selected book
                st.write(f"Selected book: {book}")
                    
        

    def search(self, keyword, num_books):
        # Call Pinecone's search_vectors function with the keyword
        query_vector = self.story2vector.encode(keyword)
        search_results = self.pinecone_interface.search_vectors(query_vector, top_k=num_books)
        return search_results


    
if __name__ == '__main__':
    ui = UI_search()
    ui.UI()