import sys
import os
import threading
from time import sleep
from typing import List, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from graphes.core import Graphe
from graphes.visualisation import VisualisationGraphe
from graphes.propagation import simulate_transmission_flows
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
        self.patient_zero = None
        self.is_simulating = False
        self.simulation_thread = None

        self.setup_ui()

    def fermer_application(self):
        if self.is_simulating:
            self.stop_simulation()
        self.root.destroy()

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_panel = ControlPanel(main_frame, self)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.graph_widget = GraphWidget(main_frame)
        self.graph_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.dessiner_graphe()

    # ===== Existing Graph Methods (unchanged) =====
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

            if sommet is None:
                sommet = self.graphe.ordre - 1

            if sommet < 0 or sommet >= self.graphe.ordre:
                messagebox.showerror("Erreur", f"Le sommet {sommet} n'existe pas")
                return

            if not messagebox.askyesno("Confirmation", 
                                     f"Supprimer le sommet {sommet} et toutes ses arêtes ?"):
                return

            self.graphe.supprimer_sommet(sommet)
            self.dessiner_graphe()
            messagebox.showinfo("Succès", f"Sommet {sommet} supprimé avec succès")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")

    def supprimer_dernier_sommet(self):
        self.supprimer_sommet()

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
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment réinitialiser le graphe ?"):
            self.graphe = Graphe(0)
            self.visualisation = None
            self.graph_widget.clear()
            self.dessiner_graphe()


    def minimum_interactions(self, source, dest):
        """Controller method with proper error handling"""
        if not hasattr(self, 'graphe'):
            return {
                'success': False,
                'message': "Graph not initialized"
            }
            
        if self.graphe.ordre == 0:
            return {
                'success': False,
                'message': "Empty graph"
            }
        
        try:
            from graphes.propagation import minimum_interactions
            return minimum_interactions(
                self.graphe.matrice_adjacence,
                source,
                dest
            )
        except Exception as e:
            return {
                'success': False,
                'message': f"Calculation error: {str(e)}"
            }


    def super_contaminateur(self) -> dict:
        """Controller method for Hamiltonian path finding"""
        if not hasattr(self, 'graphe'):
            return {
                'success': False,
                'message': "Graph not initialized"
            }
            
        if self.graphe.ordre == 0:
            return {
                'success': False,
                'message': "Empty graph"
            }
        
        try:
            from graphes.propagation import super_contaminateur
            return super_contaminateur(self.graphe.matrice_adjacence)
        except Exception as e:
            return {
                'success': False,
                'message': f"Calculation error: {str(e)}"
            }
        
    def find_hamiltonian_path(self) -> dict:
        """Controller method for Hamiltonian path finding"""
        if not hasattr(self, 'graphe'):
            return {'success': False, 'message': "Graph not initialized"}
            
        if self.graphe.ordre == 0:
            return {'success': False, 'message': "Empty graph"}
        
        try:
            from graphes.propagation import super_contaminateur
            return super_contaminateur(self.graphe.matrice_adjacence)
        except Exception as e:
            return {'success': False, 'message': f"Error: {str(e)}"}

    def detect_critical_zones(self) -> dict:
        """Controller method for zone detection"""
        if not hasattr(self, 'graphe') or self.graphe.ordre == 0:
            return {
                'success': False,
                'message': "Graph not initialized or empty",
                'components': [],
                'critical_nodes': []
            }
        
        try:
            from graphes.propagation import detect_isolated_groups
            return detect_isolated_groups(self.graphe.matrice_adjacence)
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'components': [],
                'critical_nodes': []
            }
        

    def min_time_to_infection(self, sources: List[int], target: int, time_per_step: float = 1.0) -> Optional[float]:
        """Calculates minimum infection propagation time"""
        if not hasattr(self, 'graphe') or self.graphe.ordre == 0:
            messagebox.showerror("Erreur", "Le graphe est vide")
            return None
            
        try:
            from graphes.propagation import minimum_time_to_infection
            return minimum_time_to_infection(
                self.graphe.matrice_adjacence,
                sources,
                target,
                time_per_step
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Calcul impossible: {str(e)}")
            return None




    # ===== NEW: Simulation Methods =====
    def definir_patient_zero(self):
        """Fixed version with correct method names"""
        if not hasattr(self, 'root') or not tk._default_root:
            return
                
        try:
            node = int(self.control_panel.patient_zero_entry.get())
            if node < 0 or node >= self.graphe.ordre:
                self.root.after(0, messagebox.showerror, "Erreur", f"Le sommet {node} n'existe pas")
                return
                    
            # Reset previous patient zero if exists
            if hasattr(self, 'patient_zero') and self.patient_zero is not None:
                self.root.after(0, self.graph_widget.update_node_color, self.patient_zero, "skyblue")
                    
            self.patient_zero = node
            self.root.after(0, self.graph_widget.update_node_color, node, "red")
            self.root.after(0, self.control_panel.update_info_label, f"Patient Zéro: Sommet {node}")
            
        except ValueError:
            self.root.after(0, messagebox.showerror, "Erreur", "Veuillez entrer un numéro valide")

    def set_patient_zero(self, node):
        """Set the selected node as patient zero"""
        self.patient_zero = node
        self.graph_widget.highlight_node(node, "red")
        self.control_panel.update_info_label(f"Patient Zéro: Sommet {node}")

    def start_simulation(self):
        """Start the propagation simulation"""
        if self.is_simulating:
            return
            
        if self.patient_zero is None:
            messagebox.showwarning("Attention", "Veuillez sélectionner un Patient Zéro d'abord!")
            return
            
        if self.graphe.ordre == 0:
            messagebox.showwarning("Attention", "Le graphe est vide!")
            return

        # Get parameters from control panel
        infection_prob, recovery_prob = self.control_panel.get_simulation_parameters()
        if infection_prob is None or recovery_prob is None:
            return

        # Disable controls during simulation
        self.is_simulating = True
        self.control_panel.disable_simulation_controls()
        
        # Start simulation in background thread
        self.simulation_thread = threading.Thread(
            target=self.run_simulation,
            args=(infection_prob, recovery_prob),
            daemon=True
        )
        self.simulation_thread.start()

    def run_simulation(self, infection_prob, recovery_prob):
        """Run the propagation simulation"""
        # Convert graph to adjacency list format
        adj_matrix = self.graphe.matrice_adjacence
        
        # Get simulation history
        history = simulate_transmission_flows(
            adj_matrix,
            initial_infected=[self.patient_zero],
            steps=20,
            infection_prob=infection_prob,
            recovery_prob=recovery_prob
        )
        
        # Update visualization for each step
        for step, states in enumerate(history):
            if not self.is_simulating:
                break  # Stop if simulation was cancelled
                
            # Update node colors
            for node, state in states.items():
                color = "red" if state == "infected" else "green" if state == "immune" else "blue"
                self.graph_widget.update_node_color(node, color)
                
            # Update info label
            infected_count = sum(1 for state in states.values() if state == "infected")
            self.control_panel.update_info_label(
                f"Étape {step+1}: {infected_count} infecté(s)"
            )
            
            # Force GUI update and wait
            self.root.update()
            sleep(1)  # 1 second between steps
            
        # Simulation ended
        self.is_simulating = False
        self.control_panel.enable_simulation_controls()

    def stop_simulation(self):
        """Stop the ongoing simulation"""
        self.is_simulating = False
        if self.simulation_thread:
            self.simulation_thread.join()
        self.control_panel.enable_simulation_controls()

    def reset_simulation(self):
        """Fixed reset using update_node_color"""
        self.stop_simulation()
        if hasattr(self, 'patient_zero') and self.patient_zero is not None:
            self.root.after(0, self.graph_widget.update_node_color, self.patient_zero, "skyblue")
            self.patient_zero = None
                
        if hasattr(self, 'graphe'):
            for node in range(self.graphe.ordre):
                self.root.after(0, self.graph_widget.update_node_color, node, "skyblue")
                    
        if hasattr(self, 'control_panel'):
            self.root.after(0, self.control_panel.update_info_label, "Prêt")

if __name__ == "__main__":
    root = tk.Tk()
    app = GrapheApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nFermeture de l'application...")
        root.destroy()