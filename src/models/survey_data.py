class SurveyData:
    """Class to manage survey data and operations"""

    def __init__(self):
        self.vessel_data = {}  # Shared vessel data
        self.initial = {
            'draft_data': {}, 'calculation_data': {}, 'bunker_data': {}
        }
        self.final = {
            'draft_data': {}, 'calculation_data': {}, 'bunker_data': {}
        }
        self.current_survey = 'initial'  # To track the active survey

    def set_vessel_data(self, vessel_name: str = None, draft_number: str = None, lbp: float = None,
                        light_ship: float = None, declared_constant: float = None,
                        port_of_registry: str = None, product: str = None,
                        loading_port: str = None, discharging_port: str = None, imo: str = None, client: str = None,
                        quantity_bl: float = None, table_density: float = None, operation_type: str = None,
                        dock_density: float = None):
        """Set vessel information"""
        if vessel_name:
            self.vessel_data['vessel_name'] = vessel_name
        if draft_number:
            self.vessel_data['draft_number'] = draft_number
        if lbp is not None:
            self.vessel_data['lbp'] = lbp
        if light_ship is not None:
            self.vessel_data['light_ship'] = light_ship
        if declared_constant is not None:
            self.vessel_data['declared_constant'] = declared_constant
        if port_of_registry:
            self.vessel_data['port_of_registry'] = port_of_registry
        if product:
            self.vessel_data['product'] = product
        if loading_port:
            self.vessel_data['loading_port'] = loading_port
        if imo:
            self.vessel_data['imo'] = imo
        if client:
            self.vessel_data['client'] = client
        if discharging_port:
            self.vessel_data['discharging_port'] = discharging_port
        if quantity_bl is not None:
            self.vessel_data['quantity_bl'] = quantity_bl
        if table_density is not None:
            self.vessel_data['table_density'] = table_density
        if dock_density is not None:
            self.vessel_data['dock_density'] = dock_density
        if operation_type:
            self.vessel_data['operation_type'] = operation_type

    def set_time_sheet_data(self, time_sheet_entries: dict):
        """Set time sheet entries"""
        if 'time_sheet' not in self.vessel_data:
            self.vessel_data['time_sheet'] = {}
        self.vessel_data['time_sheet'].update(time_sheet_entries)

    def set_observed_drafts(self, draft_for_port: float = 0, draft_for_star: float = 0,
                            draft_mid_port: float = 0, draft_mid_star: float = 0,
                            draft_aft_port: float = 0, draft_aft_star: float = 0):
        """Set observed draft readings"""
        self.get_current_survey_data()['draft_data']['observed_drafts'] = {
            'draft_for_port': draft_for_port,
            'draft_for_star': draft_for_star,
            'draft_mid_port': draft_mid_port,
            'draft_mid_star': draft_mid_star,
            'draft_aft_port': draft_aft_port,
            'draft_aft_star': draft_aft_star
        }

    def set_corrected_drafts(self, corrected_drafts: dict):
        """Set corrected draft data"""
        self.get_current_survey_data(
        )['draft_data']['corrected_drafts'] = corrected_drafts

    def set_mfa_mom_qm(self, mfa_mom_qm: dict):
        """Set MFA/MOM/QM data"""
        self.get_current_survey_data()['draft_data']['mfa_mom_qm'] = mfa_mom_qm

    def set_interpolation_results(self, interp_results: dict):
        """Set interpolation results data"""
        self.get_current_survey_data(
        )['draft_data']['interpolation_results'] = interp_results

    def set_mtc_results(self, mtc_results: dict):
        """Set MTC results data"""
        self.get_current_survey_data(
        )['draft_data']['mtc_results'] = mtc_results

    def set_trim_corrections(self, trim_corrections: dict):
        """Set trim corrections data"""
        self.get_current_survey_data(
        )['calculation_data']['trim_corrections'] = trim_corrections

    def set_density_corrections(self, density_corrections: dict):
        """Set density corrections data"""
        self.get_current_survey_data(
        )['calculation_data']['density_corrections'] = density_corrections

    def set_initial_results(self, initial_results: dict):
        """Set initial results data (e.g., constant)"""
        self.get_current_survey_data(
        )['calculation_data']['initial_results'] = initial_results

    def set_displacement_corrections(self, displacement_corrections: dict):
        """Set displacement correction data"""
        self.get_current_survey_data(
        )['calculation_data']['displacement_corrections'] = displacement_corrections

    def set_bunker_data(self, ballast: float = 0, fuel: float = 0, gas_oil: float = 0,
                        lub_oil: float = 0, slops: float = 0, others: float = 0, fresh_water: float = 0):
        """Set bunker quantities"""
        self.get_current_survey_data()['bunker_data'] = {
            'ballast': ballast,
            'fuel': fuel,
            'gas_oil': gas_oil,
            'lub_oil': lub_oil,
            'slops': slops,
            'others': others,
            'fresh_water': fresh_water
        }

    def get_current_survey_data(self):
        """Get the data dictionary for the current survey type"""
        return self.initial if self.current_survey == 'initial' else self.final

    def get_vessel_data(self) -> dict:
        """Get vessel data"""
        return self.vessel_data.copy()

    def get_draft_data(self) -> dict:
        """Get draft data"""
        return self.get_current_survey_data()['draft_data'].copy()

    def get_calculation_data(self) -> dict:
        """Get calculation data"""
        return self.get_current_survey_data()['calculation_data'].copy()

    def get_bunker_data(self) -> dict:
        """Get bunker data"""
        return self.get_current_survey_data()['bunker_data'].copy()

    def clear_data(self):
        """Clear all data"""
        self.vessel_data.clear()
        # Ensure time_sheet is re-initialized
        self.vessel_data['time_sheet'] = {}
        self.initial = {
            'draft_data': {}, 'calculation_data': {}, 'bunker_data': {}
        }
        self.final = {
            'draft_data': {}, 'calculation_data': {}, 'bunker_data': {}
        }

    def save_to_file(self, filename: str):
        """Save survey data to file"""
        import json
        data = {
            'vessel_data': self.vessel_data,
            'initial': self.initial,
            'final': self.final
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename: str):
        """Load survey data from file"""
        import json
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            self.vessel_data = data.get('vessel_data', {})
            self.initial = data.get(
                'initial', {'draft_data': {}, 'calculation_data': {}, 'bunker_data': {}})
            self.final = data.get(
                'final', {'draft_data': {}, 'calculation_data': {}, 'bunker_data': {}})
        except FileNotFoundError:
            print(f"File {filename} not found")
        except json.JSONDecodeError:
            print(f"Error reading JSON from {filename}")

    def search_data(self, search_term: str) -> list:
        """Search for data containing the search term"""
        results = []

        # Search in vessel data
        for key, value in self.vessel_data.items():
            if search_term.lower() in str(value).lower():
                results.append(f"Vessel Data - {key}: {value}")  # type: ignore

        # Search in time sheet data
        for key, value in self.vessel_data.get('time_sheet', {}).items():
            if search_term.lower() in str(value).lower():
                results.append(f"Time Sheet - {key}: {value}")  # type: ignore

        # Search in draft data
        # Search in initial survey data
        for key, value in self.initial.get('draft_data', {}).items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if search_term.lower() in str(sub_value).lower():
                        results.append(
                            # type: ignore
                            f"Initial Draft Data - {key}.{sub_key}: {sub_value}")
            else:
                if search_term.lower() in str(value).lower():
                    # type: ignore
                    results.append(f"Initial Draft Data - {key}: {value}")

        # Search in final survey data
        for key, value in self.final.get('draft_data', {}).items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if search_term.lower() in str(sub_value).lower():
                        results.append(
                            # type: ignore
                            f"Final Draft Data - {key}.{sub_key}: {sub_value}")
            else:
                if search_term.lower() in str(value).lower():
                    # type: ignore
                    results.append(f"Final Draft Data - {key}: {value}")

        return results
