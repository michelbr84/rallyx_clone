"""
Enemy - Carros inimigos com IA.
"""
import pygame
import math
import random
from typing import List, Tuple, Optional
from .entities_base import Entity
from ..core.constants import (
    ENEMY_SPEED, ENEMY_CONFUSED_DURATION, ENEMY_PATH_RECALC_INTERVAL,
    TILE_SIZE, SMOKE_SLOW_FACTOR
)
from ..core.assets import AssetManager
from ..core.pathfinding import bfs_pathfind, get_direction_to_tile
from ..core.collision import check_tile_collision


class Enemy(Entity):
    """Carro inimigo com IA de perseguição."""
    
    # Estados
    STATE_CHASE = "chase"
    STATE_CONFUSED = "confused"
    STATE_RESPAWN = "respawn"
    
    def __init__(self, x: float, y: float, speed: float = ENEMY_SPEED):
        super().__init__(x, y, 28, 28)
        
        # Movimento
        self.base_speed = speed
        self.speed = speed
        self.vx = 0.0
        self.vy = 0.0
        
        # IA
        self.state = self.STATE_CHASE
        self.path: List[Tuple[int, int]] = []
        self.path_index = 0
        self.target_tile: Optional[Tuple[int, int]] = None
        
        # Timers
        self.path_recalc_timer = 0.0
        self.confused_timer = 0.0
        
        # Spawn
        self._spawn_x = x
        self._spawn_y = y
        
        # Sprite
        self._load_sprite()
    
    def _load_sprite(self):
        """Carrega o sprite do inimigo."""
        assets = AssetManager()
        self.sprite = assets.load_image("enemy_car.png", scale=(28, 28))
    
    @property
    def tile_pos(self) -> Tuple[int, int]:
        """Retorna posição no grid."""
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
    
    def update(self, dt: float, player_pos: Tuple[float, float],
               grid: List[List[int]]):
        """
        Atualiza o inimigo.
        
        Args:
            dt: Delta time
            player_pos: Posição do jogador
            grid: Grid do mapa
        """
        if not self.active:
            return
        
        # Atualiza estado confuso
        if self.state == self.STATE_CONFUSED:
            self.confused_timer -= dt
            self.speed = self.base_speed * SMOKE_SLOW_FACTOR
            
            if self.confused_timer <= 0:
                self.state = self.STATE_CHASE
                self.speed = self.base_speed
                self.path = []  # Força recálculo
        
        # Atualiza timer de recálculo de caminho
        self.path_recalc_timer -= dt
        
        # Recalcula caminho se necessário
        if self.path_recalc_timer <= 0 or not self.path:
            self._calculate_path(player_pos, grid)
            self.path_recalc_timer = ENEMY_PATH_RECALC_INTERVAL
            
            # Adiciona variação quando confuso
            if self.state == self.STATE_CONFUSED:
                self.path_recalc_timer += random.uniform(0.5, 1.0)
        
        # Move em direção ao próximo tile do caminho
        self._follow_path(dt, grid)
        
        # Atualiza ângulo visual
        if self.vx != 0 or self.vy != 0:
            self.angle = math.degrees(math.atan2(self.vy, self.vx)) + 90
    
    def _calculate_path(self, player_pos: Tuple[float, float],
                        grid: List[List[int]]):
        """Calcula caminho até o jogador."""
        start = self.tile_pos
        goal = (int(player_pos[0] // TILE_SIZE), int(player_pos[1] // TILE_SIZE))
        
        # Quando confuso, pode escolher destino aleatório próximo
        if self.state == self.STATE_CONFUSED and random.random() < 0.5:
            # Destino aleatório próximo
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)
            goal = (goal[0] + offset_x, goal[1] + offset_y)
        
        self.path = bfs_pathfind(start, goal, grid)
        self.path_index = 0
    
    def _follow_path(self, dt: float, grid: List[List[int]]):
        """Segue o caminho calculado."""
        if not self.path or self.path_index >= len(self.path):
            self.vx = 0
            self.vy = 0
            return
        
        # Tile alvo atual
        target_tx, target_ty = self.path[self.path_index]
        target_x = target_tx * TILE_SIZE + TILE_SIZE / 2
        target_y = target_ty * TILE_SIZE + TILE_SIZE / 2
        
        # Distância até o centro do tile
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        # Chegou no tile?
        if dist < 4:
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.vx = 0
                self.vy = 0
                return
            # Próximo tile
            target_tx, target_ty = self.path[self.path_index]
            target_x = target_tx * TILE_SIZE + TILE_SIZE / 2
            target_y = target_ty * TILE_SIZE + TILE_SIZE / 2
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.sqrt(dx * dx + dy * dy)
        
        # Move em direção ao tile
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        
        # Aplica movimento com colisão
        new_x = self.x + self.vx
        new_y = self.y + self.vy
        
        if not check_tile_collision(new_x, self.y, self.width * 0.7, self.height * 0.7, grid):
            self.x = new_x
        
        if not check_tile_collision(self.x, new_y, self.width * 0.7, self.height * 0.7, grid):
            self.y = new_y
    
    def confuse(self, duration: float = ENEMY_CONFUSED_DURATION):
        """Coloca o inimigo em estado confuso."""
        self.state = self.STATE_CONFUSED
        self.confused_timer = duration
        self.path = []  # Força recálculo
    
    def respawn(self, x: Optional[float] = None, y: Optional[float] = None):
        """Respawna o inimigo."""
        self.x = x if x is not None else self._spawn_x
        self.y = y if y is not None else self._spawn_y
        self.vx = 0
        self.vy = 0
        self.state = self.STATE_CHASE
        self.speed = self.base_speed
        self.confused_timer = 0
        self.path = []
        self.active = True
