import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.db.models.user import User,Role
from app.core.security import hash_password
@pytest.fixture
def db():
    engine=create_engine('sqlite+pysqlite:///:memory:',connect_args={'check_same_thread':False})
    Base.metadata.create_all(engine); Session=sessionmaker(bind=engine); s=Session(); yield s; s.close()
@pytest.fixture
def customer(db):
    u=User(email='customer@example.com',full_name='Customer',password_hash=hash_password('password123'),role=Role.CUSTOMER);db.add(u);db.commit();db.refresh(u);return u
