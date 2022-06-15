from pyparsing import col
from sympy import N
from docplex.mp.model import Model
from graph import Graph
import os
import time
import cplex

#Problème rencontré: trop de variables si on prend la matrice des xij de la même taille que la matrice d'adjacence
#Solution: On récupère uniquement les données qui nous intéressent, c-à-d les aij qui ne valent pas +infini, soit uniquement les chemins de i à j qui existent
def aij_non_infini(matrice):
    L_aij = []
    L_coo_aij = []
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j] < 10:
                L_aij.append(matrice[i][j])
                L_coo_aij.append([i,j])
    return(L_aij, L_coo_aij)


#Initialisation
rep = "./src/"
file_name = "reseau_5_10_1.txt"

#Création du graphe et de sa matrice d'adjacence
g = Graph(rep+file_name)
g.readLabyrinth()
g.createAdjacencyMatrix()

A = g.AdjacencyMatrix #A est la matrice d'adjacence du graphe
nb_sommets = len(A) #nb_sommets est le nombre de sommet du graphe

s, f = g.dep_arr()

#2 listes: une pour les poids et une pour les coordonnées (ville départ, ville arrivée) pour faire le lien plus tard dans le code.
data = aij_non_infini(A)
L_sommets_utiles = data[0]
L_coo_sommets_utiles = data[1]

#print("start = ",s)
#print("finish = ",f)

start = time.time()

opt_mod = Model('Shortest Path')

# creation de la liste des variables binaires des arcs (i,j) associée aux poids utiles choisis précédemment
X = []
for i in range(len(L_sommets_utiles)):
    X.append(opt_mod.binary_var(name=None))


#Renvoie la liste des sommets utiles de la même ligne (par rapport à la matrice d'adjacence)
def ligne_utile(i, L, L_coo):
    ligne_i = []
    for j in range(len(L)):
        if L_coo[j][0] == i:
            ligne_i.append(L[j])
    return(ligne_i)

#Renvoie la liste des sommets utiles de la même colonne (par rapport à la matrice d'adjacence)
def colonne_utile(i, L, L_coo):
    colonne_i = []
    for j in range(len(L)):
        if L_coo[j][1] == i:
            colonne_i.append(L[j])
    return colonne_i


# définition des contraintes
for i in range(nb_sommets):
    x = ligne_utile(i, X, L_coo_sommets_utiles)
    y = colonne_utile(i, X, L_coo_sommets_utiles)
    if i==s:
        opt_mod.add_constraint(sum(x)-sum(y)==1)
    elif i==f:
        opt_mod.add_constraint(sum(x)-sum(y)==-1)
    else:
        opt_mod.add_constraint(sum(x)-sum(y)==0)

# contrainte : x >= 0
for x in X:
    opt_mod.add_constraint(x>=0)


# fonction objectif
SUM = []
for i in range(len(L_sommets_utiles)):
    SUM.append(X[i]*L_sommets_utiles[i])


# minimisation + résolution du modèle MAIS pb de taille pour le 50*50. La version gratuite de cplexe limite le nombre de variables
obj_fn = sum(SUM)
opt_mod.set_objective('min', obj_fn)
opt_mod.solve()

# récupération des informations intéréssantes
cout = opt_mod.solution.get_objective_value()
variables = opt_mod.solution.iter_var_values()

#Fonction de tri qui nous servira après
#Tri une liste de chemin entre 2 villes depuis la ville de départ jusqu'à la ville d'arrivée
#Exemple:
#Si on doit partir de la ville 3 pour arriver à la ville 15 et que la liste du trajet est [[1,7], [8,15], [7,8], [3,6], [6, 1]]
#La fonction renvoie la liste [[3,6], [6,1], [1,7], [7,8], [8,15]]
def tri_chemin(L, d):
    L_tri = []
    for i in range(len(L)):
        if L[i][0] == d:
            L_tri.append(L[i])
    for k in range(len(L)-1):
        for i in range(len(L)):
            if L[i][0] == L_tri[k][1]:
                L_tri.append(L[i])
    return L_tri

end = time.time()
print('time elapsed =', end - start, 's')

#écriture du cout  et du plus court chemin dans un fichier texte
#La liste du chemin sera représenté sous la forme [[ville_depart, vill_a], [ville_a, ville_b], ..., [ville_n, ville_arrivée]]
def ecriture_solution(cout, variables, L_coo, d, a):
    #On récupère dans une liste les numéros des xi utilisés dans le plus court chemin
    chemin = []
    for i in variables:
        var = str(i[0])
        index = int(var[1:])
        chemin.append(index-1)
    pcc = []
    #On récupère les doublet [ville départ, ville arrivée] associées aux xi retenus par cplexe
    for k in range(len(chemin)):
        indice = chemin[k]
        pcc.append(L_coo[indice])
    pcc = tri_chemin(pcc, d)
    OutputFileName = rep + 'sol_' + file_name
    with open(OutputFileName, 'w') as f:
        f.write('coût = ' + str(cout))
        f.write('\n')
        f.write('sommets visités = ' + str(pcc))

ecriture_solution(cout, variables, L_coo_sommets_utiles, s, f)
