#!/usr/bin/env python3

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
        except Exception as e:
            print(e)

    def createAdjacencyMatrix(self):
        """
        Crée la matrice d'ajdacence à partir du graphe d'un fichier lu précédemment

        self.AdjacencyMatrix => La matrice résultante 
        """
        k = 0
        for i in range(self.num_line,-1,-1):
            for j in range(0,self.num_column):
                None
