from src.domain.entities.job_posting import JobPosting

class TextBuilder:
    @staticmethod
    def build(job: JobPosting) -> str:
        parts = []
        
        if job.title:
            parts.append(job.title)
            
        if job.company:
            parts.append(f"Company: {job.company}")
            
        if job.location:
            parts.append(f"Location: {job.location}")
            
        if job.employment_type:
            parts.append(f"Employment: {job.employment_type}")
            
        if job.skills:
            parts.append("Skills:")
            parts.append("\n".join(job.skills))
            
        if job.description:
            parts.append("Description:")
            parts.append(job.description)
            
        return "\n\n".join(parts)
