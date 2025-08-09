
#!/usr/bin/env python3
"""
QUALITY CONTROL AUTOMATION - MASS PRODUCTION
============================================
Automated quality control for mass-produced assets
"""

import os
import json
import shutil
from pathlib import Path
from PIL import Image
from datetime import datetime
from typing import Dict, List, Tuple

class MassProductionQC:
    def __init__(self):
        self.base_dir = Path(".")
        self.quality_db = self.base_dir / "mass_production_quality.json"
        
        # Quality thresholds by rarity
        self.thresholds = {
            "legendary": 0.90,
            "epic": 0.85,
            "rare": 0.80, 
            "common": 0.75
        }
        
        # Quality criteria
        self.criteria = {
            "min_resolution": (1024, 1024),
            "max_file_size": 15 * 1024 * 1024,  # 15MB
            "required_format": ".png",
            "forbidden_keywords": ["multiple", "crowd", "text", "watermark"]
        }
        
        self.load_quality_database()
    
    def load_quality_database(self):
        """Load existing quality database."""
        if self.quality_db.exists():
            with open(self.quality_db, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
        else:
            self.db = {
                "evaluations": [],
                "statistics": {
                    "total": 0,
                    "approved": 0,
                    "rejected": 0,
                    "pending_review": 0
                },
                "batch_results": {}
            }
    
    def evaluate_asset(self, image_path: str, asset_info: Dict) -> Dict:
        """Evaluate single asset quality."""
        
        evaluation = {
            "asset_path": image_path,
            "asset_id": asset_info.get("id", "unknown"),
            "rarity": asset_info.get("rarity", "common"),
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "overall_score": 0.0,
            "status": "pending",
            "issues": []
        }
        
        try:
            # File existence check
            if not os.path.exists(image_path):
                evaluation["issues"].append("File not found")
                evaluation["status"] = "rejected"
                return evaluation
            
            # Load and analyze image
            img = Image.open(image_path)
            width, height = img.size
            file_size = os.path.getsize(image_path)
            
            # Resolution check
            min_width, min_height = self.criteria["min_resolution"]
            if width >= min_width and height >= min_height:
                evaluation["checks"]["resolution"] = {"passed": True, "value": f"{width}x{height}"}
            else:
                evaluation["checks"]["resolution"] = {"passed": False, "value": f"{width}x{height}"}
                evaluation["issues"].append(f"Low resolution: {width}x{height}")
            
            # File size check
            if file_size <= self.criteria["max_file_size"]:
                evaluation["checks"]["file_size"] = {"passed": True, "value": f"{file_size//1024}KB"}
            else:
                evaluation["checks"]["file_size"] = {"passed": False, "value": f"{file_size//1024}KB"}
                evaluation["issues"].append(f"File too large: {file_size//1024}KB")
            
            # Format check
            if image_path.lower().endswith(self.criteria["required_format"]):
                evaluation["checks"]["format"] = {"passed": True, "value": "PNG"}
            else:
                evaluation["checks"]["format"] = {"passed": False, "value": "Not PNG"}
                evaluation["issues"].append("Wrong format (not PNG)")
            
            # Visual quality check (basic)
            # Check for extreme darkness or brightness
            grayscale = img.convert('L')
            avg_brightness = sum(grayscale.getdata()) / len(grayscale.getdata())
            
            if 20 <= avg_brightness <= 220:  # Reasonable brightness range
                evaluation["checks"]["brightness"] = {"passed": True, "value": f"{avg_brightness:.1f}"}
            else:
                evaluation["checks"]["brightness"] = {"passed": False, "value": f"{avg_brightness:.1f}"}
                evaluation["issues"].append(f"Unusual brightness: {avg_brightness:.1f}")
            
            # Calculate overall score
            passed_checks = sum(1 for check in evaluation["checks"].values() if check["passed"])
            total_checks = len(evaluation["checks"])
            evaluation["overall_score"] = passed_checks / total_checks if total_checks > 0 else 0
            
            # Determine status based on rarity threshold
            rarity = evaluation["rarity"]
            threshold = self.thresholds.get(rarity, 0.75)
            
            if evaluation["overall_score"] >= threshold and not evaluation["issues"]:
                evaluation["status"] = "approved"
            elif evaluation["overall_score"] >= 0.6:
                evaluation["status"] = "review"
            else:
                evaluation["status"] = "rejected"
            
        except Exception as e:
            evaluation["issues"].append(f"Error processing: {str(e)}")
            evaluation["status"] = "error"
        
        return evaluation
    
    def batch_evaluate_directory(self, directory_path: str) -> Dict:
        """Evaluate all assets in a directory."""
        
        print(f"Evaluating directory: {directory_path}")
        
        directory = Path(directory_path)
        if not directory.exists():
            return {"error": "Directory not found"}
        
        # Find all image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(directory.rglob(f"*{ext}"))
        
        print(f"Found {len(image_files)} images to evaluate")
        
        # Evaluate each image
        evaluations = []
        for image_file in image_files:
            # Extract asset info from filename
            filename = image_file.stem
            parts = filename.split('_')
            
            asset_info = {
                "id": filename,
                "rarity": "common"  # default
            }
            
            # Try to determine rarity from path or filename
            path_str = str(image_file).lower()
            if "legendary" in path_str or "deity" in path_str:
                asset_info["rarity"] = "legendary"
            elif "epic" in path_str or ("hero" in path_str or "environment" in path_str):
                asset_info["rarity"] = "epic"  
            elif "rare" in path_str or "creature" in path_str:
                asset_info["rarity"] = "rare"
            
            evaluation = self.evaluate_asset(str(image_file), asset_info)
            evaluations.append(evaluation)
            
            status_symbol = {
                "approved": "✓",
                "rejected": "✗", 
                "review": "?",
                "error": "!"
            }.get(evaluation["status"], "?")
            
            print(f"  {status_symbol} {image_file.name}: {evaluation['status']} ({evaluation['overall_score']:.2f})")
        
        # Update database
        self.db["evaluations"].extend(evaluations)
        self.update_statistics()
        self.save_quality_database()
        
        # Generate batch report
        approved = [e for e in evaluations if e["status"] == "approved"]
        rejected = [e for e in evaluations if e["status"] == "rejected"]
        review = [e for e in evaluations if e["status"] == "review"]
        
        batch_report = {
            "timestamp": datetime.now().isoformat(),
            "directory": str(directory),
            "total_evaluated": len(evaluations),
            "approved": len(approved),
            "rejected": len(rejected), 
            "review": len(review),
            "approval_rate": len(approved) / len(evaluations) * 100 if evaluations else 0,
            "evaluations": evaluations
        }
        
        return batch_report
    
    def organize_by_quality(self, source_dir: str, output_base_dir: str):
        """Organize assets by quality status."""
        
        source = Path(source_dir)
        base_output = Path(output_base_dir)
        
        # Create quality directories
        approved_dir = base_output / "approved"
        rejected_dir = base_output / "rejected"
        review_dir = base_output / "review"
        
        for dir in [approved_dir, rejected_dir, review_dir]:
            dir.mkdir(parents=True, exist_ok=True)
        
        moved_count = {"approved": 0, "rejected": 0, "review": 0}
        
        # Move files based on latest evaluations
        for evaluation in self.db["evaluations"]:
            asset_path = Path(evaluation["asset_path"])
            status = evaluation["status"]
            
            if asset_path.exists() and status in moved_count:
                target_dir = {
                    "approved": approved_dir,
                    "rejected": rejected_dir,
                    "review": review_dir
                }[status]
                
                target_path = target_dir / asset_path.name
                
                try:
                    shutil.move(str(asset_path), str(target_path))
                    moved_count[status] += 1
                    print(f"Moved {asset_path.name} to {status}/")
                except Exception as e:
                    print(f"Error moving {asset_path.name}: {e}")
        
        print(f"\nOrganization complete:")
        for status, count in moved_count.items():
            print(f"  {status.title()}: {count} files")
    
    def update_statistics(self):
        """Update quality statistics."""
        stats = {
            "total": len(self.db["evaluations"]),
            "approved": sum(1 for e in self.db["evaluations"] if e["status"] == "approved"),
            "rejected": sum(1 for e in self.db["evaluations"] if e["status"] == "rejected"),
            "pending_review": sum(1 for e in self.db["evaluations"] if e["status"] == "review"),
            "error": sum(1 for e in self.db["evaluations"] if e["status"] == "error")
        }
        self.db["statistics"] = stats
    
    def save_quality_database(self):
        """Save quality database."""
        with open(self.quality_db, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)
    
    def generate_quality_report(self) -> str:
        """Generate comprehensive quality report."""
        
        stats = self.db["statistics"]
        
        report = f"""
MASS PRODUCTION QUALITY REPORT
==============================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

OVERALL STATISTICS:
- Total Evaluated: {stats["total"]}
- Approved: {stats["approved"]} ({stats["approved"]/max(stats["total"],1)*100:.1f}%)
- Rejected: {stats["rejected"]} ({stats["rejected"]/max(stats["total"],1)*100:.1f}%)
- Needs Review: {stats["pending_review"]} ({stats["pending_review"]/max(stats["total"],1)*100:.1f}%)
- Errors: {stats["error"]}

APPROVAL RATE BY RARITY:
"""
        
        # Group by rarity
        by_rarity = {}
        for eval in self.db["evaluations"]:
            rarity = eval.get("rarity", "unknown")
            if rarity not in by_rarity:
                by_rarity[rarity] = {"total": 0, "approved": 0, "rejected": 0, "review": 0}
            
            by_rarity[rarity]["total"] += 1
            by_rarity[rarity][eval["status"]] = by_rarity[rarity].get(eval["status"], 0) + 1
        
        for rarity, data in by_rarity.items():
            total = data["total"]
            approved = data.get("approved", 0)
            rate = approved / total * 100 if total > 0 else 0
            target_rate = self.thresholds.get(rarity, 0.75) * 100
            
            report += f"\n{rarity.upper()}:"
            report += f"\n  Total: {total} assets"
            report += f"\n  Approved: {approved} ({rate:.1f}%)"
            report += f"\n  Target: {target_rate:.0f}%"
            report += f"\n  Status: {'PASS' if rate >= target_rate else 'FAIL'}"
        
        # Production status
        target_total = 64
        completion_rate = stats["total"] / target_total * 100
        
        report += f"""

PRODUCTION STATUS:
- Target Assets: {target_total}
- Generated: {stats["total"]} ({completion_rate:.1f}%)
- Production Ready: {stats["approved"]}
- Success Rate: {stats["approved"]/target_total*100:.1f}%

NEXT STEPS:
"""
        
        if stats["total"] < target_total:
            report += f"\n- Generate remaining {target_total - stats['total']} assets"
        
        if stats["rejected"] > 0:
            report += f"\n- Regenerate {stats['rejected']} rejected assets"
        
        if stats["pending_review"] > 0:
            report += f"\n- Manual review of {stats['pending_review']} assets"
        
        if stats["approved"] >= target_total * 0.8:
            report += "\n- Ready for final production phase!"
        
        return report

def main():
    """Main quality control execution."""
    qc = MassProductionQC()
    
    print("MASS PRODUCTION QUALITY CONTROL")
    print("=" * 32)
    print("1. Evaluate directory")
    print("2. Organize by quality")  
    print("3. Generate report")
    print("0. Exit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        directory = input("Enter directory path: ").strip()
        if directory:
            report = qc.batch_evaluate_directory(directory)
            print(f"\nEvaluation complete:")
            print(f"- Approved: {report['approved']}")
            print(f"- Rejected: {report['rejected']}")
            print(f"- Review: {report['review']}")
            print(f"- Approval Rate: {report['approval_rate']:.1f}%")
    
    elif choice == "2":
        source = input("Source directory: ").strip()
        output = input("Output base directory: ").strip()
        if source and output:
            qc.organize_by_quality(source, output)
    
    elif choice == "3":
        report_text = qc.generate_quality_report()
        print(report_text)
        
        report_file = Path("mass_production_quality_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\nReport saved: {report_file}")

if __name__ == "__main__":
    main()
