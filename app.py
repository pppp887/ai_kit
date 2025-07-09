# app.py (Streamlit frontend)
import streamlit as st
import requests

st.set_page_config(page_title="AI 회로 분석기", layout="centered")
st.title("📷 AI 기반 회로 인식 & 시뮬레이션")

# 사용자 입력
image_file = st.file_uploader("회로 이미지를 업로드하세요 (jpg/png)", type=["jpg", "png"])
voltage = st.number_input("인가 전압 (V)", min_value=0.0, max_value=20.0, value=5.0)

if st.button("시뮬레이션 실행"):
    if image_file is None:
        st.warning("이미지를 업로드해주세요.")
    else:
        with st.spinner("AI 분석 및 시뮬레이션 중..."):
            try:
                # Flask 백엔드로 전송
                files = {"image": image_file}
                data = {"voltage": str(voltage)}
                BACKEND_URL = "http://192.168.0.23:5000/analyze"  # 자신의 PC IP로 변경
                res = requests.post(BACKEND_URL, files=files, data=data)

                if res.status_code == 200:
                    result = res.json()
                    st.success("시뮬레이션 성공 ✅")
                    st.subheader("🔌 생성된 Netlist")
                    st.code(result["netlist"], language="spice")

                    st.subheader("📊 시뮬레이션 결과")
                    st.text(result["result"])
                else:
                    st.error(f"❌ 오류 발생: {res.json().get('error')}")
            except Exception as e:
                st.error(f"❌ 통신 오류: {e}")
