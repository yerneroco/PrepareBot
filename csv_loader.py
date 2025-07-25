import csv
import datetime
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
                    # Handle both original format (with day) and saved format (without day)
                    date_str = row['Date'].split(' ')[0]  # Extract just the date part
                    
                    # Check if this is a saved file with Status column
                    if 'Status' in row:
                        # Load saved format with completion status and notes
                        sessions[date_str] = {
                            'topic': row['Focus Topic'],
                            'suggested_tasks': row.get('Suggested Tasks', ''),
                            'completed': row['Status'] == 'Complete',
                            'notes': row.get('Notes', '')
                        }
                    else:
                        # Load original format
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
    
    @staticmethod
    def categorize_dates(sessions):
        """Categorize dates into Overdue, Today, Tomorrow, This Week, More than a week"""
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        week_end = today + datetime.timedelta(days=7)
        
        categories = {
            'Overdue': [],
            'Today': [],
            'Tomorrow': [],
            'This Week': [],
            'More than a week': []
        }
        
        for date_str, info in sessions.items():
            try:
                task_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                
                if task_date < today:
                    categories['Overdue'].append((date_str, info))
                elif task_date == today:
                    categories['Today'].append((date_str, info))
                elif task_date == tomorrow:
                    categories['Tomorrow'].append((date_str, info))
                elif task_date <= week_end:
                    categories['This Week'].append((date_str, info))
                else:
                    categories['More than a week'].append((date_str, info))
                    
            except ValueError:
                # Skip invalid dates
                continue
        
        return categories 