"""
Sistema de Menu navegável.
"""
import pygame
from typing import List, Union, Optional, Callable
from .widgets import Button, Slider, Toggle
from ..core.audio import AudioManager


class Menu:
    """Menu navegável com teclado."""
    
    def __init__(self):
        self.items: List[Union[Button, Slider, Toggle]] = []
        self.selected_index = 0
        self._audio = AudioManager()
    
    def add_button(self, text: str, x: int, y: int, 
                   callback: Optional[Callable] = None,
                   font_size: int = 32) -> Button:
        """Adiciona um botão ao menu."""
        button = Button(text, x, y, font_size=font_size, callback=callback)
        self.items.append(button)
        self._update_selection()
        return button
    
    def add_slider(self, label: str, x: int, y: int, width: int = 200,
                   min_val: float = 0.0, max_val: float = 1.0, value: float = 0.5,
                   callback: Optional[Callable[[float], None]] = None) -> Slider:
        """Adiciona um slider ao menu."""
        slider = Slider(label, x, y, width, min_val, max_val, value, callback=callback)
        self.items.append(slider)
        self._update_selection()
        return slider
    
    def add_toggle(self, label: str, x: int, y: int, value: bool = False,
                   callback: Optional[Callable[[bool], None]] = None) -> Toggle:
        """Adiciona um toggle ao menu."""
        toggle = Toggle(label, x, y, value, callback=callback)
        self.items.append(toggle)
        self._update_selection()
        return toggle
    
    def _update_selection(self):
        """Atualiza indicador de seleção."""
        for i, item in enumerate(self.items):
            item.set_selected(i == self.selected_index)
    
    def navigate(self, direction: int):
        """
        Navega no menu.
        
        Args:
            direction: -1 para cima, 1 para baixo
        """
        if not self.items:
            return
        
        self.selected_index = (self.selected_index + direction) % len(self.items)
        self._update_selection()
        self._audio.play_sound("ui_move.mp3")
    
    def adjust(self, direction: int):
        """
        Ajusta valor do item selecionado (para sliders/toggles).
        
        Args:
            direction: -1 para esquerda, 1 para direita
        """
        if not self.items:
            return
        
        item = self.items[self.selected_index]
        
        if isinstance(item, Slider):
            item.adjust(direction * 0.1)
            self._audio.play_sound("ui_move.mp3")
        elif isinstance(item, Toggle):
            item.toggle()
            self._audio.play_sound("ui_select.mp3")
    
    def select(self):
        """Ativa o item selecionado."""
        if not self.items:
            return
        
        item = self.items[self.selected_index]
        
        if isinstance(item, Button):
            self._audio.play_sound("ui_select.mp3")
            item.activate()
        elif isinstance(item, Toggle):
            item.toggle()
            self._audio.play_sound("ui_select.mp3")
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Processa eventos.
        
        Args:
            event: Evento do pygame
        
        Returns:
            True se o evento foi consumido
        """
        if event.type != pygame.KEYDOWN:
            return False
        
        if event.key in (pygame.K_UP, pygame.K_w):
            self.navigate(-1)
            return True
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.navigate(1)
            return True
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.adjust(-1)
            return True
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.adjust(1)
            return True
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.select()
            return True
        
        return False
    
    def draw(self, screen: pygame.Surface):
        """Desenha o menu."""
        for item in self.items:
            item.draw(screen)
    
    def reset(self):
        """Reseta seleção para o primeiro item."""
        self.selected_index = 0
        self._update_selection()
