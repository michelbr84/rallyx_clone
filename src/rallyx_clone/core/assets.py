"""
Asset Manager - Carrega e cacheia imagens e dados.
"""
import os
import json
import pygame
from typing import Dict, Optional


class AssetManager:
    """Gerencia carregamento e cache de assets."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self._images: Dict[str, pygame.Surface] = {}
        self._data: Dict[str, dict] = {}
        self._base_path = self._get_base_path()
    
    def _get_base_path(self):
        """Retorna o caminho base dos assets."""
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets"
        )
    
    def load_image(self, name: str, scale: Optional[tuple] = None, 
                   convert_alpha: bool = True) -> pygame.Surface:
        """
        Carrega uma imagem com cache.
        
        Args:
            name: Nome do arquivo (sem caminho)
            scale: Tupla (width, height) para redimensionar
            convert_alpha: Se True, converte para alpha
        
        Returns:
            pygame.Surface da imagem
        """
        cache_key = f"{name}_{scale}"
        
        if cache_key in self._images:
            return self._images[cache_key]
        
        path = os.path.join(self._base_path, "images", name)
        
        try:
            if convert_alpha:
                image = pygame.image.load(path).convert_alpha()
            else:
                image = pygame.image.load(path).convert()
            
            if scale:
                image = pygame.transform.scale(image, scale)
            
            self._images[cache_key] = image
            return image
        except pygame.error as e:
            print(f"Erro ao carregar imagem {name}: {e}")
            # Retorna superfície placeholder
            surf = pygame.Surface((32, 32))
            surf.fill((255, 0, 255))  # Magenta = erro
            return surf
    
    def load_tile(self, tile_type: int) -> pygame.Surface:
        """Carrega tile pelo tipo."""
        from .constants import TILE_SIZE, TILE_ROAD, TILE_WALL, TILE_GRASS, TILE_BORDER
        
        tile_names = {
            TILE_ROAD: "tile_road.png",
            TILE_WALL: "tile_wall.png",
            TILE_GRASS: "tile_grass.png",
            TILE_BORDER: "tile_border.png"
        }
        
        name = tile_names.get(tile_type, "tile_road.png")
        return self.load_image(name, scale=(TILE_SIZE, TILE_SIZE))
    
    def load_data(self, name: str) -> dict:
        """
        Carrega arquivo JSON de dados.
        
        Args:
            name: Nome do arquivo (sem caminho)
        
        Returns:
            Dict com os dados
        """
        if name in self._data:
            return self._data[name]
        
        path = os.path.join(self._base_path, "data", name)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._data[name] = data
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar dados {name}: {e}")
            return {}
    
    def clear_cache(self):
        """Limpa cache de imagens."""
        self._images.clear()
        self._data.clear()
    
    def preload_all(self):
        """Pré-carrega todos os assets principais."""
        from .constants import TILE_SIZE
        
        # Imagens do jogo
        images = [
            "player_car.png",
            "enemy_car.png",
            "flag.png",
            "smoke.png",
            "icon_life.png",
            "title.png",
            "ui_panel.png"
        ]
        
        for img in images:
            self.load_image(img)
        
        # Tiles
        for tile_type in range(4):
            self.load_tile(tile_type)
