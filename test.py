import random 
vector_dim = 2
vector_count = 10
example_data_generator = map(lambda i: (f'id-{i}', [random.random() for _ in range(vector_dim)]), range(vector_count))
print(*list(example_data_generator), sep="\n")