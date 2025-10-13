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

class App(ctk.CTk):
    def __int__(self):
        super().__init__()
        
        self.title("Money Hype")
        self.geometry("1100x720")
        self.minsize(100, 600)
        ctk.set_appearance_mode("Dark")

        try:
            split_img = Image.open(resource_path("assets/split_icon.png"))
            txn_img = Image.open(resource_path("assets/txn_icon.png"))
            sav_img = Image.open(resource_path("assets/sav_icon.png"))
            self.split_icon = ctk.CTkImage(light_image=split_img, dark_image=split_img, size=(22, 22))
            self.txn_icon = ctk.CTkImage(light_image=txn_img, dark_image=txn_img, size=(22, 22))
            self.sav_icon = ctk.CTkImage(light_image=sav_img, dark_image=sav_img, size=(22, 22))
        except Exception as e:
            print(f"Icon loading error: {e}.")
            self.split_icon = self.txn_icon = self.sav_icon = None


        
