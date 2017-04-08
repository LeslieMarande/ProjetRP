# -*- coding: utf-8 -*-
import extraireDonnees
from gurobipy import *

""" Contraintes """
#1 Chaque slot contient au plus un serveur
#2 Aucun serveur sur slot indispo
#3 Un serveur a autant de slot que sa taille et ils sont consecutifs ou pas affecte (meme rangee et pas depasser taille)
#4 Un serveur affecte apparait au plus une fois
#5 Un serveur affecte appartient a exactement un pool

""" Variables """
# r : id rangee




m = Model("RP-OptimizeDataCenter")
m.setParam( 'OutputFlag', False) #Desactive  le mode verbeux
m.setParam('TimeLimit', 2*60) #Limite de temps pour la resolution 

def creerVariables(fileName):
    """
    """
    z_mrsi = {}
    carac, dicoObstacles, listeServeurs, dicoRangees = extraireDonnees.creeStructureDonnees(nomFichierInstance)
    
    dicoServeurCarac = {}
    for serveur in listeServeurs:
        dicoServeurCarac[str(serveur[0])] = [serveur[1], serveur[2]]
    
    for m in range(carac['M']):
        
        z_mrsi[str(m)] = {}
        
        for r in range(carac['R']):
            
            z_mrsi[str(m)][str(r)] = {}
            
            l_m = extraireDonnees.genererListe_l_m(dicoObstacles[str(r)],dicoServeurCarac[str(m)][0], carac["S"], r)
            
            for couple in l_m:
                
                z_mrsi[str(m)][str(r)][str(couple[1])] = {}
                
                for i in range(carac['P']):
                    print "var = z_mrsi {0} {1} {2} {3}".format(m, r, couple[1], i)
                    z_mrsi[str(m)][str(r)][str(couple[1])][str(i)] = m.addVar(vtype = GRB.BINARY, lb=0, name="z_mrsi {0} {1} {2} {3}" .format(m, r, couple[1], i))
    
    
    z_mrsi["id du serveur"]["num rangee"]["num slot"]["num pool"]
    
    return z_mrsi
    
#    def creerX(XNbCase,ori,init,nbTours,nom):
#    "Creation des variables X ijk  "
#    casesX ={}
#    for i in range (XNbCase):  
#        variables = {}
#        if ori == False:
#            case = init+i
#        else:
#            case = init+i*g.getColonne()
#        for j in range(nbTours+1):
#            #print("var = x %s %d %d" %(nom,(case),(j)))
#            variables[j] = m.addVar(vtype=GRB.BINARY, lb=0, name="x %s %d %d" % (nom,(case),(j)) ) #VCT
#                
#        casesX[case] = variables    
#    x[nom] = casesX
#
#    return None

def main():
    nomFichier = "petit_dc.in"
    nomFichierInstance = extraireDonnees.creeFichierInstancePourcentage(nomFichier,100) #petit_dc_100.txt
    z = creerVariables(nomFichierInstance)
    print z
    
