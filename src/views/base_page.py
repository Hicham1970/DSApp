import tkinter as tk
from tkinter import ttk


class BasePage(ttk.Frame):
    """Base class for all pages in the Draft Survey application"""

    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        # Common attributes for all pages
        from src.utils.themes import dark_theme
        self.frame_content = None
        self.controller = controller
        self.title_label = None
        self.calculator = None
        self.current_theme = dark_theme  # To hold the current theme, default to dark
        self.labeled_entries = []

        # Initialize UI
        self.setup_ui()

    def setup_ui(self):
        """Template method for initial UI setup"""
        # Configure grid weights - title in row 0, content in row 1
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create main content frame
        self.frame_content = ttk.Frame(self)
        self.frame_content.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

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
        bg = self.current_theme.get("labeled_entry_label_bg", "gray15")
        fg = self.current_theme.get("labeled_entry_label_fg", "gold")
        label = tk.Label(
            parent,
            text=label_text,
            background=bg,
            foreground=fg,
            anchor='e'
        )
        label.grid(row=row, column=column, padx=5, pady=2, sticky='e')

        entry = ttk.Entry(parent, style="TEntry", **kwargs)
        entry.grid(row=row, column=column+1, padx=5, pady=2, sticky='w')
        self.labeled_entries.append(label)
        return label, entry

    def create_tooltip(self, widget, text):
        """Creates a tooltip for a given widget."""
        tooltip_window = None

        def show_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window or not text:
                return
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
            tooltip_window = tk.Toplevel(widget)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.wm_geometry(f"+{x}+{y}")
            bg = self.current_theme.get("tooltip_bg", "#FFFFE0")
            fg = self.current_theme.get("tooltip_fg", "black")
            label = tk.Label(tooltip_window, text=text, background=bg, foreground=fg, relief="solid", borderwidth=1,
                             font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)

        def hide_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def update_style(self, theme: dict):
        """Template method to update styles for non-ttk widgets."""
        self.current_theme = theme

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
