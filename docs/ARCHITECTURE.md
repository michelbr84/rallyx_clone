# Arquitetura do Rally-X Clone

## Visão Geral

O jogo segue uma arquitetura modular com separação clara de responsabilidades.

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                         App                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  State Machine                        │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │   │
│  │  │  Title  │ │ Options │ │  Game   │ │GameOver │   │   │
│  │  └─────────┘ └─────────┘ └────┬────┘ └─────────┘   │   │
│  └───────────────────────────────┼──────────────────────┘   │
│                                  │                           │
│  ┌───────────────────────────────┼──────────────────────┐   │
│  │                   GameScene   │                       │   │
│  │  ┌─────────┐  ┌─────────┐  ┌──┴────┐  ┌─────────┐   │   │
│  │  │  World  │  │ Session │  │  HUD  │  │  Timer  │   │   │
│  │  └────┬────┘  └─────────┘  └───────┘  └─────────┘   │   │
│  │       │                                              │   │
│  │  ┌────┴────────────────────────────────────────┐    │   │
│  │  │  Player  │  Enemies  │  Flags  │  Smoke     │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Módulos

### Core (`src/rallyx_clone/core/`)
- `constants.py` - Constantes globais
- `config.py` - Configurações do jogador
- `assets.py` - Gerenciador de imagens
- `audio.py` - Gerenciador de áudio
- `timer.py` - Sistema de timers
- `state.py` - Máquina de estados
- `scene.py` - Classe base de cenas
- `collision.py` - Detecção de colisão
- `pathfinding.py` - BFS para IA

### Gameplay (`src/rallyx_clone/gameplay/`)
- `entities_base.py` - Classe base Entity
- `player.py` - Carro do jogador
- `enemy.py` - IA dos inimigos
- `smoke.py` - Sistema de fumaça
- `flag.py` - Bandeiras
- `world.py` - Mundo/mapa
- `session.py` - Score e vidas

### UI (`src/rallyx_clone/ui/`)
- `widgets.py` - Label, Button, Slider
- `menu.py` - Navegação de menus
- `hud.py` - HUD e radar

### Scenes (`src/rallyx_clone/scenes/`)
- `title_scene.py` - Tela inicial
- `options_scene.py` - Opções
- `game_scene.py` - Gameplay
- `pause_scene.py` - Pausa
- `gameover_scene.py` - Fim de jogo

## Fluxo de Estados

```
Title ──> Options
  │          │
  └────┬─────┘
       │
       v
     Game <──> Pause ──> Options
       │
       v
   GameOver ──> Title
```

## Data Flow

1. **Input** → Player/Menu
2. **Update** → World → Entities
3. **Collision** → Session (lives/score)
4. **Draw** → World → HUD → Screen
