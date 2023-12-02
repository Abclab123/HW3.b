import pinecone

# pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENVIRONMENT")
# index = pinecone.Index("pinecone-index")

class PineconeInterface:
    def __init__(self, api_key, index_name):
        pinecone.init(api_key=api_key)
        self.index = pinecone.Index(index_name)
        pinecone.init()

    def create_index(index_name, index_dim):
        pinecone.create_index(index_name, dimension=index_dim, metric="cosine", pods=4, pod_type="s1.x1")
        return pinecone.describe_index(index_name)

    def insert_vector(self, vector_id, vector_data):
        self.index.upsert(items=[(vector_id, vector_data)])

    def search_vectors(self, query_vector, top_k=5):
        pass


if __name__ == '__main__':
    print("Hello world")
    pineconePipe = PineconeInterface(api_key, index_name)