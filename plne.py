# -*- coding: utf-8 -*-
import gurobipy as g
import extraireDonnees

""" Variables """
# r : id rangee

model = g.Model("RP-OptimizeDataCenter")
model.setParam( 'OutputFlag', False) #Desactive  le mode verbeux
model.setParam('TimeLimit', 2*60) #Limite de temps pour la resolution 

def creerVariables(fileName):
    """
    Creer et retourne les dictionnaires z_mrsi, dicoServeurCarac et k_rs :
    - Les variables Gurobi du PLNE
        z_mrsi["id du serveur"]["num rangee"]["num slot"]["num pool"]
    
    - Un dictionnaire contenant les caracteristiques de chaque serveur
        dicoServeurCarac["id du serveur"] = [taille du serveur, capacite du serveur]
    
    - Pour chaque emplacement (rangee, slot) l'ensemble des serveurs pouvant etre localises a cet emplacement
        k_rs[(idRangee,idSlot)]=[idServeur1, idserveur2,...]
    """
    z_mrsi = {}
    carac, dicoObstacles, listeServeurs, dicoRangees = extraireDonnees.creeStructureDonnees(fileName)
    
    # dicoServeurCarac["id du serveur"] = [taille du serveur, capacite du serveur]
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
                    z_mrsi[str(m)][str(r)][str(couple[1])][str(i)] = model.addVar(vtype = g.GRB.BINARY, name="z_mrsi {0} {1} {2} {3}" .format(m, r, couple[1], i))
    
    model.update()

    return z_mrsi, dicoServeurCarac, k_rs, carac

def contraintes(z_mrsi, dicoServeurCarac, k_rs):

    """ Contraintes """
#1 Chaque slot contient au plus un serveur
#2 Aucun serveur sur slot indispo
#3 Un serveur a autant de slot que sa taille et ils sont consecutifs ou pas affecte (meme rangee et pas depasser taille)
#4 Un serveur affecte apparait au plus une fois
#5 Un serveur affecte appartient a exactement un pool

    '''
    contrainte 1 : Au plus un serveur occupe un slot (un marqueur max par slot + pas de chevauchement de serveurs)
    '''
    for (r,s), listeServeurs in k_rs.iteritems():
        somme = 0
        if not len(listeServeurs) == 0:
            tailleServeurMax = max([dicoServeurCarac[str(idServ)][0] for idServ in listeServeurs])
            for serveur in listeServeurs:
                for i in range(0,tailleServeurMax):
                    if str(s+i) in z_mrsi[str(serveur)][str(r)]:
                        for a,b in z_mrsi[str(serveur)][str(r)][str(s+i)].iteritems():
                            somme += b
            if not type(somme) == type(0):
                model.addConstr(somme <= 1, "Contrainte 1 : un marqueur max par slot {0} {1}".format(r, s))
 
    '''
    contrainte 2 : Un serveur apparait au plus une fois dans une affectation
    (avec un unique pool)
    '''    
    for m in z_mrsi:
        somme = 0
        for r in z_mrsi[str(m)]:
            for s in z_mrsi[str(m)][str(r)]:
                for i in z_mrsi[str(m)][str(r)][str(s)]:
                    somme += z_mrsi[str(m)][str(r)][str(s)][str(i)]
        if not type(somme) == type(0):
            print somme, "<= 1"
            model.addConstr(somme <= 1, "Contrainte 2 : le serveur {0} apparait au plus une fois dans l'affectation".format(m))
    
    
def linearisationFonctionObj(z_mrsi, carac, dicoServeurCarac):
    '''
    contrainte 3 : linearisation de la capacite garantie du pool i pour une affectation
    '''
    
    sommeCapacitesParPoolParRangee = []
    for i in range(carac["P"]):
        sommeCapacitesParPoolParRangee.append([])
        for r in range(carac["R"]):
            sommeCapacitesParPoolParRangee[r][i] = 0
    
    for m in z_mrsi.keys():
        for r in z_mrsi[m].keys():
            for s in z_mrsi[m][r].keys():
                for i in z_mrsi[m][r][s].keys():
                    sommeCapacitesParPoolParRangee[int(i)][int(r)] += z_mrsi[m][r][s][i] * dicoServeurCarac[m][1]
    
    gc_i = {}                
    for i in range(carac["P"]):
        gc_i[i] = model.addVar(vtype = g.GRB.INTEGER, name="gc_i {0}" .format(i))
        sommeTotale = sum(sommeCapacitesParPoolParRangee[i][:])
        for r in range(carac["R"]):
            model.addConstr(gc_i[i] <= sommeTotale - sommeCapacitesParPoolParRangee[i][r], "Contrainte 3 : capacite garantie par le pool {0} sans la rangee {1}".format(i, r))
    
                    
                        
    
    

def main():
    nomFichier = "petiteInstance.in"
    nomFichierInstance = extraireDonnees.creeFichierInstancePourcentage(nomFichier,100)
    z_mrsi,dicoServeurCarac,k_rs, carac = creerVariables(nomFichierInstance)
    contraintes(z_mrsi,dicoServeurCarac,k_rs)
    linearisationFonctionObj(z_mrsi, carac, dicoServeurCarac)
#    print z_mrsi
    
