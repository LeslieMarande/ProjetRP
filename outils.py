# -*- coding: utf-8 -*-

from copy import deepcopy
import os


# Instances : Q 0.2.
###############################################################################
def creeFichierInstancePourcentage(nomFichier, pourcentage):     
    """
    Creer dans le repertoire Instances, un nouveau fichier a partir du nom de fichier passe en parametre.
    Le nouveau fichier ne contient qu'un pourcentage des rangees, des slots invalides
    et des serveurs du fichier initial
    - Entree :
        nomFichier, le nom fichier de l'instance initiale
        pourcentage le pourcentage du fichier initial sauvegarde dans le nouveau fichier cree
    - Sortie :
        Le nom du nouveau fichier cree au format txt
    
    """
    if not os.path.isdir("./Instances"):
        os.mkdir("./Instances")
        
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
        
        with open(str("Instances/"+nomFichier.split('.')[0])+'_'+str(pourcentage)+".txt","w") as k:
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
    
    return str("Instances/"+nomFichier.split('.')[0])+'_'+str(pourcentage)+".txt"


# Instances : Q 0.3.
###############################################################################
def genererFichierSolution(A, nomInstance, nomMethode):
    """
    Cree dans le repertoire Resultats, un fichier "Affectation_[nomInstance]_[nomMethode].txt" 
    qui contient la solution du probleme
    - Entree : 
        tableau A contenant l'affectation pour chacun des serveurs m = 0, .., |M| - 1
        sous la forme A[m] = [ar_m, as_m, ap_m], avec :
        ar_m : numero de la rangee ou le serveur est localise
        as_m : numero du premier slot de la rangee ou le serveur est affecte sur z_m slots consecutifs
        ap_m : numero du pool ou le serveur est affecte
        Rq : A[m] = [x] designe le fait que le serveur, m, n'a pas ete affecte
    - Sortie : aucune, la fonction creee le fichier Affectation_[nomInstance].txt en interne
    """
    
    if not os.path.isdir("./Resultats"):
        os.mkdir("./Resultats")
        
    # Ecriture dans le fichier
    f = open("Resultats/Affectation_{0}_{1}.txt".format(nomInstance.split("Instances/")[1].split(".txt")[0], nomMethode), "w")
    cpt = 0
    for k in range(len(A)):
        tup = A[str(k)]
        if tup[0] != 'x':
            f.write("{0} {1} {2} \t \t Server {nb} placed in row {0} at slot {1} and assigned to pool {2}.\n".format(*tup, nb = cpt))
        else:
            f.write("x \t \t \t Server {nb} not allocated.\n".format(nb = cpt))
        cpt += 1
    f.close


###############################################################################
def creeStructureDonnees(fileName):
    """
    Creer plusieurs structures de donnees a partir des information contenu dans le fichier
    - Entree :
        fileName, le nom du fichier duquel on extrait les donnees
    - Sortie :
        carac, dictionnaire de la forme : {'R': nombre de rangees,
                                   'S': nombre de slot par rangee,
                                   'U': nombre de slot inutilisables,
                                   'P': nombre de pools,
                                   'M': nombre de serveurs}
        dicoObstacles, dictionnaire dont les cles sont les numeros de rangee,
            et les valeurs une liste ordonnee des slots initialement indisponibles
            ou qui deviennent indisponibles quand un serveur l'occupe
        listeServeurs, une liste de triplet de la forme : [identifiant du serveur, sa taille, sa capacite]
            triee par ordre decroissant de capacite des serveurs
        dicoRangees, dictionnaire dont les cles sont les numros de rangee
            et les valeurs une liste avec un x si le slot est initialement indisponibles
            ou l'identifiant du serveur si le serveur occupe cette position
    """
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
        # Un element de la liste est un triplet : [identifiant du serveur, sa taille, sa capacite]
        serverId = 0
        listeServeurs = []
        line = source.readline()
        while line != "":
            size, capacity = line.split()
            listeServeurs.append([serverId, int(size), int(capacity)])
            line = source.readline()
            serverId += 1
            
        # Trie par capacite decroissante
        listeServeurs.sort(key = lambda tup : tup[2], reverse = True) 
        source.close()
    
    return carac, dicoObstacles, listeServeurs, dicoRangees


###############################################################################
def positionServeurSlot(listeObstacles,taille,tailleRangee):
    """
    Pour une rangee donnee, retourne le numero du premier slot ou un serveur de taille donnee
    peut se positionner
    - Entree :
        listeObtacles, une liste de numero de slots occupes
        taille, la taille du serveur a placer
        tailleRangee, la taille de la rangee
    - Sortie :
        la premiere position ou peut se mettre le serveur dans cette rangee
    """

    curseurServeur = 0
    curseurObst = 0
    
    # Cas de base, il n'y a aucun obstacle dans la rangee
    if listeObstacles == []:
        if taille <= tailleRangee - curseurServeur:
            return curseurServeur
        else:
            return None

    while curseurServeur < tailleRangee:
        # Tant qu'il y a un obstable sur la position consideree, on incremente
        while(curseurServeur in listeObstacles):
            curseurServeur += 1
        
        # On incremente le curseur d'obstacle pour designer le prochain obstacle
        while( curseurServeur > listeObstacles[curseurObst]):
            curseurObst += 1
            # Cas terminal, le curseur d'obstacle correspond a la fin de la rangee
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


###############################################################################
def donnerPoolAuxServeurs(listeServeurs,carac):
    """
    Selectionne chaque serveur au fur et a mesure pour lui attibuer un numero de pool correspondant
    au pool qui a cet instant donne a la capacite la plus faible.
    - Entree :
        listeServeurs, liste de triplets [identifiant du serveur, taille, capacite],
             triee par ordre decroissant de capacite
        carac, les caracteristique de l'instance
    - Sortie :
        listeServeurs, liste de quadruplet [identifiant du serveur, taille, capacite, numero de pool],
               triee par ordre decroissant de capacite
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

    return listeServeurs


###############################################################################
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
def capaciteGarantie(affectation, numPool, carac, dicoCaracServeur):
    """
    Calcule la capacite garantie du pool i pour l'affectation A, i.e.
    la capacite totale des serveurs du pool en cas de panne d'une rangee
    - entrees : une affectation, un numero de pool,
                les caracteristiques de l'instance et les caracteristiques des serveurs, i.e.
                dicoCaracServeur[id] = [taille, capacite]
    - sortie : la valeur de capacite
    """
    
    # Calcul de la capacite des serveurs d'un pool precis pour chaque rangee
    listeCapaciteParRangee = [0 for i in range(carac["R"])]
    capaciteTotale = 0
    for serveurId, triplet in affectation.iteritems():
        if triplet != 'x':
            if triplet[2] == numPool:
                capacite = dicoCaracServeur[serveurId][1]
                listeCapaciteParRangee[triplet[0]] += capacite
                capaciteTotale += capacite
    
    # Initialisation de la capacite garantie minimale
    gc_i = capaciteTotale - listeCapaciteParRangee[0]
    
    # Calcul de la valeur minimale de la capacite garantie
    # rq : l'initialisation etant faite, on part de 1 et non de zero
    for i in range(1,carac["R"]):
        if capaciteTotale - listeCapaciteParRangee[i] < gc_i:
            gc_i = capaciteTotale - listeCapaciteParRangee[i]
    
    return gc_i


def calculScore(affectation, carac, dicoCaracServeur):
    """
    Calcul le score d'une affectation, i.e. le minimum de la capacite garantie
    pour l'ensemble des pools
    - entrees : une affectation, les caracteristiques de l'instance et les caracteristiques
    des serveurs (id, taille, capacite)
    - sorties : le score de l'affectation
    """
    
    # Initialisation du score minimal
    score = capaciteGarantie(affectation, 0, carac, dicoCaracServeur)
    
    # rq : l'initialisation etant faite, on part de 1 et non de zero
    for p in range(1, carac["P"]):
        tmpScore = capaciteGarantie(affectation, p, carac, dicoCaracServeur)
        if tmpScore < score:
            score = tmpScore
    
    return score


# Affichage
###############################################################################
def afficheAffectation(dicoRangees, carac):
    for r in range(carac['R']):
        print "rangee {} : ".format(r)
        print dicoRangees[str(r)]