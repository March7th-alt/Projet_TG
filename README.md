PROJET DE THEORIE DES GRAPHES - SIMULATION DE PROPAGATION

Fonctionnalités principales :
- Création/modification de graphes (nœuds/arêtes)
- Algorithmes de graphes (Eulerien, Hamiltonien)
- Modèles de propagation épidémique (SIR/SIS)
- Visualisation interactive

INSTALLATION :
1. Python 3.8+ requis
2. Installer les dépendances :
   pip install networkx matplotlib numpy

UTILISATION :
1. Exécuter app_tkinter.py 

2. Fonctionnalités de l'interface :
   - Onglet "Création" : Ajouter/supprimer des éléments
   - Onglet "Algorithmes" : Exécuter des analyses
   - Onglet "Simulation" : Configurer les paramètres de propagation

FICHIERS IMPORTANTS :
- graphes/core.py : Structure de données des graphes
- graphes/propagation.py : Modèles de contagion
- interface/app_tkinter.py : Interface graphique

EXEMPLE DE SIMULATION :
1. Sélectionner "Patient Zéro"
2. Choisir les probabilités d'infection/rétablissement
3. Lancer la simulation avec "Démarrer"

DEPENDANCES :
- networkx==2.6.3
- matplotlib==3.4.3
- numpy==1.21.2