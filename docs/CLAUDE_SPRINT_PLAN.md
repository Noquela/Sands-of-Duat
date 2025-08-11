# 🏺 SANDS OF DUAT - HADES-LEVEL POLISH ROADMAP

**Objetivo:** Transformar o jogo em uma experiência visual e interativa de qualidade AAA, com foco em ultrawide 3440x1440 e estilo Egyptian-Hades.

---

## 🎯 **SPRINT 1 – UI/UX CLARITY & ULTRAWIDE OPTIMIZATION**

### **Problema Atual:**
- Elementos perdidos no espaço ultrawide 3440x1440
- Hierarquia visual confusa
- HUD poluído e pouco intuitivo
- Textos pequenos demais para a resolução

### **Implementar:**

#### **1.1 Sistema de Layout Responsivo Ultrawide**
```python
# Criar novo sistema de proporções relativas
class UltraWideLayout:
    # Margens proporcionais baseadas na resolução
    CONTENT_MARGIN_PERCENT = 0.15  # 15% de margem lateral
    BUTTON_SCALE_FACTOR = 1.4      # Botões 40% maiores em ultrawide
    TEXT_SCALE_FACTOR = 1.3        # Texto 30% maior
    CARD_SPACING_FACTOR = 1.5      # Mais espaço entre elementos
```

#### **1.2 Redesenhar Hierarquia Visual**
- **Títulos**: FontSize aumentado de 48 para 72px
- **Botões**: Height de 50 para 70px, Width proporcionalmente maior
- **Cards**: Espaçamento mínimo de 20px entre cards no campo de batalha
- **HUD**: Concentrar informações essenciais em 25% da tela

#### **1.3 HUD Minimalista de Combate**
- Vida/Mana: Barras horizontais top/bottom com gradiente suave
- Botões de ação: Canto inferior direito, tamanho maior
- Informações temporárias: Tooltips que aparecem só no hover
- Remover elementos decorativos desnecessários

---

## 🎨 **SPRINT 2 – IDENTIDADE VISUAL & ARTE 4K**

### **Problema Atual:**
- Assets inconsistentes e de baixa resolução
- Falta identidade visual coesa
- Cards genéricas sem personalidade

### **Implementar:**

#### **2.1 Pipeline de Arte com IA Local**
```bash
# Setup completo de geração de assets
pip install diffusers transformers accelerate xformers
# Baixar Stable Diffusion XL + LoRA Egyptian Art
# Criar batch scripts para gerar todos os assets em 4K
```

#### **2.2 Prompts Padronizados para Consistência**
```python
EGYPTIAN_ART_STYLE = {
    "base_prompt": "ancient egyptian art style, papyrus texture, hieroglyphs, golden accents, cinematic lighting, ultra detailed, 4k masterpiece",
    "negative_prompt": "modern, cartoon, anime, low quality, blurry, text, watermark",
    "settings": {
        "width": 2048, "height": 2048,  # Base 4K para scaling
        "steps": 30, "cfg_scale": 7.5,
        "sampler": "DPM++ 2M Karras"
    }
}
```

#### **2.3 Assets a Gerar:**
- **Backgrounds**: Menu, combat, deck builder (4096x2048)
- **Card Frames**: Common, Rare, Epic, Legendary com bordas animadas
- **Character Portraits**: Ra, Anubis, Isis, Set, Thoth, Horus (1024x1024)
- **UI Elements**: Buttons, icons, decorative borders (vetorizados)
- **Particle Textures**: Sand, fire, water, light effects

---

## ⚡ **SPRINT 3 – SISTEMA DE ANIMAÇÕES DINÂMICAS**

### **Problema Atual:**
- Jogo completamente estático
- Nenhum feedback visual nas ações
- Transições abruptas entre telas

### **Implementar:**

#### **3.1 Sistema de Animação de Cards**
```python
class CardAnimationSystem:
    def animate_card_play(self, card, target_pos):
        # Sequência: hover -> drag -> play -> effect
        - Scale up (1.0 -> 1.1) em 0.2s
        - Bezier curve movement para posição final
        - Rotate slight durante movimento
        - Scale down + glow effect no final
        
    def animate_attack(self, attacker, defender):
        # Flash + particle trail + screen shake
        - Attacker: brief scale + brightness
        - Particle: linha de energia até defender
        - Defender: shake + red flash se dano
        - Numbers: float up com fade out
```

#### **3.2 Animações de Interface**
- **Menu Transitions**: Fade + slide lateral (0.5s duration)
- **Button Hover**: Scale 1.05 + color shift + drop shadow
- **Loading**: Animated hieroglyphs rotating
- **Background**: Subtle parallax scrolling

#### **3.3 Efeitos de Combate por Tipo**
- **Ataque**: Lightning bolt particle, screen flash
- **Cura**: Green healing spiral, soft glow
- **Buff**: Golden aura pulsing
- **Debuff**: Dark smoke swirling
- **Ultimate**: Full screen effect + camera shake

---

## 🎮 **SPRINT 4 – UX FLOW & PLAYER FEEDBACK**

### **Problema Atual:**
- Jogador não entende estado atual do jogo
- Falta feedback nas ações
- Curva de aprendizado muito alta

### **Implementar:**

#### **4.1 Sistema de Feedback Audiovisual**
```python
class FeedbackSystem:
    def on_valid_action(self, action_type):
        - Play sound effect (Egyptian themed)
        - Visual confirmation (green glow/checkmark)
        - Haptic feedback if controller connected
        
    def on_invalid_action(self, reason):
        - Red outline + shake animation
        - Brief tooltip explaining why invalid
        - Subtle error sound (not annoying)
```

#### **4.2 Estado de Jogo Sempre Visível**
- **Turno Atual**: Grande indicador "YOUR TURN" / "ENEMY TURN"
- **Mana Available**: Destacar cards jogáveis com glow verde
- **Next Phase**: Contador visual para próxima fase
- **Win Condition**: Progress bar para vitória

#### **4.3 Tutorial Integrado (Optional)**
- **First Time**: Overlay arrows + text bubbles
- **Progressive Disclosure**: Unlock features gradualmente
- **Quick Tips**: Context-sensitive durante gameplay

---

## 🚀 **IMPLEMENTAÇÃO PRÁTICA**

### **Estrutura de Arquivos a Criar:**
```
src/sands_of_duat/
├── ui/
│   ├── responsive/
│   │   ├── ultrawide_layout.py
│   │   ├── scaling_manager.py
│   │   └── responsive_components.py
│   ├── animations/
│   │   ├── card_animator.py
│   │   ├── transition_manager.py
│   │   ├── particle_system.py
│   │   └── feedback_system.py
│   └── themes/
│       ├── egyptian_theme.py
│       └── color_schemes.py
├── assets/
│   ├── generated_4k/
│   │   ├── backgrounds/
│   │   ├── cards/
│   │   ├── characters/
│   │   └── ui_elements/
│   └── animations/
│       ├── card_effects/
│       └── ui_transitions/
└── scripts/
    ├── generate_all_assets.py
    └── optimize_for_ultrawide.py
```

### **Prioridades de Execução:**
1. **Semana 1**: Sprint 1 (Layout + UI clarity)
2. **Semana 2**: Sprint 2 (Arte 4K + identidade visual)  
3. **Semana 3**: Sprint 3 (Sistema de animações)
4. **Semana 4**: Sprint 4 (UX polish + feedback)

### **Resultado Esperado:**
- **Performance**: 60fps estável em 3440x1440
- **Visual Quality**: Comparável ao Hades em consistência
- **User Experience**: Intuitivo desde primeiro uso
- **Polish Level**: Pronto para Early Access

---

## 📋 **PROMPT PARA CLAUDE CODE:**

"Implementar sistema completo de polish visual e UX para Sands of Duat, transformando-o em experiência AAA. Foco em ultrawide 3440x1440, estilo Egyptian-Hades, animações fluidas e clareza visual. Seguir exatamente os 4 sprints definidos, criando todos os arquivos necessários, sistema de arte com IA local, animações de cards e feedback audiovisual. Priorizar qualidade visual e responsividade ultrawide."