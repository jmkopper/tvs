# tvs
Target Value Search
This project is a modified target value search algorithm for a weighted, directed (cyclic) graph.

Inputs:
- A weighted graph (represented as an adjacency matrix)
- A second set of weights ("energy" values)
- A START node
- An END node
- A TARGET distance

The code produces a list of paths from START to END while trying to simultaneously (a) keep the distance (as measured by the adjancency matrix)
as close to TARGET as possible; (b) minimize the energy (as measured by the energy matrix); (c) minimize redundancy, i.e., the number of times a
node is visited. The scoring algorithm is relatively arbitrary in the current implementation, but easy to play with.
