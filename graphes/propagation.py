from collections import deque
import random
from typing import Dict, List, Optional

def minimum_interactions(matrice_adj: List[List[int]], source: int, destination: int) -> Dict:
  
  """
    Question 12: Une fonction permettant de déterminer combien dinteractions suffisent à propager les
    virus dun individu à un autre.

    matrice_adj: List[List[int]]: matrice d'adjacence de graphe
    Source:int :Noeud source
    Destination:int :Noeud destination
    -> Dict : La fonctions retourne un Dict qui nous aide a afficher le message apres

    en va trouver le plus cour chemin enter les deux noeuds et calculer le nombre des arcs entre eux;
  """

  # Initialisation de resultat
  result = {
        'success': False, #pour debugger
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

    #parcourir la liste des voisin de noeud courant    
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
    Question 13: Une fonction permettant de modéliser un super contaminateur qui peut visiter toute la population sans revenir deux fois. 
    donc, trouver chemin hamiltonien
    
    Param:
        ad_matrix: matrice carre for our adjacency matrix
        
    Returns:
        (same thing as Q12) a dict that helps us with affichage later, qui contient le chemin
    """

    # Initialisation
    result = {
        'success': False,
        'path': [],
        'message': "Aucun super contaminateur trouvé",
        'node_count': len(adj_matrix)
    }

    if not adj_matrix:
        result['message'] = "Graphe vide"
        return result

    # Une fonction recursive utilisee poir explorer tout les chemins possibles
    def backtrack(current: int, path: List[int], visited: List[bool]) -> Optional[List[int]]:

        #si the length of path = length de matrice, donc on a trouver le chemin hamiltonien
        if len(path) == len(adj_matrix):
            return path.copy()
        
        # prendre tout les voisins de noeud courant
        neighbors = [i for i, connected in enumerate(adj_matrix[current]) 
                    if connected == 1 and not visited[i]]
        random.shuffle(neighbors) #randomize the list of voisins (pour l'optimization)
        
        #parcourir liste des voisins
        for neighbor in neighbors:
            #ajouter le voisin dans liste des noeud visitee
            visited[neighbor] = True
            path.append(neighbor)
            
            #appel recursive pour explorer tout les chemin d'apres le voisin
            found_path = backtrack(neighbor, path, visited)
            #si on a trouver le path on le retourne
            if found_path is not None:
                return found_path
            
            #a la fin we backtrack
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

        hamiltonian_path = backtrack(debut, path, visited) #appeler la fonction pour trouver le chemin
        if hamiltonian_path: #si trouver, on le retourne
            result.update({
                'success': True,
                'path': hamiltonian_path,
                'message': f"Super contaminateur de longueur {len(hamiltonian_path)} trouvé"
            })
            return result
    
    return result

def assign_risk_states(adj_matrix: List[List[int]], 
                      initial_infected: List[int], 
                      infection_prob: float = 0.9,) -> Dict[int, str]:
    """
    Question 14: Assign risk states (healthy, infected, immune) to individuals 
    and simulate one step of propagation.
    
    param:
        graph: matrice d'adjacence
        initial_infected: liste des noeuds initialement
        infection_prob: Probabilite de transmission
        
    Returns:
        Dictionnaire qui nous donne l'etat de chaque noeud
    """
    n = len(adj_matrix)
    states = {node: 'healthy' for node in range(n)} #initialiser tout les noeud a "healthy"
    
    # mettre les noeud infectes a "infected"
    for node in initial_infected:
        if node <n:
            states[node] = 'infected'
    
    # Infecter les voisin (new infections)
    new_infections = set()
    for node, state in states.items():
                for neighbor, connected in enumerate(adj_matrix[node]):
                    if connected and states[neighbor] == 'healthy' and random.random() < infection_prob:
                        new_infections.add(neighbor)
    
    # mettre l'etat des nouveau infectee a "infected"
    for node in new_infections:
        states[node] = 'infected'
    
    return states


def detect_isolated_groups(adj_matrix: List[List[int]]) -> Dict:
    """
    Question 15: Detect isolated groups or critical zones in the contact network.
    
    Uses BFS pour trouver les composants connexe de graphe
    
    param:
        adj_matrix: matrice d'adjacence
        
    Retourner:
        Dict same thing
    """

    n = len(adj_matrix)
    
    #trouver les composants connexes
    components = detect_components(adj_matrix) #appeler fnct qui detect les composantq
    original_component_count = len(components) #calculer le nombre des composants
    
    #trouver noeuds critiques

    #NOTE: Pour moi les noeuds critiques c'etait les noeuds qui quand on l'elimine de graph, le nombre des composants connexes augmentent mais apparrament c'est les noeuds qui on le degree le plus elevée /mon algo ne marche pas dans tout les cas :'(  
    critical_nodes = set() #set pour eviter la repetition des noeuds
    for node in range(n):
        temp_adj = [row.copy() for row in adj_matrix] #creer une matrce d'adjacence temporaire ou le noeud n'existe pas (n'est pas connecte a aucun noeud)
        for i in range(n):
            temp_adj[node][i] = 0
            temp_adj[i][node] = 0
        
        #checker si l'elimination de ce noeud impact le nombre des composants connexe
        if len(detect_components(temp_adj)) > original_component_count:
            critical_nodes.add(node)
    return {
        'components': [list(c) for c in components],
        'critical_nodes': list(critical_nodes),
        'critical_edges': [],  # Implement similarly for edges
        'is_critical': len(critical_nodes) > 0,
        'message': ("Critical zones found!" if critical_nodes 
                   else "No critical zones found")
    }

#fnct qui detetct les composant connexe, utilisee dans la fct isolated groups
def detect_components(adj_matrix):
    """FCT qui trouve les composants connexe using BFS"""
    n = len(adj_matrix)
    visited = [False] * n
    components = []
    
    for node in range(n):
        if not visited[node]:
            #commencer un nv composant
            stack = [node] #stack pour keeping track of les noeuds that we are going to traiter
            visited[node] = True
            component = set() #composant
            
            while stack:
                current = stack.pop()
                component.add(current) #ajouter noeud a composant
                
                #ajouter les voisin de noeud au composant
                for neighbor in range(n):
                    if adj_matrix[current][neighbor] and not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)
            
            components.append(component) #ajouter le composants au liste des composants
    
    return components

def minimum_time_to_infection(adj_matrix: List[List[int]], sources: List[int], target: int, time_per_interaction: float = 1.0) -> Optional[float]:
    """
    Question 16: Calculate the minimum time for infection to reach a target from 
    any of the sources.
    
    Also BFS because c'est la fonction qui nous aide a parcourir le graph par "niveau"
    
    param
        adj_matrix: Matrice d'adjacence
        sources: liste des sources (in case on veut calculer le temps depuis plusieru noeuds infectee)
        target: destination
        time_per_interaction: Le temps pour infecter (initialiser a 1.0 (un jour pour arete))
        
    Retourner:
        temps minimal pour infecter
    """
    n = len(adj_matrix)
    if target in sources:
        return 0.0
    
    visited = set(sources)
    queue = deque([(source, 0) for source in sources]) #creer structure pour les sources
    
    while queue:
        current, distance = queue.popleft()
        
        #ajouter un a la distance a chaque fois qu'on visite un voisin
        for neighbor in range(n):
          if adj_matrix[current][neighbor]:  
            if neighbor == target:
                return (distance + 1) * time_per_interaction
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    
    return None  #On peut pas trouver le target


def simulate_transmission_flows(adj_matrix: List[List[int]], initial_infected: List[int], steps: int = 10, infection_prob: float = 0.9, vaccinated_nodes=[]) -> List[Dict[int, str]]:
    """
    Fonction utiliser pour simuler la propagation (flow de virus a travers le reseau)
    
    param:
        adj_matrix: matrice d'adjacence
        initial_infected: List des individus infectes
        steps: Nombre des etapes (la simulation ce fait en etapes)
        infection_prob: Probabilite de propagatiob
        vaccinated_nodes: List des noeuds vaccinees (pour le moment on peut vacciner un seul noeud)
        
    Retourner:
        List des dict pour chaque etape
    """

    n = len(adj_matrix)
    simulation_history = [] #garder trace des informations de chaque etapes
    
    # Initializer les etats des noeud
    states = {node: 'healthy' for node in range(n)}

    for node in initial_infected:
        if node < n:
            states[node] = 'infected'

    for node in vaccinated_nodes:
        if node < n:
            states[node] = 'immune'
    simulation_history.append(states.copy())
    
    for _ in range(1, steps):
        new_states = states.copy()
        
        for node in range(n):
            if node in vaccinated_nodes: #si noeud est vaccinee, on fait rien
                continue
        
        # Process new infections
        for node in range(n): #si noeud infectee, infecte ses voisin (selon la probabilite)
            if states[node] == 'infected':
                for neighbor in range(n):
                    if adj_matrix[node][neighbor] and states[neighbor] == 'healthy' and random.random() < infection_prob:
                        new_states[neighbor] = 'infected'
        
        states = new_states
        simulation_history.append(states.copy()) #ajouter les information de cette etape au historique
    
    return simulation_history
