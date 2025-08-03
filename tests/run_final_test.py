#!/usr/bin/env python3
"""
Script simplificado para executar o teste final do Sand of Duat
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_basic_imports():
    """Testa se os módulos principais podem ser importados."""
    results = {}
    
    # Test main game module
    try:
        import main
        results['main_module'] = True
    except Exception as e:
        results['main_module'] = False
        results['main_error'] = str(e)
    
    # Test core systems
    core_modules = [
        'sands_duat.core.engine',
        'sands_duat.core.hourglass', 
        'sands_duat.core.cards',
        'sands_duat.ui.ui_manager',
        'sands_duat.ui.deck_builder'
    ]
    
    results['core_systems'] = {}
    for module in core_modules:
        try:
            __import__(module)
            results['core_systems'][module] = True
        except Exception as e:
            results['core_systems'][module] = False
            results[f'{module}_error'] = str(e)
    
    return results

def test_file_structure():
    """Verifica se a estrutura de arquivos está correta."""
    results = {}
    
    required_files = [
        'main.py',
        'sands_duat/__init__.py',
        'sands_duat/core/__init__.py',
        'sands_duat/ui/__init__.py',
        'requirements.txt'
    ]
    
    for file_path in required_files:
        full_path = project_root / file_path
        results[file_path] = full_path.exists()
    
    return results

def test_game_initialization():
    """Testa se o jogo pode ser inicializado sem erros críticos."""
    results = {}
    
    try:
        # Test pygame initialization
        import pygame
        pygame.init()
        results['pygame_init'] = True
        
        # Test basic game components
        from sands_duat.core.hourglass import HourGlass
        hourglass = HourGlass()
        hourglass.set_sand(5)
        results['hourglass_system'] = hourglass.current_sand == 5
        
        # Test card system
        from sands_duat.core.cards import Card, CardType
        test_card = Card("Test", "Test card", 1, CardType.ATTACK)
        results['card_system'] = test_card.name == "Test"
        
        pygame.quit()
        
    except Exception as e:
        results['initialization_error'] = str(e)
        results['pygame_init'] = False
        results['hourglass_system'] = False
        results['card_system'] = False
    
    return results

def test_advanced_systems():
    """Testa sistemas mais avançados."""
    results = {}
    
    try:
        # Test AI system
        from sands_duat.ai.enemy_ai_enhanced import EnhancedEnemyAI, EnemyPersonality
        ai = EnhancedEnemyAI("test", EnemyPersonality.MUMMY_WARRIOR)
        results['ai_system'] = True
    except Exception as e:
        results['ai_system'] = False
        results['ai_error'] = str(e)
    
    try:
        # Test save system
        from sands_duat.core.save_system import SaveSystem
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            save_system = SaveSystem(save_directory=temp_dir)
            results['save_system'] = True
    except Exception as e:
        results['save_system'] = False
        results['save_error'] = str(e)
    
    try:
        # Test progression system
        from sands_duat.core.game_progression_manager import GameProgressionManager
        progression = GameProgressionManager()
        results['progression_system'] = True
    except Exception as e:
        results['progression_system'] = False
        results['progression_error'] = str(e)
    
    try:
        # Test audio system
        from sands_duat.audio.audio_manager import AudioManager
        audio = AudioManager()
        results['audio_system'] = True
    except Exception as e:
        results['audio_system'] = False
        results['audio_error'] = str(e)
    
    return results

def calculate_score(test_results):
    """Calcula pontuação geral baseada nos resultados."""
    total_score = 0
    max_score = 0
    
    # Basic imports (30 points)
    if test_results.get('imports', {}).get('main_module'):
        total_score += 10
    max_score += 10
    
    core_systems = test_results.get('imports', {}).get('core_systems', {})
    working_systems = sum(1 for working in core_systems.values() if working)
    total_systems = len(core_systems)
    if total_systems > 0:
        total_score += int((working_systems / total_systems) * 20)
    max_score += 20
    
    # File structure (20 points)
    file_structure = test_results.get('file_structure', {})
    working_files = sum(1 for exists in file_structure.values() if exists)
    total_files = len(file_structure)
    if total_files > 0:
        total_score += int((working_files / total_files) * 20)
    max_score += 20
    
    # Initialization (30 points)
    init_results = test_results.get('initialization', {})
    if init_results.get('pygame_init'):
        total_score += 10
    if init_results.get('hourglass_system'):
        total_score += 10
    if init_results.get('card_system'):
        total_score += 10
    max_score += 30
    
    # Advanced systems (20 points)
    advanced = test_results.get('advanced_systems', {})
    working_advanced = sum(1 for system in ['ai_system', 'save_system', 'progression_system', 'audio_system'] 
                          if advanced.get(system))
    total_score += int((working_advanced / 4) * 20)
    max_score += 20
    
    return total_score, max_score

def generate_report(test_results, score, max_score):
    """Gera relatório final."""
    percentage = (score / max_score) * 100 if max_score > 0 else 0
    
    if percentage >= 90:
        grade = "EXCELENTE"
        status = "PRONTO_PARA_LANCAMENTO"
    elif percentage >= 80:
        grade = "BOM"
        status = "PEQUENOS_PROBLEMAS"
    elif percentage >= 70:
        grade = "ACEITAVEL"
        status = "PRECISA_TRABALHO"
    elif percentage >= 60:
        grade = "PROBLEMATICO"
        status = "PROBLEMAS_SIGNIFICATIVOS"
    else:
        grade = "CRITICO"
        status = "REFORMULACAO_NECESSARIA"
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'score': score,
        'max_score': max_score,
        'percentage': percentage,
        'grade': grade,
        'status': status,
        'test_results': test_results
    }
    
    return report

def main():
    """Função principal do teste."""
    print("=" * 60)
    print("TESTE FINAL COMPLETO - SANDS OF DUAT")
    print("=" * 60)
    
    test_results = {}
    
    print("\n1. Testando importações básicas...")
    test_results['imports'] = test_basic_imports()
    
    print("2. Verificando estrutura de arquivos...")
    test_results['file_structure'] = test_file_structure()
    
    print("3. Testando inicialização do jogo...")
    test_results['initialization'] = test_game_initialization()
    
    print("4. Testando sistemas avançados...")
    test_results['advanced_systems'] = test_advanced_systems()
    
    # Calculate score
    score, max_score = calculate_score(test_results)
    
    # Generate report
    report = generate_report(test_results, score, max_score)
    
    # Save report
    report_path = Path(__file__).parent / "final_test_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("RELATORIO FINAL")
    print("=" * 60)
    print(f"Pontuacao: {score}/{max_score} ({report['percentage']:.1f}%)")
    print(f"Qualidade: {report['grade']}")
    print(f"Status: {report['status']}")
    
    print("\nDETALHES:")
    
    # Imports
    imports = test_results['imports']
    print(f"- Modulo principal: {'OK' if imports.get('main_module') else 'FALHA'}")
    
    core_systems = imports.get('core_systems', {})
    working_core = sum(1 for working in core_systems.values() if working)
    print(f"- Sistemas core: {working_core}/{len(core_systems)} OK")
    
    # File structure
    file_structure = test_results['file_structure']
    working_files = sum(1 for exists in file_structure.values() if exists)
    print(f"- Estrutura arquivos: {working_files}/{len(file_structure)} OK")
    
    # Initialization
    init_results = test_results['initialization']
    init_working = sum(1 for system in ['pygame_init', 'hourglass_system', 'card_system'] 
                      if init_results.get(system))
    print(f"- Inicializacao: {init_working}/3 sistemas OK")
    
    # Advanced
    advanced = test_results['advanced_systems']
    advanced_working = sum(1 for system in ['ai_system', 'save_system', 'progression_system', 'audio_system'] 
                          if advanced.get(system))
    print(f"- Sistemas avancados: {advanced_working}/4 OK")
    
    print(f"\nRelatorio salvo em: {report_path}")
    
    if report['percentage'] >= 70:
        print("\nJOGO APROVADO para uso!")
    else:
        print("\nJOGO PRECISA DE MELHORIAS antes do uso.")
    
    return 0 if report['percentage'] >= 70 else 1

if __name__ == '__main__':
    sys.exit(main())