import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from graphes.core import Graphe
from graphes.visualisation import VisualisationGraphe
from interface.widgets.control_panel import ControlPanel
from interface.widgets.graph_widget import GraphWidget

class GrapheApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Graphes")
        self.root.geometry("1000x700")

        self.root.protocol("WM_DELETE_WINDOW", self.fermer_application)

        self.graphe = Graphe(0)
        self.visualisation = None

        self.setup_ui()

    def fermer_application(self):
        self.root.destroy()

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_panel = ControlPanel(main_frame, self)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.graph_widget = GraphWidget(main_frame)
        self.graph_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.dessiner_graphe()

    def dessiner_graphe(self):
        if self.graphe.ordre > 0:
            self.visualisation = VisualisationGraphe(self.graphe)
            self.graph_widget.dessiner_graphe(self.graphe, self.visualisation)
        else:
            self.graph_widget.clear()

        self.control_panel.update_info_label(f"Ordre du graphe: {self.graphe.ordre}")
        self.control_panel.update_spinboxes(max(0, self.graphe.ordre - 1))

    def ajouter_sommet(self):
        self.graphe.ajouter_sommet()
        self.dessiner_graphe()

    def supprimer_sommet(self, sommet=None):
        """Supprime un sommet spécifique ou le dernier sommet si aucun n'est spécifié"""
        try:
            if self.graphe.ordre == 0:
                messagebox.showwarning("Attention", "Le graphe est déjà vide")
                return

            if sommet is None:  # Si aucun sommet spécifié, supprime le dernier
                sommet = self.graphe.ordre - 1

            # Vérifie que le sommet existe
            if sommet < 0 or sommet >= self.graphe.ordre:
                messagebox.showerror("Erreur", f"Le sommet {sommet} n'existe pas")
                return

            # Demande confirmation avant suppression
            if not messagebox.askyesno("Confirmation", 
                                     f"Supprimer le sommet {sommet} et toutes ses arêtes ?"):
                return

            # Supprime le sommet
            self.graphe.supprimer_sommet(sommet)
            self.dessiner_graphe()
            messagebox.showinfo("Succès", f"Sommet {sommet} supprimé avec succès")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")

    def supprimer_dernier_sommet(self):
        """Supprime le dernier sommet du graphe"""
        self.supprimer_sommet()  # Appelle sans paramètre pour supprimer le dernier

    def ajouter_arete(self, sommet1, sommet2):
        try:
            self.graphe.ajouter_arete(sommet1, sommet2)
            self.dessiner_graphe()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_arete(self, sommet1, sommet2):
        try:
            self.graphe.supprimer_arete(sommet1, sommet2)
            self.dessiner_graphe()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def afficher_degres(self):
        if self.graphe.ordre == 0:
            messagebox.showinfo("Degrés des sommets", "Le graphe est vide.")
            return

        result = "Degrés des sommets:\n"
        degres = self.graphe.calculer_degres()
        for sommet, degre in enumerate(degres):
            result += f"Sommet {sommet}: {degre}\n"

        messagebox.showinfo("Degrés des sommets", result)

    def trouver_cycle_eulerien(self):
        cycle = self.graphe.trouver_cycle_eulerien()
        if cycle:
            messagebox.showinfo("Cycle Eulerien", f"Cycle trouvé: {cycle}")
        else:
            messagebox.showinfo("Cycle Eulerien", "Aucun cycle eulérien trouvé")

    def trouver_chemin_eulerien(self):
        chemin = self.graphe.trouver_chemin_eulerien()
        if chemin:
            messagebox.showinfo("Chemin Eulerien", f"Chemin trouvé: {chemin}")
        else:
            messagebox.showinfo("Chemin Eulerien", "Aucun chemin eulérien trouvé")

    def generer_graphe_aleatoire(self, n, p):
        try:
            self.graphe = Graphe(0)
            self.graphe.generer_graphe_aleatoire(n, p)
            self.dessiner_graphe()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def verifier_chemin_longueur(self, depart, arrivee, longueur):
        existe = self.graphe.existe_chemin_longueur(depart, arrivee, longueur)
        if existe:
            messagebox.showinfo("Chemin de longueur L", f"Un chemin de longueur {longueur} existe entre {depart} et {arrivee}.")
        else:
            messagebox.showinfo("Chemin de longueur L", f"Aucun chemin de longueur {longueur} entre {depart} et {arrivee}.")

    def afficher_voisins(self, sommet):
        try:
            voisins = self.graphe.voisinage(sommet)
            messagebox.showinfo("Voisins", f"Sommet {sommet} a pour voisins: {voisins}")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def reinitialiser_graphe(self):
        """Réinitialise complètement le graphe"""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment réinitialiser le graphe ?"):
            self.graphe = Graphe(0)
            self.visualisation = None
            self.graph_widget.clear()
            self.dessiner_graphe()

if __name__ == "__main__":
    root = tk.Tk()
    app = GrapheApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nFermeture de l'application...")
        root.destroy()