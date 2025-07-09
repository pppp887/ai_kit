import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(layout="centered")
st.title("🔌 회로 이미지 위 클릭 테스트")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    np_image = np.array(image)
    height, width = np_image.shape[0], np_image.shape[1]

    st.image(image, caption="회로 이미지", use_column_width=True)
    st.markdown("🖱️ 이미지 위를 클릭하면 점이 찍힙니다.")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.6)",  # 클릭된 점 표시 색
        stroke_width=10,
        stroke_color="#FF0000",
        background_image=Image.fromarray(np_image),
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="point",   # ← 클릭 모드
        key="canvas",
    )

    if canvas_result.json_data and "objects" in canvas_result.json_data:
        points = canvas_result.json_data["objects"]
        if points:
            coords = [(round(obj["left"]), round(obj["top"])) for obj in points]
            st.success(f"✅ 클릭된 좌표들: {coords}")
        else:
            st.info("🖱️ 클릭하면 여기에 좌표가 표시됩니다.")
    else:
        st.info("🖱️ 이미지를 클릭해보세요.")
else:
    st.info("⬆️ 이미지를 먼저 업로드해주세요.")
