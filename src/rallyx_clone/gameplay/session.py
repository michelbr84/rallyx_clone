"""
Session - Gerencia sessão de jogo (score, vidas, high score).
"""
import json
import os
from typing import Optional


class Session:
    """Gerencia estado da sessão de jogo."""
    
    def __init__(self, lives: int = 3):
        self.score = 0
        self.lives = lives
        self.initial_lives = lives
        self.flags_collected = 0
        self.flags_total = 10
        self.is_victory = False
        self.is_game_over = False
        
        # High score
        self._highscore_path = self._get_highscore_path()
        self.high_score = self._load_high_score()
    
    def _get_highscore_path(self) -> str:
        """Retorna caminho do arquivo de high score."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        saves_dir = os.path.join(os.path.dirname(base_dir), "saves")
        os.makedirs(saves_dir, exist_ok=True)
        return os.path.join(saves_dir, "highscore.json")
    
    def _load_high_score(self) -> int:
        """Carrega high score do arquivo."""
        try:
            if os.path.exists(self._highscore_path):
                with open(self._highscore_path, 'r') as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except (json.JSONDecodeError, IOError):
            pass
        return 0
    
    def _save_high_score(self):
        """Salva high score no arquivo."""
        try:
            with open(self._highscore_path, 'w') as f:
                json.dump({"high_score": self.high_score}, f, indent=2)
        except IOError:
            pass
    
    def add_score(self, points: int):
        """Adiciona pontos ao score."""
        self.score += points
    
    def add_flag(self, points: int = 100):
        """Registra coleta de bandeira."""
        self.flags_collected += 1
        self.add_score(points)
    
    def add_time_bonus(self, time_left: float):
        """Adiciona bônus por tempo restante."""
        bonus = int(time_left * 5)  # 5 pontos por segundo
        self.add_score(bonus)
    
    def lose_life(self) -> bool:
        """
        Perde uma vida.
        
        Returns:
            True se game over (sem vidas)
        """
        self.lives -= 1
        if self.lives <= 0:
            self.is_game_over = True
            self._check_high_score()
            return True
        return False
    
    def victory(self, completion_bonus: int = 500):
        """Registra vitória."""
        self.is_victory = True
        self.add_score(completion_bonus)
        self._check_high_score()
    
    def time_out(self):
        """Tempo esgotado."""
        self.is_game_over = True
        self._check_high_score()
    
    def _check_high_score(self):
        """Verifica e atualiza high score se necessário."""
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()
    
    def reset(self):
        """Reseta a sessão para nova partida."""
        self.score = 0
        self.lives = self.initial_lives
        self.flags_collected = 0
        self.is_victory = False
        self.is_game_over = False
    
    @property
    def is_new_high_score(self) -> bool:
        """Retorna True se o score atual é um novo high score."""
        return self.score >= self.high_score and self.score > 0
