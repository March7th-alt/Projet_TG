import networkx as nx
import random

def creer_graphe(n=100, p=0.02):
  """
  Crée un graphe aléatoire modélisant un réseau social.

  Args:
      n (int): Nombre de personnes (nœuds). Par défaut 100.
      p (float): Probabilité qu'une arête existe (0.01 = réseau sparse, 0.1 = dense).

  Returns:
      nx.Graph: Un graphe non orienté.
  """
  # 1. Créer un graphe aléatoire (modèle Erdős-Rényi)
  G = nx.erdos_renyi_graph(n, p)

  # 2. Ajouter des attributs par défaut (optionnel)
  for personne in G.nodes():
      G.nodes[personne]["état"] = "sain"  # Par défaut, tout le monde est sain

  return G


Gr = creer_graphe(100, 0.2)
print(Gr)