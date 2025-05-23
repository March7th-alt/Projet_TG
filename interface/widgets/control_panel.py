# control_panel.py
import tkinter as tk
from tkinter import ttk, messagebox

class ControlPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Initialise l'interface du panneau de contrôle"""
        # Section création de graphe
        creation_frame = ttk.LabelFrame(self, text="Création de Graphe")
        creation_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(creation_frame, text="Ajouter Sommet", command=self.controller.ajouter_sommet).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(creation_frame, text="Supprimer Dernier Sommet", command=self.supprimer_dernier_sommet).pack(fill=tk.X, padx=5, pady=2)
        
        # Nouveau bouton pour supprimer un sommet spécifique
        sommet_spec_frame = ttk.Frame(creation_frame)
        sommet_spec_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(sommet_spec_frame, text="Sommet à supprimer:").grid(row=0, column=0, sticky='w')
        self.sommet_a_supprimer = ttk.Spinbox(sommet_spec_frame, width=5, from_=0, to=0)
        self.sommet_a_supprimer.grid(row=0, column=1)
        
        ttk.Button(sommet_spec_frame, text="Supprimer Sommet Spécifique", 
                  command=self.supprimer_sommet_specifique).grid(row=1, column=0, columnspan=2, sticky='ew', pady=2)

        # Contrôles pour les arêtes
        edge_frame = ttk.Frame(creation_frame)
        edge_frame.pack(fill=tk.X, pady=5)

        ttk.Label(edge_frame, text="Sommet 1:").grid(row=0, column=0, sticky='w')
        self.edge_s1 = ttk.Spinbox(edge_frame, width=5, from_=0, to=0)
        self.edge_s1.grid(row=0, column=1)

        ttk.Label(edge_frame, text="Sommet 2:").grid(row=1, column=0, sticky='w')
        self.edge_s2 = ttk.Spinbox(edge_frame, width=5, from_=0, to=0)
        self.edge_s2.grid(row=1, column=1)

        ttk.Button(edge_frame, text="Ajouter Arête", command=self.ajouter_arete).grid(row=2, column=0, columnspan=2, sticky='ew', pady=2)
        ttk.Button(edge_frame, text="Supprimer Arête", command=self.supprimer_arete).grid(row=3, column=0, columnspan=2, sticky='ew', pady=2)

        # Graphe aléatoire
        ttk.Button(creation_frame, text="Graphe Aléatoire", command=self.demander_parametres_graphe_aleatoire).pack(fill=tk.X, padx=5, pady=5)
        
        # Nouveau bouton : Réinitialiser Interface
        ttk.Button(creation_frame, text="Réinitialiser Interface", command=self.reinitialiser_interface).pack(fill=tk.X, padx=5, pady=5)

        # Section algorithmes
        algo_frame = ttk.LabelFrame(self, text="Algorithmes")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(algo_frame, text="Afficher Degrés", command=self.controller.afficher_degres).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(algo_frame, text="Trouver Cycle Eulerien", command=self.controller.trouver_cycle_eulerien).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(algo_frame, text="Trouver Chemin Eulerien", command=self.controller.trouver_chemin_eulerien).pack(fill=tk.X, padx=5, pady=2)
        
        # Nouveaux boutons pour les fonctions de propagation
        ttk.Button(algo_frame, text="Interactions Minimales", 
                  command=self.demander_parametres_interactions).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(algo_frame, text="Trouver Super Contaminateur", 
                  command=self.controller.trouver_super_contaminateur).pack(fill=tk.X, padx=5, pady=2)

        # Chemin de longueur k
        k_frame = ttk.LabelFrame(self, text="Chemin de longueur k")
        k_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(k_frame, text="k =").pack(side=tk.LEFT, padx=5)
        self.length_entry = ttk.Entry(k_frame, width=5)
        self.length_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(k_frame, text="Vérifier", command=self.verifier_chemin).pack(side=tk.LEFT, padx=5)

        # Voisins d'un sommet
        voisin_frame = ttk.LabelFrame(self, text="Voisins")
        voisin_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(voisin_frame, text="Sommet:").pack(side=tk.LEFT, padx=5)
        self.sommet_entry = ttk.Entry(voisin_frame, width=5)
        self.sommet_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(voisin_frame, text="Afficher", command=self.afficher_voisins).pack(side=tk.LEFT, padx=5)

        # Section informations
        info_frame = ttk.LabelFrame(self, text="Informations")
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        self.info_label = ttk.Label(info_frame, text="Ordre du graphe: 0")
        self.info_label.pack(pady=5)

    def demander_parametres_interactions(self):
        """Ouvre une boîte de dialogue pour les paramètres des interactions minimales"""
        dialog = tk.Toplevel()
        dialog.title("Interactions Minimales")
        
        ttk.Label(dialog, text="Sommet source:").grid(row=0, column=0, padx=5, pady=5)
        source_entry = ttk.Entry(dialog)
        source_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Sommet destination:").grid(row=1, column=0, padx=5, pady=5)
        dest_entry = ttk.Entry(dialog)
        dest_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def calculer():
            try:
                source = int(source_entry.get())
                destination = int(dest_entry.get())
                self.controller.calculer_interactions_minimales(source, destination)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des numéros valides")
        
        ttk.Button(dialog, text="Calculer", command=calculer).grid(row=2, columnspan=2, pady=10)

    def supprimer_sommet_specifique(self):
        """Gère la suppression d'un sommet spécifique"""
        try:
            sommet = int(self.sommet_a_supprimer.get())
            if hasattr(self.controller, 'supprimer_sommet'):
                self.controller.supprimer_sommet(sommet)
            else:
                messagebox.showerror("Erreur", "Fonction de suppression non disponible")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de sommet valide")

    def demander_parametres_graphe_aleatoire(self):
        """Ouvre une boîte de dialogue pour les paramètres du graphe aléatoire"""
        dialog = tk.Toplevel()
        dialog.title("Paramètres du graphe aléatoire")
        
        tk.Label(dialog, text="Nombre de sommets:").grid(row=0, column=0, padx=5, pady=5)
        n_entry = tk.Entry(dialog)
        n_entry.grid(row=0, column=1, padx=5, pady=5)
        n_entry.insert(0, "5")
        
        tk.Label(dialog, text="Probabilité d'arête (0-1):").grid(row=1, column=0, padx=5, pady=5)
        p_entry = tk.Entry(dialog)
        p_entry.grid(row=1, column=1, padx=5, pady=5)
        p_entry.insert(0, "0.5")
        
        def generer():
            try:
                n = int(n_entry.get())
                p = float(p_entry.get())
                if not (0 <= p <= 1):
                    raise ValueError
                self.controller.generer_graphe_aleatoire(n, p)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides")
        
        tk.Button(dialog, text="Générer", command=generer).grid(row=2, columnspan=2, pady=10)

    def supprimer_dernier_sommet(self):
        """Gère la suppression du dernier sommet"""
        if hasattr(self.controller, 'supprimer_dernier_sommet'):
            self.controller.supprimer_dernier_sommet()
        else:
            if hasattr(self.controller, 'graphe') and self.controller.graphe.ordre > 0:
                sommet = self.controller.graphe.ordre - 1
                self.controller.supprimer_sommet(sommet)

    def verifier_chemin(self):
        """Gère la vérification de chemin"""
        k = self.get_selected_length()
        if k is not None:
            s1, s2 = self.get_selected_vertices()
            if s1 is not None and s2 is not None:
                self.controller.verifier_chemin_longueur(s1, s2, k)

    def afficher_voisins(self):
        """Gère l'affichage des voisins"""
        sommet = self.get_selected_sommet()
        if sommet is not None:
            self.controller.afficher_voisins(sommet)

    def update_spinboxes(self, max_val):
        """Met à jour les spinboxes"""
        self.edge_s1.configure(from_=0, to=max_val)
        self.edge_s2.configure(from_=0, to=max_val)
        self.sommet_a_supprimer.configure(from_=0, to=max_val)
        self.edge_s1.set(0)
        self.edge_s2.set(1 if max_val > 0 else 0)
        self.sommet_a_supprimer.set(0)

    def update_info_label(self, text):
        """Met à jour le label d'information"""
        self.info_label.config(text=text)

    def get_selected_vertices(self):
        try:
            val1 = int(self.edge_s1.get())
            val2 = int(self.edge_s2.get())
            return val1, val2
        except ValueError:
            messagebox.showwarning("Erreur", "Veuillez entrer des numéros valides")
            return None, None

    def get_selected_length(self):
        try:
            return int(self.length_entry.get())
        except ValueError:
            messagebox.showwarning("Erreur", "Longueur invalide")
            return None

    def get_selected_sommet(self):
        try:
            return int(self.sommet_entry.get())
        except ValueError:
            messagebox.showwarning("Erreur", "Sommet invalide")
            return None

    def ajouter_arete(self):
        s1, s2 = self.get_selected_vertices()
        if s1 is not None and s2 is not None:
            self.controller.ajouter_arete(s1, s2)

    def supprimer_arete(self):
        s1, s2 = self.get_selected_vertices()
        if s1 is not None and s2 is not None:
            self.controller.supprimer_arete(s1, s2)

    def reinitialiser_interface(self):
        """Réinitialise l'interface : vide les entrées, supprime le graphe, etc."""
        if hasattr(self.controller, 'reinitialiser_graphe'):
            self.controller.reinitialiser_graphe()

        self.length_entry.delete(0, tk.END)
        self.sommet_entry.delete(0, tk.END)
        self.edge_s1.set(0)
        self.edge_s2.set(0)
        self.sommet_a_supprimer.set(0)
        self.update_info_label("Ordre du graphe: 0")
        self.update_spinboxes(0)