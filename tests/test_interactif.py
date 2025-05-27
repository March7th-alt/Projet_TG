# Test interactif pour graphes avec 200 sommets

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graphes.core import Graphe
from graphes.visualisation import VisualisationGraphe
import time

#Tester nos fonctions core.py

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def test_graphe_200_sommets():
    # Création du graphe
    g = Graphe()
    print("Création d'un graphe aléatoire avec 200 sommets...")
    g.generer_graphe_aleatoire(200, 0.1)  # 10% de probabilité d'arête
    
    # Statistiques de base
    print(f"\nGraphe créé avec {g.ordre} sommets")
    degres = g.calculer_degres()
    print(f"Degré moyen: {sum(degres)/len(degres):.2f}")
    print(f"Degré max: {max(degres)}")
    print(f"Degré min: {min(degres)}")
    
    return g

def menu_interactif(g):
    while True:
        clear_screen()
        print("\n" + "="*50)
        print("MENU INTERACTIF - GRAPHE 200 SOMMETS".center(50))
        print("="*50)
        print("\n1. Afficher les statistiques de base")
        print("2. Trouver un cycle eulérien")
        print("3. Trouver un chemin eulérien")
        print("4. Vérifier l'existence d'un chemin")
        print("5. Visualiser un sous-graphe (20 premiers sommets)")
        print("6. Quitter")
        
        choix = input("\nVotre choix (1-6): ")
        
        if choix == "1":
            clear_screen()
            print("\nSTATISTIQUES DU GRAPHE".center(50))
            print("-"*50)
            degres = g.calculer_degres()
            print(f"Nombre de sommets: {g.ordre}")
            print(f"Nombre d'arêtes: {sum(degres)//2}")
            print(f"Degré moyen: {sum(degres)/len(degres):.2f}")
            print(f"Degré max: {max(degres)} (sommet {degres.index(max(degres))})")
            print(f"Degré min: {min(degres)} (sommet {degres.index(min(degres))})")
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "2":
            clear_screen()
            print("\nRECHERCHE CYCLE EULERIEN".center(50))
            print("-"*50)
            debut = time.time()
            cycle = g.trouver_cycle_eulerien()
            duree = time.time() - debut
            
            if cycle:
                print(f"Cycle trouvé en {duree:.2f}s")
                print(f"Longueur du cycle: {len(cycle)}")
                print("\nExtrait du cycle (20 premiers éléments):")
                print(cycle[:20])
            else:
                print(f"Aucun cycle eulérien trouvé (temps: {duree:.2f}s)")
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "3":
            clear_screen()
            print("\nRECHERCHE CHEMIN EULERIEN".center(50))
            print("-"*50)
            debut = time.time()
            chemin = g.trouver_chemin_eulerien()
            duree = time.time() - debut
            
            if chemin:
                print(f"Chemin trouvé en {duree:.2f}s")
                print(f"Longueur du chemin: {len(chemin)}")
                print("\nExtrait du chemin (20 premiers éléments):")
                print(chemin[:20])
            else:
                print(f"Aucun chemin eulérien trouvé (temps: {duree:.2f}s)")
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "4":
            clear_screen()
            print("\nVERIFICATION CHEMIN".center(50))
            print("-"*50)
            try:
                s1 = int(input("Sommet de départ (0-199): "))
                s2 = int(input("Sommet d'arrivée (0-199): "))
                l = int(input("Longueur du chemin: "))
                
                if not (0 <= s1 < 200 and 0 <= s2 < 200):
                    raise ValueError
                    
                existe = g.existe_chemin_longueur(s1, s2, l)
                print(f"\nRésultat: {'EXISTE' if existe else 'N\'EXISTE PAS'}")
            except:
                print("\nErreur: saisie invalide")
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "5":
            clear_screen()
            print("\nVISUALISATION SOUS-GRAPHE".center(50))
            print("-"*50)
            
            # Création d'un sous-graphe pour la visualisation
            sous_graphe = Graphe(20)
            for i in range(20):
                for j in range(i+1, 20):
                    if g.matrice_adjacence[i][j]:
                        sous_graphe.ajouter_arete(i, j)
            
            visu = VisualisationGraphe(sous_graphe)
            visu.afficher_graphe("Sous-graphe (20 premiers sommets)")
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "6":
            print("\nAu revoir!")
            break
            
        else:
            print("\nChoix invalide!")
            time.sleep(1)

if __name__ == "__main__":
    clear_screen()
    print("TEST INTERACTIF - GRAPHE 200 SOMMETS".center(50))
    print("="*50)
    print("\nCe script va créer un graphe aléatoire avec 200 sommets")
    print("et vous permettre d'interagir avec différentes fonctionnalités.")
    print("\nAppuyez sur Entrée pour commencer...")
    input()
    
    g = test_graphe_200_sommets()
    input("\nAppuyez sur Entrée pour accéder au menu interactif...")
    menu_interactif(g)