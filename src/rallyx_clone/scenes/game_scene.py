"""
Game Scene - Cena principal do gameplay.
"""
import pygame
from ..core.scene import Scene
from ..core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STATE_PAUSE, STATE_GAMEOVER,
    COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_GREEN,
    SCORE_FLAG, SCORE_COMPLETE
)
from ..core.assets import AssetManager
from ..core.audio import AudioManager
from ..core.timer import CountdownTimer
from ..gameplay.world import World
from ..gameplay.session import Session
from ..ui.hud import HUD


class GameScene(Scene):
    """Cena principal do jogo."""
    
    def __init__(self):
        super().__init__()
        
        self._assets = AssetManager()
        self._audio = AudioManager()
        
        # Componentes do jogo
        self._world = World()
        self._session = Session()
        self._hud = HUD(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Timer
        self._timer: CountdownTimer = None
        
        # Estado
        self._respawn_delay = 0.0
        self._victory_delay = 0.0
        self._engine_channel = None
    
    def on_enter(self, **kwargs):
        """Chamado ao entrar na cena."""
        # Carrega nível
        level_data = self._assets.load_data("level_01.json")
        self._world.load_level(level_data)
        
        # Configura sessão
        self._session.reset()
        self._session.flags_total = len(self._world.flags)
        
        # Configura timer
        self._timer = CountdownTimer(self._world.time_limit, self._time_out)
        
        # Reseta estado
        self._respawn_delay = 0.0
        self._victory_delay = 0.0
        
        # Inicia música e som do motor
        self._audio.play_music("music_loop.mp3")
        self._audio.play_sound("engine_loop.mp3", loops=-1)
    
    def on_exit(self):
        """Chamado ao sair da cena."""
        self._audio.stop_sound("engine_loop.mp3")
    
    def _time_out(self):
        """Chamado quando o tempo acaba."""
        if not self._session.is_victory and not self._session.is_game_over:
            self._session.time_out()
            self._audio.play_sound("lose.mp3")
            self._go_to_gameover()
    
    def _go_to_gameover(self):
        """Vai para game over."""
        self._audio.stop_sound("engine_loop.mp3")
        self.change_scene(STATE_GAMEOVER,
                         score=self._session.score,
                         high_score=self._session.high_score,
                         is_victory=self._session.is_victory,
                         is_new_high=self._session.is_new_high_score)
    
    def update(self, dt: float):
        """Atualiza a cena."""
        # Se em delay de respawn
        if self._respawn_delay > 0:
            self._respawn_delay -= dt
            if self._respawn_delay <= 0:
                self._world.respawn_player()
                self._world.respawn_enemies()
            return
        
        # Se em delay de vitória
        if self._victory_delay > 0:
            self._victory_delay -= dt
            if self._victory_delay <= 0:
                self._go_to_gameover()
            return
        
        # Se game over, não atualiza
        if self._session.is_game_over or self._session.is_victory:
            return
        
        # Atualiza timer
        self._timer.update(dt)
        
        # Input
        keys = pygame.key.get_pressed()
        
        # Fumaça
        if keys[pygame.K_SPACE]:
            if self._world.player and self._world.player.try_smoke():
                smoke_x, smoke_y = self._world.player.get_smoke_position()
                self._world.smoke_manager.create_smoke(smoke_x, smoke_y)
                self._audio.play_sound("smoke.mp3")
        
        # Atualiza mundo
        self._world.update(dt, keys)
        
        # Verifica coleta de bandeiras
        collected = self._world.check_flag_collection()
        if collected > 0:
            for _ in range(collected):
                self._session.add_flag(SCORE_FLAG)
            self._audio.play_sound("pickup_flag.mp3")
        
        # Verifica vitória
        if self._world.all_flags_collected() and not self._session.is_victory:
            self._session.add_time_bonus(self._timer.time_left)
            self._session.victory(SCORE_COMPLETE)
            self._audio.stop_sound("engine_loop.mp3")
            self._audio.play_sound("win.mp3")
            self._victory_delay = 2.0  # Delay antes de ir para game over
            return
        
        # Verifica colisão com inimigos
        if self._world.check_enemy_collision():
            self._world.player.die()
            self._audio.play_sound("crash.mp3")
            
            if self._session.lose_life():
                # Game over
                self._audio.play_sound("lose.mp3")
                self._respawn_delay = 1.5
            else:
                # Respawn
                self._respawn_delay = 1.5
    
    def draw(self, screen: pygame.Surface):
        """Desenha a cena."""
        screen.fill(COLOR_BLACK)
        
        # Calcula offset da câmera
        camera_offset = self._world.get_camera_offset(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Desenha mundo
        self._world.draw(screen, camera_offset)
        
        # Desenha HUD
        time_left = self._timer.time_left if self._timer else 0
        self._hud.draw(screen, self._world, self._session, time_left)
        
        # Mensagens de estado
        if self._respawn_delay > 0:
            if self._session.is_game_over:
                self._hud.draw_message(screen, "GAME OVER", COLOR_RED)
            else:
                self._hud.draw_message(screen, "PERDEU UMA VIDA!", COLOR_RED)
        
        if self._victory_delay > 0:
            self._hud.draw_message(screen, "VITÓRIA!", COLOR_GREEN)
    
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._audio.pause_music()
                self._audio.stop_sound("engine_loop.mp3")
                self.change_scene(STATE_PAUSE)
