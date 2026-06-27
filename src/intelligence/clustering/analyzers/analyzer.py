from collections import Counter
import numpy as np
from src.intelligence.clustering.dataset import ClusterDataset
from src.intelligence.clustering.summaries import ClusterSummary, ClusterAnalysisReport
from src.intelligence.semantic_search.service import JobFetcher

class ClusterAnalyzer:
    def __init__(self, fetcher: JobFetcher):
        self.fetcher = fetcher

    def analyze(self, dataset: ClusterDataset) -> ClusterAnalysisReport:
        unique_clusters = set(dataset.assignments)
        summaries = []
        
        for cluster_id in unique_clusters:
            if cluster_id == -1:
                continue # Skip noise
                
            idx = np.where(dataset.assignments == cluster_id)[0]
            cluster_embeddings = dataset.base_dataset.embeddings[idx]
            cluster_fingerprints = [dataset.base_dataset.fingerprints[i] for i in idx]
            
            # Fetch jobs
            jobs = []
            for fp in cluster_fingerprints:
                job = self.fetcher.get_by_fingerprint(fp)
                if job:
                    jobs.append(job)
                    
            if not jobs:
                continue
                
            # Aggregate stats
            size = len(jobs)
            
            # Simple salary median logic
            salaries = []
            for j in jobs:
                if j.raw_data and isinstance(j.raw_data, dict):
                    # Check for explicit salary or min/max
                    sal = j.raw_data.get('salary_max')
                    if sal: salaries.append(float(sal))
                    
            median_salary = float(np.median(salaries)) if salaries else None
            
            companies = [j.company for j in jobs if j.company]
            top_companies = [c for c, _ in Counter(companies).most_common(3)]
            
            titles = [j.title for j in jobs if j.title]
            top_titles = [t for t, _ in Counter(titles).most_common(5)]
            
            all_skills = []
            for j in jobs:
                if j.raw_data and 'tags' in j.raw_data:
                    tags = j.raw_data['tags']
                    if isinstance(tags, list):
                        all_skills.extend([str(t).lower() for t in tags])
            
            top_skills = [s for s, _ in Counter(all_skills).most_common(5)]
            
            remote_count = sum(1 for j in jobs if j.location and "remote" in j.location.lower())
            remote_ratio = remote_count / size if size > 0 else 0.0
            
            # Find Representative Job (nearest to centroid)
            centroid = np.mean(cluster_embeddings, axis=0)
            distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
            nearest_idx = np.argmin(distances)
            representative_job = jobs[nearest_idx]
            rep_str = f"{representative_job.title} at {representative_job.company}"
            
            summary = ClusterSummary(
                cluster_id=cluster_id,
                size=size,
                median_salary=median_salary,
                top_companies=top_companies,
                top_skills=top_skills,
                top_titles=top_titles,
                remote_ratio=remote_ratio,
                representative_jobs=[rep_str]
            )
            summaries.append(summary)
            
        # Sort summaries by size descending
        summaries.sort(key=lambda s: s.size, reverse=True)
        return ClusterAnalysisReport(summaries=summaries)
