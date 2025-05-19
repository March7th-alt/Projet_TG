import networkx as nx

def calculer_degres(G):
    """Retourne un dictionnaire {nœud: degré}"""
    return dict(G.degree())

def super_propagateurs(G, top=3):
    """Identifie les 'top' nœuds les plus connectés"""
    degrees = calculer_degres(G)
    return sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:top]

    # Sorted: fonction qui fait le trie
    # degrees.item :
    # key=lamda:la cle de trie qui dit a la fct sorted comment fait le trie
    # x: un element de dictionnaire degrees
    # x[1] : le degre de chaque element (fait trie selon le degre)
    # reverse=true: Sorted fait le trie selon l'ordre croissant, this thing lets us do ordre decroissant
    # top: garde les tops premiers