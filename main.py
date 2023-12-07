import pinecone
import numpy as np
import time
import itertools

def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

class PineconeInterface:
    def __init__(self, api_key, index_name, index_dim):
        # pinecone.init(api_key=api_key)
        # self.index = pinecone.Index(index_name)
        pinecone.init(
            api_key=api_key,
            environment="gcp-starter"
        )
        self.index_name = index_name
        self.index_dim = index_dim
        print(pinecone.whoami())
        print(pinecone.list_indexes())
        # if index_name not in pinecone.list_indexes():
        #     _ = self.create_index(index_name, index_dim)
        self.index = None

    def change_index(self, index_name):
        self.index = pinecone.Index(index_name)
        return pinecone.describe_index(index_name)

    def create_index(self, index_name, index_dim=1024):
        if self.index_name != index_name: self.index_name = index_name
        if self.index_dim != index_dim: self.index_dim = index_dim
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                index_name,
                dimension=index_dim,
                metric="cosine",
                pods=4, pod_type="s1.x1")
            self.index = pinecone.Index(index_name)
                # pod_type_dim: 512=8,000,000, 768=5,000,000, 1024=4,000,000
        # Todo: deal error here or not?
        return pinecone.describe_index(index_name)

    def delete_index(self, index_name):
        pinecone.delete_index(index_name)
        return self.show_indexes()
        # return self.index.describe_index_stats()

    def get_vector(self, vector_id):
        vectors = self.index.fetch(ids=vector_id)
        return vectors

    def insert_vector(self, vector_id, vector_data, index_name=None, vector_num=1):
        if index_name == None: index_name = self.index_name
        ids_vectors_chunk = zip(vector_id, vector_data)

        with pinecone.Index(index_name, pool_threads=20) as index:
            async_results = [
                index.upsert(vectors=ids_vectors_chunk, async_req=True)
                for ids_vectors_chunk in chunks(ids_vectors_chunk, batch_size=10)     # not sure what if vector less than 10
            ]
            [async_result.get() for async_result in async_results]
            return index.describe_index_stats()

        # self.index.upsert(items=[(vector_id, vector_data)])

    def search_vectors(self, query_vector, top_k=5):
        # query sparse-dense vectors
        print(query_vector, top_k)
        relevant_contexts = self.index.query(vector=query_vector, top_k=top_k, include_values=True)
        return relevant_contexts["matches"]

    def show_indexes(self):
        return pinecone.list_indexes()

def get_file_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

if __name__ == '__main__':
    filename = "api_key"
    api_key = get_file_contents(filename)

    # test for add a index
    index_name = "quickstart" # index of quickstart used for the test 
    index_dim = 4
    cone = PineconeInterface(api_key, index_name, index_dim)
    if index_name in pinecone.list_indexes():
        cone.delete_index(index_name)
    cone.create_index(index_name, index_dim)
    print(cone.show_indexes())

    # test for insert data
    num_embeddings = 10
    embeddings_for_pinecone = np.random.rand(num_embeddings, index_dim)
    result = cone.insert_vector([str(i) for i in range(num_embeddings)], [embeddings_for_pinecone[i].tolist() for i in range(num_embeddings)],index_name, num_embeddings)
    print(result)

    # test for get vectors
    vectors = cone.get_vector([str(i) for i in range(num_embeddings)])
    ids = list()
    embeddings = list()
    for id, vector in vectors['vectors'].items():
        ids.append(id)
        embeddings.append(vector['values'])
    embeddings = np.array(embeddings)
    print("id", *ids)
    print(*embeddings, sep="\n")


    time.sleep(60)

    print(pinecone.Index('quickstart').describe_index_stats())

    # test for search vector
    # queries = [str(i) for i in range(num_embeddings//10)]
    print(embeddings_for_pinecone[0].tolist())
    contents = cone.search_vectors(embeddings_for_pinecone[0].tolist())
    print(contents)

    # Once we're done with the index we delete it to save resources
    cone.delete_index(index_name)   # must remain this here