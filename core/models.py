import os
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    data_json = Column(JSON)

# Database selalu di folder data/ milik aplikasi, dari folder mana pun app.py dijalankan
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
engine = create_engine(f"sqlite:///{os.path.join(DATA_DIR, 'smart_dss.db')}", connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    from core.seed import seed_default_project
    with SessionLocal() as db:
        if db.query(Project).count() == 0:
            db.add(seed_default_project())
            db.commit()
