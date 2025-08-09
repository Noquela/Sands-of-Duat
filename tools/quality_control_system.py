#!/usr/bin/env python3
"""
QUALITY CONTROL SYSTEM
======================

PHASE 8: Review and validate all generated assets
Ensure AAA-level quality standards across entire game
"""

from pathlib import Path
from PIL import Image, ImageStat
import json
import shutil

class QualityControlSystem:
    def __init__(self):
        self.assets_dir = Path("../assets/generated_art_lora")
        self.approved_dir = Path("../assets/approved_art")
        self.rejected_dir = Path("../assets/rejected_art")
        self.reports_dir = Path("../quality_reports")
        
        # Create directories
        for dir_path in [self.approved_dir, self.rejected_dir, self.reports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.quality_standards = {
            "min_resolution": (512, 512),
            "min_file_size": 50000,  # 50KB minimum
            "max_file_size": 10000000,  # 10MB maximum
            "required_formats": [".png", ".jpg", ".jpeg"],
            "min_color_diversity": 10,  # Minimum unique colors
            "brightness_range": (20, 235)  # Avoid pure black/white images
        }

    def analyze_image_quality(self, image_path):
        """Analyze individual image quality metrics."""
        try:
            with Image.open(image_path) as img:
                # Basic metrics
                width, height = img.size
                file_size = image_path.stat().st_size
                format_ext = image_path.suffix.lower()
                
                # Color analysis
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Get image statistics
                stat = ImageStat.Stat(img)
                brightness = sum(stat.mean) / len(stat.mean)
                
                # Count unique colors (approximate)
                colors = img.getcolors(maxcolors=256*256*256)
                unique_colors = len(colors) if colors else 0
                
                quality_metrics = {
                    "resolution": (width, height),
                    "file_size": file_size,
                    "format": format_ext,
                    "brightness": brightness,
                    "unique_colors": unique_colors,
                    "aspect_ratio": width / height,
                    "is_grayscale": len(set(stat.mean)) == 1
                }
                
                return quality_metrics
                
        except Exception as e:
            return {"error": str(e)}

    def evaluate_quality_standards(self, metrics, asset_type="general"):
        """Evaluate if asset meets quality standards."""
        issues = []
        passed = True
        
        # Resolution check
        if metrics.get("resolution"):
            width, height = metrics["resolution"]
            min_width, min_height = self.quality_standards["min_resolution"]
            if width < min_width or height < min_height:
                issues.append(f"Resolution too low: {width}x{height} < {min_width}x{min_height}")
                passed = False
        
        # File size check
        file_size = metrics.get("file_size", 0)
        if file_size < self.quality_standards["min_file_size"]:
            issues.append(f"File size too small: {file_size} bytes")
            passed = False
        elif file_size > self.quality_standards["max_file_size"]:
            issues.append(f"File size too large: {file_size} bytes")
            passed = False
        
        # Format check
        format_ext = metrics.get("format", "")
        if format_ext not in self.quality_standards["required_formats"]:
            issues.append(f"Invalid format: {format_ext}")
            passed = False
        
        # Brightness check
        brightness = metrics.get("brightness", 128)
        min_bright, max_bright = self.quality_standards["brightness_range"]
        if brightness < min_bright:
            issues.append(f"Image too dark: brightness {brightness:.1f}")
            passed = False
        elif brightness > max_bright:
            issues.append(f"Image too bright: brightness {brightness:.1f}")
            passed = False
        
        # Color diversity check
        unique_colors = metrics.get("unique_colors", 0)
        if unique_colors < self.quality_standards["min_color_diversity"]:
            issues.append(f"Insufficient color diversity: {unique_colors} colors")
            passed = False
        
        # Grayscale check (should have color for game assets)
        if metrics.get("is_grayscale"):
            issues.append("Image appears to be grayscale")
            passed = False
        
        return {
            "passed": passed,
            "issues": issues,
            "score": max(0, 100 - len(issues) * 10)  # Quality score out of 100
        }

    def process_asset_category(self, category_dir):
        """Process all assets in a category."""
        category_name = category_dir.name
        print(f"Processing {category_name.upper()} assets...")
        
        results = {
            "category": category_name,
            "total_assets": 0,
            "passed": 0,
            "failed": 0,
            "assets": []
        }
        
        if not category_dir.exists():
            print(f"Category directory not found: {category_dir}")
            return results
        
        for asset_path in category_dir.glob("*.png"):
            results["total_assets"] += 1
            
            print(f"  Analyzing: {asset_path.name}")
            
            # Analyze quality
            metrics = self.analyze_image_quality(asset_path)
            if "error" in metrics:
                print(f"    Error: {metrics['error']}")
                results["failed"] += 1
                continue
            
            # Evaluate standards
            evaluation = self.evaluate_quality_standards(metrics, category_name)
            
            asset_result = {
                "filename": asset_path.name,
                "path": str(asset_path),
                "metrics": metrics,
                "evaluation": evaluation
            }
            
            if evaluation["passed"]:
                print(f"    PASSED (Score: {evaluation['score']})")
                # Copy to approved directory
                approved_path = self.approved_dir / category_name
                approved_path.mkdir(exist_ok=True)
                shutil.copy2(asset_path, approved_path / asset_path.name)
                results["passed"] += 1
            else:
                print(f"    FAILED (Score: {evaluation['score']})")
                for issue in evaluation["issues"]:
                    print(f"      - {issue}")
                # Copy to rejected directory
                rejected_path = self.rejected_dir / category_name
                rejected_path.mkdir(exist_ok=True)
                shutil.copy2(asset_path, rejected_path / asset_path.name)
                results["failed"] += 1
            
            results["assets"].append(asset_result)
        
        return results

    def generate_quality_report(self, all_results):
        """Generate comprehensive quality report."""
        total_assets = sum(result["total_assets"] for result in all_results)
        total_passed = sum(result["passed"] for result in all_results)
        total_failed = sum(result["failed"] for result in all_results)
        
        success_rate = (total_passed / total_assets * 100) if total_assets > 0 else 0
        
        report_content = f"""# QUALITY CONTROL REPORT - SANDS OF DUAT ASSETS

## PHASE 8: Asset Quality Assessment Results

### Overall Statistics
- **Total Assets Processed**: {total_assets}
- **Passed Quality Control**: {total_passed} ({success_rate:.1f}%)
- **Failed Quality Control**: {total_failed} ({100-success_rate:.1f}%)

### Quality Standards Applied
- Minimum Resolution: {self.quality_standards['min_resolution']}
- File Size Range: {self.quality_standards['min_file_size']//1000}KB - {self.quality_standards['max_file_size']//1000000}MB
- Required Formats: {', '.join(self.quality_standards['required_formats'])}
- Minimum Color Diversity: {self.quality_standards['min_color_diversity']} unique colors
- Brightness Range: {self.quality_standards['brightness_range']}

### Category Breakdown
"""
        
        for result in all_results:
            category = result["category"]
            passed = result["passed"] 
            failed = result["failed"]
            total = result["total_assets"]
            rate = (passed / total * 100) if total > 0 else 0
            
            report_content += f"""
#### {category.upper()}
- Total: {total} assets
- Passed: {passed} ({rate:.1f}%)
- Failed: {failed} ({100-rate:.1f}%)
"""
        
        # Common issues summary
        all_issues = []
        for result in all_results:
            for asset in result["assets"]:
                if not asset["evaluation"]["passed"]:
                    all_issues.extend(asset["evaluation"]["issues"])
        
        issue_counts = {}
        for issue in all_issues:
            issue_type = issue.split(":")[0]
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        if issue_counts:
            report_content += "\n### Most Common Issues\n"
            for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
                report_content += f"- {issue_type}: {count} occurrences\n"
        
        report_content += f"""
### Recommended Actions
{'**All assets passed quality control!** Ready for game integration.' if total_failed == 0 else f'''
**{total_failed} assets failed quality control** and need regeneration:

1. Review failed assets in `{self.rejected_dir}`
2. Identify common issues and adjust generation parameters
3. Regenerate failed assets with improved prompts/settings
4. Re-run quality control until all assets pass
'''}

### File Locations
- **Approved Assets**: `{self.approved_dir}`
- **Rejected Assets**: `{self.rejected_dir}`  
- **Quality Reports**: `{self.reports_dir}`

---
Generated by Quality Control System v1.0
"""
        
        # Save report
        report_path = self.reports_dir / "quality_control_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Save detailed JSON report
        json_report_path = self.reports_dir / "detailed_quality_report.json"
        with open(json_report_path, 'w') as f:
            json.dump({
                "summary": {
                    "total_assets": total_assets,
                    "passed": total_passed,
                    "failed": total_failed,
                    "success_rate": success_rate
                },
                "categories": all_results,
                "quality_standards": self.quality_standards
            }, f, indent=2)
        
        print(f"Quality reports generated:")
        print(f"  - Summary: {report_path}")
        print(f"  - Detailed: {json_report_path}")

    def run_quality_control(self):
        """Execute PHASE 8: Quality Control."""
        print("=" * 60)
        print("PHASE 8: QUALITY CONTROL SYSTEM")
        print("Reviewing all generated assets for AAA standards")
        print("=" * 60)
        
        if not self.assets_dir.exists():
            print(f"Assets directory not found: {self.assets_dir}")
            print("Please run PHASE 7 (Batch Asset Generation) first")
            return
        
        all_results = []
        
        # Process each category
        for category_dir in self.assets_dir.iterdir():
            if category_dir.is_dir():
                result = self.process_asset_category(category_dir)
                all_results.append(result)
        
        # Generate comprehensive report
        self.generate_quality_report(all_results)
        
        total_assets = sum(result["total_assets"] for result in all_results)
        total_passed = sum(result["passed"] for result in all_results)
        
        print("=" * 60)
        print("PHASE 8 COMPLETE: QUALITY CONTROL FINISHED!")
        print(f"Results: {total_passed}/{total_assets} assets passed quality control")
        print("Ready for PHASE 9: Game Integration")
        print("=" * 60)

def main():
    qc = QualityControlSystem()
    qc.run_quality_control()

if __name__ == "__main__":
    main()