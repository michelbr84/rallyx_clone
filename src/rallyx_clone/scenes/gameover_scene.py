"""
GameOver Scene - Tela de fim de jogo.
"""
import pygame
from ..core.scene import Scene
from ..core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STATE_GAME, STATE_TITLE,
    COLOR_BLACK, COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN, COLOR_RED
)
from ..core.audio import AudioManager
from ..ui.menu import Menu
from ..ui.widgets import Label


class GameOverScene(Scene):
    """Tela de game over / vitória."""
    
    def __init__(self):
        super().__init__()
        
        self._audio = AudioManager()
        
        # Estado
        self._score = 0
        self._high_score = 0
        self._is_victory = False
        self._is_new_high = False
        
        # Labels (serão atualizados em on_enter)
        self._title_label = None
        self._score_label = None
        self._high_label = None
        self._new_high_label = None
        
        # Menu
        self._menu = Menu()
    
    def on_enter(self, **kwargs):
        """Chamado ao entrar na cena."""
        self._score = kwargs.get("score", 0)
        self._high_score = kwargs.get("high_score", 0)
        self._is_victory = kwargs.get("is_victory", False)
        self._is_new_high = kwargs.get("is_new_high", False)
        
        # Atualiza labels
        self._create_labels()
        
        # Cria menu
        self._menu = Menu()
        center_x = SCREEN_WIDTH // 2
        self._menu.add_button("JOGAR NOVAMENTE", center_x, 380, self._retry)
        self._menu.add_button("VOLTAR AO TÍTULO", center_x, 450, self._quit_to_title)
    
    def _create_labels(self):
        """Cria/atualiza labels baseado no estado."""
        center_x = SCREEN_WIDTH // 2
        
        # Título
        if self._is_victory:
            title_text = "VITÓRIA!"
            title_color = COLOR_GREEN
        else:
            title_text = "GAME OVER"
            title_color = COLOR_RED
        
        self._title_label = Label(title_text, center_x, 100, 72, title_color)
        
        # Score
        self._score_label = Label(
            f"PONTUAÇÃO: {self._score:06d}",
            center_x, 200, 48, COLOR_WHITE
        )
        
        # High score
        self._high_label = Label(
            f"RECORDE: {self._high_score:06d}",
            center_x, 260, 36, COLOR_YELLOW
        )
        
        # Novo recorde
        if self._is_new_high:
            self._new_high_label = Label(
                "NOVO RECORDE!",
                center_x, 310, 42, COLOR_YELLOW
            )
        else:
            self._new_high_label = None
    
    def _retry(self):
        """Joga novamente."""
        self.change_scene(STATE_GAME)
    
    def _quit_to_title(self):
        """Volta para o título."""
        self.change_scene(STATE_TITLE)
    
    def update(self, dt: float):
        """Atualiza a cena."""
        pass
    
    def draw(self, screen: pygame.Surface):
        """Desenha a cena."""
        screen.fill(COLOR_BLACK)
        
        # Labels
        if self._title_label:
            self._title_label.draw(screen)
        if self._score_label:
            self._score_label.draw(screen)
        if self._high_label:
            self._high_label.draw(screen)
        if self._new_high_label:
            self._new_high_label.draw(screen)
        
        # Menu
        self._menu.draw(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos."""
        self._menu.handle_event(event)
