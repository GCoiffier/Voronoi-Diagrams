# TIPE 2016 Guillaume Coiffier

#from maths import *
from queue import PriorityQueue

## --- File de priorité des événements---

ID_EVENT = 0

class Event:

    def __init__(self, par):
        
        self.type = None
        # True -> site
        # False -> cercle
        self.par = par
        self.site = self.par.site
        self.key = None

    ## Fonctions de comparaison pour la file de priorité

    def __lt__(self,other):
        ''' self < other'''
        return self.key < other.key or ((self.key == other.key) and (self.site[0] < other.site[0]))

    def __le__(self,other):
        ''' self <= other'''
        return self.key <= other.key or ((self.key == other.key) and (self.site[0] <= other.site[0]))

    def __gt__(self,other):
        ''' self > other'''
        return self.key > other.key or ((self.key == other.key) and (self.site[0] > other.site[0]))

    def __ge__(self,other):
        ''' self >= other'''
        self.key >= other.key or ((self.key == other.key) and (self.site[0] >= other.site[0]))


    def __str__(self):
        if self.type :
            return (str(self.site))
        return str(self.key)


class CircleEvent(Event):
    
    def __init__(self, par, t):
        global ID_EVENT

        Event.__init__(self,par)
        self.type = False
        self.key = t

        self.event_id = ID_EVENT
        self.par.event_id = ID_EVENT
        ID_EVENT += 1


class SiteEvent(Event):

    def __init__(self, par):
        Event.__init__(self,par)
        self.type = True
        self.key = self.site[1]


class FilePrio:

    def __init__(self):
        ''' 
        Classe File de priorité.
        contient : - une file de priorité
                   - une poubelle pour les événements supprimés (potentiellement encore dans la file)
        '''
        self.data = PriorityQueue()
        self.deleted = set()

    def empty(self):
        ''' renvoie True si la file est vide'''
        return self.data.empty()

    def append(self,x):
        '''Ajoute l'élément x à la file de priorité
            x est un événement => le poids est inclus'''
        self.data.put(x)
 
    def pop(self):
        '''Extrait et renvoie le premier événement de la file de priorité'''
        return self.data.get()

    def remove(self, p):
        '''
        Désactive l'éventuel événement cercle de la parabole p
        '''
        if p.event_id > -1 :
            self.deleted.add(p.event_id)
            p.event_id = -1

    def IsActive(self,ev) :
        return not (ev.event_id in self.deleted)

