"""
Widgets de UI para menus.
"""
import pygame
from typing import Tuple, Optional, Callable
from ..core.constants import COLOR_WHITE, COLOR_YELLOW, COLOR_LIGHT_GRAY


class Label:
    """Widget de texto simples."""
    
    def __init__(self, text: str, x: int, y: int, 
                 font_size: int = 24, color: Tuple[int, int, int] = COLOR_WHITE,
                 center: bool = True):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.center = center
        
        self._font = pygame.font.Font(None, font_size)
        self._render()
    
    def _render(self):
        """Renderiza o texto."""
        self._surface = self._font.render(self.text, True, self.color)
        self._rect = self._surface.get_rect()
        
        if self.center:
            self._rect.center = (self.x, self.y)
        else:
            self._rect.topleft = (self.x, self.y)
    
    def set_text(self, text: str):
        """Atualiza o texto."""
        if text != self.text:
            self.text = text
            self._render()
    
    def draw(self, screen: pygame.Surface):
        """Desenha o label."""
        screen.blit(self._surface, self._rect)


class Button:
    """Botão de menu."""
    
    def __init__(self, text: str, x: int, y: int,
                 font_size: int = 32,
                 color: Tuple[int, int, int] = COLOR_WHITE,
                 selected_color: Tuple[int, int, int] = COLOR_YELLOW,
                 callback: Optional[Callable] = None):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.selected_color = selected_color
        self.callback = callback
        self.selected = False
        
        self._font = pygame.font.Font(None, font_size)
        self._render()
    
    def _render(self):
        """Renderiza o botão."""
        color = self.selected_color if self.selected else self.color
        self._surface = self._font.render(self.text, True, color)
        self._rect = self._surface.get_rect(center=(self.x, self.y))
        
        # Adiciona indicador de seleção
        if self.selected:
            prefix = "> "
            suffix = " <"
            full_text = prefix + self.text + suffix
            self._surface = self._font.render(full_text, True, color)
            self._rect = self._surface.get_rect(center=(self.x, self.y))
    
    def set_selected(self, selected: bool):
        """Define se está selecionado."""
        if selected != self.selected:
            self.selected = selected
            self._render()
    
    def activate(self):
        """Ativa o botão."""
        if self.callback:
            self.callback()
    
    def draw(self, screen: pygame.Surface):
        """Desenha o botão."""
        screen.blit(self._surface, self._rect)


class Slider:
    """Slider para configurações."""
    
    def __init__(self, label: str, x: int, y: int, width: int = 200,
                 min_val: float = 0.0, max_val: float = 1.0, value: float = 0.5,
                 font_size: int = 24,
                 color: Tuple[int, int, int] = COLOR_WHITE,
                 selected_color: Tuple[int, int, int] = COLOR_YELLOW,
                 callback: Optional[Callable[[float], None]] = None):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.color = color
        self.selected_color = selected_color
        self.callback = callback
        self.selected = False
        
        self._font = pygame.font.Font(None, font_size)
        self._bar_height = 8
    
    @property
    def normalized_value(self) -> float:
        """Valor normalizado de 0 a 1."""
        return (self.value - self.min_val) / (self.max_val - self.min_val)
    
    def set_value(self, value: float):
        """Define o valor."""
        self.value = max(self.min_val, min(self.max_val, value))
        if self.callback:
            self.callback(self.value)
    
    def adjust(self, delta: float):
        """Ajusta o valor."""
        step = (self.max_val - self.min_val) * delta
        self.set_value(self.value + step)
    
    def set_selected(self, selected: bool):
        """Define se está selecionado."""
        self.selected = selected
    
    def draw(self, screen: pygame.Surface):
        """Desenha o slider."""
        color = self.selected_color if self.selected else self.color
        
        # Label
        label_surf = self._font.render(self.label, True, color)
        label_rect = label_surf.get_rect(midright=(self.x - 20, self.y))
        screen.blit(label_surf, label_rect)
        
        # Barra de fundo
        bar_rect = pygame.Rect(self.x, self.y - self._bar_height // 2,
                               self.width, self._bar_height)
        pygame.draw.rect(screen, COLOR_LIGHT_GRAY, bar_rect)
        
        # Barra de valor
        fill_width = int(self.width * self.normalized_value)
        fill_rect = pygame.Rect(self.x, self.y - self._bar_height // 2,
                                fill_width, self._bar_height)
        pygame.draw.rect(screen, color, fill_rect)
        
        # Valor em porcentagem
        percent = int(self.normalized_value * 100)
        value_text = f"{percent}%"
        value_surf = self._font.render(value_text, True, color)
        value_rect = value_surf.get_rect(midleft=(self.x + self.width + 10, self.y))
        screen.blit(value_surf, value_rect)


class Toggle:
    """Toggle para opções booleanas."""
    
    def __init__(self, label: str, x: int, y: int, value: bool = False,
                 font_size: int = 24,
                 color: Tuple[int, int, int] = COLOR_WHITE,
                 selected_color: Tuple[int, int, int] = COLOR_YELLOW,
                 callback: Optional[Callable[[bool], None]] = None):
        self.label = label
        self.x = x
        self.y = y
        self.value = value
        self.color = color
        self.selected_color = selected_color
        self.callback = callback
        self.selected = False
        
        self._font = pygame.font.Font(None, font_size)
    
    def toggle(self):
        """Alterna o valor."""
        self.value = not self.value
        if self.callback:
            self.callback(self.value)
    
    def set_selected(self, selected: bool):
        """Define se está selecionado."""
        self.selected = selected
    
    def draw(self, screen: pygame.Surface):
        """Desenha o toggle."""
        color = self.selected_color if self.selected else self.color
        
        # Label
        label_surf = self._font.render(self.label, True, color)
        label_rect = label_surf.get_rect(midright=(self.x - 20, self.y))
        screen.blit(label_surf, label_rect)
        
        # Valor
        value_text = "SIM" if self.value else "NÃO"
        value_surf = self._font.render(f"< {value_text} >", True, color)
        value_rect = value_surf.get_rect(midleft=(self.x, self.y))
        screen.blit(value_surf, value_rect)
