"""
Flag - Bandeiras coletáveis.
"""
import pygame
import math
from typing import Tuple
from .entities_base import Entity
from ..core.constants import TILE_SIZE
from ..core.assets import AssetManager


class Flag(Entity):
    """Bandeira coletável no mapa."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 24, 24)
        
        self.collected = False
        self._animation_time = 0.0
        self._base_y = y
        
        # Carrega sprite
        self._load_sprite()
    
    def _load_sprite(self):
        """Carrega sprite da bandeira."""
        assets = AssetManager()
        self.sprite = assets.load_image("flag.png", scale=(24, 24))
    
    @property
    def tile_pos(self) -> Tuple[int, int]:
        """Retorna posição no grid."""
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
    
    def update(self, dt: float):
        """Atualiza animação da bandeira."""
        if self.collected:
            return
        
        # Animação de flutuação suave
        self._animation_time += dt * 3
        self.y = self._base_y + math.sin(self._animation_time) * 3
    
    def collect(self) -> bool:
        """
        Coleta a bandeira.
        
        Returns:
            True se foi coletada (não estava já coletada)
        """
        if self.collected:
            return False
        
        self.collected = True
        self.active = False
        return True
    
    def reset(self):
        """Reseta a bandeira."""
        self.collected = False
        self.active = True
        self.y = self._base_y
        self._animation_time = 0.0
    
    @classmethod
    def from_tile(cls, tx: int, ty: int) -> "Flag":
        """
        Cria uma bandeira em uma posição de tile.
        
        Args:
            tx, ty: Coordenadas do tile
        
        Returns:
            Nova instância de Flag
        """
        x = tx * TILE_SIZE + TILE_SIZE / 2
        y = ty * TILE_SIZE + TILE_SIZE / 2
        return cls(x, y)
