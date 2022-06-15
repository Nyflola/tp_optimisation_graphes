#!/usr/bin/env python3
from graph_tsp import Graph

if __name__ == "__main__":
    #Initialise le graphe
    g = Graph("./src/villes_mini.txt")
    #Lis le fichier et initialise la matrice d'adjacence
    g.readMatrix()
    #Affiche tous les cycles hamiltoniens possibles
    g.tous_les_chemins()
    #Affiche les cycles hamiltoniens de taille minimale
    g.resolve_tsp()