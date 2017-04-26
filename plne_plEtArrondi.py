# -*- coding: utf-8 -*-
import gurobipy as g
import outils

""" Variables """
# r : id rangee

model = g.Model("RP-OptimizeDataCenter")
model.setParam('OutputFlag', False) #Desactive  le mode verbeux
model.setParam('TimeLimit', 60*60) #Limite de temps pour la resolution     

def creerVariables(fileName, choix):
    """
    Creer et retourne les dictionnaires z_mrsi, dicoCaracServeur, k_rs et carac :
    - Les variables Gurobi du PLNE
        z_mrsi["id du serveur"]["num rangee"]["num slot"]["num pool"]
    
    - Un dictionnaire contenant les caracteristiques de chaque serveur
        dicoCaracServeur["id du serveur"] = [taille du serveur, capacite du serveur]
    
    - Pour chaque emplacement (rangee, slot) l'ensemble des serveurs pouvant etre localises a cet emplacement
        k_rs[(idRangee,idSlot)]=[idServeur1, idserveur2,...]
    
    - Les caractéristiques de l'instance
        {'R': nombre de rangees, 'S': nombre de slot par rangee, 'U': nombre de slot inutilisables, 'P': nombre de pools, 'M': nombre de serveurs}
    """
    z_mrsi = {}
    carac, dicoObstacles, listeServeurs, dicoRangees = outils.creeStructureDonnees(fileName)
    
    # dicoCaracServeur["id du serveur"] = [taille du serveur, capacite du serveur]
    dicoCaracServeur = {}
    for serveur in listeServeurs:
        dicoCaracServeur[str(serveur[0])] = [serveur[1], serveur[2]]
        
    k_rs = {}
    for r in range(carac['R']):
        for s in range(carac['S']):
            k_rs[(r,s)] = []
    
    for m in range(carac['M']):
        
        z_mrsi[str(m)] = {}
        
        for r in range(carac['R']):
            
            z_mrsi[str(m)][str(r)] = {}
            
            l_m = outils.genererListe_l_m(dicoObstacles[str(r)],dicoCaracServeur[str(m)][0], carac["S"], r)
            
            for couple in l_m:
                
                k_rs[couple].append(m)
                
                z_mrsi[str(m)][str(r)][str(couple[1])] = {}
                
                for i in range(carac['P']):
                    if choix == "plne":
                        z_mrsi[str(m)][str(r)][str(couple[1])][str(i)] = model.addVar(vtype = g.GRB.BINARY, name="z_mrsi {0} {1} {2} {3}" .format(m, r, couple[1], i))
                    elif choix == "pl":
                        z_mrsi[str(m)][str(r)][str(couple[1])][str(i)] = model.addVar(vtype = g.GRB.CONTINUOUS, name="z_mrsi {0} {1} {2} {3}" .format(m, r, couple[1], i))
    
    model.update()

    return z_mrsi, dicoCaracServeur, k_rs, carac

def contraintes(z_mrsi, dicoCaracServeur, k_rs):

    """ Contraintes """
#1 Chaque slot contient au plus un serveur
#2 Aucun serveur sur slot indispo
#3 Un serveur a autant de slot que sa taille et ils sont consecutifs ou pas affecte (meme rangee et pas depasser taille)
#4 Un serveur affecte apparait au plus une fois
#5 Un serveur affecte appartient a exactement un pool

###############################################################################
###############################################################################
###############################################################################
#    '''
#    contrainte 1 : Au plus un serveur occupe un slot (un marqueur max par slot + pas de chevauchement de serveurs)
#    '''
#    for (r,s), listeServeurs in k_rs.iteritems():
#        somme = 0
#        if len(listeServeurs) != 0:
#            tailleServeurMax = max([dicoCaracServeur[str(idServ)][0] for idServ in listeServeurs])
#            for serveur in listeServeurs:
#                for i in range(0,tailleServeurMax):
#                    if str(s+i) in z_mrsi[str(serveur)][str(r)]:
#                        for a,b in z_mrsi[str(serveur)][str(r)][str(s+i)].iteritems():
#                            somme += b
#            if not type(somme) == type(0):
#                model.addConstr(somme <= 1, "Contrainte 1 : un marqueur max par slot {0} {1}".format(r, s))
###############################################################################
###############################################################################
###############################################################################
    '''
    contrainte 1
    '''
    for (r, s), listeServeurs in k_rs.iteritems():
        somme = 0
        if not len(listeServeurs) == 0:
            for serveur in listeServeurs:
                for k, v in z_mrsi[str(serveur)][str(r)][str(s)].iteritems():
                    somme += v
            
            if not type(somme) == type(0):
                model.addConstr(somme <= 1, "Contrainte 1 : un serveur max par slot {0} {1}".format(r, s))
                
    '''
    contrainte 2
    '''
    for (r, s), listeServeurs in k_rs.iteritems():
        if not len(listeServeurs) == 0:
            for serveur in listeServeurs:
                somme = 0
                grosChiffre = 0
                for i in range(1, dicoCaracServeur[str(serveur)][0]):
                    if not len(k_rs[(r, s + i)]) == 0:
                        for autreServeur in k_rs[(r, s + i)]:
                            if autreServeur != serveur:
                                for k, v in z_mrsi[str(autreServeur)][str(r)][str(s+i)].iteritems():
                                    somme += v
                                    grosChiffre += 1
                grosChiffre += 1
                sommeDuServeur = 0
                for k, v in z_mrsi[str(serveur)][str(r)][str(s)].iteritems():
                    sommeDuServeur += v
                
                if type(somme) != type(0) and type(sommeDuServeur) != type(0):
                    model.addConstr(somme <= grosChiffre * (1 - sommeDuServeur), "Contrainte 1 : SI le serveur {0} est affecte a la position {1} {2} ALORS il n'y a pas d'autres serveurs affecte dans les position qu'il occupe ".format(serveur, r, s))
                    
#                    print "{0} <= {1} * (1 - {2})".format(somme, grosChiffre, sommeDuServeur)
###############################################################################
###############################################################################
###############################################################################
    '''
    contrainte 3 : Un serveur apparait au plus une fois dans une affectation
    (avec un unique pool)
    '''    
    for m in z_mrsi:
        somme = 0
        for r in z_mrsi[str(m)]:
            for s in z_mrsi[str(m)][str(r)]:
                for i in z_mrsi[str(m)][str(r)][str(s)]:
                    somme += z_mrsi[str(m)][str(r)][str(s)][str(i)]
        if not type(somme) == type(0):
            model.addConstr(somme <= 1, "Contrainte 2 : le serveur {0} apparait au plus une fois dans l'affectation".format(m))
    
    
def linearisationFonctionObj(z_mrsi, carac, dicoCaracServeur):
    '''
    contrainte 4 : linearisatin du score pour une affectation avec 
    les linearisations des capacites garanties des pools i pour une affectation
    '''
    sommeCapacitesParPoolParRangee = []
    for i in range(carac["P"]):
        sommeCapacitesParPoolParRangee.append([])
        for r in range(carac["R"]):
            sommeCapacitesParPoolParRangee[i].append(0)
    
    for m in z_mrsi.keys():
        for r in z_mrsi[m].keys():
            for s in z_mrsi[m][r].keys():
                for i in z_mrsi[m][r][s].keys():
                    sommeCapacitesParPoolParRangee[int(i)][int(r)] += z_mrsi[m][r][s][i] * dicoCaracServeur[m][1]
    
    score = model.addVar(vtype = g.GRB.INTEGER, name = "score")
    model.update()
    for i in range(carac["P"]):
        sommeTotale = sum(sommeCapacitesParPoolParRangee[i][:])
        for r in range(carac["R"]):
            model.addConstr(score <= sommeTotale - sommeCapacitesParPoolParRangee[i][r], "Contrainte 3 : capacite garantie par le pool {0} sans la rangee {1}".format(i, r))
    
    f_obj = g.LinExpr() # Variable Gurobi pour une expression lineaire
    f_obj = score
    model.setObjective(f_obj, g.GRB.MAXIMIZE)
    
    model.optimize() # Resolution du Programme Linaire
    print""
    print "Solution"
    print"Valeur optimale de la fonction objectif : ", model.objVal
    print "Temps d'execution :", model.Runtime # Temps d'execution
    if model.Status == 3:
        print "PL non resolvable"
    elif model.Status == 9 and model.SolCount == 0:
        print "PL non resolvable dans la limite de temps"
    print""
    
#    model.write("Programme lineaire.lp") # Ecriture du Programme Lineaire dans un fichier
    
#    for m in z_mrsi.keys():
#        for r in z_mrsi[m].keys():
#            for s in z_mrsi[m][r].keys():
#                for i in z_mrsi[m][r][s].keys():
#                    if z_mrsi[m][r][s][i].x == 0:
#                        print "z_mrsi_{0}_{1}_{2}_{3} = {4}".format(m, r, s, i, z_mrsi[m][r][s][i].x)
                
    return z_mrsi

def resolution_PL(nomFichier, pourcentage, choix):
    """
    Fonction a appeler pour lancer la resolution par PL ou PLNE avec Gurobi
    """
    nomFichierInstance = outils.creeFichierInstancePourcentage(nomFichier, pourcentage)
    z_mrsi, dicoCaracServeur, k_rs, carac= creerVariables(nomFichierInstance, choix)
    contraintes(z_mrsi, dicoCaracServeur, k_rs)
    z_mrsi = linearisationFonctionObj(z_mrsi, carac, dicoCaracServeur)
#    print z_mrsi 
    return z_mrsi, dicoCaracServeur, carac
                    
def heuristiqueArrondi(nomFichier, pourcentage):
    z_mrsi, dicoCaracServeur, carac = resolution_PL(nomFichier, pourcentage, "pl")
    
    # cle : id du serveur, valeur : True / False pour savoir par la suite si le serveur est deja affecte ou non
    masqueServeurLibre = {}
    listeTriee = []
    for m in z_mrsi.keys():
        masqueServeurLibre[m] = True
        for r in z_mrsi[m].keys():
            for s in z_mrsi[m][r].keys():
                for i in z_mrsi[m][r][s].keys():
                    listeTriee.append((m, r, s, i, z_mrsi[m][r][s][i].x))
    
    listeTriee.sort(key = lambda tup : tup[4], reverse = True)
    
    dicoVerif = {}
    affectation = {}
    
    for i in range(0, carac['R']):
        dicoVerif[str(i)]= ['' for j in range(carac['S'])]
            
    for elt in listeTriee:
        placementOk = True
        taille = dicoCaracServeur[elt[0]][0]
        if masqueServeurLibre[elt[0]]:
            for s in range(taille):
                if(dicoVerif[elt[1]][int(elt[2]) + s] != ''):
                    placementOk = False
                    break
            # Si on peut le placer et que le serveur n'a pas encore ete affecte, on le place et on l'affecte
            if placementOk:
                affectation[elt[0]] = [int(elt[1]),int(elt[2]),int(elt[3])]
                masqueServeurLibre[elt[0]] = False
                for s in range(taille):
                    dicoVerif[elt[1]][int(elt[2]) + s] = elt[0]
            else: 
                affectation[elt[0]] = 'x'
          
    score = outils.calculScore(affectation, carac, dicoCaracServeur)
    print "Score obtenu avec l'heuristique arrondi :", score
    
    return z_mrsi, dicoCaracServeur, carac


def heuristiqueArrondiPerso1(nomFichier, pourcentage, z_mrsi, dicoCaracServeur, carac):
#    z_mrsi, dicoCaracServeur, carac = resolution_PL(nomFichier, pourcentage, "pl")
   
    masqueServeurLibre = {}
    listeTriee = []
    for m in z_mrsi.keys():
        masqueServeurLibre[m] = True
        for r in z_mrsi[m].keys():
            for s in z_mrsi[m][r].keys():
                for i in z_mrsi[m][r][s].keys():
                    listeTriee.append((m, r, s, i, z_mrsi[m][r][s][i].x))
    
    listeTriee.sort(key = lambda tup : tup[4], reverse = True)
    
    dicoVerif = {}
    affectation = {}
    
    for i in range(0, carac['R']):
        dicoVerif[str(i)]= ['' for j in range(carac['S'])]
            
    
    capacitesPools = []
    for a in range(carac['P']):
        capacitesPools.append(0)
        
        
    for elt in listeTriee:
        placementOk = True
        taille = dicoCaracServeur[elt[0]][0]
        if masqueServeurLibre[elt[0]]:
            for s in range(taille):
                if(dicoVerif[elt[1]][int(elt[2]) + s] != ''):
                    placementOk = False
                    break
            
            if placementOk:  
                affectation[elt[0]] = [int(elt[1]),int(elt[2]),capacitesPools.index(min(capacitesPools))] # affecte le pool qui a le moins de capacite
                capacitesPools[capacitesPools.index(min(capacitesPools))] += dicoCaracServeur[elt[0]][1] #ajoute sa capacité au pool
                masqueServeurLibre[elt[0]] = False #marque ce serveur comme déjà place
                for s in range(taille):
                    dicoVerif[elt[1]][int(elt[2]) + s] = elt[0]
            else: 
                affectation[elt[0]] = 'x'
        
    score = outils.calculScore(affectation, carac, dicoCaracServeur)
    print "Score obtenu avec notre heuristique perso 1 :", score

def heuristiqueArrondiPerso2(nomFichier, pourcentage, z_mrsi, dicoCaracServeur, carac):
#    z_mrsi, dicoCaracServeur, carac = resolution_PL(nomFichier, pourcentage, "pl")
   
    masqueServeurLibre = {}
    listeTriee = []
    for m in z_mrsi.keys():
        masqueServeurLibre[m] = True
        for r in z_mrsi[m].keys():
            for s in z_mrsi[m][r].keys():
                for i in z_mrsi[m][r][s].keys():
                    listeTriee.append((m, r, s, i, z_mrsi[m][r][s][i].x))
    
    listeTriee.sort(key = lambda tup : tup[4], reverse = True)
    
    dicoVerif = {}
    affectation = {}
    rangeeCapacitesPools = {}
    
    for i in range(0, carac['R']):
        dicoVerif[str(i)]= ['' for j in range(carac['S'])]
        rangeeCapacitesPools[i]=[]
        for j in range(0,carac['P']):
            rangeeCapacitesPools[i].append([j,0])    
                
    for elt in listeTriee:
        placementOk = True
        taille = dicoCaracServeur[elt[0]][0]
        if masqueServeurLibre[elt[0]]:
            for s in range(taille):
                if(dicoVerif[elt[1]][int(elt[2]) + s] != ''):
                    placementOk = False
                    break
            
            if placementOk:
                affectation[elt[0]] = [int(elt[1]),int(elt[2]),rangeeCapacitesPools[int(elt[1])][0][0]] # affecte le pool qui a le moins de capacite
                rangeeCapacitesPools[int(elt[1])][0][1] += dicoCaracServeur[elt[0]][1] #ajoute sa capacité au pool
                
                rangeeCapacitesPools[int(elt[1])].sort(key = lambda tup : tup[1])
                masqueServeurLibre[elt[0]] = False #marque ce serveur comme déjà place
                for s in range(taille):
                    dicoVerif[elt[1]][int(elt[2]) + s] = elt[0]
                    
            else: 
                affectation[elt[0]] = 'x'
        
    score = outils.calculScore(affectation, carac, dicoCaracServeur)
    print "Score obtenu avec notre heuristique perso 2 :", score
    
def testHeuristiquesArrondi(nomFichier, pourcentage):
    """
    calcul le PL sur un pourcentage de l'instance contenue dans nomFichier,
    puis a partir des resultats du PL calcul le score avec 3 methodes d'arrondi
    - Entree :
        nomFichier, le nom de l'instance
        pourcentage, le pourcentage de l'instance que l'on souhaite conserver
    - Sortie :
        aucune, affiche les scores obtenus par les methodes d'arrondi
    """
    z_mrsi, dicoCaracServeur, carac = heuristiqueArrondi(nomFichier, pourcentage)
    heuristiqueArrondiPerso1(nomFichier, pourcentage, z_mrsi, dicoCaracServeur, carac)
    heuristiqueArrondiPerso2(nomFichier, pourcentage, z_mrsi, dicoCaracServeur, carac)
    
def main():
    nomFichier = "dc.in"
    pourcentage = 30
    
    resolution_PL(nomFichier, pourcentage, "plne")
#    testHeuristiquesArrondi(nomFichier, pourcentage)
    
main()