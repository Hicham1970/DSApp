import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.controllers.survey_controller import SurveyController
from src.utils.validators import DraftValidator

from PIL import Image, ImageTk

try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None

from .base_page import BasePage


class InitialPage(BasePage):
    """Initial Draft Survey Page with comprehensive functionality"""

    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        # Initialize all entry variables
        self.entries = {}
        self.controller = controller if controller else SurveyController()
        self.validator = DraftValidator()

        # Load icons
        self._load_icons()
        self.controller.set_survey_type('initial')

        # Vessel information entries
        self.vessel_name_entry = None
        self.draft_number_entry = None
        self.lbp_entry = None
        self.light_ship_entry = None
        self.declared_constant_entry = None
        self.port_of_registry_entry = None
        self.product_entry = None
        self.imo_entry = None
        self.client_entry = None
        self.loading_port_entry = None
        self.discharging_port_entry = None
        self.quantity_bl_entry = None

        # Time sheet entries
        self.time_sheet_entries = {}
        self.time_sheet_tk_labels = []

        # Draft entries
        self.draft_for_port_entry = None
        self.draft_for_star_entry = None
        self.draft_mid_port_entry = None
        self.draft_mid_star_entry = None
        self.draft_aft_port_entry = None
        self.draft_aft_star_entry = None

        # Position and distance entries
        self.distance_from_for_pp_entry = None
        self.distance_from_aft_pp_entry = None
        self.distance_from_mid_pp_entry = None
        self.position_from_for_pp_entry = None
        self.position_from_aft_pp_entry = None
        self.position_from_mid_pp_entry = None

        # Trim and density entries
        self.trim_observed_entry = None
        self.dock_density_entry = None
        self.table_density_entry = None

        # Bunker data entries
        self.ballast_entry = None
        self.fuel_entry = None
        self.gas_oil_entry = None
        self.lub_oil_entry = None
        self.slops_entry = None
        self.others_entry = None
        self.fresh_water_entry = None

        # Operation type
        self.operation_type = tk.StringVar(value='load')

        # Results display
        self.results_text = None

        # Create the complete interface
        self.create_frame_content()

    def create_frame_content(self):
        """Create the comprehensive initial draft survey interface"""
        self.create_title("Initial Draft Survey")

        # Create notebook for organized tabs
        self.notebook = ttk.Notebook(self.frame_content)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Create tabs
        self.time_sheet_tab = ttk.Frame(
            self.notebook)  # New tab for time sheet
        self.vessel_tab = ttk.Frame(self.notebook)
        self.draft_tab = ttk.Frame(self.notebook)
        self.bunker_tab = ttk.Frame(self.notebook)
        self.calculation_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)

        self.notebook.add(
            self.vessel_tab, image=self.ship_icon, compound=tk.LEFT)
        self.notebook.add(self.time_sheet_tab,
                          image=self.time_icon, compound=tk.LEFT)
        self.notebook.add(
            self.draft_tab, image=self.draft_readings_icon, compound=tk.LEFT)
        self.notebook.add(
            self.bunker_tab, image=self.deductibles_icon, compound=tk.LEFT)
        self.notebook.add(self.calculation_tab,
                          image=self.calculations_icon, compound=tk.LEFT)
        self.notebook.add(self.results_tab,
                          image=self.results_icon, compound=tk.LEFT)

        self._create_vessel_tab()
        self._create_time_sheet_tab()  # Create content for new tab
        self._create_draft_tab()
        self._create_deductibles_tab()
        self._create_calculation_tab()
        self._create_results_tab()

        self._create_action_buttons()

        # Add tooltips to tabs
        self._create_notebook_tooltips()

    def _load_icons(self):
        """Loads all icons used on this page."""
        icon_size = (24, 24)  # Define a standard icon size

        icon_paths = {
            'clear_icon_photo': "images/clear-erase.png",
            'save_icon_photo': "images/save_data.png",
            'load_icon_photo': "images/upload.png",
            'report_icon_photo': "images/report.png",
            'draft_readings_icon': "images/Draft_Observed.png",
            'deductibles_icon': "images/bunkers.png",
            'calculations_icon': "images/Calculation1.png",
            'results_icon': "images/Result.png",
            'ship_icon': "images/ship.png",
            'time_icon': "images/time.png",
            'calculate_icon': "images/correct.png",
            'interpolation_icon': "images/interpolation.png"
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

    def _create_notebook_tooltips(self):
        """Create tooltips for notebook tabs."""
        tooltip_texts = {
            0: "Vessel Info",
            1: "Time Sheet",
            2: "Draft Readings",
            3: "Deductibles",
            4: "Calculations",
            5: "Results"
        }
        tooltip_window = None

        def show_tooltip(event):
            nonlocal tooltip_window
            try:
                # Identify the element under the cursor
                element = self.notebook.identify(event.x, event.y)
                if "tab" in element:
                    index = self.notebook.index(f"@{event.x},{event.y}")
                    text = tooltip_texts.get(index)
                    if text:
                        if tooltip_window:
                            tooltip_window.destroy()
                        x, y, _, _ = self.notebook.bbox(index)
                        x += self.notebook.winfo_rootx() + 25
                        y += self.notebook.winfo_rooty() + 20
                        tooltip_window = tk.Toplevel(self.notebook)
                        tooltip_window.wm_overrideredirect(True)
                        tooltip_window.wm_geometry(f"+{x}+{y}")
                        label = tk.Label(tooltip_window, text=text, background="#FFFFE0",
                                         relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
                        label.pack(ipadx=1)
            except tk.TclError:
                pass  # Ignore errors when the mouse is not over a tab

        def hide_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None

        self.notebook.bind("<Enter>", show_tooltip)
        self.notebook.bind("<Leave>", hide_tooltip)
        self.notebook.bind("<Motion>", show_tooltip)

    def update_style(self, theme: dict):
        """Update styles for non-ttk widgets on this page."""
        super().update_style(theme)
        self.title_label.config(
            background=theme["title_bg"], foreground=theme["title_fg"])
        self.results_text.config(
            bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["entry_insert"])
        for label in self.labeled_entries:
            label.config(background=theme["labeled_entry_label_bg"],
                         foreground=theme["labeled_entry_label_fg"])
        # Special handling for time sheet tk.Label widgets
        for label in self.time_sheet_tk_labels:
            label.config(background=theme["labeled_entry_label_bg"],
                         foreground=theme["labeled_entry_label_fg"])

        # Special handling for tkcalendar DateEntry and time Entry
        if DateEntry is not None:
            for key, (date_entry, time_entry) in self.time_sheet_entries.items():
                # DateEntry is a tk.Entry, not ttk
                date_entry.config(
                    background=theme["entry_bg"], foreground=theme["entry_fg"])
                # time_entry is a ttk.Entry, style is applied automatically

    def _create_vessel_tab(self):
        """Create vessel information tab"""
        frame = ttk.Frame(self.vessel_tab)
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Validation commands for numeric inputs
        vcmd_positive = (self.register(
            DraftValidator.validate_positive_numeric_entry_callback), '%P')
        vcmd_numeric = (self.register(
            DraftValidator.validate_numeric_entry_callback), '%P')

        # Operation Type
        op_frame = ttk.LabelFrame(frame, text="Operation Type")
        op_frame.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky='w')
        ttk.Radiobutton(op_frame, text="Loading", variable=self.operation_type,
                        value='load').pack(side='left', padx=5)
        ttk.Radiobutton(op_frame, text="Discharging", variable=self.operation_type,
                        value='discharge').pack(side='left', padx=5)

        # Vessel Name
        self.vessel_name_entry = self.create_labeled_entry(
            frame, "Vessel Name:", 1, 0, width=30
        )[1]

        # Draft Number
        self.draft_number_entry = self.create_labeled_entry(
            frame, "Draft Number:", 2, 0, width=30
        )[1]

        # LBP (Length Between Perpendiculars)
        self.lbp_entry = self.create_labeled_entry(
            frame, "LBP (m):", 3, 0, validate='key', validatecommand=vcmd_positive, width=30
        )[1]

        # Light Ship
        self.light_ship_entry = self.create_labeled_entry(
            frame, "Light Ship (mt):", 4, 0, validate='key', validatecommand=vcmd_positive, width=30
        )[1]

        # Declared Constant
        self.declared_constant_entry = self.create_labeled_entry(
            frame, "Declared Constant (mt):", 5, 0, validate='key', validatecommand=vcmd_numeric, width=30
        )[1]

        # Port of Registry
        self.port_of_registry_entry = self.create_labeled_entry(
            frame, "Port of Registry:", 1, 2, width=30
        )[1]

        # Product
        self.product_entry = self.create_labeled_entry(
            frame, "Product:", 5, 2, width=30
        )[1]

        # IMO
        self.imo_entry = self.create_labeled_entry(
            frame, "IMO:", 2, 2, width=15,
            validate='key', validatecommand=(self.register(lambda P: P.isdigit() and len(P) <= 8), '%P')
        )[1]

        # Client
        self.client_entry = self.create_labeled_entry(
            frame, "Client:", 3, 2, width=30
        )[1]

        # Loading Port
        self.loading_port_entry = self.create_labeled_entry(
            frame, "Loading Port:", 6, 0, width=30
        )[1]

        # Discharging Port
        self.discharging_port_entry = self.create_labeled_entry(
            frame, "Discharging Port:", 6, 2, width=30
        )[1]

        # Quantity B/L
        self.quantity_bl_entry = self.create_labeled_entry(
            frame, "Quantity B/L (mt):", 7, 0, validate='key', validatecommand=vcmd_positive, width=30
        )[1]

    def _create_time_sheet_tab(self):
        """Create time sheet tab"""
        frame = ttk.Frame(self.time_sheet_tab)
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        time_sheet_labels = [
            "End of Sea Passage:", "Notice Tendered:", "Pilot On Board:",
            "First Line:", "All Fast:", "Surveyor On Board:",
            "Initial Draft Started:", "Initial Draft Completed:",
            "Operation Started:", "Operation Completed:",
            "Final Draft Started:", "Final Draft Completed:",
            "Vessel Sailed:"
        ]

        if DateEntry is None:
            # Fallback to simple Entry if tkcalendar is not installed
            error_label = ttk.Label(
                frame,
                text="Warning: 'tkcalendar' is not installed. Using simple text fields.\n"
                     "Install it for a better experience: pip install tkcalendar",
                foreground="orange",
                wraplength=400
            )
            error_label.pack(pady=(5, 10))
            for i, label_text in enumerate(time_sheet_labels):
                key = label_text.replace(" ", "_").replace(":", "").lower()
                self.time_sheet_entries[key] = self.create_labeled_entry(
                    frame, label_text, i + 1, 0, width=25)[1]
        else:
            # Use DateEntry for a better UX
            for i, label_text in enumerate(time_sheet_labels):
                key = label_text.replace(" ", "_").replace(":", "").lower()
                label = tk.Label(frame, text=label_text,  # This is a tk.Label, it needs manual update
                                 background='black', foreground='gold')
                label.grid(row=i, column=0, padx=5, pady=3, sticky='e')
                self.time_sheet_tk_labels.append(label)

                # DateEntry for the date part
                date_entry = DateEntry(frame, width=12, background='darkblue',
                                       foreground='white', borderwidth=2,
                                       date_pattern='y-mm-dd')
                date_entry.grid(row=i, column=1, padx=5, pady=3, sticky='w')

                # Simple Entry for the time part
                time_entry = ttk.Entry(frame, width=8)
                time_entry.grid(row=i, column=2, padx=5, pady=3, sticky='w')

                # Store both widgets
                self.time_sheet_entries[key] = (date_entry, time_entry)

    def _create_draft_tab(self):
        """Create draft readings tab"""
        frame = ttk.Frame(self.draft_tab)
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        vcmd_numeric = (self.register(
            DraftValidator.validate_numeric_entry_callback), '%P')

        # Observed drafts section
        observed_frame = ttk.LabelFrame(frame, text="Observed Drafts (meters)")
        observed_frame.pack(fill='x', pady=5)

        # Forward drafts
        self.draft_for_port_entry = self.create_labeled_entry(
            observed_frame, "Forward Port:", 0, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.draft_for_star_entry = self.create_labeled_entry(
            observed_frame, "Forward Starboard:", 0, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # Midship drafts
        self.draft_mid_port_entry = self.create_labeled_entry(
            observed_frame, "Midship Port:", 1, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.draft_mid_star_entry = self.create_labeled_entry(
            observed_frame, "Midship Starboard:", 1, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # Aft drafts
        self.draft_aft_port_entry = self.create_labeled_entry(
            observed_frame, "Aft Port:", 2, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.draft_aft_star_entry = self.create_labeled_entry(
            observed_frame, "Aft Starboard:", 2, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # Positions and distances section
        positions_frame = ttk.LabelFrame(frame, text="Positions and Distances")
        positions_frame.pack(fill='x', pady=5)

        # Distances from perpendiculars
        self.distance_from_for_pp_entry = self.create_labeled_entry(
            positions_frame, "Dist. from Forward PP (m):", 0, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.distance_from_aft_pp_entry = self.create_labeled_entry(
            positions_frame, "Dist. from Aft PP (m):", 0, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.distance_from_mid_pp_entry = self.create_labeled_entry(
            positions_frame, "Dist. from Mid PP (m):", 0, 4,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # Positions
        self.position_from_for_pp_entry = self.create_labeled_entry(
            positions_frame, "Forward Position:", 1, 0, width=10
        )[1]

        self.position_from_aft_pp_entry = self.create_labeled_entry(
            positions_frame, "Aft Position:", 1, 2, width=10
        )[1]

        self.position_from_mid_pp_entry = self.create_labeled_entry(
            positions_frame, "Mid Position:", 1, 4, width=10
        )[1]

        # Trim and density
        trim_frame = ttk.LabelFrame(frame, text="Trim and Density")
        trim_frame.pack(fill='x', pady=5)

        self.trim_observed_entry = self.create_labeled_entry(
            trim_frame, "Observed Trim (m):", 0, 0,
            width=10, state='readonly'
        )[1]

        self.dock_density_entry = self.create_labeled_entry(
            trim_frame, "Dock Density:", 0, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.table_density_entry = self.create_labeled_entry(
            trim_frame, "Table Density:", 0, 4,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

    def _create_deductibles_tab(self):
        """Create deductibles data tab"""
        frame = ttk.Frame(self.bunker_tab)
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        vcmd_numeric = (self.register(
            DraftValidator.validate_numeric_entry_callback), '%P')

        self.ballast_entry = self.create_labeled_entry(
            frame, "Ballast (mt):", 0, 0, validate='key', validatecommand=vcmd_numeric)[1]
        self.fuel_entry = self.create_labeled_entry(
            frame, "Fuel (mt):", 1, 0, validate='key', validatecommand=vcmd_numeric)[1]
        self.gas_oil_entry = self.create_labeled_entry(
            frame, "Gas Oil (mt):", 2, 0, validate='key', validatecommand=vcmd_numeric)[1]
        self.lub_oil_entry = self.create_labeled_entry(
            frame, "Lub Oil (mt):", 3, 0, validate='key', validatecommand=vcmd_numeric)[1]
        self.slops_entry = self.create_labeled_entry(
            frame, "Slops (mt):", 4, 0, validate='key', validatecommand=vcmd_numeric)[1]
        self.others_entry = self.create_labeled_entry(
            frame, "Others (mt):", 5, 0, validate='key', validatecommand=vcmd_numeric)[1]
        self.fresh_water_entry = self.create_labeled_entry(
            frame, "Fresh Water (mt):", 6, 0, validate='key', validatecommand=vcmd_numeric)[1]

        # Button to calculate total deductibles
        ttk.Button(frame, text="Calculate Deductibles",
                   command=self.calculate_total_deductibles).grid(
            row=7, column=0, columnspan=2, pady=10)

    def _create_calculation_tab(self):
        """Create calculations tab"""
        frame = ttk.Frame(self.calculation_tab)
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Interpolation data
        interp_frame = ttk.LabelFrame(frame, text="Interpolation Data")
        interp_frame.pack(fill='x', pady=5)

        vcmd_numeric = (self.register(
            DraftValidator.validate_numeric_entry_callback), '%P')

        # Draft values
        self.entries['draft_sup'] = self.create_labeled_entry(
            interp_frame, "Draft Sup:", 0, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['draft_inf'] = self.create_labeled_entry(
            interp_frame, "Draft Inf:", 0, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # Displacement values
        self.entries['displacement_sup'] = self.create_labeled_entry(
            interp_frame, "Disp. Sup (mt):", 1, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['displacement_inf'] = self.create_labeled_entry(
            interp_frame, "Disp. Inf (mt):", 1, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # TPC values
        self.entries['tpc_sup'] = self.create_labeled_entry(
            interp_frame, "TPC Sup:", 2, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['tpc_inf'] = self.create_labeled_entry(
            interp_frame, "TPC Inf:", 2, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # LCF values
        self.entries['lcf_sup'] = self.create_labeled_entry(
            interp_frame, "LCF Sup:", 3, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['lcf_inf'] = self.create_labeled_entry(
            interp_frame, "LCF Inf:", 3, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # MTC calculation data
        mtc_frame = ttk.LabelFrame(frame, text="MTC Calculation Data")
        mtc_frame.pack(fill='x', pady=5)

        # D+50 values
        self.entries['d_plus50_sup'] = self.create_labeled_entry(
            mtc_frame, "D+50 Sup:", 0, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['d_plus50_inf'] = self.create_labeled_entry(
            mtc_frame, "D+50 Inf:", 0, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['d_plus50'] = self.create_labeled_entry(
            mtc_frame, "D+50:", 0, 4,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # MTC+ values
        self.entries['mtc_plus50_sup'] = self.create_labeled_entry(
            mtc_frame, "MTC+ Sup:", 1, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['mtc_plus50_inf'] = self.create_labeled_entry(
            mtc_frame, "MTC+ Inf:", 1, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # D-50 values
        self.entries['d_moins50_sup'] = self.create_labeled_entry(
            mtc_frame, "D-50 Sup:", 2, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['d_moins50_inf'] = self.create_labeled_entry(
            mtc_frame, "D-50 Inf:", 2, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['d_moins50'] = self.create_labeled_entry(
            mtc_frame, "D-50:", 2, 4,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        # MTC- values
        self.entries['mtc_moins50_sup'] = self.create_labeled_entry(
            mtc_frame, "MTC- Sup:", 3, 0,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.entries['mtc_moins50_inf'] = self.create_labeled_entry(
            mtc_frame, "MTC- Inf:", 3, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

    def _create_results_tab(self):
        """Create results display tab"""
        frame = ttk.Frame(self.results_tab)
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Results text area
        results_label = tk.Label(
            frame, text="Survey Results:", background='gray12', foreground='gold')
        results_label.pack(anchor='w', pady=5)
        self.labeled_entries.append(results_label)
        self.results_text = tk.Text(frame, height=20, width=80, bg='black', fg='green',
                                    insertbackground='white', selectbackground='blue')
        self.results_text.pack(fill='both', expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text.config(yscrollcommand=scrollbar.set)

    def _create_action_buttons(self):
        """Create action buttons at the bottom"""
        # Configure grid weights for button area
        self.grid_rowconfigure(2, weight=0)  # Button row - no expansion
        self.grid_columnconfigure(0, weight=1)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, sticky='ew', pady=10)

        # Configure button frame grid
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Left side buttons
        left_buttons = ttk.Frame(button_frame)
        left_buttons.grid(row=0, column=0, sticky='w')

        ttk.Button(left_buttons, text="Drafts", image=self.calculate_icon, compound=tk.LEFT,
                   command=self.calculate_corrected_drafts).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="MFA/MOM/QM", image=self.calculate_icon, compound=tk.LEFT,
                   command=self.calculate_mfa_mom_qm).pack(side='left', padx=5)
        interpolate_btn = ttk.Button(left_buttons, image=self.interpolation_icon,
                                     command=self.calculate_interpolation)
        interpolate_btn.pack(side='left', padx=5)
        self.create_tooltip(interpolate_btn, "Interpolate Values")

        ttk.Button(left_buttons, text="MTC", image=self.calculate_icon, compound=tk.LEFT,
                   command=self.calculate_mtc).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Trim Corrections", image=self.calculate_icon, compound=tk.LEFT,
                   command=self.calculate_trim_corrections).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Density Correction", image=self.calculate_icon, compound=tk.LEFT,
                   command=self.calculate_density_correction).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Initial Results", image=self.calculate_icon, compound=tk.LEFT,
                   command=self.calculate_initial_results).pack(side='left', padx=5)

        # Right side buttons
        right_buttons = ttk.Frame(button_frame)
        right_buttons.grid(row=0, column=1, sticky='e')

        # Generate Report Button
        report_btn = ttk.Button(right_buttons, image=self.report_icon_photo,
                                command=self.generate_report)
        report_btn.pack(side='right', padx=5)
        self.create_tooltip(report_btn, "Generate comprehensive survey report")

        # Save Data Button
        save_btn = ttk.Button(right_buttons, image=self.save_icon_photo,
                              command=self.save_data)
        save_btn.pack(side='right', padx=5)
        self.create_tooltip(save_btn, "Save current survey data to a file")

        # Load Data Button
        load_btn = ttk.Button(right_buttons, image=self.load_icon_photo,
                              command=self.load_data)
        load_btn.pack(side='right', padx=5)
        self.create_tooltip(load_btn, "Load survey data from a file")

        # Clear All Button
        clear_btn = ttk.Button(right_buttons, image=self.clear_icon_photo,
                               command=self.clear_all)
        clear_btn.pack(side='right', padx=5)
        self.create_tooltip(
            clear_btn, "Clear all input fields and calculated data")

    def calculate_corrected_drafts(self):
        """Calculate corrected drafts from observed values"""
        self.controller.set_survey_type('initial')
        try:
            # Validate vessel data
            vessel_data_for_validation = {
                'lbp': self.lbp_entry.get(),
                'distance_from_for_pp': self.distance_from_for_pp_entry.get(),
                'distance_from_aft_pp': self.distance_from_aft_pp_entry.get(),
                'distance_from_mid_pp': self.distance_from_mid_pp_entry.get(),
                'position_from_for_pp': self.position_from_for_pp_entry.get(),
                'position_from_aft_pp': self.position_from_aft_pp_entry.get(),
                # Add new fields for validation
                'position_from_mid_pp': self.position_from_mid_pp_entry.get(), 'light_ship': self.light_ship_entry.get(), 'declared_constant': self.declared_constant_entry.get(), 'quantity_bl': self.quantity_bl_entry.get()
            }

            # Validate all vessel related data
            is_valid, error_msg = self.controller.validate_vessel_data(
                vessel_data_for_validation)
            # Note: Other string fields like port_of_registry are not validated for format here, only presence if required.

            if not is_valid:
                messagebox.showerror("Validation Error", error_msg)
                return

            # Validate observed drafts
            observed_drafts = {
                'draft_for_port': self.draft_for_port_entry.get(),
                'draft_for_star': self.draft_for_star_entry.get(),
                'draft_mid_port': self.draft_mid_port_entry.get(),
                'draft_mid_star': self.draft_mid_star_entry.get(),
                'draft_aft_port': self.draft_aft_port_entry.get(),
                'draft_aft_star': self.draft_aft_star_entry.get()
            }

            is_valid, error_msg = self.controller.validate_observed_drafts(
                observed_drafts)
            if not is_valid:
                messagebox.showerror("Validation Error", error_msg)
                return

            # Calculate and display observed trim
            draft_for = (float(
                observed_drafts['draft_for_port']) + float(observed_drafts['draft_for_star'])) / 2
            draft_aft = (float(
                observed_drafts['draft_aft_port']) + float(observed_drafts['draft_aft_star'])) / 2
            observed_trim = draft_aft - draft_for

            self.trim_observed_entry.config(state='normal')
            self.trim_observed_entry.delete(0, tk.END)
            self.trim_observed_entry.insert(0, f"{observed_trim:.3f}")
            self.trim_observed_entry.config(state='readonly')

            # Set vessel information
            lbp_val = float(self.lbp_entry.get()
                            ) if self.lbp_entry.get() else None
            light_ship_val = float(self.light_ship_entry.get(
            )) if self.light_ship_entry.get() else None
            declared_constant_val = float(self.declared_constant_entry.get(
            )) if self.declared_constant_entry.get() else None
            quantity_bl_val = float(self.quantity_bl_entry.get(
            )) if self.quantity_bl_entry.get() else None
            table_density_val = float(self.table_density_entry.get()
                                      ) if self.table_density_entry.get() else None
            dock_density_val = float(self.dock_density_entry.get()
                                     ) if self.dock_density_entry.get() else None

            self.controller.set_vessel_information(
                vessel_name=self.vessel_name_entry.get(),
                draft_number=self.draft_number_entry.get(),
                lbp=lbp_val,
                light_ship=light_ship_val,
                declared_constant=declared_constant_val,
                port_of_registry=self.port_of_registry_entry.get(),
                product=self.product_entry.get(),
                loading_port=self.loading_port_entry.get(),
                imo=self.imo_entry.get(),
                client=self.client_entry.get(),
                discharging_port=self.discharging_port_entry.get(),
                quantity_bl=quantity_bl_val,
                table_density=table_density_val,
                dock_density=dock_density_val,
                operation_type=self.operation_type.get(),
                # Also save distances and positions to the central data store
                distance_from_for_pp=float(self.distance_from_for_pp_entry.get(
                )) if self.distance_from_for_pp_entry.get() else None,
                position_from_for_pp=self.position_from_for_pp_entry.get(),
                distance_from_mid_pp=float(self.distance_from_mid_pp_entry.get(
                )) if self.distance_from_mid_pp_entry.get() else None,
                position_from_mid_pp=self.position_from_mid_pp_entry.get(),
                distance_from_aft_pp=float(self.distance_from_aft_pp_entry.get(
                )) if self.distance_from_aft_pp_entry.get() else None,
                position_from_aft_pp=self.position_from_aft_pp_entry.get()
            )

            # Set time sheet information
            time_sheet_data = {}
            for key, (date_entry, time_entry) in self.time_sheet_entries.items():
                time_val = time_entry.get()
                # Combine date and time, handle placeholder for time
                full_datetime = f"{date_entry.get()} {time_val}".strip(
                )
                time_sheet_data[key] = full_datetime
            self.controller.set_time_sheet_information(time_sheet_data)

            # Set vessel parameters for the current survey
            vessel_params = {
                'dock_density': dock_density_val,
                'table_density': table_density_val,
                'distance_from_for_pp': float(self.distance_from_for_pp_entry.get()) if self.distance_from_for_pp_entry.get() else 0.0,
                'position_from_for_pp': self.position_from_for_pp_entry.get(),
                'distance_from_mid_pp': float(self.distance_from_mid_pp_entry.get()) if self.distance_from_mid_pp_entry.get() else 0.0,
                'position_from_mid_pp': self.position_from_mid_pp_entry.get(),
                'distance_from_aft_pp': float(self.distance_from_aft_pp_entry.get()) if self.distance_from_aft_pp_entry.get() else 0.0,
                'position_from_aft_pp': self.position_from_aft_pp_entry.get(),
            }
            self.controller.set_vessel_params(vessel_params)

            # Set observed drafts
            self.controller.set_observed_drafts(
                draft_for_port=float(observed_drafts['draft_for_port']),
                draft_for_star=float(observed_drafts['draft_for_star']),
                draft_mid_port=float(
                    observed_drafts.get('draft_mid_port', 0.0)),
                draft_mid_star=float(
                    observed_drafts.get('draft_mid_star', 0.0)),
                draft_aft_port=float(observed_drafts['draft_aft_port']),
                draft_aft_star=float(observed_drafts['draft_aft_star'])
            )

            # Calculate corrected drafts
            lbp = float(vessel_data_for_validation['lbp'])
            corrected_drafts = self.controller.calculate_corrected_drafts(
                lbp=lbp,
                distance_from_for_pp=float(
                    vessel_data_for_validation['distance_from_for_pp']),
                distance_from_aft_pp=float(
                    vessel_data_for_validation['distance_from_aft_pp']),
                distance_from_mid_pp=float(
                    vessel_data_for_validation.get('distance_from_mid_pp', 0)),
                position_from_for_pp=vessel_data_for_validation['position_from_for_pp'],
                position_from_aft_pp=vessel_data_for_validation['position_from_aft_pp'],
                position_from_mid_pp=vessel_data_for_validation.get(
                    'position_from_mid_pp', 'N/A'),  # type: ignore
                trim_observed=observed_trim
            )

            # Display results
            self.display_corrected_drafts(corrected_drafts)

        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def calculate_mfa_mom_qm(self):
        """Calculate MFA, MOM, and QM values"""
        self.controller.set_survey_type('initial')
        try:  # type: ignore
            corrected_drafts = self.controller.survey_data.get_draft_data().get(
                'corrected_drafts', {})

            if not corrected_drafts:
                messagebox.showwarning(
                    "Warning", "Please calculate corrected drafts first")
                return

            mfa_mom_qm = self.controller.calculate_mfa_mom_qm(
                corrected_drafts['draft_for_corrected'],
                corrected_drafts['draft_aft_corrected'],
                corrected_drafts['draft_mid_corrected']
            )

            self.display_mfa_mom_qm(mfa_mom_qm)

        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def calculate_interpolation(self):
        """Calculate interpolated values"""
        self.controller.set_survey_type('initial')
        try:  # type: ignore
            # Get interpolation data
            interp_data = {key: entry.get() for key, entry in self.entries.items()
                           if key in ['draft_sup', 'draft_inf', 'displacement_sup', 'displacement_inf',
                                      'tpc_sup', 'tpc_inf', 'lcf_sup', 'lcf_inf']}

            is_valid, error_msg = self.controller.validate_interpolation_data(
                interp_data)
            if not is_valid:
                messagebox.showerror("Validation Error", error_msg)
                return

            # Get QM value
            draft_data = self.controller.survey_data.get_current_survey_data().get('draft_data', {})
            qm = draft_data.get('mfa_mom_qm', {}).get('qm', 0)

            if qm == 0:
                messagebox.showwarning(
                    "Warning", "Please calculate MFA/MOM/QM first")
                return

            # Calculate interpolation
            interp_results = self.controller.calculate_interpolation(
                qm=float(qm),
                draft_sup=float(interp_data['draft_sup']),
                draft_inf=float(interp_data['draft_inf']),
                displacement_sup=float(interp_data['displacement_sup']),
                displacement_inf=float(interp_data['displacement_inf']),
                tpc_sup=float(interp_data['tpc_sup']),
                tpc_inf=float(interp_data['tpc_inf']),
                lcf_sup=float(interp_data['lcf_sup']),
                lcf_inf=float(interp_data['lcf_inf'])
            )

            self.display_interpolation_results(interp_results)

        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def calculate_mtc(self):
        """Calculate MTC values"""
        self.controller.set_survey_type('initial')
        try:  # type: ignore
            # Get MTC data
            mtc_data = {key: entry.get() for key, entry in self.entries.items()
                        if key in ['d_plus50_sup', 'd_plus50_inf', 'd_plus50',
                                   'mtc_plus50_sup', 'mtc_plus50_inf',
                                   'd_moins50_sup', 'd_moins50_inf', 'd_moins50',
                                   'mtc_moins50_sup', 'mtc_moins50_inf']}

            is_valid, error_msg = self.controller.validate_mtc_data(mtc_data)
            if not is_valid:
                messagebox.showerror("Validation Error", error_msg)
                return

            # Calculate MTC values
            mtc_results = self.controller.calculate_mtc_values(
                d_plus50_sup=float(mtc_data['d_plus50_sup']),
                d_plus50_inf=float(mtc_data['d_plus50_inf']),
                d_plus50=float(mtc_data['d_plus50']),
                mtc_plus50_sup=float(mtc_data['mtc_plus50_sup']),
                mtc_plus50_inf=float(mtc_data['mtc_plus50_inf']),
                d_moins50_sup=float(mtc_data['d_moins50_sup']),
                d_moins50_inf=float(mtc_data['d_moins50_inf']),
                d_moins50=float(mtc_data['d_moins50']),
                mtc_moins50_sup=float(mtc_data['mtc_moins50_sup']),
                mtc_moins50_inf=float(mtc_data['mtc_moins50_inf'])
            )

            self.display_mtc_results(mtc_results)

        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def calculate_trim_corrections(self):
        """Calculate first and second trim corrections."""
        self.controller.set_survey_type('initial')
        try:  # type: ignore
            draft_data = self.controller.survey_data.get_draft_data()
            corrected_drafts = draft_data.get('corrected_drafts', {})
            interp_results = draft_data.get('interpolation_results', {})
            mtc_results = draft_data.get('mtc_results', {})

            if not all([corrected_drafts, interp_results, mtc_results]):
                messagebox.showwarning(
                    "Warning", "Please perform Draft, Interpolation, and MTC calculations first.")
                return

            lbp_str = self.lbp_entry.get()
            if not lbp_str:
                messagebox.showwarning("Warning", "Please enter LBP value.")
                return

            trim_corrections = self.controller.calculate_trim_corrections(
                draft_for_corrected=corrected_drafts['draft_for_corrected'],
                draft_aft_corrected=corrected_drafts['draft_aft_corrected'],
                tpc=interp_results['tpc'],
                lcf=interp_results['lcf'],
                lbp=float(lbp_str),
                delta_mtc=mtc_results['delta_mtc'],
                displacement=interp_results['displacement']
            )

            self.display_trim_corrections(trim_corrections)

        except KeyError as e:
            messagebox.showerror(
                "Missing Data", f"Could not find required data: {e}. Please perform all previous calculations.")
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please ensure LBP is a valid number.")
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def calculate_density_correction(self):
        """Calculate density correction for displacement."""
        self.controller.set_survey_type('initial')
        try:
            # Get data from controller
            vessel_data = self.controller.survey_data.get_vessel_data()
            calculation_data = self.controller.survey_data.get_calculation_data()
            trim_corrections = calculation_data.get('trim_corrections', {})

            # Check for required data
            if 'corrected_displacement_for_trim' not in trim_corrections:
                messagebox.showwarning(
                    "Warning", "Please calculate trim corrections first.")
                return

            table_density_str = self.table_density_entry.get()
            dock_density_str = self.dock_density_entry.get()

            if not table_density_str or not dock_density_str:
                messagebox.showwarning(
                    "Warning", "Please enter Table Density and Dock Density.")
                return

            # Perform calculation
            density_correction_result = self.controller.calculate_density_corrections(
                table_density=float(table_density_str),
                dock_density=float(dock_density_str),
                corrected_displacement_for_trim=trim_corrections['corrected_displacement_for_trim']
            )

            # Display result
            self.display_density_correction(density_correction_result)

        except KeyError as e:
            messagebox.showerror(
                "Missing Data", f"Required data not found: {e}")
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def calculate_total_deductibles(self):
        """Calculate and save total deductibles."""
        self.controller.set_survey_type('initial')
        try:
            bunker_data = {
                'ballast': self.ballast_entry.get(),
                'fuel': self.fuel_entry.get(),
                'gas_oil': self.gas_oil_entry.get(),
                'lub_oil': self.lub_oil_entry.get(),
                'slops': self.slops_entry.get(),
                'others': self.others_entry.get(),
                'fresh_water': self.fresh_water_entry.get()
            }

            is_valid, error_msg = self.controller.validate_bunker_data(
                bunker_data)
            if not is_valid:
                messagebox.showerror("Validation Error", error_msg)
                return

            total_deductibles = self.controller.calculate_total_deductibles(
                bunker_data)

            messagebox.showinfo(
                "Success", f"Total deductibles calculated: {total_deductibles:.3f} mt")

        except Exception as e:
            messagebox.showerror(
                "Calculation Error", f"Error calculating deductibles: {str(e)}")

    def calculate_initial_results(self):
        """
        Calculate initial results based on operation type:
        - 'loading': Calculates the constant.
        - 'discharging': Calculates the cargo + constant.
        """
        self.controller.set_survey_type('initial')
        try:
            # Get necessary data from the controller
            vessel_data = self.controller.survey_data.get_vessel_data()
            calculation_data = self.controller.survey_data.get_calculation_data()

            op_type = vessel_data.get('operation_type')
            light_ship = vessel_data.get('light_ship')
            corrected_displacement = calculation_data.get('density_corrections', {}).get(
                'corrected_displacement_for_density')
            total_deductibles = calculation_data.get('displacement_corrections', {}).get(
                'total_deductibles')

            # Validate that all required data is present
            if not all([op_type, light_ship, corrected_displacement, total_deductibles is not None]):
                messagebox.showwarning(
                    "Missing Data", "Please ensure Operation Type, Light Ship, Density Correction, and Deductibles are all calculated/entered.")
                return

            # Perform calculations based on operation type
            if op_type == 'load':
                net_displacement = round(
                    corrected_displacement - total_deductibles, 3)
                constant = round(net_displacement - light_ship, 3)
                self.controller.set_initial_results({
                    'net_displacement': net_displacement,
                    'constant': constant
                })
                self.results_text.insert(
                    tk.END, "\n=== INITIAL RESULTS (LOADING) ===\n")
                self.results_text.insert(
                    tk.END, f"Net Displacement: {net_displacement:.3f} mt\n")
                self.results_text.insert(
                    tk.END, f"Constant: {constant:.3f} mt\n")
            elif op_type == 'discharge':
                load_displacement = round(
                    corrected_displacement - total_deductibles, 3)
                cargo_plus_constant = round(load_displacement - light_ship, 3)
                self.controller.set_initial_results({
                    'load_displacement': load_displacement,
                    'cargo_plus_constant': cargo_plus_constant
                })
                self.results_text.insert(
                    tk.END, "\n=== INITIAL RESULTS (DISCHARGING) ===\n")
                self.results_text.insert(
                    tk.END, f"Cargo + Constant: {cargo_plus_constant:.3f} mt\n")

        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def display_corrected_drafts(self, corrected_drafts: dict):
        """Display corrected draft results"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "=== CORRECTED DRAFTS ===\n\n")

        vessel_data = self.controller.get_survey_summary().get('vessel_data', {})
        observed_drafts = self.controller.survey_data.get_draft_data().get('observed_drafts', {})

        self.results_text.insert(
            tk.END, f"Vessel: {vessel_data.get('vessel_name', 'N/A')} | LBP: {vessel_data.get('lbp', 'N/A')} m\n")
        self.results_text.insert(
            tk.END, f"Dock Density: {vessel_data.get('dock_density', 'N/A')} | Table Density: {vessel_data.get('table_density', 'N/A')}\n\n")

        # Observed Drafts
        self.results_text.insert(tk.END, "--- Observed Drafts ---\n")
        self.results_text.insert(
            tk.END, f"Forward: Port={observed_drafts.get('draft_for_port', 0.0):.3f} | Starboard={observed_drafts.get('draft_for_star', 0.0):.3f}\n")
        self.results_text.insert(
            tk.END, f"Midship: Port={observed_drafts.get('draft_mid_port', 0.0):.3f} | Starboard={observed_drafts.get('draft_mid_star', 0.0):.3f}\n")
        self.results_text.insert(
            tk.END, f"Aft:     Port={observed_drafts.get('draft_aft_port', 0.0):.3f} | Starboard={observed_drafts.get('draft_aft_star', 0.0):.3f}\n\n")

        # Correction Distances
        self.results_text.insert(tk.END, "--- Correction Distances ---\n")
        self.results_text.insert(
            tk.END, f"Dist. from Fwd PP: {self.distance_from_for_pp_entry.get()} m ({self.position_from_for_pp_entry.get()})\n")
        self.results_text.insert(
            tk.END, f"Dist. from Mid PP: {self.distance_from_mid_pp_entry.get()} m ({self.position_from_mid_pp_entry.get()})\n")
        self.results_text.insert(
            tk.END, f"Dist. from Aft PP: {self.distance_from_aft_pp_entry.get()} m ({self.position_from_aft_pp_entry.get()})\n\n")

        # Corrected Drafts
        self.results_text.insert(tk.END, "--- Corrected Drafts ---\n")
        self.results_text.insert(
            tk.END, f"Corrected Forward Draft: {corrected_drafts['draft_for_corrected']:.3f} m\n")
        self.results_text.insert(
            tk.END, f"Corrected Aft Draft: {corrected_drafts['draft_aft_corrected']:.3f} m\n")
        self.results_text.insert(
            tk.END, f"Corrected Mid Draft: {corrected_drafts['draft_mid_corrected']:.3f} m\n")

        # Mean Drafts
        self.results_text.insert(tk.END, "\n--- Mean Drafts ---\n")
        self.results_text.insert(
            tk.END, f"Mean Forward Draft: {corrected_drafts['draft_for']:.3f} m\n")
        self.results_text.insert(
            tk.END, f"Mean Aft Draft: {corrected_drafts['draft_aft']:.3f} m\n")
        self.results_text.insert(
            tk.END, f"Mean Midship Draft: {corrected_drafts['draft_mid']:.3f} m\n")

        # Trims and LBM
        self.results_text.insert(tk.END, "\n--- Trims & LBM ---\n")
        self.results_text.insert(
            tk.END, f"Observed Trim: {corrected_drafts['trim_observed']:.3f} m\n")
        self.results_text.insert(
            tk.END, f"Corrected Trim: {corrected_drafts.get('trim_corrected', 0.0):.3f} m\n")
        self.results_text.insert(
            tk.END, f"LBM: {corrected_drafts['lbm']:.3f} m\n")

    def display_mfa_mom_qm(self, mfa_mom_qm: dict):
        """Display MFA/MOM/QM results"""
        if self.results_text.get(1.0, tk.END).strip() == "":
            self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "\n=== MFA/MOM/QM ===\n")
        self.results_text.insert(tk.END, f"MFA: {mfa_mom_qm['mfa']:.3f} m\n")
        self.results_text.insert(tk.END, f"MOM: {mfa_mom_qm['mom']:.3f} m\n")
        self.results_text.insert(tk.END, f"QM: {mfa_mom_qm['qm']:.3f} m\n")

    def display_interpolation_results(self, interp_results: dict):
        """Display interpolation results"""
        if self.results_text.get(1.0, tk.END).strip() == "":
            self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "\n=== INTERPOLATION RESULTS ===\n")
        self.results_text.insert(
            tk.END, f"Displacement: {interp_results['displacement']:.3f} mt\n")
        self.results_text.insert(tk.END, f"TPC: {interp_results['tpc']:.3f}\n")
        self.results_text.insert(
            tk.END, f"LCF: {interp_results['lcf']:.3f} m\n")

    def display_mtc_results(self, mtc_results: dict):
        """Display MTC calculation results"""
        self.results_text.insert(tk.END, "\n=== MTC RESULTS ===\n")
        self.results_text.insert(
            tk.END, f"MTC1 (MTC+): {mtc_results['mtc1']:.3f}\n")
        self.results_text.insert(
            tk.END, f"MTC2 (MTC-): {mtc_results['mtc2']:.3f}\n")
        self.results_text.insert(
            tk.END, f"Delta MTC: {mtc_results['delta_mtc']:.3f}\n")

    def display_trim_corrections(self, trim_corrections: dict):
        """Display trim correction results"""
        self.results_text.insert(tk.END, "\n=== TRIM CORRECTIONS ===\n")
        self.results_text.insert(
            tk.END, f"1st Trim Correction: {trim_corrections['first_trim_correction']:.3f} mt\n")
        self.results_text.insert(
            tk.END, f"2nd Trim Correction: {trim_corrections['second_trim_correction']:.3f} mt\n")
        self.results_text.insert(
            tk.END, f"Total Trim Correction: {trim_corrections['first_trim_correction'] + trim_corrections['second_trim_correction']:.3f} mt\n")
        self.results_text.insert(
            tk.END, f"Displacement Corrected for Trim: {trim_corrections['corrected_displacement_for_trim']:.3f} mt\n")

    def display_density_correction(self, density_correction: dict):
        """Display density correction results"""
        self.results_text.insert(tk.END, "\n=== DENSITY CORRECTION ===\n")
        self.results_text.insert(
            tk.END, f"Displacement Corrected for Density: {density_correction['corrected_displacement_for_density']:.3f} mt\n")

    def generate_report(self):
        """Generate complete survey report"""
        try:
            report = self.controller.generate_survey_report()
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, report)
        except Exception as e:
            messagebox.showerror("Report Error", str(e))

    def save_data(self):
        """Save survey data to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.controller.save_survey_data(filename)
                messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def load_data(self):
        """Load survey data from file"""
        try:
            filename = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.controller.load_survey_data(filename)
                self.populate_fields_from_data()
                messagebox.showinfo("Success", "Data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def populate_fields_from_data(self):
        """Populate form fields from loaded data"""
        try:
            survey_data = self.controller.get_survey_summary()

            # Populate vessel data
            vessel_data = survey_data.get('vessel_data', {})  # type: ignore
            self._set_entry_value(self.vessel_name_entry,
                                  vessel_data.get('vessel_name', ''))
            self._set_entry_value(self.draft_number_entry,
                                  vessel_data.get('draft_number', ''))
            self._set_entry_value(self.lbp_entry, vessel_data.get('lbp', ''))
            self._set_entry_value(self.light_ship_entry,
                                  vessel_data.get('light_ship', ''))
            self._set_entry_value(
                self.declared_constant_entry, vessel_data.get('declared_constant', ''))
            self._set_entry_value(
                self.port_of_registry_entry, vessel_data.get('port_of_registry', ''))
            self._set_entry_value(self.product_entry,
                                  vessel_data.get('product', ''))
            self._set_entry_value(self.loading_port_entry,
                                  vessel_data.get('loading_port', ''))
            self._set_entry_value(self.imo_entry,
                                  vessel_data.get('imo', ''))
            self._set_entry_value(self.client_entry,
                                  vessel_data.get('client', ''))
            self._set_entry_value(
                self.discharging_port_entry, vessel_data.get('discharging_port', ''))
            self._set_entry_value(self.quantity_bl_entry,
                                  vessel_data.get('quantity_bl', ''))

            # Populate time sheet data
            time_sheet_data = vessel_data.get('time_sheet', {})
            for key, (date_entry, time_entry) in self.time_sheet_entries.items():
                full_datetime = time_sheet_data.get(key, '')
                date_part, time_part = (full_datetime.split(' ', 1) + [''])[:2]
                self._set_entry_value(date_entry, date_part)
                if time_part:
                    self._set_entry_value(time_entry, time_part)
                else:
                    self._set_entry_value(time_entry, "")

            # Populate draft data (for initial survey)
            initial_draft_data = survey_data.get(
                'initial', {}).get('draft_data', {})  # type: ignore
            observed_drafts = initial_draft_data.get('observed_drafts', {})
            self._set_entry_value(self.draft_for_port_entry,
                                  observed_drafts.get('draft_for_port', ''))
            self._set_entry_value(self.draft_for_star_entry,
                                  observed_drafts.get('draft_for_star', ''))
            self._set_entry_value(self.draft_mid_port_entry,
                                  observed_drafts.get('draft_mid_port', ''))
            self._set_entry_value(self.draft_mid_star_entry,
                                  observed_drafts.get('draft_mid_star', ''))
            self._set_entry_value(self.draft_aft_port_entry,
                                  observed_drafts.get('draft_aft_port', ''))
            self._set_entry_value(self.draft_aft_star_entry,
                                  observed_drafts.get('draft_aft_star', ''))

            # Populate positions and distances
            self._set_entry_value(
                self.distance_from_for_pp_entry, vessel_data.get('distance_from_for_pp', ''))
            self._set_entry_value(
                self.distance_from_aft_pp_entry, vessel_data.get('distance_from_aft_pp', ''))
            self._set_entry_value(
                self.distance_from_mid_pp_entry, vessel_data.get('distance_from_mid_pp', ''))
            self._set_entry_value(
                self.position_from_for_pp_entry, vessel_data.get('position_from_for_pp', ''))
            self._set_entry_value(
                self.position_from_aft_pp_entry, vessel_data.get('position_from_aft_pp', ''))
            self._set_entry_value(
                self.position_from_mid_pp_entry, vessel_data.get('position_from_mid_pp', ''))

            # Populate trim and density
            self._set_entry_value(self.trim_observed_entry,
                                  vessel_data.get('trim_observed', ''))
            self._set_entry_value(self.dock_density_entry,
                                  vessel_data.get('dock_density', ''))
            self._set_entry_value(self.table_density_entry,
                                  vessel_data.get('table_density', ''))

            # Populate operation type
            self.operation_type.set(vessel_data.get('operation_type', 'load'))

        except Exception as e:
            messagebox.showerror("Error", f"Error populating fields: {str(e)}")

    def _set_entry_value(self, entry_widget, value):
        """Helper to set entry value, handling None and clearing existing text."""
        if entry_widget:
            entry_widget.delete(0, tk.END)
            if value is not None:
                entry_widget.insert(0, str(value))

    def clear_all(self):
        """Clear all form fields and data"""
        try:
            # Clear all entry fields
            for entry in [self.vessel_name_entry, self.draft_number_entry, self.lbp_entry,
                          self.light_ship_entry, self.declared_constant_entry,
                          self.port_of_registry_entry, self.product_entry, self.imo_entry, self.client_entry,
                          self.loading_port_entry, self.discharging_port_entry,
                          self.quantity_bl_entry,
                          self.draft_for_port_entry, self.draft_for_star_entry,
                          self.draft_mid_port_entry, self.draft_mid_star_entry,
                          self.draft_aft_port_entry, self.draft_aft_star_entry,
                          self.distance_from_for_pp_entry, self.distance_from_aft_pp_entry,
                          self.distance_from_mid_pp_entry, self.position_from_for_pp_entry,  # noqa
                          self.ballast_entry, self.fuel_entry, self.gas_oil_entry, self.lub_oil_entry, self.slops_entry, self.others_entry, self.fresh_water_entry,
                          self.position_from_aft_pp_entry, self.position_from_mid_pp_entry,
                          self.trim_observed_entry, self.dock_density_entry, self.table_density_entry]:
                if entry:  # type: ignore
                    entry.delete(0, tk.END)

            for date_entry, time_entry in self.time_sheet_entries.values():
                if date_entry:
                    date_entry.delete(0, tk.END)
                if time_entry:
                    time_entry.delete(0, tk.END)

            # Clear calculation entries
            for entry in self.entries.values():
                entry.delete(0, tk.END)

            # Clear results
            self.results_text.delete(1.0, tk.END)

            # Clear controller data
            self.controller.clear_all_data()

            self.operation_type.set('load')

            messagebox.showinfo("Success", "All data cleared!")

        except Exception as e:
            messagebox.showerror("Error", f"Error clearing data: {str(e)}")

    # Template method implementations
    def clear_fields(self):
        """Clear all input fields"""
        self.clear_all()

    def validate_inputs(self):
        """Validate all inputs"""
        # This would be called by parent class if needed
        return True

    def calculate_values(self):
        """Main calculation method"""
        self.calculate_corrected_drafts()

    def print_data(self):
        """Print survey report"""
        self.generate_report()

    def search_data(self):
        """Search functionality"""
        search_term = tk.simpledialog.askstring("Search", "Enter search term:")
        if search_term:
            results = self.controller.search_survey_data(search_term)
            if results:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "=== SEARCH RESULTS ===\n\n")
                for result in results:
                    self.results_text.insert(tk.END, f"• {result}\n")
            else:
                messagebox.showinfo("Search", "No results found.")
