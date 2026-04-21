import heapq

from graphs import Graph
from math import inf
from concurrent.futures import ThreadPoolExecutor

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

def pivot_sssp_graph_seq(G, source, width=10, num_pivots=5, limit=50):

    """
    Pivot-SSSP implementation

    See more in: https://arxiv.org/pdf/2504.17033
    """

    vertices = list(G.vertexes.keys())
    idx_of = {v: i for i, v in enumerate(vertices)}
    id_of = {i: v for v, i in idx_of.items()}
    n = len(vertices)

    graph = [[] for _ in range(n)]
    for u in vertices:
        u_idx = idx_of[u]
        for info in G.vertexes[u].values():
            v = info["dest"]
            w = info["weight"]
            graph[u_idx].append((idx_of[v], w))

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

        # Execução SEQUENCIAL
        for p in pivots:
            expand_pivot(p, graph, dist, lo, hi, limit)

        for u in S:
            finished.add(u)

        max_dist += width

    return {id_of[i]: dist[i] for i in range(n)}

# DEPRECATED - DOESN'T FOLLOW DE ORIGINAL ARTICLE PRINCIPLES
def pivot_sssp_graph_shared(G, source, width=10, num_pivots=5, limit=50):
    vertices = list(G.vertexes.keys())
    idx_of = {v: i for i, v in enumerate(vertices)}
    id_of = {i: v for v, i in idx_of.items()}
    n = len(vertices)

    graph = [[] for _ in range(n)]
    for u in vertices:
        u_idx = idx_of[u]
        for info in G.vertexes[u].values():
            v = info["dest"]
            w = info["weight"]
            graph[u_idx].append((idx_of[v], w))

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

        # Execução PARALELA (memória compartilhada)
        with ThreadPoolExecutor(max_workers=len(pivots)) as executor:
            executor.map(
                lambda p: expand_pivot(p, graph, dist, lo, hi, limit),
                pivots
            )

        for u in S:
            finished.add(u)

        max_dist += width

    return {id_of[i]: dist[i] for i in range(n)}

# DEPRECATED: DOENSN'T USE THE ARTICLE PRINCIPLES
def expand_pivot(p, graph, dist, lo, hi, limit):

    """
    Common function for expanding the pivot, executing a 'mini-dijkstra'
    """

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
