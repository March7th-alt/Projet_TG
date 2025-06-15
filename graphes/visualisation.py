# Module visualisation.py - Visualisation des graphes
# Ce module permet de représenter graphiquement les graphes en utilisant networkx et matplotlib

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Optional
from .core import Graphe

class VisualisationGraphe:
    # Classe pour la visualisation des graphes implémentés avec la classe Graphe
    
    def __init__(self, graphe: Graphe):
        # Initialise la visualisation avec un graphe existant

        # Args:
        #     graphe (Graphe): Instance de la classe Graphe à visualiser
        self.graphe = graphe
        self.nx_graphe = self._convertir_vers_networkx()
        
    def _convertir_vers_networkx(self) -> nx.Graph:
        # Convertit la matrice d'adjacence en un graphe networkx

        # Returns:
        #     nx.Graph: Graphe networkx correspondant
        G = nx.Graph()
        
        # Ajout des sommets
        G.add_nodes_from(range(self.graphe.ordre))
        
        # Ajout des arêtes
        for i in range(self.graphe.ordre):
            for j in range(i, self.graphe.ordre):  # On évite les doublons car graphe non orienté
                if self.graphe.matrice_adjacence[i][j] == 1:
                    G.add_edge(i, j)
                    
        return G
    
    def afficher_graphe(self, titre: str = "Graphe", avec_labels: bool = True, node_size: int = 500) -> None:
        # Affiche le graphe avec matplotlib

        # Args:
        #     titre (str): Titre du graphe
        #     avec_labels (bool): Si True, affiche les labels des sommets
        #     node_size (int): Taille des nœuds
        plt.figure(figsize=(8, 6))
        
        pos = nx.spring_layout(self.nx_graphe)
        nx.draw(self.nx_graphe, pos, with_labels=avec_labels, node_size=node_size, 
               node_color='skyblue', edge_color='gray', width=2, alpha=0.7)
        
        plt.title(titre)
        plt.show()
    
    def afficher_chemin(self, chemin: List[int], titre: str = "Chemin dans le graphe") -> None:
        # Affiche un chemin particulier dans le graphe

        # Args:
        #     chemin (List[int]): Liste des sommets du chemin
        #     titre (str): Titre du graphique
        if not chemin:
            print("Aucun chemin à afficher")
            return
            
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(self.nx_graphe)
        
        # Dessin du graphe de base
        nx.draw(self.nx_graphe, pos, with_labels=True, node_size=500,
               node_color='lightgray', edge_color='gray', width=1, alpha=0.5)
        
        # Mise en évidence du chemin
        edges = [(chemin[i], chemin[i+1]) for i in range(len(chemin)-1)]
        nx.draw_networkx_nodes(self.nx_graphe, pos, nodelist=chemin, node_color='red')
        nx.draw_networkx_edges(self.nx_graphe, pos, edgelist=edges, edge_color='red', width=3)
        
        plt.title(titre)
        plt.show()
    
    def afficher_cycle_eulerien(self) -> None:
        # Affiche le cycle eulérien s'il existe
        cycle = self.graphe.trouver_cycle_eulerien()
        if cycle:
            print(f"Cycle eulérien trouvé: {cycle}")
            self.afficher_chemin(cycle, "Cycle eulérien")
        else:
            print("Aucun cycle eulérien trouvé")
    
    def afficher_chemin_eulerien(self) -> None:
        # Affiche le chemin eulérien s'il existe
        chemin = self.graphe.trouver_chemin_eulerien()
        if chemin:
            print(f"Chemin eulérien trouvé: {chemin}")
            self.afficher_chemin(chemin, "Chemin eulérien")
        else:
            print("Aucun chemin eulérien trouvé")

def visualiser_graphe_depuis_matrice(matrice: List[List[int]]) -> None:
    # Fonction utilitaire pour visualiser directement un graphe depuis une matrice d'adjacence
    
    # Args:
    #     matrice (List[List[int]]): Matrice d'adjacence
    g = Graphe(len(matrice))
    g.matrice_adjacence = matrice
    visualisation = VisualisationGraphe(g)
    visualisation.afficher_graphe()