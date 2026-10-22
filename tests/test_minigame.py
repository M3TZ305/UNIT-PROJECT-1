import pytest
from core.database import load_data, save_data

def test_minigame_reward_logic():
    """اختبار إضافة رصيد التوكينز عند نجاح الاختراق"""
    data = load_data()
    initial_tokens = data.get("tokens", 0)
    
    # محاكاة منح الجائزة (750 TC)
    reward = 750
    data["tokens"] = initial_tokens + reward
    save_data(data)
    
    updated_data = load_data()
    assert updated_data["tokens"] == initial_tokens + reward
    
    # إعادة القيمة لما كانت عليه لعدم تخريب الحالة
    updated_data["tokens"] = initial_tokens
    save_data(updated_data)
