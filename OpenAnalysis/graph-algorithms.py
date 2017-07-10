
class UnionFind:
    """Union-find data structure.

    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:

    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.

    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.

      Union-find data structure. Based on Josiah Carlson's code,
      http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
      with significant additional changes by D. Eppstein.
      http://www.ics.uci.edu/~eppstein/PADS/UnionFind.py

    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure.

        """
        return iter(self.parents)

    def union(self, *objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        # Find the heaviest root according to its weight.
        heaviest = max(roots, key=lambda r: self.weights[r])
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


class PriorityQueue:
    def __init__(self):
        self.heap = []

    def add_task(self,task,priority):
        import heapq
        heapq.heappush(self.heap,(priority,task))

    def remove_min(self):
        import heapq
        return heapq.heappop(self.heap)[1]

    def remove(self,task):
        import heapq
        for task_pair in self.heap:
            if task_pair[1] == task:
                self.heap.remove(task_pair)
                heapq.heapify(self.heap)

    def update_task(self,task,new_priority):
        self.remove(task)
        self.add_task(task,new_priority)


import networkx as nx
import matplotlib.pyplot as plt


def kruskal_mst(G):
    """
    Finds Minimum Spanning Tree of graph by Kruskal's Algorithm
    :param G: networkx graph
    :return: iterator through edges of Minimum spanning Tree
    """
    edge_list = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    subtrees = UnionFind()
    for u, v, w in edge_list:
        if subtrees[u] != subtrees[v]:
            yield (u, v, {'weight': w})
            subtrees.union(u, v)


def prim(G):
    """
    Finds Minimum Spanning Tree of graph by Prim's Algorithm
    :param G: networkx graph
    :return: iterator through edges of Minimum spanning Tree
    """
    V = G.nodes()       # Set of all vertices of G
    while V:
        # We pop the nodes as soon as they are visited,
        # so this means "until all the nodes are visited"
        u = V.pop(0)    # Now remove the first vertex and start building the tree
        visited = {u}   # Set of visited nodes
        stringe_heap = []  # Store the stringe nodes with weights
        import heapq
        for v in G.neighbors(u):
            heapq.heappush(stringe_heap,
                           (G.edge[u][v]['weight'], u, v))
            # Now build the min heap storing (weight,source,dest) tuples
            # Tuples are sorted by their first element
        # Now start popping from heap,and build MST
        while stringe_heap:
            weight, u_star, v_star = heapq.heappop(stringe_heap)
            if v_star in visited:  # No need to do anything since v_star is already visited
                continue
            visited.add(v_star)  # Mark dest as visited
            V.remove(v_star)
            yield (u_star, v_star, {'weight': weight})  # yield the edge
            for w_star in G.neighbors(v_star):  # Update strige heap with neighbour edges of v_star
                if w_star not in visited:
                    heapq.heappush(stringe_heap, (G.edge[v_star][w_star]['weight'], v_star, w_star))


def dfs(G, root=None):
    """
    Iterates through edges of DFS tree of G
    :param G: networkx Graph
    :param root: node to start DFS from. If it is none, DFS is done for all components of G
                 else DFS is done for components connected with root
    :return: Iterator of edges of DFS tree
    """
    visited = set()
    if root is None:
        nodes = G.nodes()       # nodes to visit
    else:
        nodes = [root]
    for start in nodes:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, child) for child in sorted(G.neighbors(start), reverse=True)]
        while stack:
            parent, child = stack.pop()
            if child not in visited:
                visited.add(child)
                yield (parent, child)
                stack += [(child, grandchild) for grandchild in sorted(G.neighbors(child), reverse=True)]


def bfs(G, root=None):
    """
        Iterates through edges of DFS tree of G
        :param G: networkx Graph
        :param root: node to start DFS from. If it is none, DFS is done for all components of G
                     else DFS is done for components connected with root
        :return: Iterator of edges of DFS tree
        """
    visited = set()
    if root is None:
        nodes = G.nodes()
    else:
        nodes = [root]
    for start in nodes:
        if start in visited:
            continue
        visited.add(start)
        Q = [start]
        while Q:
            current = Q.pop(0)
            for n in sorted(G.neighbors(current)):
                if n not in visited:
                    visited.add(n)
                    Q.append(n)
                    yield (current, n)


def dijsktra(G, source=None):
    """
    Returns edges of Single source shortest path starting form source
    :param G: networkx Graph
    :param source: source to compute the distances from
    :return: Iterator through edges of SSSP Tree
    """
    if source is None: source = G.nodes()[0]
    V = G.nodes()
    dist, prev = {}, {}
    Q = PriorityQueue()
    for v in V:
        dist[v] = float("inf")
        prev[v] = None
        Q.add_task(task=v,priority=dist[v])
    dist[source] = 0
    Q.update_task(task=source,new_priority=dist[source])
    visited = set()
    for i in range(0, len(G.nodes())):
        u_star = Q.remove_min()
        if prev[u_star] is not None:
            yield (u_star, prev[u_star])
        visited.add(u_star)
        for u in G.neighbors(u_star):
            if u not in visited and dist[u_star] + G.edge[u][u_star]['weight'] < dist[u]:
                dist[u] = dist[u_star] + G.edge[u][u_star]['weight']
                prev[u] = u_star
                Q.update_task(u,dist[u])


def tree_growth_visualizer(fun):
    """
    Visualizer function for Graph algorithms yielding the edges
    :param fun: A function which has the signature f(G) and returns iterator of edges of graph G
    :return: Saves the images of growth step in given directory. ffmpeg can be used to make video
    """
    G = nx.random_geometric_graph(100, .125)
    # position is stored as node attribute data for random_geometric_graph
    pos = nx.get_node_attributes(G, 'pos')
    # find node near center (0.5,0.5)
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d
    for u, v in G.edges():
        G.edge[u][v]['weight'] = ((G.node[v]['pos'][0] - G.node[u]['pos'][0]) ** 2 +
                                  (G.node[v]['pos'][1] - G.node[u]['pos'][1]) ** 2) ** .5
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.axis('off')
    edge_list = []
    i = 0
    for i, edge in enumerate(fun(G)):
        plt.clf()
        nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
        T = nx.Graph(edge_list)
        nx.draw_networkx_edges(T, pos, nodelist=[ncenter], edge_color="r")
        nx.draw_networkx_nodes(T, pos, node_color='g', alpha=0.5, node_size=100)
        plt.axis('off')
        plt.savefig("test/fig%04d.png" % (i))
        print(i)
        edge_list += [edge]
    plt.clf()
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    T = nx.Graph(edge_list)
    nx.draw_networkx_edges(T, pos, nodelist=[ncenter], edge_color="r")
    nx.draw_networkx_nodes(T, pos, node_color='g', alpha=0.5, node_size=100)
    plt.axis('off')
    plt.savefig("test/fig%04d.png" % i)


if __name__ == "__main__":
    tree_growth_visualizer(dijsktra)
