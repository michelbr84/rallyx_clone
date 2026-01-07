## Estrutura completa de pastas (file tree)

```text
rallyx_clone/
├── .github/
│   └── workflows/
│       └── python.yml
├── docs/
│   └── ARCHITECTURE.md
├── scripts/
│   └── run_game.py
├── src/
│   └── rallyx_clone/
│       ├── assets/
│       │   ├── data/
│       │   │   └── level_01.json
│       │   ├── images/
│       │   │   ├── atlas.json
│       │   │   ├── enemy_car.png
│       │   │   ├── flag.png
│       │   │   ├── icon_life.png
│       │   │   ├── player_car.png
│       │   │   ├── smoke.png
│       │   │   ├── tile_border.png
│       │   │   ├── tile_grass.png
│       │   │   ├── tile_road.png
│       │   │   ├── tile_wall.png
│       │   │   ├── title.png
│       │   │   └── ui_panel.png
│       │   └── sounds/
│       │       ├── crash.mp3
│       │       ├── engine_loop.mp3
│       │       ├── lose.mp3
│       │       ├── manifest.json
│       │       ├── music_loop.mp3
│       │       ├── pickup_flag.mp3
│       │       ├── smoke.mp3
│       │       ├── ui_move.mp3
│       │       ├── ui_select.mp3
│       │       └── win.mp3
│       ├── core/
│       │   ├── __init__.py
│       │   ├── assets.py
│       │   ├── audio.py
│       │   ├── collision.py
│       │   ├── config.py
│       │   ├── constants.py
│       │   ├── pathfinding.py
│       │   ├── scene.py
│       │   ├── state.py
│       │   └── timer.py
│       ├── gameplay/
│       │   ├── __init__.py
│       │   ├── enemy.py
│       │   ├── entities_base.py
│       │   ├── flag.py
│       │   ├── player.py
│       │   ├── session.py
│       │   ├── smoke.py
│       │   └── world.py
│       ├── scenes/
│       │   ├── __init__.py
│       │   ├── game_scene.py
│       │   ├── gameover_scene.py
│       │   ├── options_scene.py
│       │   ├── pause_scene.py
│       │   └── title_scene.py
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── hud.py
│       │   ├── menu.py
│       │   └── widgets.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── logger.py
│       │   └── math2d.py
│       ├── __init__.py
│       ├── __main__.py
│       └── app.py
├── tests/
│   └── test_level_loading.py
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## Como rodar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
python -m rallyx_clone
```

---

## Controles (no demo)

* **Setas / WASD**: mover
* **Espaço**: soltar fumaça (smokescreen)
* **Esc**: pausa
* **Enter**: confirmar nos menus

---

## O que está implementado (demo 1 fase)

* **Mapa em grid** carregado de `assets/data/level_01.json`
* **Player** com aceleração, atrito e colisão com tiles bloqueados
* **Inimigos perseguidores (carros vermelhos)** com **pathfinding BFS** em grid (recalcula periodicamente)
* **Fumaça**:

  * cria nuvem atrás do carro
  * inimigos dentro da nuvem ficam **lentos** e **confusos** por um tempo
  * cooldown e duração configuráveis
* **Bandeiras coletáveis** (10) + **pontuação**
* **Tempo limite**
* **Vidas** e **respawn** ao colidir com inimigo
* **HUD** com score, tempo, vidas, contador de flags e **radar mini-map**
* **Menus**: Title, Options (dificuldade/volumes/fullscreen/vsync), Pause, Game Over
* **High score** salvo em `saves/highscore.json` (criado ao rodar)