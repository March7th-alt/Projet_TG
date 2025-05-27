import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

#Fichier les fcts de visualisation/mise a jour des couleurs des noeuds etc...

class GraphWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._is_destroyed = False  # Initialize the flag here
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.node_items = {}
        self.current_positions = None
        self.nx_graphe = None

    def safe_draw(self):
        """Thread-safe drawing"""
        if not self._is_destroyed:
            try:
                self.canvas.draw()
            except:
                pass

    def dessiner_graphe(self, graphe, visualisation):
        if self._is_destroyed:
            return
            
        self.ax.clear()
        self.node_items = {}
        
        if graphe.ordre > 0:
            self.nx_graphe = visualisation.nx_graphe
            pos = nx.spring_layout(self.nx_graphe, seed=42)
            self.current_positions = pos
            
            nx.draw_networkx_edges(
                self.nx_graphe, pos, ax=self.ax,
                edge_color='gray', width=2
            )
            
            for node in self.nx_graphe.nodes():
                self.node_items[node] = nx.draw_networkx_nodes(
                    self.nx_graphe, pos, ax=self.ax,
                    nodelist=[node],
                    node_size=500,
                    node_color='skyblue'
                )
                
            nx.draw_networkx_labels(
                self.nx_graphe, pos, ax=self.ax,
                font_size=10, font_color='black'
            )
            
        self.ax.set_title("Représentation du Graphe")
        self.ax.axis('off')
        self.safe_draw()

    def update_node_color(self, node, color):
        """Universal method for all color changes"""
        if hasattr(self, 'node_items') and not self._is_destroyed:
            if node in self.node_items:
                self.node_items[node].set_color(color)
                self.safe_draw()

    def update_all_node_colors(self, color_map):
        if self._is_destroyed:
            return
            
        for node, color in color_map.items():
            if node in self.node_items:
                self.node_items[node].set_color(color)
        self.safe_draw()

    def clear(self):
        if self._is_destroyed:
            return
            
        self.ax.clear()
        self.ax.set_title("Représentation du Graphe")
        self.ax.axis('off')
        self.node_items = {}
        self.current_positions = None
        self.nx_graphe = None
        self.safe_draw()

    def destroy(self):
        """Override destroy for safe cleanup"""
        self._is_destroyed = True
        try:
            plt.close(self.figure)
        except:
            pass
        super().destroy()