"""
Sistema de Timer para cooldowns e eventos temporizados.
"""
from typing import Callable, Optional


class Timer:
    """Timer simples para cooldowns e eventos."""
    
    def __init__(self, duration: float, callback: Optional[Callable] = None,
                 autostart: bool = False, loop: bool = False):
        """
        Cria um timer.
        
        Args:
            duration: Duração em segundos
            callback: Função a chamar quando terminar
            autostart: Se True, inicia automaticamente
            loop: Se True, reinicia automaticamente
        """
        self.duration = duration
        self.callback = callback
        self.loop = loop
        
        self._elapsed = 0.0
        self._running = autostart
        self._finished = False
    
    @property
    def running(self) -> bool:
        """Retorna se o timer está rodando."""
        return self._running
    
    @property
    def finished(self) -> bool:
        """Retorna se o timer terminou."""
        return self._finished
    
    @property
    def progress(self) -> float:
        """Retorna progresso de 0.0 a 1.0."""
        if self.duration <= 0:
            return 1.0
        return min(1.0, self._elapsed / self.duration)
    
    @property
    def remaining(self) -> float:
        """Retorna tempo restante em segundos."""
        return max(0.0, self.duration - self._elapsed)
    
    def start(self):
        """Inicia o timer."""
        self._running = True
        self._finished = False
    
    def stop(self):
        """Para o timer."""
        self._running = False
    
    def reset(self):
        """Reseta o timer."""
        self._elapsed = 0.0
        self._finished = False
    
    def restart(self):
        """Reinicia o timer."""
        self.reset()
        self.start()
    
    def update(self, dt: float):
        """
        Atualiza o timer.
        
        Args:
            dt: Delta time em segundos
        """
        if not self._running:
            return
        
        self._elapsed += dt
        
        if self._elapsed >= self.duration:
            self._finished = True
            
            if self.callback:
                self.callback()
            
            if self.loop:
                self._elapsed = 0.0
                self._finished = False
            else:
                self._running = False


class CountdownTimer(Timer):
    """Timer de contagem regressiva."""
    
    def __init__(self, duration: float, callback: Optional[Callable] = None):
        super().__init__(duration, callback, autostart=True)
    
    @property
    def time_left(self) -> float:
        """Retorna tempo restante."""
        return self.remaining
    
    @property
    def time_left_int(self) -> int:
        """Retorna tempo restante como inteiro."""
        return int(self.remaining)
