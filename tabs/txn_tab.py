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

