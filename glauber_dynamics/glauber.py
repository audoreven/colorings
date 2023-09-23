from collections import defaultdict
import random

n = 100
d = 5
k = 6
count = 0

# generate graphs
graph_colors = [-1 for i in range(2 * n)]
graph = defaultdict(list)
edges = [[False for i in range(2 * n)] for j in range(2 * n)]
permute = [i for i in range(n)]


for i in range(2 * n):
    graph[i] = []

random.shuffle(permute)
for i in permute:
    for j in range(d):
        v = random.randint(n, 2 * n - 1)
        if not edges[i][v] and len(graph[v]) < d:
            edges[i][v] = True
            edges[v][i] = True
            graph[i].append(v)
            graph[v].append(i)

def glauber(g, colors, k):
    global n

    # choose random vertex
    v = random.randint(0, 2 * n - 1)

    # choose random color
    c = random.randint(1, k)

    # can i color? yes no
    for w in g[v]:
        if colors[w] == c:
            return g, colors

    colors[v] = c
    return g, colors


for i in range(25):
    graph_colors = [-1 for i in range(2 * n)]
    while -1 in graph_colors:
        count += 1
        glauber(graph, graph_colors, k)

print(count/25)