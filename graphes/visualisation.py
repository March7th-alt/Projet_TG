import matplotlib.pyplot as plt
import networkx as nx

def afficher_graphe(G):
    """Affiche le graphe avec couleurs par état"""
    couleurs = {
        "sain": "lightblue",
        "infecté": "red",
        "immunisé": "green"
    }
    node_colors = [couleurs[G.nodes[n].get("état", "sain")] for n in G.nodes()]
    
    nx.draw(G, 
            with_labels=True, 
            node_color=node_colors,
            node_size=200,
            font_size=8)
    plt.title("Réseau de Propagation")
    plt.show()