import tkinter as tk
from tkinter import ttk
from graphes.creation import creer_graphe
from graphes.visualisation import afficher_graphe
from graphes.analyse import super_propagateurs

def lancer_interface():
    fenetre = tk.Tk()
    fenetre.title("Contrôle d'Épidémie")

    # Paramètres
    frame_param = ttk.LabelFrame(fenetre, text="Paramètres")
    frame_param.pack(padx=10, pady=5)

    # Slider pour le nombre de personnes
    ttk.Label(frame_param, text="Nombre de personnes:").grid(row=0, column=0)
    slider_n = ttk.Scale(frame_param, from_=10, to=200, orient="horizontal")
    slider_n.set(50)
    slider_n.grid(row=0, column=1)

    # Bouton de simulation
    def demarrer_simulation():
        n = int(slider_n.get())
        G = creer_graphe(n=n, p=0.02)
        
        # Infecte un nœud aléatoire
        import random
        patient_zero = random.choice(list(G.nodes()))
        G.nodes[patient_zero]["état"] = "infecté"
        
        # Affiche les super-propagateurs
        supers = super_propagateurs(G)
        print(f"Super-propagateurs: {supers}")
        
        afficher_graphe(G)

    ttk.Button(fenetre, 
               text="Lancer la Simulation", 
               command=demarrer_simulation).pack(pady=10)

    fenetre.mainloop()

if __name__ == "__main__":
    lancer_interface()