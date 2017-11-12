# TIPE

## ------ Importations ------

import os

path = os.getcwd()

from diagram import Voronoi

# ------ Tracé d'un diagramme aléatoire ------

vd = Voronoi(200, 800, 600)

vd.plot(delaunay = False, voronoi=True, vertices = True)
