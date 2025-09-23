import tkinter as tk
from tkinter import messagebox, ttk

from src.controllers.survey_controller import SurveyController
from src.utils.validators import DraftValidator

from .base_page import BasePage


class FinalPage(BasePage):
    """Final Draft Survey Page with comprehensive functionality"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Initialize all entry variables
        self.entries = {}

        self.controller = SurveyController()
        self.validator = DraftValidator()

        # Vessel information entries
        self.vessel_name_entry = None
        self.draft_number_entry = None
        self.lbp_entry = None

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

        # Bunker data entries
        self.ballast_entry = None
        self.fuel_entry = None
        self.gas_oil_entry = None
        self.lub_oil_entry = None
        self.slops_entry = None
        self.others_entry = None

        # Operation type
        self.operation_type = tk.StringVar(value='load')

        # Results display
        self.results_text = None

        # Create the complete interface
        self.create_frame_content()

    def create_frame_content(self):
        """Create the comprehensive final draft survey interface"""
        self.create_title("Final Draft Survey")

        # Create notebook for organized tabs
        self.notebook = ttk.Notebook(self.frame_content)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Create tabs
        self.vessel_tab = ttk.Frame(self.notebook)
        self.draft_tab = ttk.Frame(self.notebook)
        self.bunker_tab = ttk.Frame(self.notebook)
        self.calculation_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.vessel_tab, text='Vessel Info')
        self.notebook.add(self.draft_tab, text='Draft Readings')
        self.notebook.add(self.bunker_tab, text='Bunker & Ballast')
        self.notebook.add(self.calculation_tab, text='Calculations')
        self.notebook.add(self.results_tab, text='Results')

        # Create content for each tab
        self._create_vessel_tab()
        self._create_draft_tab()
        self._create_bunker_tab()
        self._create_calculation_tab()
        self._create_results_tab()

        # Create action buttons
        self._create_action_buttons()

    def _create_vessel_tab(self):
        """Create vessel information tab"""
        frame = ttk.Frame(self.vessel_tab)
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        vcmd_positive = (self.register(
            DraftValidator.validate_positive_numeric_entry_callback), '%P')

        self.vessel_name_entry = self.create_labeled_entry(
            frame, "Vessel Name:", 0, 0, width=30
        )[1]
        self.draft_number_entry = self.create_labeled_entry(
            frame, "Draft Number:", 1, 0, width=30
        )[1]
        self.lbp_entry = self.create_labeled_entry(
            frame, "LBP (m):", 2, 0,
            validate='key', validatecommand=vcmd_positive, width=15
        )[1]

    def _create_draft_tab(self):
        """Create draft readings tab"""
        frame = ttk.Frame(self.draft_tab)
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        vcmd_numeric = (self.register(
            DraftValidator.validate_numeric_entry_callback), '%P')

        observed_frame = ttk.LabelFrame(frame, text="Observed Drafts (meters)")
        observed_frame.pack(fill='x', pady=5)

        self.draft_for_port_entry = self.create_labeled_entry(
            observed_frame, "Forward Port:", 0, 0, validate='key', validatecommand=vcmd_numeric, width=10)[1]
        self.draft_for_star_entry = self.create_labeled_entry(
            observed_frame, "Forward Starboard:", 0, 2, validate='key', validatecommand=vcmd_numeric, width=10)[1]
        self.draft_mid_port_entry = self.create_labeled_entry(
            observed_frame, "Midship Port:", 1, 0, validate='key', validatecommand=vcmd_numeric, width=10)[1]
        self.draft_mid_star_entry = self.create_labeled_entry(
            observed_frame, "Midship Starboard:", 1, 2, validate='key', validatecommand=vcmd_numeric, width=10)[1]
        self.draft_aft_port_entry = self.create_labeled_entry(
            observed_frame, "Aft Port:", 2, 0, validate='key', validatecommand=vcmd_numeric, width=10)[1]
        self.draft_aft_star_entry = self.create_labeled_entry(
            observed_frame, "Aft Starboard:", 2, 2, validate='key', validatecommand=vcmd_numeric, width=10)[1]

        positions_frame = ttk.LabelFrame(frame, text="Positions and Distances")
        positions_frame.pack(fill='x', pady=5)

        self.distance_from_for_pp_entry = self.create_labeled_entry(
            positions_frame, "Dist. from Fwd PP (m):", 0, 0, validate='key', validatecommand=vcmd_numeric, width=10)[1]
        self.distance_from_aft_pp_entry = self.create_labeled_entry(
            positions_frame, "Dist. from Aft PP (m):", 0, 2, validate='key', validatecommand=vcmd_numeric, width=10)[1]
        self.distance_from_mid_pp_entry = self.create_labeled_entry(
            positions_frame, "Dist. from Mid PP (m):", 0, 4, validate='key', validatecommand=vcmd_numeric, width=10)[1]

        self.position_from_for_pp_entry = self.create_labeled_entry(
            positions_frame, "Forward Position:", 1, 0, width=10)[1]
        self.position_from_aft_pp_entry = self.create_labeled_entry(
            positions_frame, "Aft Position:", 1, 2, width=10)[1]
        self.position_from_mid_pp_entry = self.create_labeled_entry(
            positions_frame, "Mid Position:", 1, 4, width=10)[1]

        trim_frame = ttk.LabelFrame(frame, text="Trim and Density")
        trim_frame.pack(fill='x', pady=5)

        self.trim_observed_entry = self.create_labeled_entry(
            trim_frame, "Observed Trim (m):", 0, 0, validate='key', validatecommand=vcmd_numeric, width=10)[1]
        self.dock_density_entry = self.create_labeled_entry(
            trim_frame, "Dock Density:", 0, 2, validate='key', validatecommand=vcmd_numeric, width=10)[1]

    def _create_bunker_tab(self):
        """Create bunker data tab"""
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

        op_frame = ttk.LabelFrame(frame, text="Operation Type")
        op_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky='w')
        ttk.Radiobutton(op_frame, text="Loading", variable=self.operation_type,
                        value='load').pack(side='left', padx=5)
        ttk.Radiobutton(op_frame, text="Discharging", variable=self.operation_type,
                        value='discharge').pack(side='left', padx=5)

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

        self.results_text = tk.Text(
            frame, height=20, width=80, bg='black', fg='light green')
        self.results_text.pack(fill='both', expand=True)

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

        ttk.Button(left_buttons, text="Calculate Drafts",
                   command=self.calculate_corrected_drafts).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Calculate MFA/MOM/QM",
                   command=self.calculate_mfa_mom_qm).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Interpolate Values",
                   command=self.calculate_interpolation).pack(side='left', padx=5)

        # Right side buttons
        right_buttons = ttk.Frame(button_frame)
        right_buttons.grid(row=0, column=1, sticky='e')

        ttk.Button(right_buttons, text="Generate Report",
                   command=self.generate_report).pack(side='right', padx=5)
        ttk.Button(right_buttons, text="Save Data",
                   command=self.save_data).pack(side='right', padx=5)
        ttk.Button(right_buttons, text="Load Data",
                   command=self.load_data).pack(side='right', padx=5)
        ttk.Button(right_buttons, text="Clear All",
                   command=self.clear_all).pack(side='right', padx=5)

    def clear_all(self):
        """Clear all entry fields on this page."""
        entry_widgets = [
            self.vessel_name_entry, self.draft_number_entry, self.lbp_entry,
            self.draft_for_port_entry, self.draft_for_star_entry,
            self.draft_mid_port_entry, self.draft_mid_star_entry,
            self.draft_aft_port_entry, self.draft_aft_star_entry,
            self.distance_from_for_pp_entry, self.distance_from_aft_pp_entry,
            self.distance_from_mid_pp_entry, self.position_from_for_pp_entry,
            self.position_from_aft_pp_entry, self.position_from_mid_pp_entry,
            self.trim_observed_entry, self.dock_density_entry,
            self.ballast_entry, self.fuel_entry, self.gas_oil_entry,
            self.lub_oil_entry, self.slops_entry, self.others_entry
        ]
        for entry in entry_widgets:
            if entry:
                entry.delete(0, tk.END)

        # Clear calculation entries
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        if self.results_text:
            self.results_text.delete(1.0, tk.END)

        self.operation_type.set('load')
        messagebox.showinfo(
            "Cleared", "All fields on the Final Draft page have been cleared.")

    def populate_fields_from_data(self):
        """Populate form fields from loaded data"""
        try:
            survey_data = self.controller.get_survey_summary()
            vessel_data = survey_data.get('vessel_data', {})
            if 'vessel_name' in vessel_data:
                self.vessel_name_entry.delete(0, tk.END)
                self.vessel_name_entry.insert(0, vessel_data['vessel_name'])
            if 'draft_number' in vessel_data:
                self.draft_number_entry.delete(0, tk.END)
                self.draft_number_entry.insert(0, vessel_data['draft_number'])
        except Exception as e:
            messagebox.showerror("Error", f"Error populating fields: {str(e)}")

    # --- Placeholder methods to be implemented ---
    def calculate_corrected_drafts(self):
        messagebox.showinfo(
            "Info", "Calculate corrected drafts to be implemented.")

    def calculate_mfa_mom_qm(self):
        messagebox.showinfo("Info", "Calculate MFA/MOM/QM to be implemented.")

    def calculate_interpolation(self):
        messagebox.showinfo(
            "Info", "Calculate interpolation to be implemented.")

    def generate_report(self):
        messagebox.showinfo("Info", "Generate report to be implemented.")

    def save_data(self):
        messagebox.showinfo("Info", "Save data to be implemented.")

    def load_data(self):
        messagebox.showinfo("Info", "Load data to be implemented.")
