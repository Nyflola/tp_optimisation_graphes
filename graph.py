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
    
    def readLabyrinth(self):
        """
        Lis le graphe(ici appelé labyrinth) à partir d'un fichier

        self.labyrinth => Tableau contenant le graphe
        """
        try:
            labyrinth = []
            file = open(self.path_to_file,"r")
            first_line = file.readline()
            num_line = int(first_line.split(" ")[0])
            num_column = int(first_line.split(" ")[1])
            print(num_line,num_column)
            for line in file:
                row = []
                for i in range(0,num_column):
                    row.append(int(line.split(" ")[i]))
                print(line)
                labyrinth.append(row)
            for row in labyrinth:
                print(row)
        except Exception as e:
            print(e)

    def createAdjacencyMatrix(self):
        """
        Crée la matrice d'ajdacence à partir du graphe d'un fichier lu précédemment

        self.AdjacencyMatrix => La matrice résultante 
        """
    

g = Graph("/home/kali/Semestre_8/Optimisation et graphes/TP/src/reseau_10_10_1.txt")