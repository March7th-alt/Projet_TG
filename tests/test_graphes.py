import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graphes.creation import creer_graphe
import networkx as nx

def test_creation_graphe():
    """Teste si le graphe est créé correctement"""
    # 1. Appel de ta fonction
    G = creer_graphe(n=10, p=0.1)
    
    # 2. Vérifications
    assert isinstance(G, nx.Graph)  # Vérifie que c'est bien un graphe NetworkX
    assert len(G.nodes()) == 10     # Doit avoir 10 nœuds
    assert 0.05 <= len(G.edges())/45 <= 0.15  # Vérifie la densité (~10% d'arêtes possibles)
    
    # 3. Test des attributs
    assert G.nodes[0]["état"] == "sain"  # Tous initialisés à "sain"
    print("✅ test_creation_graphe : PASSÉ")

if __name__ == "__main__":
    test_creation_graphe()