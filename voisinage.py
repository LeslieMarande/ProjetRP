# -*- coding: utf-8 -*-

import random
from copy import deepcopy
import outils

def voisinageEnleverUnServeur(affectation, dicoCaracServeur, dicoObstacles):
    """
    Genere aleatoirement un voisin possible a partir d'une affectation
    en enlevant un serveur de cette affectation
    - entree : l'affectation courante, la liste des caracteristiques des serveurs 
                (id, taille, capacite), les obstacles
    - sortie : la nouvelle affectation, le nouveau dico des obstacles
    """
#    print "Choix : voisinageEnleverUnServeur"
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
    
#    print "dicoObstacles"
#    print dicoObstacles
#    print "serveurSelectionne", serveurSelectionne
#    print "rangee, slot, pool, taille"
#    print rangee, slot, pool, taille
    
    for i in range(taille):
        nouveauDicoObstacles[str(rangee)].remove(slot + i)
        
    nouvelleAffectation[serveurSelectionne] = 'x'
    
#    print("Ancienne affectation")
#    print(affectation)
#    print("Nouvelle affectation")
#    print(nouvelleAffectation)
#
#    print("Ancien dico")
#    print(dicoObstacles)
#    print("Nouveau dico")
#    print(nouveauDicoObstacles)
    
    return nouvelleAffectation, nouveauDicoObstacles
    


def voisinageChangementPool(affectation, carac):
    """
    Genere aleatoirement un voisin possible a partir d'une affectation
    en changeant le pool d'un serveur déjà affecte a un autre pool tire au sort
    - entree : l'affectation courante, les caracteristiques de l'instance
    - sortie : la nouvelle affectation possible
    """
#    print("Choix : voisinageChangementPool")
    listeServeursAffectes = []
    
    for serveurId in affectation:
        if affectation[serveurId] != 'x':
            listeServeursAffectes.append(serveurId)
    
    # Si on essaye de changer le pool d'un serveur alors qu'il n'y a aucun serveur affecte,
    # on retourne l'affectation courante, i.e. avec aucun serveur affecte        
    if listeServeursAffectes == []:
        return affectation
    
    serveurSelectionne = random.choice(listeServeursAffectes)
#    print("serveur,pool")
#    print(serveurSelectionne,affectation[serveurSelectionne][2])
    
    numPoolAlea = random.randint(0, carac['P']-1)
    while numPoolAlea == affectation[serveurSelectionne][2]:
        numPoolAlea = random.randint(0, carac['P']-1)
    
    nouvelleAffectation = deepcopy(affectation)
    
    nouvelleAffectation[serveurSelectionne][2] = numPoolAlea

#    print("Ancienne affectation")
#    print(affectation)
#    print("Nouvelle affectation")
#    print(nouvelleAffectation)
            
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
#    print("Choix : voisinageServeurNonAffecte")
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

#    print("serveur choisi")
#    print(serveurSelectionne)
    
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
    
#    print("Slots choisi")
#    print(nouvellePosition)
    
    nouvelleAffectation = deepcopy(affectation)
    
    nouvelleAffectation[serveurSelectionne] = [nouvellePosition[0], nouvellePosition[1], nouveauPool]

    nouveauDicoObstacles = deepcopy(dicoObstacles)
    
    for i in range(taille):
        nouveauDicoObstacles[str(nouvellePosition[0])].append(nouvellePosition[1] + i)
        
    nouveauDicoObstacles[str(nouvellePosition[0])].sort()

#    print("Ancienne affectation")
#    print(affectation)
#    print("Nouvelle affectation")
#    print(nouvelleAffectation)
#
#    print("Ancien dico")
#    print(dicoObstacles)
#    print("Nouveau dico")
#    print(nouveauDicoObstacles)
    
    
    return nouvelleAffectation, nouveauDicoObstacles

def uneAffectationVoisine(affectation, carac, listeServeurs, dicoObstacles, dicoCaracServeur, seuil1, seuil2):
    
    nouvelleAffectation = {}
    nouveauDicoObstacles = {}
    nbAlea = random.random()
    
    if nbAlea < seuil1: #0.2
        nouvelleAffectation, nouveauDicoObstacles = voisinageEnleverUnServeur(affectation, dicoCaracServeur, dicoObstacles)
    elif seuil1 <= nbAlea and nbAlea < seuil2: # 0.2 et 0.4
        nouvelleAffectation, nouveauDicoObstacles = voisinageServeurNonAffecte(affectation, dicoCaracServeur, dicoObstacles, carac)
    else:
        nouvelleAffectation = voisinageChangementPool(affectation, carac)
        nouveauDicoObstacles = deepcopy(dicoObstacles)
                
    return nouvelleAffectation, nouveauDicoObstacles

def uneAffectationVoisine2(affectation, carac, listeServeurs, dicoObstacles, dicoCaracServeur):
    nouvelleAffectation = {}
    nouveauDicoObstacles = {}
    nbAlea = random.random()

    if nbAlea < 0.33:
       # print"1"
        nouvelleAffectation, nouveauDicoObstacles = voisinageEnleverUnServeur(affectation, dicoCaracServeur, dicoObstacles)
        nouvelleAffectation, nouveauDicoObstacles = voisinageServeurNonAffecte(nouvelleAffectation, dicoCaracServeur, nouveauDicoObstacles, carac)
        
    elif 0.33 <= nbAlea and nbAlea < 0.66:
       # print"2"
        nouvelleAffectation, nouveauDicoObstacles = voisinageServeurNonAffecte(affectation, dicoCaracServeur, dicoObstacles, carac)
        
    else:
        #print"3"
        nouvelleAffectation = voisinageChangementPool(affectation, carac)
        nouvelleAffectation = voisinageChangementPool(nouvelleAffectation, carac)
        nouveauDicoObstacles = deepcopy(dicoObstacles)             
            
    return nouvelleAffectation, nouveauDicoObstacles