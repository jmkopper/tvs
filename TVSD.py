from collections import Counter
import heapq

NNODES = 10
SCALE_FACTOR = 1.1
MAX_REDUNDANCY = 3

"""
NNODES is the number of nodes in the graph
SCALE_FACTOR is the amount by which the algorithm will allow itself to miss the target distance. A value of 1.x
corresponds to x%. For example, if SCALE_FACTOR = 1.5 and target distance is 10, the algorithm will find routes
with distance between 5 and 15 (inclusive.)
"""

# Galbraith gap data
# adj = [[0, 6, 3.2, 0], [6, 0, 2.5, 2.5], [3.2, 2.5, 0, 2.2], [0, 2.5, 2.2, 0]]
# eng = [[0, 0.05, 0.03, 0], [0, 0, 0, 0], [0, 0.04, 0, 0.03], [0, 0, 0.04, 0]]

adj = [[0, 1.7, 0, 0.25, 0, 0, 0, 0, 2.7, 0],
       [1.7, 0, 1.5, 0, 0, 0, 0, 0, 0, 1],
       [0, 1.5, 0, 1.1, 0, 0, 0, 0, 0, 1.2],
       [0.25, 0, 1.1, 0, 0.75, 0, 0, 0, 0, 0],
       [0, 0, 0, 0.75, 0, 2.7, 0, 0, 0, 0],
       [0, 0, 0, 0, 2.7, 0, 3.7, 0, 0, 0],
       [0, 0, 0, 0, 0, 3.7, 0, 0.8, 0, 0],
       [0, 0, 0, 0, 0, 0, 0.8, 0, 2.7, 0],
       [2.7, 0, 0, 0, 0, 0, 0, 2.7, 0, 0],
       [0, 1, 1.2, 0, 0, 0, 0, 0, 0, 0]
       ]

eng = [[0, 0, 0, 0, 0, 0, 0, 0, 0.03, 0],
       [0, 0, 0.02, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0.03, 0, 0.01, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0.06, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0.02, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0.04, 0.05, 0, 0, 0, 0, 0, 0, 0]
       ]

if len(adj) != NNODES:
    print('WARNING: adjacency matrix has length ', len(adj), ' but ', NNODES, 'nodes were expected.')
if len(eng) != NNODES:
    print('WARNING: energy matrix has length ', len(eng), ' but ', NNODES, 'nodes were expected.')

for l in adj:
    if len(l) != NNODES:
        print('WARNING: adj matrix row ', l, ' has length ', len(l))

for l in eng:
    if len(l) != NNODES:
        print('WARNING: eng matrix row ', l, ' has length ', len(l))


def getNeighbors(n: int) -> list:
    return [i for i, x in enumerate(adj[n]) if x > 0]


def getDist(u: int, v: int) -> float:
    d = adj[u][v]
    return d if d != 0 else float('inf')


def getEnergy(u: int, v: int):
    return eng[u][v]


def getPathScores(path: list) -> tuple[float, float, int]:
    distance, energy, redundancy = 0, 0, 0
    for i in range(len(path) - 1):
        distance += getDist(path[i], path[i + 1])
        energy += getEnergy(path[i], path[i + 1]) * distance
    c = Counter(path)
    for x in c:
        redundancy += c[x] - 1
    return distance, energy, redundancy


def totalScore(path: list, target_d: float) -> float:
    d, e, r = getPathScores(path)
    return (2 * r / NNODES) * (d / target_d) * (1 + e)


# Main algorithm: Target Value Search D(FS)
def TVSD(n: int, end: int, target_dist: float, cur_path: list = [], cur_dist: float = 0):
    path_heap = []
    if not cur_path:
        cur_path = [n]
    if abs(cur_dist - target_dist) <= (SCALE_FACTOR - 1) * target_dist and n == end:
        path_heap = [(totalScore(cur_path, target_dist), cur_path, *getPathScores(cur_path))]
    neighbors = getNeighbors(n)
    for x in neighbors:
        d = getDist(n, x)
        if d + cur_dist <= SCALE_FACTOR * target_dist and cur_path.count(x) < MAX_REDUNDANCY:
            p = TVSD(x, end, target_dist, cur_path + [x], d + cur_dist)
            if p:
                path_heap = list(heapq.merge(p, path_heap, key=lambda x: x[0]))
    return path_heap if path_heap else None


###### Test operations
target = 17
heap = TVSD(0, 0, target)

for i in range(5):
    print(heapq.heappop(heap))

### Next thing to implement: target energy should be optional
### Also want weights for target energy, target dist, redundancy.
### Also reconsider the formula score = redun * (%error dist + %error energy)
