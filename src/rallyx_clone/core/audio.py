"""
Audio Manager - Gerencia música e efeitos sonoros.
"""
import os
import pygame
from typing import Dict, Optional
from .config import Config


class AudioManager:
    """Gerencia reprodução de áudio."""
    
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
        
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._base_path = self._get_base_path()
        self._music_playing = False
        self._current_music = None
        self._config = Config()
        
        # Inicializa mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    
    def _get_base_path(self):
        """Retorna o caminho base dos sons."""
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets", "sounds"
        )
    
    def load_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
        """
        Carrega um efeito sonoro.
        
        Args:
            name: Nome do arquivo de som
        
        Returns:
            pygame.mixer.Sound ou None se falhar
        """
        if name in self._sounds:
            return self._sounds[name]
        
        path = os.path.join(self._base_path, name)
        
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self._config.sfx_volume)
            self._sounds[name] = sound
            return sound
        except pygame.error as e:
            print(f"Erro ao carregar som {name}: {e}")
            return None
    
    def play_sound(self, name: str, loops: int = 0):
        """
        Reproduz um efeito sonoro.
        
        Args:
            name: Nome do arquivo de som
            loops: Número de repetições (-1 = infinito)
        """
        sound = self.load_sound(name)
        if sound:
            sound.set_volume(self._config.sfx_volume)
            sound.play(loops=loops)
    
    def stop_sound(self, name: str):
        """Para um efeito sonoro específico."""
        if name in self._sounds:
            self._sounds[name].stop()
    
    def play_music(self, name: str, loops: int = -1, fade_ms: int = 1000):
        """
        Reproduz música de fundo.
        
        Args:
            name: Nome do arquivo de música
            loops: Número de repetições (-1 = infinito)
            fade_ms: Tempo de fade in em ms
        """
        path = os.path.join(self._base_path, name)
        
        try:
            if self._current_music != name:
                pygame.mixer.music.load(path)
                self._current_music = name
            
            pygame.mixer.music.set_volume(self._config.music_volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self._music_playing = True
        except pygame.error as e:
            print(f"Erro ao reproduzir música {name}: {e}")
    
    def stop_music(self, fade_ms: int = 500):
        """Para a música com fade out."""
        pygame.mixer.music.fadeout(fade_ms)
        self._music_playing = False
    
    def pause_music(self):
        """Pausa a música."""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Retoma a música pausada."""
        pygame.mixer.music.unpause()
    
    def update_volumes(self):
        """Atualiza volumes baseado na configuração."""
        pygame.mixer.music.set_volume(self._config.music_volume)
        for sound in self._sounds.values():
            sound.set_volume(self._config.sfx_volume)
    
    def preload_all(self):
        """Pré-carrega todos os sons."""
        sounds = [
            "crash.mp3",
            "engine_loop.mp3",
            "lose.mp3",
            "pickup_flag.mp3",
            "smoke.mp3",
            "ui_move.mp3",
            "ui_select.mp3",
            "win.mp3"
        ]
        
        for sound in sounds:
            self.load_sound(sound)
