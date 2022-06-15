#!/usr/bin/env python3
from math import *

from numpy import s_

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

    def ajout_chemin(self, i, j, n, m): #retourne le poids pour aller du sommet i,j du labyrinthe au sommet n,m
        if self.labyrinth[i][j] == 0 or self.labyrinth[n][m] == 0:
            return 9999
        elif (i == n-1 and j == m) or (i == n+1 and j == m) or (i == n and j == m-1) or (i == n and j == m+1):
            return 1
        elif (i == n-1 and j == m-1) or (i == n+1 and j == m-1) or (i == n-1 and j == m+1) or (i == n+1 and j == m+1):
            return sqrt(2)
        else:
            return 9999

    def ajout_chemin_sommet(self, ligne, colonne): #retourne la liste des poids des chemins du sommet ligne,colonne du labyrinthe vers tous les autres sommets du labyrinthe
        n = len(self.labyrinth)
        m = len(self.labyrinth[0])
        liste_sommet = []
        for i in range(n):
            for j in range(m):
                chemin = self.ajout_chemin(ligne, colonne, n-1-i, j)
                liste_sommet.append(chemin)
        return liste_sommet



    def createAdjacencyMatrix(self):
        """
        Crée la matrice d'ajdacence à partir du graphe d'un fichier lu précédemment

        self.AdjacencyMatrix => La matrice résultante 
        """
        n = len(self.labyrinth)
        m = len(self.labyrinth[0])
        self.AdjacencyMatrix = []
        for i in range(n):
            for j in range(m):
                Liste_sommet = self.ajout_chemin_sommet(n-1-i,j)
                self.AdjacencyMatrix.append(Liste_sommet)

    def list_edge(self):
        L = []
        for ligne in self.labyrinth:
            L = ligne + L
        return L


    #retourne la liste de deux éléments [sommet départ, sommet arrivée]
    def dep_arr(self):
        L = self.list_edge()
        s = 0
        f = 0
        for i in range(len(L)):
            if L[i] == 2:
                s = i
            elif L[i] == 3:
                f = i
        return s, f
        


