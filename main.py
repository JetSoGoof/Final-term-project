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
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk. CTkFrame(self, width=220, corner_radius = 0, fq_color = "#1F2937")
        self.sidebar_frame.grid(row=0, colum=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfiqure(4, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="Money Hype", font=ctk.CTkFont(family="Inter", size=22, weight="bold")).pack(pady=25, padx=25)

        self.split_button = ctk.CTkButton(self.sidebar_frame, text=" หารเงิน", image=self.split_icon, compound="left", anchor="w", font=ctk.CTkFont(family="Inter", size=14),
                                           command=lambda: self.select_frame_by_name("split"))
        self.split_button.pack(pady=8, padx=20, fill="x")
        self.txn_button = ctk.CTkButton(self.sidebar_frame, text=" รายรับ-รายจ่าย", image=self.txn_icon, compound="left", anchor="w", font=ctk.CTkFont(family="Inter", size=14),
                                        command=lambda: self.select_frame_by_name("txn"))
        self.txn_button.pack(pady=8, padx=20, fill="x")
        self.sav_button = ctk.CTkButton(self.sidebar_frame, text=" ออมเงิน", image=self.sav_icon, compound="left", anchor="w", font=ctk.CTkFont(family="Inter", size=14),
                                        command=lambda: self.select_frame_by_name("sav"))
        self.sav_button.pack(pady=8, padx=20, fill="x")
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=ctk.set_appearance_mode)
        self.appearance_mode_menu.pack(side="bottom", pady=20, padx=20)

        self.split_frame = SplitTab(self, fg_color="transparent")
        self.txn_frame = TxnTab(self, fg_color="transparent")
        self.sav_frame = SavTab(self, fg_color="transparent")
        
        self.split_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.txn_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.sav_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.select_frame_by_name("split")
        
 def select_frame_by_name(self, name):
        selected_color = ("#3A536B", "#2E4154")
        
        self.split_button.configure(fg_color=selected_color if name == "split" else "transparent")
        self.txn_button.configure(fg_color=selected_color if name == "txn" else "transparent")
        self.sav_button.configure(fg_color=selected_color if name == "sav" else "transparent")

        if name == "split":
            self.split_frame.tkraise()
            self.split_frame._load_split() # สั่งโหลดข้อมูลเมื่อเลือก
        elif name == "txn":
            self.txn_frame.tkraise()
            self.txn_frame.on_tab_selected() # สั่งโหลดข้อมูลเมื่อเลือก
        elif name == "sav":
            self.sav_frame.tkraise()
            self.sav_frame._load_sav() # สั่งโหลดข้อมูลเมื่อเลือก

if __name__ == "__main__":
    app = App()
    app.mainloop()