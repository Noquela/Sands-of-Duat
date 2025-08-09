#!/usr/bin/env python3
"""
AUTOMATED APPROVAL SYSTEM - FASE 6
===================================
Sistema automatizado de aprovação com workflow inteligente
para organizar assets por qualidade e preparar para produção.
"""

import json
import shutil
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import logging

class AutomatedApprovalSystem:
    def __init__(self):
        self.base_dir = Path(".")
        self.qa_dir = self.base_dir / "quality_assurance"
        
        # Approval workflow directories
        self.workflow_dir = self.qa_dir / "approval_workflow"
        self.approved_dir = self.workflow_dir / "approved"
        self.rejected_dir = self.workflow_dir / "rejected" 
        self.review_dir = self.workflow_dir / "manual_review"
        self.production_ready = self.workflow_dir / "production_ready"
        
        # Organization by quality tier
        self.tier_dirs = {
            "PROFESSIONAL": self.approved_dir / "professional_tier",
            "STANDARD": self.approved_dir / "standard_tier", 
            "REVIEW": self.review_dir / "needs_improvement",
            "REJECTED": self.rejected_dir / "quality_issues"
        }
        
        # Organization by rarity
        self.rarity_dirs = {
            "legendary": self.production_ready / "legendary_assets",
            "epic": self.production_ready / "epic_assets",
            "rare": self.production_ready / "rare_assets", 
            "common": self.production_ready / "common_assets"
        }
        
        self.setup_approval_environment()
        self.setup_logging()

    def setup_approval_environment(self):
        """Configura ambiente de aprovação automatizada."""
        print("CONFIGURANDO SISTEMA DE APROVACAO AUTOMATIZADA")
        print("=" * 46)
        
        # Create all necessary directories
        directories = [
            self.workflow_dir,
            self.approved_dir,
            self.rejected_dir, 
            self.review_dir,
            self.production_ready
        ]
        
        # Add tier directories
        directories.extend(self.tier_dirs.values())
        
        # Add rarity directories
        directories.extend(self.rarity_dirs.values())
        
        # Additional organization directories
        additional_dirs = [
            self.rejected_dir / "style_issues",
            self.rejected_dir / "technical_issues", 
            self.rejected_dir / "consistency_issues",
            self.review_dir / "minor_fixes_needed",
            self.review_dir / "style_enhancement",
            self.production_ready / "final_integration",
            self.production_ready / "game_ready_assets"
        ]
        
        directories.extend(additional_dirs)
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print("Ambiente de aprovação configurado!")
        print(f"Diretório workflow: {self.workflow_dir}")

    def setup_logging(self):
        """Configura sistema de logging para auditoria."""
        log_dir = self.workflow_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"approval_log_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)

    def process_quality_results(self, results_file: str) -> Dict:
        """Processa resultados de quality control e executa aprovação automatizada."""
        
        if not Path(results_file).exists():
            self.logger.error(f"Results file not found: {results_file}")
            return {"error": "Results file not found"}
        
        self.logger.info(f"Processing quality results: {results_file}")
        
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                batch_data = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load results file: {e}")
            return {"error": f"Failed to load results: {e}"}
        
        results = batch_data.get("results", [])
        if not results:
            self.logger.warning("No results found in batch data")
            return {"warning": "No results to process"}
        
        # Process each asset
        approval_summary = {
            "processed": 0,
            "approved_professional": 0,
            "approved_standard": 0,
            "needs_review": 0,
            "rejected": 0,
            "moved_files": [],
            "errors": []
        }
        
        for result in results:
            try:
                approval_decision = self.make_approval_decision(result)
                file_moved = self.organize_asset(result, approval_decision)
                
                if file_moved:
                    approval_summary["moved_files"].append({
                        "asset_id": result.get("asset_id", "unknown"),
                        "decision": approval_decision["status"],
                        "destination": str(approval_decision["destination"])
                    })
                
                # Update counters
                approval_summary["processed"] += 1
                status_key = approval_decision["status"].lower().replace(" ", "_")
                if status_key in approval_summary:
                    approval_summary[status_key] += 1
                
            except Exception as e:
                error_msg = f"Error processing {result.get('asset_id', 'unknown')}: {e}"
                self.logger.error(error_msg)
                approval_summary["errors"].append(error_msg)
        
        # Generate approval report
        self.generate_approval_report(approval_summary, batch_data)
        
        self.logger.info(f"Approval processing complete: {approval_summary['processed']} assets")
        return approval_summary

    def make_approval_decision(self, quality_result: Dict) -> Dict:
        """Toma decisão automática de aprovação baseada nos resultados de qualidade."""
        
        asset_id = quality_result.get("asset_id", "unknown")
        overall_score = quality_result.get("overall_score", 0.0)
        approval_status = quality_result.get("approval_status", "REJECTED")
        quality_tier = quality_result.get("quality_tier", "BELOW_STANDARD")
        critical_issues = quality_result.get("critical_issues", [])
        minor_issues = quality_result.get("minor_issues", [])
        rarity = quality_result.get("rarity", "common")
        
        # Decision logic based on comprehensive criteria
        if approval_status == "APPROVED_PROFESSIONAL":
            decision = {
                "status": "APPROVED_PROFESSIONAL",
                "destination": self.tier_dirs["PROFESSIONAL"],
                "reason": f"Professional quality achieved (score: {overall_score:.2f})",
                "next_step": "production_ready",
                "priority": "high"
            }
        
        elif approval_status == "APPROVED":
            decision = {
                "status": "APPROVED_STANDARD", 
                "destination": self.tier_dirs["STANDARD"],
                "reason": f"Standard quality met (score: {overall_score:.2f})",
                "next_step": "production_ready",
                "priority": "medium"
            }
        
        elif (overall_score >= 0.70 and len(critical_issues) == 0 and 
              len(minor_issues) <= 3):
            decision = {
                "status": "NEEDS_REVIEW",
                "destination": self.tier_dirs["REVIEW"],
                "reason": f"Minor improvements needed (score: {overall_score:.2f})",
                "next_step": "enhancement",
                "priority": "medium",
                "issues": minor_issues
            }
        
        else:
            # Determine rejection reason
            if critical_issues:
                rejection_reason = f"Critical issues: {', '.join(critical_issues[:2])}"
                sub_dir = "style_issues" if any("style" in issue.lower() for issue in critical_issues) else "technical_issues"
            else:
                rejection_reason = f"Quality score too low: {overall_score:.2f}"
                sub_dir = "quality_issues"
            
            decision = {
                "status": "REJECTED",
                "destination": self.rejected_dir / sub_dir,
                "reason": rejection_reason,
                "next_step": "regeneration",
                "priority": "low",
                "issues": critical_issues + minor_issues
            }
        
        self.logger.info(f"Decision for {asset_id}: {decision['status']} - {decision['reason']}")
        return decision

    def organize_asset(self, quality_result: Dict, approval_decision: Dict) -> bool:
        """Organiza asset no sistema de arquivos baseado na decisão de aprovação."""
        
        source_file = Path(quality_result.get("file_path", ""))
        asset_id = quality_result.get("asset_id", "unknown")
        rarity = quality_result.get("rarity", "common")
        
        if not source_file.exists():
            self.logger.warning(f"Source file not found: {source_file}")
            return False
        
        # Determine destination directory
        destination_dir = approval_decision["destination"]
        destination_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate organized filename
        status = approval_decision["status"]
        timestamp = datetime.now().strftime("%Y%m%d")
        
        if status in ["APPROVED_PROFESSIONAL", "APPROVED_STANDARD"]:
            # For approved assets, organize by rarity in production_ready
            production_dir = self.rarity_dirs[rarity]
            production_dir.mkdir(parents=True, exist_ok=True)
            
            final_filename = f"{asset_id}_{rarity}_{status.lower()}.png"
            final_destination = production_dir / final_filename
            
            # Copy to both tier directory and production ready
            tier_destination = destination_dir / f"{asset_id}_{timestamp}.png"
            
            try:
                shutil.copy2(source_file, tier_destination)
                shutil.copy2(source_file, final_destination)
                
                self.logger.info(f"Asset approved and organized: {asset_id} -> {final_destination}")
                return True
                
            except Exception as e:
                self.logger.error(f"Failed to copy approved asset {asset_id}: {e}")
                return False
        
        else:
            # For rejected or review assets
            final_filename = f"{asset_id}_{status.lower()}_{timestamp}.png"
            final_destination = destination_dir / final_filename
            
            try:
                shutil.copy2(source_file, final_destination)
                
                # Create metadata file with issues and recommendations
                self.create_asset_metadata(quality_result, approval_decision, final_destination)
                
                self.logger.info(f"Asset organized for {status}: {asset_id} -> {final_destination}")
                return True
                
            except Exception as e:
                self.logger.error(f"Failed to organize asset {asset_id}: {e}")
                return False

    def create_asset_metadata(self, quality_result: Dict, approval_decision: Dict, 
                            asset_path: Path):
        """Cria arquivo de metadata com detalhes de qualidade e recomendações."""
        
        metadata = {
            "asset_info": {
                "id": quality_result.get("asset_id", "unknown"),
                "rarity": quality_result.get("rarity", "common"),
                "category": quality_result.get("category", "unknown"),
                "file_path": str(asset_path)
            },
            "quality_scores": {
                "overall_score": quality_result.get("overall_score", 0.0),
                "hades_style_compliance": (quality_result.get("pen_ink_style_score", 0) + 
                                         quality_result.get("chiaroscuro_lighting_score", 0)) / 2,
                "egyptian_authenticity": quality_result.get("egyptian_authenticity", 0),
                "technical_quality": quality_result.get("resolution_score", 0)
            },
            "approval_decision": approval_decision,
            "issues": {
                "critical": quality_result.get("critical_issues", []),
                "minor": quality_result.get("minor_issues", [])
            },
            "recommendations": quality_result.get("recommendations", []),
            "timestamp": datetime.now().isoformat()
        }
        
        metadata_file = asset_path.with_suffix('.json')
        
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.warning(f"Failed to create metadata for {asset_path}: {e}")

    def generate_approval_report(self, approval_summary: Dict, batch_data: Dict):
        """Gera relatório detalhado do processo de aprovação."""
        
        report_content = f"""
# AUTOMATED APPROVAL REPORT - FASE 6
## Workflow Execution Results

**Execution Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Batch Processed:** {batch_data.get('directory', 'Unknown')}

---

## APPROVAL SUMMARY

**ASSETS PROCESSED:** {approval_summary['processed']}

**APPROVAL RESULTS:**
- ✅ **Professional Tier:** {approval_summary.get('approved_professional', 0)} assets
- ✅ **Standard Approved:** {approval_summary.get('approved_standard', 0)} assets  
- ⚠️ **Needs Review:** {approval_summary.get('needs_review', 0)} assets
- ❌ **Rejected:** {approval_summary.get('rejected', 0)} assets

**SUCCESS RATE:** {((approval_summary.get('approved_professional', 0) + approval_summary.get('approved_standard', 0)) / max(approval_summary['processed'], 1) * 100):.1f}%

---

## WORKFLOW ORGANIZATION

**ASSETS MOVED TO PRODUCTION READY:**
"""
        
        # List production-ready assets by rarity
        for rarity, directory in self.rarity_dirs.items():
            if directory.exists():
                assets_count = len(list(directory.glob("*.png")))
                if assets_count > 0:
                    report_content += f"\n- **{rarity.title()}:** {assets_count} assets ready"
        
        report_content += f"""

**QUALITY TIER DISTRIBUTION:**
- **Professional Tier:** {approval_summary.get('approved_professional', 0)} assets (Premium quality)
- **Standard Tier:** {approval_summary.get('approved_standard', 0)} assets (Production ready)
- **Review Queue:** {approval_summary.get('needs_review', 0)} assets (Minor improvements)
- **Rejected Queue:** {approval_summary.get('rejected', 0)} assets (Major issues)

---

## FILE MOVEMENTS

**SUCCESSFULLY ORGANIZED:**
"""
        
        for moved_file in approval_summary.get("moved_files", []):
            report_content += f"\n- `{moved_file['asset_id']}` → {moved_file['decision']}"
        
        if approval_summary.get("errors"):
            report_content += f"""

**ERRORS ENCOUNTERED:**
"""
            for error in approval_summary["errors"]:
                report_content += f"\n- {error}"
        
        report_content += f"""

---

## NEXT STEPS

### FOR APPROVED ASSETS ({approval_summary.get('approved_professional', 0) + approval_summary.get('approved_standard', 0)} assets):
1. **Ready for FASE 7 Integration**
2. Assets organized in `production_ready/` by rarity
3. Professional tier assets prioritized for key game elements
4. Standard tier assets ready for implementation

### FOR REVIEW ASSETS ({approval_summary.get('needs_review', 0)} assets):
1. **Minor Enhancement Needed**
2. Review metadata files for specific recommendations
3. Apply suggested improvements
4. Re-submit for approval

### FOR REJECTED ASSETS ({approval_summary.get('rejected', 0)} assets):
1. **Regeneration Required**
2. Address critical style or technical issues
3. Follow enhanced prompts and guidelines
4. Re-process through quality control

---

## QUALITY CERTIFICATION

**APPROVAL WORKFLOW STATUS:** {'🎉 SUCCESSFUL' if approval_summary['processed'] > 0 and len(approval_summary.get('errors', [])) == 0 else '⚠️ WITH ISSUES'}

**PRODUCTION READINESS:** {approval_summary.get('approved_professional', 0) + approval_summary.get('approved_standard', 0)} assets certified for game integration

**HADES-EGYPTIAN STANDARD COMPLIANCE:** {'✅ ACHIEVED' if (approval_summary.get('approved_professional', 0) + approval_summary.get('approved_standard', 0)) / max(approval_summary['processed'], 1) >= 0.8 else '⏳ IN PROGRESS'}

---

*Automated Approval System v6.0*  
*Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        # Save report
        report_file = self.workflow_dir / "logs" / f"approval_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.logger.info(f"Approval report generated: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate approval report: {e}")

    def create_production_manifest(self) -> Dict:
        """Cria manifesto de assets prontos para produção."""
        
        manifest = {
            "generation_date": datetime.now().isoformat(),
            "assets_ready_for_production": {},
            "quality_certification": {},
            "integration_instructions": {}
        }
        
        total_production_assets = 0
        
        # Scan production-ready directories
        for rarity, directory in self.rarity_dirs.items():
            if directory.exists():
                assets = list(directory.glob("*.png"))
                asset_list = []
                
                for asset_path in assets:
                    # Try to load metadata if available
                    metadata_path = asset_path.with_suffix('.json')
                    if metadata_path.exists():
                        try:
                            with open(metadata_path, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)
                            
                            asset_info = {
                                "filename": asset_path.name,
                                "asset_id": metadata.get("asset_info", {}).get("id", asset_path.stem),
                                "quality_tier": "PROFESSIONAL" if "professional" in asset_path.name.lower() else "STANDARD",
                                "overall_score": metadata.get("quality_scores", {}).get("overall_score", 0.0),
                                "certification": "APPROVED"
                            }
                        except:
                            asset_info = {
                                "filename": asset_path.name,
                                "asset_id": asset_path.stem,
                                "quality_tier": "STANDARD",
                                "certification": "APPROVED"
                            }
                    else:
                        asset_info = {
                            "filename": asset_path.name,
                            "asset_id": asset_path.stem,
                            "quality_tier": "STANDARD", 
                            "certification": "APPROVED"
                        }
                    
                    asset_list.append(asset_info)
                
                manifest["assets_ready_for_production"][rarity] = {
                    "count": len(asset_list),
                    "assets": asset_list
                }
                
                total_production_assets += len(asset_list)
        
        # Quality certification summary
        manifest["quality_certification"] = {
            "total_production_ready_assets": total_production_assets,
            "certification_standard": "Hades-Egyptian Fusion Professional Gaming Assets",
            "quality_thresholds_met": total_production_assets > 0,
            "certification_date": datetime.now().strftime("%Y-%m-%d"),
            "certifying_system": "Extreme Quality Control System v6.0"
        }
        
        # Integration instructions
        manifest["integration_instructions"] = {
            "legendary_assets": {
                "use_case": "Primary deities, boss characters, key story elements",
                "priority": "HIGH",
                "implementation_notes": "Professional tier quality, use for prominent game features"
            },
            "epic_assets": {
                "use_case": "Main heroes, important environments, significant gameplay elements", 
                "priority": "MEDIUM-HIGH",
                "implementation_notes": "High quality assets for core gameplay"
            },
            "rare_assets": {
                "use_case": "Supporting creatures, secondary environments, special effects",
                "priority": "MEDIUM",
                "implementation_notes": "Quality assets for enhanced gameplay experience"
            },
            "common_assets": {
                "use_case": "UI elements, frames, borders, decorative elements",
                "priority": "STANDARD",
                "implementation_notes": "Consistent quality for interface elements"
            }
        }
        
        # Save manifest
        manifest_file = self.production_ready / "PRODUCTION_MANIFEST.json"
        
        try:
            with open(manifest_file, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Production manifest created: {manifest_file}")
            print(f"\nPRODUCTION MANIFEST CREATED:")
            print(f"Total assets ready: {total_production_assets}")
            print(f"Manifest location: {manifest_file}")
            
            return manifest
            
        except Exception as e:
            self.logger.error(f"Failed to create production manifest: {e}")
            return {}

def main():
    """Execução principal do sistema de aprovação automatizada."""
    
    system = AutomatedApprovalSystem()
    
    print("AUTOMATED APPROVAL SYSTEM - FASE 6")
    print("=" * 36)
    print("1. Process quality results file")
    print("2. Create production manifest") 
    print("3. Show workflow status")
    print("4. Organize existing assets")
    print("0. Exit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        results_file = input("Enter quality results file path: ").strip()
        if results_file and Path(results_file).exists():
            summary = system.process_quality_results(results_file)
            
            print(f"\nAPPROVAL PROCESSING COMPLETE:")
            print(f"  Processed: {summary.get('processed', 0)} assets")
            print(f"  Professional: {summary.get('approved_professional', 0)}")
            print(f"  Standard: {summary.get('approved_standard', 0)}")
            print(f"  Review: {summary.get('needs_review', 0)}")
            print(f"  Rejected: {summary.get('rejected', 0)}")
            
            if summary.get('errors'):
                print(f"  Errors: {len(summary['errors'])}")
        else:
            print("Invalid results file path!")
    
    elif choice == "2":
        manifest = system.create_production_manifest()
        if manifest:
            total = manifest.get("quality_certification", {}).get("total_production_ready_assets", 0)
            print(f"Production manifest created with {total} assets ready for integration!")
    
    elif choice == "3":
        print("Workflow status feature coming soon!")
    
    elif choice == "4":
        print("Asset organization feature coming soon!")

if __name__ == "__main__":
    main()