"""
Module test_core.py - Tests unitaires pour core.py
"""

import unittest
from graphes.core import Graphe

class TestGraphe(unittest.TestCase):
    """Classe de tests pour les fonctionnalités de base du graphe"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.g = Graphe(3)  # Graphe avec 3 sommets
        
    def test_creation_matrice(self):
        """Test de création d'une matrice vide"""
        self.assertEqual(self.g.matrice_adjacence, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        
    def test_ajout_arete(self):
        """Test d'ajout d'arête"""
        self.g.ajouter_arete(0, 1)
        self.assertEqual(self.g.matrice_adjacence[0][1], 1)
        self.assertEqual(self.g.matrice_adjacence[1][0], 1)  # Non orienté
        
    def test_suppression_arete(self):
        """Test de suppression d'arête"""
        self.g.ajouter_arete(0, 1)
        self.g.supprimer_arete(0, 1)
        self.assertEqual(self.g.matrice_adjacence[0][1], 0)
        
    def test_ajout_sommet(self):
        """Test d'ajout de sommet"""
        self.g.ajouter_sommet()
        self.assertEqual(self.g.ordre, 4)
        self.assertEqual(len(self.g.matrice_adjacence[0]), 4)
        
    def test_suppression_sommet(self):
        """Test de suppression de sommet"""
        self.g.ajouter_arete(0, 1)
        self.g.supprimer_sommet(2)  # Supprime le dernier sommet
        self.assertEqual(self.g.ordre, 2)
        self.assertEqual(self.g.matrice_adjacence, [[0, 1], [1, 0]])
        
    def test_calcul_ordre(self):
        """Test du calcul de l'ordre"""
        self.assertEqual(self.g.calculer_ordre(), 3)
        
    def test_calcul_degres(self):
        """Test du calcul des degrés"""
        self.g.ajouter_arete(0, 1)
        self.g.ajouter_arete(0, 2)
        self.assertEqual(self.g.calculer_degres(), [2, 1, 1])
        
    def test_voisinage(self):
        """Test de la recherche de voisinage"""
        self.g.ajouter_arete(0, 1)
        self.assertEqual(self.g.voisinage(0), [1])
        self.assertEqual(self.g.voisinage(1), [0])
        self.assertEqual(self.g.voisinage(2), [])
        
    def test_existence_chemin(self):
        """Test de l'existence d'un chemin de longueur L"""
        self.g.ajouter_arete(0, 1)
        self.g.ajouter_arete(1, 2)
        self.assertTrue(self.g.existe_chemin_longueur(0, 2, 2))
        self.assertFalse(self.g.existe_chemin_longueur(0, 2, 1))
        
    def test_cycle_eulerien(self):
        """Test de détection de cycle eulérien"""
        # Graphe sans cycle eulérien
        self.assertIsNone(self.g.trouver_cycle_eulerien())
        
        # Graphe avec cycle eulérien
        self.g.ajouter_arete(0, 1)
        self.g.ajouter_arete(1, 2)
        self.g.ajouter_arete(2, 0)
        cycle = self.g.trouver_cycle_eulerien()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 4)  # 3 sommets + retour départ
        
    def test_chemin_eulerien(self):
        """Test de détection de chemin eulérien"""
        # Graphe sans chemin eulérien
        self.g.ajouter_arete(0, 1)
        self.g.ajouter_arete(0, 2)
        self.assertIsNone(self.g.trouver_chemin_eulerien())
        
        # Graphe avec chemin eulérien
        self.g.ajouter_arete(1, 2)
        chemin = self.g.trouver_chemin_eulerien()
        self.assertIsNotNone(chemin)
        self.assertEqual(len(chemin), 4)  # 3 sommets + arête

if __name__ == "__main__":
    unittest.main()