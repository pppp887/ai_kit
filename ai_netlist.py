import uuid
import requests
import numpy as np
from PIL import Image

API_KEY = "HgOMyTUuZmcqNDrciGkU"
MODEL_ID = "electronic-detection/1"

def generate_node():
    return f"N{uuid.uuid4().hex[:4].upper()}"

def get_color_based_node(image_np, x, y):
    """주변 픽셀 색상 보고 노드 판단"""
    h, w, _ = image_np.shape
    x, y = int(x), int(y)

    area = image_np[max(0, y - 5):min(h, y + 5), max(0, x - 5):min(w, x + 5)]
    avg_color = np.mean(area.reshape(-1, 3), axis=0)  # RGB

    r, g, b = avg_color  # PIL 이미지의 RGB 순서

    if r > 180 and g < 80 and b < 80:
        return "VCC"
    elif r < 50 and g < 50 and b < 50:
        return "0"  # GND
    else:
        return generate_node()

def convert_to_spice(predictions, image_np):
    netlist = []
    count = 1

    for pred in predictions:
        if pred["class"] != "resistor":
            continue

        x_center = pred["x"]
        y_center = pred["y"]
        width = pred["width"]
        height = pred["height"]

        # 단자 두 개 추정 (가로 방향)
        x1, y1 = x_center - width / 2, y_center
        x2, y2 = x_center + width / 2, y_center

        node1 = get_color_based_node(image_np, x1, y1)
        node2 = get_color_based_node(image_np, x2, y2)

        netlist.append(f"R{count} {node1} {node2} 1k")
        count += 1

    netlist.append(".end")
    return "\n".join(netlist)

def run_analysis(image_path):
    # 1. 이미지 불러오기
    image = Image.open(image_path).convert("RGB")
    image_np = np.array(image)

    # 2. Roboflow REST API 호출
    with open(image_path, "rb") as f:
        response = requests.post(
            f"https://detect.roboflow.com/{MODEL_ID}?api_key={API_KEY}",
            files={"file": f},
        )

    if response.status_code != 200:
        raise RuntimeError(f"❌ Roboflow 추론 실패: {response.text}")

    predictions = response.json()["predictions"]

    # 3. Netlist 생성
    netlist = convert_to_spice(predictions, image_np)

    # 4. 저장
    with open("netlist.sp", "w") as f:
        f.write(netlist)

    print("=== Netlist 생성 결과 ===")
    print(netlist)
    return netlist
