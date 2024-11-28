def find_reachable_nodes(graph):
    reachable_dict = {}

    def dfs(node, visited):
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor, visited)

    for start_node in graph:
        visited = set()
        dfs(start_node, visited)
        reachable_dict[start_node] = list(visited)

    return reachable_dict

def get_graph():
    graph = {}
    i = int(input("сколько вершин в графе?: "))
    for u in range(i):
        a = input("Введите вершину графа: ")
        b = input(f"Введите все вершины через пробел, в которые от  вершины {a} идет направленная дуга: ")
        b = list(map(str, b.split(' ')))
        graph[str(a)] = b
    return graph


graph = get_graph()
reachable_nodes = find_reachable_nodes(graph)

Tg = len(reachable_nodes) * [len(reachable_nodes) * [0]]
Tg = [list(sublist) for sublist in Tg]

#строим матрицу Tg
for i in reachable_nodes:
    for j in reachable_nodes[i]:
        if (str(j) in reachable_nodes[i]): # and (str(i) in reachable_nodes[j]):
            Tg[int(i)-1][int(j)-1] = 1
        else:
            Tg[int(i)-1][int(j)-1] = 0

#строим матрицу Sg
Sg = len(reachable_nodes) * [len(reachable_nodes) * [0]]
Sg = [list(sublist) for sublist in Sg]
for i in reachable_nodes:
    for j in reachable_nodes[i]:
        if Tg[int(i)-1][int(j)-1]==1 and Tg[int(j)-1][int(i)-1]==1:
            Sg[int(i)-1][int(j)-1] = 1
        else:
            Sg[int(i)-1][int(j)-1] = 0

print('Tg')
for x in Tg:
    print(x)

print('Sg')
for x in Sg:
    print(x)

