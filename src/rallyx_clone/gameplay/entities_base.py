"""
Classe base Entity para entidades do jogo.
"""
import pygame
from typing import Tuple, Optional


class Entity:
    """Classe base para todas as entidades do jogo."""
    
    def __init__(self, x: float, y: float, width: int = 32, height: int = 32):
        """
        Cria uma entidade.
        
        Args:
            x, y: Posição central
            width, height: Dimensões
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = True
        
        self._sprite: Optional[pygame.Surface] = None
        self._angle = 0.0  # Rotação em graus
    
    @property
    def position(self) -> Tuple[float, float]:
        """Retorna posição central."""
        return self.x, self.y
    
    @position.setter
    def position(self, pos: Tuple[float, float]):
        self.x, self.y = pos
    
    @property
    def rect(self) -> pygame.Rect:
        """Retorna retângulo de colisão."""
        return pygame.Rect(
            self.x - self.width / 2,
            self.y - self.height / 2,
            self.width,
            self.height
        )
    
    @property
    def sprite(self) -> Optional[pygame.Surface]:
        """Retorna o sprite atual."""
        return self._sprite
    
    @sprite.setter
    def sprite(self, surface: pygame.Surface):
        self._sprite = surface
    
    @property
    def angle(self) -> float:
        """Retorna ângulo de rotação."""
        return self._angle
    
    @angle.setter
    def angle(self, value: float):
        self._angle = value % 360
    
    def set_sprite(self, surface: pygame.Surface):
        """Define o sprite."""
        self._sprite = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
    
    def update(self, dt: float):
        """
        Atualiza a entidade.
        
        Args:
            dt: Delta time em segundos
        """
        pass
    
    def draw(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """
        Desenha a entidade.
        
        Args:
            screen: Surface para desenhar
            camera_offset: Offset da câmera
        """
        if not self.active or not self._sprite:
            return
        
        # Calcula posição na tela
        screen_x = self.x - camera_offset[0] - self.width / 2
        screen_y = self.y - camera_offset[1] - self.height / 2
        
        # Rotaciona sprite se necessário
        if self._angle != 0:
            rotated = pygame.transform.rotate(self._sprite, -self._angle)
            rect = rotated.get_rect(center=(
                self.x - camera_offset[0],
                self.y - camera_offset[1]
            ))
            screen.blit(rotated, rect)
        else:
            screen.blit(self._sprite, (screen_x, screen_y))
    
    def collides_with(self, other: "Entity") -> bool:
        """Verifica colisão com outra entidade."""
        return self.rect.colliderect(other.rect)
    
    def distance_to(self, other: "Entity") -> float:
        """Calcula distância até outra entidade."""
        dx = other.x - self.x
        dy = other.y - self.y
        return (dx * dx + dy * dy) ** 0.5
