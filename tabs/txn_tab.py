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
