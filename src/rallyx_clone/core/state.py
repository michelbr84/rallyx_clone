"""
State Machine para gerenciar transições entre cenas.
"""
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .scene import Scene


class StateMachine:
    """Máquina de estados para gerenciar cenas do jogo."""
    
    def __init__(self):
        self._states: Dict[str, "Scene"] = {}
        self._current_state: Optional[str] = None
        self._next_state: Optional[str] = None
        self._transition_data: dict = {}
    
    @property
    def current_state(self) -> Optional[str]:
        """Retorna o nome do estado atual."""
        return self._current_state
    
    @property
    def current_scene(self) -> Optional["Scene"]:
        """Retorna a cena atual."""
        if self._current_state:
            return self._states.get(self._current_state)
        return None
    
    def add_state(self, name: str, scene: "Scene"):
        """
        Adiciona um estado/cena.
        
        Args:
            name: Nome do estado
            scene: Instância da cena
        """
        self._states[name] = scene
        scene.state_machine = self
    
    def change_state(self, name: str, **kwargs):
        """
        Muda para um novo estado.
        
        Args:
            name: Nome do estado destino
            **kwargs: Dados a passar para o novo estado
        """
        if name in self._states:
            self._next_state = name
            self._transition_data = kwargs
        else:
            print(f"Estado '{name}' não encontrado!")
    
    def _do_transition(self):
        """Executa a transição de estado."""
        if self._next_state is None:
            return
        
        # Sai do estado atual
        if self._current_state and self._current_state in self._states:
            self._states[self._current_state].on_exit()
        
        # Entra no novo estado
        self._current_state = self._next_state
        self._next_state = None
        
        if self._current_state in self._states:
            self._states[self._current_state].on_enter(**self._transition_data)
        
        self._transition_data = {}
    
    def update(self, dt: float):
        """
        Atualiza o estado atual.
        
        Args:
            dt: Delta time em segundos
        """
        # Processa transição pendente
        self._do_transition()
        
        # Atualiza estado atual
        if self._current_state and self._current_state in self._states:
            self._states[self._current_state].update(dt)
    
    def draw(self, screen):
        """
        Desenha o estado atual.
        
        Args:
            screen: Surface do pygame para desenhar
        """
        if self._current_state and self._current_state in self._states:
            self._states[self._current_state].draw(screen)
    
    def handle_event(self, event):
        """
        Passa evento para o estado atual.
        
        Args:
            event: Evento do pygame
        """
        if self._current_state and self._current_state in self._states:
            self._states[self._current_state].handle_event(event)
