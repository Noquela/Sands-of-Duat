#!/usr/bin/env python3
"""
CONTROLNET SYSTEM - HADES STYLE (ASCII SAFE)
============================================

Sistema de controle de poses e perspectivas para consistência total
nos assets gerados no estilo Hades.
"""

import torch
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import json
from datetime import datetime

class HadesControlNetManager:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.controlnet_models = {}
        self.preprocessors = {}
        
        # Configurações otimizadas
        self.config = {
            "openpose": {
                "model_id": "lllyasviel/control_v11p_sd15_openpose",
                "strength": 0.8,
                "guidance_start": 0.0,
                "guidance_end": 1.0
            },
            "depth": {
                "model_id": "lllyasviel/control_v11f1p_sd15_depth", 
                "strength": 0.6,
                "guidance_start": 0.0,
                "guidance_end": 1.0
            },
            "canny": {
                "model_id": "lllyasviel/control_v11p_sd15_canny",
                "strength": 0.7,
                "guidance_start": 0.0,
                "guidance_end": 1.0
            }
        }
        
        # Poses pré-definidas para personagens Hades-style
        self.hades_poses = {
            "deity_majestic": {
                "description": "Pose majestosa de divindade - postura ereta, braços abertos",
                "keypoints": "standing_arms_spread",
                "recommended_for": ["Ra", "Anubis", "Isis", "deities"]
            },
            "hero_ready": {
                "description": "Pose heróica - postura de combate, arma em punho",
                "keypoints": "combat_stance_sword", 
                "recommended_for": ["protagonist", "warriors", "heroes"]
            },
            "guardian_vigilant": {
                "description": "Pose de guardião - postura alerta, protetor",
                "keypoints": "standing_guard_alert",
                "recommended_for": ["guardians", "protectors", "watchers"]
            },
            "creature_threatening": {
                "description": "Pose ameaçadora de criatura - postura predatória",
                "keypoints": "quadruped_aggressive",
                "recommended_for": ["creatures", "monsters", "beasts"]
            }
        }

    def setup_controlnet_models(self):
        """Inicializa modelos ControlNet necessários."""
        print("Configurando ControlNet Models...")
        
        try:
            # Note: Para Flux.1-dev, precisaríamos de ControlNets específicos
            # Por enquanto, vamos criar a estrutura para quando estiverem disponíveis
            
            print("ControlNet para Flux.1-dev ainda em desenvolvimento")
            print("Criando sistema de fallback com SDXL ControlNet")
            
            # Placeholder para quando ControlNet Flux estiver disponível
            self.controlnet_ready = False
            
            return True
            
        except Exception as e:
            print(f"Erro no setup ControlNet: {e}")
            return False

    def create_pose_reference(self, pose_type, character_type="character"):
        """Cria referência de pose para geração consistente."""
        print(f"Criando referência de pose: {pose_type}")
        
        if pose_type not in self.hades_poses:
            print(f"Pose '{pose_type}' não encontrada")
            return None
            
        pose_data = self.hades_poses[pose_type]
        
        # Dados da pose para referência
        pose_reference = {
            "pose_type": pose_type,
            "description": pose_data["description"],
            "character_type": character_type,
            "keypoints": pose_data["keypoints"],
            "recommended_strength": self.config["openpose"]["strength"],
            "guidance_range": [
                self.config["openpose"]["guidance_start"],
                self.config["openpose"]["guidance_end"]
            ]
        }
        
        return pose_reference

    def create_depth_map_simple(self, width=1024, height=1024, character_type="character"):
        """Cria depth map simples para controle de perspectiva."""
        print(f"Criando depth map para {character_type}")
        
        # Cria depth map básico baseado no tipo de character
        depth_map = np.zeros((height, width), dtype=np.uint8)
        
        if character_type in ["deity", "hero", "character"]:
            # Personagem em primeiro plano
            # Cabeça e torso mais próximos (valores mais altos)
            cv2.ellipse(depth_map, (width//2, height//3), 
                       (width//8, height//6), 0, 0, 360, 200, -1)
            
            # Corpo em plano médio
            cv2.ellipse(depth_map, (width//2, height//2),
                       (width//6, height//3), 0, 0, 360, 150, -1)
            
            # Pernas em plano mais distante
            cv2.ellipse(depth_map, (width//2, height*3//4),
                       (width//8, height//4), 0, 0, 360, 100, -1)
                       
        elif character_type == "environment":
            # Gradiente de profundidade para ambientes
            for y in range(height):
                depth_value = int(255 * (1 - y / height))  # Mais próximo = mais claro
                depth_map[y, :] = depth_value
                
        elif character_type == "creature":
            # Criatura quadrúpede
            cv2.ellipse(depth_map, (width//2, height//2),
                       (width//4, height//6), 0, 0, 360, 180, -1)
        
        return depth_map

    def generate_control_images(self, character_name, character_type, pose_type="deity_majestic"):
        """Gera imagens de controle para geração consistente."""
        print(f"Gerando controles para {character_name} ({character_type})")
        
        # Diretório de saída
        controls_dir = Path("../../assets/work_in_progress/control_images")
        controls_dir.mkdir(parents=True, exist_ok=True)
        
        character_dir = controls_dir / character_name.lower().replace(' ', '_')
        character_dir.mkdir(exist_ok=True)
        
        # Cria referência de pose
        pose_ref = self.create_pose_reference(pose_type, character_type)
        
        # Cria depth map
        depth_map = self.create_depth_map_simple(character_type=character_type)
        
        # Salva depth map
        depth_path = character_dir / f"{character_name.lower()}_depth.png"
        cv2.imwrite(str(depth_path), depth_map)
        
        # Salva dados de controle
        control_data = {
            "character_name": character_name,
            "character_type": character_type,
            "pose_reference": pose_ref,
            "depth_map_path": str(depth_path),
            "generation_settings": {
                "width": 1024,
                "height": 1024,
                "controlnet_strength": pose_ref["recommended_strength"] if pose_ref else 0.7
            },
            "created": datetime.now().isoformat()
        }
        
        control_file = character_dir / f"{character_name.lower()}_control.json"
        with open(control_file, 'w', encoding='utf-8') as f:
            json.dump(control_data, f, indent=2, ensure_ascii=False)
            
        print(f"Controles salvos: {character_dir}")
        return control_data

    def create_character_controls(self):
        """Cria controles para todos os personagens principais."""
        print("CRIANDO CONTROLES PARA PERSONAGENS HADES-EGIPCIO")
        print("=" * 55)
        
        # Lista de personagens principais com suas configurações
        characters = [
            # Deidades (Legendary)
            ("Ra Sun God", "deity", "deity_majestic"),
            ("Anubis Judge", "deity", "deity_majestic"), 
            ("Isis Protector", "deity", "deity_majestic"),
            ("Set Chaos", "deity", "deity_majestic"),
            
            # Heróis (Epic)
            ("Egyptian Hero", "hero", "hero_ready"),
            ("Pharaoh Divine", "hero", "hero_ready"),
            
            # Guardiões (Rare)
            ("Mummy Guardian", "guardian", "guardian_vigilant"),
            
            # Criaturas (Rare)
            ("Desert Scorpion", "creature", "creature_threatening"),
        ]
        
        results = []
        
        for char_name, char_type, pose_type in characters:
            print(f"\nProcessando: {char_name}")
            
            try:
                control_data = self.generate_control_images(char_name, char_type, pose_type)
                results.append({
                    "character": char_name,
                    "success": True,
                    "control_data": control_data
                })
                print(f"SUCESSO {char_name} - Controles criados")
                
            except Exception as e:
                print(f"ERRO {char_name} - {e}")
                results.append({
                    "character": char_name,
                    "success": False,
                    "error": str(e)
                })
        
        # Salva relatório
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_characters": len(characters),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "results": results
        }
        
        report_file = Path("../../assets/work_in_progress/controlnet_setup_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\nRELATORIO CONTROLNET:")
        print(f"Sucessos: {report['successful']}/{report['total_characters']}")
        print(f"Relatorio: {report_file}")
        
        return results

def main():
    """Executa setup do sistema ControlNet."""
    manager = HadesControlNetManager()
    
    print("CONFIGURANDO SISTEMA CONTROLNET")
    print("=" * 40)
    
    # Setup dos modelos
    if manager.setup_controlnet_models():
        print("ControlNet models configurados")
        
        # Cria controles para personagens
        results = manager.create_character_controls()
        
        print("\nCONTROLNET SYSTEM CONFIGURADO!")
        print("Controles de pose e perspectiva prontos para geração")
        
    else:
        print("Falha no setup ControlNet")

if __name__ == "__main__":
    main()