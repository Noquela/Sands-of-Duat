#!/usr/bin/env python3
"""
QUALITY DASHBOARD - FASE 6
===========================
Dashboard em tempo real para monitorar qualidade, aprovações
e status de produção dos assets Hades-Egyptian.
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict, Counter

class QualityDashboard:
    def __init__(self):
        self.base_dir = Path(".")
        self.qa_dir = self.base_dir / "quality_assurance"
        self.results_dir = self.qa_dir / "results"
        self.workflow_dir = self.qa_dir / "approval_workflow"
        self.production_ready = self.workflow_dir / "production_ready"
        
        # Dashboard state
        self.dashboard_data = {
            "last_update": None,
            "total_assets_analyzed": 0,
            "quality_summary": {},
            "approval_summary": {},
            "production_status": {},
            "trend_data": [],
            "issues_analysis": {},
            "recommendations": []
        }
        
        self.update_interval = 30  # seconds
        
    def scan_quality_results(self) -> Dict:
        """Escaneia resultados de quality control mais recentes."""
        
        if not self.results_dir.exists():
            return {"error": "Quality results directory not found"}
        
        # Find latest results files
        result_files = list(self.results_dir.glob("quality_analysis_*.json"))
        
        if not result_files:
            return {"warning": "No quality analysis results found"}
        
        # Sort by modification time to get most recent
        result_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Load and aggregate recent results
        aggregated_results = []
        processed_assets = set()
        
        # Process up to 5 most recent files to avoid duplicates
        for result_file in result_files[:5]:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    batch_data = json.load(f)
                
                for result in batch_data.get("results", []):
                    asset_id = result.get("asset_id", "unknown")
                    
                    # Avoid duplicates (keep most recent)
                    if asset_id not in processed_assets:
                        aggregated_results.append(result)
                        processed_assets.add(asset_id)
                        
            except Exception as e:
                print(f"Warning: Could not load {result_file}: {e}")
        
        return {
            "total_results": len(aggregated_results),
            "results": aggregated_results,
            "files_processed": len(result_files),
            "latest_file": str(result_files[0]) if result_files else None
        }
    
    def scan_approval_workflow(self) -> Dict:
        """Escaneia status do workflow de aprovação."""
        
        workflow_status = {
            "approved_professional": 0,
            "approved_standard": 0,
            "needs_review": 0,
            "rejected": 0,
            "production_ready_by_rarity": {}
        }
        
        # Scan tier directories
        tier_dirs = {
            "approved_professional": self.workflow_dir / "approved" / "professional_tier",
            "approved_standard": self.workflow_dir / "approved" / "standard_tier",
            "needs_review": self.workflow_dir / "manual_review" / "needs_improvement",
            "rejected": self.workflow_dir / "rejected" / "quality_issues"
        }
        
        for status, directory in tier_dirs.items():
            if directory.exists():
                png_count = len(list(directory.glob("*.png")))
                workflow_status[status] = png_count
        
        # Scan production-ready by rarity
        rarity_dirs = {
            "legendary": self.production_ready / "legendary_assets",
            "epic": self.production_ready / "epic_assets", 
            "rare": self.production_ready / "rare_assets",
            "common": self.production_ready / "common_assets"
        }
        
        for rarity, directory in rarity_dirs.items():
            if directory.exists():
                assets = list(directory.glob("*.png"))
                workflow_status["production_ready_by_rarity"][rarity] = {
                    "count": len(assets),
                    "professional_tier": len([a for a in assets if "professional" in a.name.lower()]),
                    "standard_tier": len([a for a in assets if "standard" in a.name.lower()])
                }
        
        return workflow_status
    
    def analyze_quality_trends(self, quality_data: List[Dict]) -> Dict:
        """Analisa tendências de qualidade ao longo do tempo."""
        
        if not quality_data:
            return {"error": "No quality data available for trend analysis"}
        
        # Group by rarity
        by_rarity = defaultdict(list)
        for result in quality_data:
            rarity = result.get("rarity", "common")
            score = result.get("overall_score", 0.0)
            by_rarity[rarity].append(score)
        
        # Calculate statistics by rarity
        trend_analysis = {}
        for rarity, scores in by_rarity.items():
            if scores:
                trend_analysis[rarity] = {
                    "count": len(scores),
                    "average_score": sum(scores) / len(scores),
                    "min_score": min(scores),
                    "max_score": max(scores),
                    "above_threshold": len([s for s in scores if s >= 0.80])
                }
        
        # Overall trend
        all_scores = [result.get("overall_score", 0.0) for result in quality_data]
        if all_scores:
            trend_analysis["overall"] = {
                "total_assets": len(all_scores),
                "average_quality": sum(all_scores) / len(all_scores),
                "quality_distribution": {
                    "excellent": len([s for s in all_scores if s >= 0.90]),
                    "good": len([s for s in all_scores if 0.80 <= s < 0.90]),
                    "fair": len([s for s in all_scores if 0.70 <= s < 0.80]),
                    "poor": len([s for s in all_scores if s < 0.70])
                }
            }
        
        return trend_analysis
    
    def analyze_common_issues(self, quality_data: List[Dict]) -> Dict:
        """Analisa problemas mais comuns identificados."""
        
        all_critical_issues = []
        all_minor_issues = []
        
        for result in quality_data:
            all_critical_issues.extend(result.get("critical_issues", []))
            all_minor_issues.extend(result.get("minor_issues", []))
        
        # Count issue frequency
        critical_counter = Counter(all_critical_issues)
        minor_counter = Counter(all_minor_issues)
        
        return {
            "critical_issues": {
                "total_count": len(all_critical_issues),
                "unique_types": len(critical_counter),
                "most_common": critical_counter.most_common(5)
            },
            "minor_issues": {
                "total_count": len(all_minor_issues),
                "unique_types": len(minor_counter),
                "most_common": minor_counter.most_common(5)
            }
        }
    
    def generate_recommendations(self, quality_data: List[Dict], workflow_data: Dict, 
                               trend_data: Dict) -> List[str]:
        """Gera recomendações baseadas nos dados de qualidade."""
        
        recommendations = []
        
        # Check overall quality performance
        overall_stats = trend_data.get("overall", {})
        if overall_stats:
            avg_quality = overall_stats.get("average_quality", 0.0)
            
            if avg_quality < 0.75:
                recommendations.append("🚨 CRITICAL: Overall quality below target (75%). Review generation parameters.")
            elif avg_quality < 0.85:
                recommendations.append("⚠️ Quality improvement needed. Focus on Hades style compliance.")
            else:
                recommendations.append("✅ Quality performance is good. Maintain current standards.")
        
        # Check production readiness
        total_approved = workflow_data.get("approved_professional", 0) + workflow_data.get("approved_standard", 0)
        total_processed = sum(workflow_data.get(k, 0) for k in ["approved_professional", "approved_standard", "needs_review", "rejected"])
        
        if total_processed > 0:
            approval_rate = total_approved / total_processed * 100
            
            if approval_rate < 70:
                recommendations.append("🔥 Low approval rate detected. Review generation prompts and quality thresholds.")
            elif approval_rate < 85:
                recommendations.append("📈 Moderate approval rate. Consider minor prompt enhancements.")
            else:
                recommendations.append("🎯 Excellent approval rate! System performing well.")
        
        # Check rarity distribution
        production_ready = workflow_data.get("production_ready_by_rarity", {})
        
        for rarity in ["legendary", "epic", "rare", "common"]:
            rarity_data = production_ready.get(rarity, {})
            count = rarity_data.get("count", 0)
            
            if rarity == "legendary" and count < 15:
                recommendations.append(f"👑 Need more {rarity} assets for complete legendary collection.")
            elif rarity == "epic" and count < 20:
                recommendations.append(f"⚔️ Epic assets count is low. Consider prioritizing epic generation.")
        
        # Check for specific quality issues
        if len(recommendations) < 3:
            recommendations.append("🎨 System running smoothly. Consider generating additional variations for variety.")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def update_dashboard_data(self):
        """Atualiza todos os dados do dashboard."""
        
        print("Updating dashboard data...")
        
        # Scan quality results
        quality_scan = self.scan_quality_results()
        
        # Scan approval workflow
        workflow_scan = self.scan_approval_workflow()
        
        # Analyze trends and issues
        quality_data = quality_scan.get("results", [])
        trend_analysis = self.analyze_quality_trends(quality_data)
        issues_analysis = self.analyze_common_issues(quality_data)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(quality_data, workflow_scan, trend_analysis)
        
        # Update dashboard state
        self.dashboard_data.update({
            "last_update": datetime.now().isoformat(),
            "total_assets_analyzed": quality_scan.get("total_results", 0),
            "quality_summary": trend_analysis,
            "approval_summary": workflow_scan,
            "issues_analysis": issues_analysis,
            "recommendations": recommendations
        })
    
    def display_dashboard(self):
        """Exibe dashboard em tempo real."""
        
        # Clear screen (works on most terminals)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 70)
        print("QUALITY CONTROL DASHBOARD - FASE 6")
        print("Hades-Egyptian Asset Quality Monitoring")
        print("=" * 70)
        
        # Current time and last update
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_update = self.dashboard_data.get("last_update")
        if last_update:
            last_update_time = datetime.fromisoformat(last_update).strftime("%H:%M:%S")
        else:
            last_update_time = "Never"
        
        print(f"Current Time: {current_time}")
        print(f"Last Update: {last_update_time}")
        print()
        
        # Overall statistics
        total_analyzed = self.dashboard_data.get("total_assets_analyzed", 0)
        print(f"📊 OVERALL STATUS:")
        print(f"Total Assets Analyzed: {total_analyzed}")
        
        # Quality summary
        quality_summary = self.dashboard_data.get("quality_summary", {})
        overall_stats = quality_summary.get("overall", {})
        
        if overall_stats:
            avg_quality = overall_stats.get("average_quality", 0.0)
            quality_dist = overall_stats.get("quality_distribution", {})
            
            print(f"Average Quality Score: {avg_quality:.2f}/1.00")
            print()
            
            print(f"🎯 QUALITY DISTRIBUTION:")
            print(f"Excellent (≥0.90): {quality_dist.get('excellent', 0)} assets")
            print(f"Good (0.80-0.89):  {quality_dist.get('good', 0)} assets")
            print(f"Fair (0.70-0.79):  {quality_dist.get('fair', 0)} assets")
            print(f"Poor (<0.70):      {quality_dist.get('poor', 0)} assets")
            print()
        
        # Approval workflow status
        approval_summary = self.dashboard_data.get("approval_summary", {})
        
        print(f"✅ APPROVAL WORKFLOW STATUS:")
        print(f"Professional Tier: {approval_summary.get('approved_professional', 0)} assets")
        print(f"Standard Approved: {approval_summary.get('approved_standard', 0)} assets")
        print(f"Needs Review:      {approval_summary.get('needs_review', 0)} assets")
        print(f"Rejected:          {approval_summary.get('rejected', 0)} assets")
        print()
        
        # Production ready status
        production_ready = approval_summary.get("production_ready_by_rarity", {})
        
        if production_ready:
            print(f"🎮 PRODUCTION READY ASSETS:")
            for rarity, data in production_ready.items():
                count = data.get("count", 0)
                professional = data.get("professional_tier", 0)
                standard = data.get("standard_tier", 0)
                
                print(f"{rarity.title():>10}: {count:>3} assets (Prof: {professional}, Std: {standard})")
            print()
        
        # Issues analysis
        issues_analysis = self.dashboard_data.get("issues_analysis", {})
        
        critical_issues = issues_analysis.get("critical_issues", {})
        if critical_issues.get("most_common"):
            print(f"🚨 TOP CRITICAL ISSUES:")
            for issue, count in critical_issues["most_common"][:3]:
                print(f"  • {issue}: {count} occurrences")
            print()
        
        # Recommendations
        recommendations = self.dashboard_data.get("recommendations", [])
        if recommendations:
            print(f"💡 RECOMMENDATIONS:")
            for rec in recommendations[:3]:
                print(f"  {rec}")
            print()
        
        # Performance indicators
        if total_analyzed > 0:
            total_approved = approval_summary.get("approved_professional", 0) + approval_summary.get("approved_standard", 0)
            approval_rate = total_approved / total_analyzed * 100
            
            print(f"📈 KEY METRICS:")
            print(f"Approval Rate: {approval_rate:.1f}%")
            
            professional_rate = approval_summary.get("approved_professional", 0) / total_analyzed * 100
            print(f"Professional Rate: {professional_rate:.1f}%")
            
            # Status indicator
            if approval_rate >= 85:
                status = "🟢 EXCELLENT"
            elif approval_rate >= 70:
                status = "🟡 GOOD"
            elif approval_rate >= 50:
                status = "🟠 NEEDS IMPROVEMENT"
            else:
                status = "🔴 CRITICAL"
            
            print(f"System Status: {status}")
        
        print("=" * 70)
        print("Press Ctrl+C to stop monitoring")
    
    def start_monitoring(self):
        """Inicia monitoramento em tempo real."""
        
        print("Starting quality monitoring...")
        print("Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                # Update data
                self.update_dashboard_data()
                
                # Display dashboard
                self.display_dashboard()
                
                # Wait for next update
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            print("\n\nQuality monitoring stopped.")
            self.save_dashboard_snapshot()
    
    def save_dashboard_snapshot(self):
        """Salva snapshot dos dados do dashboard."""
        
        snapshot_file = self.qa_dir / f"dashboard_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(snapshot_file, 'w', encoding='utf-8') as f:
                json.dump(self.dashboard_data, f, indent=2, ensure_ascii=False)
            
            print(f"Dashboard snapshot saved: {snapshot_file}")
            
        except Exception as e:
            print(f"Failed to save dashboard snapshot: {e}")
    
    def generate_status_report(self) -> str:
        """Gera relatório de status para compartilhamento."""
        
        # Update data first
        self.update_dashboard_data()
        
        total_analyzed = self.dashboard_data.get("total_assets_analyzed", 0)
        approval_summary = self.dashboard_data.get("approval_summary", {})
        quality_summary = self.dashboard_data.get("quality_summary", {})
        
        total_approved = approval_summary.get("approved_professional", 0) + approval_summary.get("approved_standard", 0)
        approval_rate = total_approved / max(total_analyzed, 1) * 100
        
        overall_stats = quality_summary.get("overall", {})
        avg_quality = overall_stats.get("average_quality", 0.0)
        
        report = f"""
# QUALITY DASHBOARD STATUS REPORT

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Key Metrics
- **Assets Analyzed:** {total_analyzed}
- **Approval Rate:** {approval_rate:.1f}%
- **Average Quality:** {avg_quality:.2f}/1.00
- **Production Ready:** {total_approved} assets

## Production Status
"""
        
        production_ready = approval_summary.get("production_ready_by_rarity", {})
        for rarity, data in production_ready.items():
            count = data.get("count", 0)
            report += f"- **{rarity.title()}:** {count} assets ready\n"
        
        report += f"""

## Quality Performance
{'🟢 EXCELLENT' if approval_rate >= 85 else '🟡 GOOD' if approval_rate >= 70 else '🟠 NEEDS IMPROVEMENT' if approval_rate >= 50 else '🔴 CRITICAL'}

## Recommendations
"""
        
        for rec in self.dashboard_data.get("recommendations", [])[:3]:
            report += f"- {rec}\n"
        
        return report

def main():
    """Execução principal do dashboard de qualidade."""
    
    dashboard = QualityDashboard()
    
    print("QUALITY CONTROL DASHBOARD - FASE 6")
    print("=" * 36)
    print("1. Start real-time monitoring")
    print("2. Show current status")
    print("3. Generate status report")
    print("4. Save dashboard snapshot")
    print("0. Exit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        dashboard.start_monitoring()
    
    elif choice == "2":
        dashboard.update_dashboard_data()
        dashboard.display_dashboard()
        input("\nPress Enter to continue...")
    
    elif choice == "3":
        report = dashboard.generate_status_report()
        print(report)
        
        # Save report
        report_file = dashboard.qa_dir / f"status_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\nReport saved: {report_file}")
        except Exception as e:
            print(f"Failed to save report: {e}")
    
    elif choice == "4":
        dashboard.update_dashboard_data()
        dashboard.save_dashboard_snapshot()

if __name__ == "__main__":
    main()