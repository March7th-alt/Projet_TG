import sys
import os
import networkx as nx
from pathlib import Path

# Ajoute le dossier parent au chemin Python
sys.path.append(str(Path(__file__).parent.parent))

# Maintenant les imports fonctionneront
from graphes.creation import creer_graphe
from graphes.analyse import calculer_degres, super_propagateurs
from graphes.visualisation import afficher_graphe

def tester_creation():
    """Teste la génération du graphe"""
    G = creer_graphe(n=10, p=0.2)
    assert isinstance(G, nx.Graph), "Doit retourner un graphe NetworkX"
    assert len(G.nodes()) == 10, "Doit avoir 10 nœuds"
    print("✅ Test création : OK")

def tester_analyse():
    """Teste le calcul des degrés et super-propagateurs"""
    G = creer_graphe(n=10, p=0.2)
    degres = calculer_degres(G)
    assert isinstance(degres, dict), "Doit retourner un dictionnaire"
    supers = super_propagateurs(G, top=2)
    assert len(supers) == 2, "Doit retourner 2 super-propagateurs"
    print(f"Super-propagateurs trouvés : {supers}")
    print("✅ Test analyse : OK")

def tester_visualisation():
    """Teste l'affichage graphique"""
    G = creer_graphe(n=10, p=0.2)
    G.nodes[0]["état"] = "infecté"  # Nœud 0 infecté
    G.nodes[1]["état"] = "immunisé" # Nœud 1 immunisé
    try:
        afficher_graphe(G)
        print("✅ Test visualisation : OK (vérifiez la fenêtre)")
    except Exception as e:
        print(f"❌ Erreur d'affichage : {e}")

if __name__ == "__main__":
    print("--- Lancement des tests ---")
    tester_creation()
    tester_analyse()
    tester_visualisation()
    print("--- Tests terminés ---")