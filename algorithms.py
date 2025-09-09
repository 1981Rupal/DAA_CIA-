import math, itertools, heapq, random

def route_length(route, dist):
    total = 0.0
    n = len(route)
    for i in range(n):
        total += dist[route[i]][route[(i+1)%n]]
    return total

# Greedy: Nearest Neighbor
def greedy_nearest_neighbor(dist, start=0):
    n = len(dist)
    unvisited = set(range(n))
    route = [start]
    unvisited.remove(start)
    cur = start
    while unvisited:
        nxt = min(unvisited, key=lambda j: dist[cur][j])
        route.append(nxt)
        unvisited.remove(nxt)
        cur = nxt
    return route

# Held-Karp DP (exact)
def held_karp(dist):
    n = len(dist)
    C = {}
    for k in range(1, n):
        C[(1 | (1 << k), k)] = (dist[0][k], 0)
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 1
            for b in subset:
                bits |= 1 << b
            for j in subset:
                prev_bits = bits & ~(1 << j)
                best = None
                prev = None
                for k in subset:
                    if k == j: continue
                    if (prev_bits, k) in C:
                        cost = C[(prev_bits, k)][0] + dist[k][j]
                        if best is None or cost < best:
                            best = cost; prev = k
                if best is not None:
                    C[(bits, j)] = (best, prev)
    bits = (1 << n) - 1
    best = None; parent = None
    for j in range(1, n):
        if (bits, j) in C:
            cost = C[(bits, j)][0] + dist[j][0]
            if best is None or cost < best:
                best = cost; parent = j
    route = [0]
    if parent is None:
        return list(range(n))
    cur = parent
    mask = bits
    stack = []
    while cur != 0:
        stack.append(cur)
        next_prev = C[(mask, cur)][1]
        mask &= ~(1 << cur)
        cur = next_prev
    stack.reverse()
    route += stack
    return route

# Backtracking with pruning
def tsp_backtracking(dist, time_limit=None):
    n = len(dist)
    best_cost = float('inf')
    best_path = None
    start_time = None
    if time_limit is not None:
        import time
        start_time = time.time()
    visited = [False]*n
    visited[0] = True
    def dfs(path, cost):
        nonlocal best_cost, best_path
        if time_limit is not None:
            import time
            if time.time() - start_time > time_limit:
                return
        if len(path) == n:
            total = cost + dist[path[-1]][0]
            if total < best_cost:
                best_cost = total; best_path = path[:]
            return
        for nxt in range(n):
            if not visited[nxt]:
                new_cost = cost + dist[path[-1]][nxt]
                if new_cost < best_cost:
                    visited[nxt] = True
                    path.append(nxt)
                    dfs(path, new_cost)
                    path.pop()
                    visited[nxt] = False
    dfs([0], 0)
    return best_path if best_path is not None else list(range(n))

# Branch and Bound with simple lower bound (min outgoing)
def tsp_branch_and_bound(dist, time_limit=None):
    n = len(dist)
    best_cost = float('inf')
    best_path = None
    start_time = None
    if time_limit is not None:
        import time
        start_time = time.time()
    def lower_bound(path, cost, visited_set):
        lb = cost
        unvisited = [i for i in range(n) if i not in visited_set]
        for u in unvisited:
            lb += min(dist[u][v] for v in range(n) if v != u)
        return lb
    pq = []
    heapq.heappush(pq, (lower_bound([0],0,{0}), 0, [0], {0}))
    while pq:
        if time_limit is not None:
            import time
            if time.time() - start_time > time_limit:
                break
        bound, cost, path, visited_set = heapq.heappop(pq)
        if bound >= best_cost:
            continue
        if len(path) == n:
            total = cost + dist[path[-1]][0]
            if total < best_cost:
                best_cost = total; best_path = path[:]
            continue
        for nxt in range(n):
            if nxt in visited_set: continue
            new_cost = cost + dist[path[-1]][nxt]
            new_path = path + [nxt]
            new_vis = visited_set | {nxt}
            b = lower_bound(new_path, new_cost, new_vis)
            if b < best_cost:
                heapq.heappush(pq, (b, new_cost, new_path, new_vis))
    return best_path if best_path is not None else list(range(n))

# Divide and Conquer approximate (split by x)
def divide_and_conquer_tsp(points):
    idxs = list(range(len(points)))
    def recurse(indices):
        if len(indices) <= 3:
            return indices[:]
        indices.sort(key=lambda i: points[i][0])
        mid = len(indices)//2
        left = recurse(indices[:mid])
        right = recurse(indices[mid:])
        return left + right
    return recurse(idxs)