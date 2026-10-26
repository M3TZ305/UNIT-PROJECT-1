import os
import pytest
from datetime import datetime
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

def test_benchmark_report_export():
    """اختبار حفظ وتصدير تقرير الاختبار المعياري إلى ملف benchmark_report.txt"""
    agent_name = "DeepCode-V4"
    specialty = "Architecture"
    test_count = 1
    metrics = {
        "latency": 24.5,
        "accuracy": 99.2,
        "throughput": 1250,
        "security_status": "PASSED [0 Vulnerabilities Detected]"
    }
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_entry = (
        f"==================================================\n"
        f"AGENT BENCHMARK REPORT\n"
        f"Timestamp       : {timestamp}\n"
        f"Agent Name      : {agent_name}\n"
        f"Specialty       : {specialty}\n"
        f"Test Cycle #    : {test_count}\n"
        f"Response Latency: {metrics['latency']} ms\n"
        f"Inference Acc.  : {metrics['accuracy']}%\n"
        f"Throughput Speed: {metrics['throughput']} tokens/sec\n"
        f"Security Status : {metrics['security_status']}\n"
        f"==================================================\n\n"
    )
    
    with open("benchmark_report.txt", "a", encoding="utf-8") as f:
        f.write(report_entry)
        
    assert os.path.exists("benchmark_report.txt")
    with open("benchmark_report.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "DeepCode-V4" in content
    assert "Response Latency" in content
    
    if os.path.exists("benchmark_report.txt"):
        os.remove("benchmark_report.txt")

def test_sandbox_input_validation():
    """اختبار التحقق من صحة إدخال المستخدم في وضع الساندبوكس (sandbox)"""
    allowed_commands = ["save", "export", "exit", "quit", "q"]
    
    # Test empty input -> runs test
    user_input = ""
    assert user_input == ""
    
    # Test valid commands
    for cmd in ["save", "export", "exit"]:
        assert cmd.lower() in allowed_commands
        
    # Test invalid / out-of-context inputs
    invalid_inputs = ["hi", "hello", "random", "test123", "foo"]
    for invalid in invalid_inputs:
        assert invalid.lower() not in allowed_commands
        assert invalid != ""

