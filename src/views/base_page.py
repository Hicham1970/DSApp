import tkinter as tk
from tkinter import ttk


class BasePage(ttk.Frame):
    """Base class for all pages in the Draft Survey application"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        # Common attributes for all pages
        self.frame_content = None
        self.title_label = None
        self.calculator = None

        # Initialize UI
        self.setup_ui()

    def setup_ui(self):
        """Template method for initial UI setup"""
        # Configure grid weights - title in row 0, content in row 1
        self.grid_rowconfigure(0, weight=0)  # Title row - no expansion
        self.grid_rowconfigure(1, weight=1)  # Content row - expands
        self.grid_columnconfigure(0, weight=1)

        # Create main content frame
        self.frame_content = ttk.Frame(self)
        self.frame_content.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.frame_content.grid_rowconfigure(0, weight=1)
        self.frame_content.grid_columnconfigure(0, weight=1)

    def create_frame_content(self):
        """Template method to create page-specific content"""
        raise NotImplementedError(
            "Each page must implement create_frame_content()")

    def create_title(self, text):
        """Create common title label used across pages"""
        self.title_label = tk.Label(
            self,
            text=text,
            bd=6,
            font=('arial', 14, 'bold'),
            relief='groove',
            background='gray12',
            fg='gold'
        )
        self.title_label.grid(row=0, column=0, sticky='ew', pady=(5, 0))

    def create_labeled_entry(self, parent, label_text, row, column, **kwargs):
        """Helper method to create a label-entry pair"""
        label = tk.Label(
            parent,
            text=label_text,
            background='gray12',
            foreground='gold',
            anchor='e'
        )
        label.grid(row=row, column=column, padx=5, pady=2, sticky='e')

        entry = ttk.Entry(parent, **kwargs)
        entry.grid(row=row, column=column+1, padx=5, pady=2, sticky='w')
        return label, entry

    def clear_fields(self):
        """Template method to clear all input fields"""
        pass

    def validate_inputs(self):
        """Template method for input validation"""
        return True

    def calculate_values(self):
        """Template method for calculations"""
        pass

    def save_data(self):
        """Template method for saving data"""
        pass

    def load_data(self):
        """Template method for loading data"""
        pass

    def print_data(self):
        """Template method for printing data"""
        pass
