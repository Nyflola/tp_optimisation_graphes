#!/usr/bin/env python3
from math import *
from numpy import s_
import copy

#Comment numérote-t-on les sommets dans certaines fonctions de cette classe et dans d'autres script?
#Les sommet sont numérotés de 0 à nombre_de_sommets - 1
#Le sommet n°0 est le sommet en bas à gauche et le sommet n°ombre_de_sommets - 1 est le sommet en haut à droite
#On compte donc les sommets de gauche à droite et de bas en haut comme indiqué dans l'énoncé


class Graph:
    def __init__(self,path_to_file : str) -> None:
        """
        Constructeur de la classe

        path_to_file => chemin menant au fichier contenant le graphe
        """
        self.path_to_file = path_to_file
        self.AdjacencyMatrix = None
        self.num_line = None
        self.num_column = None
    
    def readMatrix(self) -> None:
        """
        Lis, à partir du fichier passé au constructeur, la matrice correspondant aux villes et aux poids
        La matrice d'adjacence est stockée dans la variable d'instance "self.AdjacencyMatrix"

        Le fichier est supposé être écris correctement et suivant la syntaxe suivante:
        "
        3 3
        0 1 1
        1 0 1
        1 1 0
        "
        La valeur 0 est utilisée, arbitrairement, pour indiquer qu'un trajet n'est pas possible
        Les valeurs doivent être >= 0
        """
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

    def get_poids(self, i : int, j : int) -> int:
        """
        Retourne le poids associé au trajet de la ville i à la ville j
        """
        return self.AdjacencyMatrix[i][j] 
        
    def trajet_possible(self,i : int,j : int) -> bool:
        """
        Indique par "True" ou "False" si le trajet de la ville i à la ville j existe
        """
        return True if self.get_poids(i,j) > 0 else False

    def trajets_possibles(self,i : int,visited : list) -> list:
        """
        Retourne la liste des villes atteignables directement (en un seul trajet) depuis la ville i.
        Cet algorithme prend en compte une liste de ville déjà visitée.

        i: Entier correspondant à l'indice dans la matrice de la ville de départ
        visited: Liste contenant soit la liste vide soit une liste d'indice de la matrice
        """
        trajets = []
        for j in range(self.num_column):
            if self.trajet_possible(i,j) and j not in visited:
                trajets.append(j)
        return trajets

    def longueur_trajet(self,trajet : list) -> int:
        """
        Retourne un entier correspondant à la longeur du trajet passé en paramètre

        trajet: Liste de la forme suivante [[0,1],[1,2]]
                Dans l'exemple ci dessous le trajet complet 
                correspond au trajet de la ville 0 à la ville 1 puis de la ville 1 à la ville 2.
        """
        res = 0
        for route in trajet:
            res += self.get_poids(route[0],route[1])
        return res

    def fonction_min(self,sommet : int,visited : list) -> list:
        """
        Fonction récursive permettant de récupérer le(s) cycle(s) hamiltonien(s) (un trajet) le(s) plus court(s) avec
        pour point de départ le sommet "sommet" passé en paramètre sachant les sommets déjà visités

        sommet: Sommet de départ, un indice de la matrice, ex: 0
        visited: liste contenant les villes déjà visitées sous forme d'indice, ex: [0,2,3]
        """
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
        """
        Fonction récursive permettant de récupérer tous les cycles hamiltoniens (trajets)
        avec pour point de départ le sommet "sommet" passé en paramètre sachant les sommets déjà visités

        sommet: Sommet de départ, un indice de la matrice, ex: 0
        visited: liste contenant les villes déjà visitées sous forme d'indice, ex: [0,2,3]
        """
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

    def resolve_tsp(self) -> None:
        """
        Résoud le problème du voyageur de commerce et affiche le(s) résultat(s).

        La matrice d'adjacence est supposée formée et le fichier lu.
        """
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
            j = 1
            print("Chemin %d (Longueur = %d):" % (i,self.longueur_trajet(trajet)),end="\n")
            for route in trajet:
                print("\t%d. Sommet %d -> Sommet %d" % (j,route[0],route[1]),end="\n")
                j += 1
            i += 1
            print()

    def tous_les_chemins(self) -> None:
        """
        Affiche la liste de tous les cycles hamiltoniens pour le problème du voyageur de commerce.

        La variable "filtre" ci-dessous permet de filtrer les résultats par longueur(20 max ici).

        Cette fonction est utile afin de vérifier le bon fonctionnement des algorithmes au dessus. 
        """
        res = []
        filtre = 20
        for sommet in range(self.num_line):
            res += self.fonction_all(sommet,[sommet])
        print("Voici tous les chemins possibles avec une durée de moins de %d :\n" % filtre)
        i = 1
        for trajet in res:
            if self.longueur_trajet(trajet) <= filtre:
                print("Chemin %d (Longueur = %d):" % (i,self.longueur_trajet(trajet)),end="\n")
                j = 1
                for route in trajet:
                    print("\t%d. Sommet %d -> Sommet %d" % (j,route[0],route[1]),end="\n")
                    j += 1
                i += 1
                print()

