# Module core.py - Gestion de base des graphes via matrice d'adjacence
# Ce module implémente les opérations fondamentales sur les graphes non orientés.

from typing import List, Optional
import random

class Graphe:
    # Classe représentant un graphe via une matrice d'adjacence.
    # Attributes:
    #     matrice_adjacence (List[List[int]]): Matrice carrée représentant les arêtes
    #     ordre (int): Nombre de sommets dans le graphe
    
    def __init__(self, n: int = 0):
        # Initialise un graphe avec n sommets sans arêtes.
        # parametres:
        #     n (int): Nombre de sommets initiaux (défaut 0)
        self.matrice_adjacence = [[0] * n for _ in range(n)]
        self.ordre = n

    def ajouter_arete(self, sommet1: int, sommet2: int) -> None:
        # Ajoute une arête entre deux sommets (non orienté).
        # parametres:
        #     sommet1 (int): Index du premier sommet (0-based)
        #     sommet2 (int): Index du second sommet (0-based)

        #     IndexError: Si un sommet n'existe pas
        if sommet1 >= self.ordre or sommet2 >= self.ordre:
            raise IndexError("Un des sommets n'existe pas")
        
        self.matrice_adjacence[sommet1][sommet2] = 1
        self.matrice_adjacence[sommet2][sommet1] = 1  # Non orienté

    def supprimer_arete(self, sommet1: int, sommet2: int) -> None:
        # Supprime une arête entre deux sommets.
        # parametres:
        #     sommet1 (int): Index du premier sommet (0-based)
        #     sommet2 (int): Index du second sommet (0-based)
        if sommet1 < self.ordre and sommet2 < self.ordre:
            self.matrice_adjacence[sommet1][sommet2] = 0
            self.matrice_adjacence[sommet2][sommet1] = 0

    def ajouter_sommet(self) -> None:
        # Ajoute un nouveau sommet isolé au graphe.
        for ligne in self.matrice_adjacence:
            ligne.append(0)
        self.matrice_adjacence.append([0] * (self.ordre + 1))
        self.ordre += 1

    def supprimer_sommet(self, sommet: int) -> None:
        # Supprime un sommet et toutes ses arêtes incidentes.
        # parametres:
        #     sommet (int): Index du sommet à supprimer (0-based)

        #     IndexError: Si le sommet n'existe pas
        if sommet >= self.ordre:
            raise IndexError("Le sommet n'existe pas")
            
        del self.matrice_adjacence[sommet]
        for ligne in self.matrice_adjacence:
            del ligne[sommet]
        self.ordre -= 1

    def calculer_degres(self) -> List[int]:
        # Calcule le degré de chaque sommet.
        # Retourner:
        #     List[int]: Liste des degrés pour chaque sommet
        return [sum(ligne) for ligne in self.matrice_adjacence]

    def voisinage(self, sommet: int) -> List[int]:
        # Retourne la liste des voisins d'un sommet.
        # parametres:
        #     sommet (int): Index du sommet (0-based)

        # Retourner:
        #     List[int]: Indices des sommets voisins
        if sommet >= self.ordre:
            return []
        return [i for i, val in enumerate(self.matrice_adjacence[sommet]) if val == 1]

    def existe_chemin_longueur(self, depart: int, arrivee: int, longueur: int) -> bool:
        # Vérifie s'il existe un chemin de longueur exacte L entre deux sommets.
        # parametres
        #     depart (int): Sommet de départ
        #     arrivee (int): Sommet d'arrivée
        #     longueur (int): Longueur exacte recherchée
        # Retourner:
        #     bool: True si un tel chemin existe, False sinon
        if longueur == 0:
            return depart == arrivee
        if longueur == 1:
            return self.matrice_adjacence[depart][arrivee] == 1
            
        # On utilise une multiplication de matrices pour calculer les chemins
        resultat = self.matrice_adjacence
        for _ in range(longueur - 1):
            resultat = [[sum(a * b for a, b in zip(ligne, colonne)) 
                        for colonne in zip(*self.matrice_adjacence)] 
                       for ligne in resultat]
        return resultat[depart][arrivee] > 0

    def trouver_cycle_eulerien(self) -> Optional[List[int]]:
        # Trouve un cycle eulérien si le graphe en possède un.
        # Retourner:
        #     Optional[List[int]]: Liste des sommets du cycle ou None si inexistant
        degres = self.calculer_degres()
        if any(deg % 2 != 0 for deg in degres):
            return None  # Condition nécessaire non remplie
            
        # Algorithme de Hierholzer
        if self.ordre == 0:
            return None
            
        stack = [0]
        cycle = []
        while stack:
            sommet = stack[-1]
            voisins = self.voisinage(sommet)
            if voisins:
                suivant = voisins[0]
                stack.append(suivant)
                self.supprimer_arete(sommet, suivant)
            else:
                cycle.append(stack.pop())
        return cycle[::-1] if len(cycle) > 1 else None

    def trouver_chemin_eulerien(self) -> Optional[List[int]]:
        # Trouve un chemin eulérien si le graphe en possède un.

        # Retourner:
        #     Optional[List[int]]: Liste des sommets du chemin ou None si inexistant
        degres = self.calculer_degres()
        impairs = [i for i, deg in enumerate(degres) if deg % 2 != 0]
        
        if len(impairs) not in (0, 2):
            return None  # Doit avoir 0 ou 2 sommets de degré impair
            
        # Algorithme de Hierholzier
        if self.ordre == 0:
            return None
            
        depart = impairs[0] if impairs else 0
        stack = [depart]
        chemin = []
        while stack:
            sommet = stack[-1]
            voisins = self.voisinage(sommet)
            if voisins:
                suivant = voisins[0]
                stack.append(suivant)
                self.supprimer_arete(sommet, suivant)
            else:
                chemin.append(stack.pop())
        return chemin[::-1] if len(chemin) > 1 else None

    def generer_graphe_aleatoire(self, n: int, p: float) -> None:
        
        # Génère un graphe aléatoire avec n sommets et une probabilité p pour chaque arête.
        
        # retourner
        #    n (int): Nombre de sommets
        #    p (float): Probabilité qu'une arête existe entre deux sommets (0 <= p <= 1)

        if p < 0 or p > 1:
            raise ValueError("La probabilité p doit être entre 0 et 1")
        
        # Réinitialiser le graphe
        self.matrice_adjacence = [[0] * n for _ in range(n)]
        self.ordre = n
        
        # Générer les arêtes aléatoirement
        for i in range(n):
            for j in range(i+1, n):  # Éviter les boucles et les doublons
                if random.random() < p:
                    self.ajouter_arete(i, j)