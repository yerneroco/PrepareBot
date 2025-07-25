import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from task_dialog import TaskNotesDialog

class TaskActions:
    def __init__(self, main_app):
        self.main_app = main_app
    
    def edit_task(self):
        """Handle editing a selected task"""
        selected = self.main_app.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return
        
        date = selected[0]
        task_info = self.main_app.sessions[date].copy()
        task_info['date'] = date
        
        dialog = TaskNotesDialog(self.main_app, task_info)
        self.main_app.wait_window(dialog)
        
        if dialog.result:
            result = dialog.result
            self.main_app.sessions[date]['notes'] = result['notes']
            self.main_app.sessions[date]['completed'] = result['completed']
            self.main_app.populate_tree()
    
    def show_incomplete(self):
        """Show list of incomplete tasks"""
        incomplete = [day for day, info in self.main_app.sessions.items() if not info['completed']]
        if not incomplete:
            messagebox.showinfo("Complete", "All sessions completed! 🎉")
        else:
            incomplete_text = "\n".join([f"{day}: {self.main_app.sessions[day]['topic']}" for day in incomplete])
            messagebox.showinfo("Incomplete Sessions", f"Remaining tasks:\n\n{incomplete_text}")
    
    def export_progress(self):
        """Export progress to CSV file"""
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
                    
                    for date, info in self.main_app.sessions.items():
                        status = "Complete" if info['completed'] else "Pending"
                        writer.writerow([date, info['topic'], status, info.get('notes', '')])
                
                messagebox.showinfo("Success", f"Progress exported to {export_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}") 