#!/usr/bin/env python3
from graph import Graph

if __name__ == "__main__":
    g = Graph("./src/reseau_10_10_2.txt")
    g.readLabyrinth()
    g.createAdjacencyMatrix()
    print(g.AdjacencyMatrix)