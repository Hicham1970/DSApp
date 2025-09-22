class SurveyData:
    """Class to manage survey data and operations"""

    def __init__(self):
        self.vessel_data = {}
        self.draft_data = {}
        self.calculation_data = {}
        self.bunker_data = {}

    def set_vessel_data(self, vessel_name: str = None, draft_number: str = None,
                       time_sheet: dict = None):
        """Set vessel information"""
        if vessel_name:
            self.vessel_data['vessel_name'] = vessel_name
        if draft_number:
            self.vessel_data['draft_number'] = draft_number
        if time_sheet:
            self.vessel_data['time_sheet'] = time_sheet

    def set_observed_drafts(self, draft_for_port: float = 0, draft_for_star: float = 0,
                           draft_mid_port: float = 0, draft_mid_star: float = 0,
                           draft_aft_port: float = 0, draft_aft_star: float = 0):
        """Set observed draft readings"""
        self.draft_data['observed_drafts'] = {
            'draft_for_port': draft_for_port,
            'draft_for_star': draft_for_star,
            'draft_mid_port': draft_mid_port,
            'draft_mid_star': draft_mid_star,
            'draft_aft_port': draft_aft_port,
            'draft_aft_star': draft_aft_star
        }

    def set_corrected_drafts(self, corrected_drafts: dict):
        """Set corrected draft data"""
        self.draft_data['corrected_drafts'] = corrected_drafts

    def set_mfa_mom_qm(self, mfa_mom_qm: dict):
        """Set MFA/MOM/QM data"""
        self.draft_data['mfa_mom_qm'] = mfa_mom_qm

    def set_displacement_corrections(self, displacement_corrections: dict):
        """Set displacement correction data"""
        self.calculation_data['displacement_corrections'] = displacement_corrections

    def set_bunker_data(self, ballast: float = 0, fuel: float = 0, gas_oil: float = 0,
                       lub_oil: float = 0, slops: float = 0, others: float = 0):
        """Set bunker quantities"""
        self.bunker_data = {
            'ballast': ballast,
            'fuel': fuel,
            'gas_oil': gas_oil,
            'lub_oil': lub_oil,
            'slops': slops,
            'others': others
        }

    def get_vessel_data(self) -> dict:
        """Get vessel data"""
        return self.vessel_data.copy()

    def get_draft_data(self) -> dict:
        """Get draft data"""
        return self.draft_data.copy()

    def get_calculation_data(self) -> dict:
        """Get calculation data"""
        return self.calculation_data.copy()

    def get_bunker_data(self) -> dict:
        """Get bunker data"""
        return self.bunker_data.copy()

    def clear_data(self):
        """Clear all data"""
        self.vessel_data.clear()
        self.draft_data.clear()
        self.calculation_data.clear()
        self.bunker_data.clear()

    def save_to_file(self, filename: str):
        """Save survey data to file"""
        import json
        data = {
            'vessel_data': self.vessel_data,
            'draft_data': self.draft_data,
            'calculation_data': self.calculation_data,
            'bunker_data': self.bunker_data
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
            self.draft_data = data.get('draft_data', {})
            self.calculation_data = data.get('calculation_data', {})
            self.bunker_data = data.get('bunker_data', {})
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
                results.append(f"Vessel Data - {key}: {value}")

        # Search in draft data
        for key, value in self.draft_data.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if search_term.lower() in str(sub_value).lower():
                        results.append(f"Draft Data - {key}.{sub_key}: {sub_value}")
            else:
                if search_term.lower() in str(value).lower():
                    results.append(f"Draft Data - {key}: {value}")

        # Search in calculation data
        for key, value in self.calculation_data.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if search_term.lower() in str(sub_value).lower():
                        results.append(f"Calculation Data - {key}.{sub_key}: {sub_value}")
            else:
                if search_term.lower() in str(value).lower():
                    results.append(f"Calculation Data - {key}: {value}")

        return results
