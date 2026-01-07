"""
Player - Carro do jogador.
"""
import pygame
import math
from typing import List, Tuple, Optional
from .entities_base import Entity
from ..core.constants import (
    PLAYER_MAX_SPEED, PLAYER_ACCELERATION, PLAYER_FRICTION,
    SMOKE_COOLDOWN, TILE_SIZE
)
from ..core.assets import AssetManager
from ..core.collision import check_tile_collision


class Player(Entity):
    """Carro controlado pelo jogador."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 28, 28)
        
        # Movimento
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 0.0
        self.max_speed = PLAYER_MAX_SPEED
        self.acceleration = PLAYER_ACCELERATION
        self.friction = PLAYER_FRICTION
        
        # Direção (0=cima, 90=direita, 180=baixo, 270=esquerda)
        self.facing = 0.0
        self._target_angle = 0.0
        
        # Fumaça
        self.smoke_cooldown = 0.0
        self.can_smoke = True
        
        # Estado
        self.is_dead = False
        self._spawn_x = x
        self._spawn_y = y
        
        # Sprite
        self._load_sprite()
    
    def _load_sprite(self):
        """Carrega o sprite do jogador."""
        assets = AssetManager()
        self.sprite = assets.load_image("player_car.png", scale=(28, 28))
    
    @property
    def tile_pos(self) -> Tuple[int, int]:
        """Retorna posição no grid."""
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
    
    def handle_input(self, keys):
        """
        Processa input do jogador.
        
        Args:
            keys: Estado das teclas (pygame.key.get_pressed())
        """
        if self.is_dead:
            return
        
        # Direção do movimento
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
        
        # Acelera se há input
        if dx != 0 or dy != 0:
            # Calcula ângulo alvo
            self._target_angle = math.degrees(math.atan2(dy, dx)) + 90
            
            # Normaliza direção
            length = math.sqrt(dx * dx + dy * dy)
            dx /= length
            dy /= length
            
            # Acelera
            self.vx += dx * self.acceleration
            self.vy += dy * self.acceleration
        
        # Limita velocidade
        self.speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        if self.speed > self.max_speed:
            factor = self.max_speed / self.speed
            self.vx *= factor
            self.vy *= factor
            self.speed = self.max_speed
    
    def try_smoke(self) -> bool:
        """
        Tenta soltar fumaça.
        
        Returns:
            True se conseguiu soltar fumaça
        """
        if self.can_smoke and self.smoke_cooldown <= 0:
            self.smoke_cooldown = SMOKE_COOLDOWN
            self.can_smoke = False
            return True
        return False
    
    def update(self, dt: float, grid: Optional[List[List[int]]] = None):
        """Atualiza o jogador."""
        if self.is_dead:
            return
        
        # Atualiza cooldown da fumaça
        if self.smoke_cooldown > 0:
            self.smoke_cooldown -= dt
            if self.smoke_cooldown <= 0:
                self.can_smoke = True
        
        # Aplica atrito
        if self.speed > 0:
            friction_factor = 1.0 - self.friction
            self.vx *= friction_factor
            self.vy *= friction_factor
            self.speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
            
            if self.speed < 0.1:
                self.vx = 0
                self.vy = 0
                self.speed = 0
        
        # Movimento com colisão
        new_x = self.x + self.vx
        new_y = self.y + self.vy
        
        if grid:
            # Testa movimento X
            if not check_tile_collision(new_x, self.y, self.width * 0.8, self.height * 0.8, grid):
                self.x = new_x
            else:
                self.vx = 0
            
            # Testa movimento Y
            if not check_tile_collision(self.x, new_y, self.width * 0.8, self.height * 0.8, grid):
                self.y = new_y
            else:
                self.vy = 0
        else:
            self.x = new_x
            self.y = new_y
        
        # Atualiza ângulo suavemente
        if self.speed > 0.5:
            angle_diff = (self._target_angle - self.facing + 180) % 360 - 180
            self.facing += angle_diff * 0.3
            self.angle = self.facing
    
    def die(self):
        """Marca jogador como morto."""
        self.is_dead = True
        self.vx = 0
        self.vy = 0
        self.speed = 0
    
    def respawn(self, x: Optional[float] = None, y: Optional[float] = None):
        """Respawna o jogador."""
        self.x = x if x is not None else self._spawn_x
        self.y = y if y is not None else self._spawn_y
        self._spawn_x = self.x
        self._spawn_y = self.y
        self.vx = 0
        self.vy = 0
        self.speed = 0
        self.is_dead = False
        self.facing = 0
        self.angle = 0
    
    def get_smoke_position(self) -> Tuple[float, float]:
        """Retorna posição onde a fumaça deve ser criada."""
        # Posição atrás do carro
        angle_rad = math.radians(self.facing)
        offset = 20
        smoke_x = self.x - math.sin(angle_rad) * offset
        smoke_y = self.y + math.cos(angle_rad) * offset
        return smoke_x, smoke_y
