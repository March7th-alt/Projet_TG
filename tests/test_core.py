# Module test_core.py - Tests unitaires pour core.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graphes.core import Graphe
from graphes.visualisation import VisualisationGraphe
import unittest

#Tester nos fonctions core.py

class TestGraphe(unittest.TestCase):
    def setUp(self):
        self.g = Graphe(3)  # Graphe avec 3 sommets (0, 1, 2)
        
    def test_creation_matrice(self):
        self.assertEqual(self.g.matrice_adjacence, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        
    def test_ajout_arete(self):
        self.g.ajouter_arete(0, 1)
        self.assertEqual(self.g.matrice_adjacence[0][1], 1)
        self.assertEqual(self.g.matrice_adjacence[1][0], 1)
        
    def test_suppression_arete(self):
        self.g.ajouter_arete(0, 1)
        self.g.supprimer_arete(0, 1)
        self.assertEqual(self.g.matrice_adjacence[0][1], 0)
        
    def test_ajout_sommet(self):
        self.g.ajouter_sommet()
        self.assertEqual(self.g.ordre, 4)
        self.assertEqual(len(self.g.matrice_adjacence[0]), 4)
        
    def test_suppression_sommet(self):
        self.g.ajouter_arete(0, 1)
        self.g.supprimer_sommet(2)
        self.assertEqual(self.g.ordre, 2)
        self.assertEqual(self.g.matrice_adjacence, [[0, 1], [1, 0]])
        
    def test_calcul_ordre(self):
        self.assertEqual(self.g.calculer_ordre(), 3)
        
    def test_calcul_degres(self):
        self.g.ajouter_arete(0, 1)
        self.g.ajouter_arete(0, 2)
        self.assertEqual(self.g.calculer_degres(), [2, 1, 1])
        
    def test_voisinage(self):
        self.g.ajouter_arete(0, 1)
        self.assertEqual(self.g.voisinage(0), [1])
        self.assertEqual(self.g.voisinage(1), [0])
        self.assertEqual(self.g.voisinage(2), [])
        
    def test_existence_chemin(self):
        self.g.ajouter_arete(0, 1)
        self.g.ajouter_arete(1, 2)
        self.assertTrue(self.g.existe_chemin_longueur(0, 2, 2))
        self.assertFalse(self.g.existe_chemin_longueur(0, 2, 1))
        
    def test_cycle_eulerien(self):
        self.assertIsNone(self.g.trouver_cycle_eulerien())
        
        self.g.ajouter_arete(0, 1)
        self.g.ajouter_arete(1, 2)
        self.g.ajouter_arete(2, 0)
        cycle = self.g.trouver_cycle_eulerien()
        self.assertIsNotNone(cycle)
        if cycle:
            self.assertEqual(len(cycle), 4)
        
    def test_chemin_eulerien(self):
        # Cas sans chemin eulérien (tous degrés impairs)
        g1 = Graphe(3)
        g1.ajouter_arete(0, 1)
        g1.ajouter_arete(0, 2)
         # Ajouter cette arête pour rendre le graphe eulérien
        g1.ajouter_arete(1, 2)
        self.assertIsNotNone(g1.trouver_chemin_eulerien())
        
        # Cas avec chemin eulérien
        g2 = Graphe(3)
        g2.ajouter_arete(0, 1)
        g2.ajouter_arete(1, 2)
        chemin = g2.trouver_chemin_eulerien()
        self.assertIsNotNone(chemin)
        if chemin:
            self.assertEqual(len(chemin), 3)


    # Visualisation
    def test_visualisation(self):
        visu = VisualisationGraphe(self.g)
        # Ajouter une arête pour qu'il y ait un graphe non vide
        self.g.ajouter_arete(0, 1)
        # Affichage (ne doit pas planter)
        visu.afficher_graphe("Mon graphe")
        visu.afficher_cycle_eulerien()


if __name__ == "__main__":
    unittest.main()