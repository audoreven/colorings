from collections import defaultdict
import random
import matplotlib.pyplot as plt
import math

n = 5000
d = random.randint(2, n//2)
max_kd = 3.5
trials = 3
step = max_kd / 60

# plot details
mix_times = []
fixed_kds = []
curr = 1.2
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


def not_same(colors_a, colors_b):
    global n

    for i in range(2 * n):
        if colors_a[i] != colors_b[i]:
            return True

    return False


# glauber dynamics
def glauber(graph, colors, k):
    global n

    # choose random vertex
    v = random.randint(0, 2 * n - 1)

    # choose random color
    c = random.randint(1, k)

    # can i color? yes no
    for w in graph[v]:
        if colors[w] == c:
            return graph, colors

    colors[v] = c
    return graph, colors


def coupled_glauber(graph_a, graph_b, colors_a, colors_b, k):
    global n

    # choose random vertex
    v = random.randint(0, 2 * n - 1)

    # choose random color
    c = random.randint(1, k)

    # can i color? yes no
    for w in graph_a[v]:
        if colors_a[w] == c:
            for m in graph_b[v]:
                if colors_b[m] == c:
                    return graph_a, graph_b, colors_a, colors_b

    colors_a[v] = c
    colors_b[v] = c
    return graph_a, graph_b, colors_a, colors_b


def simulate_glauber(graph_a, graph_b, kds):
    mt = []
    for kd in kds:
        # reset X and Y
        total = 0
        k = int(kd * d)
        for t in range(trials):
            colors_a = [-1 for i in range(2 * n)]
            colors_b = [-1 for i in range(2 * n)]

            # glauber on X
            while -1 in colors_a:
                graph_a, colors_a = glauber(graph_a, colors_a, k)

            # glauber on Y
            while -1 in colors_b:
                graph_b, colors_b = glauber(graph_b, colors_b, k)

            # couple X and Y and record time it takes for them to mix
            while not_same(colors_a, colors_b):
                graph_a, graph_b, colors_a, colors_b = coupled_glauber(graph_a, graph_b, colors_a, colors_b, k)
                total += 1

        mt.append(total / trials)
        print(f'k = {k}: K/DELTA = {k / d}, MIXING TIME = {total / trials}')

    return mt


glauber_mix_times = simulate_glauber(graphX, graphY, fixed_kds)

print(glauber_mix_times)

# plot graphs

title = 'Glauber: Vertex Coloring on Bipartite Graph w/ Max Degree Delta'
subtitle = f'N = {n}, Delta = {d}'
plt.suptitle(title, fontsize=14)
plt.title(subtitle, fontsize=10)
plt.plot(fixed_kds, glauber_mix_times)
plt.ylabel("Mixing Time")
plt.xlabel("K/Delta")
plt.axvline(x=2, c='red')
plt.axhline(y=(2*n)*math.log(2*n, 2), c='black')
plt.show()
