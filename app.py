
import streamlit as st
from PIL import Image
import base64
import requests
import json
import pandas as pd
import os
from io import BytesIO

# -----------------------------
# 설정
# -----------------------------
st.set_page_config(page_title="GASSAFE CHECKER (무료 테스트용)", layout="centered")
st.title("🏠 GASSAFE CHECKER | Hugging Face 무료 API 버전")

# -----------------------------
# Hugging Face 설정
# -----------------------------
hf_token = st.text_input("🔑 Hugging Face API 토큰 입력 (https://huggingface.co/settings/tokens)", type="password")
API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
headers = {"Authorization": f"Bearer {hf_token}"} if hf_token else {}

# -----------------------------
# 이미지 업로드
# -----------------------------
uploaded_file = st.file_uploader("📷 점검할 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

# -----------------------------
# 유사 사례 추천 함수
# -----------------------------
def recommend_case(result_text):
    try:
        if not os.path.exists("data/inspection_cases.csv"):
            return "📂 유사 사례 DB가 없습니다. data/inspection_cases.csv 파일을 추가하세요."

        df = pd.read_csv("data/inspection_cases.csv")
        for idx, row in df.iterrows():
            if row['problem_keyword'].lower() in result_text.lower():
                return row['tip']
        return "📂 유사 사례가 아직 등록되지 않았습니다."
    except Exception as e:
        return f"⚠️ 오류: {str(e)}"

# -----------------------------
# 이미지 분석 함수 (Hugging Face)
# -----------------------------
def analyze_image_hf(image_bytes):
    try:
        response = requests.post(API_URL, headers=headers, data=image_bytes)
        if response.status_code != 200:
            return f"⚠️ Hugging Face API 오류: {response.text}"

        results = response.json()
        if isinstance(results, dict) and results.get("error"):
            return f"⚠️ 오류: {results['error']}"

        labels = [f"- {item['label']} ({round(item['score']*100, 2)}%)" for item in results]
        return "\n".join(labels)
    except Exception as e:
        return f"⚠️ 분석 중 오류 발생: {str(e)}"

# -----------------------------
# 메인 실행
# -----------------------------
if uploaded_file and hf_token:
    file_bytes = uploaded_file.read()
    image = Image.open(BytesIO(file_bytes))
    st.image(image, caption="🔍 업로드된 이미지", use_container_width=True)

    with st.spinner("AI가 Hugging Face를 통해 이미지를 분석 중입니다..."):
        result = analyze_image_hf(file_bytes)

    st.markdown("### ✅ AI 점검 결과")
    st.markdown(result)

    st.markdown("### 💡 유사 사례 팁")
    st.info(recommend_case(result))

# -----------------------------
# 안내 문구
# -----------------------------
tabs = st.expander("📄 사용 안내")
with tabs:
    st.markdown("""
    - 이 버전은 Hugging Face의 무료 이미지 분석 모델 `vit-base-patch16-224`을 사용합니다.
    - 분석 정확도는 GPT-4보다 낮지만, 무료로 충분한 테스트가 가능합니다.
    - Hugging Face 회원 가입 후 [settings/tokens](https://huggingface.co/settings/tokens)에서 Read 토큰을 발급받아 입력하세요.
    - 유사 사례 추천을 위해 `data/inspection_cases.csv` 파일이 필요합니다.
    """)
