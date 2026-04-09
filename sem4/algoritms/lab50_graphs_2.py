from collections import deque, Counter
import os


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


def print_block(title):
    print('\n' + '=' * 20, title, '=' * 20)


def print_matrix(verts, matrix):
    print('  ', *verts)
    for i, row in enumerate(matrix):
        print(verts[i], *row)


def make_demo_files(base):
    with open(os.path.join(base, 'task1_in.txt'), 'w', encoding='utf-8') as f:
        f.write('A\nB\nC\nD\nA B\nB C\nC A\nC D\n')

    with open(os.path.join(base, 'task3_in.txt'), 'w', encoding='utf-8') as f:
        f.write('A\nB\nC\nD\nA B 2\nB C 3\nC A 4\nC D 5\n')

    with open(os.path.join(base, 'task4_in.txt'), 'w', encoding='utf-8') as f:
        f.write('1\n2\n3\n4\n5\n1 2\n1 3\n2 4\n3 4\n4 5\n')

    with open(os.path.join(base, 'task5_in.txt'), 'w', encoding='utf-8') as f:
        f.write('X\nY\nZ\nX Y 1\nX Z 2\nY Z 3\n')


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    make_demo_files(base)

    # 1
    print_block('ЗАДАНИЕ 1')
    g1 = UndirectedGraph()
    g1.read_from_file(os.path.join(base, 'task1_in.txt'))
    g1.write_to_file(os.path.join(base, 'task1_out.txt'))
    print('Граф:', g1.adj)
    print('Степень C:', g1.degree('C'))
    print('A и B смежны:', g1.is_adjacent('A', 'B'))
    print('Есть петли:', g1.has_loops())
    print('Есть параллельные ребра:', g1.has_parallel_edges())
    print('Есть цикл:', g1.has_cycle())
    print('Файл записи: task1_out.txt')

    # 2
    print_block('ЗАДАНИЕ 2')
    verts, matrix = adj_list_to_matrix(g1.adj)
    print('Матрица смежности:')
    print_matrix(verts, matrix)
    print('Обратно в список смежности:', matrix_to_adj_list(verts, matrix))

    # 3
    print_block('ЗАДАНИЕ 3')
    g3 = WeightedUndirectedGraph()
    g3.read_from_file(os.path.join(base, 'task3_in.txt'))
    g3.write_to_file(os.path.join(base, 'task3_out.txt'))
    print('Граф:', g3.adj)
    print('Степень C:', g3.degree('C'))
    print('A и B смежны:', g3.is_adjacent('A', 'B'))
    print('Есть петли:', g3.has_loops())
    print('Есть параллельные ребра:', g3.has_parallel_edges())
    print('Есть цикл:', g3.has_cycle())
    print('Файл записи: task3_out.txt')

    # 4
    print_block('ЗАДАНИЕ 4')
    g4 = DirectedGraph()
    g4.read_from_file(os.path.join(base, 'task4_in.txt'))
    g4.write_to_file(os.path.join(base, 'task4_out.txt'))
    print('Граф:', g4.adj)
    print('DFS от 1:', g4.dfs('1'))
    print('BFS от 1:', g4.bfs('1'))
    print('Полустепень захода 4:', g4.in_degree('4'))
    print('Полустепень исхода 1:', g4.out_degree('1'))
    print('1 и 3 смежны:', g4.is_adjacent('1', '3'))
    print('Есть петли:', g4.has_loops())
    print('Есть параллельные ребра:', g4.has_parallel_edges())
    print('Есть цикл:', g4.has_cycle())
    print('Файл записи: task4_out.txt')

    # 5
    print_block('ЗАДАНИЕ 5')
    g5 = WeightedDirectedGraph()
    g5.read_from_file(os.path.join(base, 'task5_in.txt'))
    g5.write_to_file(os.path.join(base, 'task5_out.txt'))
    print('Граф:', g5.adj)
    print('Полустепень захода Z:', g5.in_degree('Z'))
    print('Полустепень исхода X:', g5.out_degree('X'))
    print('X и Y смежны:', g5.is_adjacent('X', 'Y'))
    print('Есть петли:', g5.has_loops())
    print('Есть параллельные ребра:', g5.has_parallel_edges())
    print('Файл записи: task5_out.txt')

    # 6
    print_block('ЗАДАНИЕ 6')
    print('DFS неориентированного графа:', dfs_undirected(g1, 'A'))
    print('BFS неориентированного графа:', bfs_undirected(g1, 'A'))
    print('DFS ориентированного графа:', dfs_directed(g4, '1'))
    print('BFS ориентированного графа:', bfs_directed(g4, '1'))

    # 7
    print_block('ЗАДАНИЕ 7')
    cycle_u = UndirectedGraph()
    cycle_u.add_edge('A', 'B')
    cycle_u.add_edge('B', 'C')
    cycle_u.add_edge('C', 'A')
    cycle_d = DirectedGraph()
    cycle_d.add_edge('1', '2')
    cycle_d.add_edge('2', '3')
    cycle_d.add_edge('3', '1')
    print('Цикл в неориентированном графе:', has_cycle(cycle_u))
    print('Цикл в ориентированном графе:', has_cycle(cycle_d))

    # 8
    print_block('ЗАДАНИЕ 8')
    dag = DirectedGraph()
    dag.add_edge('1', '3')
    dag.add_edge('2', '3')
    dag.add_edge('3', '4')
    dag.add_edge('3', '5')
    print('Топологическая сортировка Кана:', kahn_topological_sort(dag))

    # 9
    print_block('ЗАДАНИЕ 9')
    print('Топологическая сортировка через DFS:', dfs_topological_sort(dag))

    # 10
    print_block('ЗАДАНИЕ 10')
    color_graph = UndirectedGraph()
    color_graph.add_edge('1', '5')
    color_graph.add_edge('2', '3')
    color_graph.add_edge('2', '4')
    color_graph.add_edge('3', '5')
    color_graph.add_edge('4', '5')
    print('Граф:', color_graph.adj)
    print('Раскраска:', greedy_coloring(color_graph))
