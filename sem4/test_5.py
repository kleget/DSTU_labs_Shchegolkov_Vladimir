from heapq import heappush, heappop

class Graph:
    def __init__(self):
        self.g = {}

    def add_vertex(self, v):
        if v not in self.g:
            self.g[v] = []

    def add_edge(self, a, b, time, fuel, undirected=False):
        self.add_vertex(a)
        self.add_vertex(b)
        self.g[a].append((b, time, fuel))
        if undirected:
            self.g[b].append((a, time, fuel))

    def shortest_by_sum(self, start, end):
        dist = {v: float("inf") for v in self.g}
        prev = {v: None for v in self.g}
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            d, v = heappop(pq)
            if d > dist[v]:
                continue

            for to, t, f in self.g[v]:
                nd = d + t + f
                if nd < dist[to]:
                    dist[to] = nd
                    prev[to] = (v, t, f)
                    heappush(pq, (nd, to))

        if dist[end] == float("inf"):
            return None

        path = []
        total_time = 0
        total_fuel = 0
        cur = end

        while cur is not None:
            path.append(cur)
            p = prev[cur]
            if p is not None:
                total_time += p[1]
                total_fuel += p[2]
                cur = p[0]
            else:
                cur = None

        path.reverse()
        return path, total_time, total_fuel, dist[end]


g = Graph()
g.add_edge("A", "B", 4, 7)
g.add_edge("A", "C", 2, 10)
g.add_edge("B", "D", 3, 4)
g.add_edge("C", "D", 5, 2)
g.add_edge("A", "D", 10, 3)
g.add_edge("B", "C", 1, 1)

ans = g.shortest_by_sum("A", "D")
print(ans)