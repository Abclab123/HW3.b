import pinecone

class PineconeInterface:
    def __init__(self, api_key, index_name):
        # pinecone.init(api_key=api_key)
        # self.index = pinecone.Index(index_name)
        pinecone.init(
            api_key=api_key,
            environment=gcp-starter
        )
        print(pinecone.whoami())
        if index_name not in pinecone.list_indexes():
             _ = self.create_index(index_name)
        self.index = pinecone.GRPCIndex(index_name)
        self.index_dim = None
        self.index_name = index_name

    def change_index(index_name):
        self.index = pinecone.GRPCIndex(index_name)
        return pinecone.describe_index(index_name)

    def create_index(index_name, index_dim=1024):
        if self.index_name != index_name: self.index_name = index_name
        if self.index_dim != index_dim: self.index_dim = index_dim
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                index_name,
                dimension=index_dim,
                metric="cosine",
                pods=4, pod_type="s1.x1")
                # pod_type_dim: 512=8,000,000, 768=5,000,000, 1024=4,000,000
        # Todo: deal error here or not?
        return pinecone.describe_index(index_name)

    def delete_index(index_name):
        pinecone.delete_index(index_name)
        return index.describe_index_stats()

    def get_vector(vector_id):
        vectors = self.index.fetch(ids=vector_id)
        return vectors

    def insert_vector(self, index_name=None, vector_id, vector_data, vector_num=1):
        if index_name == None: index_name = self.index_name
        ids_vectors_chunk = items=[(vector_id, vector_data)]

        with pinecone.GRPCIndex(self.index_name, pool_threads=20) as index:
            async_results = [
                index.upsert(vectors=ids_vectors_chunk, async_req=True)
                for ids_vectors_chunk in chunks(items=[(vector_id, vector_data)], batch_size=10)     # not sure what if vector less than 10
            ]
            [async_result.get() for async_result in async_results]

        self.index.upsert(items=[(vector_id, vector_data)])
        return index.describe_index_stats()

    def search_vectors(self, query_vector, top_k=5):
        # query sparse-dense vectors
        relevant_contexts = self.index.query(query_vector, top_k, include_values=True, include_metadata=True)
        contexts = [ [ x['score'], x['metadata']['text'] ] for x in relevant_contexts['matches'] ]
        return contexts

    def show_indexes():
        return pinecone.list_indexes()

def get_file_contents(filename):
    try: with open(filename, 'r') as f:
        return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

if __name__ == '__main__':
    filename = "api_key"
    api_key = get_file_contents(filename)

    # test for add a index
    index_name = "quickstart" # index of quickstart used for the test 
    index_dim = 1024
    cone = PineconeInterface(api_key, index_name)
    cone.create_index(index_name, index_dim)
    print(cone.show_indexes())

    # test for insert data
    num_embeddings = 999
    embeddings_for_pinecone = np.random.rand(num_embeddings, 128)
    result = cone.insert_vector(index_name, [str(i) for i in range(num_embeddings)], [embeddings_for_pinecone[i].tolist() for i in range(num_embeddings)], num_embeddings)
    print(result)

    # test for get vectors
    vectors = cone.get_vector([str(i) for i in range(num_embeddings)])
    ids = list()
    embeddings = list()
    for id, vector in vectors['vectors'].items():
        ids.append(id)
        embeddings.append(vector['values'])
    embeddings = np.array(embeddings)
    print(*ids, sep="\n")
    print(*embeddings, sep="\n")

    # test for search vector
    queries = [str(i) for i in range(num_embeddings/10)]
    contents = core.search_vectors(queries)
    print(contents)

    # Once we're done with the index we delete it to save resources
    core.delete_index(index_name)   # must remain this here