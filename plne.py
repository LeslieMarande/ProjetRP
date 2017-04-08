# -*- coding: utf-8 -*-
import gurobipy as g
import extraireDonnees

""" Contraintes """
#1 Chaque slot contient au plus un serveur
#2 Aucun serveur sur slot indispo
#3 Un serveur a autant de slot que sa taille et ils sont consecutifs ou pas affecte (meme rangee et pas depasser taille)
#4 Un serveur affecte apparait au plus une fois
#5 Un serveur affecte appartient a exactement un pool

""" Variables """
# r : id rangee

model = g.Model("RP-OptimizeDataCenter")
model.setParam( 'OutputFlag', False) #Desactive  le mode verbeux
model.setParam('TimeLimit', 2*60) #Limite de temps pour la resolution 

def creerVariables(fileName):
    """
    Creer le ictionnaire :
    z_mrsi["id du serveur"]["num rangee"]["num slot"]["num pool"]
    k_rs[(idRangee,idSlot)]=[idServeur1,Idserveur2,...]
    """
    z_mrsi = {}
    carac, dicoObstacles, listeServeurs, dicoRangees = extraireDonnees.creeStructureDonnees(fileName)
    
    dicoServeurCarac = {}
    for serveur in listeServeurs:
        dicoServeurCarac[str(serveur[0])] = [serveur[1], serveur[2]]
        
    k_rs = {}
    for r in range(carac['R']):
        for s in range(carac['S']):
            k_rs[(r,s)] = []
    
    for m in range(carac['M']):
        
        z_mrsi[str(m)] = {}
        
        for r in range(carac['R']):
            
            z_mrsi[str(m)][str(r)] = {}
            
            l_m = extraireDonnees.genererListe_l_m(dicoObstacles[str(r)],dicoServeurCarac[str(m)][0], carac["S"], r)
            
            for couple in l_m:
                
                k_rs[couple].append(m)
                
                z_mrsi[str(m)][str(r)][str(couple[1])] = {}
                
                for i in range(carac['P']):
                    z_mrsi[str(m)][str(r)][str(couple[1])][str(i)] = model.addVar(vtype = g.GRB.BINARY, lb=0, name="z_mrsi {0} {1} {2} {3}" .format(m, r, couple[1], i))
    
    model.update()

    return z_mrsi, dicoServeurCarac, k_rs

def contraintes(z_mrsi, dicoServeurCarac, k_rs):
    """
    contrainte 1 : un serveur par slot (  un marqueur max par slot + pas de chevauchement de serveurs)
    """
    
    for key, value in k_rs.iteritems():
        somme = 0
        if not len(value) == 0:
            for serveur in value:
                tailleServeur = dicoServeurCarac[str(serveur)][0]
                for i in range(0,tailleServeur):
                    if str(key[1]+i) in z_mrsi[str(serveur)][str(key[0])]:
                        for a,b in z_mrsi[str(serveur)][str(key[0])][str(key[1]+i)].iteritems():
                            somme += b
            print(somme, " <=  1 ") 
            model.addConstr(somme <= 1, "Contrainte 1 : un marqueur max par slot %d %d" % (key[0], key[1]))
 
        
    

def main():
    nomFichier = "petiteInstance.in"
    nomFichierInstance = extraireDonnees.creeFichierInstancePourcentage(nomFichier,100) #petit_dc_100.txt
    z,dicoServeurCarac,k_rs = creerVariables(nomFichierInstance)
    contraintes(z,dicoServeurCarac,k_rs)
#    print z
    
