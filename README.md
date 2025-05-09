# Gassafe Checker

이 프로젝트는 Hugging Face Inference API를 안전하게 호출하고, 점검 케이스 추천 데이터를 활용하는 예제입니다.

## 🔧 사용법

1. `.env` 파일 생성:
```
HF_TOKEN=your_actual_huggingface_token
```

2. 패키지 설치:
```
pip install -r requirements.txt
```

3. 실행:
```
python huggingface_api_example.py
```

## 📁 파일 설명

- `huggingface_api_example.py`: API 요청 예제
- `data/inspection_cases.csv`: 점검 항목 및 추천 문구 데이터
- `.env.example`: 환경 변수 예시 (토큰은 .env에 따로 저장)
