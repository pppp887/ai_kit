# app.py

import streamlit as st
import tempfile
from ai_netlist import generate_netlist_from_image
from simulator import run_simulation

st.set_page_config(page_title="회로 AI 시뮬레이터", layout="centered")
st.title("🧠 회로 이미지 분석 + 전압 시뮬레이션")

uploaded_file = st.file_uploader("회로 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
voltage = st.number_input("인가할 전압 (V)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_file.read())
        image_path = tmp.name

    if st.button("📤 분석 및 시뮬레이션 실행"):
        with st.spinner("AI 분석 및 Ngspice 시뮬레이션 중..."):
            try:
                netlist = generate_netlist_from_image(image_path)
                result = run_simulation(netlist, voltage)
                st.success("✅ 시뮬레이션 완료!")
                st.code(result)
            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")
