# -*- coding: utf-8 -*-

#2 5 1 2 5 : 2 rows of 5 slots each, 1 slot unavailable, 2 pools and 5 servers.
import random
from copy import deepcopy
def creeFichierInstancePourcentage(nomFichier, pourcentage):     
    """
    Creation d'un nouveau fichier ayant le pourcentage de rangées, slots invalides et serveurs
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
        print "AFFECTATION", tup
        if tup[0] != 'x':
            f.write("{0} {1} {2} \t Server {nb} placed in row {0} at slot {1} and assigned to pool {2}.\n".format(*tup, nb = cpt))
        else:
            f.write("x \t \t \t Server {nb} not allocated.\n".format(nb = cpt))
        cpt += 1
    f.close



def creeStructureDonnees(fileName):
    with open(fileName, 'r') as source:
        # Enregistre les caracteristiques de l'instance dans la variable caracteristics
        r, s, u, p, m = source.readline().split()
        caracteristics = {'R': int(r), 'S': int(s), 'U': int(u), 'P': int(p), 'M': int(m)}
        unavailableSlots = {}
        dicoRangees = {}
        i = 0
        
        # Enregistre dans le dictionnaire unavailableSlots les slots indisponibles tel que :
        # - cle = numero de la rangee
        # - valeur = liste de numeros de slot qui sont indisponibles
        
        for i in range(0, caracteristics['R']):
            unavailableSlots[str(i)] =  []
            dicoRangees[str(i)]= ['' for i in range(caracteristics['S'])]
        
        i = 0
        while i < caracteristics['U']:
            row, slot = source.readline().split()
            unavailableSlots[str(row)].append(int(slot))
            dicoRangees[str(row)][int(slot)] = 'x'
            i += 1
        
            
        # Trie les liste de numero de slot pour chaque rangee
        for k, v in unavailableSlots.items():
            unavailableSlots[k].sort()
        
        # Enregistre les serveurs dans une liste.
        # Un element de la liste est un triplet : (identifiant du serveur, sa taille, sa capacite)
        serverId = 0
        servers = []
        line = source.readline()
        while line != "":
            size, capacity = line.split()
            servers.append([serverId, int(size), int(capacity)])
            line = source.readline()
            serverId += 1
            
        # Trie par capacity decroissante
        servers.sort(key = lambda tup : tup[2], reverse = True) 
        source.close()
    
    return caracteristics, unavailableSlots, servers, dicoRangees
    
            
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
    print(affectation)
    print(dicoRangees)
    
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

    print "affectation finale"
    print affectation

    print "rangees"
    print dicoRangees
    
    genererFichierSolution(affectation)
    
    return affectation, carac, listeServeurs, dicoRangees, dicoObstacles
        
        
def positionServeurSlot(listeObstacles,taille,tailleRangee):
    """ retourne le num du premier slot où le serveur se positionne"""
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

    #Numero Pools : [numero Range, capacite dans la range de ce pool]  
    print(dicoPoolsCapacite)
    
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

    print "affectation finale"
    print affectation

    print "rangees"
    print dicoRangees
    
    genererFichierSolution(affectation)
    
    return affectation, carac, listeServeurs, dicoRangees, dicoObstacles

    
def donnerPoolAuxServeurs(listeServeurs,carac):
    "Chaque serveur appartient au Pool qui avait le moins de capacité à l'instant donné"
    cpt = 0
    capacitesPools = []
    listeTemp = deepcopy(listeServeurs)
    for a in range(carac['P']):
        capacitesPools.append(0)
    
    while len(listeTemp) > 0 and cpt < len(listeServeurs):
        capacitesPools[capacitesPools.index(min(capacitesPools))] += listeServeurs[cpt][2]
        listeServeurs[cpt].append(capacitesPools.index(min(capacitesPools)))
        
        cpt+=1
        listeTemp.pop(0)
    print("Fin Pool")
    print(listeServeurs)
    return listeServeurs
        
    
def descenteStochastique(fileName):
    affectation, carac, listeServeurs, dicoRangees, dicoObstacles = methodeGloutonne2(fileName)
    listeVoisins = []
    nbAlea = random.random()
    cpt = 0
    maxIteration = 3
    
    while cpt < maxIteration:
        if nbAlea < 0.3:
            listeVoisins = voisinageEnleverUnServeur(affectation)
        elif 0.3 <= nbAlea and nbAlea < 0.6:
            listeVoisins = voisinageServeurNonAffecte(affectation, listeServeurs, dicoObstacles)
        else:
            listeVoisins = voisinageChangementPool(affectation, carac)
        
    """
    if score(listeVoisins[k]) < score(affectation)
        affectation <- listeVoisins[k]
        EN PLUS MAJ DES VAR GLOBALES : dicoRangee
    """
    
    
    return None 

def voisinageEnleverUnServeur(affectation):
    """
    Genere tous les voisins possibles a partir d'une affectation
    en enlevant un serveur de cette affectation
    - entree : l'affectation courante
    - sortie : la liste des voisins de l'affectation courante
    """
    
    listeVoisins = {}
    
    for serveurId in affectation:
        if affectation[serveurId] != 'x':
            tmp = deepcopy(affectation)
            tmp[serveurId] = 'x'
            listeVoisins[serveurId] = tmp
        
    return listeVoisins

def voisinageServeurNonAffecte(affectation, listeServeurs, dicoObstacles):
    """
    Genere tous les voisins possibles a partir d'une affectation
    en placant un serveur non encore affecte sur un emplacement libre
    tire au sort et un pooltire au sort
    - entree : l'affectation courante, la liste des caracteristiques des serveurs 
                (taille, capacite)
    - sortie : la liste des voisins de l'affectation courante
    """
        
    listeVoisins = {}
    
    for serveurId in affectation:
        if affectation[serveurId] == 'x':
            
            for serveur in listeServeurs:
                if serveurId == str(serveur[0]):
                    taille = serveur[1]
                    break

            # l_m, l'ensemble des slots (r,s) a partir duquel le serveur peut etre localises
            l_m = []
            
    

def voisinageChangementPool(affectation, carac):
    """
    Genere tous les voisins possibles a partir d'une affectation
    en changeant le pool d'un serveur déjà affecte a un autre pool tire au sort
    - entree : l'affectation courante
    - sortie : la liste des voisins de l'affectation courante
    """
    
    listeVoisins = {}
    
    for serveurId in affectation:
        if affectation[serveurId] != 'x':
            tmp = deepcopy(affectation)
            
            nbPoolAlea = random.randint(0, carac['P'])
            while nbPoolAlea == affectation[serveurId][2]:
                nbPoolAlea = random.randint(0, carac['P'])
            
            tmp[serveurId][2] = nbPoolAlea
            listeVoisins[serveurId].append(tmp)
        
    return listeVoisins
  
def genererListe_l_m(listeObstacles,taille,tailleRangee, rangeeId):
    """ retourne le num du premier slot où le serveur se positionne"""
    curseurServeur = 0
    curseurObst = 0
    liste_l_m = []
    
    if listeObstacles == []:
        for i in range(tailleRangee - taille + 1):
            liste_l_m.append((i, rangeeId))
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
                        liste_l_m.append((i, rangeeId))
                    return liste_l_m
                else :
                    return liste_l_m
            
        if taille <= listeObstacles[curseurObst] - curseurServeur :
            for i in range(curseurServeur, listeObstacles[curseurObst] - taille + 1):
                liste_l_m.append((i, rangeeId))
            
        curseurServeur = listeObstacles[curseurObst] + 1 
    return liste_l_m

###############################################################################
# MAIN
###############################################################################
def main():
#    methodeGloutonne2(creeFichierInstancePourcentage("dc.in",10))
#    # Creation d'un tableau d'affectation A pour tester la fonction genererFichierSolution(A)
#    A = []
#    A.append((0, 1, 0))
#    A.append((1, 0, 1))
#    A.append((1, 3, 0))
#    A.append((0, 4, 1))
#    A.append('x')
#
#    genererFichierSolution(A)
    
