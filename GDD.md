# 📘 GAME DESIGN DOCUMENT (GDD)

## Rally-X Clone – Demo (Python + Pygame)

---

## 1. Visão Geral

**Título provisório:** Rally-X Clone
**Gênero:** Ação / Arcade / Labirinto
**Plataforma:** PC (Windows / Linux / macOS)
**Tecnologia:** Python 3 + Pygame
**Modo de jogo:** Single-player
**Estilo:** Arcade retrô moderno
**Duração da demo:** 5–10 minutos
**Objetivo da demo:** Provar jogabilidade, IA, controles e loop principal com 1 fase completa

---

## 2. Objetivo do Jogo

O jogador controla um carro que deve:

* Navegar por um **mapa em grid estilo labirinto**
* **Coletar todas as bandeiras**
* **Evitar ou atrasar inimigos**
* Sobreviver até completar o objetivo **antes do tempo acabar**

O desafio cresce com:

* Pressão do tempo
* IA inimiga persistente
* Gestão estratégica da fumaça

---

## 3. Público-Alvo

* Fãs de jogos arcade clássicos
* Desenvolvedores indie / estudantes (demo educacional)
* Jogadores casuais que gostam de partidas rápidas
* Nostálgicos de jogos dos anos 80

---

## 4. Loop Principal de Gameplay

1. Jogador inicia a fase
2. Move-se pelo mapa em grid
3. Coleta bandeiras
4. Inimigos perseguem o jogador
5. Jogador usa fumaça para escapar
6. Colisão com inimigo → perde vida
7. Coleta todas as bandeiras → vitória
8. Tempo acaba ou vidas zeram → game over

---

## 5. Controles

| Ação            | Tecla         |
| --------------- | ------------- |
| Mover           | Setas ou WASD |
| Soltar fumaça   | Espaço        |
| Pausar          | Esc           |
| Confirmar menus | Enter         |

---

## 6. Mecânicas Principais

### 6.1 Movimento do Jogador

* Movimento em **grid livre**
* Aceleração progressiva
* Atrito ao soltar a tecla
* Colisão com tiles bloqueados
* Direção suave (não instantânea)

---

### 6.2 Fumaça (Smokescreen)

**Função:** Defesa estratégica

**Comportamento:**

* Criada atrás do carro
* Duração limitada
* Cooldown entre usos

**Efeito nos inimigos:**

* Redução de velocidade
* Confusão de pathfinding
* Delay na perseguição

**Configuração (exemplo):**

* Duração: 2.5s
* Cooldown: 4s
* Área de efeito circular

---

### 6.3 Bandeiras

* Total por fase: **10**
* Coleta obrigatória para vencer
* Cada bandeira:

  * Soma pontos
  * Atualiza HUD
* Distribuídas em áreas de risco

---

### 6.4 Inimigos

**Tipo:** Carros perseguidores (vermelhos)

**IA:**

* Pathfinding BFS em grid
* Recalcula rota periodicamente
* Prioriza caminho mais curto até o jogador

**Estados:**

* Perseguição
* Confusão (fumaça)
* Respawn após colisão

---

### 6.5 Colisão e Vidas

* Colisão com inimigo:

  * Perde 1 vida
  * Respawn do jogador
* Total inicial: 3 vidas
* Sem invencibilidade prolongada (arcade)

---

### 6.6 Tempo

* Tempo limite por fase
* Conta regressiva
* Tempo zerado → derrota
* Exibido no HUD

---

## 7. HUD e Interface

### HUD Principal

Exibe:

* Pontuação
* Tempo restante
* Vidas
* Bandeiras coletadas
* Mini-map radar

### Radar

* Visão simplificada do mapa
* Mostra:

  * Jogador
  * Inimigos
  * Bandeiras
* Sem fog of war (na demo)

---

## 8. Menus

### 8.1 Title Screen

* Logo
* Start Game
* Options
* Quit

---

### 8.2 Options Menu

Configurações:

* Dificuldade
* Volume música
* Volume efeitos
* Fullscreen
* VSync

---

### 8.3 Pause Menu

* Resume
* Options
* Quit to Title

---

### 8.4 Game Over

* Score final
* High score
* Retry
* Quit

---

## 9. Sistema de Pontuação

| Ação             | Pontos |
| ---------------- | ------ |
| Coletar bandeira | +100   |
| Completar fase   | +500   |
| Tempo restante   | bônus  |

**High Score**

* Salvo localmente em:

  ```
  saves/highscore.json
  ```

---

## 10. Fase (Level Design)

### Estrutura da Fase

* Baseada em grid
* Tiles:

  * Estrada
  * Parede
  * Grama
  * Borda
* JSON define:

  * Layout
  * Spawns
  * Flags
  * Tempo limite

### Objetivo da Fase 01

* Introduzir todas as mecânicas
* Layout simples com pontos de estrangulamento
* Risco gradual

---

## 11. Áudio

### Música

* Loop contínuo durante gameplay
* Volume configurável

### Efeitos Sonoros

* Motor do carro
* Coleta de bandeira
* Fumaça
* Colisão
* Vitória
* Derrota
* Navegação de menus

---

## 12. Estilo Visual

* Pixel art simples
* Vista top-down
* Cores contrastantes
* UI clara e legível
* Assets **originais**

---

## 13. Arquitetura Técnica (Resumo)

* Scene system
* Entity base
* World em grid
* Pathfinding desacoplado
* Assets manager
* Audio manager
* State machine para cenas

---

## 14. Escopo da Demo

### Incluído

* 1 fase completa
* Gameplay completo
* Menus
* HUD
* High score
* Sons e música

### Fora do escopo (futuro)

* Múltiplas fases
* Inimigos especializados
* Power-ups
* Multiplayer
* Rankings online

---

## 15. Possíveis Expansões Futuras

* 3–5 fases adicionais
* IA com emboscada
* Radar com fog of war
* Bônus temporários
* Dificuldades dinâmicas
* Port mobile (Android)

---

## 16. Métricas de Sucesso da Demo

* Jogador entende as regras em < 30s
* Taxa de conclusão da fase > 60%
* Uso estratégico da fumaça
* Feedback positivo sobre controles

---

## 17. Conclusão

Este GDD define um **jogo arcade completo, funcional e extensível**, com:

* Mecânicas claras
* Escopo controlado
* Arquitetura limpa
* Potencial de expansão comercial ou educacional