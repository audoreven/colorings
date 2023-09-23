from collections import defaultdict
import random
import matplotlib.pyplot as plt

n = 25
d = random.randint(1, n//2)
max_kd = 3
trials = 10
step = max_kd / 60

# plot details
mix_times = []
fixed_kds = []
curr = 1.5
while curr <= max_kd:
    fixed_kds.append(curr)
    curr += step

# generate graphs
colorsX = [-1 for i in range(2 * n)]
colorsY = [-1 for i in range(2 * n)]
graphX = defaultdict(list)
graphY = defaultdict(list)
edgesX = [[False for i in range(2 * n)] for j in range(2 * n)]
edgesY = [[False for i in range(2 * n)] for j in range(2 * n)]
permute = [i for i in range(n)]

for i in range(2 * n):
    graphX[i] = []
    graphY[i] = []

random.shuffle(permute)
for i in permute:
    for j in range(d):
        v = random.randint(n, 2 * n - 1)
        if not edgesX[i][v] and len(graphX[v]) < d:
            edgesX[i][v] = True
            edgesX[v][i] = True
            graphX[i].append(v)
            graphX[v].append(i)
            edgesY[i][v] = True
            edgesY[v][i] = True
            graphY[i].append(v)
            graphY[v].append(i)


def is_proper(g, gc):
    global n

    for v in range(n):
        for w in g[v]:
            if gc[w] == gc[v]:
                return False

    return True


def not_same(colors_a, colors_b):
    global n

    for i in range(2 * n):
        if colors_a[i] != colors_b[i]:
            return True

    return False


# flip dynamics
def get_cluster(g, gc, v, c):  # run bfs from v
    vis = [False for i in range(len(gc))]
    cluster = [v]
    q = [v]
    vis[v] = True
    while len(q) > 0:
        cur = q.pop()

        for w in g[cur]:
            if not vis[w]:
                if gc[w] == c and gc[cur] == gc[v]:
                    q.append(w)
                    cluster.append(w)
                    vis[w] = True
                elif gc[w] == gc[v] and gc[cur] == c:
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


def flip(graph, colors, k):
    global n

    # choose random vertex
    v = random.randint(0, 2 * n - 1)

    # choose random color
    c = random.randint(1, k)
    while c == colors[v]:
        c = random.randint(1, k)

    # find flip cluster
    cluster = get_cluster(graph, colors, v, c)

    # decide flip with probability whatever
    flip_chance = get_flip_chance(len(cluster))
    p = random.random()
    if p > flip_chance:     # do not flip
        return graph, colors

    # flip cluster
    for w in cluster:
        if colors[w] == colors[v]:
            colors[w] = c
            for b in graph[w]:
                if colors[b] == c:
                    colors[b] = recolor(b, graph, colors, k)
        elif colors[w] == v:
            colors[w] = colors[v]
            for b in graph[w]:
                if colors[b] == colors[v]:
                    colors[b] = recolor(b, graph, colors, k)

    return graph, colors


def flip_cluster(cluster, graph, colors, c1, c2, k):
    for v in cluster:
        if colors[v] == c1:
            colors[v] = c2
            for b in graph[v]:
                if colors[b] == c2:
                    colors[b] = recolor(b, graph, colors, k)
        elif colors[v] == c2:
            colors[v] = c1
            for b in graph[v]:
                if colors[b] == c1:
                    colors[b] = recolor(b, graph, colors, k)

    return graph, colors


def coupled_flip(graph_a, graph_b, colors_a, colors_b, k):
    global n

    # choose random vertex
    v = random.randint(0, 2 * n - 1)

    # choose random color
    c = random.randint(1, k)

    # find flip clusters
    cluster_a = get_cluster(graph_a, colors_a, v, c) if colors_a[v] != c else [v]
    cluster_b = get_cluster(graph_b, colors_b, v, c) if colors_b[v] != c else [v]

    other_clusters_a = []
    other_clusters_b = []
    A, B = 0, 0
    i_max, j_max, a_ind, b_ind = 0, 0, 0, 0
    for w in graph_a[v]:
        if colors_a[w] == c and colors_b[w] == c:
            new_a = get_cluster(graph_b, colors_b, w, colors_a[v])
            new_b = get_cluster(graph_a, colors_a, w, colors_b[v])
            if len(new_a) > i_max:
                i_max = len(new_a)
                a_ind = len(other_clusters_a)
            if len(new_b) > j_max:
                j_max = len(new_b)
                b_ind = len(other_clusters_b)
            A += len(new_a)
            B += len(new_b)
            other_clusters_a.append(new_a)
            other_clusters_b.append(new_b)

    pA, pB = get_flip_chance(A+1), get_flip_chance(B+1)

    if random.random() < pA:  # do not flip
        # flip cluster_a and max of other cluster b
        ac = colors_a[v]
        flip_cluster(cluster_a, graph_a, colors_a, c, ac, k)
        if len(other_clusters_a) > 0:
            flip_cluster(other_clusters_a[a_ind], graph_b, colors_b, c, ac, k)
        else:
            colors_b[v] = ac
            flip_cluster([v], graph_b, colors_b, c, ac, k)

    elif random.random() < pB:
        # flip cluster_b and max of other cluster a
        bc = colors_b[v]
        flip_cluster(cluster_b, graph_b, colors_b, c, bc, k)
        if len(other_clusters_b) > 0:
            flip_cluster(other_clusters_b[b_ind], graph_a, colors_a, c, bc, k)
        else:
            colors_a[v] = bc
            flip_cluster([v], graph_a, colors_a, c, bc, k)
    else:
        for i in range(len(other_clusters_a)):
            ql_a = (get_flip_chance(len(other_clusters_a[i])) - pA) if i == a_ind else get_flip_chance(
                len(other_clusters_a[i]))
            ql_b = (get_flip_chance(len(other_clusters_b[i])) - pB) if i == b_ind else get_flip_chance(
                len(other_clusters_b[i]))
            if random.random() < min(ql_a, ql_b):
                flip_cluster(other_clusters_a[i], graph_b, colors_b, c, colors_a[v], k)
                flip_cluster(other_clusters_b[i], graph_a, colors_a, c, colors_b[v], k)
            elif random.random() < ql_a - min(ql_a, ql_b):
                flip_cluster(other_clusters_a[i], graph_b, colors_b, c, colors_a[v], k)
            elif random.random() < ql_b - min(ql_a, ql_b):
                flip_cluster(other_clusters_b[i], graph_a, colors_a, c, colors_b[v], k)

    return graph_a, graph_b, colors_a, colors_b


def simulate_flip(graph_a, graph_b, kds):
    mt = []
    for kd in kds:
        # reset X and Y
        total = 0
        k = int(kd * d + 2)
        for t in range(trials):
            colors_a = [-1 for i in range(2 * n)]
            colors_b = [-1 for i in range(2 * n)]

            # flip on X
            while -1 in colors_a:
                graph_a, colors_a = flip(graph_a, colors_a, k)

            # flip on Y
            while -1 in colors_b:
                graph_b, colors_b = flip(graph_b, colors_b, k)

            # couple X and Y and record time it takes for them to mix
            while not_same(colors_a, colors_b):
                graph_a, graph_b, colors_a, colors_b = coupled_flip(graph_a, graph_b, colors_a, colors_b, k)
                total += 1

        mt.append(total / trials)
        print(f'k = {k}: K/DELTA = {k / d}, MIXING TIME = {total / trials}')

    return mt


flip_mix_times = simulate_flip(graphX, graphY, fixed_kds)

print(flip_mix_times)

# plot graphs

title = 'Flip: Vertex Coloring on K_n,n w/ Max Degree Delta'
subtitle = f'N = {n}, Delta = {d}'
plt.suptitle(title, fontsize=14)
plt.title(subtitle, fontsize=10)
plt.plot(fixed_kds, flip_mix_times, color='red')
plt.ylabel("Mixing Time")
plt.xlabel("K/Delta")
plt.axvline(x=11/6, c='black')
plt.show()
