import os
import shutil
import winreg
import glob

# 方法1：环境变量
def find_armcc_by_env():
    return shutil.which("armcc")

# 方法2：注册表
def find_armcc_by_reg():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Keil\Products\MDK")
        path, _ = winreg.QueryValueEx(key, "Path")
        armcc_path = os.path.join(path, "ARM", "ARMCC", "bin", "armcc.exe")
        if os.path.exists(armcc_path):
            return armcc_path
    except Exception:
        pass
    return None

# 方法3：常见路径
def find_armcc_by_common_path():
    for base in [r".", r"C:\Keil_v5", r"C:\Keil", r"C:\Users\liyi\AppData\Local\Keil_v5"]:
        armcc_path = os.path.join(base, "ARM", "ARMCC", "bin", "armcc.exe")
        if os.path.exists(armcc_path):
            return armcc_path
    return None

# 方法4：命令行
def find_armcc_by_cmd():
    import subprocess
    try:
        out = subprocess.check_output("where armcc", shell=True, encoding="gbk")
        return out.strip().splitlines()[0]
    except Exception:
        return None
    
if __name__ == "__main__":
    armcc_path = (find_armcc_by_env() or 
                  find_armcc_by_reg() or 
                  find_armcc_by_common_path() or 
                  find_armcc_by_cmd())
    
    if armcc_path:
        print(f"找到 armcc 路径: {armcc_path}")