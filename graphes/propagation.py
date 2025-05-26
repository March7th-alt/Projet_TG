from collections import deque, defaultdict
import random
from typing import Dict, List, Tuple, Optional, Set

def minimum_interactions(matrice_adj: List[List[int]], source: int, destination: int) -> Dict:
  
  """
    Question 12: Une fonction permettant de déterminer combien dinteractions suffisent à propager les
    virus dun individu à un autre.
    graph: Dict[int, List[int]]: matrice d'adjacence de graphe
    noeud1:int :Noeud source
    noeud2:int :Noeud destination
    -> Optional[int] : La fonctions retourne un eniter ou None

    en va trouver le plus cour chemin enter les deux noeuds et calculer le nombre des arcs entre eux;
  """
  result = {
        'success': False,
        'interactions': None,
        'path': [],
        'message': "",
        'source': source,
        'destination': destination
    }

  if source == destination:
    return{
            'success': True,
            'message': "Source et destination sont les meme"
    }


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
          return {
                        'success': True,
                        'interactions': distance + 1,
                        'path': chemin + [voisin],
          }
        if voisin not in visitee:
          visitee.add(voisin)
          file.append((voisin, distance + 1, chemin+ [voisin]))
  
  result['message'] = "No path found between nodes"
  return result


def super_contaminateur(adj_matrix: List[List[int]]) -> dict:
    """
    Finds a Hamiltonian path using an adjacency matrix representation.
    
    Args:
        ad_matrix: Square matrix where adj_matrix[i][j] == 1 indicates an edge
        
    Returnsj:
        List of node indices representing the path, or empty list if none found
    """
    result = {
        'success': False,
        'path': [],
        'message': "Aucun super contaminateur trouvé",
        'node_count': len(adj_matrix)
    }

    if not adj_matrix:
        result['message'] = "Graphe vide"
        return result

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
            
            found_path = backtrack(neighbor, path, visited)
            if found_path is not None:
                return found_path
                
            path.pop()
            visited[neighbor] = False
        
        return None

    
    n = len(adj_matrix) #n = nombre des noeuds
    nodes = list(range(n)) #on met les noueds dans une liste
    random.shuffle(nodes) #Shuffle les noeuds
    
    for debut in nodes:
        visited = [False] * n #mettre tout les noeuds a false (on a pas visite tout les noeuds)
        visited[debut] = True #on met le noeud 'debut' a true (car on a visite ce noeud)
        path = [debut] #on ajoute debut dans le chemin pour demarer

        hamiltonian_path = backtrack(debut, path, visited)
        if hamiltonian_path:
            result.update({
                'success': True,
                'path': hamiltonian_path,
                'message': f"Super contaminateur de longueur {len(hamiltonian_path)} trouvé"
            })
            return result
    
    return result

def assign_risk_states(adj_matrix: List[List[int]], 
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
    n = len(adj_matrix)
    states = {node: 'healthy' for node in range(n)}
    
    # Set initial infected
    for node in initial_infected:
        if node <n:
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
                for neighbor, connected in enumerate(adj_matrix[node]):
                    if connected and states[neighbor] == 'healthy' and random.random() < infection_prob:
                        new_infections.add(neighbor)
    
    # Apply new infections
    for node in new_infections:
        states[node] = 'infected'
    
    return states


def detect_isolated_groups(adj_matrix: List[List[int]]) -> Dict:
    """
    Question 15: Detect isolated groups or critical zones in the contact network.
    
    Uses BFS to find all connected components in the graph.
    
    Args:
        graph: Adjacency list representing the contact network
        
    Returns:
        List of sets, where each set contains nodes in an isolated group
    """
    n = len(adj_matrix)
    visited = set()
    visited = [False] * n
    components = []
    
    for node in range(n):
        if node not in visited:
            # Start BFS for this component
            queue = deque([node])
            visited.add(node)
        if not visited[node]:
            queue = [node]
            visited[node] = True
            component = set()
            
            while queue:
                current = queue.popleft()
                current = queue.pop()
                component.add(current)
                
                for neighbor in range(n):
                    if adj_matrix[current][neighbor] and neighbor not in visited:
                        visited.add(neighbor)
                    if adj_matrix[current][neighbor] and not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            
            components.append(component)

    # Critical nodes/edges detection (simplified)
    critical_nodes = set()
    critical_edges = set()

    # For each node, check if removing it increases components
    original_components = len(components)
    for node in range(n):
        temp_adj = [row.copy() for row in adj_matrix]
        # Remove node (clear its row/column)
        for i in range(n):
            temp_adj[node][i] = 0
            temp_adj[i][node] = 0
        
        # Recalculate components
        new_components = len(detect_components(temp_adj))
        if new_components > original_components:
            critical_nodes.add(node)
    
    # Similarly for edges (exercise left for you)
    
    return {
        'components': components,
        'critical_nodes': list(critical_nodes),
        'critical_edges': list(critical_edges),  # Implement similarly
        'is_critical': len(critical_nodes) > 0
    }
      
def detect_components(adj_matrix):
    """Helper for component detection"""
    n = len(adj_matrix)
    visited = [False] * n
    components = []
    for node in range(n):
        if not visited[node]:
            component = set()
            stack = [node]
            visited[node] = True
            while stack:
                current = stack.pop()
                component.add(current)
                for neighbor in range(n):
                    if adj_matrix[current][neighbor] and not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)
            components.append(component)
    return components


def minimum_time_to_infection(adj_matrix: List[List[int]], 
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
    n = len(adj_matrix)
    if target in sources:
        return 0.0
    
    visited = set(sources)
    queue = deque([(source, 0) for source in sources])
    
    while queue:
        current, distance = queue.popleft()
        
        for neighbor in range(n):
          if adj_matrix[current][neighbor]:  
            if neighbor == target:
                return (distance + 1) * time_per_interaction
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    
    return None  # Target not reachable


def simulate_transmission_flows(adj_matrix: List[List[int]], 
                               initial_infected: List[int], 
                               steps: int = 10,
                               infection_prob: float = 0.5,
                               recovery_prob: float = 0.2) -> List[Dict[int, str]]:
    """
    Question 17: Simulate transmission flows over multiple time steps.
    
    Args:
        graph: Adjacency list representing the contact network
        initial_infected: List of initially infected individuals
        steps: Number of time steps to simulate
        infection_prob: Probability of transmission per contact
        recovery_prob: Probability an infected individual recovers and becomes immune
        
    Returns:
        List of state dictionaries for each time step
    """
    n = len(adj_matrix)
    simulation_history = []
    
    # Initialize states
    states = {node: 'healthy' for node in range(n)}
    for node in initial_infected:
        if node < n:
            states[node] = 'infected'
    simulation_history.append(states.copy())
    
    for _ in range(1, steps):
        new_states = states.copy()
        
        # Process recovery and immunity
        for node in range(n):
            if states[node] == 'infected':
                if random.random() < recovery_prob:
                    new_states[node] = 'immune'
        
        # Process new infections
        for node in range(n):
            if states[node] == 'infected':
                for neighbor in range(n):
                    if adj_matrix[node][neighbor] and states[neighbor] == 'healthy' and random.random() < infection_prob:
                        new_states[neighbor] = 'infected'
        
        states = new_states
        simulation_history.append(states.copy())
    
    return simulation_history
