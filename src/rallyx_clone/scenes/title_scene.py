"""
Title Scene - Tela inicial do jogo.
"""
import pygame
from ..core.scene import Scene
from ..core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STATE_OPTIONS, STATE_GAME,
    COLOR_BLACK, COLOR_WHITE, COLOR_YELLOW
)
from ..core.assets import AssetManager
from ..core.audio import AudioManager
from ..ui.menu import Menu
from ..ui.widgets import Label


class TitleScene(Scene):
    """Tela inicial com logo e menu."""
    
    def __init__(self):
        super().__init__()
        
        self._assets = AssetManager()
        self._audio = AudioManager()
        
        # Logo
        self._logo = self._assets.load_image("title.png", scale=(400, 200))
        self._logo_rect = self._logo.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Menu
        self._menu = Menu()
        center_x = SCREEN_WIDTH // 2
        self._menu.add_button("INICIAR JOGO", center_x, 320, self._start_game)
        self._menu.add_button("OPÇÕES", center_x, 380, self._open_options)
        self._menu.add_button("SAIR", center_x, 440, self._quit_game)
        
        # Instruções
        self._instructions = [
            Label("SETAS ou WASD: Mover", SCREEN_WIDTH // 2, 520, 20, COLOR_WHITE),
            Label("ESPAÇO: Fumaça  |  ESC: Pausar", SCREEN_WIDTH // 2, 545, 20, COLOR_WHITE),
        ]
        
        # Copyright
        self._copyright = Label("© 2024 Rally-X Clone", SCREEN_WIDTH // 2, 
                                SCREEN_HEIGHT - 20, 18, (100, 100, 100))
    
    def on_enter(self, **kwargs):
        """Chamado ao entrar na cena."""
        self._audio.play_music("music_loop.mp3")
        self._menu.reset()
    
    def _start_game(self):
        """Inicia o jogo."""
        self.change_scene(STATE_GAME)
    
    def _open_options(self):
        """Abre opções."""
        self.change_scene(STATE_OPTIONS, from_title=True)
    
    def _quit_game(self):
        """Sai do jogo."""
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def update(self, dt: float):
        """Atualiza a cena."""
        pass
    
    def draw(self, screen: pygame.Surface):
        """Desenha a cena."""
        screen.fill(COLOR_BLACK)
        
        # Logo
        screen.blit(self._logo, self._logo_rect)
        
        # Menu
        self._menu.draw(screen)
        
        # Instruções
        for label in self._instructions:
            label.draw(screen)
        
        # Copyright
        self._copyright.draw(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos."""
        self._menu.handle_event(event)
