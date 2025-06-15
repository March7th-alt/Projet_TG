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
        ttk.Button(algo_frame, text="Afficher Matrice", command=self.show_adjacency_matrix).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(algo_frame, text="Afficher Ordre", command=self.show_graph_order).pack(fill=tk.X, padx=5, pady=2)


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

        #Section Propagation
        proba_frame = ttk.LabelFrame(self, text="Analayse de Propagation")
        proba_frame.pack(fill=tk.X, padx=5, pady=5)

        # Minimum interactions controls
        min_int_frame = ttk.Frame(proba_frame)
        min_int_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(min_int_frame, text="Source:").pack(side=tk.LEFT)
        self.min_int_source = ttk.Spinbox(min_int_frame, from_=0, to=0, width=5)
        self.min_int_source.pack(side=tk.LEFT)
        
        ttk.Label(min_int_frame, text="Destination:").pack(side=tk.LEFT, padx=(5,0))
        self.min_int_dest = ttk.Spinbox(min_int_frame, from_=0, to=0, width=5)
        self.min_int_dest.pack(side=tk.LEFT)
        
        ttk.Button(min_int_frame, text="Interactions Min.", 
              command=self.show_min_interactions).pack(side=tk.LEFT, padx=(10,0))

        #Super contaminateur
        ttk.Button(
        proba_frame,
        text="Super Contaminateur",
        command=self.handle_super_contaminateur  # Handler method
    ).pack(fill=tk.X, pady=2)
        
        #zone critique/ isolee
        ttk.Button(
        proba_frame,
        text="Détecter Zones Isolées/Critiques",
        command=self.handle_critical_zones
    ).pack(fill=tk.X, pady=2)
        
        #min time to infect
        ttk.Button(
        proba_frame,
        text="Temps Minimum d'Infection",
        command=self.handle_min_infection_time
    ).pack(fill=tk.X, pady=2)


         # ===== Simulation Section =====
        sim_frame = ttk.LabelFrame(self, text="Simulation de Propagation", padding=5)
        sim_frame.pack(fill=tk.X, padx=5, pady=5)

        # Patient Zero input
        patient_zero_frame = ttk.Frame(sim_frame)
        patient_zero_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(patient_zero_frame, text="Patient Zéro:").pack(side=tk.LEFT)
        self.patient_zero_entry = ttk.Entry(patient_zero_frame, width=5)
        self.patient_zero_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(patient_zero_frame, text="Définir", 
                  command=self.controller.definir_patient_zero).pack(side=tk.LEFT)

        # Simulation controls
        sim_controls = ttk.Frame(sim_frame)
        sim_controls.pack(fill=tk.X, pady=2)
        
        ttk.Button(sim_controls, text="Démarrer", 
                  command=self.controller.start_simulation).pack(side=tk.LEFT, expand=True, padx=2)
        ttk.Button(sim_controls, text="Arrêter", 
                  command=self.controller.stop_simulation).pack(side=tk.LEFT, expand=True, padx=2)
        ttk.Button(sim_controls, text="Réinitialiser", 
                  command=self.controller.reset_simulation).pack(side=tk.LEFT, expand=True, padx=2)

        # Simulation parameters
        param_frame = ttk.Frame(sim_frame)
        param_frame.pack(fill=tk.X, pady=2)

        ttk.Label(param_frame, text="Prob. Infection:").pack(side=tk.LEFT)
        self.infection_prob = ttk.Spinbox(param_frame, from_=0, to=1, increment=0.1, width=5)
        self.infection_prob.set(0.9)
        self.infection_prob.pack(side=tk.LEFT, padx=2)

        vacc_frame = ttk.Frame(sim_frame)
        vacc_frame.pack(fill=tk.X, pady=5)

        ttk.Button(vacc_frame, text="Vaccinate Highest Degree", 
              command=self.controller.vaccinate_highest_degree).pack(side=tk.LEFT, padx=2)
    
        ttk.Button(vacc_frame, text="Simulate After Vaccination", 
              command=self.controller.simulate_after_vaccination).pack(side=tk.LEFT, padx=2)

        # Section informations
        info_frame = ttk.LabelFrame(self, text="Informations")
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        self.info_label = ttk.Label(info_frame, text="Ordre du graphe: 0")
        self.info_label.pack(pady=5)

    def show_adjacency_matrix(self):
        """Display the adjacency matrix in a popup window"""
        if not hasattr(self.controller, 'graphe') or self.controller.graphe.ordre == 0:
            messagebox.showinfo("Info", "Le graphe est vide.")
            return

        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Matrice d'adjacence")
        popup.geometry("500x400")
        
        # Add scrollbars
        frame = ttk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True)
        
        y_scroll = ttk.Scrollbar(frame)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create text widget with monospace font for alignment
        text = tk.Text(
            frame,
            wrap=tk.NONE,
            font=("Courier New", 10),
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )
        text.pack(fill=tk.BOTH, expand=True)
        
        y_scroll.config(command=text.yview)
        x_scroll.config(command=text.xview)
        
        # Get matrix data
        matrice = self.controller.graphe.matrice_adjacence
        n = self.controller.graphe.ordre
        
        # Create header
        header = "    " + "  ".join(f"{i:>3}" for i in range(n)) + "\n"
        text.insert(tk.END, header)
        text.insert(tk.END, "   " + "-" * (4 * n) + "\n")
        
        # Add matrix rows
        for i in range(n):
            row = f"{i:2}| " + "  ".join(f"{matrice[i][j]:>3}" for j in range(n)) + "\n"
            text.insert(tk.END, row)
        
        # Make text read-only
        text.config(state=tk.DISABLED)
        
        # Add close button
        ttk.Button(
            popup,
            text="Fermer",
            command=popup.destroy
        ).pack(pady=5)

    def show_graph_order(self):
        """Display the graph order"""
        if not hasattr(self.controller, 'graphe'):
            messagebox.showinfo("Ordre du Graphe", "Aucun graphe n'est chargé")
            return
        
        order = self.controller.graphe.ordre
        messagebox.showinfo(
            "Ordre du Graphe",
            f"Le graphe contient {order} sommet(s)",
        )

    def show_min_interactions(self):
        """Handle minimum interactions button"""
        if not hasattr(self.controller, 'graphe') or self.controller.graphe.ordre == 0:
            messagebox.showwarning("Erreur", "Le graphe est vide!")
            return
        
        try:
            source = int(self.min_int_source.get())
            dest = int(self.min_int_dest.get())
            max_node = self.controller.graphe.ordre - 1
            
            if source < 0 or source > max_node or dest < 0 or dest > max_node:
                raise ValueError("Noeud invalide")
                
            result = self.controller.minimum_interactions(source, dest)
            
            # Safe dictionary access with .get()
            interactions = result.get('interactions')
            path = result.get('path', [])
            message = result.get('message', "")
            
            if interactions is not None:
                display_msg = (
                    f"Interactions minimales: {interactions}\n"
                    f"Chemin: {path}\n"
                    f"{message}"
                )
            else:
                display_msg = f"Aucun chemin trouvé\n{message}"
                
            messagebox.showinfo("Résultat", display_msg)
            
        except ValueError as e:
            messagebox.showerror("Erreur", f"Entrée invalide: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")


    def handle_super_contaminateur(self):
        """Handles button click and shows results"""
        # Get results from controller
        result = self.controller.find_hamiltonian_path()
        
        # Prepare message
        if result.get('success'):
            message = (
                f"{result.get('message', '')}\n"
                f"Chemin: {result['path']}"
            )
        else:
            message = f"Aucun chemin trouvé\n\n{result.get('message', '')}"
        
        # Show simple messagebox (no visualization)
        messagebox.showinfo("Résultat", message)


    def handle_critical_zones(self):
        """Handles detection of both isolated groups and critical nodes (altho its kinda wrong)"""
        try:
            # Get results from controller
            result = self.controller.detect_critical_zones()
            
            # Build the display message
            message = [
                f"=== Résultats d'Analyse ===",
                f"Groupes isolés: {len(result['components'])}",
                f"Noeuds critiques: {len(result['critical_nodes'])}"
            ]
            
            # Add component details
            for i, group in enumerate(result['components'], 1):
                message.append(f"\nGroupe {i} ({len(group)} nœuds): {sorted(group)}")
            
            # Add critical nodes
            if result['critical_nodes']:
                message.append("\n\n🔴 Noeuds critiques:")
                message.append(", ".join(map(str, result['critical_nodes'])))
            else:
                message.append("\n🟢 Aucun noeud critique trouvé")
            
            # Show scrollable results
            self.show_scrollable_message(
                title="Zones Isolées & Critiques",
                message="\n".join(message)
            )
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Analyse impossible: {str(e)}")

    def show_scrollable_message(self, title: str, message: str):
        """Generic scrollable display window"""
        win = tk.Toplevel()
        win.title(title)
        
        text = tk.Text(win, wrap=tk.WORD, width=60, height=15)
        scroll = ttk.Scrollbar(win, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        text.insert(tk.END, message)
        text.config(state=tk.DISABLED)
        
        ttk.Button(win, text="Fermer", command=win.destroy).pack(pady=5)

    def handle_min_infection_time(self):
        """Handles minimum infection time calculation"""
        # Create parameter input dialog
        dialog = tk.Toplevel()
        dialog.title("Paramètres d'Infection")
        
        # Source nodes input
        ttk.Label(dialog, text="Sources (séparées par des virgules):").grid(row=0, column=0, padx=5, pady=5)
        sources_entry = ttk.Entry(dialog)
        sources_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Target node input
        ttk.Label(dialog, text="Cible:").grid(row=1, column=0, padx=5, pady=5)
        target_spin = ttk.Spinbox(dialog, from_=0, to=0, width=5)
        target_spin.grid(row=1, column=1, padx=5, pady=5)
        
        # Time per interaction
        ttk.Label(dialog, text="Temps par interaction:").grid(row=2, column=0, padx=5, pady=5)
        time_entry = ttk.Entry(dialog)
        time_entry.insert(0, "1.0")  # Default value
        time_entry.grid(row=2, column=1, padx=5, pady=5)

        def calculate():
            try:
                # Get user inputs
                sources = [int(s.strip()) for s in sources_entry.get().split(",")]
                target = int(target_spin.get())
                time_per_step = float(time_entry.get())
                
                # Call controller
                result = self.controller.min_time_to_infection(
                    sources, 
                    target,
                    time_per_step
                )
                
                # Display results
                if result is not None:
                    message = f"Temps minimum: {result:.2f} jour(s)"
                else:
                    message = "La cible n'est pas atteignable"
                    
                messagebox.showinfo("Résultat", message)
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides")

        ttk.Button(dialog, text="Calculer", command=calculate).grid(row=3, columnspan=2, pady=10)
        
        # Update spinbox range based on current graph
        if hasattr(self.controller, 'graphe'):
            max_node = max(0, self.controller.graphe.ordre - 1)
            target_spin.config(from_=0, to=max_node)



    def get_patient_zero_input(self):
        """Get the patient zero node from entry field"""
        try:
            return int(self.patient_zero_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de sommet valide")
            return None

    def get_simulation_parameters(self):
        """Returns the current simulation parameters"""
        try:
            infection = float(self.infection_prob.get())
            recovery = 0.0
            return infection, recovery
        except ValueError:
            messagebox.showerror("Erreur", "Paramètres de simulation invalides")
            return None, None

    def disable_simulation_controls(self):
        """Disable simulation buttons during simulation"""
        for child in self.winfo_children():
            if isinstance(child, ttk.Button):
                child.config(state=tk.DISABLED)

    def enable_simulation_controls(self):
        """Enable simulation buttons"""
        for child in self.winfo_children():
            if isinstance(child, ttk.Button):
                child.config(state=tk.NORMAL)

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