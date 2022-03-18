import numpy as np
import heapq

NNODES = 4
SCALE_FACTOR = 1.0

adj = np.array([[0, 1, 3, 8], [1, 0, 2, 9], [0, 0, 0, 1], [0, 0, 0, 0]])
adj_T = np.transpose(adj)


def getNeighbors(n: int) -> list:
    return [i for i, x in enumerate(adj[n]) if x > 0]


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


def TVSD(start, end, target: int):
    target *= SCALE_FACTOR
    best, best_ind = float('inf'), -1
    g_score = Dijkstra(start)
    open_set = [start]
    while open_set:
        for v in open_set:
            if g_score[v] <= target:
                delta = target - g_score[v]
                if delta < best:
                    best, best_ind = delta, v
        open_set = getNeighbors(best_ind)

    return best, best_ind

print(TVSD(0, 1, 10))

"""
Current status: TVSD finds a path less than target and it has nothing to do with the end node
"""