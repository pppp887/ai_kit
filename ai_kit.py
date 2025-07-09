import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(layout="centered")
st.title("🔌 회로 이미지 클릭 테스트")

uploaded_file = st.file_uploader("회로 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    np_img = np.array(image)
    height, width = np_img.shape[0:2]

    st.image(image, caption="업로드된 이미지", use_column_width=True)
    st.markdown("🖱️ 이미지를 클릭하여 VCC / GND를 지정해보세요.")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=10,
        background_image=Image.fromarray(np_img),
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data and "objects" in canvas_result.json_data:
        objects = canvas_result.json_data["objects"]
        if objects:
            st.success(f"🎯 클릭된 좌표: {[(obj['left'], obj['top']) for obj in objects]}")
        else:
            st.info("🖱️ 이미지를 클릭해보세요.")
else:
    st.info("⬆️ 이미지를 먼저 업로드하세요.")
