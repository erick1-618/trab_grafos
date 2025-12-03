import uuid
import random
import string
import yaml

class Graph:
    def __init__(self, kind):
        """
        Initializes a empty graph
        Args:
            kind: determines the direcionality of the graph. "t" for targeted, "n" for no-targeted
        """

        if kind not in ['t', 'n']:
            raise ValueError('Kind must be "t" for targeted graphs or "n" for non-targeted')
        
        self.kind = kind
        self.vertexes = {}

    def add_vertex(self, name=None):
        """
        Inserts a vertex in the graph
        Args:
            name: vertex name
        """

        unique_name = name if name != None else uuid.uuid4()

        self.vertexes[unique_name] = {}

    def add_edge(self, origin, destination, w, name=None):
        """
        Inserts an edge into the graph
        Args:
            origin: origin vertex
            destination: destination vertex
            w: weight of the edge
            name: unique name for the edge
        """
    
        unique_name = name if name != None else uuid.uuid4()

        self.vertexes[origin][unique_name] = {'dest': destination,'weight': w}

        # Inserting the reverse edge for non-targeted ones
        if self.kind == 'n':
            self.vertexes[destination][f'{unique_name}_R'] = {'dest': origin,'weight': w}

    def rem_edge(self, e_name):
        """
        Removes an edge from the graph
        Args:
            e_name: name of the edge
        """

        for v, edges in self.vertexes.items():
            if e_name in edges.keys():
                del edges[e_name]

                # Deleting the reverse edge for non-targeted ones
                if self.kind == 'n':
                    self.rem_edge(f'{e_name}_R')
                break

    def rem_vertex(self, name):
        """
        Remove a vertex from the graph and all of its edges
        Args:
            name: name of the vertex
        """

        for v, edges in self.vertexes.items():

            edges_for_deletion = []

            for edge, info in edges.items():
                if info['dest'] == name:
                    edges_for_deletion.append(edge)

            for e in edges_for_deletion:
                del edges[e]

        del self.vertexes[name]

    def __str__(self):
        vertexes = self.vertexes
        vertex_and_edges = ''
        for v in vertexes.keys():
            edges = vertexes[v]
            vertex_and_edges += f'{v}'
            for edge, info in edges.items():
                vertex_and_edges += f' -> ({edge}) ({info['dest']}) {info['weight']}'
            vertex_and_edges += '\n'
        return vertex_and_edges
    
def generate_random_graph(n_v, n_e, is_simple, max_weight):
    """
    Creates a random Graph object
    Args:
        n_v: number of vertexes
        n_e: number of edges
        is_simples: determines if the graph is simple or not
    """

    g = Graph('t')

    for _ in range(n_v):
        while True:
            v_name = f'{random.choice(string.ascii_uppercase)}-{random.choice(range(n_v))}'
            if v_name not in g.vertexes.keys():
                break
        g.add_vertex(v_name)

    for _ in range(n_e):
        
        while True:

            vertexes = list(g.vertexes.keys())

            origin = random.choice(vertexes)
            destination = random.choice(vertexes)

            if is_simple:
                break

            if origin != destination and destination not in g.vertexes[origin].keys():
                break
        
        weight = random.randint(0, max_weight)

        g.add_edge(origin, destination, weight)

    return g

def import_graph(graph_file):
    """
    Reads a yaml file containing informations about the graph and returns the correspondent Graph object
    Args:
        graph_file: the graph yaml file
    """

    with open(graph_file, 'r') as file: 
        graph_data = yaml.safe_load(file)

    g = Graph(graph_data['dir'])

    vertexes = graph_data['vertexes']

    for v in vertexes:
        g.add_vertex(v)

    edges = graph_data['edges']

    for e in edges:
        origin, destination, weight = e.split('-')
        g.add_edge(origin, destination, int(weight))

    return g