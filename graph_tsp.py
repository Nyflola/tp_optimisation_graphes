#!/usr/bin/env python3
from math import *
from numpy import s_
import copy

#Comment numérote-t-on les sommets dans certaines fonctions de cette classe et dans d'autres script?
#Les sommet sont numérotés de 0 à nombre_de_sommets - 1
#Le sommet n°0 est le sommet en bas à gauche et le sommet n°ombre_de_sommets - 1 est le sommet en haut à droite
#On compte donc les sommets de gauche à droite et de bas en haut comme indiqué dans l'énoncé


class Graph:
    def __init__(self,path_to_file):
        #Constructeur de la classe
        #path_to_file => chemin menant au fichier contenant le graphe
        self.path_to_file = path_to_file
        self.AdjacencyMatrix = None
        self.num_line = None
        self.num_column = None
    
    def readMatrix(self):
        #Lis le graphe(ici appelé labyrinth) à partir d'un fichier et le stock dans self.labyrinth
        try:
            AdjacencyMatrix = []
            file = open(self.path_to_file,"r")
            first_line = file.readline()
            self.num_line = int(first_line.split(" ")[0])
            self.num_column = int(first_line.split(" ")[1])
            for line in file:
                row = []
                for i in range(0,self.num_column):
                    row.append(int(line.split(" ")[i]))
                AdjacencyMatrix.append(row)
            self.AdjacencyMatrix = AdjacencyMatrix
        except Exception as e:
            print(e)

    #retourne le poids pour aller du sommet i,j du labyrinthe au sommet n,m
    def get_poids(self, i, j):
        return self.AdjacencyMatrix[i][j] 
        
    def trajet_possible(self,i,j):
        return True if self.get_poids(i,j) > 0 else False

    def trajets_possibles(self,i,visited):
        trajets = []
        for j in range(self.num_column):
            if self.trajet_possible(i,j) and j not in visited:
                trajets.append(j)
        return trajets

    def longueur_trajet(self,trajet):
        res = 0
        for route in trajet:
            res += self.get_poids(route[0],route[1])
        return res

    def fonction_min(self,sommet : int,visited : list) -> list:
        possibilites = []
        sommets_possibles = self.trajets_possibles(sommet,visited)
        for s in sommets_possibles:
            visited_copy = copy.deepcopy(visited)
            visited_copy.append(s)
            trajets = self.fonction_min(s,visited_copy)
            if trajets == [] and len(visited_copy) == self.num_line:
                possibilites.append([[sommet,s]])
            elif trajets != [] and len(visited_copy) < self.num_line:
                nouveaux_trajets = []
                for trajet in trajets:
                    nouveaux_trajets.append([[sommet,s]] + trajet)
                min = [nouveaux_trajets[0]]
                for i in range(1,len(nouveaux_trajets)):
                    if self.longueur_trajet(nouveaux_trajets[i]) < self.longueur_trajet(min[0]):
                        min = [nouveaux_trajets[i]]
                    elif self.longueur_trajet(nouveaux_trajets[i]) == self.longueur_trajet(min[0]):
                        min.append(nouveaux_trajets[i])
                for trajet in min:
                    possibilites.append(trajet)
        return possibilites

    def fonction_all(self,sommet : int,visited : list) -> list:
        possibilites = []
        sommets_possibles = self.trajets_possibles(sommet,visited)
        for s in sommets_possibles:
            visited_copy = copy.deepcopy(visited)
            visited_copy.append(s)
            trajets = self.fonction_all(s,visited_copy)
            if trajets == [] and len(visited_copy) == self.num_line:
                possibilites.append([[sommet,s]])
            elif trajets != [] and len(visited_copy) < self.num_line:
                for trajet in trajets:
                    nouveaux_trajet = [[sommet,s]] + trajet
                    possibilites.append(nouveaux_trajet)
        return possibilites

    def resolve_tsp(self):
        res = []
        for sommet in range(self.num_line):
            res += self.fonction_min(sommet,[sommet])
        min = [res[0]]
        for i in range(1,len(res)):
            if self.longueur_trajet(res[i]) < self.longueur_trajet(min[0]):
                min = [res[i]]
            elif self.longueur_trajet(res[i]) == self.longueur_trajet(min[0]):
                min.append(res[i])
        print("\n\nVoici le(s) chemin(s) le(s) plus court(s) trouvé(s) :\n")
        i = 1
        for trajet in min:
            print("Chemin %d (Longueur = %d):" % (i,self.longueur_trajet(trajet)),end="\n")
            for route in trajet:
                print("\tSommet %d -> Sommet %d" % (route[0],route[1]),end="\n")
            i += 1
            print()

    def tous_les_chemins(self):
        res = []
        filtre = 30
        for sommet in range(self.num_line):
            res += self.fonction_all(sommet,[sommet])
        print("Voici tous les chemins possibles avec une durée de moins de %d :\n" % filtre)
        i = 1
        for trajet in res:
            print("Chemin %d (Longueur = %d):" % (i,self.longueur_trajet(trajet)),end="\n")
            for route in trajet:
                print("\tSommet %d -> Sommet %d" % (route[0],route[1]),end="\n")
            i += 1
            print()

