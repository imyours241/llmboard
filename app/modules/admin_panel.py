import gradio as gr
import pandas as pd
from fastapi import UploadFile
from app.db.session import get_db
from app.db.models import ModelInfo
from app.modules.export_utils import export_excel


def insert_one(model_name, alias, vendor, release_date, start_date, end_date, status,
                io_type, usage, applied_service, parameter_count, architecture,
                max_input_tokens, multimodal_support, supported_languages,
                license_info, gpu_idx, deployment_method, onprem_difficulty,
                memory_requirements, inference_speed, fine_tuning,
                embedding_support, tooling_friendly, eval_metrics,
                inbuilt_safety, paper_link):
    """단건 모델 정보를 DB에 추가한다."""
    from app.db.session import SessionLocal
    import datetime

    def parse_date(s: str):
        if not s:
            return None
        for fmt in ('%Y-%m-%d', '%Y.%m', '%Y-%m'):
            try:
                dt = datetime.datetime.strptime(s, fmt)
                if fmt in ('%Y.%m', '%Y-%m'):
                    dt = dt.replace(day=1)
                return dt.date()
            except ValueError:
                continue
        raise ValueError(f"Unsupported date format: {s}")

    rd = parse_date(release_date)
    sd = parse_date(start_date)
    ed = parse_date(end_date)

    db = SessionLocal()
    try:
        m = ModelInfo(
            model_name=model_name,
            alias=alias,
            vendor=vendor,
            release_date=rd,
            start_date=sd,
            end_date=ed,
            status=status,
            io_type=io_type,
            usage=usage,
            applied_service=applied_service,
            parameter_count=parameter_count,
            architecture=architecture,
            max_input_tokens=max_input_tokens,
            multimodal_support=multimodal_support,
            supported_languages=supported_languages,
            license_info=license_info,
            gpu_idx=gpu_idx,
            deployment_method=deployment_method,
            onprem_difficulty=onprem_difficulty,
            memory_requirements=memory_requirements,
            inference_speed=inference_speed,
            fine_tuning=fine_tuning,
            embedding_support=embedding_support,
            tooling_friendly=tooling_friendly,
            eval_metrics=eval_metrics,
            inbuilt_safety=inbuilt_safety,
            paper_link=paper_link,
        )
        db.add(m)
        db.commit()
        return f"단건 등록 완료: {model_name}"
    except Exception as e:
        db.rollback()
        return f"오류 발생: {e}"
    finally:
        db.close()


def upload_csv(file):
    # TODO: read CSV, validate and upsert into DB
    return "CSV 업로드 완료"


def download_csv():
    # TODO: fetch all models and return as CSV bytes
    return export_excel(pd.DataFrame())


def build_admin_panel():
    with gr.Column():
        gr.Markdown("### 단건 등록")
        # 모든 필드에 대한 입력 폼 생성
        fields = [
            'model_name','alias','vendor','release_date','start_date','end_date','status',
            'io_type','usage','applied_service','parameter_count','architecture',
            'max_input_tokens','multimodal_support','supported_languages','license_info',
            'gpu_idx','deployment_method','onprem_difficulty','memory_requirements',
            'inference_speed','fine_tuning','embedding_support','tooling_friendly',
            'eval_metrics','inbuilt_safety','paper_link'
        ]
        inputs = [gr.Textbox(label=field) for field in fields]
        submit = gr.Button("등록")
        msg = gr.Textbox()
        submit.click(fn=insert_one, inputs=inputs, outputs=msg)

        gr.Markdown("### 다건 CSV 업로드/다운로드")
        csv_upload = gr.File(label="CSV 업로드")
        upload_msg = gr.Textbox()
        csv_upload.change(fn=upload_csv, inputs=csv_upload, outputs=upload_msg)
        download_btn = gr.Button("CSV 다운로드")
        download_file = gr.File()
        download_btn.click(fn=download_csv, outputs=download_file) 