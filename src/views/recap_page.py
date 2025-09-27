import tkinter as tk
from datetime import datetime
import os
from tkinter import messagebox, ttk, filedialog

from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

from src.controllers.survey_controller import SurveyController
from .base_page import BasePage
from src.utils.themes import dark_theme


class RecapPage(BasePage):
    """Recap page for displaying survey summary and generating reports"""

    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller if controller else SurveyController()
        self.current_theme = dark_theme  # Assume dark theme by default
        self.value_labels = {}

        # Load icons
        self._load_icons()

        # Create the interface
        self.create_frame_content()

    def update_style(self, theme: dict):
        """Update styles for non-ttk widgets on this page."""
        self.current_theme = theme
        self.title_label.config(
            background=theme["title_bg"], foreground=theme["title_fg"])

    def update_data(self, survey_data=None):
        """Update page with new survey data"""
        if survey_data:
            self.controller.survey_data = survey_data
        self.update_display()

    def update_display(self):
        """Update all display labels with current data"""
        try:
            summary = self.controller.get_survey_summary()
            vessel_data = summary.get('vessel_data', {})
            initial_survey = summary.get('initial', {})
            final_survey = summary.get('final', {})

            # --- Update Vessel Info ---
            self.update_section(self.vessel_info_labels, vessel_data)

            # --- Update Time Sheet ---
            self.update_section(
                self.timesheet_labels, vessel_data.get('time_sheet', {}))

            # --- Calculate and Update Cargo Summary ---
            # Initial Survey
            i_disp_corr_dens = initial_survey.get('calculation_data', {}).get(
                'density_corrections', {}).get('corrected_displacement_for_density', 0)
            i_deductibles = initial_survey.get('calculation_data', {}).get(
                'displacement_corrections', {}).get('total_deductibles', 0)
            i_net_disp = i_disp_corr_dens - i_deductibles

            # Final Survey
            f_disp_corr_dens = final_survey.get('calculation_data', {}).get(
                'density_corrections', {}).get('corrected_displacement_for_density', 0)
            f_deductibles = final_survey.get('calculation_data', {}).get(
                'displacement_corrections', {}).get('total_deductibles', 0)
            f_net_disp = f_disp_corr_dens - f_deductibles

            # Cargo Calculation
            op_type = vessel_data.get('operation_type', 'load')
            cargo_qty = abs(
                f_net_disp - i_net_disp) if op_type == 'load' else abs(i_net_disp - f_net_disp)

            # Update summary labels
            self.value_labels['initial_displacement'].config(
                text=f"{i_disp_corr_dens:.3f}")
            self.value_labels['initial_deductibles'].config(
                text=f"{i_deductibles:.3f}")
            self.value_labels['initial_net_displacement'].config(
                text=f"{i_net_disp:.3f}")

            self.value_labels['final_displacement'].config(
                text=f"{f_disp_corr_dens:.3f}")
            self.value_labels['final_deductibles'].config(
                text=f"{f_deductibles:.3f}")
            self.value_labels['final_net_displacement'].config(
                text=f"{f_net_disp:.3f}")

            self.value_labels['cargo_quantity'].config(
                text=f"{cargo_qty:.3f}")
            self.value_labels['quantity_bl'].config(
                text=f"{vessel_data.get('quantity_bl', 0):.3f}")
            diff = cargo_qty - vessel_data.get('quantity_bl', 0)
            self.value_labels['difference'].config(text=f"{diff:.3f}")

        except Exception as e:
            messagebox.showerror(
                "Display Error", f"Error updating display: {str(e)}")

    def update_section(self, section_labels, data_source):
        """Helper to update a section of labels from a data source."""
        for key, label_widget in section_labels.items():
            value = data_source.get(key, 'N/A')
            if isinstance(value, (int, float)):
                label_widget.config(text=f"{value:.3f}")
            else:
                label_widget.config(text=str(value))

    def _load_icons(self):
        """Loads all icons used on this page."""
        icon_size = (24, 24)  # Define a standard icon size

        icon_paths = {
            'refresh_icon_photo': "images/refresh.png",
            'report_icon_photo': "images/report.png",
            'export_pdf_icon_photo': "images/export_pdf.png",
            'save_summary_icon_photo': "images/save_data.png"
        }

        for attr_name, path in icon_paths.items():
            try:
                img = Image.open(path).resize(icon_size, Image.LANCZOS)
                setattr(self, attr_name, ImageTk.PhotoImage(img))
            except FileNotFoundError:
                print(
                    f"Icon Error: Could not find icon file: {path}. Please ensure images are in the 'images' folder.")
                setattr(self, attr_name, None)
            except tk.TclError as e:
                print(
                    f"Icon Error: TclError while loading {path}: {e}. This might indicate a corrupted image file or an issue with Pillow/Tkinter.")
                setattr(self, attr_name, None)
            except Exception as e:
                print(
                    f"Icon Error: An unexpected error occurred loading {path}: {e}")
                setattr(self, attr_name, None)

    def create_frame_content(self):
        """Create the main content of the recap page"""
        self.create_title("Draft Survey Summary")

        # Create main content frame
        main_frame = ttk.Frame(self.frame_content)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)

        # Create sections
        self.vessel_info_labels = self.create_section(
            main_frame, "Vessel Information",
            [
                ('vessel_name', "Vessel Name:"), ('draft_number',
                                                  "Draft Number:"), ('imo', "IMO:"),
                ('port_of_registry', "Port of Registry:"), ('client', "Client:"),
                ('lbp', "LBP (m):"), ('light_ship', "Light Ship (mt):"),
                ('declared_constant', "Declared Constant (mt):"),
                ('product', "Product:"),
                ('loading_port', "Loading Port:"),
                ('discharging_port', "Discharging Port:"),
                ('table_density', "Table Density:"), ('dock_density', "Dock Density:")
            ],
            row=0, column=0, sticky='new'
        )

        self.timesheet_labels = self.create_section(
            main_frame, "Time Sheet",
            [
                ('end_of_sea_passage', "End of Sea Passage:"),
                ('notice_tendered', "Notice Tendered:"),
                ('pilot_on_board', "Pilot On Board:"),
                ('first_line', "First Line:"),
                ('all_fast', "All Fast:"),
                ('surveyor_on_board', "Surveyor On Board:"),
                ('initial_draft_started', "Initial Draft Started:"),
                ('initial_draft_completed', "Initial Draft Completed:"),
                ('operation_started', "Operation Started:"),
                ('operation_completed', "Operation Completed:"),
                ('final_draft_started', "Final Draft Started:"),
                ('final_draft_completed', "Final Draft Completed:"),
                ('vessel_sailed', "Vessel Sailed:")
            ],
            row=0, column=1, rowspan=2, sticky='nsew'
        )

        self.cargo_summary_labels = self.create_cargo_summary_section(
            main_frame, row=1, column=0, sticky='sew')

        # Create action buttons
        self.create_action_buttons(main_frame)

    def create_section(self, parent, title, labels_keys, **grid_options):
        """Generic method to create a section with labels."""
        frame = ttk.LabelFrame(parent, text=title)
        frame.grid(**grid_options, padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        created_labels = {}
        for i, (key, text) in enumerate(labels_keys):
            ttk.Label(frame, text=text, style="Recap.TLabel").grid(
                row=i, column=0, padx=5, pady=2, sticky='w')
            value_label = ttk.Label(
                frame, text="N/A", anchor='e', style="Recap.TLabel")
            value_label.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
            created_labels[key] = value_label
        return created_labels

    def create_cargo_summary_section(self, parent, **grid_options):
        """Create the cargo summary section with specific layout."""
        frame = ttk.LabelFrame(parent, text="Cargo Summary")
        frame.grid(**grid_options, padx=5, pady=5)
        for i in range(3):
            frame.grid_columnconfigure(i, weight=1)

        # Headers
        ttk.Label(frame, text="", style="Recap.TLabel").grid(row=0, column=0)
        ttk.Label(frame, text="Initial", font=('Arial', 10, 'bold'), style="Recap.TLabel", anchor='center').grid(
            row=0, column=1, sticky='ew')
        ttk.Label(frame, text="Final", font=('Arial', 10, 'bold'), style="Recap.TLabel", anchor='center').grid(
            row=0, column=2, sticky='ew')

        # Rows
        self.value_labels['initial_displacement'] = self.add_summary_row(
            frame, "Displacement:", 1, colspan=1, style="Recap.TLabel")
        self.value_labels['final_displacement'] = ttk.Label(
            frame, text="0.000", style="Recap.TLabel", anchor='center')
        self.value_labels['final_displacement'].grid(
            row=1, column=2, sticky='ew', padx=5)
        self.value_labels['initial_deductibles'] = self.add_summary_row(
            frame, "Deductibles:", 2, colspan=1, style="Recap.TLabel")
        self.value_labels['final_deductibles'] = ttk.Label(
            frame, text="0.000", style="Recap.TLabel", anchor='center')
        self.value_labels['final_deductibles'].grid(
            row=2, column=2, sticky='ew', padx=5)
        self.value_labels['initial_net_displacement'] = self.add_summary_row(
            frame, "Net Displacement:", 3, colspan=1, style="Recap.TLabel")
        self.value_labels['final_net_displacement'] = ttk.Label(
            frame, text="0.000", style="Recap.TLabel", anchor='center')
        self.value_labels['final_net_displacement'].grid(
            row=3, column=2, sticky='ew', padx=5)

        # Final Cargo Result
        ttk.Separator(frame, orient='horizontal').grid(
            row=4, columnspan=3, sticky='ew', pady=5)
        self.value_labels['cargo_quantity'] = self.add_summary_row(
            frame, "Cargo Quantity (Survey):", 5, colspan=2, style="Cargo.TLabel")
        self.value_labels['quantity_bl'] = self.add_summary_row(
            frame, "Cargo Quantity (B/L):", 6, colspan=2, style="Recap.TLabel")
        self.value_labels['difference'] = self.add_summary_row(
            frame, "Difference:", 7, colspan=2, style="Difference.TLabel")

    def add_summary_row(self, parent, text, row, colspan=1, font=None, style=None):
        """Helper to add a row to the summary table."""
        ttk.Label(parent, text=text, font=font, style=style).grid(
            row=row, column=0, sticky='w', padx=5)
        value_label = ttk.Label(parent, text="0.000",
                                font=font, style=style, anchor='center')
        value_label.grid(row=row, column=colspan, sticky='ew', padx=5)
        return value_label

    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)

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
            # Ask where to save the PDF
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save PDF Report",
                initialfile=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            if not save_path:
                return  # User cancelled

            # --- Header function to draw logo on each page ---
            # Build an absolute path to the image to avoid issues with the current working directory
            project_root = os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))
            logo_path = os.path.join(project_root, "images", "Capt.png")
            try:
                logo = ImageReader(logo_path)
            except Exception:
                logo = None
                print(f"Warning: Could not load logo from {logo_path}")

            def header_and_footer(canvas, doc):
                # --- Header ---
                canvas.saveState()
                if logo:
                    # Draw logo on the top left.
                    # The coordinates (doc.leftMargin, doc.height + doc.topMargin - 30) place it near the top-left corner.
                    # A smaller number after topMargin moves it higher.
                    canvas.drawImage(logo, doc.leftMargin, doc.height + doc.topMargin - 30,
                                     width=100, height=50, preserveAspectRatio=True, mask='auto')
                canvas.restoreState()

                # --- Footer ---
                canvas.saveState()
                canvas.setFont('Helvetica', 8)

                # Contact Info
                contact_text = "GH Maritime Surveys | https://mysiteweb2frontend.onrender.com/.com | Tel: +212 123 456 789"
                canvas.drawCentredString(
                    doc.width/2 + doc.leftMargin, 50, contact_text)

                # Disclaimer
                disclaimer_line1 = "Disclaimer: The calculations herein are based on the vessel's documents and are believed to be accurate at the time of survey."
                disclaimer_line2 = "This report is issued without prejudice, and no liability is accepted for any errors or discrepancies."
                canvas.drawCentredString(
                    doc.width/2 + doc.leftMargin, 40, disclaimer_line1)
                canvas.drawCentredString(
                    doc.width/2 + doc.leftMargin, 30, disclaimer_line2)

                # Page Number
                # Reset font size for page number
                canvas.setFont('Helvetica', 9)
                page_num_text = f"Page {canvas.getPageNumber()}"
                canvas.drawCentredString(
                    doc.width/2 + doc.leftMargin, 15, page_num_text)
                canvas.restoreState()

            # Use colors from the current theme
            theme_colors = self.current_theme
            cargo_color = colors.black  # Force black color for cargo quantity
            diff_color = colors.HexColor(theme_colors["diff_label_fg"])

            from reportlab.lib.colors import navy, red

            # 1. Generate the PDF content
            # report_text = self.controller.generate_survey_report()

            doc = SimpleDocTemplate(save_path, pagesize=A4,
                                    rightMargin=72, leftMargin=72,
                                    topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            # Use a monospaced font for the report
            styles['Normal'].fontName = 'Courier'
            styles['Normal'].fontSize = 9

            # Modify existing styles instead of adding new ones with the same name
            styles['Title'].fontName = 'Helvetica-Bold'
            styles['Title'].fontSize = 16
            styles['Title'].alignment = TA_CENTER
            styles['Title'].spaceAfter = 20

            styles['h2'].fontName = 'Helvetica-Bold'

            styles.add(ParagraphStyle(name='CargoLabel', fontName='Helvetica-Bold',
                       fontSize=10, textColor=cargo_color, alignment=TA_CENTER))
            styles.add(ParagraphStyle(name='DiffLabel', fontName='Helvetica-Bold',
                       fontSize=10, textColor=diff_color, alignment=TA_CENTER))

            # --- Get Data ---
            summary = self.controller.get_survey_summary()
            vessel_data = summary.get('vessel_data', {})
            initial_data = summary.get('initial', {})
            final_data = summary.get('final', {})

            def get_val(data_dict, *keys, default='N/A', precision=3):
                temp_dict = data_dict
                for key in keys:
                    if isinstance(temp_dict, dict):
                        temp_dict = temp_dict.get(key)
                    else:
                        return default
                if temp_dict is None:
                    return default
                if isinstance(temp_dict, (int, float)):
                    return f"{temp_dict:.{precision}f}"
                return str(temp_dict)

            # --- Build Story ---
            story = []
            story.append(Paragraph("DRAFT SURVEY REPORT", styles['Title']))

            # --- Vessel Information (2 columns) ---
            story.append(Paragraph("VESSEL INFORMATION", styles['h2']))
            vessel_info_data = [
                [f"Vessel Name: {get_val(vessel_data, 'vessel_name')}",
                 f"Port of Registry: {get_val(vessel_data, 'port_of_registry')}"],
                [f"Draft Number: {get_val(vessel_data, 'draft_number')}",
                 f"IMO: {get_val(vessel_data, 'imo')}"],
                [f"Client: {get_val(vessel_data, 'client')}",
                 f"Product: {get_val(vessel_data, 'product')}"],
                [f"LBP (m): {get_val(vessel_data, 'lbp')}",
                 f"Loading Port: {get_val(vessel_data, 'loading_port')}"],
                [f"Light Ship (mt): {get_val(vessel_data, 'light_ship')}",
                 f"Discharging Port: {get_val(vessel_data, 'discharging_port')}"],
                [f"Declared Constant: {get_val(vessel_data, 'declared_constant')}",
                 f"Quantity B/L (mt): {get_val(vessel_data, 'quantity_bl')}"],
                [f"Table Density: {get_val(vessel_data, 'table_density')}",
                 f"Operation Type: {get_val(vessel_data, 'operation_type', default='').upper()}"],
            ]
            vessel_table = Table(vessel_info_data, colWidths=[250, 250])
            vessel_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONT', (0, 0), (-1, -1), 'Courier', 8),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            story.append(vessel_table)

            # --- Time Sheet (2 columns) ---
            story.append(Paragraph("TIME SHEET", styles['h2']))
            time_sheet = vessel_data.get('time_sheet', {})
            time_sheet_items = list(time_sheet.keys())
            time_sheet_data = []
            for i in range(0, len(time_sheet_items), 2):
                key1 = time_sheet_items[i]
                label1 = key1.replace('_', ' ').title()
                val1 = time_sheet.get(key1, 'N/A')
                col1 = f"{label1}: {val1}"

                col2 = ""
                if i + 1 < len(time_sheet_items):
                    key2 = time_sheet_items[i+1]
                    label2 = key2.replace('_', ' ').title()
                    val2 = time_sheet.get(key2, 'N/A')
                    col2 = f"{label2}: {val2}"
                time_sheet_data.append([col1, col2])

            time_sheet_table = Table(time_sheet_data, colWidths=[250, 250])
            time_sheet_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONT', (0, 0), (-1, -1), 'Courier', 8),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            story.append(time_sheet_table)

            # --- Observed Drafts and Distances ---
            # --- Observed Drafts and Distances ---
            story.append(
                Paragraph("OBSERVED DRAFTS & DISTANCES", styles['h2']))

            obs_drafts_data = [
                ['Description', 'Initial', 'Final'],
                ['Fwd Port', get_val(initial_data, 'draft_data', 'observed_drafts', 'draft_for_port'), get_val(
                    final_data, 'draft_data', 'observed_drafts', 'draft_for_port')],
                ['Fwd Starboard', get_val(initial_data, 'draft_data', 'observed_drafts', 'draft_for_star'), get_val(
                    final_data, 'draft_data', 'observed_drafts', 'draft_for_star')],
                ['Mid Port', get_val(initial_data, 'draft_data', 'observed_drafts', 'draft_mid_port'), get_val(
                    final_data, 'draft_data', 'observed_drafts', 'draft_mid_port')],
                ['Mid Starboard', get_val(initial_data, 'draft_data', 'observed_drafts', 'draft_mid_star'), get_val(
                    final_data, 'draft_data', 'observed_drafts', 'draft_mid_star')],
                ['Aft Port', get_val(initial_data, 'draft_data', 'observed_drafts', 'draft_aft_port'), get_val(
                    final_data, 'draft_data', 'observed_drafts', 'draft_aft_port')],
                ['Aft Starboard', get_val(initial_data, 'draft_data', 'observed_drafts', 'draft_aft_star'), get_val(
                    final_data, 'draft_data', 'observed_drafts', 'draft_aft_star')],
                [Spacer(0, 10), '', ''],
                ['Dock Density', get_val(initial_data, 'vessel_params', 'dock_density'), get_val(
                    final_data, 'vessel_params', 'dock_density')],
                ['Dist. Fwd PP (m)', get_val(initial_data, 'vessel_params', 'distance_from_for_pp'),
                 get_val(final_data, 'vessel_params', 'distance_from_for_pp')],
                ['Pos. Fwd PP', get_val(initial_data, 'vessel_params', 'position_from_for_pp'),
                 get_val(final_data, 'vessel_params', 'position_from_for_pp')],
                ['Dist. Mid PP (m)', get_val(initial_data, 'vessel_params', 'distance_from_mid_pp'),
                 get_val(final_data, 'vessel_params', 'distance_from_mid_pp')],
                ['Pos. Mid PP', get_val(initial_data, 'vessel_params', 'position_from_mid_pp'),
                 get_val(final_data, 'vessel_params', 'position_from_mid_pp')],
                ['Dist. Aft PP (m)', get_val(initial_data, 'vessel_params', 'distance_from_aft_pp'),
                 get_val(final_data, 'vessel_params', 'distance_from_aft_pp')],
                ['Pos. Aft PP', get_val(initial_data, 'vessel_params', 'position_from_aft_pp'),
                 get_val(final_data, 'vessel_params', 'position_from_aft_pp')],
            ]

            obs_drafts_table = Table(
                obs_drafts_data, colWidths=[150, 175, 175])
            obs_drafts_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(obs_drafts_table)

            # Force a page break before the next section
            story.append(PageBreak())

            # --- Survey Data Comparison (3 columns table) ---
            story.append(Paragraph("SURVEY DATA COMPARISON", styles['h2']))

            table_data = [['DESCRIPTION', 'INITIAL', 'FINAL']]
            report_items = [
                ("Fwd Draft Corrected", 'draft_data',
                 'corrected_drafts', 'draft_for_corrected'),
                ("Aft Draft Corrected", 'draft_data',
                 'corrected_drafts', 'draft_aft_corrected'),
                ("Mid Draft Corrected", 'draft_data',
                 'corrected_drafts', 'draft_mid_corrected'),
                ("Corrected Trim", 'draft_data',
                 'corrected_drafts', 'trim_corrected'),
                ("LBM", 'draft_data', 'corrected_drafts', 'lbm'),
                ("MFA", 'draft_data', 'mfa_mom_qm', 'mfa'),
                ("MOM", 'draft_data', 'mfa_mom_qm', 'mom'),
                ("QM", 'draft_data', 'mfa_mom_qm', 'qm'),
                ("Displacement", 'draft_data',
                 'interpolation_results', 'displacement'),
                ("TPC", 'draft_data', 'interpolation_results', 'tpc'),
                ("LCF", 'draft_data', 'interpolation_results', 'lcf'),
                ("1st Trim Correction", 'calculation_data',
                 'trim_corrections', 'first_trim_correction'),
                ("2nd Trim Correction", 'calculation_data',
                 'trim_corrections', 'second_trim_correction'),
                ("Disp Corrected (Trim)", 'calculation_data',
                 'trim_corrections', 'corrected_displacement_for_trim'),
                ("Disp Corrected (Density)", 'calculation_data',
                 'density_corrections', 'corrected_displacement_for_density'),
                ("Total Deductibles", 'calculation_data',
                 'displacement_corrections', 'total_deductibles'),
            ]
            for item in report_items:
                label, keys = item[0], item[1:]
                i_val = get_val(initial_data, *keys)
                f_val = get_val(final_data, *keys)
                table_data.append([label, i_val, f_val])

            survey_table = Table(table_data, colWidths=[150, 175, 175])
            survey_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                # Description column to the left
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                # Value columns to the right
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(survey_table)

            # --- Final Cargo Summary and Signatures (on the same page) ---
            # Use KeepTogether to try to keep the summary and signatures on the same page as the table if possible
            # or together on the next page if they don't fit.
            final_section = []
            final_section.append(Spacer(1, 12))  # Further reduced space
            final_section.append(
                Paragraph("FINAL CARGO SUMMARY", styles['h2']))

            i_disp = float(get_val(initial_data, 'calculation_data',
                                   'density_corrections', 'corrected_displacement_for_density', default=0.0))
            i_deduct = float(get_val(initial_data, 'calculation_data',
                                     'displacement_corrections', 'total_deductibles', default=0.0))
            i_net = i_disp - i_deduct

            f_disp = float(get_val(final_data, 'calculation_data', 'density_corrections',
                                   'corrected_displacement_for_density', default=0.0))
            f_deduct = float(get_val(final_data, 'calculation_data',
                                     'displacement_corrections', 'total_deductibles', default=0.0))
            f_net = f_disp - f_deduct

            cargo_qty = abs(f_net - i_net)
            qty_bl = float(vessel_data.get('quantity_bl', 0))
            diff = cargo_qty - qty_bl

            summary_data = [
                ['Initial Displacement:', f'{i_disp:.3f} mt'],
                ['Initial Deductibles:', f'{i_deduct:.3f} mt'],
                ['Initial Net Displacement:', f'{i_net:.3f} mt'],
                [Spacer(0, 10), Spacer(0, 10)],
                ['Final Displacement:', f'{f_disp:.3f} mt'],
                ['Final Deductibles:', f'{f_deduct:.3f} mt'],
                ['Final Net Displacement:', f'{f_net:.3f} mt'],
                [Spacer(0, 20), Spacer(0, 20)],
                [Paragraph('Cargo Quantity (Survey):', styles['CargoLabel']), Paragraph(
                    # type: ignore
                    f'{cargo_qty:.3f} mt', styles['CargoLabel'])]
            ]

            summary_table = Table(summary_data, colWidths=[250, 250])
            summary_table.setStyle(TableStyle([
                # Description column to the left
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                # Value column to the right
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONT', (0, 0), (-1, -1), 'Courier', 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            final_section.append(summary_table)

            # Add space before the signature block
            final_section.append(Spacer(1, 36))  # Further reduced space

            # 2. Create the signature block
            signature_data = [
                ['Le Chef Officier ou le Captain', "L'inspecteur"],
                ['(Signature)', "(Signature de l'inspecteur)"]
            ]
            signature_table = Table(signature_data, colWidths=[250, 250])
            signature_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black,
                 None, None, 2, 2),  # type: ignore
                ('TOPPADDING', (0, 0), (-1, 0), 20),  # Space for signature
            ]))
            final_section.append(signature_table)

            # Add the final section to the main story
            story.extend(final_section)

            # 3. Build the PDF
            doc.build(story, onFirstPage=header_and_footer,
                      onLaterPages=header_and_footer)

            messagebox.showinfo(
                "Success", f"Signed PDF report saved to:\n{save_path}")

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
                                if isinstance(value, (int, float)):
                                    f.write(f"{key}: {value:.3f}\n")
                                else:
                                    f.write(f"{key}: {value}\n")
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
