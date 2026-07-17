"""
Módulo de Algoritmos de Logística: MST (Kruskal) e Shortest Paths (Dijkstra)
Implementação manual de estruturas para Algoritmos e Estruturas de Dados (Módulo 7).
"""

class UnionFind:
    """Disjoint-set data structure (Union-Find) para Kruskal."""
    
    def __init__(self, elements):
        """Inicializar com lista de elementos únicos."""
        self.parent = {elem: elem for elem in elements}
        self.rank = {elem: 0 for elem in elements}
    
    def find(self, x):
        """Encontrar raiz do conjunto contendo x com path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Unir dois conjuntos. Retorna True se unidos, False se já estavam."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True


def mst_kruskal(graph):
    """
    Algoritmo de Kruskal para Árvore Geradora Mínima.
    
    Entrada:
        graph: Instância de Graph com método edges() e nodes()
    
    Retorno:
        (mst_edges, total_weight): tuple
            - mst_edges: lista de tuplas (from, to, weight)
            - total_weight: soma dos pesos das arestas
    """
    nodes = graph.nodes()
    edges = graph.edges()
    
    # Ordenar arestas por peso (ascending)
    sorted_edges = sorted(edges, key=lambda e: e[2])
    
    # Inicializar Union-Find
    uf = UnionFind(nodes)
    
    mst_edges = []
    total_weight = 0
    
    for from_node, to_node, weight, metadata in sorted_edges:
        if uf.union(from_node, to_node):
            mst_edges.append((from_node, to_node, weight))
            total_weight += weight
            
            if len(mst_edges) == len(nodes) - 1:
                break
    
    return mst_edges, total_weight


def dijkstra(graph, source):
    """
    Dijkstra's algorithm for shortest paths from a source node.
    
    Input:
        graph: Graph instance
        source: source node
    
    Returns:
        (distances, parents): tuple
            - distances: dict {node: shortest_distance_from_source}
            - parents: dict {node: parent_in_shortest_path} (None for source)
    """
    nodes = graph.nodes()
    distances = {node: float('inf') for node in nodes}
    parents = {node: None for node in nodes}
    distances[source] = 0
    
    unvisited = set(nodes)
    
    while unvisited:
        # Select unvisited node with smallest distance (greedy choice)
        current = min(unvisited, key=lambda n: distances[n])
        
        if distances[current] == float('inf'):
            break
        
        unvisited.remove(current)
        
        # Relax edges from current node
        for neighbor, weight, metadata in graph.neighbors(current):
            if neighbor in unvisited:
                new_dist = distances[current] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parents[neighbor] = current
    
    return distances, parents


def reconstruct_path(parents, source, target):
    """
    Reconstruir caminho mais curto de source até target usando dicionário de pais.
    
    Retorno:
        path: lista de nós [source, ..., target] ou None se não alcançável
    """
    if target not in parents:
        return None
    
    path = []
    current = target
    
    while current is not None:
        path.append(current)
        current = parents[current]
    
    path.reverse()
    return path if path[0] == source else None
