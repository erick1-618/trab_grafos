import time
from graphs import generate_random_graph
from mpp import djikstra

max_weight = 20

tamanhos = {
    "pequeno": 10,
    "médio": 100,
    "grande": 500
}

for tamanho_nome, n_vertexes in tamanhos.items():
    print(f"\n=== Benchmark com {n_vertexes} vértices ({tamanho_nome}) ===")
    
    # Grafo esparso: mesmo número de vértices e arestas
    sparse_graph = generate_random_graph(n_vertexes, n_vertexes, True, max_weight)
    
    start_time = time.time()
    distances_sparse = djikstra(sparse_graph, list(sparse_graph.vertexes.keys())[0])
    end_time = time.time()
    print(f"Tempo grafo esparso: {end_time - start_time:.10f} segundos")
    
    # Grafo denso: bem mais arestas que vértices
    dense_graph = generate_random_graph(n_vertexes, n_vertexes * 10, False, max_weight)
    
    start_time = time.time()
    distances_dense = djikstra(dense_graph, list(dense_graph.vertexes.keys())[0])
    end_time = time.time()
    print(f"Tempo grafo denso: {end_time - start_time:.10f} segundos")
