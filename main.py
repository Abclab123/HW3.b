import pinecone
from sentence_transformers import SentenceTransformer
import time
class text2vector:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1')

    def __call__(self, text):
        return self.model.encode(text)


class PineconeInterface:
    def __init__(self, api_key, index_name, create=True):
        pinecone.init(api_key=api_key, environment="gcp-starter")

        if index_name not in pinecone.list_indexes() and create:
            pinecone.create_index(index_name, dimension=768 ,metric="cosine")
        
        self.index = pinecone.Index(index_name)

    def insert_vector(self, all_embeddings):

        self.index.upsert(vectors=all_embeddings, async_req=False)

    def search_vectors(self, query, top_k=5, include_values=False):
        embedder = text2vector()
        query_embedding = embedder(query).tolist()
        
        results = self.index.query(vector=query_embedding, top_k=top_k)

        return results
    
    def delete_index(self):
        pinecone.delete_index(index_name)

    def fetch_vector(self, id):
        self.index.fetch([id])

if __name__ == '__main__':
    api_key = "847f30d1-e4ee-4be2-bdee-b3b7206bf8e0"

    #just temporary
    #(book name, book content)
    books = [
        ("book_1", "idkwuttoput but yap"), 
        ("book_2", "just random textt"), 
        ("book 3 name", "liao"),
        ("hmm book 4", "big data"),
        ("this is book 5", "night class"),
        ("book 6", "this will take a while to run for the first time"),
        ("7", "since you need to download the transformer model"),
        ("book 8", "but yap"),

    ]

    #creating the index, so each interface is equal to 1 index
    index_name = "testing"
    interface = PineconeInterface(api_key, index_name)

    #embedding text -> vector
    embedder = text2vector()
    counter = 0
    
    embeddings= []
    for book in books:
        #combined bookname + book content
        combined = book[0] + " " + book[1]

        text_embedding = embedder(combined).tolist()

        embeddings.append((str(counter), text_embedding))
        counter += 1

    interface.insert_vector(embeddings)

    print("input your search keyword:")
    query = input()

    #need to wait for insert vector to be done, cuz seems like it is asynchronous by default
    time.sleep(10)
                
    result = interface.search_vectors(query)

    print("The vector search, note: I dont print out the values cuz it will take all the terminal space")
    print(result['matches'])

    print("so this is the top 5 books which is most similar to the query u just put")
    for i in result['matches']:
        book = books[int(i['id'])]
        print(f"book name: {book[0]}\n book content: {book[1]}\n")

    #delete index after everything is done
    interface.delete_index()
