"""
HUD - Interface durante o gameplay.
"""
import pygame
from typing import Tuple, Optional
from ..core.constants import (
    SCREEN_WIDTH, TILE_SIZE, COLOR_WHITE, COLOR_YELLOW, 
    COLOR_RED, COLOR_GREEN, COLOR_HUD_BG, COLOR_RADAR_BG
)
from ..core.assets import AssetManager
from ..gameplay.world import World
from ..gameplay.session import Session


class HUD:
    """HUD do jogo com score, tempo, vidas e radar."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fontes
        self._font_large = pygame.font.Font(None, 36)
        self._font_small = pygame.font.Font(None, 24)
        
        # Assets
        self._assets = AssetManager()
        self._life_icon = self._assets.load_image("icon_life.png", scale=(24, 24))
        
        # Radar
        self.radar_width = 150
        self.radar_height = 120
        self.radar_x = screen_width - self.radar_width - 10
        self.radar_y = 10
        self.radar_scale = 0.1  # Escala do mundo para o radar
    
    def draw(self, screen: pygame.Surface, world: World, session: Session,
             time_left: float):
        """
        Desenha o HUD completo.
        
        Args:
            screen: Surface para desenhar
            world: Mundo do jogo
            session: Sessão atual
            time_left: Tempo restante em segundos
        """
        self._draw_score(screen, session)
        self._draw_time(screen, time_left)
        self._draw_lives(screen, session)
        self._draw_flags(screen, session, world)
        self._draw_radar(screen, world)
    
    def _draw_score(self, screen: pygame.Surface, session: Session):
        """Desenha pontuação."""
        score_text = f"SCORE: {session.score:06d}"
        score_surf = self._font_large.render(score_text, True, COLOR_WHITE)
        screen.blit(score_surf, (10, 10))
        
        # High score
        high_text = f"HI: {session.high_score:06d}"
        high_surf = self._font_small.render(high_text, True, COLOR_YELLOW)
        screen.blit(high_surf, (10, 45))
    
    def _draw_time(self, screen: pygame.Surface, time_left: float):
        """Desenha tempo restante."""
        minutes = int(time_left) // 60
        seconds = int(time_left) % 60
        
        # Cor muda quando tempo está acabando
        color = COLOR_RED if time_left < 30 else COLOR_WHITE
        
        time_text = f"TIME: {minutes:02d}:{seconds:02d}"
        time_surf = self._font_large.render(time_text, True, color)
        time_rect = time_surf.get_rect(midtop=(self.screen_width // 2, 10))
        screen.blit(time_surf, time_rect)
    
    def _draw_lives(self, screen: pygame.Surface, session: Session):
        """Desenha vidas."""
        x = 10
        y = self.screen_height - 40
        
        lives_text = "LIVES:"
        lives_surf = self._font_small.render(lives_text, True, COLOR_WHITE)
        screen.blit(lives_surf, (x, y))
        
        # Ícones de vida
        icon_x = x + lives_surf.get_width() + 10
        for i in range(session.lives):
            screen.blit(self._life_icon, (icon_x + i * 28, y - 2))
    
    def _draw_flags(self, screen: pygame.Surface, session: Session, world: World):
        """Desenha contador de bandeiras."""
        collected, total = world.count_flags()
        
        flags_text = f"FLAGS: {collected}/{total}"
        color = COLOR_GREEN if collected == total else COLOR_WHITE
        flags_surf = self._font_large.render(flags_text, True, color)
        flags_rect = flags_surf.get_rect(topleft=(10, 70))
        screen.blit(flags_surf, flags_rect)
    
    def _draw_radar(self, screen: pygame.Surface, world: World):
        """Desenha mini-map radar."""
        # Fundo do radar
        radar_rect = pygame.Rect(self.radar_x, self.radar_y,
                                  self.radar_width, self.radar_height)
        pygame.draw.rect(screen, COLOR_RADAR_BG, radar_rect)
        pygame.draw.rect(screen, COLOR_WHITE, radar_rect, 2)
        
        # Calcula escala
        if world.pixel_width > 0 and world.pixel_height > 0:
            scale_x = (self.radar_width - 4) / world.pixel_width
            scale_y = (self.radar_height - 4) / world.pixel_height
            scale = min(scale_x, scale_y)
        else:
            scale = 0.1
        
        # Offset para centralizar
        radar_world_w = world.pixel_width * scale
        radar_world_h = world.pixel_height * scale
        offset_x = self.radar_x + 2 + (self.radar_width - 4 - radar_world_w) / 2
        offset_y = self.radar_y + 2 + (self.radar_height - 4 - radar_world_h) / 2
        
        # Desenha bandeiras (amarelo)
        for flag in world.flags:
            if not flag.collected:
                fx = int(offset_x + flag.x * scale)
                fy = int(offset_y + flag.y * scale)
                pygame.draw.circle(screen, COLOR_YELLOW, (fx, fy), 3)
        
        # Desenha inimigos (vermelho)
        for enemy in world.enemies:
            ex = int(offset_x + enemy.x * scale)
            ey = int(offset_y + enemy.y * scale)
            pygame.draw.circle(screen, COLOR_RED, (ex, ey), 3)
        
        # Desenha jogador (verde)
        if world.player:
            px = int(offset_x + world.player.x * scale)
            py = int(offset_y + world.player.y * scale)
            pygame.draw.circle(screen, COLOR_GREEN, (px, py), 4)
    
    def draw_message(self, screen: pygame.Surface, text: str,
                     color: Tuple[int, int, int] = COLOR_WHITE,
                     y_offset: int = 0):
        """Desenha mensagem centralizada."""
        msg_surf = self._font_large.render(text, True, color)
        msg_rect = msg_surf.get_rect(center=(
            self.screen_width // 2,
            self.screen_height // 2 + y_offset
        ))
        
        # Fundo semi-transparente
        bg_rect = msg_rect.inflate(20, 10)
        bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 180))
        screen.blit(bg_surf, bg_rect)
        
        screen.blit(msg_surf, msg_rect)
