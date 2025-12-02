import uuid

class Graph:
    def __init__(self, kind):
        """
        Initializes a empty graph
        Args:
            kind: determines the direcionality of the graph. "t" for targeted, "n" for no-targeted, and "m" for mixed
        """
        self.kind = kind
        self.vertexes = {}

    def add_vertex(self, name=None):
        """
        Insert a vertex in the graph
        Args:
            name: vertex name
        """

        unique_name = name if name != None else uuid.uuid4()

        self.vertexes[unique_name] = {}

    def add_edge(self, origin, destination, w, name=None):
        """
        Insert an edge into the graph
        Args:
            origin: origin vertex
            destination: destination vertex
            w: weight of the edge
            name: unique name for the edge
        """
    
        unique_name = name if name != None else uuid.uuid4()

        self.vertexes[origin][unique_name] = {'dest': destination,'weight': w}

    def rem_edge(self, e_name):
        """
        Remove an edge from the graph
        Args:
            e_name: name of the edge
        """

        for v, edges in self.vertexes.items():
            if e_name in edges.keys():
                del edges[e_name]
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