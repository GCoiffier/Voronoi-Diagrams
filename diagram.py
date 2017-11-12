"""
TIPE 2016 Guillaume Coiffier
Modified code of my original implementation that works with pygame
"""


## ------ Importations ------

from random import randint,random
from time import time
import pygame
from class_event import *
from class_edge import *
from class_parabola import *
from maths import *

## ------ Diagramme de Voronoi ------

class Voronoi:

    ## ------ Fonctions d'initialisation ------

    def __init__(self, sites, width = 800, height = 600):
        '''
        Crée le diagramme de Voronoi des sites (donnés sous forme de liste ou d'un entier pour un certain nombre de points aléatoires)
        Le balayage s'effectue selon les y croissants
        '''
        # Données d'affichage
        
        self.width = width
        self.height = height
        # Droites délimitant les bords de l'ecran
        ''' les 4 arêtes definies ci-dessous servent a calculer un point hors de l'écran dans la fonction Edge.prolonge() '''
        d1 = Edge((-10,10), (-10,-10), None, None)
        d2 = Edge((10,10),(-10, height+10), None, None)
        d3 = Edge((10,-10),(10+width, 10+height), None, None)
        d4 = Edge((-10,-10), (10+width, -10), None, None)
        self.bords = (d1,d2,d3,d4)

        # 1. Initialisation l'arbre
        self.root = Root()

        # 2. Initialisation des sites
        if isinstance(sites,int) :
            self.sites = self._generateSites(sites)
        elif isinstance(sites,list):
            self.sites = sites
        else :
            raise TypeError("Argument must be an integer for random points or a list of points")

        # Temps de calcul
        print("Computing Voronoi diagram")
        t0 = time()

        # 3. Initialisation d'un graphe vide
        self.edges = []
        self.vertices = []

        # 4. Initialisation de la file de priorité
        self.file_evenement = FilePrio()
        for x in self.sites :
            self.file_evenement.append(SiteEvent(Parabola(x)))

        # 5. Traitement
        while not self.file_evenement.empty() :
            ev = self.file_evenement.pop()
            if ev.type : # Evénement de type Site : la ligne passe au dessus d'un nouveau point
                self._HandleSiteEvent(ev)
            else :  # Evénement de type Cercle : un arc disparaît de la ligne
                if self.file_evenement.IsActive(ev) :
                    self._HandleCircleEvent(ev)

        # Temps de calcul
        self.time = time()-t0
        print("Diagram calculated : " + str(self.time) + " seconds")

    def _generateSites(self, n):
            '''Renvoie une liste de n coordonnées de sites pseudo-aléatoires'''
            output = set()
            k = 0
            while k < n :
                pt = (randint(1, self.width -1)+random(),randint(1,self.height -1)+random())
                if pt not in output :
                    output.add(pt)
                    k += 1
            return output

    ## ------ Fonctions utilitaires de l'algorithme de Fortune ------

    def _CheckCircleEvent(self, par, t) :
            ''' 
            Prend en paramètre un object de type 'Parabola', recherche l'éventuelle disparition future
            de l'arc dans le processus, crée l'événement associé et l'insère dans la file de priorité

            t = position de la ligne de balayage lors de la vérification
            '''

            # Les éventuels arcs voisins à gauche et à droite de 'par'
            # et les arêtes du diagramme délimitant 'par'
            arete_g,arc_g = Parabola.LeftParab(par)
            arete_d,arc_d = Parabola.RightParab(par)
            
            
            # Si l'arc est a l'un des bords du front parabolique ou si les sites de gauche et de droite sont confondus,
            # l'arc ne disparaitra pas => pas d'événement cercle
            if arc_g is None or arc_d is None or arc_g.site == arc_d.site  :
                    return
                    
            s = find_intersection_edge(arete_g,arete_d)

            if s is None : #les aretes ne s'intersectent jamais => pas d'événement cercle
                return

            r = distance(s, par.site)

            if (s[1] + r) < t+eps : # l'événement cercle se situe avant la ligne de balayage => pas d'événement cercle
                    return
            
            # Dans les autres cas, l'événement cercle et créé et inséré :
            # Un événement de type cercle est représenté par la plus grande valeur t de la droite de balayage tangente au cercle
            # ici, cette valeur vaut s.y + r (ordonnée du centre + rayon)

            e = CircleEvent(par, s[1] + r)
            self.file_evenement.append(e)


    def _HandleSiteEvent(self, event):
            ''' 
            Fonction appelée lorsque l'événement est un événement site, 
            c'est a dire lorsque la ligne de balayage passe sur un nouveau site 
            '''
            
            u = event.site # le site balayé
            t = event.key # la position de la ligne de balayage

            par = Tree.FindParabolaIntersection(self.root,u)

            if par is None :
                    # par n'existe pas si u est le tout premier evenement site
                    self.root = Root(Parabola(u))
                    return

            s = par.site

            # On désactive l'eventuel événement cercle correspondant
            self.file_evenement.remove(par)

            # Initialisation des 3 arcs qui vont remplacer 'par' dans le front parabolique
            a,b,c = Parabola(s),Parabola(u),Parabola(s)

            # Création de deux demi arêtes
            direct = orthog(s,u)
            pt = find_intersection_point(s,u)

            nouv_arete_g = Edge(direct, pt, s, u)
            nouv_arete_d = Edge(opposite(direct), pt, u, s)

            nouv_arete_g.half = nouv_arete_d
            nouv_arete_d.half = nouv_arete_g

            self.edges.append(nouv_arete_g)
            self.edges.append(nouv_arete_d)

            # Actualisation de l'arbre
            Tree.Insert(self.root, par, a, nouv_arete_g, b, nouv_arete_d, c)
            ''' la sequence G : par : D est remplacee par la sequence
                G : a : nouv_arete_g : b : nouv_arete_d : c : D '''

            # On recherche quand les arcs a et c disparaitront à cause de la croissance de leurs voisins
            self._CheckCircleEvent(a,t)
            self._CheckCircleEvent(c,t)


    def _HandleCircleEvent(self, event):
        ''' 
        Fonction appelee lorsque ev est un evenement cercle, 
        c'est a dire lorsqu'une parabole disparait du front de balayage
        '''
        
        t = event.key # La position de la ligne de balayage 
        par = event.par # La parabole qui disparaît

        arete_g,arc_g = Parabola.LeftParab(par)
        arete_d,arc_d = Parabola.RightParab(par)
        
        # On désactive les événements cercles correspondants a arc_g et arc_d
        # Ces événements seront reinsérés correctement une fois que le front parabolique a été modifié 
        self.file_evenement.remove(arc_g)
        self.file_evenement.remove(arc_d)
        
        s = find_intersection_edge(arete_g,arete_d)
        
        nouv_arete = Edge(orthog(arc_g.site, arc_d.site), s, arc_g.site, arc_d.site)
        nouv_arete.som1 = s
        nouv_arete.disappearing_site = par.site
        self.edges.append(nouv_arete)

        Tree.Delete(self.root, par, nouv_arete)

        arete_g.som2 = s
        arete_d.som2 = s

        self.vertices.append(s)

        self._CheckCircleEvent(arc_g, t)
        self._CheckCircleEvent(arc_d, t)
    

    ## ------ Post-traitement des aretes ------

    def _fusionAretes(self):
        ''' fusionne les demi-arêtes '''
        out = []
        for x in self.edges :
            if not x.seen :
                if x.half is not None :
                    y = x.half
                    y.seen = True
                    x.som1 = y.som2
                out.append(x)
        self.edges = out

    def _completeAretes(self):
        ''' Fusionne les demi-arêtes et prolonge les arêtes dont une extremité est à
        l'infini avec un point en dehors de l'ecran'''
        self._fusionAretes()
        for x in self.edges :
            x.updateDirection()
            x.prolonge(self.bords)

    ## ------ Fonction de sortie ------

    def VoronoiDiagram(self, completed = True) : 
        ''' Renvoie le diagramme de Voronoi des sites sous la forme d'une liste de sites et d'une liste d'arêtes '''
        if not completed :
            self._fusionAretes()       
        else :
            self._completeAretes()
        return self.vertices, [x.output() for x in self.edges]

    def VoronoiCellsEdges(self, completed = False):
        '''
        Renvoie le diagramme de Voronoi des sites sous forme d'un dictionnaire
        tel que dict[s] est l'ensemble des arêtes de la cellule de voronoi du point s
        '''
        d = {}
        if completed :
            self._completeAretes()
        else :
            self._fusionAretes()
        for s in self.sites :
            d[s] = set()
        for ar in self.edges :
            sg,sd = ar.sites
            d[sg].add(ar.output())
            d[sd].add(ar.output())
        return d

    def VoronoiCellsVertices(self, completed = False, integer = False):
        '''
        Renvoie le diagramme de Voronoi des sites sous forme d'un dictionnaire
        tel que dict[s] est l'ensemble des sommets de la cellule de voronoi du point s.
        Si integer est vrai, les coordonnées des points sont arrondies à l'entier près.
        '''
        d = {}
        if completed :
            self._completeAretes()
        else :
            self._fusionAretes()
        for s in self.sites :
            d[s] = set()
        for ar in self.edges :
            sg,sd = ar.sites
            if integer :
                d[sg].add((int(ar.som1[0]), int(ar.som1[1])))
                d[sg].add((int(ar.som2[0]), int(ar.som2[1])))
                d[sd].add((int(ar.som1[0]), int(ar.som1[1])))
                d[sd].add((int(ar.som2[0]), int(ar.som2[1])))
            else :
                d[sg].add(ar.som1)
                d[sg].add(ar.som2)
                d[sd].add(ar.som1)
                d[sd].add(ar.som2)
        return d


    def Delaunay(self):
        ''' 
        Calcule la triangulation de Delaunay des points sites à partir de l'algorithme de Fortune.
        Renvoie une liste de tuples correspondant aux coordonnées des extrémités des arêtes.
        '''
        delaunay_aretes = []
        for ar in self.edges :
            delaunay_aretes.append(ar.sites)
        return delaunay_aretes

    def plot(self, voronoi = True, vertices = True, delaunay = False):
        """
        Runs the main loop.
        """
        pygame.display.set_caption("Map Generator")
        clock = pygame.time.Clock()
        pygame.display.set_mode((self.width,self.height))
        screen = pygame.display.get_surface()

        edges = [e[0] for e in self.VoronoiDiagram(completed = True)[1]]
        delaunay_edges = self.Delaunay()
        vertices = [ (int(p[0]), int(p[1]))  for p in self.sites ]

        while True:
            clock.tick(60)
            screen.fill((255,255,255))

            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    return

            if voronoi :
                for edge in edges :
                    x1,y1 = int(edge[0][0]), int(edge[0][1])
                    x2,y2 = int(edge[1][0]), int(edge[1][1])
                    pygame.draw.line(screen, pygame.Color("black"), (x1,y1), (x2,y2), 1)

            if delaunay :
                for edge in delaunay_edges :
                    x1,y1 = int(edge[0][0]), int(edge[0][1])
                    x2,y2 = int(edge[1][0]), int(edge[1][1])
                    pygame.draw.line(screen, pygame.Color("green"), (x1,y1), (x2,y2), 1)

            if vertices :
                for vert in vertices :
                    x,y = int(vert[0]), int(vert[1])
                    pygame.draw.circle(screen, pygame.Color("blue"), (x,y), 2, 0)

            pygame.display.flip()


