#!/usr/bin/env python3
from graph_tsp import Graph

if __name__ == "__main__":
    g = Graph("./src/villes_mini.txt")
    g.readMatrix()
    g.tous_les_chemins()
    g.resolve_tsp()