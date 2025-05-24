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
        
        # Simulation-related attributes
        self.node_items = {}  # Stores node artists for color updates
        self.current_positions = None  # Stores node positions
        self.nx_graphe = None  # Reference to networkx graph

    def dessiner_graphe(self, graphe, visualisation):
        self.ax.clear()
        self.node_items = {}  # Reset node items
        
        if graphe.ordre > 0:
            self.nx_graphe = visualisation.nx_graphe
            pos = nx.spring_layout(self.nx_graphe, seed=42)
            self.current_positions = pos  # Store positions for later updates
            
            # Draw edges first
            nx.draw_networkx_edges(
                self.nx_graphe, pos, ax=self.ax,
                edge_color='gray', width=2
            )
            
            # Draw nodes with individual control
            for node in self.nx_graphe.nodes():
                color = 'skyblue'  # Default healthy color
                self.node_items[node] = nx.draw_networkx_nodes(
                    self.nx_graphe, pos, ax=self.ax,
                    nodelist=[node],
                    node_size=500,
                    node_color=color
                )
                
            # Draw labels
            nx.draw_networkx_labels(
                self.nx_graphe, pos, ax=self.ax,
                font_size=10, font_color='black'
            )
            
        self.ax.set_title("Représentation du Graphe")
        self.ax.axis('off')
        self.canvas.draw()

    def clear(self):
        self.ax.clear()
        self.ax.set_title("Représentation du Graphe")
        self.ax.axis('off')
        self.node_items = {}
        self.current_positions = None
        self.nx_graphe = None
        self.canvas.draw()

    # ===== NEW: Simulation-related methods =====
    def update_node_color(self, node, color):
        """Update the color of a specific node"""
        if node in self.node_items:
            self.node_items[node].set_color(color)
            self.canvas.draw()

    def highlight_node(self, node, color):
        """Highlight a specific node"""
        self.update_node_color(node, color)

    def reset_node_color(self, node):
        """Reset a node to default color"""
        self.update_node_color(node, 'skyblue')

    def update_all_node_colors(self, color_dict):
        """Update colors for multiple nodes at once"""
        for node, color in color_dict.items():
            if node in self.node_items:
                self.node_items[node].set_color(color)
        self.canvas.draw()