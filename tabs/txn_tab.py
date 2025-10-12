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
        
        ctk.CTkLabel(summary_card, text="สรุปยอดเดือนนี้", font=ctk.CTkFont(family="Inter", size=18, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=20)
        
        # แก้ไขตรงนี้: ไม่ต้องส่ง fg_color="transparent" แล้ว
        self.donut_chart = CTkDonutChart(summary_card, size=200) 
        self.donut_chart.grid(row=1, column=0, columnspan=2, pady=(10, 20), sticky="n")
        
        # self.sum_net_label จะอยู่บน canvas ของ donut_chart
        self.sum_net_label = AnimatedNumberLabel(self.donut_chart.canvas, text="0.00", font=ctk.CTkFont(family="Inter", size=32, weight="bold"), fg_color="transparent")
        self.sum_net_label.place(relx=0.5, rely=0.5, anchor="center")
        
        inc_frame = ctk.CTkFrame(summary_card, fg_color="transparent")
        inc_frame.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))
        ctk.CTkLabel(inc_frame, text="รายรับ", text_color="#A0A0A0", font=ctk.CTkFont(family="Inter", size=12)).pack(anchor="w")
        self.sum_inc = AnimatedNumberLabel(inc_frame, text="0.00", font=ctk.CTkFont(family="Inter", size=22, weight="bold"), text_color="#4BC0C0")
        self.sum_inc.pack(anchor="w")
        exp_frame = ctk.CTkFrame(summary_card, fg_color="transparent")
        exp_frame.grid(row=2, column=1, sticky="e", padx=20, pady=(10, 5))
        ctk.CTkLabel(exp_frame, text="รายจ่าย", text_color="#A0A0A0", font=ctk.CTkFont(family="Inter", size=12)).pack(anchor="e")
        self.sum_exp = AnimatedNumberLabel(exp_frame, text="0.00", font=ctk.CTkFont(family="Inter", size=22, weight="bold"), text_color="#FF6384")
        self.sum_exp.pack(anchor="e")
        
        table_card = ctk.CTkFrame(self, corner_radius=15)
        table_card.grid(row=2, column=0, sticky="nsew", padx=10, pady=(15, 10))
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(table_card, text="ประวัติรายการ", font=ctk.CTkFont(family="Inter", size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=20, pady=20)
        cols = ("date", "direction", "category", "amount", "note", "id")
        self.txn_table = CTkTree(table_card, columns=cols, show="headings")
        for c, w in zip(cols, (100, 80, 120, 100, 250, 0)):
            self.txn_table.heading(c, text=c.upper()); self.txn_table.column(c, width=w, anchor="w")
        self.txn_table.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,10))
        sb = ctk.CTkScrollbar(table_card, command=self.txn_table.yview)
        sb.grid(row=1, column=1, sticky="ns", pady=(0,10))
        self.txn_table.configure(yscroll=sb.set)
        ctk.CTkButton(table_card, text="ลบรายการที่เลือก", command=self._del_selected_txn, fg_color="#EF4444", hover_color="#DC2626", font=ctk.CTkFont(family="Inter", size=14, weight="bold")).grid(row=2, column=0, sticky="w", padx=20, pady=(0,20))

        self.on_tab_selected()

    def on_tab_selected(self):
        self._load_txns()

    def _add_txn(self):
        try: amount = float(self.txn_amount.get().strip())
        except Exception: messagebox.showerror("ผิดพลาด", "กรอกจำนวนเงินเป็นตัวเลข"); return
        direction = self.txn_direction.get().upper()
        category  = self.txn_category.get().strip()
        note      = self.txn_note.get().strip()
        day       = self.txn_date.get().strip() or date.today().isoformat()
        if not category: messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณาใส่หมวดหมู่"); return
        if direction == "EXPENSE" and amount > 0: amount = -amount
        if direction == "INCOME"  and amount < 0: amount = -amount
        doc = {"txn_id": str(uuid.uuid4()),"amount": amount,"direction": direction,"category": category,"note": note,"date": day,"created_at": datetime.utcnow().isoformat()}
        T_TXNS.insert(doc)
        self.txn_amount.delete(0, END); self.txn_note.delete(0, END); self.txn_category.delete(0, END)
        self._load_txns()
    
    def _load_txns(self):
        ym = date.today().strftime("%Y-%m")
        docs = [t for t in T_TXNS.all() if str(t.get("date","")).startswith(ym)]
        docs.sort(key=lambda x: (x.get("date",""), x.get("created_at","")), reverse=True)
        for i in self.txn_table.get_children(): self.txn_table.delete(i)
        
        inc, exp = 0.0, 0.0
        for t in docs:
            amt = float(t.get("amount", 0))
            if t.get("direction") == "INCOME": inc += abs(amt)
            else: exp += abs(amt) if amt < 0 else amt
            self.txn_table.insert("","end",values=(t.get("date",""),t.get("direction",""),t.get("category",""),money(amt),t.get("note",""),t.get("txn_id","")))
        
        net = inc - exp
        
        self.sum_inc.animate_to(inc); self.sum_exp.animate_to(exp); self.sum_net_label.animate_to(net)
        
        progress = exp / inc if inc > 0 else (1 if exp > 0 else 0)
        self.donut_chart.set_progress(progress)

    def _del_selected_txn(self):
        sel = self.txn_table.selection()
        if not sel: return
        if not messagebox.askyesno("ยืนยัน", "ลบรายการที่เลือก?"): return
        for it in sel:
            row = self.txn_table.item(it)["values"]
            tid = row[-1]
            T_TXNS.remove(Q.txn_id == tid)
        self._load_txns()x