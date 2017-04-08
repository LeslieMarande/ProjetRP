# -*- coding: utf-8 -*-
import extraireDonnees

""" Contraintes """
#1 Chaque slot contient au plus un serveur
#2 Aucun serveur sur slot indispo
#3 Un serveur a autant de slot que sa taille et ils sont consecutifs ou pas affecte (meme rangee et pas depasser taille)
#4 Un serveur affecte apparait au plus une fois
#5 Un serveur affecte appartient a exactement un pool

""" Variables """
# r : id rangee




m = Model("mogplex")
m.setParam( 'OutputFlag', False) #Desactive  le mode verbeux
m.setParam('TimeLimit', 2*60) #Limite de temps pour la resolution 

def creerR():

    return None

def main():
    nomFichier = "petit_dc.in"
    creeFichierInstancePourcentage(nomFichier,100) #petit_dc_100.txt
