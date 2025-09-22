import tkinter as tk
from tkinter import messagebox, ttk

from src.models.draft_calculations import DraftCalculations
from src.utils.validators import DraftValidator
from .base_page import BasePage


class BallastPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.calculator = DraftCalculations()

        # Initialize entry variables
        self.ballast_entries = []
        self.total_ballast_var = tk.StringVar()  # noqa: F821
        self.ballast_table_frame = None

        self.create_frame_content()

    def create_frame_content(self):
        """Create the main content of the ballast page"""
        self.create_title("Ballast Operations")

        # Create main content frame
        content_frame = ttk.Frame(self)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create ballast table frame (for grid layout)
        self.ballast_table_frame = ttk.Frame(content_frame)
        self.ballast_table_frame.pack(fill='both', expand=True, pady=5)

        # Create ballast table headers
        self.create_ballast_table(self.ballast_table_frame)

        # Create total display
        total_frame = ttk.Frame(content_frame)
        total_frame.pack(fill='x', pady=10)

        ttk.Label(
            total_frame,
            text="Total Ballast:",
        ).pack(side='left', padx=5)

        ttk.Entry(
            total_frame,
            textvariable=self.total_ballast_var,
            state='readonly'
        ).pack(side='left', padx=5)

        # Create buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill='x', pady=5)

        ttk.Button(
            button_frame,
            text="Add Tank",
            command=self.add_ballast_row
        ).pack(side='left', padx=5)

        ttk.Button(
            button_frame,
            text="Calculate Total",
            command=self.calculate_total
        ).pack(side='left', padx=5)

    def create_ballast_table(self, parent):
        """Create the ballast table headers"""
        headers = ['Tank Name', 'Initial', 'Final', 'Difference']

        for col, header in enumerate(headers):
            ttk.Label(
                parent,
                text=header,
                font=('times new roman', 12, 'bold')
            ).grid(row=0, column=col, padx=5, pady=5)

    def add_ballast_row(self):
        """Add a new row of ballast entries"""
        row = len(self.ballast_entries) + 1
        entries = []

        vcmd = (self.register(DraftValidator.validate_entry_callback), '%P')

        # Tank name entry
        name_entry = ttk.Entry(self.ballast_table_frame)
        name_entry.grid(row=row, column=0, padx=5, pady=2)
        entries.append(name_entry)

        # Initial and Final value entries
        for col in [1, 2]:
            entry = ttk.Entry(
                self.ballast_table_frame,
                validate='key',
                validatecommand=vcmd
            )
            entry.grid(row=row, column=col, padx=5, pady=2)
            entries.append(entry)

        # Difference label
        diff_label = ttk.Label(self.ballast_table_frame, text="0")
        diff_label.grid(row=row, column=3, padx=5, pady=2)
        entries.append(diff_label)

        self.ballast_entries.append(entries)

    def calculate_total(self):
        """Calculate total ballast difference"""
        total = 0

        for entries in self.ballast_entries:
            try:
                initial = float(entries[1].get() or 0)
                final = float(entries[2].get() or 0)
                difference = final - initial
                entries[3].configure(text=f"{difference:.2f}")
                total += difference
            except ValueError:
                messagebox.showerror("Error", "Invalid numeric value")
                return

        self.total_ballast_var.set(f"{total:.2f}")
