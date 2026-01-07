"""
Options Scene - Menu de configurações.
"""
import pygame
from ..core.scene import Scene
from ..core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STATE_TITLE, STATE_PAUSE,
    COLOR_BLACK, COLOR_WHITE, COLOR_YELLOW,
    DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD
)
from ..core.config import Config
from ..core.audio import AudioManager
from ..ui.menu import Menu
from ..ui.widgets import Label, Button


class OptionsScene(Scene):
    """Tela de opções/configurações."""
    
    def __init__(self):
        super().__init__()
        
        self._config = Config()
        self._audio = AudioManager()
        self._from_title = True
        
        # Título
        self._title = Label("OPÇÕES", SCREEN_WIDTH // 2, 60, 48, COLOR_YELLOW)
        
        # Dificuldade (inicializar antes do menu)
        self._difficulties = [DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD]
        self._difficulty_names = ["FÁCIL", "NORMAL", "DIFÍCIL"]
        self._difficulty_index = self._get_difficulty_index()
        
        # Menu
        self._menu = Menu()
        self._setup_menu()
    
    def _setup_menu(self):
        """Configura o menu."""
        self._menu = Menu()
        center_x = SCREEN_WIDTH // 2
        slider_x = center_x
        
        # Dificuldade (botão customizado)
        self._difficulty_button = self._menu.add_button(
            self._get_difficulty_text(), center_x, 150,
            callback=self._cycle_difficulty
        )
        
        # Volume música
        self._music_slider = self._menu.add_slider(
            "Música", slider_x, 210, 200,
            value=self._config.music_volume,
            callback=self._set_music_volume
        )
        
        # Volume efeitos
        self._sfx_slider = self._menu.add_slider(
            "Efeitos", slider_x, 270, 200,
            value=self._config.sfx_volume,
            callback=self._set_sfx_volume
        )
        
        # Fullscreen
        self._fullscreen_toggle = self._menu.add_toggle(
            "Tela Cheia", slider_x, 330,
            value=self._config.fullscreen,
            callback=self._toggle_fullscreen
        )
        
        # VSync
        self._vsync_toggle = self._menu.add_toggle(
            "VSync", slider_x, 390,
            value=self._config.vsync,
            callback=self._toggle_vsync
        )
        
        # Voltar
        self._menu.add_button("VOLTAR", center_x, 480, self._go_back)
    
    def _get_difficulty_index(self) -> int:
        """Retorna índice da dificuldade atual."""
        difficulties = [DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD]
        try:
            return difficulties.index(self._config.difficulty)
        except ValueError:
            return 1
    
    def _get_difficulty_text(self) -> str:
        """Retorna texto da dificuldade."""
        names = ["FÁCIL", "NORMAL", "DIFÍCIL"]
        return f"Dificuldade: < {names[self._difficulty_index]} >"
    
    def _cycle_difficulty(self):
        """Cicla entre dificuldades."""
        self._difficulty_index = (self._difficulty_index + 1) % 3
        self._config.difficulty = self._difficulties[self._difficulty_index]
        self._difficulty_button.text = self._get_difficulty_text()
        self._difficulty_button._render()
        self._config.save()
    
    def _set_music_volume(self, value: float):
        """Define volume da música."""
        self._config.music_volume = value
        self._audio.update_volumes()
        self._config.save()
    
    def _set_sfx_volume(self, value: float):
        """Define volume dos efeitos."""
        self._config.sfx_volume = value
        self._audio.update_volumes()
        self._config.save()
    
    def _toggle_fullscreen(self, value: bool):
        """Alterna fullscreen."""
        self._config.fullscreen = value
        self._config.save()
        # Fullscreen será aplicado no reinício
    
    def _toggle_vsync(self, value: bool):
        """Alterna VSync."""
        self._config.vsync = value
        self._config.save()
    
    def _go_back(self):
        """Volta para a cena anterior."""
        if self._from_title:
            self.change_scene(STATE_TITLE)
        else:
            self.change_scene(STATE_PAUSE)
    
    def on_enter(self, **kwargs):
        """Chamado ao entrar na cena."""
        self._from_title = kwargs.get("from_title", True)
        self._menu.reset()
        
        # Atualiza valores
        self._difficulty_index = self._get_difficulty_index()
        self._difficulty_button.text = self._get_difficulty_text()
        self._difficulty_button._render()
        self._music_slider.value = self._config.music_volume
        self._sfx_slider.value = self._config.sfx_volume
        self._fullscreen_toggle.value = self._config.fullscreen
        self._vsync_toggle.value = self._config.vsync
    
    def update(self, dt: float):
        """Atualiza a cena."""
        pass
    
    def draw(self, screen: pygame.Surface):
        """Desenha a cena."""
        screen.fill(COLOR_BLACK)
        
        # Título
        self._title.draw(screen)
        
        # Menu
        self._menu.draw(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._go_back()
            return
        
        self._menu.handle_event(event)
