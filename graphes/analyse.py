import networkx as nx

def calculer_degres(G):
    """Retourne un dictionnaire {nœud: degré}"""
    return dict(G.degree())

def super_propagateurs(G, top=3):
    """Identifie les 'top' nœuds les plus connectés"""
    degres = calculer_degres(G)
    return sorted(degres.items(), key=lambda x: x[1], reverse=True)[:top]