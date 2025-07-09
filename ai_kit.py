import streamlit as st
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="회로 AI 툴킷", layout="centered")
st.title("🔌 회로 이미지 업로드 및 VCC/GND 지정")

uploaded_file = st.file_uploader("회로 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        np_image = np.array(image)  # numpy 배열로 강제 변환

        st.image(image, caption="업로드된 회로 이미지", use_column_width=True)
        st.markdown("🖱️ 이미지 위를 **두 번 클릭**하여 VCC와 GND 위치를 선택하세요.")

        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=5,
            background_image=Image.fromarray(np_image),  # numpy → PIL → canvas
            update_streamlit=True,
            height=np_image.shape[0],
            width=np_image.shape[1],
            drawing_mode="point",
            key="canvas",
        )

        if canvas_result.json_data and "objects" in canvas_result.json_data:
            clicks = canvas_result.json_data["objects"]
            if len(clicks) >= 2:
                vcc = clicks[0]["left"], clicks[0]["top"]
                gnd = clicks[1]["left"], clicks[1]["top"]
                st.success(f"✅ VCC 좌표: {vcc}")
                st.success(f"✅ GND 좌표: {gnd}")
            else:
                st.info("🖱️ 최소 두 번 클릭해야 VCC와 GND를 지정할 수 있습니다.")
        else:
            st.info("🖱️ 캔버스를 클릭해보세요!")
    except Exception as e:
        st.error(f"❌ 이미지 처리 중 오류 발생: {e}")
else:
    st.info("이미지를 업로드하면 시작할 수 있습니다.")

