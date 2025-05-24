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

def assign_risk_states(graph: Dict[int, List[int]], 
                      initial_infected: List[int], 
                      infection_prob: float = 0.7,
                      recovery_prob: float = 0.1) -> Dict[int, str]:
    """
    Question 14: Assign risk states (healthy, infected, immune) to individuals 
    and simulate one step of propagation.
    
    Args:
        graph: Adjacency list representing the contact network
        initial_infected: List of initially infected individuals
        infection_prob: Probability of transmission per contact
        recovery_prob: Probability an infected individual recovers and becomes immune
        
    Returns:
        Dictionary mapping individuals to their states ('healthy', 'infected', 'immune')
    """
    states = {node: 'healthy' for node in graph}
    
    # Set initial infected
    for node in initial_infected:
        if node in states:
            states[node] = 'infected'
    
    # Determine new infections
    new_infections = set()
    for node, state in states.items():
        if state == 'infected':
            # With recovery_prob chance, recover
            if random.random() < recovery_prob:
                states[node] = 'immune'
            else:
                # Infect neighbors
                for neighbor in graph.get(node, []):
                    if states[neighbor] == 'healthy' and random.random() < infection_prob:
                        new_infections.add(neighbor)
    
    # Apply new infections
    for node in new_infections:
        states[node] = 'infected'
    
    return states


def detect_isolated_groups(graph: Dict[int, List[int]]) -> List[Set[int]]:
    """
    Question 15: Detect isolated groups or critical zones in the contact network.
    
    Uses BFS to find all connected components in the graph.
    
    Args:
        graph: Adjacency list representing the contact network
        
    Returns:
        List of sets, where each set contains nodes in an isolated group
    """
    visited = set()
    components = []
    
    for node in graph:
        if node not in visited:
            # Start BFS for this component
            queue = deque([node])
            visited.add(node)
            component = set()
            
            while queue:
                current = queue.popleft()
                component.add(current)
                
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
    
    return components


def minimum_time_to_infection(graph: Dict[int, List[int]], 
                             sources: List[int], 
                             target: int,
                             time_per_interaction: float = 1.0) -> Optional[float]:
    """
    Question 16: Calculate the minimum time for infection to reach a target from 
    any of the sources.
    
    Uses multi-source BFS where all sources start with distance 0.
    
    Args:
        graph: Adjacency list representing the contact network
        sources: List of source nodes where infection starts
        target: Target node to reach
        time_per_interaction: Time taken for one interaction
        
    Returns:
        Minimum time needed or None if target can't be reached
    """
    if target in sources:
        return 0.0
    
    visited = set(sources)
    queue = deque([(source, 0) for source in sources])
    
    while queue:
        current, distance = queue.popleft()
        
        for neighbor in graph.get(current, []):
            if neighbor == target:
                return (distance + 1) * time_per_interaction
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    
    return None  # Target not reachable


#test:

ma = [
  [0, 1, 1, 1, 0],
  [1, 0, 1, 0, 0], 
  [1, 1, 0, 1, 0],
  [1, 0, 1, 0, 1],
  [0, 0, 0, 1, 0]
]

dic = {
    0: [1, 2, 3],
    1: [0, 2],
    2: [0, 1, 3],
    3: [0, 2, 4],
    4: [3],
    5: []
}


minimum_interactions(ma, 4, 4)

print(super_contaminateur(ma))
print(assign_risk_states(dic, [0]))
print(detect_isolated_groups(dic))
print(minimum_time_to_infection(dic, [0], 4))

