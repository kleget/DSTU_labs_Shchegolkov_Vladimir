graph = {1: [2, 5],
         2: [3],
         3: [1, 4],
         4: [5],
         5: [4]}

#нахождение всех возможных путей
graph_full = {1:[],
              2:[],
              3:[],
              4:[],
              5:[]}


def search_ones_vertices(ver):
    if len(graph[ver]) == 1:
        graph_full[ver].append(graph[ver])
        print(graph_full)
    # elif:
    #     for y in graph[ver]:
    #         search_ones_vertices(y)
    ###########
    elif len(graph[ver]) >= 2:
        for y in graph[ver]:
            search_ones_vertices(y)
        p = [graph[x][0] for x in graph[ver]]
        for o in graph[ver]:
            p.append(o)
        # p = str(p)
        graph_full[ver].append(p)

# def search_other_vertices(ver):
#     if len(graph[ver]) >= 2:
#         p = [graph[x][0] for x in graph[ver]]
#         for o in graph[ver]:
#             p.append(o)
#         # p = str(p)
#         graph_full[ver].append(p)

    #     return graph[ver]
    # elif graph[ver] != []:
    #     for x in graph[ver]:
    #         a = search_all_vertices(x)
    #         graph_full[x].append(a[0])

    #         print(graph_full)
    #     print(graph_full)
    # print(graph_full)

# for x in graph.keys():
#     search_ones_vertices(x)
#
# m = 0
# for u in graph.keys():
#     if m <= len(graph[u]): m=len(graph[u])

for j in range(3):
    for x in graph.keys():
        search_ones_vertices(x)
        # search_other_vertices(x)
    # i+=1
    # search_other_vertices(ver)


print(graph_full)