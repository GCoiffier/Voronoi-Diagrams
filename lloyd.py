# Lloyd relaxation

## ------ Importation ------

import diagram

## ------
def relax(vordiagram, n=1):
    """
    apply the Lloyd relaxation on a voronoi diagram n times.
    The Lloyad relaxation works on sites of the diagram, replacing every site by the barycenter of every vertices of its voronoi cell.
    """
    print("Relaxing ...")
    cells = vordiagram.VoronoiCellsVertices(completed = False)
    new_sites = []
    for i in range(n):

        for s in vordiagram.sites :
            x,y = 0,0
            n = len(cells[s])
            for vert in cells[s] :
                if vert is not None :
                    x+= vert[0]
                    y+= vert[1]
            new_sites.append((x/n , y/n))

    return diagram.Voronoi(new_sites)
