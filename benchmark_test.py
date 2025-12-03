from time import time
from graphs import generate_random_graph
from mpp import dijkstra, pivot_sssp_graph
import csv

# Tamanhos dos grafos
tamanhos = (10, 100, 500)

# Modelos de MPP
modelos = {
    'dijkstra': dijkstra,
    'pivot_sssp': pivot_sssp_graph
}

# Fator do tipo de grafo
tipo_grafo = {
    'esparso': 1,
    'denso': 0
}

# Peso máximo das arestas
max_weight = 20

with open('benchmark_results.csv', mode='w', newline='') as file:

    # Cria o objeto writer
    writer = csv.writer(file, delimiter=';')
    
    # Escreve o cabeçalho do csv
    writer.writerow(["tamanho", "modelo_mpp", "tipo_grafo", "tempo"])

    x = 30

    # Cada combinação de possibilidade de execução será realizada x vezes
    for _ in range(x):
        for tamanho in tamanhos:
            for tipo, fator in tipo_grafo.items():
                
                # Gera o grafo aleatório
                grafo = generate_random_graph(tamanho, tamanho * fator, True, 20)

                for modelo, func in modelos.items():

                    # Medição de uma execução
                    inicio = time()
                    distancias = func(grafo, list(grafo.vertexes.keys())[0])
                    fim = time()

                    tempo = fim - inicio

                    # Escrita do resultado no csv
                    writer.writerow([tamanho, modelo, tipo, tempo])


