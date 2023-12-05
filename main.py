import pinecone
import numpy as np
import time

# insert API key here 
API_KEY = ""

class PineconeInterface:
    def __init__(self, api_key, index_name, create=True):
        pinecone.init(api_key=api_key, environment="gcp-starter")
        self.index = pinecone.Index(index_name)
        # print(self.index)
        if index_name not in self.list_indexes() and create:
            self.create_index(index_name)
        # pinecone.create_index()

    def insert_vector(self, vector_id, vector_data):
        return self.index.upsert(vectors=[(vector_id, vector_data)])

    def search_vectors(self, query_vector, top_k=5, include_values=False):
        results = self.index.query(vector=query_vector, top_k=top_k, include_values=include_values)
        return results
    
    def create_index(self, index_name, index_dim=1024, index_metric="cosine"):
        pinecone.create_index(
            name=index_name, 
            dimension=index_dim, 
            metric=index_metric,
        )
    
    def delete_index(self, index_name):
        return pinecone.delete_index(index_name)
    
    def list_indexes(self):
        return pinecone.list_indexes()
    
    def describe_content(self):
        return self.index.describe_index_stats()

    def delete_vector(self, vec_list):
        return self.index.delete(ids=vec_list)
    
    def fetch_vector(self, vec_list):
        return self.index.fetch(vec_list)
    

def main():
    index_name = "test"

    interface = PineconeInterface(
        api_key=API_KEY,
        index_name=index_name
    )

    # Below are sample testing for the class functionalities  
    
    # index creation
    print(interface.list_indexes()) # return: ['test']

    # vector insertion 
    n_books = 5
    books = [[f'book_{i}', np.random.rand(1024)] for i in range(n_books)] # book id, book data 
    for i in range(5):
        interface.insert_vector(books[i][0], books[i][1].tolist())
    
    print(interface.describe_content())

    time.sleep(12)

    try:
        # vector retrieval
        test_id = 'book_4'
        fetch_response = interface.fetch_vector([test_id])
        extracted_fetch_response = fetch_response.to_dict()['vectors'][test_id]
        print("fetched id:", extracted_fetch_response['id']) 
        # print(extracted_fetch_response['values'])

        # vector query
        query_vector = extracted_fetch_response['values'] # try to query previously fetched vector  
        # query_vector[0] = query_vector[-1] = 0.12341 # experiment to change the vector a bit
        query_response = interface.search_vectors(query_vector=query_vector)
        extracted_query_response = query_response.to_dict()['matches']
        top_match = extracted_query_response[0] # extract top match out of the k matches
        print(f"top match: {top_match['id']}, score: {top_match['score']}") # ideally top match should still be equal to test_id

        # index removal
        interface.delete_index(index_name)

    except IndexError:
        print("\033[91mIndex error occured. Try running again.\n")


if __name__ == "__main__":
    main()