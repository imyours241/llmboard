import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
import tempfile


def export_excel(df: pd.DataFrame) -> BytesIO:
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer


def export_pdf(df: pd.DataFrame) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data)
    doc.build([table])
    buffer.seek(0)
    return buffer


def export_excel_file(df: pd.DataFrame) -> str:
    """DataFrame을 임시 xlsx 파일로 저장하고 경로를 반환합니다."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    df.to_excel(tmp.name, index=False)
    tmp.close()
    return tmp.name


def export_pdf_file(df: pd.DataFrame) -> str:
    """DataFrame을 임시 PDF 파일로 저장하고 경로를 반환합니다."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmp.name, pagesize=letter)
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data)
    doc.build([table])
    tmp.close()
    return tmp.name 