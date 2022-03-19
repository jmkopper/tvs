from collections import Counter

NNODES = 4
SCALE_FACTOR = 1.1

"""
NNODES is the number of nodes in the graph
SCALE_FACTOR is the amount by which the algorithm will allow itself to miss the target distance. A value of 1.x
corresponds to x%. For example, if SCALE_FACTOR = 1.5 and target distance is 10, the algorithm will find routes
with distance between 5 and 15 (inclusive.)
"""

adj = [[0, 6, 3.2, 0], [6, 0, 2.5, 2.5], [3.2, 2.5, 0, 2.2], [0, 2.5, 2.2, 0]]
eng = [[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]]

if len(adj) != NNODES:
    print('WARNING: adjacency matrix has length ', len(adj), ' but ', NNODES, 'nodes were expected.')
if len(eng) != NNODES:
    print('WARNING: energy matrix has length ', len(eng), ' but ', NNODES, 'nodes were expected.')


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
        distance += getDist(p[i], p[i + 1])
        energy += getEnergy(p[i], p[i + 1])
    c = Counter(path)
    for x in c:
        redundancy += c[x] - 1
    return distance, energy, redundancy


def totalScore(path: list, target_d: float, target_e: float) -> float:
    d, e, r = getPathScores(path)
    return r*(d / target_d + e / target_e)


# Main algorithm: Target Value Search D(FS)
def TVSD(n: int, end: int, target_dist: float, cur_path: list = [], cur_dist: float = 0):
    if not cur_path:
        cur_path = [n]
    paths = []
    neighbors = getNeighbors(n)
    if abs(cur_dist - target_dist) <= (SCALE_FACTOR - 1) * target_dist and n == end:
        paths.append(cur_path)
    for x in neighbors:
        d = getDist(n, x)
        if d + cur_dist <= SCALE_FACTOR * target_dist:
            p = TVSD(x, end, target_dist, cur_path + [x], d + cur_dist)
            if p:
                paths += p

    return paths if paths else None


###### Test operations
target = 20
target_energy = 8
scores = []
for p in TVSD(0, 0, target):
    d, e, r = getPathScores(p)
    t = totalScore(p, target, target_energy)
    dscore = abs(d - target) / target
    escore = abs(e - target_energy) / target_energy
    scores.append((round(t, 2), round(dscore, 2), round(escore, 2), round(d, 2), p, r))

for y in sorted(scores):
    print(y)

### Next thing to implement: target energy should be optional
### Also want weights for target energy, target dist, redundancy.
### Also reconsider the formula score = redun * (%error dist + %error energy)
