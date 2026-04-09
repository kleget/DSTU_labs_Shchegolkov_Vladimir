from collections import deque, Counter


# ---------- Задание 1 ----------
class UndirectedGraph:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, v):
        self.adj.setdefault(v, [])

    def add_edge(self, a, b):
        self.add_vertex(a)
        self.add_vertex(b)
        self.adj[a].append(b)
        self.adj[b].append(a)

    def read_from_file(self, name):
        self.adj = {}
        with open(name, 'r', encoding='utf-8') as f:
            for line in f:
                p = line.split()
                if not p:
                    continue
                if len(p) == 1:
                    self.add_vertex(p[0])
                elif len(p) >= 2:
                    self.add_edge(p[0], p[1])

    def write_to_file(self, name):
        with open(name, 'w', encoding='utf-8') as f:
            for v in self.adj:
                f.write(f'{v}\n')
            cnt = Counter()
            for a in self.adj:
                for b in self.adj[a]:
                    cnt[tuple(sorted((a, b)))] += 1
            for (a, b), k in cnt.items():
                for _ in range(k // 2):
                    f.write(f'{a} {b}\n')

    def degree(self, v):
        return len(self.adj.get(v, []))

    def is_adjacent(self, a, b):
        return b in self.adj.get(a, [])

    def has_loops(self):
        return any(v in self.adj[v] for v in self.adj)

    def has_parallel_edges(self):
        return any(any(c > 1 for c in Counter(self.adj[v]).values()) for v in self.adj)

    def dfs(self, start):
        if start not in self.adj:
            return []
        vis, st, res = {start}, [start], []
        while st:
            v = st.pop()
            res.append(v)
            for u in reversed(self.adj[v]):
                if u not in vis:
                    vis.add(u)
                    st.append(u)
        return res

    def bfs(self, start):
        if start not in self.adj:
            return []
        vis, q, res = {start}, deque([start]), []
        while q:
            v = q.popleft()
            res.append(v)
            for u in self.adj[v]:
                if u not in vis:
                    vis.add(u)
                    q.append(u)
        return res

    def has_cycle(self):
        if self.has_loops() or self.has_parallel_edges():
            return True
        vis = set()

        def go(v, parent):
            vis.add(v)
            for u in self.adj[v]:
                if u not in vis:
                    if go(u, v):
                        return True
                elif u != parent:
                    return True
            return False

        for v in self.adj:
            if v not in vis and go(v, None):
                return True
        return False


# ---------- Задание 2 ----------
def adj_list_to_matrix(adj):
    verts = list(adj)
    pos = {v: i for i, v in enumerate(verts)}
    m = [[0] * len(verts) for _ in verts]
    for a in verts:
        for b in adj[a]:
            m[pos[a]][pos[b]] = 1
    return verts, m


def matrix_to_adj_list(verts, matrix):
    adj = {v: [] for v in verts}
    for i, a in enumerate(verts):
        for j, b in enumerate(verts):
            if matrix[i][j] != 0:
                adj[a].append(b)
    return adj


# ---------- Задание 3 ----------
class WeightedUndirectedGraph:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, v):
        self.adj.setdefault(v, [])

    def add_edge(self, a, b, w):
        self.add_vertex(a)
        self.add_vertex(b)
        self.adj[a].append((b, w))
        self.adj[b].append((a, w))

    def read_from_file(self, name):
        self.adj = {}
        with open(name, 'r', encoding='utf-8') as f:
            for line in f:
                p = line.split()
                if not p:
                    continue
                if len(p) == 1:
                    self.add_vertex(p[0])
                elif len(p) >= 3:
                    self.add_edge(p[0], p[1], float(p[2]))

    def write_to_file(self, name):
        with open(name, 'w', encoding='utf-8') as f:
            for v in self.adj:
                f.write(f'{v}\n')
            seen = Counter()
            for a in self.adj:
                for b, w in self.adj[a]:
                    key = tuple(sorted((a, b))) + (w,)
                    seen[key] += 1
            for (a, b, w), k in seen.items():
                for _ in range(k // 2):
                    f.write(f'{a} {b} {w}\n')

    def degree(self, v):
        return len(self.adj.get(v, []))

    def is_adjacent(self, a, b):
        return any(x == b for x, _ in self.adj.get(a, []))

    def has_loops(self):
        return any(any(x == v for x, _ in self.adj[v]) for v in self.adj)

    def has_parallel_edges(self):
        for v in self.adj:
            c = Counter(x for x, _ in self.adj[v])
            if any(k > 1 for k in c.values()):
                return True
        return False

    def has_cycle(self):
        if self.has_loops() or self.has_parallel_edges():
            return True
        vis = set()

        def go(v, parent):
            vis.add(v)
            for u, _ in self.adj[v]:
                if u not in vis:
                    if go(u, v):
                        return True
                elif u != parent:
                    return True
            return False

        for v in self.adj:
            if v not in vis and go(v, None):
                return True
        return False


# ---------- Задание 4 ----------
class DirectedGraph:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, v):
        self.adj.setdefault(v, [])

    def add_edge(self, a, b):
        self.add_vertex(a)
        self.add_vertex(b)
        self.adj[a].append(b)

    def read_from_file(self, name):
        self.adj = {}
        with open(name, 'r', encoding='utf-8') as f:
            for line in f:
                p = line.split()
                if not p:
                    continue
                if len(p) == 1:
                    self.add_vertex(p[0])
                elif len(p) >= 2:
                    self.add_edge(p[0], p[1])

    def write_to_file(self, name):
        with open(name, 'w', encoding='utf-8') as f:
            for v in self.adj:
                f.write(f'{v}\n')
            for a in self.adj:
                for b in self.adj[a]:
                    f.write(f'{a} {b}\n')

    def out_degree(self, v):
        return len(self.adj.get(v, []))

    def in_degree(self, v):
        return sum(x == v for a in self.adj for x in self.adj[a])

    def is_adjacent(self, a, b):
        return b in self.adj.get(a, [])

    def has_loops(self):
        return any(v in self.adj[v] for v in self.adj)

    def has_parallel_edges(self):
        return any(any(c > 1 for c in Counter(self.adj[v]).values()) for v in self.adj)

    def dfs(self, start):
        if start not in self.adj:
            return []
        vis, st, res = {start}, [start], []
        while st:
            v = st.pop()
            res.append(v)
            for u in reversed(self.adj[v]):
                if u not in vis:
                    vis.add(u)
                    st.append(u)
        return res

    def bfs(self, start):
        if start not in self.adj:
            return []
        vis, q, res = {start}, deque([start]), []
        while q:
            v = q.popleft()
            res.append(v)
            for u in self.adj[v]:
                if u not in vis:
                    vis.add(u)
                    q.append(u)
        return res

    def has_cycle(self):
        color = {}

        def go(v):
            color[v] = 1
            for u in self.adj[v]:
                if color.get(u, 0) == 1:
                    return True
                if color.get(u, 0) == 0 and go(u):
                    return True
            color[v] = 2
            return False

        for v in self.adj:
            if color.get(v, 0) == 0 and go(v):
                return True
        return False


# ---------- Задание 5 ----------
class WeightedDirectedGraph:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, v):
        self.adj.setdefault(v, [])

    def add_edge(self, a, b, w):
        self.add_vertex(a)
        self.add_vertex(b)
        self.adj[a].append((b, w))

    def read_from_file(self, name):
        self.adj = {}
        with open(name, 'r', encoding='utf-8') as f:
            for line in f:
                p = line.split()
                if not p:
                    continue
                if len(p) == 1:
                    self.add_vertex(p[0])
                elif len(p) >= 3:
                    self.add_edge(p[0], p[1], float(p[2]))

    def write_to_file(self, name):
        with open(name, 'w', encoding='utf-8') as f:
            for v in self.adj:
                f.write(f'{v}\n')
            for a in self.adj:
                for b, w in self.adj[a]:
                    f.write(f'{a} {b} {w}\n')

    def out_degree(self, v):
        return len(self.adj.get(v, []))

    def in_degree(self, v):
        return sum(x == v for a in self.adj for x, _ in self.adj[a])

    def is_adjacent(self, a, b):
        return any(x == b for x, _ in self.adj.get(a, []))

    def has_loops(self):
        return any(any(x == v for x, _ in self.adj[v]) for v in self.adj)

    def has_parallel_edges(self):
        for v in self.adj:
            c = Counter(x for x, _ in self.adj[v])
            if any(k > 1 for k in c.values()):
                return True
        return False


# ---------- Задание 6 ----------
def dfs_undirected(graph, start):
    return graph.dfs(start)


def bfs_undirected(graph, start):
    return graph.bfs(start)


def dfs_directed(graph, start):
    return graph.dfs(start)


def bfs_directed(graph, start):
    return graph.bfs(start)


# ---------- Задание 7 ----------
def has_cycle(graph):
    return graph.has_cycle()


# ---------- Задание 8 ----------
def kahn_topological_sort(graph):
    indeg = {v: 0 for v in graph.adj}
    for v in graph.adj:
        for u in graph.adj[v]:
            indeg[u] += 1
    q = deque([v for v in indeg if indeg[v] == 0])
    res = []
    while q:
        v = q.popleft()
        res.append(v)
        for u in graph.adj[v]:
            indeg[u] -= 1
            if indeg[u] == 0:
                q.append(u)
    return res if len(res) == len(graph.adj) else None


# ---------- Задание 9 ----------
def dfs_topological_sort(graph):
    color = {}
    res = []

    def go(v):
        color[v] = 1
        for u in graph.adj[v]:
            if color.get(u, 0) == 1:
                return False
            if color.get(u, 0) == 0 and not go(u):
                return False
        color[v] = 2
        res.append(v)
        return True

    for v in graph.adj:
        if color.get(v, 0) == 0 and not go(v):
            return None
    return res[::-1]


# ---------- Задание 10 ----------
def greedy_coloring(graph):
    colors = {}
    for v in graph.adj:
        used = {colors[u] for u in graph.adj[v] if u in colors}
        c = 0
        while c in used:
            c += 1
        colors[v] = c
    return colors


if __name__ == '__main__':
    g = UndirectedGraph()
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'A')
    print('Undirected DFS:', g.dfs('A'))
    print('Undirected BFS:', g.bfs('A'))
    print('Has cycle:', g.has_cycle())
    print('Coloring:', greedy_coloring(g))

    d = DirectedGraph()
    d.add_edge('1', '3')
    d.add_edge('2', '3')
    d.add_edge('3', '4')
    d.add_edge('3', '5')
    print('Directed DFS:', d.dfs('1'))
    print('Directed BFS:', d.bfs('1'))
    print('Kahn:', kahn_topological_sort(d))
    print('Topo DFS:', dfs_topological_sort(d))
