from collections import Counter
import heapq
import json

"""
SCALE_FACTOR is the amount by which the algorithm will allow itself to miss the target distance. A value of 1.x
corresponds to x%. For example, if SCALE_FACTOR = 1.5 and target distance is 10, the algorithm will find routes
with distance between 5 and 15 (inclusive.)
MAX_REDUNDANCY is the maximum number of times the algorithm will visit a given node. Anything more than 4 will set my
computer on fire and is so dispreffered by the scoring algorithm that it's probably useless anyway.
"""

SCALE_FACTOR = 1.1
MAX_REDUNDANCY = 3

BASE_PATH = './'
IMPORT_FILE_NAME = 'sample.json'
EXPORT_FILE_NAME = 'output.json'

# Load from the json file
with open(BASE_PATH + IMPORT_FILE_NAME) as file:
        data = json.load(file)
route_name = data['name']
adj = data['distanceMatrix']
eng = data['energyMatrix']
start = data['start']
end = data['end']
target = data['target']
NNODES = len(adj)


# Verify the data
assert len(adj) == len(eng)

for n in adj:
    assert len(n) == NNODES

for n in eng:
    assert len(n) == NNODES


# Scrape the matrix to find neighbors of a given node
def get_neighbors(n: int) -> list:
    return [i for i, x in enumerate(adj[n]) if x > 0]


# Get the distance between two nodes
def get_dist(u: int, v: int) -> float:
    d = adj[u][v]
    return d if d != 0 else float('inf')


# Get the energy between two nodes
def get_energy(u: int, v: int) -> float:
    return eng[u][v]


# Compute the distance, energy, redundancy scores of a given path
def get_path_scores(path: list) -> tuple[float, float, int]:
    distance, energy, redundancy = 0, 0, 0
    for i in range(len(path) - 1):
        distance += get_dist(path[i], path[i + 1])
        energy += get_energy(path[i], path[i + 1]) * distance
    c = Counter(path)
    for x in c:
        redundancy += c[x] - 1
    return distance, energy, redundancy


# Compute the total score of a path
def total_score(path: list, target_d: float) -> float:
    d, e, r = get_path_scores(path)
    return (r ** 2) * (d / target_d) * (1 + e)


# Main algorithm: Target Value Search D(FS)
# Store result in a heap [score: float, path: list, distance score: float, energy score: float, redundancy score: int]
def TVSD(n: int, end: int, target_dist: float, cur_path: list = None, cur_dist: float = 0):
    path_heap = []
    if not cur_path:
        cur_path = [n]
    if abs(cur_dist - target_dist) <= (SCALE_FACTOR - 1) * target_dist and n == end:
        path_heap = [(total_score(cur_path, target_dist), cur_path, *get_path_scores(cur_path))]
    neighbors = get_neighbors(n)
    for x in neighbors:
        d = get_dist(n, x)
        if d + cur_dist <= SCALE_FACTOR * target_dist and cur_path.count(x) < MAX_REDUNDANCY:
            p = TVSD(x, end, target_dist, cur_path + [x], d + cur_dist)
            if p:
                path_heap = list(heapq.merge(p, path_heap, key=lambda x: x[0]))
    return path_heap if path_heap else None


# Run the algorithm
heap = TVSD(start, end, target)
json_dictionary = {}

for i in range(5):
    line = heapq.heappop(heap)
    current_dict = {
        'score': round(line[0],2),
        'path': line[1],
        'distance': round(line[2],2)
    }
    json_dictionary['name'] = route_name
    json_dictionary[i] = current_dict
    print(line)

json_object = json.dumps(json_dictionary, indent=4)
with open(BASE_PATH + EXPORT_FILE_NAME, 'w') as file:
    file.write(json_object)