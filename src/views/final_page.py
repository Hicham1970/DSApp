import tkinter as tk
from tkinter import messagebox, ttk, filedialog

from src.controllers.survey_controller import SurveyController
from src.utils.validators import DraftValidator
from .base_page import BasePage


class FinalPage(BasePage):
    """Final Draft Survey Page with comprehensive functionality"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = SurveyController()
        self.validator = DraftValidator()

        # Initialize all entry variables
        self.entries = {}

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
        self.notebook.add(self.bunker_tab, text='Bunker Data')
        self.notebook.add(self.calculation_tab, text='Calculations')
        self.notebook.add(self.results_tab, text='Results')

        # Create content for each tab
        self._create_vessel_tab()
        self._create_draft_tab()
        self._create_bunker_tab()
        self._create_calculation_tab()
        self._create_results_tab()
