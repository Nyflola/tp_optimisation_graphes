from pyparsing import col
from sympy import N
from docplex.mp.model import Model
from graph import Graph
import os
import time
import cplex


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
file_name = "reseau_5_10_2.txt"

g = Graph(rep+file_name)
g.readLabyrinth()
g.createAdjacencyMatrix()

A = g.AdjacencyMatrix #A est la matrice d'adjacence du graphe
nb_sommets = len(A) #n est le nombre de sommet du graphe

s, f = g.dep_arr()

data = aij_non_infini(A)
L_sommets_utiles = data[0]
L_coo_sommets_utiles = data[1]

#print("start = ",s)
#print("finish = ",f)

start = time.time()
#opt_mod = Model(name = "Shortest Path")
opt_mod = Model('Shortest Path')

# creation de la liste des variables binaires des arcs (i,j) associée à la liste d'adjacence
X = []
for i in range(len(L_sommets_utiles)):
    X.append(opt_mod.binary_var(name=None))


#Renvoie la liste des sommets utiles de la même ligne
def ligne_utile(i, L, L_coo):
    ligne_i = []
    for j in range(len(L)):
        if L_coo[j][0] == i:
            ligne_i.append(L[j])
    return(ligne_i)

#Renvoie la liste des sommets utiles de la même colonne
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
        #contrainte de visite de toutes les villes
        if x != []:
            opt_mod.add_constraint(sum(x) >= 1)

# contrainte : x >= 0
for x in X:
    opt_mod.add_constraint(x>=0)


# fonction objectif
SUM = []
for i in range(len(L_sommets_utiles)):
    SUM.append(X[i]*L_sommets_utiles[i])


# minimisation + résolution du modèle  ----> pb de taille ici
obj_fn = sum(SUM)
opt_mod.set_objective('min', obj_fn)
#opt_mod.print_information()
opt_mod.solve()
#opt_mod.print_solution()


# récupération des informations intéréssantes
cout = opt_mod.solution.get_objective_value()
variables = opt_mod.solution.iter_var_values()

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

# écriture du cout + pcc dans un fichier texte
def ecriture_solution(cout, variables, L_coo, d, a):
    chemin = []
    for i in variables:
        var = str(i[0])
        index = int(var[1:])
        chemin.append(index-1)
    pcc = []
    for k in range(len(chemin)):
        indice = chemin[k]
        pcc.append(L_coo[indice])
    #pcc = tri_chemin(pcc[1:], d)
    OutputFileName = rep + 'sol_voyageur_' + file_name
    with open(OutputFileName, 'w') as f:
        f.write('coût = ' + str(cout))
        f.write('\n')
        f.write('départ = ' + str(d) + ', arrivée = ' + str(a))
        f.write('\n')
        f.write('sommets visités = ' + str(pcc))

ecriture_solution(cout, variables, L_coo_sommets_utiles, s, f)







