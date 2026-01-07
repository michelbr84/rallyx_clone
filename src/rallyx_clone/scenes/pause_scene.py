"""
Pause Scene - Menu de pausa.
"""
import pygame
from ..core.scene import Scene
from ..core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STATE_GAME, STATE_OPTIONS, STATE_TITLE,
    COLOR_BLACK, COLOR_WHITE, COLOR_YELLOW
)
from ..core.audio import AudioManager
from ..ui.menu import Menu
from ..ui.widgets import Label


class PauseScene(Scene):
    """Menu de pausa do jogo."""
    
    def __init__(self):
        super().__init__()
        
        self._audio = AudioManager()
        
        # Fundo semi-transparente
        self._overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._overlay.fill((0, 0, 0, 180))
        
        # Título
        self._title = Label("PAUSADO", SCREEN_WIDTH // 2, 150, 64, COLOR_YELLOW)
        
        # Menu
        self._menu = Menu()
        center_x = SCREEN_WIDTH // 2
        self._menu.add_button("CONTINUAR", center_x, 280, self._resume)
        self._menu.add_button("OPÇÕES", center_x, 350, self._open_options)
        self._menu.add_button("SAIR PARA TÍTULO", center_x, 420, self._quit_to_title)
    
    def on_enter(self, **kwargs):
        """Chamado ao entrar na cena."""
        self._menu.reset()
    
    def _resume(self):
        """Retoma o jogo."""
        self._audio.unpause_music()
        self._audio.play_sound("engine_loop.mp3", loops=-1)
        self.change_scene(STATE_GAME)
    
    def _open_options(self):
        """Abre opções."""
        self.change_scene(STATE_OPTIONS, from_title=False)
    
    def _quit_to_title(self):
        """Volta para o título."""
        self._audio.stop_music()
        self.change_scene(STATE_TITLE)
    
    def update(self, dt: float):
        """Atualiza a cena."""
        pass
    
    def draw(self, screen: pygame.Surface):
        """Desenha a cena."""
        # Não limpa a tela - mantém o jogo por baixo
        # Desenha overlay
        screen.blit(self._overlay, (0, 0))
        
        # Título
        self._title.draw(screen)
        
        # Menu
        self._menu.draw(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._resume()
                return
        
        self._menu.handle_event(event)
