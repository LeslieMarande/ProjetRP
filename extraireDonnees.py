# -*- coding: utf-8 -*-

#2 5 1 2 5 : 2 rows of 5 slots each, 1 slot unavailable, 2 pools and 5 servers.
    
def creeFichierInstancePourcentage(nomFichier, pourcentage):         
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
        i = 0
        
        # Enregistre dans le dictionnaire unavailableSlots les slots indisponibles tel que :
        # - cle = numero de la rangee
        # - valeur = liste de numeros de slot qui sont indisponibles
        
        for i in range(0, caracteristics['R']):
            unavailableSlots[str(i)] =  []
        
        i = 0
        while i < caracteristics['U']:
            row, slot = source.readline().split()
            unavailableSlots[str(row)].append(int(slot))
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
            servers.append((serverId, int(size), int(capacity)))
            line = source.readline()
            serverId += 1
            
        # Trie par capacity decroissante
        servers.sort(key = lambda tup : tup[2], reverse = True) 
        source.close()
    
    return caracteristics, unavailableSlots, servers
    
            
def methodeGloutonne(fileName):
    carac, dicoObstacles, listeServeurs = creeStructureDonnees(fileName)
    affectation = {}
    slotTrouve = False     
    
    #Creer le dico
    numPool = 0
    for s in listeServeurs:
        for r in range(carac["R"]):
            numSlot = positionServeurSlot(dicoObstacles[str(r)], s[1], carac["S"])
            if numSlot != None:
                for i in range(s[1]):
                    dicoObstacles[str(r)].append(numSlot + i)
                dicoObstacles[str(r)].sort()
                slotTrouve = True 
                affectation[str(s[0])] = (r, numSlot, numPool ) 
                break
        if slotTrouve == False :
            affectation[str(s[0])] = 'x' 
        
        slotTrouve = False
        if numPool < carac["P"] - 1:
            numPool += 1
        else:
            numPool = 0

    print "affectation finale"
    print affectation
    
    genererFichierSolution(affectation)
        
        
def positionServeurSlot(listeObstacles,capacite,tailleRangee):
    """ retourne le num du premier slot """
    curseurServeur = 0
    curseurObst = 0
    
    if listeObstacles == []:
        if capacite <= tailleRangee - curseurServeur:
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
                elif capacite <= tailleRangee - curseurServeur:
                    return curseurServeur
                else :
                    return None
            
        if capacite <= listeObstacles[curseurObst] - curseurServeur :
            return curseurServeur
            
        curseurServeur = listeObstacles[curseurObst] + 1 
    return None
    
        
            
        
    
###############################################################################
# MAIN
###############################################################################
def main():
    creeFichierInstancePourcentage("petit_dc.in",100)
    methodeGloutonne("petit_dc_100.txt")
#    # Creation d'un tableau d'affectation A pour tester la fonction genererFichierSolution(A)
#    A = []
#    A.append((0, 1, 0))
#    A.append((1, 0, 1))
#    A.append((1, 3, 0))
#    A.append((0, 4, 1))
#    A.append('x')
#
#    genererFichierSolution(A)
    
