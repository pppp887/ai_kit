import cv2
import uuid
import numpy as np
from PIL import Image
from inference_sdk import InferenceHTTPClient

API_KEY = "YOUR_API_KEY"
MODEL_ID = "electronic-detection/1"

def generate_node():
    return f"N{uuid.uuid4().hex[:4].upper()}"

def get_color_based_node(image, x, y):
    """주변 픽셀 색상 보고 노드 판단"""
    h, w, _ = image.shape
    x, y = int(x), int(y)

    # 반경 5픽셀 내 평균색 계산
    area = image[max(0, y-5):min(h, y+5), max(0, x-5):min(w, x+5)]
    avg_color = np.mean(area.reshape(-1, 3), axis=0)  # BGR

    b, g, r = avg_color

    if r > 180 and g < 80 and b < 80:
        return "VCC"
    elif r < 50 and g < 50 and b < 50:
        return "0"  # GND
    else:
        return generate_node()

def convert_to_spice(predictions, image_path):
    image = cv2.imread(image_path)
    netlist = []
    count = 1

    for pred in predictions:
        if pred["class"] != "resistor":
            continue

        x_center = pred["x"]
        y_center = pred["y"]
        width = pred["width"]
        height = pred["height"]

        # 단자 두 개 추정 (가로 배치 기준)
        x1, y1 = x_center - width / 2, y_center
        x2, y2 = x_center + width / 2, y_center

        node1 = get_color_based_node(image, x1, y1)
        node2 = get_color_based_node(image, x2, y2)

        netlist.append(f"R{count} {node1} {node2} 1k")
        count += 1

    netlist.append(".end")
    return "\n".join(netlist)

def run_analysis(img_path):
    client = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=API_KEY
    )
    result = client.infer(img_path, model_id=MODEL_ID)
    netlist = convert_to_spice(result["predictions"], img_path)

    print("=== Netlist 생성 결과 ===")
    print(netlist)

    with open("netlist.sp", "w") as f:
        f.write(netlist)

    return netlist
