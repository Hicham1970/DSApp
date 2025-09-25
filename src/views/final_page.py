import tkinter as tk
from tkinter import messagebox, ttk

from PIL import Image, ImageTk
from src.controllers.survey_controller import SurveyController
from src.utils.validators import DraftValidator

from .base_page import BasePage


class FinalPage(BasePage):
    """Final Draft Survey Page with comprehensive functionality"""

    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        # Initialize all entry variables
        self.entries = {}

        self.controller = controller if controller else SurveyController()
        self.validator = DraftValidator()

        # Load icons
        self._load_icons()
        self.controller.set_survey_type('final')

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

        # Create the complete interface
        self.create_frame_content()

    def create_frame_content(self):
        """Create the comprehensive final draft survey interface"""
        self.create_title("Final Draft Survey")

        # Create notebook for organized tabs
        self.notebook = ttk.Notebook(self.frame_content)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Create tabs
        self.draft_tab = ttk.Frame(self.notebook)
        self.bunker_tab = ttk.Frame(self.notebook)
        self.calculation_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.draft_tab, text='Draft Readings')
        self.notebook.add(self.bunker_tab, text='Deductibles')
        self.notebook.add(self.calculation_tab, text='Calculations')
        self.notebook.add(self.results_tab, text='Results')

        # Create content for each tab
        self._create_draft_tab()
        self._create_deductibles_tab()
        self._create_calculation_tab()
        self._create_results_tab()

        # Create action buttons
        self._create_action_buttons()

    def _load_icons(self):
        """Loads all icons used on this page."""
        icon_size = (24, 24)  # Define a standard icon size

        icon_paths = {
            'clear_icon_photo': "images/clear-erase.png",
            'save_icon_photo': "images/save_data.png",
            'load_icon_photo': "images/upload.png",
            'report_icon_photo': "images/report.png"
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
            trim_frame, "Observed Trim (m):", 0, 0, width=10, state='readonly')[1]
        self.dock_density_entry = self.create_labeled_entry(
            trim_frame, "Dock Density:", 0, 2, validate='key', validatecommand=vcmd_numeric, width=10)[1]

        self.table_density_entry = self.create_labeled_entry(
            trim_frame, "Table Density:", 0, 4,
            validate='key', validatecommand=vcmd_numeric, width=10, state='readonly')[1]

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
                   # No icon for these
                   command=self.calculate_corrected_drafts).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Calculate MFA/MOM/QM",
                   # No icon for these
                   command=self.calculate_mfa_mom_qm).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Interpolate Values",
                   # No icon for these
                   command=self.calculate_interpolation).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Calculate MTC",
                   # No icon for these
                   command=self.calculate_mtc).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Calculate Trim Corrections",
                   # No icon for these
                   command=self.calculate_trim_corrections).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Calculate Density Correction",
                   # No icon for these
                   command=self.calculate_density_correction).pack(side='left', padx=5)
        ttk.Button(left_buttons, text="Calculate Final Results",
                   # No icon for these
                   command=self.calculate_final_results).pack(side='left', padx=5)

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

    def clear_all(self, show_message=True):
        """Clear all entry fields on this page."""
        entry_widgets = [
            self.draft_for_port_entry, self.draft_for_star_entry,  # type: ignore
            self.draft_mid_port_entry, self.draft_mid_star_entry,
            self.draft_aft_port_entry, self.draft_aft_star_entry,
            self.distance_from_for_pp_entry, self.distance_from_aft_pp_entry,
            self.distance_from_mid_pp_entry, self.position_from_for_pp_entry,
            self.position_from_aft_pp_entry, self.position_from_mid_pp_entry,
            self.trim_observed_entry, self.dock_density_entry, self.table_density_entry,
            self.ballast_entry, self.fuel_entry, self.gas_oil_entry,
            self.lub_oil_entry, self.slops_entry, self.others_entry, self.fresh_water_entry
        ]
        for entry in entry_widgets:
            if entry:
                # Handle readonly entries
                if entry.cget('state') == 'readonly':
                    entry.config(state='normal')
                    entry.delete(0, tk.END)
                    entry.config(state='readonly')
                else:
                    entry.delete(0, tk.END)

        # Clear calculation entries
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        if self.results_text:
            self.results_text.delete(1.0, tk.END)

        # Clear controller data for the final survey if it's handled separately
        # For now, we assume a single controller state. If final/initial are
        # separate states, this would need a different controller method.
        if show_message:
            messagebox.showinfo(
                "Cleared", "All fields on the Final Draft page have been cleared.")

    def populate_fields_from_data(self):
        """Populate form fields from loaded data"""

        try:
            # Clear all fields first to ensure no stale data
            self.clear_all(show_message=False)

            survey_data = self.controller.get_survey_summary()
            vessel_data = survey_data.get('vessel_data', {})

            # Helper to set entry value
            def _set_entry_value(entry_widget, value, readonly=False):
                if entry_widget:
                    is_readonly = entry_widget.cget('state') == 'readonly'
                    if is_readonly:
                        entry_widget.config(state='normal')

                    entry_widget.delete(0, tk.END)
                    if value is not None:
                        entry_widget.insert(0, str(value))

                    if is_readonly or readonly:
                        entry_widget.config(state='readonly')

            # Populate draft data (for final survey)
            final_draft_data = survey_data.get(
                'final', {}).get('draft_data', {})
            observed_drafts = final_draft_data.get('observed_drafts', {})
            _set_entry_value(self.draft_for_port_entry,
                             observed_drafts.get('draft_for_port', ''))
            _set_entry_value(self.draft_for_star_entry,
                             observed_drafts.get('draft_for_star', ''))
            _set_entry_value(self.draft_mid_port_entry,
                             observed_drafts.get('draft_mid_port', ''))
            _set_entry_value(self.draft_mid_star_entry,
                             observed_drafts.get('draft_mid_star', ''))
            _set_entry_value(self.draft_aft_port_entry,
                             observed_drafts.get('draft_aft_port', ''))
            _set_entry_value(self.draft_aft_star_entry,
                             observed_drafts.get('draft_aft_star', ''))

            # Populate positions and distances
            _set_entry_value(self.distance_from_for_pp_entry,
                             vessel_data.get('distance_from_for_pp', ''))
            _set_entry_value(self.distance_from_aft_pp_entry,
                             vessel_data.get('distance_from_aft_pp', ''))
            _set_entry_value(self.distance_from_mid_pp_entry,
                             vessel_data.get('distance_from_mid_pp', ''))
            _set_entry_value(self.position_from_for_pp_entry,
                             vessel_data.get('position_from_for_pp', ''))
            _set_entry_value(self.position_from_aft_pp_entry,
                             vessel_data.get('position_from_aft_pp', ''))
            _set_entry_value(self.position_from_mid_pp_entry,
                             vessel_data.get('position_from_mid_pp', ''))

            # Populate trim and density
            # Observed trim is calculated, so we check the final survey data
            final_corrected_drafts = final_draft_data.get(
                'corrected_drafts', {})
            _set_entry_value(self.trim_observed_entry, final_corrected_drafts.get(
                'trim_observed', ''), readonly=True)

            # Dock density for final survey
            _set_entry_value(self.dock_density_entry,
                             vessel_data.get('dock_density', ''))

            # Table density comes from initial survey and should be readonly
            _set_entry_value(self.table_density_entry, vessel_data.get(
                'table_density', ''), readonly=True)

        except Exception as e:
            messagebox.showerror("Error", f"Error populating fields: {str(e)}")

    # --- Placeholder methods to be implemented ---
    def calculate_corrected_drafts(self):
        """Calculate corrected drafts from observed values"""
        self.controller.set_survey_type('final')
        try:
            # Validate vessel data
            # Note: Vessel data is primarily entered on InitialPage. Here we retrieve it from controller.
            vessel_data_from_controller = self.controller.survey_data.get_vessel_data()
            vessel_data = {
                # Fallback to entry if not in controller
                'lbp': vessel_data_from_controller.get('lbp'),
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

            # Set observed drafts in the controller
            self.controller.set_observed_drafts(
                draft_for_port=float(observed_drafts['draft_for_port']),
                draft_for_star=float(observed_drafts['draft_for_star']),
                draft_mid_port=float(observed_drafts.get('draft_mid_port', 0)),
                draft_mid_star=float(observed_drafts.get('draft_mid_star', 0)),
                draft_aft_port=float(observed_drafts['draft_aft_port']),
                draft_aft_star=float(observed_drafts['draft_aft_star'])
            )

            # Calculate corrected drafts
            lbp = float(vessel_data.get('lbp', 0))  # Ensure LBP is retrieved
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
                    'position_from_mid_pp', 'N/A'),  # type: ignore
                trim_observed=observed_trim
            )

            # Display results
            self.display_corrected_drafts(corrected_drafts)

        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def calculate_mfa_mom_qm(self):
        """Calculate MFA, MOM, and QM values"""
        self.controller.set_survey_type('final')
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
        self.controller.set_survey_type('final')
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
        self.controller.set_survey_type('final')
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
        self.controller.set_survey_type('final')
        try:  # type: ignore
            draft_data = self.controller.survey_data.get_draft_data()
            corrected_drafts = draft_data.get('corrected_drafts', {})
            interp_results = draft_data.get('interpolation_results', {})
            mtc_results = draft_data.get('mtc_results', {})

            if not all([corrected_drafts, interp_results, mtc_results]):
                messagebox.showwarning(
                    "Warning", "Please perform Draft, Interpolation, and MTC calculations first.")
                return

            lbp = self.controller.survey_data.get_vessel_data().get('lbp')
            if not lbp:
                messagebox.showwarning("Warning", "Please enter LBP value.")
                return

            trim_corrections = self.controller.calculate_trim_corrections(
                draft_for_corrected=corrected_drafts['draft_for_corrected'],
                draft_aft_corrected=corrected_drafts['draft_aft_corrected'],
                tpc=interp_results['tpc'],
                lcf=interp_results['lcf'],
                lbp=float(lbp),
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
        self.controller.set_survey_type('final')
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

            table_density_str = vessel_data.get('table_density')
            dock_density_str = self.dock_density_entry.get()

            if not table_density_str or not dock_density_str:
                messagebox.showwarning(
                    "Warning", "Please ensure Table Density (in Initial) and Dock Density are entered.")
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
        self.controller.set_survey_type('final')
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

    def calculate_final_results(self):
        """
        Calculate final results based on operation type:
        - 'loading': Calculates final Load Displacement and Cargo.
        - 'discharging': Calculates final Net Displacement and Cargo.
        """
        self.controller.set_survey_type('final')
        try:
            # Get necessary data from the controller
            summary = self.controller.get_survey_summary()
            vessel_data = summary.get('vessel_data', {})
            initial_survey = summary.get('initial', {})
            final_survey = summary.get('final', {})

            op_type = vessel_data.get('operation_type')
            corrected_displacement = final_survey.get('calculation_data', {}).get(
                'density_corrections', {}).get('corrected_displacement_for_density')
            total_deductibles = final_survey.get('calculation_data', {}).get(
                'displacement_corrections', {}).get('total_deductibles')

            # Validate that all required data is present
            if not all([op_type, corrected_displacement, total_deductibles is not None]):
                messagebox.showwarning(
                    "Missing Data", "Please ensure Operation Type, Density Correction, and Deductibles are all calculated/entered for the final survey.")
                return

            # Perform calculations based on operation type
            self.results_text.insert(tk.END, "\n=== FINAL RESULTS ===\n")
            if op_type == 'load':
                initial_net_disp = initial_survey.get('calculation_data', {}).get(
                    'initial_results', {}).get('net_displacement')
                if initial_net_disp is None:
                    messagebox.showwarning(
                        "Missing Data", "Initial Net Displacement not found. Please calculate initial results first.")
                    return
                load_displacement = round(
                    corrected_displacement - total_deductibles, 3)
                cargo = round(load_displacement - initial_net_disp, 3)
                self.results_text.insert(
                    tk.END, f"Final Load Displacement: {load_displacement:.3f} mt\n")
                self.results_text.insert(
                    tk.END, f"Cargo Loaded: {cargo:.3f} mt\n")

            elif op_type == 'discharge':
                initial_load_disp = initial_survey.get('calculation_data', {}).get(
                    'initial_results', {}).get('load_displacement')
                if initial_load_disp is None:
                    messagebox.showwarning(
                        "Missing Data", "Initial Load Displacement not found. Please calculate initial results first.")
                    return
                net_displacement = round(
                    corrected_displacement - total_deductibles, 3)
                cargo = round(initial_load_disp - net_displacement, 3)
                self.results_text.insert(
                    tk.END, f"Final Net Displacement: {net_displacement:.3f} mt\n")
                self.results_text.insert(
                    tk.END, f"Cargo Discharged: {cargo:.3f} mt\n")

        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def generate_report(self):
        """Generate a report for the final survey."""
        # This assumes the controller holds the state of the *final* survey.
        # If both initial and final states need to be managed, the controller
        # and data model would need to be more complex.
        try:
            report = self.controller.generate_survey_report()
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, report)
        except Exception as e:
            messagebox.showerror("Report Error", str(e))

    def save_data(self):
        """Save final survey data to a file."""
        try:
            filename = tk.filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save Final Survey Data"
            )
            if filename:
                # Here we'd ideally save the state of the UI fields to the controller
                # before saving, or have the controller manage the state directly.
                self.controller.save_survey_data(filename)
                messagebox.showinfo(
                    "Success", "Final survey data saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def load_data(self):
        """Load final survey data from a file."""
        try:
            filename = tk.filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Load Final Survey Data"
            )
            if filename:
                self.controller.load_survey_data(filename)
                self.populate_fields_from_data()
                messagebox.showinfo(
                    "Success", "Final survey data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def display_corrected_drafts(self, corrected_drafts: dict):
        """Display corrected draft results"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "=== CORRECTED DRAFTS ===\n\n")
        self.results_text.insert(
            tk.END, f"Forward Draft: {corrected_drafts['draft_for']:.3f} m\n")
        self.results_text.insert(
            tk.END, f"Aft Draft: {corrected_drafts['draft_aft']:.3f} m\n")
        self.results_text.insert(
            tk.END, f"Mid Draft: {corrected_drafts.get('draft_mid', 0.0):.3f} m\n")
        self.results_text.insert(
            tk.END, f"Corrected Forward Draft: {corrected_drafts['draft_for_corrected']:.3f} m\n")
        self.results_text.insert(
            tk.END, f"Corrected Aft Draft: {corrected_drafts['draft_aft_corrected']:.3f} m\n")
        self.results_text.insert(
            tk.END, f"Corrected Mid Draft: {corrected_drafts.get('draft_mid_corrected', 0.0):.3f} m\n")
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
