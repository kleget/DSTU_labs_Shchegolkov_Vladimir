graph = {1: [2,5],
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


def search_all_vertices(ver):
    if (len(graph[ver]) == 1) and (graph[ver] in graph_full[ver]):
        return graph[ver]
    else:
    #     return graph[ver]
    # elif graph[ver] != []:
        for x in graph[ver]:
            a = search_all_vertices(x)
            graph_full[x].append(a[0])


    #         print(graph_full)
    #     print(graph_full)
    # print(graph_full)


search_all_vertices(1)
print(graph_full)