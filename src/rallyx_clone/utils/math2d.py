"""
Funções matemáticas 2D.
"""
import math
from typing import Tuple


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Limita um valor entre min e max."""
    return max(min_val, min(max_val, value))


def lerp(a: float, b: float, t: float) -> float:
    """Interpolação linear entre a e b."""
    return a + (b - a) * clamp(t, 0.0, 1.0)


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calcula distância entre dois pontos."""
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def distance_squared(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calcula distância ao quadrado (mais rápido)."""
    dx = x2 - x1
    dy = y2 - y1
    return dx * dx + dy * dy


def normalize(x: float, y: float) -> Tuple[float, float]:
    """Normaliza um vetor 2D."""
    length = math.sqrt(x * x + y * y)
    if length > 0:
        return x / length, y / length
    return 0.0, 0.0


def angle_to_direction(angle_degrees: float) -> Tuple[float, float]:
    """Converte ângulo em graus para vetor direção."""
    rad = math.radians(angle_degrees)
    return math.cos(rad), math.sin(rad)


def direction_to_angle(dx: float, dy: float) -> float:
    """Converte vetor direção para ângulo em graus."""
    return math.degrees(math.atan2(dy, dx))
