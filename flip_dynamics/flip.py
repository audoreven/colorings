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

def done(gc):
    for i in gc:
        if i == -1:
            return False

    return True


def is_proper(g, gc):
    global n

    for v in range(n):
        for w in g[v]:
            if gc[w] == gc[v]:
                return False

    return True



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


def get_cluster(g, gc, v, c):  # run bfs from v
    vis = [False for i in range(len(gc))]
    cluster = [v]
    q = [v]
    vis[v] = True
    while len(q) > 0:
        curr = q.pop()

        for w in g[curr]:
            if not vis[w]:
                if gc[w] == c and gc[curr] == gc[v]:
                    q.append(w)
                    cluster.append(w)
                    vis[w] = True
                elif gc[w] == gc[v] and gc[curr] == c:
                    q.append(w)
                    cluster.append(w)
                    vis[w] = True

    return cluster


def get_flip_chance(s):
    if s == 1:
        return 1
    elif s == 2:
        return 13 / 42
    elif s == 3:
        return 1 / 6
    elif s == 4:
        return 2 / 21
    elif s == 5:
        return 1 / 21
    elif s == 6:
        return 1 / 84
    return 0


def recolor(v, g, gc, k):
    appear = [False for i in range(k+1)]
    appear[0] = True
    for w in g[v]:
        appear[gc[w]] = True

    for i in range(k):
        if not appear[i]:
            return i

    return -1


def flip(graph_a, colors_a, k):
    global n

    # choose random vertex
    v = random.randint(0, 2 * n - 1)

    # choose random color
    c = random.randint(1, k)
    while c == colors_a[v]:
        c = random.randint(1, k)

    # find flip cluster
    cluster = get_cluster(graph_a, colors_a, v, c)

    # decide flip with probability whatever
    flip_chance = get_flip_chance(len(cluster))
    p = random.random()
    if p > flip_chance:     # do not flip
        return graph_a, colors_a

    # flip cluster
    for w in cluster:
        if colors_a[w] == colors_a[v]:
            colors_a[w] = c
            for b in graph_a[w]:
                if colors_a[b] == c:
                    colors_a[b] = recolor(b, graph_a, colors_a, k)
        elif colors_a[w] == v:
            colors_a[w] = colors_a[v]
            for b in graph_a[w]:
                if colors_a[b] == colors_a[v]:
                    colors_a[b] = recolor(b, graph_a, colors_a, k)

    return graph_a, colors_a


# while not done(graph_colors) or not is_proper(graph, graph_colors):
#     count += 1
#     flip(graph, graph_colors, k)
#     print(graph_colors)
#     print(count)
#
# print(graph)

# while count > 0 and is_proper(graph, graph_colors):
#     count -= 1
#     flip(graph, graph_colors, k)
#     print(graph_colors)
#     print(count)
#
# print(graph)
# print(is_proper(graph, graph_colors))


for i in range(25):
    graph_colors = [-1 for i in range(2 * n)]
    while -1 in graph_colors:
        count += 1
        flip(graph, graph_colors, k)

print(count/25)
