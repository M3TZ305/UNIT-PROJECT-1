import pytest
from core.database import load_data, save_data
from services.store import search_agents, add_to_cart, remove_from_cart
from ui.menus import calculate_operator_rank
from services.synergy import check_agent_synergy

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

def test_operator_rank():
    """اختبار حساب رتبة المستخدم بناءً على سجل المشتريات"""
    assert "Novice Operator" in calculate_operator_rank({"history": []})
    assert "Cyber Specialist" in calculate_operator_rank({"history": [{}]})
    assert "Elite Hacker" in calculate_operator_rank({"history": [{}, {}, {}]})
    assert "Master Architect" in calculate_operator_rank({"history": [{}, {}, {}, {}, {}, {}]})

def test_synergy_logic():
    """اختبار حساب قواعد التناغم الاستراتيجي للوكلاء"""
    # اختبار تداخل البرمجة والأمان
    agents = [{"name": "DeepCode-V4"}, {"name": "SecGuard"}]
    synergies = check_agent_synergy(agents)
    assert len(synergies) == 1
    assert "Cyber-Defense Grid" in synergies[0]["title"]
    
    # اختبار امتلاك 3 وكلاء أو أكثر
    agents_swarm = [{"name": "Agent1"}, {"name": "Agent2"}, {"name": "Agent3"}]
    synergies_swarm = check_agent_synergy(agents_swarm)
    assert any("Neural Swarm" in s["title"] for s in synergies_swarm)
