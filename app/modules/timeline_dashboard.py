import gradio as gr
import pandas as pd
import plotly.express as px
from app.modules.export_utils import export_excel_file, export_pdf_file


def get_timeline_data():
    """DB에서 ModelInfo를 조회해 타임라인 시각화용 DataFrame으로 반환한다."""
    from app.db.session import SessionLocal
    from app.db.models import ModelInfo
    import datetime

    db = SessionLocal()
    try:
        records = db.query(ModelInfo).all()
        data = []
        today = datetime.date.today()
        for m in records:
            # 서비스 종료일이 없으면 오늘 날짜 사용
            end_dt = m.end_date or today
            data.append({
                'model_name': m.model_name,
                'vendor': m.vendor,
                'usage': m.usage,
                'release_date': m.release_date,
                'end_date': end_dt,
                'alias': m.alias,
                'status': m.status,
            })
        return pd.DataFrame(data)
    finally:
        db.close()


def build_timeline_dashboard():
    df = get_timeline_data()
    # TODO: adjust x_start/x_end column names if needed
    fig = px.timeline(df, x_start="release_date", x_end="end_date", y="usage", color="status")
    with gr.Column():
        gr.Plot(value=fig, label="모델 타임라인")
        excel_btn = gr.Button("Export Excel")
        excel_file = gr.File(label="Excel 파일(.xlsx)")
        excel_btn.click(fn=lambda: export_excel_file(df), outputs=excel_file)
        pdf_btn = gr.Button("Export PDF")
        pdf_file = gr.File(label="PDF 파일(.pdf)")
        pdf_btn.click(fn=lambda: export_pdf_file(df), outputs=pdf_file) 