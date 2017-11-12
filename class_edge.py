# TIPE 2016 Guillaume Coiffier

import os
path = os.getcwd()

from class_tree_root import *

class Edge(Tree):
    '''
    Sous-classe de Tree : objet présent aux noeuds de l'arbre
    Un objet représentant une arête du diagramme de Voronoi.
    Contient :
        - le vecteur directeur de l'arête
        - les coordonnées des sommets lorsque ceux-ci sont connus
        - les sites des deux arcs dont l'arête est intersection 
    '''
        
    def __init__(self, direction, som, s1, s2):

        Tree.__init__(self)
        self.somref = som # Un point de référence dont on est sur qu'il est sur l'arête.
        self.som1 = None
        self.som2 = None # les sommets ne sont pas connus a priori lors de la création de l'arête
        self.dir = direction # vecteur (x,y)
        self.half = None # Gestion des demi-arêtes
        self.seen = False # Utile lors de la fusion des arêtes a la fin du traitement

        self.sites = (s1,s2) # site à gauche et site à droite

        self.disappearing_site = None # le 3e site d'un cercle de voronoi 
                                      # lorsque l'arête est crée lors d'un événement site

    def get_half_id(self):
        if self.half is None : 
            return None
        return self.half.id

    def __repr__(self):
        return "id = {0}, sommet 1 = {1} , sommet 2 = {2} , direction = {3} , moitie = {4}, sites = {5}".format(self.id, self.som1, self.som2, 
                                                                                                                self.dir, self.get_half_id(), self.sites)

    def output(self):
        ''' renvoie une arËte simplifiée '''
        return ((self.som1, self.som2), distance(self.sites[0],self.sites[1]))

    def updateDirection(self):
            ''' si l'arête a une extremité qui est à l'infini, cette fonction met à jour 
            la direction de l'arête pour correspondre à son sens reel'''
            if self.half is not None :
                if (self.som1 is None and self.som2 is not None) :
                    v = vecteur(self.som2, self.somref)
                    self.dir = v
                elif (self.som2 is None and self.som1 is not None) :
                    v = vecteur(self.som1, self.somref)
                    self.dir = v
            else :
                sg,sd = self.sites
                sf = self.disappearing_site
                a = vecteur(sg,sf)
                b = vecteur(sf,sd)
                if determinant(a,b) > 0 :
                    (x,y) = self.dir
                    self.dir = (-x,-y)

    def findCorrectEdgeOfScreen(self,bords):
        ''' 
        ar est une arête dont une des extremités est à l'infini et dont la direction a été mise à jour.
        Cette fonction renvoie, parmi les droites d1,d2,d3 et d4, 
        celle qui va être intersectée hors de l'écran par l'arête
        '''
        d1,d2,d3,d4 = bords
        d = self.dir
        x,y = (produit_scalaire(d,(1,0)) >=0), (produit_scalaire(d,(0,1)) >= 0)
        if x and y :
            return d3
        elif x and not y :
            return d4
        elif not x and y :
            return d2
        else :
            return d1

    def prolonge(self,bords):
        '''
        Complète les sommets de l'arête lorsqu'elle n'en a pas 
        (lorsqu'une de ses extremités est à l'infini) 
        '''
        d1,d2,d3,d4 = bords
        if (self.som1 is None) and (self.som2 is None) : # Les deux sommets sont manquants
            if goesToLeft(self) :
                self.som1 = find_intersection_edge(self,d2)
                self.som2 = find_intersection_edge(self,d4)
            else :
                self.som1 = find_intersection_edge(self,d1)
                self.som2 = find_intersection_edge(self,d3)
        elif (self.som2 is None) : # Il ne manque que le sommet droit
            d = self.findCorrectEdgeOfScreen(bords)
            self.som2 = find_intersection_edge(self, d, check = False)
        elif (self.som1 is None) : # Il ne manque que le sommet gauche
            d = self.findCorrectEdgeOfScreen(bords)
            self.som1 = find_intersection_edge(self, d, check = False)