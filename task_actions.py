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
        self.selected_tasks = set()  # Track selected tasks
    
    def edit_task(self):
        """Handle editing a selected task"""
        selected = self.main_app.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return
        
        # Get the date from the selected item (it's the iid)
        date = selected[0]
        
        # Check if this is a header row (should not be editable)
        if date.startswith("header_"):
            messagebox.showwarning("Warning", "Cannot edit category headers.")
            return
        
        # Check if the date exists in sessions
        if date not in self.main_app.sessions:
            messagebox.showwarning("Warning", "Selected item is not a valid task.")
            return
        
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
            incomplete_text = "\n".join([f"{day}: {self.main_app.sessions[day]['topic']} - {self.main_app.sessions[day].get('suggested_tasks', '')[:50]}..." for day in incomplete])
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
    
    def generate_export_content(self, task_dates, title="Jacob's Selected Pre-Class Study Tasks"):
        """Generate export content for given task dates"""
        export_content = f"### {title}\n\n"
        
        # Sort tasks by date
        task_dates.sort()
        
        for date in task_dates:
            if date in self.main_app.sessions:
                info = self.main_app.sessions[date]
                export_content += f"[{date}] - {info['topic']}\n"
                export_content += f"• Task: {info.get('suggested_tasks', '')}\n"
                
                if info.get('notes'):
                    export_content += f"• Notes: {info['notes']}\n"
                else:
                    export_content += "• Notes: \n"
                
                export_content += "\n"
        
        return export_content
    
    def export_selected_to_clipboard(self):
        """Export selected tasks to clipboard (default)"""
        selected = self.main_app.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select tasks to export.")
            return
        
        # Filter out header rows and get only valid task dates
        task_dates = []
        for item in selected:
            if not item.startswith("header_"):
                task_dates.append(item)
        
        if not task_dates:
            messagebox.showwarning("Warning", "Please select valid tasks to export (not category headers).")
            return
        
        try:
            export_content = self.generate_export_content(task_dates)
            
            # Copy to clipboard
            import pyperclip
            pyperclip.copy(export_content)
            messagebox.showinfo("Success", f"Selected tasks copied to clipboard!\n\nExported {len(task_dates)} tasks.")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_selected_to_file(self):
        """Export selected tasks to file"""
        selected = self.main_app.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select tasks to export.")
            return
        
        # Filter out header rows and get only valid task dates
        task_dates = []
        for item in selected:
            if not item.startswith("header_"):
                task_dates.append(item)
        
        if not task_dates:
            messagebox.showwarning("Warning", "Please select valid tasks to export (not category headers).")
            return
        
        try:
            export_content = self.generate_export_content(task_dates)
            
            # Ask user where to save
            export_file = filedialog.asksaveasfilename(
                title="Export Selected Tasks",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if export_file:
                with open(export_file, 'w', encoding='utf-8') as f:
                    f.write(export_content)
                
                messagebox.showinfo("Success", f"Selected tasks exported to {export_file}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_all_to_clipboard(self):
        """Export all tasks to clipboard"""
        try:
            task_dates = list(self.main_app.sessions.keys())
            export_content = self.generate_export_content(task_dates, "Jacob's Complete Pre-Class Study Tasks")
            
            # Copy to clipboard
            import pyperclip
            pyperclip.copy(export_content)
            messagebox.showinfo("Success", f"All tasks copied to clipboard!\n\nExported {len(task_dates)} tasks.")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_all_to_file(self):
        """Export all tasks to file"""
        try:
            task_dates = list(self.main_app.sessions.keys())
            export_content = self.generate_export_content(task_dates, "Jacob's Complete Pre-Class Study Tasks")
            
            # Ask user where to save
            export_file = filedialog.asksaveasfilename(
                title="Export All Tasks",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if export_file:
                with open(export_file, 'w', encoding='utf-8') as f:
                    f.write(export_content)
                
                messagebox.showinfo("Success", f"All tasks exported to {export_file}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def toggle_selection(self):
        """Toggle selection of the currently selected task"""
        selected = self.main_app.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to toggle selection.")
            return
        
        # Get the first selected item (for simplicity, handle one at a time)
        item = selected[0]
        
        # Check if this is a header row
        if item.startswith("header_"):
            messagebox.showwarning("Warning", "Cannot select category headers.")
            return
        
        # Check if the date exists in sessions
        if item not in self.main_app.sessions:
            messagebox.showwarning("Warning", "Selected item is not a valid task.")
            return
        
        # Toggle selection
        if item in self.selected_tasks:
            self.selected_tasks.remove(item)
            # Update tree to show as unselected
            self.main_app.tree.item(item, tags=())
        else:
            self.selected_tasks.add(item)
            # Update tree to show as selected
            self.main_app.tree.item(item, tags=("selected",))
        
        # Update the tree to reflect selection
        self.main_app.main_interface.populate_tree()
        
        # Show selection status
        if item in self.selected_tasks:
            messagebox.showinfo("Selection", f"Task for {item} marked for export")
        else:
            messagebox.showinfo("Selection", f"Task for {item} removed from export") 