import tkinter as tk

class TaskNotesDialog(tk.Toplevel):
    def __init__(self, parent, task_info):
        super().__init__(parent)
        self.task_info = task_info
        self.result = None
        self.setup_ui()
        
    def setup_ui(self):
        self.title("Task Notes")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Center the dialog
        self.transient(self.master)
        self.grab_set()
        
        # Main container frame
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Top section for task info
        top_frame = tk.Frame(container)
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Task info
        tk.Label(top_frame, text=f"Date: {self.task_info['date']}", font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(top_frame, text=f"Topic: {self.task_info['topic']}", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        
        # Show suggested tasks if available
        if self.task_info.get('suggested_tasks'):
            suggested_frame = tk.Frame(top_frame)
            suggested_frame.pack(fill="x", pady=(0, 10))
            
            tk.Label(suggested_frame, text="Suggested Tasks:", font=("Arial", 10, "bold")).pack(anchor="w")
            suggested_text = tk.Text(suggested_frame, height=3, width=60, wrap="word")
            suggested_text.pack(fill="x", pady=(2, 0))
            suggested_text.insert("1.0", self.task_info['suggested_tasks'])
            suggested_text.config(state="disabled")  # Make it read-only
        
        # Middle section for notes
        middle_frame = tk.Frame(container)
        middle_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Notes section
        tk.Label(middle_frame, text="What was done:").pack(anchor="w")
        self.notes_text = tk.Text(middle_frame, height=12, width=60)
        self.notes_text.pack(fill="both", expand=True, pady=(5, 0))
        
        # Load existing notes if any
        if self.task_info.get('notes'):
            self.notes_text.insert("1.0", self.task_info['notes'])
        
        # Bottom section for buttons
        bottom_frame = tk.Frame(container)
        bottom_frame.pack(fill="x", pady=(10, 0))
        
        # Buttons frame with better spacing
        btn_frame = tk.Frame(bottom_frame)
        btn_frame.pack(expand=True)
        
        # Create buttons with better styling
        save_btn = tk.Button(btn_frame, text="Save Notes Only", command=self.save_notes_only, 
                           bg="lightblue", relief="raised", padx=10, pady=5)
        save_btn.pack(side="left", padx=5)
        
        complete_btn = tk.Button(btn_frame, text="Mark Complete", command=self.mark_complete,
                               bg="lightgreen", relief="raised", padx=10, pady=5)
        complete_btn.pack(side="left", padx=5)
        
        incomplete_btn = tk.Button(btn_frame, text="Mark Incomplete", command=self.mark_incomplete,
                                 bg="lightcoral", relief="raised", padx=10, pady=5)
        incomplete_btn.pack(side="left", padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.cancel,
                             bg="lightgray", relief="raised", padx=10, pady=5)
        cancel_btn.pack(side="right", padx=5)
        
        # Focus on notes text
        self.notes_text.focus()
        
        # Bind Enter key to Mark Complete
        self.bind('<Return>', lambda e: self.mark_complete())
        # Bind Escape key to Cancel
        self.bind('<Escape>', lambda e: self.cancel())
    
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