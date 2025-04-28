# app.py
import streamlit as st
from PIL import Image
import openai
import base64
import pandas as pd
import os
from io import BytesIO

# -----------------------------
# 설정
# -----------------------------
st.set_page_config(page_title="GASSAFE CHECKER", layout="centered")
st.title("🏠 미래엔서해에너지 서부안전팀 | GASSAFE CHECKER")

# -----------------------------
# API 키 입력
# -----------------------------
api_key = st.text_input("🔑 OpenAI API 키를 입력하세요", type="password")
if api_key:
    openai.api_key = api_key

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
# 이미지 분석 함수
# -----------------------------
def analyze_image(file_bytes):
    try:
        b64_image = base64.b64encode(file_bytes).decode("utf-8")

        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 도시가스 점검 보조 인공지능이야. "
                        "사용자가 업로드한 사진을 보고, 어떤 도시가스 시설물인지 판단하고 "
                        "KGS CODE 및 도시가스사업법에 따라 설치 기준에 맞는지 평가해줘. "
                        "항목별로 Pass/Fail을 표시하고, 유사 사례 팁이 있으면 추천해줘."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 사진을 분석해줘. 기준에 맞는지 알려줘."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                    ]
                }
            ],
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ OpenAI 오류: {str(e)}"

# -----------------------------
# 메인 실행
# -----------------------------
if uploaded_file and api_key:
    file_bytes = uploaded_file.read()
    image = Image.open(uploaded_file)
    st.image(image, caption="🔍 업로드된 이미지", use_column_width=True)

    with st.spinner("AI가 사진을 분석하고 있습니다..."):
        result = analyze_image(file_bytes)

    st.markdown("### ✅ AI 점검 결과")
    st.markdown(result)

    st.markdown("### 💡 유사 사례 팁")
    st.info(recommend_case(result))

# 샘플 이미지 테스트용
if st.button("🎯 샘플 이미지로 테스트하기"):
    def create_sample_image():
        img = Image.new('RGB', (400, 300), color=(255, 228, 225))
        buf = BytesIO()
        img.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        return byte_im

    file_bytes = create_sample_image()
    st.image(Image.open(BytesIO(file_bytes)), caption="🖼️ 샘플 이미지", use_column_width=True)

    with st.spinner("AI가 샘플 이미지를 분석하고 있습니다..."):
        result = analyze_image(file_bytes)

    st.markdown("### ✅ AI 점검 결과 (샘플)")
    st.markdown(result)

    st.markdown("### 💡 유사 사례 팁 (샘플)")
    st.info(recommend_case(result))

# -----------------------------
# 주의 안내
# -----------------------------
tabs = st.expander("📄 파일/DB 안내")
with tabs:
    st.markdown("""
    - `data/inspection_cases.csv` 파일이 필요합니다. (`problem_keyword`, `tip` 컬럼 필수)
    - OpenAI API 키는 gpt-4-vision-preview 모델을 사용할 수 있는 키여야 합니다.
    - 파일이 없으면 일부 기능이 정상 작동하지 않을 수 있습니다.
    """)
