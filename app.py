import streamlit as st
from PIL import Image
import tempfile
import os
from ai_netlist import run_analysis  # ← 당신의 ai_netlist.py 함수 가져오기

st.set_page_config(page_title="회로 분석 AI", layout="centered")
st.title("🧠 회로 이미지로 Netlist 자동 생성")

uploaded_file = st.file_uploader("회로 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="업로드된 회로 이미지", use_column_width=True)

    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    if st.button("📤 AI 분석 및 Netlist 생성"):
        with st.spinner("AI 분석 중..."):
            netlist = run_analysis(tmp_path)  # ← ai_netlist.py 안의 함수 호출
            st.success("✅ Netlist 생성 완료")
            st.code(netlist, language="spice")

        os.remove(tmp_path)  # 임시 이미지 삭제
