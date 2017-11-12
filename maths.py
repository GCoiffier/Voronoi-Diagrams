# TIPE 2016 Guillaume Coiffier

from math import sqrt

eps = 1E-7 # précision globale

## ------ Fonctions géometriques utilitaires ------

def vecteur(a,b) :
    ''' renvoie les coordonnées du vecteur a->b'''
    return (b[0]-a[0], b[1]-a[1])

def opposite(x):
    ''' renvoie le vecteur opposé à x'''
    return (-x[0], -x[1])

def produit_scalaire(a,b):
    ''' produit scalaire canonique '''
    return (a[0]*b[0]) + (a[1]*b[1])

def distance(a,b):
    ''' distance euclidienne '''
    vect = vecteur(a,b)
    return sqrt(produit_scalaire(vect,vect))

def orthog(a,b):
    ''' renvoie un vecteur orthogonal au vecteur a->b'''
    x = b[1]-a[1]
    y = a[0]-b[0]
    return (x,y)

def normalize(vect):
    ''' le vecteur colinéaire dans le meme sens de norme 1 '''
    n = sqrt(produit_scalaire(vect,vect))
    return (vect[0]/n , vect[1]/n)


def determinant(v1,v2) :
    ''' déterminant 2*2 '''
    return v1[0]*v2[1] - v1[1]*v2[0]


def goesToLeft(ar):
    ''' Renvoie True si l'arête ar est orientée sur la gauche (x décroissants)'''
    if ar.som1 is None and ar.som2 is None :
        direction = ar.dir
    elif ar.som1 is not None :
        direction = vecteur(ar.som1, ar.som_ref)
    else :
        direction = vecteur(ar.som2, ar.som_ref)
    return (produit_scalaire(direction,(1,0)) >=0)


def find_intersection_edge(ar1,ar2, check = True):
    ''' renvoie le point d'intersection de deux arêtes, s'il existe
        si check est True, renvoie le point d'intersection uniquement s'il est situe dans la bonne direction  '''

    (x1,y1) = ar1.somref
    (x2,y2) = ar2.somref

    (dirx1,diry1) = ar1.dir
    (dirx2,diry2) = ar2.dir

    d1 = determinant((x2-x1,y2-y1),(-dirx2,-diry2))
    d2 = determinant((dirx1,diry1),(-dirx2,-diry2))
    
    if abs(d2) < eps :
                return None # aretes paralleles => pas d'intersection
    inter = (x1+(d1*dirx1)/d2, y1+(d1*diry1)/d2)
    if check and ((inter[0]-x1)*dirx1 < 0 or (inter[1]-y1)*diry1 < 0 or (inter[0]-x2)*dirx2 < 0 or  (inter[1]-y2)*diry2 < 0) :
       return None
    return inter


def find_intersection_point(s,u) :
    '''
    Renvoie le point d'intersection de la parabole donnée par le site s
    et de la droite d'équation x = u[0] (parabole dégénérée de foyer u)
    avec une droite d'équation y = u[1]
    '''
    p = u[1]-s[1]
    if abs(p) < eps : # Les deux sites sont à la meme ordonnee. l'abscisse cherchée est au milieu du segment
        return ((s[0]+u[0])/2, u[1])
    x = u[0]-s[0]
    return (x + s[0], - (x*x)/(2*p) + (u[1]-s[1])/2 + s[1])


def find_intersection_parabola(s1,s2,t):
    '''
    Trouve le point d'intersection des paraboles 
    de droite directrice x=t et de foyers s1 et s2
    '''

    if abs(s1[1] - s2[1]) < eps  :
        return (s1[0]+s2[0])/2

    d1 = 2*(s1[1]-t)
    d2 = 2*(s2[1]-t)

    if abs(d1) < eps :
        return s1[0]

    elif abs(d2) < eps :
        return s2[0]

    b1 = -2*s1[0]/d1
    b2 = -2*s2[0]/d2

    c1 = d1/4 + ((s1[0])**2)/d1
    c2 = d2/4 + ((s2[0])**2)/d2

    a = 1/d1 - 1/d2
    b = b1 - b2
    c = c1-c2
    delta = b*b - 4*a*c
    r1 = (-b + sqrt(delta))/(2*a)
    r2 = (-b - sqrt(delta))/(2*a)

    if s1[1] <= s2[1] :
        return max(r1,r2)
    return min(r1,r2)
