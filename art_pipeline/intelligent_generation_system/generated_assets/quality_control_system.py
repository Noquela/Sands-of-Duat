
#!/usr/bin/env python3
"""
QUALITY CONTROL SYSTEM - HADES EGYPTIAN ASSETS
==============================================
Sistema automatizado de validação de qualidade
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class QualityController:
    def __init__(self):
        self.quality_standards = {
            "legendary": {
                "min_resolution": (1024, 1024),
                "max_file_size": 10 * 1024 * 1024,  # 10MB
                "required_elements": ["dramatic_lighting", "high_detail", "vibrant_colors"],
                "forbidden_elements": ["multiple_characters", "text", "watermarks", "blur"]
            },
            "epic": {
                "min_resolution": (768, 768), 
                "max_file_size": 8 * 1024 * 1024,
                "required_elements": ["good_lighting", "detailed", "clear"],
                "forbidden_elements": ["multiple_characters", "text", "watermarks"]
            },
            "rare": {
                "min_resolution": (512, 512),
                "max_file_size": 6 * 1024 * 1024,
                "required_elements": ["clear", "recognizable"],
                "forbidden_elements": ["multiple_characters", "text"]
            },
            "common": {
                "min_resolution": (512, 512),
                "max_file_size": 5 * 1024 * 1024,
                "required_elements": ["clear"],
                "forbidden_elements": ["text"]
            }
        }
        
        self.quality_db = Path("quality_database.json")
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
                    "total_evaluated": 0,
                    "approved": 0,
                    "rejected": 0,
                    "pending_review": 0
                }
            }
    
    def evaluate_image(self, image_path: str, expected_rarity: str) -> Dict:
        """Evaluate single image quality."""
        
        evaluation = {
            "image_path": image_path,
            "timestamp": datetime.now().isoformat(),
            "rarity": expected_rarity,
            "checks": {},
            "overall_score": 0.0,
            "status": "pending",
            "issues": []
        }
        
        try:
            from PIL import Image
            
            # Basic file checks
            if not os.path.exists(image_path):
                evaluation["issues"].append("File not found")
                evaluation["status"] = "rejected"
                return evaluation
            
            # Load image
            img = Image.open(image_path)
            width, height = img.size
            file_size = os.path.getsize(image_path)
            
            standards = self.quality_standards[expected_rarity]
            
            # Resolution check
            min_width, min_height = standards["min_resolution"]
            if width >= min_width and height >= min_height:
                evaluation["checks"]["resolution"] = {"passed": True, "value": f"{width}x{height}"}
            else:
                evaluation["checks"]["resolution"] = {"passed": False, "value": f"{width}x{height}"}
                evaluation["issues"].append(f"Resolution too low: {width}x{height}")
            
            # File size check  
            if file_size <= standards["max_file_size"]:
                evaluation["checks"]["file_size"] = {"passed": True, "value": f"{file_size//1024}KB"}
            else:
                evaluation["checks"]["file_size"] = {"passed": False, "value": f"{file_size//1024}KB"}
                evaluation["issues"].append(f"File too large: {file_size//1024}KB")
            
            # Calculate score
            passed_checks = sum(1 for check in evaluation["checks"].values() if check["passed"])
            total_checks = len(evaluation["checks"])
            evaluation["overall_score"] = passed_checks / total_checks if total_checks > 0 else 0
            
            # Determine status
            if evaluation["overall_score"] >= 0.8 and not evaluation["issues"]:
                evaluation["status"] = "approved"
            elif evaluation["overall_score"] >= 0.6:
                evaluation["status"] = "review"
            else:
                evaluation["status"] = "rejected"
            
        except Exception as e:
            evaluation["issues"].append(f"Error processing image: {str(e)}")
            evaluation["status"] = "error"
        
        return evaluation
    
    def batch_evaluate(self, images_directory: str) -> Dict:
        """Evaluate all images in directory."""
        
        print(f"Evaluating images in: {images_directory}")
        
        image_dir = Path(images_directory)
        if not image_dir.exists():
            return {"error": "Directory not found"}
        
        # Find all image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(image_dir.rglob(f"*{ext}"))
        
        print(f"Found {len(image_files)} images to evaluate")
        
        results = []
        for image_file in image_files:
            # Determine expected rarity from path
            rarity = "common"  # default
            path_str = str(image_file).lower()
            if "legendary" in path_str:
                rarity = "legendary"
            elif "epic" in path_str:
                rarity = "epic"
            elif "rare" in path_str:
                rarity = "rare"
            
            evaluation = self.evaluate_image(str(image_file), rarity)
            results.append(evaluation)
            
            print(f"  {image_file.name}: {evaluation['status']} ({evaluation['overall_score']:.2f})")
        
        # Update database
        self.db["evaluations"].extend(results)
        self.update_statistics()
        self.save_quality_database()
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_evaluated": len(results),
            "approved": sum(1 for r in results if r["status"] == "approved"),
            "rejected": sum(1 for r in results if r["status"] == "rejected"),
            "review": sum(1 for r in results if r["status"] == "review"),
            "error": sum(1 for r in results if r["status"] == "error"),
            "average_score": sum(r["overall_score"] for r in results) / len(results) if results else 0,
            "details": results
        }
        
        return report
    
    def update_statistics(self):
        """Update quality statistics."""
        stats = {
            "total_evaluated": len(self.db["evaluations"]),
            "approved": sum(1 for e in self.db["evaluations"] if e["status"] == "approved"),
            "rejected": sum(1 for e in self.db["evaluations"] if e["status"] == "rejected"),
            "pending_review": sum(1 for e in self.db["evaluations"] if e["status"] == "review"),
            "error": sum(1 for e in self.db["evaluations"] if e["status"] == "error")
        }
        self.db["statistics"] = stats
    
    def save_quality_database(self):
        """Save quality database to file."""
        with open(self.quality_db, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)
    
    def generate_quality_report(self) -> str:
        """Generate comprehensive quality report."""
        
        stats = self.db["statistics"]
        
        report = f"""
QUALITY CONTROL REPORT - HADES EGYPTIAN ASSETS
==============================================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

OVERALL STATISTICS:
- Total Evaluated: {stats["total_evaluated"]}
- Approved: {stats["approved"]} ({stats["approved"]/stats["total_evaluated"]*100:.1f}%)
- Rejected: {stats["rejected"]} ({stats["rejected"]/stats["total_evaluated"]*100:.1f}%)
- Needs Review: {stats["pending_review"]} ({stats["pending_review"]/stats["total_evaluated"]*100:.1f}%)
- Errors: {stats["error"]}

QUALITY BREAKDOWN BY RARITY:
"""
        
        # Group by rarity
        by_rarity = {}
        for eval in self.db["evaluations"]:
            rarity = eval.get("rarity", "unknown")
            if rarity not in by_rarity:
                by_rarity[rarity] = {"approved": 0, "rejected": 0, "review": 0, "total": 0}
            
            by_rarity[rarity]["total"] += 1
            by_rarity[rarity][eval["status"]] = by_rarity[rarity].get(eval["status"], 0) + 1
        
        for rarity, data in by_rarity.items():
            report += f"\n{rarity.upper()}:"
            report += f"\n  Total: {data['total']}"
            report += f"\n  Approved: {data.get('approved', 0)} ({data.get('approved', 0)/data['total']*100:.1f}%)"
            report += f"\n  Rejected: {data.get('rejected', 0)}"
            report += f"\n  Review: {data.get('review', 0)}"
        
        # Common issues
        all_issues = []
        for eval in self.db["evaluations"]:
            all_issues.extend(eval.get("issues", []))
        
        if all_issues:
            from collections import Counter
            issue_counts = Counter(all_issues)
            
            report += "\n\nCOMMON ISSUES:"
            for issue, count in issue_counts.most_common(5):
                report += f"\n- {issue}: {count} times"
        
        report += "\n\nRECOMMENDATIONS:"
        if stats["rejected"] > stats["approved"]:
            report += "\n- Quality is below standards. Review generation settings."
            report += "\n- Consider using higher-end AI service or model."
        elif stats["pending_review"] > 0:
            report += f"\n- {stats['pending_review']} images need manual review."
        else:
            report += "\n- Quality is excellent! Assets ready for production."
        
        return report

def main():
    """Run quality control evaluation."""
    controller = QualityController()
    
    print("QUALITY CONTROL SYSTEM")
    print("=" * 22)
    print("1. Evaluate all images")
    print("2. Generate quality report")
    print("0. Exit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        images_dir = input("Enter images directory path: ").strip()
        if not images_dir:
            images_dir = "generated_assets"
        
        report = controller.batch_evaluate(images_dir)
        
        print(f"\nEVALUATION COMPLETE:")
        print(f"- Total: {report['total_evaluated']}")
        print(f"- Approved: {report['approved']}")
        print(f"- Rejected: {report['rejected']}")
        print(f"- Review: {report['review']}")
        print(f"- Average Score: {report['average_score']:.2f}")
        
    elif choice == "2":
        report_text = controller.generate_quality_report()
        
        report_file = Path("quality_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(report_text)
        print(f"\nReport saved: {report_file}")

if __name__ == "__main__":
    main()
