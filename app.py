import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import csv
import json
import os
from pathlib import Path

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

class TaskNotesDialog(tk.Toplevel):
    def __init__(self, parent, task_info):
        super().__init__(parent)
        self.task_info = task_info
        self.result = None
        self.setup_ui()
        
    def setup_ui(self):
        self.title("Task Notes")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Center the dialog
        self.transient(parent)
        self.grab_set()
        
        # Main frame
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Task info
        tk.Label(main_frame, text=f"Date: {self.task_info['date']}", font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(main_frame, text=f"Topic: {self.task_info['topic']}", font=("Arial", 10)).pack(anchor="w", pady=(0, 10))
        
        # Notes section
        tk.Label(main_frame, text="What was done:").pack(anchor="w")
        self.notes_text = tk.Text(main_frame, height=10, width=50)
        self.notes_text.pack(fill="both", expand=True, pady=(5, 10))
        
        # Load existing notes if any
        if self.task_info.get('notes'):
            self.notes_text.insert("1.0", self.task_info['notes'])
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="Save Notes Only", command=self.save_notes_only).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Mark Complete", command=self.mark_complete).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Mark Incomplete", command=self.mark_incomplete).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side="right", padx=5)
        
        # Focus on notes text
        self.notes_text.focus()
    
    def save_notes_only(self):
        notes = self.notes_text.get("1.0", "end-1c")
        self.result = {
            'action': 'save_notes',
            'notes': notes,
            'completed': self.task_info.get('completed', False)
        }
        self.destroy()
    
    def mark_complete(self):
        notes = self.notes_text.get("1.0", "end-1c")
        self.result = {
            'action': 'complete',
            'notes': notes,
            'completed': True
        }
        self.destroy()
    
    def mark_incomplete(self):
        notes = self.notes_text.get("1.0", "end-1c")
        self.result = {
            'action': 'incomplete',
            'notes': notes,
            'completed': False
        }
        self.destroy()
    
    def cancel(self):
        self.result = None
        self.destroy()

class LearningTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learning Schedule Tracker")
        self.geometry("800x600")
        
        self.current_file = None
        self.sessions = {}
        
        # Start with file selection
        self.show_file_selection()
    
    def show_file_selection(self):
        # Clear current widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Show file selection frame
        self.file_frame = FileSelectionFrame(self, self.load_schedule)
        self.file_frame.pack(expand=True, fill="both")
    
    def load_schedule(self, file_path):
        self.current_file = file_path
        self.sessions = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    date_str = row['Date'].split(' ')[0]  # Extract just the date part
                    self.sessions[date_str] = {
                        'topic': row['Focus Topic'],
                        'suggested_tasks': row.get('Suggested Tasks', ''),
                        'completed': False,
                        'notes': ''
                    }
            
            self.show_main_interface()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")
    
    def show_main_interface(self):
        # Clear current widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Main interface
        self.setup_main_interface()
    
    def setup_main_interface(self):
        # Header
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(header_frame, text=f"Learning Schedule: {os.path.basename(self.current_file)}", 
                font=("Arial", 14, "bold")).pack(side="left")
        
        tk.Button(header_frame, text="Change File", command=self.show_file_selection).pack(side="right")
        
        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Date", "Topic", "Status", "Notes"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Topic", text="Focus Topic")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Notes", text="Notes")
        
        # Configure column widths
        self.tree.column("Date", width=120)
        self.tree.column("Topic", width=300)
        self.tree.column("Status", width=100)
        self.tree.column("Notes", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate tree
        self.populate_tree()
        
        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(btn_frame, text="Edit Task", command=self.edit_task).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Show Incomplete", command=self.show_incomplete).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Export Progress", command=self.export_progress).pack(side="left", padx=5)
        
        # Bind double-click
        self.tree.bind("<Double-1>", lambda e: self.edit_task())
    
    def populate_tree(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add sessions
        for date, info in self.sessions.items():
            status = "✓ Complete" if info['completed'] else "⏳ Pending"
            notes_preview = info.get('notes', '')[:30] + "..." if len(info.get('notes', '')) > 30 else info.get('notes', '')
            
            self.tree.insert("", "end", iid=date, values=(
                date, 
                info['topic'], 
                status,
                notes_preview
            ))
    
    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return
        
        date = selected[0]
        task_info = self.sessions[date].copy()
        task_info['date'] = date
        
        dialog = TaskNotesDialog(self, task_info)
        self.wait_window(dialog)
        
        if dialog.result:
            result = dialog.result
            self.sessions[date]['notes'] = result['notes']
            self.sessions[date]['completed'] = result['completed']
            self.populate_tree()
    
    def show_incomplete(self):
        incomplete = [day for day, info in self.sessions.items() if not info['completed']]
        if not incomplete:
            messagebox.showinfo("Complete", "All sessions completed! 🎉")
        else:
            incomplete_text = "\n".join([f"{day}: {self.sessions[day]['topic']}" for day in incomplete])
            messagebox.showinfo("Incomplete Sessions", f"Remaining tasks:\n\n{incomplete_text}")
    
    def export_progress(self):
        try:
            export_file = filedialog.asksaveasfilename(
                title="Export Progress",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            
            if export_file:
                with open(export_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Date', 'Topic', 'Status', 'Notes'])
                    
                    for date, info in self.sessions.items():
                        status = "Complete" if info['completed'] else "Pending"
                        writer.writerow([date, info['topic'], status, info.get('notes', '')])
                
                messagebox.showinfo("Success", f"Progress exported to {export_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

if __name__ == "__main__":
    app = LearningTracker()
    app.mainloop()
