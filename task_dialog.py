import tkinter as tk

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
        self.transient(self.master)
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