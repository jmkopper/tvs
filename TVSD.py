NNODES = 4
SCALE_FACTOR = 1.25

"""
NNODES is the number of nodes in the graph
SCALE_FACTOR is the amount by which the algorithm will allow itself to miss the target distance. A value of 1.x
corresponds to x%. For example, if SCALE_FACTOR = 1.5 and target distance is 10, the algorithm will find routes
with distance between 5 and 15 (inclusive.)
"""

adj = [[0, 6, 3.2, 0], [6, 0, 2.5, 2.5], [3.2, 2.5, 0, 2.2], [0, 2.5, 2.2, 0]]


def getNeighbors(n: int) -> list:
    return [i for i, x in enumerate(adj[n]) if x > 0]


def getDist(u, v):
    d = adj[u][v]
    return d if d != 0 else float('inf')


def getPathLength(p):
    d = 0
    for i in range(len(p) - 1):
        d += getDist(p[i], p[i + 1])
    return d


# Main algorithm: Target Value Search D(FS)
def TVSD(n, end, target: int, cur_path: list = [], cur_dist: float = 0):
    if not cur_path:
        cur_path = [n]
    paths = []
    neighbors = getNeighbors(n)
    if abs(cur_dist - target) <= (SCALE_FACTOR - 1) * target and n == end:
        paths.append(cur_path)
    for x in neighbors:
        d = getDist(n, x)
        if d + cur_dist <= SCALE_FACTOR * target:
            p = TVSD(x, end, target, cur_path + [x], d + cur_dist)
            if p:
                paths += p

    return paths if paths else None


###### Test operations
target = 10
scores = []
for p in TVSD(0, 0, target):
    d = getPathLength(p)
    score = abs(d - target) / target
    scores.append((score, d, p))

for y in sorted(scores):
    print(y)

### Next thing to implement: scoring each edge based on non-distance
### and adjusting score by dispreferring repeated visits to the same node
