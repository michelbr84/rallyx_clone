"""
Rally-X Clone - Aplicação principal.
"""
import sys
import pygame
from .core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK,
    STATE_TITLE, STATE_OPTIONS, STATE_GAME, STATE_PAUSE, STATE_GAMEOVER
)
from .core.config import Config
from .core.assets import AssetManager
from .core.audio import AudioManager
from .core.state import StateMachine
from .scenes.title_scene import TitleScene
from .scenes.options_scene import OptionsScene
from .scenes.game_scene import GameScene
from .scenes.pause_scene import PauseScene
from .scenes.gameover_scene import GameOverScene


class App:
    """Aplicação principal do jogo."""
    
    def __init__(self):
        # Inicializa Pygame
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Configuração
        self._config = Config()
        
        # Cria janela
        flags = 0
        if self._config.fullscreen:
            flags |= pygame.FULLSCREEN
        if self._config.vsync:
            flags |= pygame.DOUBLEBUF
        
        self._screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            flags
        )
        pygame.display.set_caption("Rally-X Clone")
        
        # Clock
        self._clock = pygame.time.Clock()
        
        # Managers
        self._assets = AssetManager()
        self._audio = AudioManager()
        
        # Pré-carrega assets
        self._assets.preload_all()
        self._audio.preload_all()
        
        # State machine
        self._state_machine = StateMachine()
        self._setup_scenes()
        
        # Estado
        self._running = True
    
    def _setup_scenes(self):
        """Configura todas as cenas."""
        self._state_machine.add_state(STATE_TITLE, TitleScene())
        self._state_machine.add_state(STATE_OPTIONS, OptionsScene())
        self._state_machine.add_state(STATE_GAME, GameScene())
        self._state_machine.add_state(STATE_PAUSE, PauseScene())
        self._state_machine.add_state(STATE_GAMEOVER, GameOverScene())
        
        # Inicia na tela de título
        self._state_machine.change_state(STATE_TITLE)
    
    def run(self):
        """Loop principal do jogo."""
        while self._running:
            # Delta time
            dt = self._clock.tick(FPS) / 1000.0
            
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                else:
                    self._state_machine.handle_event(event)
            
            # Update
            self._state_machine.update(dt)
            
            # Draw
            self._state_machine.draw(self._screen)
            
            # Flip
            pygame.display.flip()
        
        # Cleanup
        self._cleanup()
    
    def _cleanup(self):
        """Limpa recursos."""
        pygame.mixer.quit()
        pygame.quit()


def main():
    """Função principal."""
    try:
        app = App()
        app.run()
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
