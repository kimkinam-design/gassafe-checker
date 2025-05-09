# Hugging Face API 예제 프로젝트

이 프로젝트는 Hugging Face Inference API를 안전하게 호출하는 Python 예제입니다.

## 📦 구성 파일
- `huggingface_api_example.py`: API 요청을 수행하는 메인 스크립트
- `.env`: Hugging Face API 토큰을 보관 (업로드 금지)
- `requirements.txt`: 필요한 패키지 목록
- `.gitignore`: 민감 정보 제외 설정

## 🔐 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```
HF_TOKEN=your_huggingface_api_token
```

## ▶️ 실행 방법

```bash
pip install -r requirements.txt
python huggingface_api_example.py
```

