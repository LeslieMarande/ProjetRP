# -*- coding: utf-8 -*-

#2 5 1 2 5 : 2 rows of 5 slots each, 1 slot unavailable, 2 pools and 5 servers.

import random
import math
from copy import deepcopy

# Instances : Q 0.2.
###############################################################################
def creeFichierInstancePourcentage(nomFichier, pourcentage):     
    """
    Creation d'un nouveau fichier ayant le pourcentage de rangees,
    slots invalides et serveurs
    """
    
    n = 0
    cpt = 0
    with open(nomFichier, "r") as s:
        with open("temp.txt", "w") as f:
            premiereLigne = s.readline().split()
            nbRangees = int(int(premiereLigne[0])*int(pourcentage)/100)
            premiereLigne[0] = int(nbRangees)
            premiereLigne[3] = int(int(premiereLigne[3])*int(pourcentage)/100)
            premiereLigne[4] = int(int(premiereLigne[4])*int(pourcentage)/100)
            while(n<int(premiereLigne[2])):
                n=n+1
                ligne = s.readline()
                ligne1 = ligne.split()
                if(int(ligne1[0])<nbRangees):
                    f.write(ligne)
                    cpt = cpt+1
                    
            premiereLigne[2] = cpt
            premiereLigneBis = map(str, premiereLigne)    
            premiereLigneBis = ' '.join(premiereLigneBis) 
            f.close()
        
        with open(str(nomFichier.split('.')[0])+'_'+str(pourcentage)+".txt","w") as k:
            k.write(premiereLigneBis+'\n')
            with open("temp.txt", "r") as f:
                k.write(f.read())
                f.close()
            n=0
            while(n<premiereLigne[4]):
                n=n+1
                k.write(s.readline())
            
            k.close()
            s.close()
    
    return str(nomFichier.split('.')[0])+'_'+str(pourcentage)+".txt"

# Instances : Q 0.3.
###############################################################################
def genererFichierSolution(A):
    """
    Cree un fichier "Affectation.txt" qui contient la solution du probleme
    - entree : tableau A contenant l'affectation pour chacun des serveurs m = 0, .., |M| - 1
    sous la forme A[m] = [ar_m, as_m, ap_m], avec :
        ar_m : numero de la rangee ou le serveur est localise
        as_m : numero du premier slot de la rangee ou le serveur est affecte sur z_m slots consecutifs
        ap_m : numero du pool ou le serveur est affecte
    Rq : A[m] = [x] designe le fait que le serveur, m, n'a pas ete affecte
    - sortie : aucune, la fonction creee le fichier affectation.txten interne
    """
    
    # Ecriture dans le fichier
    f = open("Affectation.txt", "w")
    cpt = 0
    for k in range(len(A)):
        tup = A[str(k)]
        if tup[0] != 'x':
            f.write("{0} {1} {2} \t Server {nb} placed in row {0} at slot {1} and assigned to pool {2}.\n".format(*tup, nb = cpt))
        else:
            f.write("x \t \t \t Server {nb} not allocated.\n".format(nb = cpt))
        cpt += 1
    f.close


# Methodes gloutonnes : Q 1.1.
###############################################################################
def creeStructureDonnees(fileName):
    with open(fileName, 'r') as source:
        # Enregistre les caracteristiques de l'instance dans la variable carac
        r, s, u, p, m = source.readline().split()
        carac = {'R': int(r), 'S': int(s), 'U': int(u), 'P': int(p), 'M': int(m)}
        dicoObstacles = {}
        dicoRangees = {}
        
        # Enregistre dans le dictionnaire dicoObstacles les slots indisponibles tel que :
        # - cle = numero de la rangee
        # - valeur = liste de numeros de slot qui sont indisponibles
        
        for i in range(0, carac['R']):
            dicoObstacles[str(i)] =  []
            dicoRangees[str(i)]= ['' for j in range(carac['S'])]
        
        i = 0
        while i < carac['U']:
            row, slot = source.readline().split()
            dicoObstacles[str(row)].append(int(slot))
            dicoRangees[str(row)][int(slot)] = 'x'
            i += 1
        
            
        # Trie les liste de numero de slot pour chaque rangee
        for k, v in dicoObstacles.items():
            dicoObstacles[k].sort()
        
        # Enregistre les serveurs dans une liste.
        # Un element de la liste est un triplet : (identifiant du serveur, sa taille, sa capacite)
        serverId = 0
        listeServeurs = []
        line = source.readline()
        while line != "":
            size, capacity = line.split()
            listeServeurs.append([serverId, int(size), int(capacity)])
            line = source.readline()
            serverId += 1
            
        # Trie par capacity decroissante
        listeServeurs.sort(key = lambda tup : tup[2], reverse = True) 
        source.close()
    
    return carac, dicoObstacles, listeServeurs, dicoRangees
    
            
def methodeGloutonne1(fileName):
    carac, dicoObstacles, listeServeurs, dicoRangees = creeStructureDonnees(fileName)
    affectation = {}
    slotTrouve = False    
    
    
    #Creer affectation
    for s in listeServeurs:
        for r in range(carac["R"]):
            numSlot = positionServeurSlot(dicoObstacles[str(r)], s[1], carac["S"])
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
    numPool = 0 
    for s in dicoRangees['0']:
        if not s == 'x':
            valTemp = s
            affectation[s].append(numPool)
            numPool +=1
            break
        
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

#    print "affectation finale"
#    print affectation

#    print "rangees"
#    print dicoRangees
    
    genererFichierSolution(affectation)
    
    return affectation, carac, listeServeurs, dicoRangees, dicoObstacles
        
        


def positionServeurSlot(listeObstacles,taille,tailleRangee):
    """ Pour une rangee, retourne le num du premier slot où le serveur se positionne"""

    curseurServeur = 0
    curseurObst = 0
    
    if listeObstacles == []:
        if taille <= tailleRangee - curseurServeur:
            return curseurServeur
        else:
            return None

    while curseurServeur < tailleRangee:
        while(curseurServeur in listeObstacles):
            curseurServeur += 1
        
        while( curseurServeur > listeObstacles[curseurObst]):
            curseurObst += 1
            if curseurObst >= len(listeObstacles):
                if curseurServeur >= tailleRangee:
                    return None
                elif taille <= tailleRangee - curseurServeur:
                    return curseurServeur
                else :
                    return None
            
        if taille <= listeObstacles[curseurObst] - curseurServeur :
            return curseurServeur
            
        curseurServeur = listeObstacles[curseurObst] + 1 
    return None
    
    
# Methodes gloutonnes : Q 1.2.
###############################################################################
def methodeGloutonne2(fileName):
    carac, dicoObstacles, listeServeurs, dicoRangees = creeStructureDonnees(fileName)
    listeServeurs = donnerPoolAuxServeurs(listeServeurs,carac)
    dicoPoolsCapacite = {}
    affectation = {}
    slotTrouve = False   
    
    for i in range(0, carac['P']):
            dicoPoolsCapacite[str(i)] =  []
            for j in range(0, carac['R']):
                dicoPoolsCapacite[str(i)].append([j,0])
    #Numero Pool : [numero Range, capacite dans la range de ce pool]                      

    for s in listeServeurs :
        for r in dicoPoolsCapacite[str(s[3])] :
            numSlot = positionServeurSlot((dicoObstacles[str(r[0])]), s[1], carac["S"])
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

#    print "affectation finale"
#    print affectation

#    print "rangees"
#    print dicoRangees
    
    genererFichierSolution(affectation)
    
    return affectation, carac, listeServeurs, dicoRangees, dicoObstacles

    
def donnerPoolAuxServeurs(listeServeurs,carac):
    """
    Chaque serveur appartient au Pool qui avait le moins de capacité à l'instant donné
    """
    cpt = 0
    capacitesPools = []
    listeTemp = deepcopy(listeServeurs)
    for a in range(carac['P']):
        capacitesPools.append(0)
    
    while len(listeTemp) > 0 and cpt < len(listeServeurs):
        listeServeurs[cpt].append(capacitesPools.index(min(capacitesPools)))
        capacitesPools[capacitesPools.index(min(capacitesPools))] += listeServeurs[cpt][2]
        cpt+=1
        listeTemp.pop(0)

#    print("Fin Pool")
#    print(listeServeurs)

    return listeServeurs
        
# Meta-heuristique : Q 2.1.
###############################################################################    
def descenteStochastique(fileName):
    affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne2(fileName)
    nouvelleAffectation = {}
    nouveauDicoObstacles = {}
    nbAlea = random.random()
    cpt = 0
    maxIteration = 400

    print("Score avant descente: ",calculScore(affectation, carac, listeServeurs)[0] )
    
    while cpt < maxIteration:
        if nbAlea < 0.3:
            nouvelleAffectation, nouveauDicoObstacles = voisinageEnleverUnServeur(affectation, listeServeurs, dicoObstacles)
        elif 0.3 <= nbAlea and nbAlea < 0.6:
            nouvelleAffectation, nouveauDicoObstacles = voisinageServeurNonAffecte(affectation, listeServeurs, dicoObstacles, carac)
        else:
            nouvelleAffectation = voisinageChangementPool(affectation, carac)
            nouveauDicoObstacles = deepcopy(dicoObstacles)   
        nbAlea = random.random()
        cpt+=1
       # print("Nouveau score",calculScore(nouvelleAffectation, carac, listeServeurs)[0] )
        if calculScore(nouvelleAffectation, carac, listeServeurs)[0] >= calculScore(affectation, carac, listeServeurs)[0]:
        #    print("BETTER")
            affectation = deepcopy(nouvelleAffectation)
            dicoObstacles = deepcopy(nouveauDicoObstacles)
        
##        if cpt %4 == 0:
##            if calculScore(nouvelleAffectation, carac, listeServeurs)[0] >= calculScore(bestAffectation, carac, listeServeurs)[0]:
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
            


        
    print("Score final: ", calculScore(affectation, carac, listeServeurs)[0])
    
    
    return None 


def voisinageEnleverUnServeur(affectation, listeServeurs, dicoObstacles):
    """
    Genere tous les voisins possibles a partir d'une affectation
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
        
    serveurSelectionne = random.choice(listeServeursAffectes)
    
    nouvelleAffectation = deepcopy(affectation)
    nouveauDicoObstacles = deepcopy(dicoObstacles)
    
    rangee, slot, pool = affectation[serveurSelectionne]
    
    for serveur in listeServeurs:
        if serveurSelectionne == str(serveur[0]):
            taille = serveur[1]
            break
        
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
    Genere tous les voisins possibles a partir d'une affectation
    en changeant le pool d'un serveur déjà affecte a un autre pool tire au sort
    - entree : l'affectation courante, les caracteristiques de l'instance
    - sortie : la nouvelle affectation possible
    """
    #print("Choix : voisinageChangementPool")
    listeServeursAffectes = []
    
    for serveurId in affectation:
        if affectation[serveurId] != 'x':
            listeServeursAffectes.append(serveurId)
            
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


def voisinageServeurNonAffecte(affectation, listeServeurs, dicoObstacles, carac):
    """
    Genere tous les voisins possibles a partir d'une affectation
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
    
    if len(listeServeursNonAffectes) == 0:
        #print("Tous les serveurs sont affectes")
        return affectation, dicoObstacles
    
    serveurSelectionne = random.choice(listeServeursNonAffectes)

##    print("serveur choisi")
##    print(serveurSelectionne)
    
    for serveur in listeServeurs:
        if serveurSelectionne == str(serveur[0]):
            taille = serveur[1]
            break
            
    # l_m, l'ensemble des slots (r,s) a partir duquel le serveur peut etre localises
    l_m = []
    for i in range(carac["R"]):
        a = genererListe_l_m(dicoObstacles[str(i)], taille, carac["S"], i)
        if not len(a) == 0: 
            l_m += a

    #print("Slots Possibles")
    #print(l_m)

    if len(l_m) == 0:
        #print("aucun endroit dispo")
        return affectation, dicoObstacles
    
    nouvellePosition = random.choice(l_m)    
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
 

def genererListe_l_m(listeObstacles,taille,tailleRangee, rangeeId):
    """
    retourne la liste de slots ou le serveur peut se positionner sur une rangee specifique
    - entrees : la liste d'obstacle de la rangee, la taille du serveur,
                la taille de la rangee et l'ID de la rangee
    - sortie : liste de couples (numero de la rangee, numero de slot)
    """
    curseurServeur = 0
    curseurObst = 0
    liste_l_m = []
    
    if listeObstacles == []:
        for i in range(tailleRangee - taille + 1):
            liste_l_m.append((rangeeId, i))
        return liste_l_m

    while curseurServeur < tailleRangee:
        while(curseurServeur in listeObstacles):
            curseurServeur += 1
        
        while( curseurServeur > listeObstacles[curseurObst]):
            curseurObst += 1
            if curseurObst >= len(listeObstacles):
                if curseurServeur >= tailleRangee:
                    return liste_l_m
                elif taille <= tailleRangee - curseurServeur:
                    for i in range(curseurServeur, tailleRangee - taille + 1):
                        liste_l_m.append((rangeeId, i))
                    return liste_l_m
                else :
                    return liste_l_m
            
        if taille <= listeObstacles[curseurObst] - curseurServeur :
            for i in range(curseurServeur, listeObstacles[curseurObst] - taille + 1):
                liste_l_m.append((rangeeId, i))
            
        curseurServeur = listeObstacles[curseurObst] + 1 
    return liste_l_m

# Score d'une solution
###############################################################################
def capaciteGarantie(affectation, numPool, carac, listeServeurs):
    """
    Calcule la capacite garantie du pool i pour l'affectation A, i.e.
    la capacite totale des serveurs du pool en cas de panne d'une rangee
    - entrees : une affectation, un numero de pool,
                les caracteristiques de l'instance et les caracteristiques des serveurs
                (id, taille, capacite)
    - sortie : la valeur de capacite et le numero de la rangee qui minimise cette valeur
    """
    
    # Calcul de la capacite des serveurs d'un pool precis pour chaque rangee
    listeCapaciteParRangee = [0 for i in range(carac["R"])]
    capaciteTotale = 0
    
    for serveurId, triplet in affectation.iteritems():
        if triplet != 'x':
            if triplet[2] == numPool:
                for s in listeServeurs:
                    if serveurId == str(s[0]):
                        capacite = s[2]
                        break
                listeCapaciteParRangee[triplet[0]] += capacite
                capaciteTotale += capacite
    
    # Initialisation
    gc_i = capaciteTotale - listeCapaciteParRangee[0]
    idRangee = 0
    
    # Calcul de la valeur minimale de la capacite garantie
    # rq : l'initialisation etant faite, on part de 1 et non de zero
    for i in range(1,carac["R"]):
        if capaciteTotale - listeCapaciteParRangee[i] < gc_i:
            gc_i = capaciteTotale - listeCapaciteParRangee[i]
            idRangee = i
    
    return gc_i, idRangee


def calculScore(affectation, carac, listeServeurs):
    """
    Calcul le score d'une affectation, i.e. le minimum de la capacite garantie
    pour l'ensemble des pools
    - entrees : une affectation, les caracteristiques de l'instance et les caracteristiques
    des serveurs (id, taille, capacite)
    - sorties : le score de l'affectation, la rangee et le pool qui ont minimisees
                ce score
    """
    score, idRangee = capaciteGarantie(affectation, 0, carac, listeServeurs)
    numPool = 0
    for p in range(1, carac["P"]):
        tmpScore, tmpIdRangee = capaciteGarantie(affectation, p, carac, listeServeurs)
        if tmpScore < score:
            score, idRangee = tmpScore, tmpIdRangee
            numPool = p
    
    return score, idRangee, numPool

def recuitSimule(fileName):
    affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne2(fileName)
    temperature = 400 #Il faut jouer ici
    cpt = 0
    nouveauDicoObstacles = dicoObstacles
    RX = affectation
    X = affectation
    print("Score avant descente: ",calculScore(affectation, carac, listeServeurs)[0] )
    
    while(temperature > 0 ):         
        
        Y, nouveauDicoObstacles = unVoisinAffectation2(X,carac,listeServeurs,dicoObstacles)
        scoreY = calculScore(Y,carac,listeServeurs)[0]
        scoreRX = calculScore(RX,carac,listeServeurs)[0]
        scoreX = calculScore(X,carac,listeServeurs)[0]
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
            
    print("Score apres descente: ",calculScore(RX, carac, listeServeurs)[0] )
    

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
    pourcentage = 30
    recuitSimule(creeFichierInstancePourcentage(nomFichier,pourcentage))
##    for pourcentage in range(10,110,10):
##        print("pourcentage : ", pourcentage)
##        recuitSimule(creeFichierInstancePourcentage(nomFichier,pourcentage))
        
        
        
###############################################################################
# Tests
###############################################################################             
def testAllPourcentage():
    """
    Test performance methode 1 et 2
    """
    nomFichier = "dc.in"
    for pourcentage in range(10,110,10):
        print("--------")
        print "pourcentage", pourcentage
        print("--------")
        print "methode gloutonne 1"
        affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne1(creeFichierInstancePourcentage(nomFichier,pourcentage))
        score, idRangee, numPool = calculScore(affectation, carac, listeServeurs)
        print "END"
        print score, idRangee, numPool
        
        print "methode gloutonne 2"
        affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne2(creeFichierInstancePourcentage(nomFichier,pourcentage))
        score, idRangee, numPool = calculScore(affectation, carac, listeServeurs)
        print "Score : ", score

def testStochastique():
    nomFichier = "dc.in"
    #pourcentage = 60
    for pourcentage in range(10,110,10):
        print("pourcentage : ", pourcentage)
        descenteStochastique(creeFichierInstancePourcentage(nomFichier,pourcentage))


    
