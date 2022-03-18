import numpy as np
import heapq

NNODES = 4
SCALE_FACTOR = 1.5

adj = np.array([[0, 1, 4, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]])
adj_T = np.transpose(adj)


def getNeighbors(n: int) -> list:
    return [i for i, x in enumerate(adj[n]) if x > 0]

def getDist(u, v):
    d = adj[u][v]
    return d if d != 0 else float('inf')


def getPathLength(p):
    d = 0
    for i in range(len(p)-1):
        d += getDist(p[i], p[i+1])
    return d


def Dijkstra(start):
    dist = []
    prev = []
    for i in range(NNODES):
        dist.append(float('inf'))
        prev.append(None)
    dist[start] = 0
    heap = [(d, n) for n, d in enumerate(dist)]
    heapq.heapify(heap)

    while heap:
        u = heapq.heappop(heap)[1]
        heap_vals = [z for y, z in heap]  # Can't figure out a better way to do this

        for v in getNeighbors(u):
            if v in heap_vals:
                alt = dist[u] + adj[u][v]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

    return dist#, prev


def TVSD(n, end, target: int, cur_path: list = [], cur_dist: int = 0):
    if not cur_path:
        cur_path = [n]
    paths = []
    neighbors = getNeighbors(n)
    if abs(cur_dist - target) < (SCALE_FACTOR-1) * target and n == end:
        paths.append(cur_path)
    for x in neighbors:
        d = getDist(n, x)
        if d + cur_dist <= SCALE_FACTOR * target:
            p = TVSD(x, end, target, cur_path + [x], d + cur_dist)
            if p:
                paths += p

    return paths if paths else None

for x in TVSD(0,1,10):
    print(getPathLength(x), ": ", x)