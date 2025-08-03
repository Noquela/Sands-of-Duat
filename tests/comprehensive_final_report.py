#!/usr/bin/env python3
"""
Relatório Final Abrangente - Sands of Duat
Análise detalhada da qualidade e estado atual do jogo
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class SandsOfDuatQualityAssessment:
    """Avaliação completa da qualidade do Sands of Duat."""
    
    def __init__(self):
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'game_info': {
                'name': 'Sands of Duat',
                'genre': 'Roguelike Deck-Builder',
                'theme': 'Egyptian Mythology',
                'target_platform': 'PC (Ultrawide Support)'
            },
            'assessment_results': {},
            'system_scores': {},
            'recommendations': [],
            'critical_issues': [],
            'working_features': [],
            'overall_quality': {}
        }
    
    def assess_code_architecture(self):
        """Avalia a arquitetura do código."""
        results = {
            'score': 0,
            'max_score': 100,
            'details': []
        }
        
        # Check project structure
        expected_structure = {
            'main.py': 'Entry point do jogo',
            'sands_duat/': 'Pacote principal',
            'sands_duat/core/': 'Sistemas centrais',
            'sands_duat/ui/': 'Interface do usuário',
            'sands_duat/ai/': 'Sistema de IA',
            'sands_duat/audio/': 'Sistema de áudio',
            'sands_duat/content/': 'Conteúdo do jogo',
            'tests/': 'Testes automatizados',
            'docs/': 'Documentação'
        }
        
        structure_score = 0
        for path, description in expected_structure.items():
            full_path = project_root / path
            if full_path.exists():
                results['details'].append(f"✓ {path} - {description}")
                structure_score += 10
            else:
                results['details'].append(f"✗ {path} - {description} (FALTANDO)")
        
        results['score'] += min(structure_score, 40)  # Max 40 points for structure
        
        # Check code organization
        core_modules = [
            'engine.py', 'hourglass.py', 'cards.py', 'combat.py',
            'save_system.py', 'game_progression_manager.py'
        ]
        
        core_score = 0
        core_path = project_root / 'sands_duat' / 'core'
        if core_path.exists():
            for module in core_modules:
                if (core_path / module).exists():
                    core_score += 5
                    results['details'].append(f"✓ Core module: {module}")
                else:
                    results['details'].append(f"✗ Core module: {module} (FALTANDO)")
        
        results['score'] += min(core_score, 30)  # Max 30 points for core modules
        
        # Check UI organization
        ui_modules = ['deck_builder.py', 'combat_screen.py', 'ui_manager.py']
        ui_score = 0
        ui_path = project_root / 'sands_duat' / 'ui'
        if ui_path.exists():
            for module in ui_modules:
                if (ui_path / module).exists():
                    ui_score += 10
                    results['details'].append(f"✓ UI module: {module}")
                else:
                    results['details'].append(f"✗ UI module: {module} (FALTANDO)")
        
        results['score'] += min(ui_score, 30)  # Max 30 points for UI modules
        
        results['percentage'] = (results['score'] / results['max_score']) * 100
        return results
    
    def assess_content_systems(self):
        """Avalia os sistemas de conteúdo."""
        results = {
            'score': 0,
            'max_score': 100,
            'details': []
        }
        
        # Check card content
        content_path = project_root / 'sands_duat' / 'content'
        if content_path.exists():
            results['details'].append("✓ Diretório de conteúdo existe")
            results['score'] += 20
            
            # Check card files
            card_files = ['egyptian_cards.yaml', 'starter_cards.yaml']
            for card_file in card_files:
                card_path = content_path / 'cards' / card_file
                if card_path.exists():
                    results['details'].append(f"✓ Arquivo de cartas: {card_file}")
                    results['score'] += 15
                else:
                    results['details'].append(f"✗ Arquivo de cartas: {card_file} (FALTANDO)")
            
            # Check enemy files
            enemy_files = ['basic_enemies.yaml', 'hourglass_enemies.yaml']
            for enemy_file in enemy_files:
                enemy_path = content_path / 'enemies' / enemy_file
                if enemy_path.exists():
                    results['details'].append(f"✓ Arquivo de inimigos: {enemy_file}")
                    results['score'] += 10
                else:
                    results['details'].append(f"✗ Arquivo de inimigos: {enemy_file} (FALTANDO)")
            
            # Check deck files
            deck_files = ['starter_decks.yaml']
            for deck_file in deck_files:
                deck_path = content_path / 'decks' / deck_file
                if deck_path.exists():
                    results['details'].append(f"✓ Arquivo de decks: {deck_file}")
                    results['score'] += 10
                else:
                    results['details'].append(f"✗ Arquivo de decks: {deck_file} (FALTANDO)")
        else:
            results['details'].append("✗ Diretório de conteúdo não encontrado")
        
        # Check loading systems
        content_loaders = ['egyptian_card_loader.py', 'loader.py', 'starter_cards.py']
        for loader in content_loaders:
            loader_path = content_path / loader
            if loader_path.exists():
                results['details'].append(f"✓ Sistema de carregamento: {loader}")
                results['score'] += 5
            else:
                results['details'].append(f"✗ Sistema de carregamento: {loader} (FALTANDO)")
        
        results['percentage'] = (results['score'] / results['max_score']) * 100
        return results
    
    def assess_game_features(self):
        """Avalia as funcionalidades implementadas do jogo."""
        results = {
            'score': 0,
            'max_score': 100,
            'details': []
        }
        
        feature_systems = {
            'HourGlass System': 'sands_duat/core/hourglass.py',
            'Card System': 'sands_duat/core/cards.py',
            'Combat System': 'sands_duat/core/combat.py',
            'Enhanced Combat': 'sands_duat/core/combat_enhanced.py',
            'Enemy AI': 'sands_duat/ai/enemy_ai_enhanced.py',
            'Save System': 'sands_duat/core/save_system.py',
            'Progression System': 'sands_duat/core/game_progression_manager.py',
            'Achievement System': 'sands_duat/core/achievements.py',
            'Deck Builder': 'sands_duat/ui/deck_builder.py',
            'Animation System': 'sands_duat/ui/animation_system.py',
            'Particle System': 'sands_duat/ui/particle_system.py',
            'Audio Manager': 'sands_duat/audio/audio_manager.py',
            'Combat Sounds': 'sands_duat/audio/combat_sounds.py',
            'Music Manager': 'sands_duat/audio/music_manager.py'
        }
        
        implemented_features = 0
        for feature, file_path in feature_systems.items():
            full_path = project_root / file_path
            if full_path.exists():
                results['details'].append(f"✓ {feature} implementado")
                implemented_features += 1
                results['score'] += 7  # ~100/14 features
            else:
                results['details'].append(f"✗ {feature} não encontrado")
        
        # Bonus points for advanced features
        advanced_features = {
            'Backup Manager': 'sands_duat/core/backup_manager.py',
            'Save Security': 'sands_duat/core/save_security.py',
            'Combat Effects': 'sands_duat/ui/combat_effects.py',
            'Theme System': 'sands_duat/ui/theme.py'
        }
        
        for feature, file_path in advanced_features.items():
            full_path = project_root / file_path
            if full_path.exists():
                results['details'].append(f"✓ {feature} (Avançado)")
                results['score'] += 2
        
        results['percentage'] = (results['score'] / results['max_score']) * 100
        results['implemented_count'] = implemented_features
        results['total_features'] = len(feature_systems)
        return results
    
    def assess_documentation_quality(self):
        """Avalia a qualidade da documentação."""
        results = {
            'score': 0,
            'max_score': 100,
            'details': []
        }
        
        # Check main documentation
        docs_path = project_root / 'docs'
        if docs_path.exists():
            results['details'].append("✓ Diretório de documentação existe")
            results['score'] += 20
            
            # Check specific documentation files
            doc_files = {
                'README.md': 'Documentação principal',
                'COMPLETE_SAVE_PROGRESSION_SYSTEM.md': 'Sistema de save/progressão',
                'COMPREHENSIVE_CARD_EFFECTS_REPORT.md': 'Efeitos de cartas',
                'COMPREHENSIVE_DRAG_DROP_ANALYSIS_REPORT.md': 'Sistema drag-drop',
                'ULTRAWIDE_DISPLAY_ANALYSIS_REPORT.md': 'Suporte ultrawide'
            }
            
            for doc_file, description in doc_files.items():
                doc_path = docs_path / doc_file
                if doc_path.exists():
                    results['details'].append(f"✓ {description}: {doc_file}")
                    results['score'] += 10
                else:
                    results['details'].append(f"✗ {description}: {doc_file} (FALTANDO)")
        else:
            results['details'].append("✗ Diretório de documentação não encontrado")
        
        # Check README at root
        root_readme = project_root / 'README.md'
        if root_readme.exists():
            results['details'].append("✓ README principal existe")
            results['score'] += 15
        else:
            results['details'].append("✗ README principal não encontrado")
        
        # Check analysis documentation
        analysis_path = project_root / 'analysis'
        if analysis_path.exists():
            results['details'].append("✓ Documentação de análise existe")
            results['score'] += 10
        
        # Check MCP analysis
        mcp_path = project_root / 'mcp_analysis'
        if mcp_path.exists():
            results['details'].append("✓ Análise MCP documentada")
            results['score'] += 5
        
        results['percentage'] = (results['score'] / results['max_score']) * 100
        return results
    
    def assess_testing_coverage(self):
        """Avalia a cobertura de testes."""
        results = {
            'score': 0,
            'max_score': 100,
            'details': []
        }
        
        tests_path = project_root / 'tests'
        if tests_path.exists():
            results['details'].append("✓ Diretório de testes existe")
            results['score'] += 20
            
            # Count test files
            test_files = list(tests_path.glob('test_*.py'))
            results['details'].append(f"✓ {len(test_files)} arquivos de teste encontrados")
            results['score'] += min(len(test_files) * 5, 40)  # Max 40 points for test files
            
            # Check specific test categories
            test_categories = {
                'test_cards.py': 'Testes de sistema de cartas',
                'test_combat.py': 'Testes de sistema de combate',
                'test_hourglass.py': 'Testes de sistema HourGlass',
                'test_integration.py': 'Testes de integração',
                'test_deck_builder*.py': 'Testes de deck builder'
            }
            
            for pattern, description in test_categories.items():
                matching_files = list(tests_path.glob(pattern))
                if matching_files:
                    results['details'].append(f"✓ {description}: {len(matching_files)} arquivo(s)")
                    results['score'] += 8
                else:
                    results['details'].append(f"✗ {description}: não encontrado")
        else:
            results['details'].append("✗ Diretório de testes não encontrado")
        
        results['percentage'] = (results['score'] / results['max_score']) * 100
        return results
    
    def identify_critical_issues(self):
        """Identifica problemas críticos baseados nos testes anteriores."""
        issues = []
        
        # Check previous test report if exists
        test_report_path = project_root / 'tests' / 'final_test_report.json'
        if test_report_path.exists():
            try:
                with open(test_report_path, 'r') as f:
                    test_data = json.load(f)
                    
                # Check import issues
                imports = test_data.get('test_results', {}).get('imports', {})
                if not imports.get('main_module'):
                    issues.append("CRÍTICO: Módulo principal não pode ser importado")
                
                core_systems = imports.get('core_systems', {})
                failed_systems = [k for k, v in core_systems.items() if not v]
                if failed_systems:
                    issues.append(f"CRÍTICO: Sistemas core falhando: {', '.join(failed_systems)}")
                
                # Check initialization issues
                init_results = test_data.get('test_results', {}).get('initialization', {})
                if 'initialization_error' in init_results:
                    issues.append(f"CRÍTICO: Erro na inicialização: {init_results['initialization_error']}")
                
                # Check advanced system issues
                advanced = test_data.get('test_results', {}).get('advanced_systems', {})
                if not advanced.get('save_system'):
                    issues.append("IMPORTANTE: Sistema de save não funcionando")
                if not advanced.get('ai_system'):
                    issues.append("IMPORTANTE: Sistema de IA não funcionando")
                    
            except Exception as e:
                issues.append(f"Erro ao analisar relatório de teste: {e}")
        
        # Check for missing critical files
        critical_files = [
            'main.py',
            'sands_duat/__init__.py',
            'requirements.txt'
        ]
        
        for file_path in critical_files:
            if not (project_root / file_path).exists():
                issues.append(f"CRÍTICO: Arquivo essencial faltando: {file_path}")
        
        return issues
    
    def generate_recommendations(self):
        """Gera recomendações baseadas na análise."""
        recommendations = []
        
        # Based on architecture assessment
        arch_results = self.report['assessment_results'].get('architecture', {})
        if arch_results.get('percentage', 0) < 80:
            recommendations.append("Melhorar organização da arquitetura do código")
        
        # Based on content assessment
        content_results = self.report['assessment_results'].get('content', {})
        if content_results.get('percentage', 0) < 70:
            recommendations.append("Adicionar mais conteúdo de jogo (cartas, inimigos, eventos)")
        
        # Based on features assessment
        features_results = self.report['assessment_results'].get('features', {})
        if features_results.get('percentage', 0) < 80:
            recommendations.append("Completar implementação de funcionalidades principais")
        
        # Based on documentation assessment
        docs_results = self.report['assessment_results'].get('documentation', {})
        if docs_results.get('percentage', 0) < 70:
            recommendations.append("Melhorar documentação do projeto")
        
        # Based on testing assessment
        testing_results = self.report['assessment_results'].get('testing', {})
        if testing_results.get('percentage', 0) < 60:
            recommendations.append("Expandir cobertura de testes automatizados")
        
        # General recommendations
        recommendations.extend([
            "Resolver problemas de importação de módulos",
            "Implementar sistema de CI/CD para testes automáticos",
            "Adicionar logs de debugging mais detalhados",
            "Otimizar performance para displays ultrawide",
            "Implementar sistema de telemetria para monitoramento"
        ])
        
        return recommendations
    
    def identify_working_features(self):
        """Identifica funcionalidades que estão funcionando."""
        working = []
        
        # Check from features assessment
        features_results = self.report['assessment_results'].get('features', {})
        if 'details' in features_results:
            working_details = [d for d in features_results['details'] if d.startswith('✓')]
            working.extend([d.replace('✓ ', '') for d in working_details])
        
        # Add from previous test if available
        test_report_path = project_root / 'tests' / 'final_test_report.json'
        if test_report_path.exists():
            try:
                with open(test_report_path, 'r') as f:
                    test_data = json.load(f)
                    
                advanced = test_data.get('test_results', {}).get('advanced_systems', {})
                if advanced.get('progression_system'):
                    working.append("Sistema de progressão funcionando")
                if advanced.get('audio_system'):
                    working.append("Sistema de áudio funcionando")
                    
            except Exception:
                pass
        
        return working
    
    def calculate_overall_quality(self):
        """Calcula qualidade geral do projeto."""
        scores = []
        weights = {
            'architecture': 0.25,
            'content': 0.20,
            'features': 0.30,
            'documentation': 0.15,
            'testing': 0.10
        }
        
        total_weighted_score = 0
        total_weight = 0
        
        for category, weight in weights.items():
            if category in self.report['assessment_results']:
                percentage = self.report['assessment_results'][category].get('percentage', 0)
                total_weighted_score += percentage * weight
                total_weight += weight
        
        overall_percentage = total_weighted_score / total_weight if total_weight > 0 else 0
        
        # Determine grade
        if overall_percentage >= 90:
            grade = "EXCELENTE"
            status = "PRONTO_PARA_LANCAMENTO"
        elif overall_percentage >= 80:
            grade = "BOM"
            status = "PEQUENOS_AJUSTES_NECESSARIOS"
        elif overall_percentage >= 70:
            grade = "ACEITAVEL"
            status = "MELHORIAS_IMPORTANTES_NECESSARIAS"
        elif overall_percentage >= 60:
            grade = "PROBLEMATICO"
            status = "REFATORACAO_SIGNIFICATIVA_NECESSARIA"
        else:
            grade = "CRITICO"
            status = "REFORMULACAO_COMPLETA_NECESSARIA"
        
        return {
            'percentage': overall_percentage,
            'grade': grade,
            'status': status,
            'weighted_scores': {k: self.report['assessment_results'].get(k, {}).get('percentage', 0) 
                               for k in weights.keys()}
        }
    
    def run_complete_assessment(self):
        """Executa avaliação completa do projeto."""
        print("=" * 80)
        print("AVALIAÇÃO COMPLETA DE QUALIDADE - SANDS OF DUAT")
        print("=" * 80)
        
        # Run all assessments
        print("\n1. Avaliando arquitetura do código...")
        self.report['assessment_results']['architecture'] = self.assess_code_architecture()
        
        print("2. Avaliando sistemas de conteúdo...")
        self.report['assessment_results']['content'] = self.assess_content_systems()
        
        print("3. Avaliando funcionalidades do jogo...")
        self.report['assessment_results']['features'] = self.assess_game_features()
        
        print("4. Avaliando documentação...")
        self.report['assessment_results']['documentation'] = self.assess_documentation_quality()
        
        print("5. Avaliando cobertura de testes...")
        self.report['assessment_results']['testing'] = self.assess_testing_coverage()
        
        print("6. Identificando problemas críticos...")
        self.report['critical_issues'] = self.identify_critical_issues()
        
        print("7. Gerando recomendações...")
        self.report['recommendations'] = self.generate_recommendations()
        
        print("8. Identificando funcionalidades funcionais...")
        self.report['working_features'] = self.identify_working_features()
        
        print("9. Calculando qualidade geral...")
        self.report['overall_quality'] = self.calculate_overall_quality()
        
        return self.report
    
    def save_report(self, filename='comprehensive_quality_report.json'):
        """Salva o relatório em arquivo."""
        report_path = project_root / 'tests' / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        return report_path
    
    def print_summary(self):
        """Imprime resumo do relatório."""
        print("\n" + "=" * 80)
        print("RESUMO DA AVALIAÇÃO DE QUALIDADE")
        print("=" * 80)
        
        overall = self.report['overall_quality']
        print(f"QUALIDADE GERAL: {overall['grade']} ({overall['percentage']:.1f}%)")
        print(f"STATUS: {overall['status']}")
        
        print("\nPONTUAÇÕES POR CATEGORIA:")
        for category, score in overall['weighted_scores'].items():
            category_name = {
                'architecture': 'Arquitetura',
                'content': 'Conteúdo',
                'features': 'Funcionalidades',
                'documentation': 'Documentação',
                'testing': 'Testes'
            }.get(category, category)
            print(f"  {category_name}: {score:.1f}%")
        
        print(f"\nFUNCIONALIDADES IMPLEMENTADAS: {len(self.report['working_features'])}")
        print(f"PROBLEMAS CRÍTICOS: {len(self.report['critical_issues'])}")
        print(f"RECOMENDAÇÕES: {len(self.report['recommendations'])}")
        
        if self.report['critical_issues']:
            print("\nPROBLEMAS CRÍTICOS:")
            for issue in self.report['critical_issues'][:5]:  # Show first 5
                print(f"  - {issue}")
            if len(self.report['critical_issues']) > 5:
                print(f"  ... e mais {len(self.report['critical_issues']) - 5} problemas")
        
        print(f"\nRELATÓRIO COMPLETO SALVO EM: tests/comprehensive_quality_report.json")


def main():
    """Função principal."""
    assessment = SandsOfDuatQualityAssessment()
    report = assessment.run_complete_assessment()
    
    # Save report
    report_path = assessment.save_report()
    
    # Print summary
    assessment.print_summary()
    
    # Return appropriate exit code
    overall_percentage = report['overall_quality']['percentage']
    return 0 if overall_percentage >= 70 else 1


if __name__ == '__main__':
    sys.exit(main())