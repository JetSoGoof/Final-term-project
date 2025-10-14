import sys
import os
from pathlib import Path

def resource_path(*paths):
    """
    รองรับตอนรันจากซอร์ส และตอนแพ็ก --onefile (PyInstaller)
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *paths)

def user_data_dir(appname="MoneyHype"):
    """
    คืนพาธโฟลเดอร์เก็บข้อมูลถาวรของผู้ใช้ (เขียนได้ใน --onefile)
    """
    home = Path.home()
    if sys.platform.startswith("win"):
        base = os.getenv("APPDATA", str(home / "AppData" / "Roaming"))
        return os.path.join(base, appname)
    elif sys.platform == "darwin":
        return os.path.join(str(home), "Library", "Application Support", appname)
    else:
        return os.path.join(str(home), f".{appname.lower()}")

def money(n: float) -> str:
    """
    จัดรูปแบบตัวเลขเป็นทศนิยม 2 ตำแหน่งพร้อม comma
    """
    try:
        return f"{float(n):,.2f}"
    except (ValueError, TypeError):
        return "0.00"