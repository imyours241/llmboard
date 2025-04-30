# main.py
import gradio as gr
import sqlite3
import pandas as pd

# 데이터베이스 연결 및 테이블 생성
conn = sqlite3.connect("models.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS model_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    용도 TEXT,
    입출력유형 TEXT,
    모델명 TEXT UNIQUE,
    모델명ALIAS TEXT,
    서비스여부 TEXT,
    모델출시년월 TEXT,
    서비스시작월 TEXT,
    서비스종료월 TEXT
)
""")
conn.commit()

# 페이지별 함수 정의

def show_model_status():
    """모델 현황정보를 리스트 형태(JSON)로 반환"""
    df = pd.read_sql("SELECT * FROM model_info", conn)
    return df.to_dict(orient="records")


def show_timeline():
    """모델 타임라인 데이터를 리스트 형태(JSON)로 반환"""
    df = pd.read_sql("SELECT * FROM model_info", conn)
    return df.to_dict(orient="records")


def register_single(용도, 입출력유형, 모델명, 모델명ALIAS, 서비스여부, 모델출시년월, 서비스시작월, 서비스종료월):
    """단건 모델정보 등록 또는 업데이트"""
    cursor.execute("""
    INSERT INTO model_info (용도, 입출력유형, 모델명, 모델명ALIAS, 서비스여부, 모델출시년월, 서비스시작월, 서비스종료월)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(모델명) DO UPDATE SET
        용도=excluded.용도,
        입출력유형=excluded.입출력유형,
        모델명ALIAS=excluded.모델명ALIAS,
        서비스여부=excluded.서비스여부,
        모델출시년월=excluded.모델출시년월,
        서비스시작월=excluded.서비스시작월,
        서비스종료월=excluded.서비스종료월
    """, (용도, 입출력유형, 모델명, 모델명ALIAS, 서비스여부, 모델출시년월, 서비스시작월, 서비스종료월))
    conn.commit()
    return "단건 등록 완료"


def register_bulk(file):
    """CSV 파일을 업로드하여 다건 모델정보 등록(추후 구현)"""
    df = pd.read_csv(file.name)
    # TODO: upsert 로직 구현
    return "다건 등록 완료"

# Gradio 인터페이스 설정
status_interface = gr.Interface(
    fn=show_model_status,
    inputs=[],
    outputs=gr.JSON(label="모델 현황정보"),
    title="모델 현황정보 대시보드"
)

timeline_interface = gr.Interface(
    fn=show_timeline,
    inputs=[],
    outputs=gr.JSON(label="모델 타임라인"),
    title="모델 타임라인 시각화 대시보드"
)

single_interface = gr.Interface(
    fn=register_single,
    inputs=[
        gr.Dropdown(['범용','추론','번역','코딩','OCR'], label="용도"),
        gr.Dropdown(['텍스트-텍스트','이미지-텍스트','음성-텍스트'], label="입출력유형"),
        gr.Textbox(label="모델명"),
        gr.Textbox(label="모델명ALIAS"),
        gr.Dropdown(['운영','종료','반입','반입검토'], label="서비스여부"),
        gr.Textbox(label="모델출시년월 (YYYYMM)"),
        gr.Textbox(label="서비스시작월 (YYYYMM)"),
        gr.Textbox(label="서비스종료월 (YYYYMM)")
    ],
    outputs="text",
    title="단건 모델정보 등록"
)

bulk_interface = gr.Interface(
    fn=register_bulk,
    inputs=gr.File(label="CSV 파일 업로드"),
    outputs="text",
    title="다건 모델정보 등록"
)

app = gr.TabbedInterface(
    [status_interface, timeline_interface, single_interface, bulk_interface],
    ["현황", "타임라인", "단건등록", "다건등록"]
)

if __name__ == "__main__":
    app.launch(share=True) 