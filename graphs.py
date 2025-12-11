from dataclasses import dataclass
import json

@dataclass
class Node:
    x: int
    y: int
    n_id: int

@dataclass
class Edge:
    a: Node
    b: Node
    a_id: int
    b_id: int

def xyToIdx(x, y, w):
    return x+w*y

@dataclass
class Graph:
    nodes: list[Node]
    edges: list[Edge]

    def to_json_file(self, filepath):
        """Dump the graph to a JSON file"""
        # Serialize nodes
        nodes_data = [
            {"x": node.x, "y": node.y, "n_id": node.n_id}
            for node in self.nodes
        ]

        # Serialize edges (store only IDs, not full node objects)
        edges_data = [
            {"a_id": edge.a_id, "b_id": edge.b_id}
            for edge in self.edges
        ]

        graph_data = {
            "nodes": nodes_data,
            "edges": edges_data
        }

        with open(filepath, 'w') as f:
            json.dump(graph_data, f, indent=2)

    @classmethod
    def from_json_file(cls, filepath):
        """Load a graph from a JSON file"""
        with open(filepath, 'r') as f:
            graph_data = json.load(f)

        # Reconstruct nodes
        nodes = [
            Node(x=node_data["x"], y=node_data["y"], n_id=node_data["n_id"])
            for node_data in graph_data["nodes"]
        ]

        # Create a mapping from node ID to node object for efficient lookup
        node_map = {node.n_id: node for node in nodes}

        # Reconstruct edges
        edges = [
            Edge(
                a=node_map[edge_data["a_id"]],
                b=node_map[edge_data["b_id"]],
                a_id=edge_data["a_id"],
                b_id=edge_data["b_id"]
            )
            for edge_data in graph_data["edges"]
        ]

        return cls(nodes=nodes, edges=edges)

class RectGridGraph(Graph):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.nodes = [Node(x, y, x+w*y) for y in range(h) for x in range(w)]
        self.edges = []
        for y in range(h):
            for x in range(w):
                a_id = x+w*y
                a = self.nodes[a_id]
                if x < w-1:
                    b_id = x+1+w*y
                    b = self.nodes[b_id]
                    self.edges.append(Edge(a, b, a_id, b_id))

                if y < h-1:
                    b_id = x+w*(y+1)
                    b = self.nodes[b_id]
                    self.edges.append(Edge(a, b, a_id, b_id))
