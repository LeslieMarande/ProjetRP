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
        
        with open(str(nomFichier)+'_'+str(pourcentage)+".txt","w") as k:
            k.write(premiereLigneBis+'\n')
            with open("temp.txt", "r") as f:
                k.write(f.read())
                f.close()
            n=0
            while(n+1<premiereLigne[4]):
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
    for line in A:
        if line[0] != 'x':
            f.write("{0} {1} {2} \t Server {nb} placed in row {0} at slot {1} and assigned to pool {2}.\n".format(*line, nb = cpt))
        else:
            f.write("x \t \t Server {nb} not allocated.\n".format(nb = cpt))
        cpt += 1
    f.close  



def methodeGloutonne(fileName):
    with open(fileName, 'r') as source:
        # Enregistre les caracteristiques de l'instance dans la variables caracteristics
        r, s, u, p, m = source.readline().split()
        caracteristics = {'R': r, 'S': s, 'U': u, 'P': p, 'M': m}
        unavailableSlots = []
        i = 0
        
        
        # Enregistre dans le dictionnaire unavailableSlots les slots indisponibles tel que :
        # - cle = numero de la rangee
        # - valeur = liste de numeros de slot qui sont indisponibles
        
        unavailableSlots = {str(i): [] for i in range(0, caracteristics['R'])}
        while i < caracteristics['U']:
            row, slot = source.readline().split()
            unavailableSlots[str(row)].append(int(slot))
            i += 1
            
        # Trie les liste de numero de slot pour chaque rangee
        for k, v in unavailableSlots.items():
            unavailableSlots[k] = value.sort()
        
        # Enregistre les serveurs dans une liste.
        # Un element de la liste est un triplet : (identifiant du serveur, sa taille, sa capacite)
        serverId = 0
        servers = []
        line = source.readline()
        while line != "":
            size, capacity = line.split()
            serverId += 1
            servers.append(serverId, int(size), int(capacity))
            line = source.readline()
            
        # Trie par capacity decroissante
        servers.sort(key = lambda tup : tup[2], reverse = True) 
        source.close()
    
    # Debut de l'algorithme glouton pour determiner l'affectation    
    affectation = {}
    row = 0
    # Pour chaque row, on attribut une position
    positionsList = [0 for i in range(0, caracteristics['S'])]
    # compteur
    unavailableSlotsCountersList = [0 for i in range(0, caracteristics['S'])]
    
            
def affecterServeurs(listeServeurs, rangees):
    #Creer le dico
    for s in listeServeurs:
        for r in rangees:
            solution = rangeeEtPos(capaciteS, listeObstacles)
            if solution != None:
                #Mettre à jour listeObstacles de cette rangee
                #Remplir Affection
                break
            #Si je suis à la derniere rangee mettre 'x' dans affectation
            

def rangeeEtPos(capacite, listeObstacles):
    pos = 0
    #Tant que jarrive pas à caser mon serveur et que j'ai un Obstacle
            while(pos in listeObstacles):
            pos = pos + 1
        #comparer distance entre pos et prochain obstacle 
        #return   
    #Place entre ma position et le bord?
    #retourner None
            
        
    
###############################################################################
# MAIN
###############################################################################
def main():
    creeFichierInstancePourcentage("dc.in",10)
    
    # Creation d'un tableau d'affectation A pour tester la fonction genererFichierSolution(A)
    A = []
    A.append([0, 1, 0])
    A.append([1, 0, 1])
    A.append([1, 3, 0])
    A.append([0, 4, 1])
    A.append(['x'])

    genererFichierSolution(A)
    
