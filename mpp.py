from graphs import Graph
from math import inf
import heapq

def djikstra(graph: Graph, origin):
    """
    Function that implements the Djikstra Algorithm for the Minimum Path Problem
    args:
        graph: the Graph input
        origin: the origin vertex
    """

    # The dict with every vertex and its edges
    vertexes = graph.vertexes

    # Data structure for keeping every cost of every vertex
    distances = {}

    # Initizalize the distances
    for v in vertexes.keys():
        distances[v] = inf
    distances[origin] = 0

    pq = []
    heapq.heappush(pq, (0, origin))

    while len(pq) != 0:

        dist_u, u = heapq.heappop(pq)

        #Ignores old entries
        if dist_u > distances[u]:
            continue

        for info_edges in vertexes[u].values():
            neighboor_vertex = info_edges['dest']

            alternative = distances[u] + info_edges['weight']

            if alternative < distances[neighboor_vertex]:
                distances[neighboor_vertex] = alternative
                heapq.heappush(pq, (alternative, neighboor_vertex))

    return distances

def enhanced_djikstra(graph: Graph, origin):
    """
    Algorithm that implements the new "version" of Djikstra Algorithm, which uses Divide and Conquer paradigm, fusing Djikstra and Belman-Ford

    For more info, visit https://arxiv.org/pdf/2504.17033
    """