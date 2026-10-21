import pytest
from core.database import load_data, save_data
from services.store import search_agents, add_to_cart, remove_from_cart

def test_database_structure():
    """التحقق من أن قاعدة البيانات تحمل الهيكل الأساسي بشكل صحيح"""
    data = load_data()
    assert "agents" in data
    assert "cart" in data
    assert "history" in data
    assert "tokens" in data

def test_agent_search():
    """اختبار وظيفة البحث عن وكيل بالاسم أو التخصص"""
    results = search_agents("DeepCode")
    assert len(results) > 0
    assert results[0]["name"] == "DeepCode-V4"

def test_cart_flow():
    """اختبار دورة السلة (الإضافة، التحقق، والحذف)"""
    # تفريغ السلة للبدء باختبار نظيف
    data = load_data()
    data["cart"] = []
    save_data(data)
    
    # 1. اختبار إضافة وكيل للسلة
    added = add_to_cart("01")
    assert added is True
    
    data_checked = load_data()
    assert len(data_checked["cart"]) == 1
    assert data_checked["cart"][0]["id"] == "01"
    
    # 2. اختبار إزالة الوكيل من السلة
    removed = remove_from_cart("01")
    assert removed is True
    
    data_final = load_data()
    assert len(data_final["cart"]) == 0
