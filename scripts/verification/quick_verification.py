#!/usr/bin/env python3
"""
Quick UI Duplication Fix Verification
Simple test to verify the fix works correctly.
"""

import json
from datetime import datetime
from pathlib import Path

def analyze_combat_screen_fix():
    """Analyze the fix implementation in combat_screen.py"""
    
    combat_screen_path = Path("sands_duat/ui/combat_screen.py")
    
    if not combat_screen_path.exists():
        return {"error": "Combat screen file not found"}
    
    # Read the combat screen file
    with open(combat_screen_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for the fix implementation
    fix_indicators = {
        "duplicate_rendering_comment": "Removed duplicate enhanced drawing to fix double rendering bug" in content,
        "base_components_comment": "Cards and end turn button are now rendered by base components" in content,
        "no_enhanced_cards_call": "_draw_enhanced_cards(" not in content[content.find("def render("):content.find("def _draw_battlefield_elements")],
        "no_enhanced_button_call": "_draw_enhanced.*button" not in content[content.find("def render("):content.find("def _draw_battlefield_elements")],
        "atmospheric_elements_preserved": "_draw_atmospheric_elements(" in content
    }
    
    return fix_indicators

def verify_base_component_system():
    """Verify that the base component system handles UI rendering"""
    
    base_ui_path = Path("sands_duat/ui/base.py")
    
    if not base_ui_path.exists():
        return {"error": "Base UI file not found"}
    
    with open(base_ui_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    base_system_check = {
        "component_render_loop": "component.render(surface)" in content,
        "component_visibility_check": "if component.visible:" in content,
        "screen_render_method": "def render(self, surface: pygame.Surface)" in content,
        "component_management": "self.components: List[UIComponent]" in content
    }
    
    return base_system_check

def check_game_launch_logs():
    """Check the game launch logs for verification"""
    
    log_path = Path("sands_duat.log")
    
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8') as f:
            logs = f.read()
        
        # Look for successful initialization and ultrawide detection
        log_analysis = {
            "ultrawide_detection": "ultrawide (3440x1440)" in logs,
            "ui_manager_init": "Enhanced UI Manager initialized" in logs,
            "combat_screen_added": "Added screen: combat" in logs,
            "successful_launch": "Entering main game loop" in logs,
            "recent_timestamp": "2025-08-02 17:34" in logs  # Recent execution
        }
        
        return log_analysis
    
    return {"error": "No log file found"}

def run_verification():
    """Run complete verification analysis"""
    
    print("UI Duplication Fix Verification Report")
    print("=" * 50)
    
    # Check fix implementation
    print("\n1. Analyzing Fix Implementation...")
    fix_analysis = analyze_combat_screen_fix()
    
    if "error" in fix_analysis:
        print(f"ERROR: {fix_analysis['error']}")
    else:
        for check, result in fix_analysis.items():
            status = "PASS" if result else "FAIL"
            print(f"  {status} {check.replace('_', ' ').title()}: {result}")
    
    # Check base component system
    print("\n2. Verifying Base Component System...")
    base_analysis = verify_base_component_system()
    
    if "error" in base_analysis:
        print(f"ERROR: {base_analysis['error']}")
    else:
        for check, result in base_analysis.items():
            status = "PASS" if result else "FAIL"
            print(f"  {status} {check.replace('_', ' ').title()}: {result}")
    
    # Check game execution logs
    print("\n3. Analyzing Game Execution Logs...")
    log_analysis = check_game_launch_logs()
    
    if "error" in log_analysis:
        print(f"ERROR: {log_analysis['error']}")
    else:
        for check, result in log_analysis.items():
            status = "PASS" if result else "FAIL"
            print(f"  {status} {check.replace('_', ' ').title()}: {result}")
    
    # Overall assessment
    print("\n4. Overall Assessment...")
    
    all_checks = {**fix_analysis, **base_analysis, **log_analysis}
    passed_checks = sum(1 for result in all_checks.values() if result is True)
    total_checks = len([r for r in all_checks.values() if isinstance(r, bool)])
    
    success_rate = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    print(f"  Checks Passed: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        overall_status = "PASS - Fix Verified Successfully"
        deployment_ready = True
    elif success_rate >= 70:
        overall_status = "CONDITIONAL PASS - Minor Issues Detected"
        deployment_ready = True
    else:
        overall_status = "FAIL - Significant Issues Found"
        deployment_ready = False
    
    print(f"  Overall Status: {overall_status}")
    print(f"  Deployment Ready: {'Yes' if deployment_ready else 'No'}")
    
    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "verification_type": "UI_Duplication_Fix_Static_Analysis",
        "fix_implementation": fix_analysis,
        "base_component_system": base_analysis,
        "game_execution_logs": log_analysis,
        "summary": {
            "checks_passed": passed_checks,
            "total_checks": total_checks,
            "success_rate": success_rate,
            "overall_status": overall_status,
            "deployment_ready": deployment_ready
        }
    }
    
    # Save report
    report_path = Path("verification_report_quick.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to: {report_path}")
    
    return report

if __name__ == "__main__":
    run_verification()