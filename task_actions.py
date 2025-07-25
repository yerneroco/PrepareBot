import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import datetime
import threading
import time
from task_dialog import TaskNotesDialog

class TaskActions:
    def __init__(self, main_app):
        self.main_app = main_app
        self.autosave_enabled = False
        self.autosave_thread = None
        self.autosave_stop_event = threading.Event()
    
    def edit_task(self):
        """Handle editing a selected task"""
        selected = self.main_app.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return
        
        # Get the date from the selected item (it's the iid)
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
        """Show list of incomplete tasks scheduled today or in the past"""
        today = datetime.date.today()
        incomplete = []
        
        for day, info in self.main_app.sessions.items():
            # Parse the date string to compare with today
            try:
                task_date = datetime.datetime.strptime(day, "%Y-%m-%d").date()
                if task_date <= today and not info['completed']:
                    incomplete.append(day)
            except ValueError:
                # Skip invalid date formats
                continue
        
        if not incomplete:
            messagebox.showinfo("Complete", "All past and current sessions completed! 🎉")
        else:
            incomplete_text = "\n".join([f"{day}: {self.main_app.sessions[day]['topic']}" for day in incomplete])
            messagebox.showinfo("Incomplete Sessions", f"Remaining tasks (today and past):\n\n{incomplete_text}")
    
    def save_progress(self):
        """Save progress to the current CSV file"""
        if not self.main_app.current_file:
            messagebox.showerror("Error", "No file loaded to save to.")
            return
            
        try:
            # Create backup of original file
            backup_file = self.main_app.current_file + ".backup"
            with open(self.main_app.current_file, 'r', encoding='utf-8') as original:
                with open(backup_file, 'w', encoding='utf-8') as backup:
                    backup.write(original.read())
            
            # Save updated data
            with open(self.main_app.current_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Focus Topic', 'Suggested Tasks', 'Status', 'Notes'])
                
                # Sort sessions by date for consistent output
                sorted_sessions = sorted(self.main_app.sessions.items(), key=lambda x: x[0])
                
                for date, info in sorted_sessions:
                    status = "Complete" if info['completed'] else "Pending"
                    writer.writerow([
                        date, 
                        info['topic'], 
                        info.get('suggested_tasks', ''),
                        status,
                        info.get('notes', '')
                    ])
            
            messagebox.showinfo("Success", f"Progress saved to {self.main_app.current_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def toggle_autosave(self):
        """Toggle autosave functionality"""
        if self.autosave_enabled:
            self.stop_autosave()
        else:
            self.start_autosave()
    
    def start_autosave(self):
        """Start autosave thread"""
        if not self.main_app.current_file:
            messagebox.showerror("Error", "No file loaded for autosave.")
            return
            
        self.autosave_enabled = True
        self.autosave_stop_event.clear()
        self.autosave_thread = threading.Thread(target=self._autosave_worker, daemon=True)
        self.autosave_thread.start()
        self.main_app.main_interface.update_autosave_button(True)
        messagebox.showinfo("Autosave", "Autosave enabled - saving every 30 seconds")
    
    def stop_autosave(self):
        """Stop autosave thread"""
        self.autosave_enabled = False
        self.autosave_stop_event.set()
        if self.autosave_thread:
            self.autosave_thread.join(timeout=1)
        self.main_app.main_interface.update_autosave_button(False)
        messagebox.showinfo("Autosave", "Autosave disabled")
    
    def _autosave_worker(self):
        """Background thread for autosave functionality"""
        while not self.autosave_stop_event.is_set():
            time.sleep(30)  # Wait 30 seconds
            if not self.autosave_stop_event.is_set():
                try:
                    # Save without showing message to avoid interrupting user
                    with open(self.main_app.current_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Date', 'Focus Topic', 'Suggested Tasks', 'Status', 'Notes'])
                        
                        # Sort sessions by date for consistent output
                        sorted_sessions = sorted(self.main_app.sessions.items(), key=lambda x: x[0])
                        
                        for date, info in sorted_sessions:
                            status = "Complete" if info['completed'] else "Pending"
                            writer.writerow([
                                date, 
                                info['topic'], 
                                info.get('suggested_tasks', ''),
                                status,
                                info.get('notes', '')
                            ])
                except Exception as e:
                    # Log error but don't show message to avoid interrupting user
                    print(f"Autosave error: {str(e)}") 