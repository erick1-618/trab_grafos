from graphs import Graph
from math import inf
import heapq

def dijkstra(graph: Graph, origin):
    """
    Function that implements the Dijkstra Algorithm for the Minimum Path Problem
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

def pivot_sssp_graph(G, source, width=10, num_pivots=5, limit=50):
    """
    Pivot-SSSP implementation

    See more in: https://arxiv.org/pdf/2504.17033
    """

    # --- 1) Mapping vertexes to indexes ---
    vertices = list(G.vertexes.keys())
    idx_of = {v: i for i, v in enumerate(vertices)}
    id_of = {i: v for v, i in idx_of.items()}

    n = len(vertices)

    # --- 2) Adapting the adjacency list of Graph obj---
    # graph[u] = [(v, w), ...]
    graph = [[] for _ in range(n)]
    for u in vertices:
        u_idx = idx_of[u]
        for edge, info in G.vertexes[u].items():
            v = info["dest"]
            w = info["weight"]
            v_idx = idx_of[v]
            graph[u_idx].append((v_idx, w))

    # --- 3) Adapting the original algorithm ---
    INF = float("inf")
    dist = [INF] * n
    dist[idx_of[source]] = 0

    max_dist = 0
    finished = set()

    while True:
        lo = max_dist
        hi = max_dist + width

        S = [u for u in range(n) if lo <= dist[u] < hi and u not in finished]
        if not S:
            break

        pivots = sorted(S, key=lambda x: dist[x])[:num_pivots]

        for p in pivots:
            pq = [(dist[p], p)]
            expanded = 0
            visited = set()

            while pq and expanded < limit:
                d, u = heapq.heappop(pq)
                if u in visited:
                    continue
                visited.add(u)
                expanded += 1

                for v, w in graph[u]:
                    nd = d + w
                    if lo <= nd < hi and nd < dist[v]:
                        dist[v] = nd
                        heapq.heappush(pq, (nd, v))

        for u in S:
            finished.add(u)

        max_dist += width

    # --- 4) Converting to dictionary ---
    return { id_of[i]: dist[i] for i in range(n) }
