# 🏺 Sand of Duat - Development Roadmap

## Visão Geral

Este roadmap está estruturado em 5 sprints com prioridades claras para orientar a próxima fase de desenvolvimento do jogo. Cada sprint pode durar 1–2 semanas dependendo da complexidade e da disponibilidade da equipe.

---

## 🟧 Sprint 1 – Integração Básica e Adaptação a Ultrawide (Prioridade Alta)

**Objetivo:** Substituir placeholders e garantir que o jogo se adapte bem a 3440 × 1440.

### 1. Integrar assets de alta resolução

- Carregar fundos 4K de cada tela via `asset_loader.load_background()` com base no mapeamento:
  - `bg_main_menu_4k.png`
  - `bg_deck_builder_4k.png`
  - `bg_combat_4k.png`
  - `bg_hall_of_gods_4k.png`
  - `bg_settings_4k.png`
- Utilizar retratos 2K e molduras de cartas de acordo com a raridade
- Integrar cartas animadas do diretório `animated_cards/`

### 2. Refatorar layouts com `Layout`

- Alterar o posicionamento de painéis e botões para usar:
  - `CONTENT_WIDTH`
  - `UI_SAFE_LEFT`
  - `UI_SAFE_RIGHT`
  - `SCREEN_CENTER`
- Escalar tamanhos de fontes e botões dinamicamente com base em `SCREEN_WIDTH`/`SCREEN_HEIGHT`
- Preencher laterais vazias com texturas ou padrões temáticos (hieróglifos ou partículas)

### 3. Incluir novos ícones no HUD

- Substituir barras simples de vida/mana por medidores com:
  - `ui_ankh_health_icon.png`
  - `ui_scarab_energy_icon.png`
  - `ui_khopesh_attack_icon.png`
  - `ui_shield_defense_icon.png`

---

## 🟧 Sprint 2 – Polimento de Telas e UX (Prioridade Alta)

**Objetivo:** Tornar cada tela visualmente coesa e agradável de usar.

### 1. Menu principal

- Ajustar a posição e estilo do título, centralizar os botões com espaçamento proporcional
- Adicionar animações sutis de fade‑in e partículas para vida
- Remover textos de debug no canto superior esquerdo

### 2. Deck Builder

- Reestruturar a UI: integrar fundo temático, barras laterais decoradas
- Painel para exibir detalhes da carta selecionada
- Usar molduras de alta resolução e arte completa das cartas
- Adicionar filtro visual por raridade
- Ajustar a navegação e a rolagem para funcionar suavemente em ultrawide

### 3. Combate

- Trocar backgrounds antigos pelo `bg_combat_4k.png`
- Redesigner a área de batalha com bordas egípcias decoradas
- Incorporar barras de mana e saúde personalizadas
- Adicionar efeitos de destaque quando cartas são selecionadas ou jogadas

---

## 🟧 Sprint 3 – Novas Funcionalidades e Conteúdo (Prioridade Média)

**Objetivo:** Enriquecer a experiência de jogo e criar espaço para progressão.

### 1. Hall of Gods / Coleção

- Implementar a tela de coleção com exibição de todas as cartas desbloqueadas
- Ordenadas por raridade e deus
- Permitir visualização ampliada com lore e efeitos

### 2. Sistema de salvamento

- Criar mecanismos para salvar e carregar:
  - Decks personalizados
  - Progresso de campanha
  - Configurações do usuário em arquivos JSON

### 3. Narrativa e diálogos

- Estruturar um módulo básico de narrativa para introduzir a mitologia egípcia entre combates
- Usando retratos 2K dos deuses e cenários 4K

---

## 🟧 Sprint 4 – Ajustes Finais e Qualidade (Prioridade Média)

**Objetivo:** Alcançar nível de polimento Hades‑like e preparar para playtest.

### 1. Tela de configurações completa

- Usar `bg_settings_4k.png` como fundo
- Organizar sliders de áudio e opções gráficas com ícones

### 2. Transições e efeitos

- Implementar um sistema genérico de transições (desvanecimentos, deslizamentos) entre telas
- Adicionar efeitos visuais (glow, partículas) aos botões e ao HUD

### 3. Testes de UX e ajustes finos

- Fazer sessões de playtest para coletar feedback sobre navegabilidade, legibilidade e estética
- Ajustar cores, fontes e elementos com base no retorno dos playtesters

---

## 🟧 Sprint 5 – Expansão de Arte e IA (Prioridade Baixa, Contínua)

**Objetivo:** Consolidar o pipeline de arte e garantir assets de qualidade AAA.

### 1. Treinamento e uso de LoRAs

- Treinar uma LoRA personalizada com 75–100 imagens egípcias para refinar o estilo
- Gerar mais variações de fundos e personagens
- Substituir gradualmente quaisquer assets provisórios pelos gerados via LoRA em resolução maior:
  - 1024×1536 para cartas
  - 2048×2048 para personagens
  - 4096×2048 para cenários

### 2. Ampliação das animações

- Criar spritesheets mais detalhados para cartas e efeitos de combate
  - Explosões de areia
  - Chamas azuis
- Otimizar compressão e integração usando `run_animation_pipeline.py` e o `quality_validator`

---

## 📋 Estrutura de Arquivos

### Assets Aprovados (Hades Quality)
- `assets/approved_hades_quality/backgrounds/` - Fundos 4K
- `assets/approved_hades_quality/cards/` - Arte das cartas
- `assets/approved_hades_quality/characters/` - Retratos 2K
- `assets/approved_hades_quality/ui_elements/` - Ícones de interface

### Código Principal
- `src/sands_of_duat/core/asset_loader.py` - Carregamento de assets
- `src/sands_of_duat/ui/components/` - Componentes de interface
- `src/sands_of_duat/ui/screens/` - Telas do jogo

---

## 🎯 Considerações Importantes

- **Sempre colocar arquivos dentro das pastas apropriadas**
- **Focar nos aspectos mais urgentes primeiro** (integração de assets, adaptação a ultrawide)
- **Garantir que as melhorias visuais e de usabilidade sejam concretizadas** antes de avançar para novas funcionalidades
- **Manter consistência com o estilo Hades** em todos os elementos visuais

---

*Essa estrutura em sprints ajuda a focar nos aspectos mais urgentes primeiro, garantindo que as melhorias visuais e de usabilidade sejam concretizadas antes de avançar para novas funcionalidades e o incremento de arte.*