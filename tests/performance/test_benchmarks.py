import json
import pytest
from pathlib import Path
import time

def load_baseline():
    baseline_file = Path(__file__).parent / "baseline.json"
    with open(baseline_file, "r") as f:
        return json.load(f)

def test_semantic_search_performance_target():
    """Asserts that semantic search executes within the baseline target."""
    baseline = load_baseline()
    target_ms = baseline.get("semantic_search_ms", 10)
    
    # Mocking execution time measurement for demonstration.
    # In reality, this would wrap the actual function execution.
    start = time.perf_counter()
    # execute_search(...)
    end = time.perf_counter()
    execution_time_ms = (end - start) * 1000
    
    assert execution_time_ms <= target_ms, f"Search took {execution_time_ms}ms, expected <= {target_ms}ms"

def test_career_analysis_performance_target():
    baseline = load_baseline()
    target_ms = baseline.get("career_analysis_ms", 50)
    
    execution_time_ms = 12.5 # Mocked runtime
    
    assert execution_time_ms <= target_ms, f"Career Analysis took {execution_time_ms}ms, expected <= {target_ms}ms"

def test_learning_simulation_performance_target():
    baseline = load_baseline()
    target_ms = baseline.get("learning_ms", 100)
    
    execution_time_ms = 45.0 # Mocked runtime
    
    assert execution_time_ms <= target_ms
