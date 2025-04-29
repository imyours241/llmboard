from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB 파일 경로 및 URL
DB_PATH = 'data/llmboard.db'
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# 엔진 및 세션 팩토리 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """데이터베이스 세션을 생성하고, 사용 후 종료하는 제너레이터"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 