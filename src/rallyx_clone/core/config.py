"""
Configurações mutáveis do jogo.
"""
import json
import os
from .constants import DIFFICULTY_NORMAL


class Config:
    """Gerencia configurações do jogo que podem ser alteradas pelo jogador."""
    
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
        
        # Configurações padrão
        self.difficulty = DIFFICULTY_NORMAL
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.fullscreen = False
        self.vsync = True
        
        # Caminho do arquivo de configuração
        self._config_path = self._get_config_path()
        self.load()
    
    def _get_config_path(self):
        """Retorna o caminho do arquivo de configuração."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        saves_dir = os.path.join(os.path.dirname(base_dir), "saves")
        os.makedirs(saves_dir, exist_ok=True)
        return os.path.join(saves_dir, "config.json")
    
    def load(self):
        """Carrega configurações do arquivo JSON."""
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r') as f:
                    data = json.load(f)
                    self.difficulty = data.get("difficulty", self.difficulty)
                    self.music_volume = data.get("music_volume", self.music_volume)
                    self.sfx_volume = data.get("sfx_volume", self.sfx_volume)
                    self.fullscreen = data.get("fullscreen", self.fullscreen)
                    self.vsync = data.get("vsync", self.vsync)
        except (json.JSONDecodeError, IOError):
            pass  # Usa valores padrão
    
    def save(self):
        """Salva configurações no arquivo JSON."""
        data = {
            "difficulty": self.difficulty,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "fullscreen": self.fullscreen,
            "vsync": self.vsync
        }
        try:
            with open(self._config_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass
    
    def reset(self):
        """Reseta para valores padrão."""
        self.difficulty = DIFFICULTY_NORMAL
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.fullscreen = False
        self.vsync = True
