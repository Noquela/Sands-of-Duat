#!/usr/bin/env python3
"""
MASTER QUALITY CONTROL INTERFACE - FASE 6
==========================================
Interface unificada para todos os sistemas de quality control extremo.
"""

import os
import sys
from pathlib import Path

def show_main_menu():
    """Display main quality control menu."""
    print("EXTREME QUALITY CONTROL SYSTEM - FASE 6")
    print("=" * 42)
    print("Professional Hades-Egyptian Asset Quality Control")
    print()
    print("QUALITY ANALYSIS:")
    print("1. Run Extreme Quality Control Analysis")
    print("2. Process Quality Results with Auto-Approval")
    print("3. Real-Time Quality Dashboard")
    print()
    print("WORKFLOW MANAGEMENT:")
    print("4. Show Approval Workflow Status")
    print("5. Create Production Manifest")
    print("6. Generate Comprehensive Quality Report")
    print()
    print("UTILITIES:")
    print("7. Show System Status")
    print("8. Open Quality Assurance Directory")
    print("9. Show FASE 6 Usage Guide")
    print("0. Exit")
    
    return input("\nSelect option: ").strip()

def run_extreme_quality_control():
    """Run extreme quality control analysis."""
    print("\nEXTREME QUALITY CONTROL ANALYSIS")
    print("=" * 33)
    
    print("This will perform comprehensive quality analysis with:")
    print("- Technical quality assessment")
    print("- Hades style compliance check")
    print("- Egyptian authenticity verification")
    print("- Consistency analysis")
    print("- Advanced metrics calculation")
    print()
    
    directory = input("Enter assets directory for analysis: ").strip()
    if directory and Path(directory).exists():
        print(f"\nRunning quality analysis on: {directory}")
        os.system(f"python extreme_quality_control.py")
    else:
        print("Invalid directory! Please ensure the path exists.")

def run_automated_approval():
    """Run automated approval system."""
    print("\nAUTOMATED APPROVAL WORKFLOW")
    print("=" * 27)
    
    print("This will process quality results and organize assets by:")
    print("- Professional tier (95%+ quality)")
    print("- Standard approved (80%+ quality)")
    print("- Needs review (70%+ quality)")
    print("- Rejected (below standards)")
    print()
    
    results_file = input("Enter quality results file path: ").strip()
    if results_file and Path(results_file).exists():
        print(f"\nProcessing results: {results_file}")
        os.system(f"python automated_approval_system.py")
    else:
        print("Results file not found! Run quality analysis first.")

def run_quality_dashboard():
    """Run quality dashboard."""
    print("\nSTARTING QUALITY DASHBOARD")
    print("=" * 26)
    
    print("Real-time monitoring will show:")
    print("- Overall quality statistics")
    print("- Approval workflow status") 
    print("- Production readiness metrics")
    print("- Issue analysis and recommendations")
    print()
    
    confirm = input("Start real-time monitoring? (y/n): ").lower()
    if confirm == 'y':
        os.system("python quality_dashboard.py")

def show_workflow_status():
    """Show current approval workflow status."""
    print("\nAPPROVAL WORKFLOW STATUS")
    print("=" * 24)
    
    workflow_dir = Path("approval_workflow")
    
    if not workflow_dir.exists():
        print("Workflow directory not found. Run quality analysis first.")
        return
    
    # Check each workflow stage
    stages = {
        "Professional Tier": workflow_dir / "approved" / "professional_tier",
        "Standard Approved": workflow_dir / "approved" / "standard_tier",
        "Needs Review": workflow_dir / "manual_review" / "needs_improvement",
        "Rejected": workflow_dir / "rejected" / "quality_issues"
    }
    
    total_assets = 0
    for stage, directory in stages.items():
        if directory.exists():
            count = len(list(directory.glob("*.png")))
            total_assets += count
            status = "✅" if count > 0 else "⚪"
            print(f"{status} {stage}: {count} assets")
    
    print(f"\nTotal assets in workflow: {total_assets}")
    
    # Check production ready
    production_dir = workflow_dir / "production_ready"
    if production_dir.exists():
        rarity_counts = {}
        for rarity in ["legendary", "epic", "rare", "common"]:
            rarity_dir = production_dir / f"{rarity}_assets"
            if rarity_dir.exists():
                count = len(list(rarity_dir.glob("*.png")))
                rarity_counts[rarity] = count
        
        if rarity_counts:
            print(f"\nPRODUCTION READY ASSETS:")
            for rarity, count in rarity_counts.items():
                print(f"  {rarity.title()}: {count} assets")

def create_production_manifest():
    """Create production manifest."""
    print("\nCREATING PRODUCTION MANIFEST")
    print("=" * 28)
    
    print("This will create a comprehensive manifest of all production-ready assets")
    print("organized by rarity and quality tier for game integration.")
    print()
    
    confirm = input("Create production manifest? (y/n): ").lower()
    if confirm == 'y':
        # Run the automated approval system with manifest creation
        from automated_approval_system import AutomatedApprovalSystem
        
        try:
            system = AutomatedApprovalSystem()
            manifest = system.create_production_manifest()
            
            if manifest:
                total = manifest.get("quality_certification", {}).get("total_production_ready_assets", 0)
                print(f"\n✅ Production manifest created successfully!")
                print(f"Total production-ready assets: {total}")
                print(f"Manifest location: approval_workflow/production_ready/PRODUCTION_MANIFEST.json")
            else:
                print("❌ Failed to create production manifest.")
        
        except Exception as e:
            print(f"Error creating manifest: {e}")

def generate_comprehensive_report():
    """Generate comprehensive quality report."""
    print("\nGENERATING COMPREHENSIVE QUALITY REPORT")
    print("=" * 39)
    
    results_dir = Path("results")
    if not results_dir.exists() or not list(results_dir.glob("*.json")):
        print("No quality analysis results found.")
        print("Run quality analysis first to generate reports.")
        return
    
    print("Generating comprehensive report from all available quality data...")
    
    try:
        from extreme_quality_control import ExtremeQualityController
        
        controller = ExtremeQualityController()
        
        # Find all result files
        result_files = list(results_dir.glob("quality_analysis_*.json"))
        batch_results = []
        
        for result_file in result_files:
            try:
                import json
                with open(result_file, 'r', encoding='utf-8') as f:
                    batch_data = json.load(f)
                    batch_results.append(batch_data)
            except Exception as e:
                print(f"Warning: Could not load {result_file}: {e}")
        
        if batch_results:
            report = controller.generate_comprehensive_report(batch_results)
            
            # Save report
            from datetime import datetime
            report_file = Path(f"comprehensive_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"\n✅ Comprehensive report generated: {report_file}")
            print("Report includes:")
            print("- Executive summary")
            print("- Quality metrics analysis") 
            print("- Issue analysis and recommendations")
            print("- Production readiness certification")
        else:
            print("❌ No valid quality data found for reporting.")
    
    except Exception as e:
        print(f"Error generating report: {e}")

def show_system_status():
    """Show overall system status."""
    print("\nSYSTEM STATUS - FASE 6")
    print("=" * 22)
    
    # Check system components
    components = {
        "Extreme Quality Control": Path("extreme_quality_control.py"),
        "Automated Approval System": Path("automated_approval_system.py"),
        "Quality Dashboard": Path("quality_dashboard.py"),
        "Quality Results": Path("results"),
        "Approval Workflow": Path("approval_workflow"),
        "Production Ready": Path("approval_workflow/production_ready")
    }
    
    print("SYSTEM COMPONENTS:")
    for component, path in components.items():
        if path.exists():
            status = "✅ READY"
            if path.is_dir():
                file_count = len(list(path.rglob("*.*")))
                status += f" ({file_count} files)" if file_count > 0 else " (empty)"
        else:
            status = "❌ MISSING"
        
        print(f"  {component}: {status}")
    
    # Check for recent activity
    results_dir = Path("results")
    if results_dir.exists():
        recent_files = sorted(results_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        if recent_files:
            from datetime import datetime
            latest = recent_files[0]
            mod_time = datetime.fromtimestamp(latest.stat().st_mtime)
            print(f"\nLast quality analysis: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Results file: {latest.name}")
    
    print(f"\nSYSTEM STATUS: {'🟢 OPERATIONAL' if all(p.exists() for p in components.values()[:3]) else '🟡 PARTIAL'}")

def open_qa_directory():
    """Open quality assurance directory."""
    qa_dir = Path(".")
    
    if qa_dir.exists():
        print(f"\nOpening Quality Assurance directory: {qa_dir.resolve()}")
        
        # Try to open with system default file manager
        import subprocess
        import platform
        
        try:
            if platform.system() == "Windows":
                subprocess.run(['explorer', str(qa_dir.resolve())])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', str(qa_dir.resolve())])
            else:  # Linux
                subprocess.run(['xdg-open', str(qa_dir.resolve())])
        except Exception as e:
            print(f"Could not open directory: {e}")
            print(f"Directory path: {qa_dir.resolve()}")
    else:
        print("Quality assurance directory not found!")

def show_usage_guide():
    """Show FASE 6 usage guide."""
    print("\nFASE 6 - EXTREME QUALITY CONTROL USAGE GUIDE")
    print("=" * 45)
    
    guide = """
WORKFLOW OVERVIEW:
1. Run quality analysis on generated assets
2. Process results through automated approval
3. Monitor progress with real-time dashboard
4. Create production manifest for integration

DETAILED STEPS:

STEP 1: Quality Analysis
- Use option 1 to analyze asset directories
- System performs comprehensive quality checks:
  * Technical quality (resolution, format, file size)
  * Hades style compliance (pen & ink, chiaroscuro, proportions)
  * Egyptian authenticity (mythology, architecture, symbolism)
  * Consistency analysis across similar assets
  * Advanced metrics for professional assessment

STEP 2: Automated Approval
- Use option 2 to process quality results
- Assets automatically organized into:
  * Professional Tier (95%+ quality)
  * Standard Approved (80%+ quality) 
  * Needs Review (70%+ quality)
  * Rejected (below standards)

STEP 3: Monitor Progress
- Use option 3 for real-time dashboard
- Shows approval rates, quality trends, common issues
- Provides actionable recommendations

STEP 4: Production Ready
- Use option 5 to create production manifest
- Assets organized by rarity for game integration
- Quality certification included

QUALITY THRESHOLDS:
- Legendary: 95% minimum (professional tier: 98%)
- Epic: 90% minimum (professional tier: 95%)
- Rare: 85% minimum (professional tier: 90%)
- Common: 80% minimum (professional tier: 85%)

SUCCESS METRICS:
- Target: 80%+ approval rate overall
- Goal: 60%+ professional tier rate
- Standard: Consistent Hades-Egyptian fusion style
"""
    
    print(guide)

def main():
    """Main quality control interface."""
    
    # Ensure we're in the quality_assurance directory
    current_dir = Path.cwd()
    if not current_dir.name == "quality_assurance":
        qa_dir = current_dir / "quality_assurance"
        if qa_dir.exists():
            os.chdir(qa_dir)
        else:
            print("Quality assurance directory not found!")
            print(f"Current directory: {current_dir}")
            print("Please run from art_pipeline/quality_assurance/")
            return
    
    print("FASE 6 - EXTREME QUALITY CONTROL SYSTEM")
    print("=" * 41)
    print("Professional Hades-Egyptian Asset Quality Control")
    print(f"Working directory: {Path.cwd()}")
    print()
    
    while True:
        choice = show_main_menu()
        
        if choice == "0":
            print("Quality control system closed.")
            break
        elif choice == "1":
            run_extreme_quality_control()
        elif choice == "2":
            run_automated_approval()
        elif choice == "3":
            run_quality_dashboard()
        elif choice == "4":
            show_workflow_status()
        elif choice == "5":
            create_production_manifest()
        elif choice == "6":
            generate_comprehensive_report()
        elif choice == "7":
            show_system_status()
        elif choice == "8":
            open_qa_directory()
        elif choice == "9":
            show_usage_guide()
        else:
            print("Invalid option!")
        
        if choice != "3":  # Dashboard has its own loop
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()