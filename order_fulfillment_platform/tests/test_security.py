from datetime import timedelta
from app.core.security import hash_password,verify_password,create_token,decode_token
def test_password_hash():
    h=hash_password('password123'); assert h!='password123'; assert verify_password('password123',h)
def test_token_roundtrip():
    t=create_token('42','access',timedelta(minutes=5)); p=decode_token(t); assert p['sub']=='42' and p['type']=='access'
