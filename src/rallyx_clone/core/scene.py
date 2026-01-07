"""
Classe base Scene para todas as cenas do jogo.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .state import StateMachine


class Scene(ABC):
    """Classe abstrata base para cenas do jogo."""
    
    def __init__(self):
        self.state_machine: Optional["StateMachine"] = None
    
    def on_enter(self, **kwargs):
        """
        Chamado quando a cena entra em foco.
        
        Args:
            **kwargs: Dados passados pela transição
        """
        pass
    
    def on_exit(self):
        """Chamado quando a cena sai de foco."""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """
        Atualiza a lógica da cena.
        
        Args:
            dt: Delta time em segundos
        """
        pass
    
    @abstractmethod
    def draw(self, screen):
        """
        Desenha a cena.
        
        Args:
            screen: Surface do pygame
        """
        pass
    
    @abstractmethod
    def handle_event(self, event):
        """
        Processa eventos.
        
        Args:
            event: Evento do pygame
        """
        pass
    
    def change_scene(self, scene_name: str, **kwargs):
        """
        Muda para outra cena.
        
        Args:
            scene_name: Nome da cena destino
            **kwargs: Dados a passar
        """
        if self.state_machine:
            self.state_machine.change_state(scene_name, **kwargs)
