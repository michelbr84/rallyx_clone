"""
Pathfinding BFS para inimigos.
"""
from collections import deque
from typing import List, Tuple, Optional
from .collision import is_tile_blocked


def bfs_pathfind(start: Tuple[int, int], goal: Tuple[int, int],
                 grid: List[List[int]], max_distance: int = 50) -> List[Tuple[int, int]]:
    """
    Encontra caminho usando BFS.
    
    Args:
        start: Tile inicial (tx, ty)
        goal: Tile destino (tx, ty)
        grid: Grid do mapa
        max_distance: Distância máxima de busca
    
    Returns:
        Lista de tiles do caminho (vazio se não encontrou)
    """
    if start == goal:
        return [goal]
    
    # BFS
    queue = deque([(start, [start])])
    visited = {start}
    
    # Direções: cima, baixo, esquerda, direita
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    while queue:
        (cx, cy), path = queue.popleft()
        
        # Limita distância
        if len(path) > max_distance:
            continue
        
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            
            if (nx, ny) in visited:
                continue
            
            if is_tile_blocked(nx, ny, grid):
                continue
            
            new_path = path + [(nx, ny)]
            
            if (nx, ny) == goal:
                return new_path
            
            visited.add((nx, ny))
            queue.append(((nx, ny), new_path))
    
    # Não encontrou caminho
    return []


def get_next_tile(start: Tuple[int, int], goal: Tuple[int, int],
                  grid: List[List[int]]) -> Optional[Tuple[int, int]]:
    """
    Retorna o próximo tile no caminho para o objetivo.
    
    Args:
        start: Tile atual
        goal: Tile destino
        grid: Grid do mapa
    
    Returns:
        Próximo tile ou None se bloqueado
    """
    path = bfs_pathfind(start, goal, grid)
    
    if len(path) > 1:
        return path[1]  # Próximo tile (índice 0 é o atual)
    
    return None


def get_direction_to_tile(current_x: float, current_y: float,
                          target_tx: int, target_ty: int,
                          tile_size: int) -> Tuple[float, float]:
    """
    Calcula direção normalizada para um tile.
    
    Args:
        current_x, current_y: Posição atual em pixels
        target_tx, target_ty: Tile destino
        tile_size: Tamanho do tile
    
    Returns:
        Tupla (dx, dy) normalizada
    """
    target_x = target_tx * tile_size + tile_size / 2
    target_y = target_ty * tile_size + tile_size / 2
    
    dx = target_x - current_x
    dy = target_y - current_y
    
    # Normaliza
    length = (dx * dx + dy * dy) ** 0.5
    if length > 0:
        dx /= length
        dy /= length
    
    return dx, dy
