#!/usr/bin/env python3
from math import *

class Graph:
    def __init__(self,path_to_file):
        """
        Constructeur de la classe

        path_to_file => chemin menant au fichier contenant le graphe
        """
        self.path_to_file = path_to_file
        self.labyrinth = None
        self.AdjacencyMatrix = None
        self.num_line = None
        self.num_column = None
    
    def readLabyrinth(self):
        """
        Lis le graphe(ici appelé labyrinth) à partir d'un fichier

        self.labyrinth => Tableau contenant le graphe
        """
        try:
            labyrinth = []
            file = open(self.path_to_file,"r")
            first_line = file.readline()
            self.num_line = int(first_line.split(" ")[0])
            self.num_column = int(first_line.split(" ")[1])
            for line in file:
                row = []
                for i in range(0,self.num_column):
                    row.append(int(line.split(" ")[i]))
                labyrinth.append(row)
            self.labyrinth = labyrinth
        except Exception as e:
            print(e)

    def ajout_chemin(self, i, j, n, m):
        if self.labyrinth[i][j] == 0 or self.labyrinth[n][m] == 0:
            return 9999
        elif (i == n-1 and j == m) or (i == n+1 and j == m) or (i == n and j == m-1) or (i == n and j == m+1):
            return 1
        elif (i == n-1 and j == m-1) or (i == n+1 and j == m-1) or (i == n-1 and j == m+1) or (i == n+1 and j == m+1):
            return sqrt(2)
        else:
            return 9999

    def ajout_chemin_sommet(self, ligne, colonne):
        n = len(self.labyrinth)
        liste_sommet = []
        for i in range(n):
            for j in range(n):
                chemin = self.ajout_chemin(ligne, colonne, n-1-i, j)
                liste_sommet.append(chemin)
        return liste_sommet



    def createAdjacencyMatrix(self):
        """
        Crée la matrice d'ajdacence à partir du graphe d'un fichier lu précédemment

        self.AdjacencyMatrix => La matrice résultante 
        """
        n = len(self.labyrinth)
        k = 0
        self.AdjacencyMatrix = []
        for i in range(n):
            for j in range(n):
                Liste_sommet = self.ajout_chemin_sommet(n-1-i,j)
                self.AdjacencyMatrix.append(Liste_sommet)
