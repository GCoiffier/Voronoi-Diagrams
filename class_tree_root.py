# TIPE 2016 Guillaume Coiffier

import os
path = os.getcwd()

from maths import *
from copy import copy

ID_NODE = 0

## ------ Arbre des arcs ------

class Root:
    
    def __init__(self,tree = None):
        ''' Classe contenant la racine d'un arbre. Définit par défaut un arbre vide'''
        self.tree = tree


    def GetRemainingEdges(self):
        ''' renvoie les arêtes restantes dans l'arbre de racine root (ie les arêtes non terminées)
        '''
        def GRErec(t):
            if t.IsLeaf():
                return []
            return [t]+GRErec(t.left)+GRErec(t.left)
        return GRErec(self.tree)
    
class Tree:

    def __init__(self):
        '''
        Classe utilisée pour représenter les objets dans l'arbre
        '''
        
        global ID_NODE

        self.father = None
        self.left = None
        self.right = None
        self.id = ID_NODE
        ID_NODE +=1


    def __eq__(self,other):
        '''test d'égalité entre noeuds'''
        return self.id == other.id

    def __repr__(self):
        return str(self.id)


    def IsLeaf(self):
        return (self.left is None) and (self.right is None)


    def IsRoot(self):
        return (self.father is None)


    def IsRightChild(self):
        ''' 
        Renvoie True si self est le fils droit de son père
        Renvoie False si self est le fils gauche de son père
        Renvoie True si le noeud est la racine
        '''
        if self.IsRoot() : return True
        return (self == self.father.right)


    def IsLeftChild(self):
        ''' 
        Renvoie False si self est le fils droit de son père
        Renvoie True si self est le fils gauche de son père
        Renvoie True si le noeud est la racine
        '''
        if self.IsRoot() : return True
        return (self == self.father.left)


    @staticmethod
    def UltimateLeftChild(x):
        '''
        La feuille la plus à gauche du sous-arbre dont x est racine
        '''
        if x.IsLeaf() : 
            return x
        return Tree.UltimateLeftChild(x.left)


    @staticmethod
    def UltimateRightChild(x):
        '''
        La feuille la plus à droite du sous-arbre dont x est racine
        '''
        if x.IsLeaf() : 
            return x
        return Tree.UltimateRightChild(x.right)


    @staticmethod
    def GetLeftNeighbour(x):
        ''' accède à la feuille à gauche du noeud x'''
        return Tree.UltimateRightChild(x.left)


    @staticmethod
    def GetRightNeighbour(x):
        ''' accède à la feuille à droite du noeud x'''
        return Tree.UltimateLeftChild(x.right)


    @staticmethod
    def LeftParent(x):
        ''' renvoie le premier ancêtre de x dont x n'est pas le fils gauche '''
        p = x.father
        if p is None : 
            return None
        if x.IsLeftChild() :
            return Tree.LeftParent(p)
        return p


    @staticmethod
    def RightParent(x):
        ''' renvoie le premier ancêtre de x dont x n'est pas le fils droit '''
        p = x.father
        if p is None : 
            return None
        if x.IsRightChild() :
            return Tree.RightParent(p)
        return p


    @staticmethod
    def FindParabolaIntersection(root, u):
        '''
        Trouve l'arc de parabole ( <=> feuille de l'arbre) intersecté
        par la parabole dégénérée de site u
        '''
        if root.tree is None : 
            return None # arbre vide
        def FPIrec(t,u):
            if t.IsLeaf(): 
                return t
            s_left, s_right = t.sites
            x = find_intersection_parabola(s_left, s_right, u[1])
            if x <= u[0] :
                return FPIrec(t.left,u)
            else :
                return FPIrec(t.right,u)
        return FPIrec(root.tree,u)


    @staticmethod
    def HighestPredecessor(root, node):
        ''' le noeud parmis le peère de gauche et le père de droite de 'node' situé le plus haut dans l'arbre'''
        predec = Tree.LeftParent(node)
        if predec is None : 
            return root.tree # la racine
        if node.father == predec : 
            return Tree.RightParent(node)
        return predec


    @staticmethod
    def ReplaceNode(root, x, y):
        ''' remplace le noeud x par le noeud y dans l'arbre de racine root'''

        if x.IsRoot(): # x.father is None
            root.tree = y
            y.father = None
        else :
            pere = x.father
            if x.IsRightChild():
                pere.right = y
            else :
                pere.left = y
            y.father = pere

        y.left = x.left
        if y.left is not None :
            y.left.father = y

        y.right = x.right
        if y.right is not None :
            y.right.father = y


    @staticmethod
    def Insert(root, x, a, ar1, b, ar2, c):
        ''' insère le sous-arbre a,ar1,b,ar2,c à la place de x'''
        # Insertion de ar1 dans l'arbre à la place de x
        Tree.ReplaceNode(root,x,ar1)

        # Construction du sous-arbre de racine ar1
        b.father = ar2
        b.right = None
        b.left = None

        c.father = ar2
        c.right = None
        c.left = None

        ar2.father = ar1
        ar2.left = b
        ar2.right = c

        a.father = ar1
        a.left = None
        a.right = None

        ar1.left = a
        ar1.right = ar2

        
    @staticmethod
    def Delete(root, leaf, ar):
        '''supprime la feuille leaf de l'arbre. ar est l'arête qui sera insérée entre
        les voisins de gauche et de droite de leaf'''

        pere = leaf.father

        if leaf.IsRightChild() :
            frere = pere.left
        else :
            frere = pere.right

        hpredec = Tree.HighestPredecessor(root, leaf)
        Tree.ReplaceNode(root, hpredec, ar)
        if pere.IsRoot():
            root.tree = frere
            frere.father = None
        else :
            gp = pere.father
            if pere.IsRightChild():
                gp.right = frere
            else :
                gp.left = frere
            frere.father = gp