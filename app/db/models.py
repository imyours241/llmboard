from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, Enum

Base = declarative_base()

class ModelInfo(Base):
    __tablename__ = 'model_info'
    model_name = Column(String, primary_key=True)
    alias = Column(String)
    vendor = Column(String)
    release_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    status = Column(Enum('운영','종료','반입','반입검토', name='status_enum'))
    io_type = Column(String)
    usage = Column(String)
    applied_service = Column(String)
    parameter_count = Column(String)
    architecture = Column(String)
    max_input_tokens = Column(String)
    multimodal_support = Column(String)
    supported_languages = Column(String)
    license_info = Column(String)
    gpu_idx = Column(String)
    deployment_method = Column(String)
    onprem_difficulty = Column(String)
    memory_requirements = Column(String)
    inference_speed = Column(String)
    fine_tuning = Column(String)
    embedding_support = Column(String)
    tooling_friendly = Column(String)
    eval_metrics = Column(String)
    inbuilt_safety = Column(String)
    paper_link = Column(String)

class ModelOperation(Base):
    __tablename__ = 'model_operation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String)
    service_start = Column(Date)
    service_end = Column(Date, nullable=True)
    operation_period = Column(Integer) 