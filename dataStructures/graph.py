from typing import Dict, List, Tuple, Any
import json


class Graph:
    """Simple undirected weighted graph using adjacency lists.

    Nodes are identified by strings or integers. Edges carry a weight (travel_time)
    and optional metadata (distance, cost, etc.).
    """

    def __init__(self):
        # adjacency: node -> list of (neighbor, weight, metadata)
        self.adj: Dict[Any, List[Tuple[Any, float, Dict[str, Any]]]] = {}

    def add_node(self, node_id: Any) -> None:
        if node_id not in self.adj:
            self.adj[node_id] = []

    def add_edge(self, u: Any, v: Any, weight: float = 1.0, metadata: Dict[str, Any] | None = None) -> None:
        """Add undirected edge between u and v with given weight and optional metadata."""
        self.add_node(u)
        self.add_node(v)
        meta = metadata or {}
        self.adj[u].append((v, float(weight), meta))
        self.adj[v].append((u, float(weight), meta))

    def neighbors(self, node_id: Any) -> List[Tuple[Any, float, Dict[str, Any]]]:
        return list(self.adj.get(node_id, []))

    def nodes(self) -> List[Any]:
        return list(self.adj.keys())

    def edges(self) -> List[Tuple[Any, Any, float, Dict[str, Any]]]:
        seen = set()
        out: List[Tuple[Any, Any, float, Dict[str, Any]]] = []
        for u, lst in self.adj.items():
            for v, w, meta in lst:
                key = tuple(sorted((str(u), str(v))))
                if key in seen:
                    continue
                seen.add(key)
                out.append((u, v, w, meta))
        return out

    def get_edge_weight(self, u: Any, v: Any) -> float | None:
        for nbr, w, _ in self.adj.get(u, []):
            if nbr == v:
                return w
        return None


def load_graph_from_json(regions_path: str, roads_path: str) -> Graph:
    """
    Load graph from regions.json and roads.json files.
    
    Entrada:
        regions_path: caminho para regions.json
        roads_path: caminho para roads.json
    
    Retorno:
        Graph instance com nós e arestas carregadas
    """
    graph = Graph()
    
    # Carregar regiões (nós)
    with open(regions_path, 'r', encoding='utf-8') as f:
        regions = json.load(f)
    for region in regions:
        graph.add_node(region['id'])
    
    # Carregar estradas (arestas)
    with open(roads_path, 'r', encoding='utf-8') as f:
        roads = json.load(f)
    for road in roads:
        graph.add_edge(
            road['from'],
            road['to'],
            weight=road['travel_time'],
            metadata={'distance_km': road['distance_km']}
        )
    
    return graph

