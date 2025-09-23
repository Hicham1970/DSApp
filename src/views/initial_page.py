import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.controllers.survey_controller import SurveyController
from src.utils.validators import DraftValidator

from .base_page import BasePage


class InitialPage(BasePage):
    """Initial Draft Survey Page with comprehensive functionality"""

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
        """Create the comprehensive initial draft survey interface"""
        self.create_title("Initial Draft Survey")

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

        # Validation commands
        vcmd_numeric = (self.register(
            DraftValidator.validate_numeric_entry_callback), '%P')
        vcmd_positive = (self.register(
            DraftValidator.validate_positive_numeric_entry_callback), '%P')

        # Vessel name
        self.vessel_name_entry = self.create_labeled_entry(
            frame, "Vessel Name:", 0, 0, width=30
        )[1]

        # Draft number
        self.draft_number_entry = self.create_labeled_entry(
            frame, "Draft Number:", 1, 0, width=30
        )[1]

        # LBP (Length Between Perpendiculars)
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
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

        self.dock_density_entry = self.create_labeled_entry(
            trim_frame, "Dock Density:", 0, 2,
            validate='key', validatecommand=vcmd_numeric, width=10
        )[1]

    def _create_bunker_tab(self):
        """Create bunker and ballast data tab"""
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

        # Results text area
        results_label = tk.Label(
            frame, text="Survey Results:", background='gray12', foreground='gold')
        results_label.pack(anchor='w', pady=5)

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

    def calculate_corrected_drafts(self):
        """Calculate corrected drafts from observed values"""
        try:
            # Validate vessel data
            vessel_data = {
                'lbp': self.lbp_entry.get(),
                'distance_from_for_pp': self.distance_from_for_pp_entry.get(),
                'distance_from_aft_pp': self.distance_from_aft_pp_entry.get(),
                'distance_from_mid_pp': self.distance_from_mid_pp_entry.get(),
                'position_from_for_pp': self.position_from_for_pp_entry.get(),
                'position_from_aft_pp': self.position_from_aft_pp_entry.get(),
                'position_from_mid_pp': self.position_from_mid_pp_entry.get()
            }

            is_valid, error_msg = self.controller.validate_vessel_data(
                vessel_data)
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

            # Set vessel information
            self.controller.set_vessel_information(
                vessel_name=self.vessel_name_entry.get(),
                draft_number=self.draft_number_entry.get()
            )

            # Set observed drafts
            self.controller.set_observed_drafts(
                draft_for_port=float(observed_drafts['draft_for_port']),
                draft_for_star=float(observed_drafts['draft_for_star']),
                draft_mid_port=float(observed_drafts.get('draft_mid_port', 0)),
                draft_mid_star=float(observed_drafts.get('draft_mid_star', 0)),
                draft_aft_port=float(observed_drafts['draft_aft_port']),
                draft_aft_star=float(observed_drafts['draft_aft_star'])
            )

            # Calculate corrected drafts
            lbp = float(vessel_data['lbp'])
            corrected_drafts = self.controller.calculate_corrected_drafts(
                lbp=lbp,
                distance_from_for_pp=float(
                    vessel_data['distance_from_for_pp']),
                distance_from_aft_pp=float(
                    vessel_data['distance_from_aft_pp']),
                distance_from_mid_pp=float(
                    vessel_data.get('distance_from_mid_pp', 0)),
                position_from_for_pp=vessel_data['position_from_for_pp'],
                position_from_aft_pp=vessel_data['position_from_aft_pp'],
                position_from_mid_pp=vessel_data.get(
                    'position_from_mid_pp', 'N/A'),
                trim_observed=float(self.trim_observed_entry.get())
            )

            # Display results
            self.display_corrected_drafts(corrected_drafts)

        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def calculate_mfa_mom_qm(self):
        """Calculate MFA, MOM, and QM values"""
        try:
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
        try:
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
            draft_data = self.controller.survey_data.get_draft_data()
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

    def display_corrected_drafts(self, corrected_drafts: dict):
        """Display corrected draft results"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "=== CORRECTED DRAFTS ===\n\n")
        self.results_text.insert(
            tk.END, f"Forward Draft: {corrected_drafts['draft_for']:.2f} m\n")
        self.results_text.insert(
            tk.END, f"Aft Draft: {corrected_drafts['draft_aft']:.2f} m\n")
        self.results_text.insert(
            tk.END, f"Mid Draft: {corrected_drafts['draft_mid']:.2f} m\n")
        self.results_text.insert(
            tk.END, f"Corrected Forward Draft: {corrected_drafts['draft_for_corrected']:.2f} m\n")
        self.results_text.insert(
            tk.END, f"Corrected Aft Draft: {corrected_drafts['draft_aft_corrected']:.2f} m\n")
        self.results_text.insert(
            tk.END, f"Corrected Mid Draft: {corrected_drafts['draft_mid_corrected']:.2f} m\n")
        self.results_text.insert(
            tk.END, f"Observed Trim: {corrected_drafts['trim_observed']:.2f} m\n")
        self.results_text.insert(
            tk.END, f"LBM: {corrected_drafts['lbm']:.2f} m\n")

    def display_mfa_mom_qm(self, mfa_mom_qm: dict):
        """Display MFA/MOM/QM results"""
        self.results_text.insert(tk.END, "\n=== MFA/MOM/QM ===\n")
        self.results_text.insert(tk.END, f"MFA: {mfa_mom_qm['mfa']:.2f} m\n")
        self.results_text.insert(tk.END, f"MOM: {mfa_mom_qm['mom']:.2f} m\n")
        self.results_text.insert(tk.END, f"QM: {mfa_mom_qm['qm']:.2f} m\n")

    def display_interpolation_results(self, interp_results: dict):
        """Display interpolation results"""
        self.results_text.insert(tk.END, "\n=== INTERPOLATION RESULTS ===\n")
        self.results_text.insert(
            tk.END, f"Displacement: {interp_results['displacement']:.3f} mt\n")
        self.results_text.insert(tk.END, f"TPC: {interp_results['tpc']:.3f}\n")
        self.results_text.insert(
            tk.END, f"LCF: {interp_results['lcf']:.3f} m\n")

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
            vessel_data = survey_data.get('vessel_data', {})
            if 'vessel_name' in vessel_data:
                self.vessel_name_entry.delete(0, tk.END)
                self.vessel_name_entry.insert(0, vessel_data['vessel_name'])

            if 'draft_number' in vessel_data:
                self.draft_number_entry.delete(0, tk.END)
                self.draft_number_entry.insert(0, vessel_data['draft_number'])

            # Populate draft data
            draft_data = survey_data.get('draft_data', {})
            observed_drafts = draft_data.get('observed_drafts', {})

            if observed_drafts:
                self.draft_for_port_entry.delete(0, tk.END)
                self.draft_for_port_entry.insert(
                    0, str(observed_drafts.get('draft_for_port', '')))

                self.draft_for_star_entry.delete(0, tk.END)
                self.draft_for_star_entry.insert(
                    0, str(observed_drafts.get('draft_for_star', '')))

                self.draft_aft_port_entry.delete(0, tk.END)
                self.draft_aft_port_entry.insert(
                    0, str(observed_drafts.get('draft_aft_port', '')))

                self.draft_aft_star_entry.delete(0, tk.END)
                self.draft_aft_star_entry.insert(
                    0, str(observed_drafts.get('draft_aft_star', '')))

        except Exception as e:
            messagebox.showerror("Error", f"Error populating fields: {str(e)}")

    def clear_all(self):
        """Clear all form fields and data"""
        try:
            # Clear all entry fields
            for entry in [self.vessel_name_entry, self.draft_number_entry, self.lbp_entry,
                          self.draft_for_port_entry, self.draft_for_star_entry,
                          self.draft_mid_port_entry, self.draft_mid_star_entry,
                          self.draft_aft_port_entry, self.draft_aft_star_entry,
                          self.distance_from_for_pp_entry, self.distance_from_aft_pp_entry,
                          self.distance_from_mid_pp_entry, self.position_from_for_pp_entry, # noqa
                          self.ballast_entry, self.fuel_entry, self.gas_oil_entry, self.lub_oil_entry, self.slops_entry, self.others_entry,
                          self.position_from_aft_pp_entry, self.position_from_mid_pp_entry,
                          self.trim_observed_entry, self.dock_density_entry]:
                if entry:
                    entry.delete(0, tk.END)

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
