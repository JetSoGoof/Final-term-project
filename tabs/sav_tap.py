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
        
        self.sav_total = ctk.CTkLabel(input_card, text="ยอดออมสะสม: 0.00", font=ctk.CTkFont(family="Inter", size=18, weight="bold"))
        self.sav_total.grid(row=3, column=0, sticky="w", padx=20, pady=15)

        table_card = ctk.CTkFrame(self, corner_radius=15)
        table_card.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(table_card, text="ประวัติการออม", font=ctk.CTkFont(family="Inter", size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=20, pady=20)
        cols = ("date", "amount", "note", "id")
        self.sav_table = CTkTree(table_card, columns=cols, show="headings", height=16)
        for c, w in zip(cols, (160, 160, 580, 0)):
            self.sav_table.heading(c, text=c.upper()); self.sav_table.column(c, width=w, anchor="w")
        self.sav_table.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        sb = ctk.CTkScrollbar(table_card, command=self.sav_table.yview)
        sb.grid(row=1, column=1, sticky="ns", pady=(0, 10))
        self.sav_table.configure(yscroll=sb.set)
        ctk.CTkButton(table_card, text="ลบรายการที่เลือก", command=self._del_selected_sav, fg_color="#EF4444", hover_color="#DC2626", font=ctk.CTkFont(family="Inter", size=14, weight="bold")).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 20))

        self._load_sav()

    def _add_sav(self):
        try: amount = float(self.sav_amount.get().strip())
        except Exception: messagebox.showerror("ผิดพลาด", "กรอกจำนวนเงินเป็นตัวเลข"); return
        day = self.sav_date.get().strip() or date.today().isoformat()
        note = self.sav_note.get().strip()
        doc = {"saving_id": str(uuid.uuid4()),"amount": amount,"note": note,"date": day,"created_at": datetime.utcnow().isoformat()}
        T_SAV.insert(doc)
        self.sav_amount.delete(0, END); self.sav_note.delete(0, END)
        self._load_sav()

        def _load_sav(self):
        for i in self.sav_table.get_children(): self.sav_table.delete(i)
        docs = T_SAV.all(); docs.sort(key=lambda x: (x.get("date",""), x.get("created_at","")), reverse=True)
        total = 0.0
        for s in docs:
            amt = float(s.get("amount", 0)); total += amt
            self.sav_table.insert("", "end", values=(s.get("date",""), money(amt), s.get("note",""), s.get("saving_id","")))
        self.sav_total.configure(text=f"ยอดออมสะสม: {money(total)}")

    def _del_selected_sav(self):
        sel = self.sav_table.selection()
        if not sel: return
        if not messagebox.askyesno("ยืนยัน", "ลบรายการที่เลือก?"): return
        for it in sel:
            row = self.sav_table.item(it)["values"]; sid = row[-1]
            T_SAV.remove(Q.saving_id == sid)
        self._load_sav()