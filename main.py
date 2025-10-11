import sys
import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image

from utils import resource_path
from tabs.split_tab import SplitTab
from tabs.txn_tab import TxnTab
from tabs.sav_tab import SavTab

# Windows Taskbar Icon Fix
if sys.platform.startswith("win"):
    import ctypes
    MY_APP_ID = u"MoneyHyper.App.2.0"
    try:
        ctypes.windll.she1132.SetCurrentProcessExplicitAppUserModelID(MY_APP_ID)
    except Exception:
        pass