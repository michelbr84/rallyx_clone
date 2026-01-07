"""
Constantes globais do jogo Rally-X Clone.
"""

# Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Tiles
TILE_SIZE = 32

# Cores
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_DARK_GRAY = (40, 40, 40)
COLOR_LIGHT_GRAY = (150, 150, 150)
COLOR_HUD_BG = (20, 20, 40)
COLOR_RADAR_BG = (10, 30, 10)

# Estados do jogo
STATE_TITLE = "title"
STATE_OPTIONS = "options"
STATE_GAME = "game"
STATE_PAUSE = "pause"
STATE_GAMEOVER = "gameover"

# Tiles do mapa
TILE_ROAD = 0
TILE_WALL = 1
TILE_GRASS = 2
TILE_BORDER = 3

# Gameplay
PLAYER_MAX_SPEED = 4.0
PLAYER_ACCELERATION = 0.3
PLAYER_FRICTION = 0.1
INITIAL_LIVES = 3
TOTAL_FLAGS = 10
DEFAULT_TIME_LIMIT = 120  # segundos

# Fumaça
SMOKE_DURATION = 2.5  # segundos
SMOKE_COOLDOWN = 4.0  # segundos
SMOKE_RADIUS = 48  # pixels
SMOKE_SLOW_FACTOR = 0.3

# Inimigos
ENEMY_SPEED = 2.5
ENEMY_CONFUSED_DURATION = 2.0  # segundos
ENEMY_PATH_RECALC_INTERVAL = 0.5  # segundos

# Pontuação
SCORE_FLAG = 100
SCORE_COMPLETE = 500

# Dificuldades
DIFFICULTY_EASY = "easy"
DIFFICULTY_NORMAL = "normal"
DIFFICULTY_HARD = "hard"

DIFFICULTY_SETTINGS = {
    DIFFICULTY_EASY: {
        "enemy_speed": 2.0,
        "enemy_count": 2,
        "time_bonus": 30
    },
    DIFFICULTY_NORMAL: {
        "enemy_speed": 2.5,
        "enemy_count": 3,
        "time_bonus": 0
    },
    DIFFICULTY_HARD: {
        "enemy_speed": 3.5,
        "enemy_count": 5,
        "time_bonus": -20
    }
}
