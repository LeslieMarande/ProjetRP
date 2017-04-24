# -*- coding: utf-8 -*-

#2 5 1 2 5 : 2 rows of 5 slots each, 1 slot unavailable, 2 pools and 5 servers.

import random
import math
from copy import deepcopy
import time
import outils

# Methodes gloutonnes : Q 1.1.
###############################################################################
def methodeGloutonne1(nomFichier):
    """
    Implementation de l'algorithme glouton de la Q 1.1. du sujet
    - Entree :
        nomFichier, nom de l'instance sur laquelle on applique l'algorithme
    - Sortie :
        aucune, genere un fichier enregistrant l'affectation, 
        affiche la repartition des serveurs sur les rangees et le score dans la console
    """
    carac, dicoObstacles, listeServeurs, dicoRangees = outils.creeStructureDonnees(nomFichier)
    affectation = {}
    slotTrouve = False    
    
    #Creer affectation
    for s in listeServeurs:
        for r in range(carac["R"]):
            numSlot = outils.positionServeurSlot(dicoObstacles[str(r)], s[1], carac["S"])
            if numSlot != None:
                for i in range(s[1]):
                    dicoObstacles[str(r)].append(numSlot + i)
                    dicoRangees[str(r)][numSlot+i] = str(s[0])
                dicoObstacles[str(r)].sort()
                slotTrouve = True 
                affectation[str(s[0])] = [r, numSlot]  
                break
        if slotTrouve == False :
            affectation[str(s[0])] = 'x' 
        
        slotTrouve = False
    
    #Affection des pools 
    numPool = -1
    valTemp = None        
    for k in dicoRangees.keys() :
        for v in dicoRangees[k]:
            if not v == 'x':
                if not v == valTemp:
                    if numPool < carac["P"] - 1:
                        numPool += 1
                    else:
                        numPool = 0
                    affectation[v].append(numPool)
                    valTemp = v
    
    outils.genererFichierSolution(affectation, nomFichier, "glouton1")
    
    # dicoCaracServeur["id du serveur"] = [taille du serveur, capacite du serveur]
    dicoCaracServeur = {}
    for serveur in listeServeurs:
        dicoCaracServeur[str(serveur[0])] = [serveur[1], serveur[2]]
    
    print "Affectation methode gloutonne 1 : "
    outils.afficheAffectation(dicoRangees, carac)
    
    score = outils.calculScore(affectation, carac, dicoCaracServeur)
    print "Score methode gloutonne 1 : ", score
    print ""
    
    
# Methodes gloutonnes : Q 1.2.
###############################################################################
def methodeGloutonne2(nomFichier):
    """
    Implementation de notre l'algorithme personnelle glouton de la Q 1.2. du sujet
    - Entree :
        nomFichier, nom de l'instance sur laquelle on applique l'algorithme
    - Sortie :
        aucune, genere un fichier enregistrant l'affectation,
        affiche la repartition des serveurs sur les rangees et le score dans la console
    """
    carac, dicoObstacles, listeServeurs, dicoRangees = outils.creeStructureDonnees(nomFichier)
    listeServeurs = outils.donnerPoolAuxServeurs(listeServeurs,carac)
    dicoPoolsCapacite = {}
    affectation = {}
    slotTrouve = False
    
    # dictionnaire dicoPoolsCapacite
    # cle : numero de pool, valeur : [numero de rangee, capacite dans la rangee de ce pool] 
    for i in range(0, carac['P']):
            dicoPoolsCapacite[str(i)] =  []
            for j in range(0, carac['R']):
                dicoPoolsCapacite[str(i)].append([j,0])             

    for s in listeServeurs :
        for r in dicoPoolsCapacite[str(s[3])] :
            numSlot = outils.positionServeurSlot((dicoObstacles[str(r[0])]), s[1], carac["S"])
            if numSlot != None:
                for i in range(s[1]):
                    dicoObstacles[str(r[0])].append(numSlot + i)
                    dicoRangees[str(r[0])][numSlot+i] = str(s[0])
                dicoObstacles[str(r[0])].sort()
                slotTrouve = True 
                affectation[str(s[0])] = [r[0], numSlot,s[3]]
                
                r[1] +=  s[2]
                dicoPoolsCapacite[str(s[3])].sort(key = lambda tup : tup[1])
                break
            
        if slotTrouve == False :
            affectation[str(s[0])] = 'x' 
        
        slotTrouve = False
    
    outils.genererFichierSolution(affectation, nomFichier, "glouton2")
    
    # dicoCaracServeur["id du serveur"] = [taille du serveur, capacite du serveur]
    dicoCaracServeur = {}
    for serveur in listeServeurs:
        dicoCaracServeur[str(serveur[0])] = [serveur[1], serveur[2]]
    
    print "Affectation methode gloutonne 2 : "
    outils.afficheAffectation(dicoRangees, carac)
    
    score = outils.calculScore(affectation, carac, dicoCaracServeur)
    print "Score methode gloutonne 2 : ", score
    print ""


# Meta-heuristique : Q 2.1.
###############################################################################    
def descenteStochastique(nomFichier):
    affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne2(nomFichier)
    nouvelleAffectation = {}
    nouveauDicoObstacles = {}
    cpt = 0
    maxIteration = 1000
    
    # dicoCaracServeur["id du serveur"] = [taille du serveur, capacite du serveur]
    dicoCaracServeur = {}
    for serveur in listeServeurs:
        dicoCaracServeur[str(serveur[0])] = [serveur[1], serveur[2]]

    print "Score avant descente: ",outils.calculScore(affectation, carac, dicoCaracServeur)
    
    while cpt < maxIteration:
        nbAlea = random.random()
        changement = False
        if nbAlea < 0.3:
            nouvelleAffectation, nouveauDicoObstacles = voisinageEnleverUnServeur(affectation, dicoCaracServeur, dicoObstacles)
            changement = True
        elif 0.3 <= nbAlea and nbAlea < 0.6:
            nouvelleAffectation, nouveauDicoObstacles = voisinageServeurNonAffecte(affectation, dicoCaracServeur, dicoObstacles, carac)
            changement = True
        else:
            nouvelleAffectation = voisinageChangementPool(affectation, carac)
        cpt+=1
       # print("Nouveau score",calculScore(nouvelleAffectation, carac, dicoCaracServeur) )
        if outils.calculScore(nouvelleAffectation, carac, dicoCaracServeur) >= outils.calculScore(affectation, carac, dicoCaracServeur):
        #    print("BETTER")
            affectation = deepcopy(nouvelleAffectation)
            if changement:
                dicoObstacles = deepcopy(nouveauDicoObstacles)
        
##        if cpt %4 == 0:
##            if calculScore(nouvelleAffectation, carac, dicoCaracServeur) >= outils.calculScore(bestAffectation, carac, dicoCaracServeur):
##                affectation = nouvelleAffectation
##                dicoObstacles = nouveauDicoObstacles
##                bestAffectation = deepcopy(affectation)
##                bestDicoObstacles= deepcopy(dicoObstacles)
##            else:
##                affectation =bestAffectation 
##                dicoObstacles=bestDicoObstacles
##        else:
##                affectation = nouvelleAffectation
##                dicoObstacles = nouveauDicoObstacles
            


        
    print "Score final: ", outils.calculScore(affectation, carac, dicoCaracServeur)
    
    
    return None 


def voisinageEnleverUnServeur(affectation, dicoCaracServeur, dicoObstacles):
    """
    Genere aleatoirement un voisin possible a partir d'une affectation
    en enlevant un serveur de cette affectation
    - entree : l'affectation courante, la liste des caracteristiques des serveurs 
                (id, taille, capacite), les obstacles
    - sortie : la nouvelle affectation, le nouveau dico des obstacles
    """
    #print("Choix : VoisinageEnleverUnServeur")
    listeServeursAffectes = []
    
    for serveurId in affectation:
        if affectation[serveurId] != 'x':
            listeServeursAffectes.append(serveurId)
    
    # Si on essaye d'enlever un serveur alors qu'on a deja enlever tous les serveur,
    # on retourne l'affectation courante, i.e. avec aucun serveur affecte
    if listeServeursAffectes == []:
        return affectation, dicoObstacles
    
    serveurSelectionne = random.choice(listeServeursAffectes)
    
    nouvelleAffectation = deepcopy(affectation)
    nouveauDicoObstacles = deepcopy(dicoObstacles)
    
    rangee, slot, pool = affectation[serveurSelectionne]
    
    taille = dicoCaracServeur[serveurSelectionne][0]
        
    #print("serveur, taille")    
    #print(serveurSelectionne,taille)
    
    for i in range(taille):
        nouveauDicoObstacles[str(affectation[serveurSelectionne][0])].remove(slot + i)
        
    nouvelleAffectation[serveurSelectionne] = 'x'
    
##    print("Ancienne affectation")
##    print(affectation)
##    print("Nouvelle affectation")
##    print(nouvelleAffectation)
##
##    print("Ancien dico")
##    print(dicoObstacles)
##    print("Nouveau dico")
##    print(nouveauDicoObstacles)
    
    return nouvelleAffectation, nouveauDicoObstacles
    


def voisinageChangementPool(affectation, carac):
    """
    Genere aleatoirement un voisin possible a partir d'une affectation
    en changeant le pool d'un serveur déjà affecte a un autre pool tire au sort
    - entree : l'affectation courante, les caracteristiques de l'instance
    - sortie : la nouvelle affectation possible
    """
    #print("Choix : voisinageChangementPool")
    listeServeursAffectes = []
    
    for serveurId in affectation:
        if affectation[serveurId] != 'x':
            listeServeursAffectes.append(serveurId)
    
    # Si on essaye de changer le pool d'un serveur alors qu'il n'y a aucun serveur affecte,
    # on retourne l'affectation courante, i.e. avec aucun serveur affecte        
    if listeServeursAffectes == []:
        return affectation
    
    serveurSelectionne = random.choice(listeServeursAffectes)
    #print("serveur,pool")
    #print(serveurSelectionne,affectation[serveurSelectionne][2])
    
    numPoolAlea = random.randint(0, carac['P']-1)
    while numPoolAlea == affectation[serveurSelectionne][2]:
        numPoolAlea = random.randint(0, carac['P']-1)
    
    nouvelleAffectation = deepcopy(affectation)
    
    nouvelleAffectation[serveurSelectionne][2] = numPoolAlea

##    print("Ancienne affectation")
##    print(affectation)
##    print("Nouvelle affectation")
##    print(nouvelleAffectation)
            
    return nouvelleAffectation


def voisinageServeurNonAffecte(affectation, dicoCaracServeur, dicoObstacles, carac):
    """
    Genere aleatoirement un voisin possible a partir d'une affectation
    en placant un serveur non encore affecte sur un emplacement libre
    tire au sort et un pool tire au sort
    - entree : l'affectation courante, la liste des caracteristiques des serveurs 
                (id, taille, capacite), les obstacles et les caracteristiques
                de l'instance
    - sortie : la nouvelle affectation possible et le dico des obstacles possibles
    """
    #print("Choix : voisinageServeurNonAffecte")  
    listeServeursNonAffectes = []
    
    for serveurId in affectation:
        if affectation[serveurId] == 'x':
            listeServeursNonAffectes.append(serveurId)

##    print("Serveurs non affectes")
##    print(listeServeursNonAffectes)
       
###############################################################################
###############################################################################
    if len(listeServeursNonAffectes) == 0:
        #print("Tous les serveurs sont affectes")
        return affectation, dicoObstacles
    
    serveurSelectionne = random.choice(listeServeursNonAffectes)

##    print("serveur choisi")
##    print(serveurSelectionne)
    
    taille = dicoCaracServeur[serveurSelectionne]
            
    # l_m, l'ensemble des slots (r,s) a partir duquel le serveur peut etre localises
    l_m = []
    for i in range(carac["R"]):
        a = outils.genererListe_l_m(dicoObstacles[str(i)], taille, carac["S"], i)
        if not len(a) == 0: 
            l_m += a

    #print("Slots Possibles")
    #print(l_m)

    if len(l_m) == 0:
        #print("aucun endroit dispo")
        return affectation, dicoObstacles
###############################################################################
###############################################################################
#    '''
#    Dans la boucle suivante,
#    On tire un serveur au hasard parmi les serveurs non encore affectes,
#    (rq : s'il n'y a aucun serveur non affecte, on retourne la solution initiale)
#    on cherche toute les positions ou ce serveur peut etre affecte,
#    s'il n'y a aucune position, on retire ce serveur de la liste des serveurs non encore affectes et on reboucle
#    sinon on sort de la boucle
#    '''
#    pasDePositionsTrouvees = True
#    while pasDePositionsTrouvees:
#        if len(listeServeursNonAffectes) == 0:
#            #print("Tous les serveurs sont affectes ou aucune position possible trouvee pour les serveurs non encore affectes")
#            return affectation, dicoObstacles
#        
#        serveurSelectionne = random.choice(listeServeursNonAffectes)
#        taille = dicoCaracServeur[serveurSelectionne]
##        print("serveur choisi")
##        print(serveurSelectionne)
#        
#        # l_m, l'ensemble des slots (r,s) a partir duquel le serveur peut etre localises
#        l_m = []
#        for i in range(carac["R"]):
#            a = genererListe_l_m(dicoObstacles[str(i)], taille, carac["S"], i)
#            if not len(a) == 0: 
#                l_m += a
#    
#        #print("Slots Possibles")
#        #print(l_m)
#        
#        if len(l_m) == 0:
#            listeServeursNonAffectes.remove(serveurSelectionne)
#        else:
#            pasDePositionsTrouvees = False
###############################################################################
###############################################################################

    nouvellePosition = random.choice(l_m)
    
    nouveauPool = random.choice(range(carac["P"]))
    while nouveauPool == affectation[serveurSelectionne][2]:
        nouveauPool = random.choice(range(carac["P"]))
    
##    print("Slots choisi")
##    print(nouvellePosition)
    
    nouvelleAffectation = deepcopy(affectation)
    
    nouvelleAffectation[serveurSelectionne] = [nouvellePosition[0], nouvellePosition[1], nouveauPool]

    nouveauDicoObstacles = deepcopy(dicoObstacles)
    
    for i in range(taille):
        nouveauDicoObstacles[str(nouvellePosition[0])].append(nouvellePosition[1] + i)
        
    nouveauDicoObstacles[str(nouvellePosition[0])].sort()

##    print("Ancienne affectation")
##    print(affectation)
##    print("Nouvelle affectation")
##    print(nouvelleAffectation)
##
##    print("Ancien dico")
##    print(dicoObstacles)
##    print("Nouveau dico")
##    print(nouveauDicoObstacles)
    
    
    return nouvelleAffectation, nouveauDicoObstacles
 

def recuitSimule(nomFichier):
    affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne2(nomFichier)
    temperature = 400 #Il faut jouer ici
    cpt = 0
    nouveauDicoObstacles = dicoObstacles
    RX = affectation
    X = affectation
    
    # dicoCaracServeur["id du serveur"] = [taille du serveur, capacite du serveur]
    dicoCaracServeur = {}
    for serveur in listeServeurs:
        dicoCaracServeur[str(serveur[0])] = [serveur[1], serveur[2]]
        
    print("Score avant descente: ",outils.calculScore(affectation, carac, dicoCaracServeur) )
    
    while(temperature > 0 ):         
        
        Y, nouveauDicoObstacles = unVoisinAffectation2(X,carac,listeServeurs,dicoObstacles)
        scoreY = outils.calculScore(Y,carac,dicoCaracServeur)
        scoreRX = outils.calculScore(RX,carac,dicoCaracServeur)
        scoreX = outils.calculScore(X,carac,dicoCaracServeur)
       # print("ScoreY, ScoreX, ScoreRX")
        #print( scoreY, scoreX, scoreRX)
        
        if  scoreY > scoreRX :
            RX = deepcopy(Y)
            dicoObstacles = deepcopy(nouveauDicoObstacles)
        if scoreY > scoreX :
            X = deepcopy(Y)
            dicoObstacles = deepcopy(nouveauDicoObstacles)
        else: 
            RND = random.random() #Il faut jouer ici
            if( RND <= math.exp( (scoreY - scoreX) / temperature) ):
               # print("Hasard",RND,math.exp( (scoreY - scoreX) / temperature) )
                X = deepcopy(Y)
                dicoObstacles = deepcopy(nouveauDicoObstacles)
        
        #if cpt%10 == 0:
        #    temperature -= 1
        #cpt+=1
       
        temperature -= 1
            
    print("Score apres descente: ",outils.calculScore(RX, carac, dicoCaracServeur) )
    

def unVoisinAffectation(affectation, carac, listeServeurs, dicoObstacles):
    
    nouvelleAffectation = {}
    nouveauDicoObstacles = {}
    nbAlea = random.random()
    
    if nbAlea < 0.2:
       # print"1"
        nouvelleAffectation, nouveauDicoObstacles = voisinageEnleverUnServeur(affectation, listeServeurs, dicoObstacles)
    elif 0.2 <= nbAlea and nbAlea < 0.4:
       # print"2"
        nouvelleAffectation, nouveauDicoObstacles = voisinageServeurNonAffecte(affectation, listeServeurs, dicoObstacles, carac)
    else:
        #print"3"
        nouvelleAffectation = voisinageChangementPool(affectation, carac)
        nouveauDicoObstacles = deepcopy(dicoObstacles)             
            
    return nouvelleAffectation, nouveauDicoObstacles


def unVoisinAffectation2(affectation, carac, listeServeurs, dicoObstacles):
    nouvelleAffectation = {}
    nouveauDicoObstacles = {}
    nbAlea = random.random()

    if nbAlea < 0.33:
       # print"1"
        nouvelleAffectation, nouveauDicoObstacles = voisinageEnleverUnServeur(affectation, listeServeurs, dicoObstacles)
        nouvelleAffectation, nouveauDicoObstacles = voisinageServeurNonAffecte(nouvelleAffectation, listeServeurs, nouveauDicoObstacles, carac)
        
    elif 0.33 <= nbAlea and nbAlea < 0.66:
       # print"2"
        nouvelleAffectation, nouveauDicoObstacles = voisinageServeurNonAffecte(affectation, listeServeurs, dicoObstacles, carac)
        
    else:
        #print"3"
        nouvelleAffectation = voisinageChangementPool(affectation, carac)
        nouvelleAffectation = voisinageChangementPool(nouvelleAffectation, carac)
        nouveauDicoObstacles = deepcopy(dicoObstacles)             
            
    return nouvelleAffectation, nouveauDicoObstacles
    



###############################################################################
# MAIN
###############################################################################
def main():
    nomFichier = "dc.in"
    pourcentage = 20
#    recuitSimule(creeFichierInstancePourcentage(nomFichier,pourcentage))
##    for pourcentage in range(10,110,10):
##        print("pourcentage : ", pourcentage)
##        recuitSimule(creeFichierInstancePourcentage(nomFichier,pourcentage))

#    descenteStochastique(creeFichierInstancePourcentage(nomFichier,pourcentage))
    nouvelleInstance = outils.creeFichierInstancePourcentage(nomFichier,pourcentage)
        
    affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne1(nouvelleInstance)
        
        
###############################################################################
# Tests
###############################################################################             
def testMethodesGloutonnes():
    """
    Test performance methode 1 et 2
    """
    nomFichier = "dc.in"
    for pourcentage in range(10,110,10):
        print("---------------")
        print "pourcentage", pourcentage
        print("---------------")
        nouvelleInstance = outils.creeFichierInstancePourcentage(nomFichier,pourcentage)
        methodeGloutonne1(nouvelleInstance)        
        methodeGloutonne2(nouvelleInstance)

def testDescenteStochastique():
    nomFichier = "dc.in"
    for pourcentage in range(10,110,10):
        print("pourcentage : ", pourcentage)
        startTime = time.time()
        descenteStochastique(outils.creeFichierInstancePourcentage(nomFichier,pourcentage))
        print "duree d'execution : ", time.time() - startTime