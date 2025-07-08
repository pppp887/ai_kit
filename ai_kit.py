# ai_kit
import streamlit as st
from PIL import Image
import uuid
import os

st.set_page_config(page_title="회로 분석 AI", layout="centered")
st.title("🧠 회로 이미지 분석 AI")
st.write("회로 사진을 업로드하고, VCC와 GND 위치를 클릭하세요.")

uploaded_file = st.file_uploader("회로 사진 업로드", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드된 회로", use_column_width=True)

    # 클릭 위치 받기 (Streamlit drawable canvas 사용 필요)
    from streamlit_drawable_canvas import st_canvas

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",  # 클릭 위치 표시
        stroke_width=5,
        background_image=img,
        update_streamlit=True,
        height=img.height,
        width=img.width,
        drawing_mode="point",
        key="canvas",
    )

    # 클릭된 위치 추출
    if canvas_result.json_data and "objects" in canvas_result.json_data:
        clicks = canvas_result.json_data["objects"]
        if len(clicks) >= 2:
            vcc = clicks[0]["left"], clicks[0]["top"]
            gnd = clicks[1]["left"], clicks[1]["top"]
            st.success(f"✅ VCC 위치: {vcc}")
            st.success(f"✅ GND 위치: {gnd}")
            # 다음 단계로 좌표 넘기기
            st.session_state["vcc"] = vcc
            st.session_state["gnd"] = gnd
        else:
            st.warning("❗ 최소 2번 클릭하여 VCC, GND를 지정하세요.")
