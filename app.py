# CashMate — CustomTkinter + TinyDB (พร้อมไอคอน Taskbar บน Windows + รองรับ PyInstaller)
# ติดตั้ง: pip install customtkinter tinydb

import sys
import os
import uuid
from pathlib import Path
from datetime import date, datetime
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from tinydb import TinyDB, Query
