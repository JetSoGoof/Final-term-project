from tkinter import ttk, Canvas
import customtkinter as ctk

class CTkTree(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Inter", 11, "bold"))
        style.configure("Treeview", rowheight=26, font=("Inter", 11))


class CTkDonutChart(ctk.CTkFrame):
    def __init__(self, master, size=180, hole_size_ratio=0.65, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs) # ทำให้ Frame ตัวเองโปร่งใส
        self.size = size
        self.hole_size_ratio = hole_size_ratio
        
        # ใช้สีพื้นหลังของ master ที่แท้จริง
        # **kwargs อาจมี bg_color หรือ fg_color ที่จะถูกส่งต่อมาจาก master**
        # เราจะพยายามดึงค่าสีจาก master โดยตรงถ้าเป็นไปได้ หรือใช้ default
        
        # แก้ไขตรงนี้: ให้ Canvas ใช้สีพื้นหลังของ master ที่เป็น CTkFrame จริงๆ
        # เพื่อให้มันกลืนไปกับ Summary Card
        self.actual_bg_color = master._apply_appearance_mode(master.cget("fg_color"))


        self.canvas = Canvas(self, width=size, height=size, highlightthickness=0, bg=self.actual_bg_color)
        self.canvas.pack()
        
        self.progress = 0.0 # ค่า 0.0 ถึง 1.0
        self.colors = ["#FF6384", "#4BC0C0"] # สี [Expense, Income]
        
        self.canvas.bind("<Configure>", self._on_resize)
        self._draw_chart()

    def _on_resize(self, event):
        self.size = min(event.width, event.height)
        self.canvas.config(width=self.size, height=self.size)
        self._draw_chart()

    def _draw_chart(self):
        self.canvas.delete("all")
        
        center_x, center_y = self.size / 2, self.size / 2
        outer_radius = self.size / 2 - 5
        inner_radius = outer_radius * self.hole_size_ratio

        # วาดพื้นหลังวงกลมสีเทาอ่อน (ส่วนของรายรับที่เหลือ)
        self.canvas.create_oval(center_x - outer_radius, center_y - outer_radius,
                                center_x + outer_radius, center_y + outer_radius,
                                fill=self.colors[1], outline="") # สีเขียวของรายรับ

        # วาดส่วนของรายจ่าย (แดง)
        if self.progress > 0:
            start_angle = 90
            extent_angle = - (self.progress * 360) # วาดทวนเข็มนาฬิกา
            self.canvas.create_arc(center_x - outer_radius, center_y - outer_radius,
                                   center_x + outer_radius, center_y + outer_radius,
                                   start=start_angle, extent=extent_angle,
                                   fill=self.colors[0], outline="")

        # วาดวงกลมตรงกลางเพื่อสร้าง "รู"
        # ใช้ self.actual_bg_color เพื่อให้กลืนกับพื้นหลังของ master
        self.canvas.create_oval(center_x - inner_radius, center_y - inner_radius,
                                center_x + inner_radius, center_y + inner_radius,
                                fill=self.actual_bg_color, outline="")

    def set_progress(self, progress_value):
        self.progress = max(0, min(1, progress_value))
        self._draw_chart()