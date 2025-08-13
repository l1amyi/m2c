import argparse
from mdk2cmake import mdk2cmake

import os

def find_armcc_by_common_path():
    for base in [r".", r"C:\Keil_v5", r"C:\Keil", r"C:\Users\liyi\AppData\Local\Keil_v5"]:
        armcc_path = os.path.join(base, "ARM", "ARMCC", "bin", "armcc.exe")
        if os.path.exists(armcc_path):
            return armcc_path
    return None

def main():
    parser = argparse.ArgumentParser(description="MDK工程转CMake工具")
    parser.add_argument("uvprojx_path", help="uvprojx工程文件路径")
    parser.add_argument("control_string_path", help="控制字符串文件路径")
    parser.add_argument("-o", "--output_dir", default=".", help="输出目录")
    parser.add_argument("-t", "--tool_chain_path", default=None, help="工具链路径")
    args = parser.parse_args()
    
    uvprojx_path = args.uvprojx_path
    control_string_path = args.control_string_path
    output_dir = args.output_dir
    tool_chain_path = args.tool_chain_path
    
    # 调用路径转换函数
    uvprojx_path = uvprojx_path.replace("\\", "/")
    control_string_path = control_string_path.replace("\\", "/")
    output_dir = output_dir.replace("\\", "/")
    tool_chain_path = tool_chain_path.replace("\\", "/") if tool_chain_path else None
    
    if tool_chain_path == None:
        tool_chain_path = find_armcc_by_common_path()
        if tool_chain_path == None:
            print("未找到 armcc 路径")
            return

    mdk2cmake(uvprojx_path, control_string_path, output_dir, tool_chain_path)

if __name__ == "__main__":
    main()
