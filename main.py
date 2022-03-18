import heapq

NNODES = 4

adj = [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]


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

    return dist, prev

