# simulator.py

import subprocess

def create_netlist_with_voltage(netlist_text: str, voltage: float) -> str:
    lines = netlist_text.splitlines()
    result = []

    for line in lines:
        if line.startswith("V1 "):
            result.append(f"V1 VCC 0 DC {voltage}")
        else:
            result.append(line)

    # 시뮬레이션 명령 추가
    if not any(l.startswith(".dc") for l in result):
        result.insert(-1, ".dc V1 0 {0} 1".format(voltage))
    if not any(l.startswith(".print") for l in result):
        result.insert(-1, ".print dc all")

    return "\n".join(result)

def run_simulation(netlist_text: str, voltage: float) -> str:
    final_netlist = create_netlist_with_voltage(netlist_text, voltage)
    with open("netlist.sp", "w") as f:
        f.write(final_netlist)

    try:
        result = subprocess.run(
            ["ngspice", "-b", "netlist.sp"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"❌ Ngspice 실패:\n{result.stderr}"
    except Exception as e:
        return f"❌ Ngspice 실행 중 오류: {e}"
