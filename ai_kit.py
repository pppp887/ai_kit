#ai_kit
import streamlit as st
from PIL import Image, UnidentifiedImageError
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="회로 AI 툴킷", layout="centered")
st.title("🔌 회로 이미지 업로드 및 VCC/GND 지정")

st.markdown("🖼️ 이미지를 업로드한 뒤, **두 번 클릭**하여 VCC와 GND 위치를 선택하세요.")
st.markdown("*지원 포맷: JPG, PNG*")

uploaded_file = st.file_uploader("회로 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        # PIL로 이미지 열기 + RGB 변환
        image = Image.open(uploaded_file).convert("RGB")
        width, height = image.size

        st.image(image, caption="업로드된 회로 이미지", use_column_width=True)

        # 캔버스 위 클릭 인터페이스
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=5,
            background_image=image,
            update_streamlit=True,
            height=height,
            width=width,
            drawing_mode="point",
            key="canvas",
        )

        # 클릭된 점 좌표 추출
        if canvas_result.json_data and "objects" in canvas_result.json_data:
            clicks = canvas_result.json_data["objects"]
            num_clicks = len(clicks)

            if num_clicks >= 2:
                vcc = clicks[0]["left"], clicks[0]["top"]
                gnd = clicks[1]["left"], clicks[1]["top"]
                st.success(f"✅ VCC 좌표: {vcc}")
                st.success(f"✅ GND 좌표: {gnd}")

                # 추후 처리에 사용할 세션 저장
                st.session_state["vcc"] = vcc
                st.session_state["gnd"] = gnd
                st.session_state["image"] = uploaded_file

                # 다음 단계 버튼
                if st.button("📤 분석 시작"):
                    st.write("🔍 AI 모델 호출 준비 중...")
                    # 여기서 inference 코드로 넘어감 (다음 단계 구현)
            else:
                st.info("🖱️ 두 번 클릭해야 VCC, GND 좌표가 지정됩니다.")
        else:
            st.info("🖱️ 캔버스 위를 클릭해보세요. (두 점)")
    except UnidentifiedImageError:
        st.error("⚠️ 이미지 파일이 손상되었거나 지원되지 않는 형식입니다.")
else:
    st.info("이미지를 업로드하면 시작할 수 있습니다.")

