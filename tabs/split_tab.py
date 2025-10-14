import customtkinter as ctk
from tkinter import messagebox
import uuid
from datetime import date, datetime

from db import T_SPL, Q
from utils import money
from widgets import CTkTree

class SplitTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self, text="หารเงิน", font=ctk.CTkFont(family="Inter", size=24, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=15)

        # Input Card
        input_card = ctk.CTkFrame(self, corner_radius=15)
        input_card.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15))
        input_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_card, text="ยอดเงินรวม").grid(row=0, column=0, sticky="w", padx=20, pady=15)
        self.split_total = ctk.CTkEntry(input_card, placeholder_text="0.00", font=ctk.CTkFont(family="Inter", size=14))
        self.split_total.grid(row=0, column=1, sticky="ew", padx=20, pady=15)

        ctk.CTkLabel(input_card, text="จำนวนคน").grid(row=1, column=0, sticky="w", padx=20, pady=15)
        self.split_people = ctk.CTkEntry(input_card, placeholder_text="จำนวนคน", font=ctk.CTkFont(family="Inter", size=14))
        self.split_people.grid(row=1, column=1, sticky="ew", padx=20, pady=15)

        ctk.CTkButton(input_card, text="คำนวณ", command=self._do_split, font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
                      fg_color="#3B82F6", hover_color="#2563EB").grid(row=2, column=1, sticky="e", padx=20, pady=15)

        self.split_result = ctk.CTkLabel(input_card, text="ต่อคน: -", font=ctk.CTkFont(family="Inter", size=18, weight="bold"))
        self.split_result.grid(row=2, column=0, sticky="w", padx=20, pady=15)


        # History Table Card
        table_card = ctk.CTkFrame(self, corner_radius=15)
        table_card.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(table_card, text="ประวัติการหารเงิน", font=ctk.CTkFont(family="Inter", size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=20, pady=20)

        cols = ("date", "total", "people", "per", "id")
        self.split_table = CTkTree(table_card, columns=cols, show="headings", height=16)
        for c, w in zip(cols, (160, 160, 120, 160, 0)):
            self.split_table.heading(c, text=c.upper())
            self.split_table.column(c, width=w, anchor="w")
        self.split_table.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))

        sb = ctk.CTkScrollbar(table_card, command=self.split_table.yview)
        sb.grid(row=1, column=1, sticky="ns", pady=(0, 10))
        self.split_table.configure(yscroll=sb.set)

        ctk.CTkButton(table_card, text="ลบรายการที่เลือก", fg_color="#EF4444", hover_color="#DC2626", font=ctk.CTkFont(family="Inter", size=14, weight="bold")).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 20))

        self._load_split()

    # --- Methods (เหมือนเดิม) ---
    def _do_split(self):
        try: total = float(self.split_total.get().strip())
        except Exception: messagebox.showerror("ผิดพลาด", "กรอกยอดรวมและจำนวนคนให้ถูกต้อง"); return
        people = int(self.split_people.get().strip())
        if people <= 0: messagebox.showerror("ผิดพลาด", "จำนวนคนต้องมากกว่า 0"); return
        per = round(total / people, 2)
        self.split_result.configure(text=f"ต่อคน: {money(per)} บาท")
        doc = {"split_id": str(uuid.uuid4()), "total_amount": total, "people_count": people, "per_person": per, "date": date.today().isoformat(), "created_at": datetime.utcnow().isoformat()}
        T_SPL.insert(doc)
        self._load_split()

    def _load_split(self):
        for i in self.split_table.get_children(): self.split_table.delete(i)
        docs = T_SPL.all()
        docs.sort(key=lambda x: (x.get("date",""), x.get("created_at","")), reverse=True)
        for s in docs: self.split_table.insert("", "end", values=(s.get("date",""), money(s.get("total_amount",0)), s.get("people_count",""), money(s.get("per_person",0)), s.get("split_id","")))

    def _del_selected_split(self):
        sel = self.split_table.selection()
        if not sel: return
        if not messagebox.askyesno("ยืนยัน", "ลบรายการที่เลือก?"): return
        for it in sel:
            row = self.split_table.item(it)["values"]
            sid = row[-1]
            T_SPL.remove(Q.split_id == sid)
        self._load_split()