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

def main():
    extraireInfos("dc.in",10,"P")
