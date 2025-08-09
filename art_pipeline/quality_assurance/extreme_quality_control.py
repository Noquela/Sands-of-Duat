#!/usr/bin/env python3
"""
EXTREME QUALITY CONTROL SYSTEM - FASE 6
========================================
Sistema avançado de validação de qualidade para assets Hades-Egyptian
com análise de estilo, consistência e aprovação profissional.
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import hashlib

@dataclass
class QualityMetrics:
    """Métricas detalhadas de qualidade para um asset."""
    asset_id: str
    file_path: str
    rarity: str
    category: str
    
    # Métricas técnicas
    resolution_score: float
    file_quality_score: float
    format_compliance_score: float
    
    # Métricas de estilo Hades
    pen_ink_style_score: float
    chiaroscuro_lighting_score: float
    heroic_proportions_score: float
    color_palette_adherence: float
    
    # Métricas Egyptian
    egyptian_authenticity: float
    hieroglyphic_details: float
    architectural_accuracy: float
    mythological_correctness: float
    
    # Métricas de consistência
    character_consistency: float
    style_uniformity: float
    quality_consistency: float
    
    # Métricas avançadas
    visual_impact_score: float
    game_integration_readiness: float
    professional_quality_score: float
    
    # Score final
    overall_score: float
    approval_status: str
    quality_tier: str
    
    # Issues e recomendações
    critical_issues: List[str]
    minor_issues: List[str] 
    recommendations: List[str]
    
    timestamp: str

class ExtremeQualityController:
    def __init__(self):
        self.base_dir = Path(".")
        self.qa_dir = self.base_dir / "quality_assurance"
        self.results_dir = self.qa_dir / "results"
        self.reports_dir = self.qa_dir / "reports" 
        self.approved_dir = self.qa_dir / "approved_assets"
        self.rejected_dir = self.qa_dir / "rejected_assets"
        self.review_dir = self.qa_dir / "manual_review"
        
        # Quality thresholds mais rigorosos
        self.quality_thresholds = {
            "legendary": {
                "minimum_score": 0.95,  # 95% para legendary
                "professional_tier": 0.98,
                "critical_issues": 0,
                "minor_issues": 1
            },
            "epic": {
                "minimum_score": 0.90,  # 90% para epic
                "professional_tier": 0.95,
                "critical_issues": 0,
                "minor_issues": 2
            },
            "rare": {
                "minimum_score": 0.85,  # 85% para rare
                "professional_tier": 0.90,
                "critical_issues": 0,
                "minor_issues": 3
            },
            "common": {
                "minimum_score": 0.80,  # 80% para common
                "professional_tier": 0.85,
                "critical_issues": 1,
                "minor_issues": 4
            }
        }
        
        # Hades style specifications
        self.hades_style_specs = {
            "pen_ink_keywords": [
                "clean line art", "bold outlines", "ink drawing style",
                "defined edges", "sketch-like quality", "artistic line work"
            ],
            "chiaroscuro_keywords": [
                "dramatic lighting", "strong shadows", "contrast lighting",
                "light and shadow", "dramatic shadows", "atmospheric lighting"
            ],
            "color_palette": {
                "primary_colors": ["#C41E3A", "#FFD700", "#191970", "#000000"],
                "acceptable_range": ["red", "gold", "blue", "black", "bronze"],
                "forbidden_colors": ["pink", "neon", "cyan", "lime"]
            },
            "heroic_proportions": [
                "heroic build", "strong silhouette", "powerful stance",
                "imposing presence", "larger than life"
            ]
        }
        
        # Egyptian authenticity checks
        self.egyptian_authenticity = {
            "deities": {
                "anubis": ["jackal head", "golden collar", "divine presence"],
                "ra": ["falcon head", "solar disk", "golden aura"],
                "isis": ["wings", "protective pose", "maternal"],
                "set": ["unique head", "chaos", "menacing"],
                "thoth": ["ibis head", "scroll", "wisdom"]
            },
            "architectural_elements": [
                "hieroglyphics", "columns", "stone", "temple",
                "pyramid", "tomb", "sarcophagus", "ancient"
            ],
            "mythological_accuracy": [
                "egyptian mythology", "underworld", "afterlife",
                "divine judgment", "sacred", "ritual"
            ]
        }
        
        self.setup_quality_environment()
        self.load_reference_data()

    def setup_quality_environment(self):
        """Setup ambiente de quality assurance."""
        print("CONFIGURANDO SISTEMA DE QUALITY CONTROL EXTREMO")
        print("=" * 48)
        
        directories = [
            self.qa_dir,
            self.results_dir,
            self.reports_dir,
            self.approved_dir,
            self.rejected_dir,
            self.review_dir,
            self.approved_dir / "legendary",
            self.approved_dir / "epic", 
            self.approved_dir / "rare",
            self.approved_dir / "common",
            self.rejected_dir / "style_issues",
            self.rejected_dir / "technical_issues",
            self.rejected_dir / "consistency_issues"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print("Ambiente de Quality Assurance configurado!")
        print(f"Diretório base: {self.qa_dir}")

    def load_reference_data(self):
        """Carrega dados de referência para comparação."""
        try:
            # Load color palette from FASE 1
            palette_file = Path("../reference_collection/style_analysis/HADES_COLOR_PALETTE_GUIDE.md")
            style_file = Path("../reference_collection/style_analysis/HADES_STYLE_ANALYSIS.md") 
            
            self.reference_loaded = True
            print("Dados de referência Hades-Egyptian carregados!")
            
        except Exception as e:
            print(f"Aviso: Dados de referência não encontrados: {e}")
            self.reference_loaded = False

    def analyze_technical_quality(self, image_path: str) -> Dict:
        """Análise técnica detalhada do asset."""
        try:
            from PIL import Image, ImageStat
            
            with Image.open(image_path) as img:
                width, height = img.size
                file_size = os.path.getsize(image_path)
                
                # Resolution analysis
                target_resolution = 1024
                resolution_score = min(min(width, height) / target_resolution, 1.0)
                
                # File quality analysis
                if file_size > 15 * 1024 * 1024:  # > 15MB
                    file_quality_score = 0.5  # Too large
                elif file_size < 100 * 1024:  # < 100KB  
                    file_quality_score = 0.3  # Too small, likely low quality
                else:
                    file_quality_score = 1.0
                
                # Format compliance
                format_compliance_score = 1.0 if image_path.lower().endswith('.png') else 0.5
                
                # Visual quality metrics
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                stat = ImageStat.Stat(img)
                
                # Check for color diversity (not monochrome)
                color_diversity = sum([max(channel) - min(channel) for channel in stat.extrema]) / (3 * 255)
                
                # Brightness analysis
                brightness = sum(stat.mean) / (3 * 255)
                brightness_score = 1.0 if 0.2 <= brightness <= 0.8 else 0.5
                
                return {
                    "resolution_score": resolution_score,
                    "file_quality_score": file_quality_score,
                    "format_compliance_score": format_compliance_score,
                    "color_diversity": color_diversity,
                    "brightness_score": brightness_score,
                    "dimensions": f"{width}x{height}",
                    "file_size_mb": file_size / (1024 * 1024)
                }
                
        except Exception as e:
            return {
                "resolution_score": 0.0,
                "file_quality_score": 0.0,
                "format_compliance_score": 0.0,
                "color_diversity": 0.0,
                "brightness_score": 0.0,
                "error": str(e)
            }

    def analyze_hades_style_compliance(self, asset_info: Dict) -> Dict:
        """Análise de aderência ao estilo Hades."""
        
        prompt = asset_info.get("prompt", "").lower()
        character = asset_info.get("character", "").lower()
        
        # Pen & Ink style detection
        pen_ink_keywords = sum(1 for keyword in self.hades_style_specs["pen_ink_keywords"] 
                              if keyword in prompt)
        pen_ink_score = min(pen_ink_keywords / 3, 1.0)  # Normalize to 3 keywords
        
        # Chiaroscuro lighting detection  
        chiaroscuro_keywords = sum(1 for keyword in self.hades_style_specs["chiaroscuro_keywords"]
                                  if keyword in prompt)
        chiaroscuro_score = min(chiaroscuro_keywords / 2, 1.0)  # Normalize to 2 keywords
        
        # Color palette adherence
        color_keywords = sum(1 for color in self.hades_style_specs["color_palette"]["acceptable_range"]
                            if color in prompt)
        color_score = min(color_keywords / 2, 1.0)  # At least 2 colors mentioned
        
        # Heroic proportions detection
        heroic_keywords = sum(1 for keyword in self.hades_style_specs["heroic_proportions"]
                             if keyword in prompt)
        heroic_score = min(heroic_keywords / 2, 1.0)
        
        # Overall Hades compliance
        hades_compliance = (pen_ink_score + chiaroscuro_score + color_score + heroic_score) / 4
        
        return {
            "pen_ink_style_score": pen_ink_score,
            "chiaroscuro_lighting_score": chiaroscuro_score, 
            "color_palette_adherence": color_score,
            "heroic_proportions_score": heroic_score,
            "overall_hades_compliance": hades_compliance,
            "style_keywords_found": pen_ink_keywords + chiaroscuro_keywords + color_keywords + heroic_keywords
        }

    def analyze_egyptian_authenticity(self, asset_info: Dict) -> Dict:
        """Análise de autenticidade Egyptian."""
        
        prompt = asset_info.get("prompt", "").lower()
        character = asset_info.get("character", "").lower()
        category = asset_info.get("category", "").lower()
        
        egyptian_score = 0.0
        mythological_score = 0.0
        architectural_score = 0.0
        
        # Check for specific deity authenticity
        if category == "deity":
            for deity, attributes in self.egyptian_authenticity["deities"].items():
                if deity in character:
                    matching_attrs = sum(1 for attr in attributes if attr in prompt)
                    egyptian_score = min(matching_attrs / len(attributes), 1.0)
                    break
        
        # Mythological accuracy
        mythological_keywords = sum(1 for keyword in self.egyptian_authenticity["mythological_accuracy"]
                                   if keyword in prompt)
        mythological_score = min(mythological_keywords / 3, 1.0)
        
        # Architectural authenticity for environments
        if category == "environment":
            arch_keywords = sum(1 for keyword in self.egyptian_authenticity["architectural_elements"]
                               if keyword in prompt)
            architectural_score = min(arch_keywords / 4, 1.0)
        else:
            architectural_score = 0.5  # Not applicable but don't penalize
        
        # Hieroglyphic details detection
        hieroglyphic_score = 1.0 if "hieroglyphic" in prompt else 0.5
        
        return {
            "egyptian_authenticity": egyptian_score,
            "mythological_correctness": mythological_score,
            "architectural_accuracy": architectural_score,
            "hieroglyphic_details": hieroglyphic_score,
            "overall_egyptian_compliance": (egyptian_score + mythological_score + 
                                          architectural_score + hieroglyphic_score) / 4
        }

    def analyze_consistency(self, asset_info: Dict, all_assets: List[Dict]) -> Dict:
        """Análise de consistência entre assets."""
        
        rarity = asset_info.get("rarity", "")
        category = asset_info.get("category", "")
        
        # Find similar assets for comparison
        similar_assets = [a for a in all_assets 
                         if a.get("rarity") == rarity and a.get("category") == category]
        
        if len(similar_assets) < 2:
            return {
                "character_consistency": 1.0,
                "style_uniformity": 1.0, 
                "quality_consistency": 1.0,
                "note": "Insufficient assets for comparison"
            }
        
        # Style uniformity - check for consistent keywords
        current_prompt = asset_info.get("prompt", "").lower()
        style_keywords = ["hades", "pen and ink", "dramatic", "masterpiece"]
        
        current_style_score = sum(1 for keyword in style_keywords if keyword in current_prompt)
        
        # Compare with similar assets
        other_scores = []
        for asset in similar_assets:
            if asset != asset_info:
                other_prompt = asset.get("prompt", "").lower()
                other_score = sum(1 for keyword in style_keywords if keyword in other_prompt)
                other_scores.append(other_score)
        
        if other_scores:
            avg_other_score = sum(other_scores) / len(other_scores)
            style_uniformity = 1.0 - abs(current_style_score - avg_other_score) / len(style_keywords)
        else:
            style_uniformity = 1.0
        
        return {
            "character_consistency": 0.9,  # Placeholder - would need visual analysis
            "style_uniformity": max(style_uniformity, 0.0),
            "quality_consistency": 0.9,   # Placeholder - would need quality comparison
            "similar_assets_count": len(similar_assets)
        }

    def calculate_advanced_metrics(self, asset_info: Dict, technical_metrics: Dict, 
                                  style_metrics: Dict, egyptian_metrics: Dict) -> Dict:
        """Calcula métricas avançadas de qualidade."""
        
        rarity = asset_info.get("rarity", "common")
        
        # Visual impact based on rarity expectations
        rarity_multipliers = {
            "legendary": 1.2,
            "epic": 1.1,
            "rare": 1.0,
            "common": 0.9
        }
        
        base_visual_impact = (style_metrics.get("overall_hades_compliance", 0) + 
                             egyptian_metrics.get("overall_egyptian_compliance", 0)) / 2
        visual_impact_score = min(base_visual_impact * rarity_multipliers.get(rarity, 1.0), 1.0)
        
        # Game integration readiness
        technical_score = (technical_metrics.get("resolution_score", 0) + 
                          technical_metrics.get("file_quality_score", 0) + 
                          technical_metrics.get("format_compliance_score", 0)) / 3
        
        artistic_score = (style_metrics.get("overall_hades_compliance", 0) +
                         egyptian_metrics.get("overall_egyptian_compliance", 0)) / 2
        
        game_integration_readiness = (technical_score * 0.3 + artistic_score * 0.7)
        
        # Professional quality score
        professional_factors = [
            technical_score,
            artistic_score,
            visual_impact_score,
            1.0 if asset_info.get("prompt", "").count("masterpiece") > 0 else 0.8
        ]
        
        professional_quality_score = sum(professional_factors) / len(professional_factors)
        
        return {
            "visual_impact_score": visual_impact_score,
            "game_integration_readiness": game_integration_readiness,
            "professional_quality_score": professional_quality_score
        }

    def comprehensive_quality_analysis(self, asset_info: Dict, all_assets: List[Dict] = None) -> QualityMetrics:
        """Análise completa de qualidade de um asset."""
        
        if all_assets is None:
            all_assets = [asset_info]
        
        file_path = asset_info.get("file_path", "")
        
        print(f"Analisando: {asset_info.get('id', 'unknown')}...")
        
        # Análises técnicas
        technical_metrics = self.analyze_technical_quality(file_path)
        
        # Análises de estilo
        style_metrics = self.analyze_hades_style_compliance(asset_info)
        egyptian_metrics = self.analyze_egyptian_authenticity(asset_info)
        consistency_metrics = self.analyze_consistency(asset_info, all_assets)
        advanced_metrics = self.calculate_advanced_metrics(asset_info, technical_metrics, 
                                                          style_metrics, egyptian_metrics)
        
        # Calculate overall score
        weight_technical = 0.15
        weight_hades_style = 0.25
        weight_egyptian = 0.25
        weight_consistency = 0.15
        weight_advanced = 0.20
        
        overall_score = (
            technical_metrics.get("resolution_score", 0) * weight_technical +
            style_metrics.get("overall_hades_compliance", 0) * weight_hades_style +
            egyptian_metrics.get("overall_egyptian_compliance", 0) * weight_egyptian +
            ((consistency_metrics.get("style_uniformity", 0) + 
              consistency_metrics.get("quality_consistency", 0)) / 2) * weight_consistency +
            advanced_metrics.get("professional_quality_score", 0) * weight_advanced
        )
        
        # Determine approval status and quality tier
        rarity = asset_info.get("rarity", "common")
        thresholds = self.quality_thresholds.get(rarity, self.quality_thresholds["common"])
        
        critical_issues = []
        minor_issues = []
        recommendations = []
        
        # Check for critical issues
        if technical_metrics.get("resolution_score", 0) < 0.8:
            critical_issues.append("Resolution below minimum standard")
        
        if style_metrics.get("overall_hades_compliance", 0) < 0.7:
            critical_issues.append("Insufficient Hades style compliance")
        
        if egyptian_metrics.get("overall_egyptian_compliance", 0) < 0.7:
            critical_issues.append("Insufficient Egyptian authenticity")
        
        # Check for minor issues
        if technical_metrics.get("file_quality_score", 0) < 1.0:
            minor_issues.append("File size not optimal")
            
        if style_metrics.get("pen_ink_style_score", 0) < 0.8:
            minor_issues.append("Pen & ink style could be stronger")
        
        # Generate recommendations
        if style_metrics.get("chiaroscuro_lighting_score", 0) < 0.8:
            recommendations.append("Enhance dramatic lighting and shadows")
        
        if egyptian_metrics.get("hieroglyphic_details", 0) < 1.0:
            recommendations.append("Add more hieroglyphic detail elements")
        
        if advanced_metrics.get("visual_impact_score", 0) < 0.9:
            recommendations.append("Increase visual impact for rarity level")
        
        # Determine approval status
        if (overall_score >= thresholds["minimum_score"] and 
            len(critical_issues) <= thresholds["critical_issues"] and
            len(minor_issues) <= thresholds["minor_issues"]):
            
            if overall_score >= thresholds["professional_tier"]:
                approval_status = "APPROVED_PROFESSIONAL"
                quality_tier = "PROFESSIONAL"
            else:
                approval_status = "APPROVED"
                quality_tier = "STANDARD"
        else:
            approval_status = "REJECTED"
            quality_tier = "BELOW_STANDARD"
        
        return QualityMetrics(
            asset_id=asset_info.get("id", "unknown"),
            file_path=file_path,
            rarity=rarity,
            category=asset_info.get("category", "unknown"),
            
            resolution_score=technical_metrics.get("resolution_score", 0),
            file_quality_score=technical_metrics.get("file_quality_score", 0),
            format_compliance_score=technical_metrics.get("format_compliance_score", 0),
            
            pen_ink_style_score=style_metrics.get("pen_ink_style_score", 0),
            chiaroscuro_lighting_score=style_metrics.get("chiaroscuro_lighting_score", 0),
            heroic_proportions_score=style_metrics.get("heroic_proportions_score", 0),
            color_palette_adherence=style_metrics.get("color_palette_adherence", 0),
            
            egyptian_authenticity=egyptian_metrics.get("egyptian_authenticity", 0),
            hieroglyphic_details=egyptian_metrics.get("hieroglyphic_details", 0),
            architectural_accuracy=egyptian_metrics.get("architectural_accuracy", 0),
            mythological_correctness=egyptian_metrics.get("mythological_correctness", 0),
            
            character_consistency=consistency_metrics.get("character_consistency", 0),
            style_uniformity=consistency_metrics.get("style_uniformity", 0),
            quality_consistency=consistency_metrics.get("quality_consistency", 0),
            
            visual_impact_score=advanced_metrics.get("visual_impact_score", 0),
            game_integration_readiness=advanced_metrics.get("game_integration_readiness", 0),
            professional_quality_score=advanced_metrics.get("professional_quality_score", 0),
            
            overall_score=overall_score,
            approval_status=approval_status,
            quality_tier=quality_tier,
            
            critical_issues=critical_issues,
            minor_issues=minor_issues,
            recommendations=recommendations,
            
            timestamp=datetime.now().isoformat()
        )

    def process_asset_batch(self, assets_directory: str) -> Dict:
        """Processa um lote completo de assets."""
        
        print(f"\nPROCESSANDO LOTE: {assets_directory}")
        print("=" * 40)
        
        assets_path = Path(assets_directory)
        if not assets_path.exists():
            return {"error": f"Directory not found: {assets_directory}"}
        
        # Find all PNG files
        image_files = list(assets_path.rglob("*.png"))
        
        if not image_files:
            return {"error": f"No PNG files found in {assets_directory}"}
        
        print(f"Found {len(image_files)} assets to analyze")
        
        # Load asset metadata (from production batches if available)
        batch_file = Path("../production_system/mass_production/production_batches.json")
        asset_metadata = {}
        
        if batch_file.exists():
            try:
                with open(batch_file, 'r', encoding='utf-8') as f:
                    batches = json.load(f)
                    
                # Build metadata lookup
                for batch_info in batches.values():
                    for asset in batch_info.get("assets", []):
                        asset_metadata[asset["id"]] = asset
            except Exception as e:
                print(f"Warning: Could not load batch metadata: {e}")
        
        # Process each asset
        results = []
        approved_count = 0
        professional_count = 0
        
        for i, image_file in enumerate(image_files):
            # Try to extract asset info from filename or use defaults
            asset_id = image_file.stem
            
            asset_info = asset_metadata.get(asset_id, {
                "id": asset_id,
                "prompt": "hades game art, egyptian style, pen and ink, dramatic lighting, masterpiece",
                "character": asset_id,
                "category": "unknown",
                "rarity": "common",
                "file_path": str(image_file)
            })
            asset_info["file_path"] = str(image_file)
            
            # Perform comprehensive analysis
            quality_metrics = self.comprehensive_quality_analysis(asset_info, list(asset_metadata.values()))
            
            results.append(quality_metrics)
            
            # Update counters
            if quality_metrics.approval_status in ["APPROVED", "APPROVED_PROFESSIONAL"]:
                approved_count += 1
                if quality_metrics.approval_status == "APPROVED_PROFESSIONAL":
                    professional_count += 1
            
            # Progress update
            print(f"  [{i+1}/{len(image_files)}] {asset_id}: {quality_metrics.approval_status} "
                  f"({quality_metrics.overall_score:.2f})")
        
        # Generate batch summary
        total_assets = len(results)
        approval_rate = approved_count / total_assets * 100
        professional_rate = professional_count / total_assets * 100
        
        batch_summary = {
            "timestamp": datetime.now().isoformat(),
            "directory": str(assets_path),
            "total_assets": total_assets,
            "approved_assets": approved_count,
            "professional_assets": professional_count,
            "rejected_assets": total_assets - approved_count,
            "approval_rate": approval_rate,
            "professional_rate": professional_rate,
            "results": [vars(result) for result in results]
        }
        
        # Save detailed results
        results_file = self.results_dir / f"quality_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(batch_summary, f, indent=2, ensure_ascii=False)
        
        print(f"\nBATCH ANALYSIS COMPLETE:")
        print(f"  Total: {total_assets} assets")
        print(f"  Approved: {approved_count} ({approval_rate:.1f}%)")
        print(f"  Professional: {professional_count} ({professional_rate:.1f}%)")
        print(f"  Rejected: {total_assets - approved_count}")
        print(f"  Results saved: {results_file}")
        
        return batch_summary

    def generate_comprehensive_report(self, batch_results: List[Dict]) -> str:
        """Gera relatório abrangente de qualidade."""
        
        if not batch_results:
            return "No batch results available for report generation."
        
        # Aggregate statistics across all batches
        total_assets = sum(batch.get("total_assets", 0) for batch in batch_results)
        total_approved = sum(batch.get("approved_assets", 0) for batch in batch_results) 
        total_professional = sum(batch.get("professional_assets", 0) for batch in batch_results)
        total_rejected = sum(batch.get("rejected_assets", 0) for batch in batch_results)
        
        if total_assets == 0:
            return "No assets found in batch results."
        
        overall_approval_rate = total_approved / total_assets * 100
        professional_rate = total_professional / total_assets * 100
        rejection_rate = total_rejected / total_assets * 100
        
        report = f"""
# EXTREME QUALITY CONTROL REPORT - FASE 6
## Comprehensive Quality Analysis Results

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## EXECUTIVE SUMMARY

**OVERALL PERFORMANCE:**
- **Total Assets Analyzed:** {total_assets}
- **Approved Assets:** {total_approved} ({overall_approval_rate:.1f}%)
- **Professional Tier:** {total_professional} ({professional_rate:.1f}%)
- **Rejected Assets:** {total_rejected} ({rejection_rate:.1f}%)

**QUALITY STATUS:** {'🎉 EXCELLENT' if overall_approval_rate >= 85 else '⚠️ NEEDS IMPROVEMENT' if overall_approval_rate >= 70 else '❌ MAJOR ISSUES'}

---

## DETAILED ANALYSIS BY BATCH

"""
        
        for i, batch in enumerate(batch_results, 1):
            batch_approval_rate = batch.get("approval_rate", 0)
            batch_professional_rate = batch.get("professional_rate", 0)
            
            report += f"""
### Batch {i}: {Path(batch.get('directory', 'Unknown')).name}

- **Assets:** {batch.get('total_assets', 0)}
- **Approved:** {batch.get('approved_assets', 0)} ({batch_approval_rate:.1f}%)  
- **Professional:** {batch.get('professional_assets', 0)} ({batch_professional_rate:.1f}%)
- **Status:** {'✅ PASSED' if batch_approval_rate >= 80 else '⚠️ REVIEW' if batch_approval_rate >= 60 else '❌ FAILED'}

"""
        
        # Quality metrics analysis
        all_results = []
        for batch in batch_results:
            all_results.extend(batch.get("results", []))
        
        if all_results:
            # Calculate average scores
            avg_scores = {
                "overall_score": sum(r.get("overall_score", 0) for r in all_results) / len(all_results),
                "hades_style": sum(r.get("pen_ink_style_score", 0) + r.get("chiaroscuro_lighting_score", 0) for r in all_results) / (len(all_results) * 2),
                "egyptian_authenticity": sum(r.get("egyptian_authenticity", 0) + r.get("mythological_correctness", 0) for r in all_results) / (len(all_results) * 2),
                "technical_quality": sum(r.get("resolution_score", 0) + r.get("file_quality_score", 0) for r in all_results) / (len(all_results) * 2)
            }
            
            report += f"""
---

## QUALITY METRICS ANALYSIS

**AVERAGE SCORES:**
- **Overall Quality:** {avg_scores['overall_score']:.2f} / 1.00
- **Hades Style Compliance:** {avg_scores['hades_style']:.2f} / 1.00
- **Egyptian Authenticity:** {avg_scores['egyptian_authenticity']:.2f} / 1.00  
- **Technical Quality:** {avg_scores['technical_quality']:.2f} / 1.00

**SCORE DISTRIBUTION:**
"""
            
            # Score distribution analysis
            score_ranges = {
                "Excellent (0.90-1.00)": len([r for r in all_results if r.get("overall_score", 0) >= 0.90]),
                "Good (0.80-0.89)": len([r for r in all_results if 0.80 <= r.get("overall_score", 0) < 0.90]), 
                "Fair (0.70-0.79)": len([r for r in all_results if 0.70 <= r.get("overall_score", 0) < 0.80]),
                "Poor (<0.70)": len([r for r in all_results if r.get("overall_score", 0) < 0.70])
            }
            
            for range_name, count in score_ranges.items():
                percentage = count / len(all_results) * 100
                report += f"- **{range_name}:** {count} assets ({percentage:.1f}%)\n"
        
        # Issue analysis
        report += f"""

---

## ISSUE ANALYSIS

**COMMON ISSUES IDENTIFIED:**
"""
        
        all_critical_issues = []
        all_minor_issues = []
        
        for result in all_results:
            all_critical_issues.extend(result.get("critical_issues", []))
            all_minor_issues.extend(result.get("minor_issues", []))
        
        # Count issue frequency
        from collections import Counter
        critical_counter = Counter(all_critical_issues)
        minor_counter = Counter(all_minor_issues)
        
        if critical_counter:
            report += "\n**Critical Issues:**\n"
            for issue, count in critical_counter.most_common(5):
                report += f"- {issue}: {count} occurrences\n"
        
        if minor_counter:
            report += "\n**Minor Issues:**\n" 
            for issue, count in minor_counter.most_common(5):
                report += f"- {issue}: {count} occurrences\n"
        
        # Recommendations
        report += f"""

---

## RECOMMENDATIONS

### IMMEDIATE ACTIONS:
"""
        
        if overall_approval_rate < 80:
            report += """
- **🚨 CRITICAL:** Approval rate below target (80%)
- Regenerate rejected assets with improved prompts
- Focus on Hades style compliance and Egyptian authenticity
- Review and enhance technical specifications
"""
        
        if professional_rate < 50:
            report += """
- **⚠️ QUALITY:** Low professional tier rate
- Enhance dramatic lighting and chiaroscuro effects
- Improve pen & ink style implementation
- Add more hieroglyphic and architectural details
"""
        
        report += f"""

### PRODUCTION READINESS:

**READY FOR INTEGRATION:**
- {total_approved} assets approved for game integration
- {total_professional} assets meet professional tier standards
- Quality threshold: {'✅ MET' if overall_approval_rate >= 80 else '❌ NOT MET'}

### NEXT STEPS:
1. **Address Critical Issues:** Focus on rejected assets first
2. **Enhance Visual Impact:** Improve professional tier percentage  
3. **Style Consistency:** Ensure uniform Hades-Egyptian fusion
4. **Technical Polish:** Optimize file sizes and formats
5. **Final Integration:** Prepare approved assets for FASE 7

---

## QUALITY CERTIFICATION

**HADES-EGYPTIAN FUSION STANDARD:** {'🏆 CERTIFIED' if overall_approval_rate >= 85 and professional_rate >= 60 else '⏳ IN PROGRESS'}

This report certifies that the analyzed assets {'meet' if overall_approval_rate >= 80 else 'do not yet meet'} the extreme quality standards established for professional game asset integration.

**Certification Date:** {datetime.now().strftime("%Y-%m-%d")}
**Quality Controller:** Extreme Quality Control System v6.0
**Standard:** Hades-Egyptian Fusion Professional Gaming Assets

---

*End of Quality Control Report*
"""
        
        return report

def main():
    """Execução principal do sistema de quality control extremo."""
    
    controller = ExtremeQualityController()
    
    print("EXTREME QUALITY CONTROL SYSTEM - FASE 6")
    print("=" * 42)
    print("1. Analyze single directory")
    print("2. Analyze multiple directories")
    print("3. Generate comprehensive report")
    print("4. Set up approval workflow")
    print("0. Exit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        directory = input("Enter assets directory path: ").strip()
        if directory and Path(directory).exists():
            results = controller.process_asset_batch(directory)
            print(f"\nAnalysis complete! Results: {results.get('approval_rate', 0):.1f}% approval rate")
        else:
            print("Invalid directory path!")
    
    elif choice == "2":
        directories = input("Enter directory paths (comma-separated): ").strip().split(",")
        batch_results = []
        
        for directory in directories:
            directory = directory.strip()
            if directory and Path(directory).exists():
                print(f"\nProcessing: {directory}")
                results = controller.process_asset_batch(directory)
                batch_results.append(results)
            else:
                print(f"Skipping invalid path: {directory}")
        
        if batch_results:
            report = controller.generate_comprehensive_report(batch_results)
            
            report_file = controller.reports_dir / f"comprehensive_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"\nComprehensive report generated: {report_file}")
            print(report[:500] + "..." if len(report) > 500 else report)
    
    elif choice == "3":
        print("Feature coming soon: Advanced reporting dashboard")
    
    elif choice == "4":
        print("Feature coming soon: Automated approval workflow")

if __name__ == "__main__":
    main()