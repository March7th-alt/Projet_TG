from collections import deque, defaultdict
import random
from typing import Dict, List, Tuple, Optional, Set

def minimum_interactions(matrice_adj: List[List[int]], source: int, destination: int) -> None:
  
  """
    Question 12: Une fonction permettant de déterminer combien dinteractions suffisent à propager les
    virus dun individu à un autre.
    graph: Dict[int, List[int]]: matrice d'adjacence de graphe
    noeud1:int :Noeud source
    noeud2:int :Noeud destination
    -> Optional[int] : La fonctions retourne un eniter ou None

    en va trouver le plus cour chemin enter les deux noeuds et calculer le nombre des arcs entre eux;
  """

  if source == destination:
    print(f"Interactions minimales: 0 (chemin: [{source}])")
    return


  #Stocker le noeud courant, la distance entre le noeud courant et le source, et le chemin depuis le source vers le noeud courant
  n = len(matrice_adj)
  file = deque()
  file.append((source, 0, [source]))

  #Pour garder une trace sur les noeuds qu'on a deja visitée (on utilise le set pour eviter le passage par un noeud plusieur fois)
  visitee = set()
  visitee.add(source)
    
  while file:
    courant, distance, chemin= file.popleft()
        
    for voisin in range(n):
      if matrice_adj[courant][voisin] == 1:
        if voisin == destination:
          print(f"Interactions minimales: {distance + 1} Chemin: {chemin + [voisin]})")
          return
        if voisin not in visitee:
          visitee.add(voisin)
          file.append((voisin, distance + 1, chemin+ [voisin]))
  
  print("Aucun chemin trouvé entre le source et la destination.")


def super_contaminateur(adj_matrix: List[List[int]]) -> List[int]:
    """
    Finds a Hamiltonian path using an adjacency matrix representation.
    
    Args:
        ad_matrix: Square matrix where adj_matrix[i][j] == 1 indicates an edge
        
    Returnsj:
        List of node indices representing the path, or empty list if none found
    """
    def backtrack(current: int, path: List[int], visited: List[bool]) -> Optional[List[int]]:
        if len(path) == len(adj_matrix):
            return path.copy()
        
        # Get all possible neighbors
        neighbors = [i for i, connected in enumerate(adj_matrix[current]) 
                    if connected == 1 and not visited[i]]
        random.shuffle(neighbors)
        
        for neighbor in neighbors:
            visited[neighbor] = True
            path.append(neighbor)
            
            result = backtrack(neighbor, path, visited)
            if result is not None:
                return result
                
            path.pop()
            visited[neighbor] = False
        
        return None


    #si graphe vide, retourner liste vide
    if not adj_matrix:
        return []
    
    n = len(adj_matrix) #n = nombre des noeuds
    nodes = list(range(n)) #on met les noueds dans une liste
    random.shuffle(nodes) #Shuffle les noeuds
    
    for debut in nodes:
        visited = [False] * n #mettre tout les noeuds a false (on a pas visite tout les noeuds)
        visited[debut] = True #on met le noeud 'debut' a true (car on a visite ce noeud)
        path = [debut] #on ajoute debut dans le chemin pour demarer
        
        result = backtrack(debut, path, visited)
        if result is not None:
            return result
    
    return []


    #test:

    ma = [
    [0, 1, 1, 1, 0],
    [1, 0, 1, 0, 0], 
    [1, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 1, 0]
    ]

    minimum_interactions(ma,4,4)