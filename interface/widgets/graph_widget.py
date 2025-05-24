# graph_widget.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

class GraphWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def dessiner_graphe(self, graphe, visualisation):
        self.ax.clear()
        if graphe.ordre > 0:
            pos = nx.spring_layout(visualisation.nx_graphe, seed=42)
            nx.draw(
                visualisation.nx_graphe, pos, ax=self.ax, with_labels=True,
                node_size=500, node_color='skyblue', edge_color='gray', width=2
            )
        self.ax.set_title("Représentation du Graphe")
        self.canvas.draw()
    
        # Ajoute ceci à la fin de la classe GraphWidget
    def clear(self):
        self.ax.clear()
        self.ax.set_title("Représentation du Graphe")
        self.canvas.draw()

