#!/usr/bin/env python3
from graph import Graph

if __name__ == "__main__":
    g = Graph("/home/kali/Semestre_8/Optimisation et graphes/TP/src/reseau_10_10_1.txt")
    g.readLabyrinth()
    g.createAdjacencyMatrix()