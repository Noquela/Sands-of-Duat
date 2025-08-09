#!/usr/bin/env python3
"""
PROCESS GENERATED ASSETS THROUGH QUALITY CONTROL
ASCII-safe version for processing newly generated Hades-Egyptian assets
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from PIL import Image

class GeneratedAssetProcessor:
    def __init__(self):
        self.base_dir = Path(".")
        self.generated_assets_dir = Path("../../assets/generated_art")
        self.approved_dir = Path("approval_workflow/approved")
        self.production_ready_dir = Path("approval_workflow/production_ready")
        
        # Create directories
        for directory in [self.approved_dir, self.production_ready_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            for rarity in ["legendary", "epic", "rare", "common"]:
                (directory / f"{rarity}_assets").mkdir(exist_ok=True)

    def analyze_asset(self, image_path: Path) -> dict:
        """Basic quality analysis of generated asset"""
        
        try:
            with Image.open(image_path) as img:
                # Basic technical metrics
                width, height = img.size
                file_size = image_path.stat().st_size
                
                # Basic quality assessment
                quality_metrics = {
                    "filename": image_path.name,
                    "resolution": f"{width}x{height}",
                    "file_size_mb": round(file_size / (1024 * 1024), 2),
                    "format": img.format,
                    "mode": img.mode,
                }
                
                # Quality scoring based on our specifications
                resolution_score = 1.0 if (width >= 1024 and height >= 1024) else 0.7
                file_size_score = 1.0 if (0.5 <= file_size / (1024*1024) <= 10) else 0.8
                format_score = 1.0 if img.format == "PNG" else 0.6
                
                overall_score = (resolution_score + file_size_score + format_score) / 3
                
                quality_metrics.update({
                    "resolution_score": resolution_score,
                    "file_size_score": file_size_score, 
                    "format_score": format_score,
                    "overall_score": overall_score,
                    "quality_tier": self.determine_quality_tier(overall_score)
                })
                
                return quality_metrics
                
        except Exception as e:
            return {"error": str(e), "overall_score": 0.0}

    def determine_quality_tier(self, score: float) -> str:
        """Determine quality tier based on score"""
        if score >= 0.95:
            return "PROFESSIONAL"
        elif score >= 0.80:
            return "APPROVED"
        elif score >= 0.70:
            return "NEEDS_REVIEW"
        else:
            return "REJECTED"

    def determine_rarity_from_filename(self, filename: str) -> str:
        """Extract rarity from filename"""
        filename_lower = filename.lower()
        
        if "legendary" in filename_lower:
            return "legendary"
        elif "epic" in filename_lower:
            return "epic" 
        elif "rare" in filename_lower:
            return "rare"
        elif "common" in filename_lower:
            return "common"
        else:
            # Default fallback based on content keywords
            if any(deity in filename_lower for deity in ["anubis", "ra", "isis", "set", "thoth"]):
                return "legendary"
            elif any(hero in filename_lower for hero in ["warrior", "hero", "pharaoh"]):
                return "epic"
            elif any(creature in filename_lower for creature in ["sphinx", "mummy", "scarab"]):
                return "rare"
            else:
                return "rare"  # Default

    def process_generated_assets(self) -> dict:
        """Process all generated assets through quality control"""
        
        print("PROCESSING GENERATED ASSETS THROUGH QUALITY CONTROL")
        print("=" * 52)
        
        if not self.generated_assets_dir.exists():
            print(f"Generated assets directory not found: {self.generated_assets_dir}")
            return {"error": "No generated assets found"}
        
        # Find all PNG files
        png_files = list(self.generated_assets_dir.glob("*.png"))
        
        if not png_files:
            print("No PNG assets found for processing")
            return {"error": "No assets to process"}
        
        print(f"Found {len(png_files)} assets to process")
        
        processing_results = {
            "timestamp": datetime.now().isoformat(),
            "total_assets": len(png_files),
            "processed_assets": [],
            "summary": {
                "professional": 0,
                "approved": 0,
                "needs_review": 0,
                "rejected": 0
            },
            "by_rarity": {
                "legendary": {"total": 0, "approved": 0},
                "epic": {"total": 0, "approved": 0},
                "rare": {"total": 0, "approved": 0},
                "common": {"total": 0, "approved": 0}
            }
        }
        
        for i, asset_path in enumerate(png_files):
            print(f"\n[{i+1}/{len(png_files)}] Processing {asset_path.name}...")
            
            # Analyze asset quality
            analysis = self.analyze_asset(asset_path)
            rarity = self.determine_rarity_from_filename(asset_path.name)
            
            # Update statistics
            processing_results["by_rarity"][rarity]["total"] += 1
            
            if analysis.get("overall_score", 0) > 0:
                quality_tier = analysis["quality_tier"]
                processing_results["summary"][quality_tier.lower()] += 1
                
                print(f"  Quality Score: {analysis['overall_score']:.2f}")
                print(f"  Quality Tier: {quality_tier}")
                print(f"  Rarity: {rarity}")
                
                # Move to appropriate directory if approved
                if quality_tier in ["PROFESSIONAL", "APPROVED"]:
                    self.move_to_approved(asset_path, rarity, quality_tier, analysis)
                    processing_results["by_rarity"][rarity]["approved"] += 1
                    print(f"  STATUS: APPROVED for production")
                else:
                    print(f"  STATUS: {quality_tier}")
            else:
                processing_results["summary"]["rejected"] += 1
                print(f"  STATUS: ANALYSIS FAILED")
            
            # Store detailed results
            processing_results["processed_assets"].append({
                "filename": asset_path.name,
                "rarity": rarity,
                "analysis": analysis,
                "status": analysis.get("quality_tier", "ERROR")
            })
        
        # Save processing report
        self.save_processing_report(processing_results)
        
        # Display summary
        self.display_summary(processing_results)
        
        return processing_results

    def move_to_approved(self, asset_path: Path, rarity: str, quality_tier: str, analysis: dict):
        """Move approved asset to production ready directory"""
        
        # Determine target directory
        if quality_tier == "PROFESSIONAL":
            target_dir = self.approved_dir / "professional_tier" 
        else:
            target_dir = self.approved_dir / "standard_tier"
        
        target_dir.mkdir(exist_ok=True)
        
        # Copy to approved directory
        import shutil
        target_path = target_dir / asset_path.name
        shutil.copy2(asset_path, target_path)
        
        # Also copy to production ready by rarity
        production_target = self.production_ready_dir / f"{rarity}_assets" / asset_path.name
        shutil.copy2(asset_path, production_target)
        
        # Create approval metadata
        approval_metadata = {
            "approval_info": {
                "approved_date": datetime.now().isoformat(),
                "quality_tier": quality_tier,
                "rarity": rarity,
                "approved_for_production": True
            },
            "quality_analysis": analysis,
            "production_path": str(production_target),
            "approved_path": str(target_path)
        }
        
        metadata_path = target_path.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(approval_metadata, f, indent=2)

    def save_processing_report(self, results: dict):
        """Save comprehensive processing report"""
        
        report_file = Path(f"generated_assets_qc_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nProcessing report saved: {report_file}")

    def display_summary(self, results: dict):
        """Display processing summary"""
        
        total = results["total_assets"]
        summary = results["summary"]
        
        print(f"\n" + "=" * 50)
        print("QUALITY CONTROL PROCESSING COMPLETE")
        print("=" * 50)
        
        print(f"Total Assets Processed: {total}")
        print(f"Professional Tier: {summary['professional']}")
        print(f"Standard Approved: {summary['approved']}")
        print(f"Needs Review: {summary['needs_review']}")
        print(f"Rejected: {summary['rejected']}")
        
        approved_total = summary['professional'] + summary['approved']
        approval_rate = (approved_total / total) * 100 if total > 0 else 0
        
        print(f"\nOverall Approval Rate: {approval_rate:.1f}%")
        
        print(f"\nAPPROVED ASSETS BY RARITY:")
        for rarity, stats in results["by_rarity"].items():
            if stats["total"] > 0:
                rarity_rate = (stats["approved"] / stats["total"]) * 100
                print(f"  {rarity.title()}: {stats['approved']}/{stats['total']} ({rarity_rate:.1f}%)")
        
        if approved_total > 0:
            print(f"\n{approved_total} ASSETS READY FOR FINAL INTEGRATION!")

def main():
    processor = GeneratedAssetProcessor()
    results = processor.process_generated_assets()
    
    if "error" not in results:
        print("\nAssets are now ready for FASE 7 - Final Integration!")

if __name__ == "__main__":
    main()