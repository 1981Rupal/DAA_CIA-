import random, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def gen_points(n=12, seed=42, width=800, height=600):
    rnd = random.Random(seed)
    return [(rnd.uniform(0,width), rnd.uniform(0,height)) for _ in range(n)]

def euclidean_distances(points):
    n = len(points)
    d = [[0.0]*n for _ in range(n)]
    for i in range(n):
        xi, yi = points[i]
        for j in range(n):
            if i==j: continue
            xj, yj = points[j]
            d[i][j] = math.hypot(xi-xj, yi-yj)
    return d

def length_of_route(route, dist):
    total = 0.0
    n = len(route)
    for i in range(n):
        total += dist[route[i]][route[(i+1)%n]]
    return total

def plot_route(points, route, title="TSP Route", save_path=None):
    xs = [points[i][0] for i in route] + [points[route[0]][0]]
    ys = [points[i][1] for i in route] + [points[route[0]][1]]
    plt.figure(figsize=(8,5))
    plt.scatter([p[0] for p in points], [p[1] for p in points])
    plt.plot(xs, ys, marker='o')
    for idx,(x,y) in enumerate(points):
        plt.text(x,y,str(idx))
    plt.title(title)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150); plt.close()
    else:
        return plt.gcf()