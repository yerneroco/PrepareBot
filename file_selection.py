import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

class FileSelectionFrame(tk.Frame):
    def __init__(self, parent, on_file_selected):
        super().__init__(parent)
        self.on_file_selected = on_file_selected
        self.setup_ui()
        self.load_last_file()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self, text="Learning Schedule Tracker", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # File selection frame
        file_frame = tk.Frame(self)
        file_frame.pack(pady=20)
        
        tk.Label(file_frame, text="Select CSV File:").pack()
        
        # File path display
        self.file_path_var = tk.StringVar()
        self.file_path_label = tk.Label(file_frame, textvariable=self.file_path_var, 
                                      wraplength=400, fg="blue")
        self.file_path_label.pack(pady=5)
        
        # Buttons
        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Browse Files", command=self.browse_file).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Use Last File", command=self.use_last_file).pack(side="left", padx=5)
        
        # Load button
        self.load_btn = tk.Button(file_frame, text="Load Schedule", command=self.load_file, 
                                 state="disabled", bg="green", fg="white")
        self.load_btn.pack(pady=10)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.load_btn.config(state="normal")
    
    def use_last_file(self):
        last_file = self.get_last_file()
        if last_file and os.path.exists(last_file):
            self.file_path_var.set(last_file)
            self.load_btn.config(state="normal")
        else:
            messagebox.showwarning("Warning", "No previous file found or file no longer exists.")
    
    def load_file(self):
        file_path = self.file_path_var.get()
        if file_path and os.path.exists(file_path):
            self.save_last_file(file_path)
            self.on_file_selected(file_path)
        else:
            messagebox.showerror("Error", "Please select a valid CSV file.")
    
    def load_last_file(self):
        last_file = self.get_last_file()
        if last_file and os.path.exists(last_file):
            self.file_path_var.set(last_file)
            self.load_btn.config(state="normal")
    
    def get_last_file(self):
        try:
            with open("last_file.json", "r") as f:
                data = json.load(f)
                return data.get("last_file")
        except:
            return None
    
    def save_last_file(self, file_path):
        try:
            with open("last_file.json", "w") as f:
                json.dump({"last_file": file_path}, f)
        except:
            pass 