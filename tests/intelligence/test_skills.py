import os
import pytest
import yaml
from src.intelligence.skills.ontology import SkillOntology
from src.intelligence.skills.normalizer import SkillNormalizer
from src.intelligence.skills.extractor import SkillExtractor
from src.intelligence.skills.statistics import SkillStatistics
from src.domain.entities.job_posting import JobPosting

@pytest.fixture
def mock_ontology_file(tmp_path):
    filepath = tmp_path / "skills.yaml"
    data = {
        "Python": {
            "category": "Programming Language",
            "aliases": ["python", "python3"]
        },
        "AWS": {
            "category": "Cloud",
            "aliases": ["aws", "amazon web services"]
        }
    }
    with open(filepath, "w") as f:
        yaml.dump(data, f)
    return str(filepath)

def test_ontology_loading(mock_ontology_file):
    ontology = SkillOntology(mock_ontology_file)
    assert "Python" in ontology.skills
    
    # Test alias resolution
    assert ontology.resolve("python3") == "Python"
    assert ontology.resolve("PYTHON") == "Python"
    assert ontology.resolve("amazon web services") == "AWS"
    assert ontology.resolve("unknown") is None

def test_skill_normalizer(mock_ontology_file):
    ontology = SkillOntology(mock_ontology_file)
    normalizer = SkillNormalizer(ontology)
    
    raw = ["python3", "aws", "docker"] # docker is unknown here
    occurrences = normalizer.normalize(raw)
    
    assert len(occurrences) == 2
    assert occurrences[0].skill == "Python"
    assert occurrences[0].confidence == 1.0
    assert occurrences[0].source == "metadata"
    
    assert occurrences[1].skill == "AWS"

def test_skill_extractor(mock_ontology_file):
    ontology = SkillOntology(mock_ontology_file)
    extractor = SkillExtractor(ontology)
    
    from datetime import datetime, timezone
    job = JobPosting(
        id="1",
        title="Python Engineer at AWS",
        company="Amazon",
        description="We need someone with python3 and amazon web services experience.",
        url="http://test.com",
        raw_data={},
        metadata=None
    )
    
    occurrences = extractor.extract_all(job)
    
    # Expect: Python (title), AWS (title), Python (desc), AWS (desc)
    assert len(occurrences) == 4
    
    skills = [o.skill for o in occurrences]
    assert skills.count("Python") == 2
    assert skills.count("AWS") == 2
    
    assert occurrences[0].confidence == 0.9

def test_skill_statistics(mock_ontology_file):
    ontology = SkillOntology(mock_ontology_file)
    normalizer = SkillNormalizer(ontology)
    
    raw = ["python", "python3", "aws"]
    occurrences = normalizer.normalize(raw)
    
    stats = SkillStatistics.aggregate(occurrences)
    assert stats["Python"] == 2
    assert stats["AWS"] == 1
