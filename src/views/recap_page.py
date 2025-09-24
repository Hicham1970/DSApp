import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk, filedialog

from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.controllers.survey_controller import SurveyController
from .base_page import BasePage


class RecapPage(BasePage):
    """Recap page for displaying survey summary and generating reports"""

    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller if controller else SurveyController()
        self.value_labels = {}

        # Load icons
        self._load_icons()

        # Create the interface
        self.create_frame_content()

    def update_data(self, survey_data=None):
        """Update page with new survey data"""
        if survey_data:
            self.controller.survey_data = survey_data
        self.update_display()

    def update_display(self):
        """Update all display labels with current data"""
        try:
            # Get summary data from controller
            summary = self.controller.get_survey_summary()

            # Update initial survey data
            initial_data = summary.get('initial_survey', {})
            if initial_data:
                self.value_labels['initial_mean'].configure(
                    text=f"{initial_data.get('mean_draft', 0):.3f}")
                self.value_labels['initial_displacement'].configure(
                    text=f"{initial_data.get('displacement', 0):.3f}")
                self.value_labels['initial_deductibles'].configure(
                    text=f"{initial_data.get('deductibles', 0):.3f}")

            # Update final survey data
            final_data = summary.get('final_survey', {})
            if final_data:
                self.value_labels['final_mean'].configure(
                    text=f"{final_data.get('mean_draft', 0):.3f}")
                self.value_labels['final_displacement'].configure(
                    text=f"{final_data.get('displacement', 0):.3f}")
                self.value_labels['final_deductibles'].configure(
                    text=f"{final_data.get('deductibles', 0):.3f}")

            # Update ballast and cargo data
            ballast_data = summary.get('ballast_data', {})
            if ballast_data:
                self.value_labels['ballast_change'].configure(
                    text=f"{ballast_data.get('total_change', 0):.3f}")

            # Update cargo quantity
            cargo_data = summary.get('cargo_data', {})
            if cargo_data:
                self.value_labels['cargo_quantity'].configure(
                    text=f"{cargo_data.get('quantity', 0):.3f}")

        except Exception as e:
            messagebox.showerror(
                "Display Error", f"Error updating display: {str(e)}")

    def _load_icons(self):
        """Loads all icons used on this page."""
        icon_size = (24, 24)  # Define a standard icon size

        try:
            self.refresh_icon_photo = ImageTk.PhotoImage(
                Image.open("images/refresh.png").resize(icon_size, Image.LANCZOS))
            self.report_icon_photo = ImageTk.PhotoImage(
                Image.open("images/report.png").resize(icon_size, Image.LANCZOS))
            self.export_pdf_icon_photo = ImageTk.PhotoImage(
                Image.open("images/export_pdf.png").resize(icon_size, Image.LANCZOS))
            self.save_summary_icon_photo = ImageTk.PhotoImage(
                Image.open("images/save_data.png").resize(icon_size, Image.LANCZOS))
        except FileNotFoundError as e:
            print(
                f"Icon Error: Could not load icon: {e}. Please ensure images are in the 'images' folder.")
            self.refresh_icon_photo = self.report_icon_photo = self.export_pdf_icon_photo = self.save_summary_icon_photo = None
        except Exception as e:
            print(f"Icon Error: An error occurred loading icons: {e}")
            self.refresh_icon_photo = self.report_icon_photo = self.export_pdf_icon_photo = self.save_summary_icon_photo = None

    def create_frame_content(self):
        """Create the main content of the recap page"""
        self.create_title("Draft Survey Summary")

        # Create main content frame
        content_frame = ttk.Frame(self.frame_content)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create sections
        self.create_initial_section(content_frame)
        self.create_final_section(content_frame)
        self.create_ballast_section(content_frame)
        self.create_result_section(content_frame)

        # Create action buttons
        self.create_action_buttons(content_frame)

    def create_initial_section(self, parent):
        """Create initial draft survey summary section"""
        frame = ttk.LabelFrame(parent, text="Initial Survey")
        frame.pack(fill='x', padx=5, pady=5)

        labels = ["Mean Draft (m):", "Displacement (MT):", "Deductibles (MT):"]
        keys = ['initial_mean', 'initial_displacement', 'initial_deductibles']

        for i, (text, key) in enumerate(zip(labels, keys)):
            ttk.Label(frame, text=text).grid(
                row=i, column=0, padx=5, pady=2, sticky='w')
            label = ttk.Label(frame, text="0.000")
            label.grid(row=i, column=1, padx=5, pady=2, sticky='e')
            self.value_labels[key] = label

    def create_final_section(self, parent):
        """Create final draft survey summary section"""
        frame = ttk.LabelFrame(parent, text="Final Survey")
        frame.pack(fill='x', padx=5, pady=5)

        labels = ["Mean Draft (m):", "Displacement (MT):", "Deductibles (MT):"]
        keys = ['final_mean', 'final_displacement', 'final_deductibles']

        for i, (text, key) in enumerate(zip(labels, keys)):
            ttk.Label(frame, text=text).grid(
                row=i, column=0, padx=5, pady=2, sticky='w')
            label = ttk.Label(frame, text="0.000")
            label.grid(row=i, column=1, padx=5, pady=2, sticky='e')
            self.value_labels[key] = label

    def create_ballast_section(self, parent):
        """Create ballast operations summary section"""
        frame = ttk.LabelFrame(parent, text="Ballast Operations")
        frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(frame, text="Total Ballast Change (MT):").grid(
            row=0, column=0, padx=5, pady=2, sticky='w')
        label = ttk.Label(frame, text="0.000")
        label.grid(row=0, column=1, padx=5, pady=2, sticky='e')
        self.value_labels['ballast_change'] = label

    def create_result_section(self, parent):
        """Create final results section"""
        frame = ttk.LabelFrame(parent, text="Results")
        frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(
            frame,
            text="Cargo Quantity (MT):",
            font=('Arial', 12, 'bold')
        ).grid(row=0, column=0, padx=5, pady=5, sticky='w')

        label = ttk.Label(
            frame,
            text="0.000",
            font=('Arial', 14, 'bold')
        )
        label.grid(row=0, column=1, padx=5, pady=5, sticky='e')
        self.value_labels['cargo_quantity'] = label

    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=10)

        # Left side buttons
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side='left')

        # Refresh Data Button
        refresh_btn = ttk.Button(
            left_buttons,
            image=self.refresh_icon_photo,
            command=self.refresh_data
        )
        refresh_btn.pack(side='left', padx=5)
        self.create_tooltip(
            refresh_btn, "Refresh displayed data from controller")

        # Generate Report Button
        generate_report_btn = ttk.Button(
            left_buttons,
            image=self.report_icon_photo,
            command=self.generate_report
        )
        generate_report_btn.pack(side='left', padx=5)
        self.create_tooltip(generate_report_btn,
                            "Generate comprehensive survey report in a dialog")

        # Right side buttons
        right_buttons = ttk.Frame(button_frame)
        right_buttons.pack(side='right')

        # Export PDF Button
        export_pdf_btn = ttk.Button(
            right_buttons,
            image=self.export_pdf_icon_photo,
            command=self.export_pdf
        )
        export_pdf_btn.pack(side='right', padx=5)
        self.create_tooltip(
            export_pdf_btn, "Export survey report to a PDF file")

        # Save Summary Button
        save_summary_btn = ttk.Button(
            right_buttons,
            image=self.save_summary_icon_photo,
            command=self.save_summary
        )
        save_summary_btn.pack(side='right', padx=5)
        self.create_tooltip(
            save_summary_btn, "Save survey summary to a text file")

    def refresh_data(self):
        """Refresh data from controller"""
        self.update_display()

    def generate_report(self):
        """Generate comprehensive survey report"""
        try:
            report = self.controller.generate_survey_report()
            # Display report in a new window or dialog
            self.show_report_dialog(report)
        except Exception as e:
            messagebox.showerror(
                "Report Error", f"Error generating report: {str(e)}")

    def show_report_dialog(self, report_text):
        """Show report in a dialog window"""
        dialog = tk.Toplevel(self)
        dialog.title("Survey Report")
        dialog.geometry("800x600")

        # Create text widget for report
        text_widget = tk.Text(dialog, wrap='word', padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(text_widget, command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.config(yscrollcommand=scrollbar.set)

        # Insert report text
        text_widget.insert('1.0', report_text)
        text_widget.config(state='disabled')

        # Add close button
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=5)

    def export_pdf(self):
        """Export survey report to PDF"""
        try:
            filename = f"draft_survey_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join('Output', filename)

            # Create PDF
            c = canvas.Canvas(filepath, pagesize=A4)
            width, height = A4

            # Add title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Draft Survey Report")

            # Add date
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 70,
                         f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

            # Get report data
            summary = self.controller.get_survey_summary()

            # Add sections
            y = height - 100
            sections = [
                ("Initial Survey", summary.get('initial_survey', {})),
                ("Final Survey", summary.get('final_survey', {})),
                ("Ballast Operations", summary.get('ballast_data', {})),
                ("Cargo Results", summary.get('cargo_data', {}))
            ]

            c.setFont("Helvetica-Bold", 14)
            for section_title, data in sections:
                if data:  # Only add sections with data
                    y -= 30
                    c.drawString(50, y, section_title)
                    c.setFont("Helvetica", 11)
                    for key, value in data.items():
                        if value is not None and value != 0:
                            y -= 20
                            c.drawString(70, y, f"{key}: {value:.3f}")
                    y -= 10  # Extra space between sections

            c.save()
            messagebox.showinfo("Success", f"PDF report saved as {filename}")

        except Exception as e:
            messagebox.showerror(
                "PDF Error", f"Failed to generate PDF: {str(e)}")

    def save_summary(self):
        """Save summary data to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                summary = self.controller.get_survey_summary()
                with open(filename, 'w') as f:
                    f.write("DRAFT SURVEY SUMMARY\n")
                    f.write("=" * 50 + "\n\n")

                    for section_name, data in summary.items():
                        if data:
                            f.write(f"{section_name.upper()}:\n")
                            f.write("-" * 30 + "\n")
                            for key, value in data.items():
                                f.write(f"{key}: {value:.3f}\n")
                            f.write("\n")

                messagebox.showinfo("Success", "Summary saved successfully!")
        except Exception as e:
            messagebox.showerror(
                "Save Error", f"Error saving summary: {str(e)}")

    def clear_all(self):
        """Clear all data and reset display"""
        try:
            self.controller.clear_all_data()
            for label in self.value_labels.values():
                label.configure(text="0.000")
        except Exception as e:
            messagebox.showerror("Error", f"Error clearing data: {str(e)}")

    # Template method implementations
    def clear_fields(self):
        """Clear all display fields"""
        self.clear_all()

    def validate_inputs(self):
        """Validate displayed data"""
        return True

    def calculate_values(self):
        """Recalculate and update display"""
        self.update_display()

    def save_data(self):
        """Save summary data"""
        self.save_summary()

    def load_data(self):
        """Load data from controller"""
        self.update_display()

    def print_data(self):
        """Print/export report"""
        self.export_pdf()
