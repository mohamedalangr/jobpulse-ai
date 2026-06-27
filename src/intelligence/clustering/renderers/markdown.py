import os
from typing import Dict
from src.intelligence.clustering.summaries import ClusterAnalysisReport
from src.intelligence.clustering.labeling import ClusterLabel

class MarketReportGenerator:
    def render(self, 
               report: ClusterAnalysisReport, 
               labels: Dict[int, ClusterLabel], 
               output_path: str) -> None:
        """
        Renders the cluster summaries and labels into a clean Markdown document.
        """
        lines = []
        lines.append("# Semantic Market Discovery Report")
        lines.append("")
        
        for summary in report.summaries:
            cluster_label = labels.get(summary.cluster_id)
            title = cluster_label.label if cluster_label else f"Cluster {summary.cluster_id}"
            
            lines.append(f"## {title}")
            lines.append(f"**Size**: {summary.size} jobs | **Remote Ratio**: {summary.remote_ratio * 100:.1f}%")
            if summary.median_salary:
                lines.append(f"**Median Salary**: ${summary.median_salary:,.0f}")
            else:
                lines.append("**Median Salary**: Unknown")
                
            lines.append("")
            
            if summary.top_skills:
                lines.append(f"**Top Skills**: {', '.join(summary.top_skills)}")
            
            if summary.top_companies:
                lines.append(f"**Top Companies**: {', '.join(summary.top_companies)}")
                
            lines.append("")
            if summary.representative_jobs:
                lines.append("**Representative Jobs:**")
                for rj in summary.representative_jobs:
                    lines.append(f"- {rj}")
                    
            lines.append("---")
            lines.append("")
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
