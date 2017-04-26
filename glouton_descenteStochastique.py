# -*- coding: utf-8 -*-

#2 5 1 2 5 : 2 rows of 5 slots each, 1 slot unavailable, 2 pools and 5 servers.

import random
import math
from copy import deepcopy
import time
import outils
import voisinage

# Methodes gloutonnes : Q 1.1.
###############################################################################
def methodeGloutonne1(nomFichier):
    """
    Implementation de l'algorithme glouton de la Q 1.1. du sujet
    - Entree :
        nomFichier, nom de l'instance sur laquelle on applique l'algorithme
    - Sortie :
        genere un fichier enregistrant l'affectation, 
        affiche la repartition des serveurs sur les rangees et le score dans la console
        retourne les differentes structure de donnees generees
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
    
    score = outils.calculScore(affectation, carac, dicoCaracServeur)
    print "Score methode gloutonne 1 : ", score
    
    return affectation, carac, listeServeurs, dicoRangees, dicoObstacles
    
# Methodes gloutonnes : Q 1.2.
###############################################################################
def methodeGloutonne2(nomFichier):
    """
    Implementation de notre l'algorithme personnelle glouton de la Q 1.2. du sujet
    - Entree :
        nomFichier, nom de l'instance sur laquelle on applique l'algorithme
    - Sortie :
        genere un fichier enregistrant l'affectation,
        affiche la repartition des serveurs sur les rangees et le score dans la console
        retourne les differentes structure de donnees generees
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
    
    score = outils.calculScore(affectation, carac, dicoCaracServeur)
    print "Score methode gloutonne 2 : ", score
    
    return affectation, carac, listeServeurs, dicoRangees, dicoObstacles


# Meta-heuristique : Q 2.1.
###############################################################################    
def descenteStochastique(nomFichier):
    affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne2(nomFichier)
    cpt = 0
    maxIteration = 5000
    
    # dicoCaracServeur["id du serveur"] = [taille du serveur, capacite du serveur]
    dicoCaracServeur = {}
    for serveur in listeServeurs:
        dicoCaracServeur[str(serveur[0])] = [serveur[1], serveur[2]]
        
    while cpt < maxIteration:
        nouvelleAffectation, nouveauDicoObstacles = voisinage.uneAffectationVoisine(affectation, carac, listeServeurs, dicoObstacles, dicoCaracServeur, 0.33, 0.66)
        if outils.calculScore(nouvelleAffectation, carac, dicoCaracServeur) > outils.calculScore(affectation, carac, dicoCaracServeur):
            affectation = deepcopy(nouvelleAffectation)
            dicoObstacles = deepcopy(nouveauDicoObstacles)
        cpt += 1

    outils.genererFichierSolution(affectation, nomFichier, "descenteStochastique")
    
    print "Score descente stochastique: ", outils.calculScore(affectation, carac, dicoCaracServeur)
    


def recuitSimule(nomFichier):
    affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne2(nomFichier)
    temperature = 5000 #Il faut jouer ici
    cpt = 0
#    nouveauDicoObstacles = dicoObstacles
    RX = deepcopy(affectation)
    X = deepcopy(affectation)
    
    # dicoCaracServeur["id du serveur"] = [taille du serveur, capacite du serveur]
    dicoCaracServeur = {}
    for serveur in listeServeurs:
        dicoCaracServeur[str(serveur[0])] = [serveur[1], serveur[2]]
    
    while(temperature > 0 ):         
        
#        Y, nouveauDicoObstacles = voisinage.uneAffectationVoisine2(X,carac,listeServeurs,dicoObstacles, dicoCaracServeur)
        Y, nouveauDicoObstacles = voisinage.uneAffectationVoisine(X, carac, listeServeurs, dicoObstacles, dicoCaracServeur, 0.33, 0.66)
        scoreY = outils.calculScore(Y,carac,dicoCaracServeur)
        scoreRX = outils.calculScore(RX,carac,dicoCaracServeur)
        scoreX = outils.calculScore(X,carac,dicoCaracServeur)
        print("ScoreY, ScoreX, ScoreRX")
        print( scoreY, scoreX, scoreRX)
        
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
            
    outils.genererFichierSolution(RX, nomFichier, "recuitSimule")
    
    print("Score recuit simule: ",outils.calculScore(RX, carac, dicoCaracServeur) )
    

###############################################################################
# MAIN
###############################################################################
def main():
    nomFichier = "dc.in"
    pourcentage = 20
    
#    startTime = time.time()
#    descenteStochastique(outils.creeFichierInstancePourcentage(nomFichier,pourcentage))
#    print "duree d'execution methode descente stochastique sur {0}% : ".format(pourcentage), time.time() - startTime
    
    startTime = time.time()
    recuitSimule(outils.creeFichierInstancePourcentage(nomFichier,pourcentage))
    print "duree d'execution methode recuit simule sur {0}% : ".format(pourcentage), time.time() - startTime
                                                       
##    for pourcentage in range(10,110,10):
##        print("pourcentage : ", pourcentage)
##        recuitSimule(creeFichierInstancePourcentage(nomFichier,pourcentage))
        
###############################################################################
# Tests
###############################################################################             
def testMethodesGloutonnes():
    """
    Test performance methode 1 et 2
    """
    nomFichier = "dc.in"
    for pourcentage in range(10,110,10):
        print "---------------"
        print "pourcentage", pourcentage
        print "---------------"
        nouvelleInstance = outils.creeFichierInstancePourcentage(nomFichier,pourcentage)
        startTime = time.time()
        affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne1(nouvelleInstance)
        print "Affectation methode gloutonne 1 : "
        outils.afficheAffectation(dicoRangees, carac)
        print "duree d'execution methode gloutonne 1 sur {0}%: ".format(pourcentage), time.time() - startTime
        startTime = time.time()
        affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne2(nouvelleInstance)
        print "Affectation methode gloutonne 2 : "
        outils.afficheAffectation(dicoRangees, carac)
        print "duree d'execution methode gloutonne 2 sur {0}%: ".format(pourcentage), time.time() - startTime


def testDescenteStochastique():
    nomFichier = "dc.in"
    for pourcentage in range(10,110,10):
        print "---------------"
        print "pourcentage : ", pourcentage
        print "---------------"
        startTime = time.time()
        descenteStochastique(outils.creeFichierInstancePourcentage(nomFichier,pourcentage))
        print "duree d'execution : ", time.time() - startTime