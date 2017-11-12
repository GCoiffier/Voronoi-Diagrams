# TIPE 2016 Guillaume Coiffier

import os
path = os.getcwd()

from class_tree_root import *

class Parabola(Tree):
    ''' Sous-classe de Tree : objet présent aux feuilles de l'arbre '''
    
    def __init__(self, site):
        Tree.__init__(self)
        self.site = site

        self.event_id = -1 # L'id de l'événement cercle correspondant à la parabole

    def __repr__(self):
        return "id = {0}, site = {1}".format(self.id, self.site)
        
    @staticmethod
    def RightParab(par):
        '''le voisin de droite de self '''
        x = Tree.RightParent(par)
        if x is None : 
            return None, None
        return x , Tree.GetRightNeighbour(x)

    @staticmethod
    def LeftParab(par):
        ''' le voisin de gauche de self'''
        x = Tree.LeftParent(par)
        if x is None : 
            return None, None
        return x, Tree.GetLeftNeighbour(x)   