import tkinter as tk
from file_selection import FileSelectionFrame
from csv_loader import CSVLoader
from main_interface import MainInterface
from task_actions import TaskActions

class LearningTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learning Schedule Tracker")
        self.geometry("800x600")
        
        self.current_file = None
        self.sessions = {}
        
        # Initialize components
        self.csv_loader = CSVLoader()
        self.main_interface = MainInterface(self)
        self.task_actions = TaskActions(self)
        
        # Start with file selection
        self.show_file_selection()
    
    def show_file_selection(self):
        """Show the file selection interface"""
        # Clear current widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Show file selection frame
        self.file_frame = FileSelectionFrame(self, self.load_schedule)
        self.file_frame.pack(expand=True, fill="both")
    
    def load_schedule(self, file_path):
        """Load schedule from selected file"""
        self.current_file = file_path
        self.sessions = self.csv_loader.load_schedule(file_path)
        
        if self.sessions is not None:
            self.show_main_interface()
    
    def show_main_interface(self):
        """Show the main interface"""
        # Clear current widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Setup main interface
        self.main_interface.setup_main_interface()
    
    def populate_tree(self):
        """Delegate to main interface"""
        self.main_interface.populate_tree()

if __name__ == "__main__":
    app = LearningTracker()
    app.mainloop()
