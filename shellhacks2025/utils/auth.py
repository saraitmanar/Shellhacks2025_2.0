# utils/auth.py
from typing import Optional, Dict, List

USERS: List[Dict] = [
    {"id": "S1001", "name": "Ava",  "role": "student", "band": "middle",     "password": "pass123"},
    {"id": "S1002", "name": "Liam", "role": "student", "band": "high",       "password": "pass123"},
    {"id": "S1003", "name": "Maya", "role": "student", "band": "elementary", "password": "pass123"},
    {"id": "A0001", "name": "Admin","role": "admin",   "band": None,         "password": "adminpw"},
]

def find_user(user_id: str) -> Optional[Dict]:
    for u in USERS:
        if u["id"] == user_id:
            return u
    return None

def verify_login(user_id: str, password: str) -> Optional[Dict]:
    u = find_user(user_id)
    if not u: return None
    if u["password"] != password: return None
    return u
