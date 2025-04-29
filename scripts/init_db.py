# PYTHONPATH를 설정하여 상위 디렉터리의 `app` 패키지를 인식하도록 합니다
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from app.db.models import Base

# DB 파일 경로
DB_PATH = 'data/llmboard.db'

def init_db():
    engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)
    # 기존 테이블이 있으면 삭제 후 재생성
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
    print('Initialized database at', DB_PATH) 