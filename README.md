# Learning Schedule Tracker

A modular Python application for tracking learning schedules from CSV files.

## Project Structure

The application has been split into logical modules for better organization and maintainability:

### Core Modules

- **`app.py`** - Main application entry point and controller
- **`file_selection.py`** - File selection interface and caching functionality
- **`csv_loader.py`** - CSV file loading and parsing
- **`main_interface.py`** - Main UI setup and treeview management
- **`task_actions.py`** - Task editing, completion tracking, and export functionality
- **`task_dialog.py`** - Task notes dialog for editing individual tasks

### Module Responsibilities

#### `app.py` (Main Controller)
- Application initialization
- Navigation between interfaces
- Component coordination

#### `file_selection.py` (File Selection Module)
- **`FileSelectionFrame`** class
- File browsing functionality
- Last file caching (`last_file.json`)
- File validation

#### `csv_loader.py` (Data Loading Module)
- **`CSVLoader`** class with static methods
- CSV parsing and data structure creation
- Error handling for file loading

#### `main_interface.py` (UI Management Module)
- **`MainInterface`** class
- Treeview setup and configuration
- Button layout and event binding
- Tree population and updates

#### `task_actions.py` (Task Operations Module)
- **`TaskActions`** class
- `edit_task()` - Handle task editing
- `show_incomplete()` - Display incomplete tasks
- `export_progress()` - Export progress to CSV

#### `task_dialog.py` (Task Dialog Module)
- **`TaskNotesDialog`** class
- Notes input interface
- Completion status management
- Dialog result handling

## Features

- **File Selection**: Browse and select CSV files with caching
- **Task Management**: Edit tasks with detailed notes
- **Progress Tracking**: Mark tasks complete/incomplete
- **Export Functionality**: Export progress to CSV
- **Visual Indicators**: Status icons and progress previews

## Usage

1. Run `python app.py`
2. Select a CSV file (or use the last used file)
3. View and edit tasks by double-clicking or using the "Edit Task" button
4. Add notes and mark completion status
5. Export progress as needed

## CSV Format

Expected CSV columns:
- `Date` - Date in format "YYYY-MM-DD (Day)"
- `Focus Topic` - Topic name
- `Suggested Tasks` - Optional suggested activities

## Dependencies

- `tkinter` - GUI framework (included with Python)
- `csv` - CSV file handling (included with Python)
- `json` - Configuration caching (included with Python)
- `os` - File system operations (included with Python) 