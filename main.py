import pinecone

# pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENVIRONMENT")
# index = pinecone.Index("pinecone-index")

class PineconeInterface:
    def __init__(self, api_key, index_name, index_dim):
        # pinecone.init(api_key=api_key)
        # self.index = pinecone.Index(index_name)
        pinecone.init(api_key=api_key)
        _ = self.create_index(index_name, index_dim)
        self.index = pinecone.Index(index_name)
        self.index_dim = index_dim
        self.index_name = index_name

    def create_index(index_name, index_dim):
        pinecone.create_index(index_name, dimension=index_dim, metric="cosine", pods=4, pod_type="s1.x1")
        return pinecone.describe_index(index_name)

    def insert_vector(self, index_name=None, vector_id, vector_data, vector_num=1):
        if index_name = None: index_name = self.index_name

        with pinecone.Index(self.index_name, pool_threads=20) as index:
            async_results = [
                index.upsert(vectors=ids_vectors_chunk, async_req=True)
                for ids_vectors_chunk in chunks(items=[(vector_id, vector_data)], batch_size=100)
            ]
            [async_result.get() for async_result in async_results]

        self.index.upsert(items=[(vector_id, vector_data)])
        return index.describe_index_stats()

    def search_vectors(self, query_vector, top_k=5):
        pass


if __name__ == '__main__':
    print("hello world")

"""
# Upsert data with 100 vectors per upsert request asynchronously
# - Create pinecone.Index with pool_threads=30 (limits to 30 simultaneous requests)
# - Pass async_req=True to index.upsert()
with pinecone.Index('example-index', pool_threads=30) as index:
    # Send requests in parallel
    async_results = [
        index.upsert(vectors=ids_vectors_chunk, async_req=True)
        for ids_vectors_chunk in chunks(example_data_generator, batch_size=100)
    ]
    # Wait for and retrieve responses (this raises in case of error)
    [async_result.get() for async_result in async_results]
"""