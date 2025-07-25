import tkinter as tk
from tkinter import ttk
import os

class MainInterface:
    def __init__(self, main_app):
        self.main_app = main_app
    
    def setup_main_interface(self):
        """Setup the main interface with treeview and buttons"""
        # Header
        header_frame = tk.Frame(self.main_app)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(header_frame, text=f"Learning Schedule: {os.path.basename(self.main_app.current_file)}", 
                font=("Arial", 14, "bold")).pack(side="left")
        
        tk.Button(header_frame, text="Change File", command=self.main_app.show_file_selection).pack(side="right")
        
        # Treeview
        tree_frame = tk.Frame(self.main_app)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.main_app.tree = ttk.Treeview(tree_frame, columns=("Category", "Date", "Topic", "Status", "Notes"), show="headings")
        self.main_app.tree.heading("Category", text="Category")
        self.main_app.tree.heading("Date", text="Date")
        self.main_app.tree.heading("Topic", text="Focus Topic")
        self.main_app.tree.heading("Status", text="Status")
        self.main_app.tree.heading("Notes", text="Notes")
        
        # Configure column widths
        self.main_app.tree.column("Category", width=120)
        self.main_app.tree.column("Date", width=100)
        self.main_app.tree.column("Topic", width=250)
        self.main_app.tree.column("Status", width=100)
        self.main_app.tree.column("Notes", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.main_app.tree.yview)
        self.main_app.tree.configure(yscrollcommand=scrollbar.set)
        
        self.main_app.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate tree
        self.populate_tree()
        
        # Buttons
        btn_frame = tk.Frame(self.main_app)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(btn_frame, text="Edit Task", command=self.main_app.task_actions.edit_task).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Show Incomplete", command=self.main_app.task_actions.show_incomplete).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save", command=self.main_app.task_actions.save_progress).pack(side="left", padx=5)
        self.autosave_btn = tk.Button(btn_frame, text="Enable Autosave", command=self.main_app.task_actions.toggle_autosave)
        self.autosave_btn.pack(side="left", padx=5)
        
        # Bind double-click
        self.main_app.tree.bind("<Double-1>", lambda e: self.main_app.task_actions.edit_task())
    
    def populate_tree(self):
        """Populate the treeview with categorized session data"""
        # Clear existing items
        for item in self.main_app.tree.get_children():
            self.main_app.tree.delete(item)
        
        # Get categorized sessions
        from csv_loader import CSVLoader
        categories = CSVLoader.categorize_dates(self.main_app.sessions)
        
        # Add sessions by category
        for category_name, category_items in categories.items():
            if category_items:  # Only show categories with items
                # Sort items within each category by date
                category_items.sort(key=lambda x: x[0])
                
                for date, info in category_items:
                    status = "✓ Complete" if info['completed'] else "⏳ Pending"
                    notes_preview = info.get('notes', '')[:30] + "..." if len(info.get('notes', '')) > 30 else info.get('notes', '')
                    
                    self.main_app.tree.insert("", "end", iid=date, values=(
                        category_name,
                        date, 
                        info['topic'], 
                        status,
                        notes_preview
                    ))
    
    def update_autosave_button(self, enabled):
        """Update autosave button text based on state"""
        if hasattr(self, 'autosave_btn'):
            if enabled:
                self.autosave_btn.config(text="Disable Autosave", bg="red", fg="white")
            else:
                self.autosave_btn.config(text="Enable Autosave", bg="SystemButtonFace", fg="black") 