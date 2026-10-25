import pytest
from services.sandbox import calculate_benchmark_metrics

def test_calculate_benchmark_metrics():
    """اختبار حساب مقاييس الأداء والاختبار المعياري للوكيل"""
    agent = {"name": "DeepCode-V4", "success_rate": 99.4}
    metrics = calculate_benchmark_metrics(agent)
    
    assert isinstance(metrics, dict)
    assert "latency" in metrics
    assert "accuracy" in metrics
    assert "throughput" in metrics
    assert "security_status" in metrics
    assert isinstance(metrics["latency"], float)
    assert isinstance(metrics["accuracy"], float)
    assert isinstance(metrics["throughput"], int)
    assert isinstance(metrics["security_status"], str)
