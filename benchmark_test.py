import time
from graphs import generate_random_graph
from mpp import dijkstra, pivot_sssp_graph
import csv

max_weight = 20

tamanhos = {
    "pequeno": 10,
    "médio": 100,
    "grande": 500
}
with open('benchmark_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["Tamanho", "Dijkstra Esparso", "Pivot SSSP Esparso", "Dijkstra Denso", "Pivot SSSP Denso"])

    for i in range(5):
            resultados_aux = []

            for tamanho_nome, n_vertexes in tamanhos.items():
                
                # Grafo esparso: mesmo número de vértices e arestas
                sparse_graph = generate_random_graph(n_vertexes, n_vertexes, True, max_weight)
                
                #sssp
                start_time = time.time()
                distances_sparse = pivot_sssp_graph(sparse_graph, list(sparse_graph.vertexes.keys())[0])
                end_time = time.time()
                resultados_aux.append(end_time - start_time)

                #Dijkstra normal
                start_time = time.time()
                distances_sparse = dijkstra(sparse_graph, list(sparse_graph.vertexes.keys())[0])
                end_time = time.time()
                resultados_aux.append(end_time - start_time)
                
                # Grafo denso: bem mais arestas que vértices
                dense_graph = generate_random_graph(n_vertexes, n_vertexes * 10, False, max_weight)
                #sssp
                start_time = time.time()
                distances_dense = pivot_sssp_graph(dense_graph, list(dense_graph.vertexes.keys())[0])
                end_time = time.time()
                resultados_aux.append(end_time - start_time)

                #Dijkstra normal
                start_time = time.time()
                distances_dense = dijkstra(dense_graph, list(dense_graph.vertexes.keys())[0])
                end_time = time.time()
                resultados_aux.append(end_time - start_time)

                linha_formatada = [tamanho_nome] + [f"{val:.6f}".replace('.', ',') for val in resultados_aux]
                writer.writerow(linha_formatada)
                resultados_aux = []