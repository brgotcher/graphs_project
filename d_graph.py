# Course: CS261 - Data Structures
# Author:
# Assignment:
# Description:

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        add a new vertex to the adjacency matrix
        """
        # add a new item to the end of each existing list for the new vertex
        for i in range(self.v_count):
            self.adj_matrix[i].append(0)
        # increment the vertex count and add a new list of 0's for the new vertex
        self.v_count += 1
        self.adj_matrix.append([0] * self.v_count)

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        add a new edge to the specified vertex
        """
        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        reset the specified edge to 0
        """
        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        return a list of vertices- since the vertices are only represented by
        index, this list is basically just a count
        """
        vertices = []
        for i in range(self.v_count):
            vertices.append(i)
        return vertices

    def get_edges(self) -> []:
        """
        return a list of all edges as tuples: (source, destination, weight)
        """
        edges = []
        # iterate through outer list of source vertices
        for i in range(self.v_count):
            # iterate inner list of destination vertices
            for j in range(self.v_count):
                # if the value is anything other than 0, this is an edge and
                # should be appended to the edges list
                weight = self.adj_matrix[i][j]
                if weight:
                    edges.append((i, j, weight))
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        accepts a list of vertex indices and returns true if the list
        represents a valid path along existing edges
        """
        # iterate through the path list
        for i in range(len(path)-1):
            # if weight between the current and next vertices in the path
            #
            if not self.adj_matrix[path[i]][path[i+1]]:
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        depth first search starting at v_start
        if v_end argument is provided, stop the search
         when/if v_end is encountered
        returns a list showing the order of vertices traversed
        """
        if v_start < 0 or v_start >= self.v_count:
            return []

        temp = []
        visited = []

        temp.append(v_start)
        while temp:
            v = temp.pop()
            if v not in visited:
                visited.append(v)
                source = self.adj_matrix[v]
                if v == v_end:
                    return visited
                new_verts = []
                for u in range(self.v_count):
                    if source[u] and u not in visited:
                        new_verts.append(u)
                new_verts.sort(reverse=True)
                for i in new_verts:
                    temp.append(i)
        return visited



    def bfs(self, v_start, v_end=None) -> []:
        """
        breadth first search starting with v_start
        """
        if v_start < 0 or v_start >= self.v_count:
            return []

        temp = []
        visited = []

        temp.append(v_start)
        while temp:
            v = temp.pop(0)
            if v not in visited:
                visited.append(v)
                source = self.adj_matrix[v]
                if v == v_end:
                    return visited
                new_verts = []
                for u in range(self.v_count):
                    if source[u] and u not in visited:
                        new_verts.append(u)
                for i in new_verts:
                    temp.append(i)
        return visited

    def has_cycle(self):
        """
        TODO: fix this
        """
        visited = [0] * self.v_count
        active = [0] * self.v_count
        for i in range(self.v_count):
            if self.cycle_helper(i, visited, active):
                return True
        return False

    def cycle_helper(self, i, visited, active):
        if (active[i]):
            return True

        if visited[i]:
            return False

        visited[i] = 1
        active[i] = 1

        neighbors = self.adj_matrix[i]

        for j in range(self.v_count):
            if neighbors[j] and self.cycle_helper(j, visited, active):
                return True

        active[i] = 0
        return False


    def dijkstra(self, src: int) -> []:
        """
        finds the shortest path from the source vertex to all other vertices
        """
        # use a priority queue
        pq = []
        visited = [float('inf')] * self.v_count

        # push the source vertex to the priority queue with a distance of 0
        heapq.heappush(pq, [0, src])

        # keep popping as long as the pq is not empty
        while len(pq) > 0:
            temp = heapq.heappop(pq)
            d = temp[0]
            v = temp[1]

            # if the vertex hasn't been visited:
            if visited[v] == float('inf'):
                visited[v] = d

                # iterate all neighbor vertices
                for i in range(self.v_count):
                    dist = self.adj_matrix[v][i]
                    if dist:
                        heapq.heappush(pq, [d + dist, i])
        return visited





if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)
    #
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)


    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    #
    # edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    # for src, dst in edges_to_remove:
    #     g.remove_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    #
    # edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    # for src, dst in edges_to_add:
    #     g.add_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    # print('\n', g)



    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')

