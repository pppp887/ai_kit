# ai_netlist.py

import uuid
import requests
import numpy as np
from PIL import Image

API_KEY = "HgOMyTUuZmcqNDrciGkU"
MODEL_ID = "electronic-detection/1"

def generate_node():
    return f"N{uuid.uuid4().hex[:4].upper()}"

def get_color_based_node(image_np, x, y):
    h, w, _ = image_np.shape
    x, y = int(x), int(y)
    area = image_np[max(0, y-5):min(h, y+5), max(0, x-5):min(w, x+5)]
    avg_color = np.mean(area.reshape(-1, 3), axis=0)
    r, g, b = avg_color
    if r > 180 and g < 80 and b < 80:
        return "VCC"
    elif r < 50 and g < 50 and b < 50:
        return "0"
    else:
        return generate_node()

def convert_to_netlist(predictions, image_np):
    netlist = []
    count = 1
    used_nodes = set()

    for pred in predictions:
        if pred["class"] != "resistor":
            continue
        x, y = pred["x"], pred["y"]
        w, h = pred["width"], pred["height"]
        x1, y1 = x - w / 2, y
        x2, y2 = x + w / 2, y

        node1 = get_color_based_node(image_np, x1, y1)
        node2 = get_color_based_node(image_np, x2, y2)

        netlist.append(f"R{count} {node1} {node2} 1k")
        used_nodes.update([node1, node2])
        count += 1

    return "\n".join(netlist), used_nodes

def generate_netlist_from_image(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    image_np = np.array(image)

    with open(image_path, "rb") as f:
        response = requests.post(
            f"https://detect.roboflow.com/{MODEL_ID}?api_key={API_KEY}",
            files={"file": f}
        )
    if response.status_code != 200:
        raise RuntimeError(f"Roboflow 오류: {response.text}")
    
    predictions = response.json()["predictions"]
    body, used_nodes = convert_to_netlist(predictions, image_np)

    lines = []
    if "VCC" in used_nodes:
        lines.append("V1 VCC 0 DC 5")
    lines += body.splitlines()
    lines.append(".end")

    return "\n".join(lines)
