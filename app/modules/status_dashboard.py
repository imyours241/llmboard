import gradio as gr
import pandas as pd
from app.db.session import get_db
from app.db.models import ModelInfo
from app.modules.export_utils import export_excel_file, export_pdf_file
from gradio_modal import Modal
import functools


def get_overview_df():
    """DB에서 ModelInfo를 조회해 DataFrame으로 반환한다."""
    from app.db.session import SessionLocal
    from app.db.models import ModelInfo

    db = SessionLocal()
    try:
        records = db.query(ModelInfo).all()
        data = []
        for m in records:
            data.append({
                'model_name': m.model_name,
                'alias': m.alias,
                'vendor': m.vendor,
                'release_date': m.release_date,
                'start_date': m.start_date,
                'end_date': m.end_date,
                'status': m.status,
            })
        return pd.DataFrame(data)
    finally:
        db.close()


def show_detail(selected_models):
    """선택된 모델 리스트에 대해 상세 정보를 Markdown으로 반환한다."""
    from app.db.session import SessionLocal
    from app.db.models import ModelInfo

    db = SessionLocal()
    md = ""
    try:
        for name in selected_models or []:
            m = db.query(ModelInfo).filter_by(model_name=name).first()
            if not m:
                continue
            md += f"### {m.model_name}\n\n"
            md += "| 항목 | 값 |\n| --- | --- |\n"
            md += f"| 모델명 | {m.model_name} |\n"
            md += f"| Alias | {m.alias or ''} |\n"
            md += f"| 개발사 | {m.vendor or ''} |\n"
            md += f"| 릴리즈일 | {m.release_date} |\n"
            md += f"| 서비스시작일 | {m.start_date} |\n"
            md += f"| 서비스종료일 | {m.end_date or ''} |\n"
            md += f"| 서비스여부 | {m.status} |\n"
            # 추가 정보
            md += f"| 적용서비스 | {m.applied_service or ''} |\n"
            md += f"| 파라미터 수 | {m.parameter_count or ''} |\n"
            md += f"| 아키텍처 | {m.architecture or ''} |\n"
            md += f"| 입력 토큰 수 | {m.max_input_tokens or ''} |\n"
            md += f"| 멀티모달 지원 | {m.multimodal_support or ''} |\n"
            md += f"| 지원 언어 | {m.supported_languages or ''} |\n"
            md += f"| 라이선스 | {m.license_info or ''} |\n"
            md += f"| GPU idx | {m.gpu_idx or ''} |\n"
            md += f"| 배포 방식 | {m.deployment_method or ''} |\n"
            md += f"| on-prem 배포 난이도 | {m.onprem_difficulty or ''} |\n"
            md += f"| 메모리 요구사항 | {m.memory_requirements or ''} |\n"
            md += f"| Inference 속도 | {m.inference_speed or ''} |\n"
            md += f"| Fine-tuning | {m.fine_tuning or ''} |\n"
            md += f"| Embedding 지원 | {m.embedding_support or ''} |\n"
            md += f"| 툴콜링/에이전트 친화성 | {m.tooling_friendly or ''} |\n"
            md += f"| 평가 지표 | {m.eval_metrics or ''} |\n"
            md += f"| 안전성 내장 | {m.inbuilt_safety or ''} |\n"
            md += f"| 논문 링크 | {m.paper_link or ''} |\n\n"
        return md or "선택된 모델이 없습니다."
    finally:
        db.close()


def build_status_dashboard():
    df = get_overview_df()
    with gr.Column():
        with gr.TabItem("표 보기"):
            # 상단 우측에 Excel/PDF 다운로드 버튼 배치
            with gr.Row():
                with gr.Column(scale=5):
                    pass
                with gr.Column(scale=1):
                    excel_btn = gr.Button("💾 Excel", variant="secondary")
                    excel_file = gr.File(visible=False)
                    excel_btn.click(
                        fn=lambda: gr.update(value=export_excel_file(df), visible=True),
                        outputs=excel_file,
                    )
                    excel_file
                with gr.Column(scale=1):
                    pdf_btn = gr.Button("📄 PDF", variant="secondary")
                    pdf_file = gr.File(visible=False)
                    pdf_btn.click(
                        fn=lambda: gr.update(value=export_pdf_file(df), visible=True),
                        outputs=pdf_file,
                    )
            # Modal 컴포넌트로 실제 팝업 레이아웃 구현
            detail_modal = Modal(visible=False)
            with detail_modal:
                detail_md = gr.Markdown()
                close_btn = gr.Button("닫기")
                # 모달 닫기
                close_btn.click(fn=lambda: gr.update(visible=False), outputs=detail_modal)
            with gr.Row():
                with gr.Column(scale=1):
                    # 모델별 상세 버튼
                    for name in df['model_name'].tolist():
                        btn = gr.Button(f"상세 {name}")
                        # 모달 내용 설정
                        btn.click(fn=functools.partial(show_detail, [name]), outputs=detail_md)
                        # 모달 표시
                        btn.click(fn=lambda: gr.update(visible=True), outputs=detail_modal)
                with gr.Column(scale=5):
                    # 데이터프레임 표시
                    gr.DataFrame(value=df, label="모델 현황")
        with gr.TabItem("Markdown 보기"):
            gr.Markdown(value=df.to_markdown(), label="모델 현황")
        # Deprecated: bottom export buttons removed 