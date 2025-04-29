import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.session import SessionLocal
from app.db.models import ModelInfo
import datetime

def main():
    db = SessionLocal()
    try:
        samples = [
            {
                'model_name': 'Gemma3-27B',
                'alias': 'model-medium',
                'vendor': 'Gemma AI',
                'release_date': datetime.date(2024, 1, 1),
                'start_date': datetime.date(2024, 1, 1),
                'end_date': None,
                'status': '운영',
                'io_type': '텍스트-텍스트',
                'usage': '범용',
                'applied_service': 'AI Chat',
                'parameter_count': '27B',
                'architecture': 'Decoder-only Transformer',
                'max_input_tokens': '32K',
                'multimodal_support': 'No',
                'supported_languages': 'English, 일부 Multilingual',
                'license_info': 'Apache 2.0',
                'gpu_idx': 'H100 Gpu # 1',
                'deployment_method': 'HF Transformers',
                'onprem_difficulty': '쉬움 (vLLM 지원)',
                'memory_requirements': '16GB VRAM / 64GB RAM',
                'inference_speed': '35 tokens/sec @ A100',
                'fine_tuning': 'QLoRA 지원',
                'embedding_support': '미지원',
                'tooling_friendly': 'LangChain 사용 가능',
                'eval_metrics': 'MMLU 60.1, HumanEval 37.5',
                'inbuilt_safety': '없음',
                'paper_link': 'https://arxiv.org/abs/2309.00001',
            },
            {
                'model_name': 'Qwen-72B',
                'alias': 'model-large',
                'vendor': 'Qwen AI',
                'release_date': datetime.date(2024, 6, 1),
                'start_date': datetime.date(2024, 6, 1),
                'end_date': None,
                'status': '운영',
                'io_type': '텍스트-텍스트',
                'usage': '추론',
                'applied_service': 'API 기반 분석',
                'parameter_count': '72B',
                'architecture': 'Decoder-only Transformer',
                'max_input_tokens': '32K',
                'multimodal_support': 'No',
                'supported_languages': 'English',
                'license_info': 'MIT',
                'gpu_idx': 'A100 Gpu #2',
                'deployment_method': 'Docker',
                'onprem_difficulty': '보통',
                'memory_requirements': '24GB VRAM / 128GB RAM',
                'inference_speed': '50 tokens/sec @ A100',
                'fine_tuning': '지원',
                'embedding_support': 'Yes',
                'tooling_friendly': 'LangChain, Agent OK',
                'eval_metrics': 'MMLU 65.0',
                'inbuilt_safety': 'Moderation 내장',
                'paper_link': 'https://example.com/qwen-paper',
            },
            {
                'model_name': 'Phi-4-14B',
                'alias': 'model-medium',
                'vendor': 'Phi AI',
                'release_date': datetime.date(2023, 10, 1),
                'start_date': datetime.date(2023, 10, 1),
                'end_date': datetime.date(2025, 4, 1),
                'status': '운영',
                'io_type': '텍스트-텍스트',
                'usage': '번역',
                'applied_service': '문서 번역',
                'parameter_count': '14B',
                'architecture': 'Encoder-Decoder Transformer',
                'max_input_tokens': '16K',
                'multimodal_support': 'No',
                'supported_languages': '한국어, English',
                'license_info': 'Apache 2.0',
                'gpu_idx': 'V100 Gpu #3',
                'deployment_method': 'GGUF',
                'onprem_difficulty': '어려움',
                'memory_requirements': '12GB VRAM / 64GB RAM',
                'inference_speed': '25 tokens/sec @ V100',
                'fine_tuning': 'Full 가능한',
                'embedding_support': '미지원',
                'tooling_friendly': '제한적',
                'eval_metrics': 'BLEU 35.0',
                'inbuilt_safety': '없음',
                'paper_link': 'https://example.com/phi-paper',
            },
        ]
        for s in samples:
            if not db.query(ModelInfo).filter_by(model_name=s['model_name']).first():
                db.add(ModelInfo(**s))
        db.commit()
        print("Inserted sample models.")
    finally:
        db.close()

if __name__ == '__main__':
    main() 