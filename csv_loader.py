import csv
from tkinter import messagebox

class CSVLoader:
    @staticmethod
    def load_schedule(file_path):
        """Load schedule from CSV file"""
        sessions = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    date_str = row['Date'].split(' ')[0]  # Extract just the date part
                    sessions[date_str] = {
                        'topic': row['Focus Topic'],
                        'suggested_tasks': row.get('Suggested Tasks', ''),
                        'completed': False,
                        'notes': ''
                    }
            
            return sessions
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")
            return None 