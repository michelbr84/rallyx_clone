"""
Sistema de detecção de colisão.
"""
import math
from typing import List, Tuple
from .constants import TILE_SIZE, TILE_WALL, TILE_BORDER


def check_tile_collision(x: float, y: float, width: float, height: float,
                         grid: List[List[int]]) -> bool:
    """
    Verifica colisão com tiles bloqueados.
    
    Args:
        x, y: Posição central da entidade
        width, height: Dimensões da entidade
        grid: Grid do mapa
    
    Returns:
        True se há colisão
    """
    # Calcula tiles que a entidade ocupa
    left = int((x - width / 2) // TILE_SIZE)
    right = int((x + width / 2) // TILE_SIZE)
    top = int((y - height / 2) // TILE_SIZE)
    bottom = int((y + height / 2) // TILE_SIZE)
    
    # Verifica cada tile
    for ty in range(top, bottom + 1):
        for tx in range(left, right + 1):
            if is_tile_blocked(tx, ty, grid):
                return True
    
    return False


def is_tile_blocked(tx: int, ty: int, grid: List[List[int]]) -> bool:
    """
    Verifica se um tile é bloqueado.
    
    Args:
        tx, ty: Coordenadas do tile
        grid: Grid do mapa
    
    Returns:
        True se o tile bloqueia passagem
    """
    # Fora do mapa = bloqueado
    if ty < 0 or ty >= len(grid) or tx < 0 or tx >= len(grid[0]):
        return True
    
    tile_type = grid[ty][tx]
    return tile_type in (TILE_WALL, TILE_BORDER)


def check_circle_collision(x1: float, y1: float, r1: float,
                           x2: float, y2: float, r2: float) -> bool:
    """
    Verifica colisão entre dois círculos.
    
    Args:
        x1, y1, r1: Centro e raio do primeiro círculo
        x2, y2, r2: Centro e raio do segundo círculo
    
    Returns:
        True se há colisão
    """
    dx = x2 - x1
    dy = y2 - y1
    dist_sq = dx * dx + dy * dy
    radius_sum = r1 + r2
    
    return dist_sq <= radius_sum * radius_sum


def check_rect_collision(rect1: Tuple[float, float, float, float],
                         rect2: Tuple[float, float, float, float]) -> bool:
    """
    Verifica colisão entre dois retângulos.
    
    Args:
        rect1, rect2: Tuplas (x, y, width, height)
    
    Returns:
        True se há colisão
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)


def get_tile_at(x: float, y: float) -> Tuple[int, int]:
    """
    Retorna as coordenadas do tile em uma posição.
    
    Args:
        x, y: Posição em pixels
    
    Returns:
        Tupla (tile_x, tile_y)
    """
    return int(x // TILE_SIZE), int(y // TILE_SIZE)


def tile_center(tx: int, ty: int) -> Tuple[float, float]:
    """
    Retorna a posição central de um tile.
    
    Args:
        tx, ty: Coordenadas do tile
    
    Returns:
        Tupla (center_x, center_y)
    """
    return tx * TILE_SIZE + TILE_SIZE / 2, ty * TILE_SIZE + TILE_SIZE / 2
