# -*- coding: utf-8 -*-

#2 5 1 2 5 2rows of 5 slots each, 1 slot unavailable, 2 pools and 5 servers.
global r
r=0

global p
p=0

global se
se=0

def extraireInfos(nomFichier,pourcentage,param):
    if param == "R":
        extraireInfosRangees(nomFichier,pourcentage)
    elif param == "P":
        extraireInfosPools(nomFichier,pourcentage)
    elif param == "S":
        extraireInfosServeurs(nomFichier,pourcentage)
    else :
        print("Erreur de saisie")


def extraireInfosRangees(nomFichier,pourcentage):
    print("Dans Rangees")
    global r
    n=0
    nbSlotUnavailable = 0
    with open(nomFichier, "r") as s:
        with open("infosRangees"+str(r)+".txt","w") as f:
            r=r+1
            premiereLigne = s.readline()
            f.write(premiereLigne)
            nbSlotUnavailable = premiereLigne.split()[2]

            while(n<int(int(nbSlotUnavailable)*int(pourcentage)/100)):
                n=n+1
                f.write(s.readline())
            f.close()
            s.close()
            print("fin")
    
def extraireInfosPools(nomFichier,pourcentage):
    print("Dans pools")
    global p
    with open(nomFichier, "r") as s:
        with open("infosPool"+str(p)+".txt","w") as f:
            p=p+1
            premiereLigne = s.readline()
            f.write(premiereLigne)
            nbPools = int(int(premiereLigne.split()[3])*int(pourcentage)/100)
            f.write(str(nbPools))
            
            f.close()
            s.close()
            print("fin")
       
def extraireInfosServeurs(nomFichier,pourcentage):
    global se
    k = 0
    nbServeurs = 0
    print("Dans Serveurs")
    with open(nomFichier, "r") as s:
        with open("infosServeurs"+str(se)+".txt","w") as f:
            se = se+1
            premiereLigne = s.readline()
            f.write(premiereLigne)
            nbSlotUnavailable = premiereLigne.split()[2]
            nbServeurs = premiereLigne.split()[-1]
            while(k<int(nbSlotUnavailable)):
                k=k+1
                s.readline()
            k = 0
            while(k+1<int(nbServeurs)*int(pourcentage)/100): #k+1 je crois
                k=k+1
                f.write(s.readline())
            f.close()
            s.close()
            print("fin")   

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

###############################################################################
# MAIN
###############################################################################
def main():
    extraireInfos("dc.in",10,"P")
    
    A = []
    A.append([0, 1, 0])
    A.append([1, 0, 1])
    A.append([1, 3, 0])
    A.append([0, 4, 1])
    A.append(['x'])

