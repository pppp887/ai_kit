# backend.py
from flask import Flask, request, jsonify
import tempfile
import os
from ai_netlist import generate_netlist_from_image
from simulator import run_simulation

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files or "voltage" not in request.form:
        return jsonify({"error": "이미지 파일과 전압 값을 모두 제공해야 합니다."}), 400

    image_file = request.files["image"]
    voltage = float(request.form["voltage"])

    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image_path = tmp.name
        image_file.save(image_path)

    try:
        netlist = generate_netlist_from_image(image_path)
        result = run_simulation(netlist, voltage)
        os.remove(image_path)
        return jsonify({"netlist": netlist, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
