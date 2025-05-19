import sys
import os
import random
import networkx as nx
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from graphes.creation import creer_graphe
from graphes.analyse import calculer_degres, super_propagateurs
from graphes.visualisation import afficher_graphe

def infecter_aleatoire(G, nombre_infections=1):
    """
    Infecte un nombre spécifique de nœuds aléatoirement
    Args:
        G (nx.Graph): Le graphe à modifier
        nombre_infections (int): Nombre de nœuds à infecter (1 par défaut)
    Returns:
        list: Liste des IDs des nœuds infectés
    """
    # Sélection aléatoire sans remise
    noeuds_infectes = random.sample(list(G.nodes()), min(nombre_infections, len(G.nodes())))
    
    for noeud in noeuds_infectes:
        G.nodes[noeud]["état"] = "infecté"
    
    return noeuds_infectes

def tester_tout():
    """Fonction principale de test avec un seul nœud infecté"""
    print("--- Lancement des tests ---")
    
    # 1. Création du graphe
    G = creer_graphe(n=100, p=0.2)
    
    # Test de création
    try:
        assert isinstance(G, nx.Graph), "Doit retourner un graphe NetworkX"
        assert len(G.nodes()) == 100, "Doit avoir 100 nœuds"
        print("✅ Test création : OK")
    except AssertionError as e:
        print(f"❌ Test création échoué : {e}")
    
    # 2. Test d'analyse
    try:
        degres = calculer_degres(G)
        assert isinstance(degres, dict), "Doit retourner un dictionnaire"
        
        # Infection d'UN SEUL nœud dans le graphe principal
        noeud_infecte = infecter_aleatoire(G, 1)[0]
        print(f"Nœud infecté principal : {noeud_infecte}")
        
        supers = super_propagateurs(G, top=2)
        assert len(supers) == 2, "Doit retourner 2 super-propagateurs"
        print(f"Super-propagateurs trouvés : {supers}")
        print("✅ Test analyse : OK")
    except AssertionError as e:
        print(f"❌ Test analyse échoué : {e}")
    
    # 3. Test de visualisation
    try:
        # Création d'un sous-graphe de 50 nœuds
        petit_G = G.subgraph(list(G.nodes)[:50]).copy()  # Copie indépendante
        
        # Vérification si le nœud infecté principal est dans le sous-graphe
        if noeud_infecte in petit_G.nodes():
            print(f"Le nœud infecté principal {noeud_infecte} est dans la visualisation")
        else:
            # Si le nœud infecté n'est pas dans le sous-graphe, on en infecte un nouveau
            nouveau_infecte = infecter_aleatoire(petit_G, 1)[0]
            print(f"Nouveau nœud infecté pour la visualisation : {nouveau_infecte}")
        
        # Sélection d'un nœud à immuniser (différent de l'infecté)
        noeuds_dispos = [n for n in petit_G.nodes() if petit_G.nodes[n]["état"] != "infecté"]
        noeud_immunise = random.choice(noeuds_dispos)
        petit_G.nodes[noeud_immunise]["état"] = "immunisé"
        
        print(f"Nœud immunisé : {noeud_immunise}")
        
        afficher_graphe(petit_G)
        print("✅ Test visualisation : OK (vérifiez la fenêtre)")
    except Exception as e:
        print(f"❌ Erreur d'affichage : {e}")
    
    print("--- Tests terminés ---")

if __name__ == "__main__":
    tester_tout()