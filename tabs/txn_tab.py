import customtkinter as ctk
from tkinter import messagebox, END
import uuid
from datetime import date, datetime

from db import T_TXNS, Q
from utils import money
from widgets import CTkTree, CTkDonutChart

class AnimatedNumberLabel(ctk.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.current_value = 0.0
        self.target_value = 0.0
        self.animation_steps = 20
        self.animation_id = None

    def animate_to(self, target):
        if self.animation_id: self.after_cancel(self.animation_id)
        self.target_value = target
        self.step = (self.target_value - self.current_value) / self.animation_steps
        self._update_animation()

    def _update_animation(self):
        if (self.step > 0 and self.current_value < self.target_value) or \
           (self.step < 0 and self.current_value > self.target_value):
            self.current_value += self.step
            self.configure(text=money(self.current_value))
            self.animation_id = self.after(15, self._update_animation)
        else:
            self.current_value = self.target_value
            self.configure(text=money(self.target_value))
            self.animation_id = None


class TxnTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self, text="รายรับ-รายจ่าย", font=ctk.CTkFont(family="Inter", size=24, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=15)
        main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_content_frame.grid(row=1, column=0, sticky="nsew", padx=10)
        main_content_frame.grid_columnconfigure(0, weight=1)
        main_content_frame.grid_columnconfigure(1, weight=1)
        main_content_frame.grid_rowconfigure(0, weight=1)

        add_card = ctk.CTkFrame(main_content_frame, corner_radius=15)
        add_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)
        add_card.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(add_card, text="เพิ่มรายการใหม่", font=ctk.CTkFont(family="Inter", size=18, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=20)
        ctk.CTkLabel(add_card, text="จำนวนเงิน").grid(row=1, column=0, sticky="w", padx=20, pady=8)
        self.txn_amount = ctk.CTkEntry(add_card, placeholder_text="0.00", font=ctk.CTkFont(family="Inter", size=14))
        self.txn_amount.grid(row=1, column=1, sticky="ew", padx=20, pady=8)
        ctk.CTkLabel(add_card, text="ประเภท").grid(row=2, column=0, sticky="w", padx=20, pady=8)
        self.txn_direction = ctk.CTkOptionMenu(add_card, values=["EXPENSE", "INCOME"], font=ctk.CTkFont(family="Inter", size=14))
        self.txn_direction.set("EXPENSE")
        self.txn_direction.grid(row=2, column=1, sticky="ew", padx=20, pady=8)
        ctk.CTkLabel(add_card, text="หมวดหมู่").grid(row=3, column=0, sticky="w", padx=20, pady=8)
        self.txn_category = ctk.CTkEntry(add_card, placeholder_text="เช่น ค่าอาหาร, เงินเดือน", font=ctk.CTkFont(family="Inter", size=14))
        self.txn_category.grid(row=3, column=1, sticky="ew", padx=20, pady=8)
        ctk.CTkLabel(add_card, text="วันที่").grid(row=4, column=0, sticky="w", padx=20, pady=8)
        self.txn_date = ctk.CTkEntry(add_card, placeholder_text="YYYY-MM-DD", font=ctk.CTkFont(family="Inter", size=14))
        self.txn_date.insert(0, date.today().isoformat())
        self.txn_date.grid(row=4, column=1, sticky="ew", padx=20, pady=8)
        ctk.CTkLabel(add_card, text="โน้ต").grid(row=5, column=0, sticky="w", padx=20, pady=8)
        self.txn_note = ctk.CTkEntry(add_card, placeholder_text="-", font=ctk.CTkFont(family="Inter", size=14))
        self.txn_note.grid(row=5, column=1, sticky="ew", padx=20, pady=8)
        ctk.CTkButton(add_card, text="บันทึกรายการ", command=self._add_txn, font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
                      fg_color="#3B82F6", hover_color="#2563EB").grid(row=6, column=1, sticky="e", padx=20, pady=20)

        summary_card = ctk.CTkFrame(main_content_frame, corner_radius=15)
        summary_card.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        summary_card.grid_columnconfigure((0, 1), weight=1)
        summary_card.grid_rowconfigure(1, weight=1)