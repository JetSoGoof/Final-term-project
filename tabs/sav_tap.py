import customtkinter as ctk
from tkinter import messagebox, END
import uuid
from datetime import date, datetime

from db import T_SAV, Q
from utils import money
from widgets import CTkTree

    class SavTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

         self.grid_columnconfigure(0, weight=1)
         self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self, text="ออมเงิน", font=ctk.CTkFont(family="Inter", size=24, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=15)

        input_card = ctk.CTkFrame(self, corner_radius=15)
        input_card.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15))
        input_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_card, text="จำนวนเงินออม").grid(row=0, column=0, sticky="w", padx=20, pady=15)
        self.sav_amount = ctk.CTkEntry(input_card, placeholder_text="0.00", font=ctk.CTkFont(family="Inter", size=14))
        self.sav_amount.grid(row=0, column=1, sticky="ew", padx=20, pady=15)
        ctk.CTkLabel(input_card, text="วันที่").grid(row=1, column=0, sticky="w", padx=20, pady=15)
        self.sav_date = ctk.CTkEntry(input_card, placeholder_text="YYYY-MM-DD", font=ctk.CTkFont(family="Inter", size=14))
        self.sav_date.insert(0, date.today().isoformat())
        self.sav_date.grid(row=1, column=1, sticky="ew", padx=20, pady=15)
        ctk.CTkLabel(input_card, text="โน้ต").grid(row=2, column=0, sticky="w", padx=20, pady=15)
        self.sav_note = ctk.CTkEntry(input_card, placeholder_text="-", font=ctk.CTkFont(family="Inter", size=14))
        self.sav_note.grid(row=2, column=1, sticky="ew", padx=20, pady=15)
        ctk.CTkButton(input_card, text="บันทึกรายการ", command=self._add_sav, font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
                      fg_color="#3B82F6", hover_color="#2563EB").grid(row=3, column=1, sticky="e", padx=20, pady=15)