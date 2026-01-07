"""
Smoke - Sistema de fumaça defensiva.
"""
import pygame
from typing import List, Tuple
from .entities_base import Entity
from ..core.constants import SMOKE_DURATION, SMOKE_RADIUS
from ..core.assets import AssetManager
from ..core.collision import check_circle_collision


class Smoke(Entity):
    """Nuvem de fumaça individual."""
    
    def __init__(self, x: float, y: float, duration: float = SMOKE_DURATION):
        super().__init__(x, y, SMOKE_RADIUS * 2, SMOKE_RADIUS * 2)
        
        self.duration = duration
        self.elapsed = 0.0
        self.radius = SMOKE_RADIUS
        
        # Carrega sprite
        self._load_sprite()
    
    def _load_sprite(self):
        """Carrega sprite da fumaça."""
        assets = AssetManager()
        size = int(self.radius * 2)
        self.sprite = assets.load_image("smoke.png", scale=(size, size))
    
    @property
    def progress(self) -> float:
        """Retorna progresso de 0.0 a 1.0."""
        return min(1.0, self.elapsed / self.duration)
    
    @property
    def alpha(self) -> int:
        """Retorna alfa atual (fade out)."""
        # Fade out nos últimos 30%
        if self.progress > 0.7:
            fade = 1.0 - ((self.progress - 0.7) / 0.3)
            return int(255 * fade)
        return 255
    
    def update(self, dt: float):
        """Atualiza a fumaça."""
        self.elapsed += dt
        
        if self.elapsed >= self.duration:
            self.active = False
    
    def draw(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Desenha a fumaça com fade."""
        if not self.active or not self._sprite:
            return
        
        # Copia sprite para aplicar alpha
        temp = self._sprite.copy()
        temp.set_alpha(self.alpha)
        
        screen_x = self.x - camera_offset[0] - self.width / 2
        screen_y = self.y - camera_offset[1] - self.height / 2
        
        screen.blit(temp, (screen_x, screen_y))
    
    def contains_point(self, x: float, y: float) -> bool:
        """Verifica se um ponto está dentro da fumaça."""
        dx = x - self.x
        dy = y - self.y
        return dx * dx + dy * dy <= self.radius * self.radius


class SmokeManager:
    """Gerencia todas as instâncias de fumaça."""
    
    def __init__(self):
        self.smokes: List[Smoke] = []
    
    def create_smoke(self, x: float, y: float) -> Smoke:
        """
        Cria uma nova fumaça.
        
        Args:
            x, y: Posição central
        
        Returns:
            Instância da fumaça criada
        """
        smoke = Smoke(x, y)
        self.smokes.append(smoke)
        return smoke
    
    def update(self, dt: float):
        """Atualiza todas as fumaças."""
        for smoke in self.smokes:
            smoke.update(dt)
        
        # Remove fumaças inativas
        self.smokes = [s for s in self.smokes if s.active]
    
    def draw(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Desenha todas as fumaças."""
        for smoke in self.smokes:
            smoke.draw(screen, camera_offset)
    
    def check_entity(self, x: float, y: float) -> bool:
        """
        Verifica se uma entidade está em qualquer fumaça.
        
        Args:
            x, y: Posição da entidade
        
        Returns:
            True se está em fumaça ativa
        """
        for smoke in self.smokes:
            if smoke.active and smoke.contains_point(x, y):
                return True
        return False
    
    def clear(self):
        """Remove todas as fumaças."""
        self.smokes.clear()
