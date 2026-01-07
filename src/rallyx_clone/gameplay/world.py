"""
World - Gerencia o mapa e entidades do jogo.
"""
import pygame
from typing import List, Tuple, Optional
from .player import Player
from .enemy import Enemy
from .flag import Flag
from .smoke import SmokeManager
from ..core.constants import (
    TILE_SIZE, TILE_ROAD, TILE_WALL, TILE_GRASS, TILE_BORDER,
    DIFFICULTY_SETTINGS
)
from ..core.assets import AssetManager
from ..core.config import Config


class World:
    """Gerencia o mundo do jogo."""
    
    def __init__(self):
        self.grid: List[List[int]] = []
        self.width = 0
        self.height = 0
        self.pixel_width = 0
        self.pixel_height = 0
        
        # Entidades
        self.player: Optional[Player] = None
        self.enemies: List[Enemy] = []
        self.flags: List[Flag] = []
        self.smoke_manager = SmokeManager()
        
        # Spawn points
        self.player_spawn: Tuple[int, int] = (1, 1)
        self.enemy_spawns: List[Tuple[int, int]] = []
        
        # Tempo limite
        self.time_limit = 120
        
        # Cache de tiles
        self._tile_cache: dict = {}
        self._surface_cache: Optional[pygame.Surface] = None
    
    def load_level(self, level_data: dict):
        """
        Carrega um nível do JSON.
        
        Args:
            level_data: Dados do nível
        """
        # Carrega grid
        self.grid = level_data.get("grid", [[0]])
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.height > 0 else 0
        self.pixel_width = self.width * TILE_SIZE
        self.pixel_height = self.height * TILE_SIZE
        
        # Carrega spawns
        self.player_spawn = tuple(level_data.get("player_spawn", [1, 1]))
        self.enemy_spawns = [tuple(s) for s in level_data.get("enemy_spawns", [])]
        
        # Carrega tempo limite
        config = Config()
        difficulty = config.difficulty
        time_bonus = DIFFICULTY_SETTINGS.get(difficulty, {}).get("time_bonus", 0)
        self.time_limit = level_data.get("time_limit", 120) + time_bonus
        
        # Carrega bandeiras
        flag_positions = level_data.get("flags", [])
        self.flags = [Flag.from_tile(f[0], f[1]) for f in flag_positions]
        
        # Cria jogador
        px = self.player_spawn[0] * TILE_SIZE + TILE_SIZE / 2
        py = self.player_spawn[1] * TILE_SIZE + TILE_SIZE / 2
        self.player = Player(px, py)
        
        # Cria inimigos baseado na dificuldade
        enemy_count = DIFFICULTY_SETTINGS.get(difficulty, {}).get("enemy_count", 3)
        enemy_speed = DIFFICULTY_SETTINGS.get(difficulty, {}).get("enemy_speed", 2.5)
        
        self.enemies = []
        for i, spawn in enumerate(self.enemy_spawns[:enemy_count]):
            ex = spawn[0] * TILE_SIZE + TILE_SIZE / 2
            ey = spawn[1] * TILE_SIZE + TILE_SIZE / 2
            self.enemies.append(Enemy(ex, ey, speed=enemy_speed))
        
        # Limpa fumaça
        self.smoke_manager.clear()
        
        # Invalida cache de renderização
        self._surface_cache = None
    
    def update(self, dt: float, keys):
        """Atualiza o mundo."""
        if not self.player:
            return
        
        # Atualiza jogador
        self.player.handle_input(keys)
        self.player.update(dt, self.grid)
        
        # Atualiza inimigos
        for enemy in self.enemies:
            # Verifica se inimigo está em fumaça
            if self.smoke_manager.check_entity(enemy.x, enemy.y):
                enemy.confuse()
            
            enemy.update(dt, (self.player.x, self.player.y), self.grid)
        
        # Atualiza fumaça
        self.smoke_manager.update(dt)
        
        # Atualiza bandeiras
        for flag in self.flags:
            flag.update(dt)
    
    def draw(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Desenha o mundo."""
        # Desenha mapa (com cache)
        self._draw_map(screen, camera_offset)
        
        # Desenha bandeiras
        for flag in self.flags:
            if not flag.collected:
                flag.draw(screen, camera_offset)
        
        # Desenha fumaça
        self.smoke_manager.draw(screen, camera_offset)
        
        # Desenha inimigos
        for enemy in self.enemies:
            enemy.draw(screen, camera_offset)
        
        # Desenha jogador
        if self.player:
            self.player.draw(screen, camera_offset)
    
    def _draw_map(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
        """Desenha o mapa com cache."""
        assets = AssetManager()
        
        # Cria cache se não existe
        if self._surface_cache is None:
            self._surface_cache = pygame.Surface((self.pixel_width, self.pixel_height))
            
            for ty, row in enumerate(self.grid):
                for tx, tile_type in enumerate(row):
                    tile_img = assets.load_tile(tile_type)
                    self._surface_cache.blit(
                        tile_img,
                        (tx * TILE_SIZE, ty * TILE_SIZE)
                    )
        
        # Desenha cache com offset
        screen.blit(self._surface_cache, (-camera_offset[0], -camera_offset[1]))
    
    def get_camera_offset(self, screen_width: int, screen_height: int) -> Tuple[float, float]:
        """
        Calcula offset da câmera centrada no jogador.
        
        Returns:
            Tupla (offset_x, offset_y)
        """
        if not self.player:
            return (0, 0)
        
        # Centraliza no jogador
        offset_x = self.player.x - screen_width / 2
        offset_y = self.player.y - screen_height / 2
        
        # Limita aos bounds do mapa
        offset_x = max(0, min(offset_x, self.pixel_width - screen_width))
        offset_y = max(0, min(offset_y, self.pixel_height - screen_height))
        
        return (offset_x, offset_y)
    
    def check_flag_collection(self) -> int:
        """
        Verifica coleta de bandeiras.
        
        Returns:
            Número de bandeiras coletadas neste frame
        """
        if not self.player:
            return 0
        
        collected = 0
        for flag in self.flags:
            if not flag.collected and flag.collides_with(self.player):
                flag.collect()
                collected += 1
        
        return collected
    
    def check_enemy_collision(self) -> bool:
        """
        Verifica colisão com inimigos.
        
        Returns:
            True se houve colisão
        """
        if not self.player or self.player.is_dead:
            return False
        
        for enemy in self.enemies:
            if enemy.active and self.player.collides_with(enemy):
                return True
        
        return False
    
    def respawn_player(self):
        """Respawna o jogador."""
        if self.player:
            px = self.player_spawn[0] * TILE_SIZE + TILE_SIZE / 2
            py = self.player_spawn[1] * TILE_SIZE + TILE_SIZE / 2
            self.player.respawn(px, py)
    
    def respawn_enemies(self):
        """Respawna todos os inimigos."""
        for i, enemy in enumerate(self.enemies):
            if i < len(self.enemy_spawns):
                spawn = self.enemy_spawns[i]
                ex = spawn[0] * TILE_SIZE + TILE_SIZE / 2
                ey = spawn[1] * TILE_SIZE + TILE_SIZE / 2
                enemy.respawn(ex, ey)
    
    def count_flags(self) -> Tuple[int, int]:
        """
        Conta bandeiras.
        
        Returns:
            Tupla (coletadas, total)
        """
        total = len(self.flags)
        collected = sum(1 for f in self.flags if f.collected)
        return collected, total
    
    def all_flags_collected(self) -> bool:
        """Retorna True se todas as bandeiras foram coletadas."""
        return all(f.collected for f in self.flags)
