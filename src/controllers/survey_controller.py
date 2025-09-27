
from src.models.draft_calculations import DraftCalculations
from src.models.survey_data import SurveyData
from src.utils.validators import DraftValidator


class SurveyController:
    """Controller class to manage survey operations and business logic"""

    def __init__(self):
        self.calculator = DraftCalculations()
        self.survey_data = SurveyData()
        self.validator = DraftValidator()

    def set_survey_type(self, survey_type: str):
        """Set the current survey type ('initial' or 'final')"""
        self.survey_data.current_survey = survey_type

    def set_vessel_information(self, vessel_name: str = None, draft_number: str = None, lbp: float = None,
                               light_ship: float = None, declared_constant: float = None,
                               port_of_registry: str = None, product: str = None,
                               loading_port: str = None, discharging_port: str = None, imo: str = None, client: str = None,
                               quantity_bl: float = None, table_density: float = None, operation_type: str = None, dock_density: float = None,
                               distance_from_for_pp: float = None, position_from_for_pp: str = None,
                               distance_from_mid_pp: float = None, position_from_mid_pp: str = None,
                               distance_from_aft_pp: float = None, position_from_aft_pp: str = None
                               ):
        """Set vessel information"""
        self.survey_data.set_vessel_data(vessel_name, draft_number, lbp,
                                         light_ship, declared_constant, port_of_registry, product, loading_port,
                                         discharging_port, imo, client, quantity_bl, table_density,
                                         operation_type, dock_density,
                                         distance_from_for_pp, position_from_for_pp,
                                         distance_from_mid_pp, position_from_mid_pp,
                                         distance_from_aft_pp, position_from_aft_pp)

    def set_time_sheet_information(self, time_sheet_entries: dict):
        """Set time sheet entries"""
        self.survey_data.set_time_sheet_data(time_sheet_entries)

    def set_vessel_params(self, vessel_params: dict):
        """Set vessel parameters for the current survey (initial or final)."""
        self.survey_data.set_vessel_params(vessel_params)

    def set_observed_drafts(self, draft_for_port: float = 0, draft_for_star: float = 0,
                            draft_mid_port: float = 0, draft_mid_star: float = 0,
                            draft_aft_port: float = 0, draft_aft_star: float = 0):
        """Set observed draft readings"""
        self.survey_data.set_observed_drafts(
            draft_for_port, draft_for_star, draft_mid_port, draft_mid_star,
            draft_aft_port, draft_aft_star
        )

    def calculate_corrected_drafts(self, lbp: float, distance_from_for_pp: float,
                                   distance_from_aft_pp: float, distance_from_mid_pp: float,
                                   position_from_for_pp: str, position_from_aft_pp: str,
                                   position_from_mid_pp: str, trim_observed: float) -> dict:
        """
        Calculate corrected drafts using observed values
        """
        observed_drafts = self.survey_data.get_current_survey_data().get(
            'draft_data', {}).get('observed_drafts', {})

        corrected_drafts = self.calculator.calculate_corrected_drafts(
            lbp=lbp,
            draft_for_port=observed_drafts.get('draft_for_port', 0),
            draft_for_star=observed_drafts.get('draft_for_star', 0),
            draft_aft_port=observed_drafts.get('draft_aft_port', 0),
            draft_aft_star=observed_drafts.get('draft_aft_star', 0),
            draft_mid_port=observed_drafts.get('draft_mid_port', 0),
            draft_mid_star=observed_drafts.get('draft_mid_star', 0),
            distance_from_for_pp=distance_from_for_pp,
            distance_from_aft_pp=distance_from_aft_pp,
            distance_from_mid_pp=distance_from_mid_pp,
            position_from_for_pp=position_from_for_pp,
            position_from_aft_pp=position_from_aft_pp,
            position_from_mid_pp=position_from_mid_pp,
            trim_observed=trim_observed
        )

        self.survey_data.set_corrected_drafts(corrected_drafts)
        return corrected_drafts

    def calculate_mfa_mom_qm(self, draft_for_corrected: float, draft_aft_corrected: float,
                             draft_mid_corrected: float) -> dict:
        """
        Calculate MFA, MOM, and QM values
        """
        mfa_mom_qm = self.calculator.calculate_mfa_mom_qm(
            draft_for_corrected, draft_aft_corrected, draft_mid_corrected
        )

        self.survey_data.set_mfa_mom_qm(mfa_mom_qm)
        return mfa_mom_qm

    def calculate_interpolation(self, qm: float, draft_sup: float, draft_inf: float,
                                displacement_sup: float, displacement_inf: float,
                                tpc_sup: float, tpc_inf: float,
                                lcf_sup: float, lcf_inf: float) -> dict:
        """
        Calculate and store interpolated values for displacement, TPC, and LCF
        """
        interp_results = self.calculator.calculate_interpolation_values(
            qm, draft_sup, draft_inf, displacement_sup, displacement_inf,
            tpc_sup, tpc_inf, lcf_sup, lcf_inf
        )
        self.survey_data.set_interpolation_results(interp_results)
        return interp_results

    def calculate_mtc_values(self, d_plus50_sup: float, d_plus50_inf: float, d_plus50: float,
                             mtc_plus50_sup: float, mtc_plus50_inf: float,
                             d_moins50_sup: float, d_moins50_inf: float, d_moins50: float,
                             mtc_moins50_sup: float, mtc_moins50_inf: float) -> dict:
        """
        Calculate and store MTC values using interpolation
        """
        mtc_results = self.calculator.calculate_mtc_values(
            d_plus50_sup, d_plus50_inf, d_plus50,
            mtc_plus50_sup, mtc_plus50_inf,
            d_moins50_sup, d_moins50_inf, d_moins50,
            mtc_moins50_sup, mtc_moins50_inf
        )
        self.survey_data.set_mtc_results(mtc_results)
        return mtc_results

    def calculate_trim_corrections(self, draft_for_corrected: float, draft_aft_corrected: float,
                                   tpc: float, lcf: float, lbp: float, delta_mtc: float,
                                   displacement: float) -> dict:
        """
        Calculate trim corrections
        """
        trim_corrections = self.calculator.calculate_trim_corrections(
            draft_for_corrected, draft_aft_corrected, tpc, lcf, lbp, delta_mtc, displacement
        )

        self.survey_data.set_trim_corrections(trim_corrections)
        return trim_corrections

    def calculate_density_corrections(self, table_density: float, dock_density: float,
                                      corrected_displacement_for_trim: float) -> dict:
        """
        Calculate density corrections
        """
        density_corrections = self.calculator.calculate_density_corrections(
            table_density, dock_density, corrected_displacement_for_trim
        )
        self.survey_data.set_density_corrections(density_corrections)
        return density_corrections

    def set_bunker_data(self, ballast: float = 0, fuel: float = 0, gas_oil: float = 0,
                        lub_oil: float = 0, slops: float = 0, others: float = 0, fresh_water: float = 0):
        """Set bunker quantities"""
        self.survey_data.set_bunker_data(
            ballast, fuel, gas_oil, lub_oil, slops, others, fresh_water)

    def calculate_total_deductibles(self, bunker_data_str: dict) -> float:
        """Calculate total deductibles from bunker data"""
        # Convert string data from UI to floats
        bunker_data_float = {key: float(
            value) if value else 0.0 for key, value in bunker_data_str.items()}

        # Set the data in the model
        self.set_bunker_data(**bunker_data_float)

        # Calculate the total
        total = self.calculator.calculate_total_deductibles(
            **bunker_data_float)

        # Store the result in the model
        displacement_corrections = self.survey_data.get_calculation_data().get(
            'displacement_corrections', {})
        displacement_corrections['total_deductibles'] = total
        self.survey_data.set_displacement_corrections(
            displacement_corrections)

        return total

    def set_initial_results(self, initial_results: dict):
        """Set initial calculation results like constant or cargo+constant."""
        self.survey_data.set_initial_results(initial_results)

    def calculate_load_displacement(self, corrected_displacement: float,
                                    operation_type: str, net_init_displacement: float = 0) -> dict:
        """
        Calculate load displacement and cargo
        """
        total_deductibles = self.calculate_total_deductibles()

        load_data = self.calculator.calculate_load_displacement(
            corrected_displacement, total_deductibles, net_init_displacement, operation_type
        )

        # Update calculation data
        displacement_corrections = {
            'total_deductibles': total_deductibles,
            'load_displacement': load_data['load_displacement'],
            'cargo': load_data['cargo']
        }

        self.survey_data.set_displacement_corrections(displacement_corrections)
        return load_data

    def generate_survey_report(self) -> str:
        """
        Generate complete survey report
        """
        return self.calculator.format_two_column_report(  # type: ignore
            self.survey_data.get_vessel_data(),
            self.survey_data.initial,
            self.survey_data.final
        )

    def save_survey_data(self, filename: str):
        """Save survey data to file"""
        self.survey_data.save_to_file(filename)

    def load_survey_data(self, filename: str):
        """Load survey data from file"""
        self.survey_data.load_from_file(filename)

    def search_survey_data(self, search_term: str) -> list:
        """Search for data in survey"""
        return self.survey_data.search_data(search_term)

    def clear_all_data(self):
        """Clear all survey data"""
        self.survey_data.clear_data()

    def validate_observed_drafts(self, data: dict) -> tuple[bool, str]:
        """Validate observed draft data"""
        return self.validator.validate_observed_drafts(data)

    def validate_vessel_data(self, data: dict) -> tuple[bool, str]:
        """Validate vessel data"""
        return self.validator.validate_vessel_data(data)

    def validate_bunker_data(self, data: dict) -> tuple[bool, str]:
        """Validate bunker data"""
        return self.validator.validate_bunker_data(data)

    def validate_interpolation_data(self, data: dict) -> tuple[bool, str]:
        """Validate interpolation data"""
        return self.validator.validate_interpolation_data(data)

    def validate_mtc_data(self, data: dict) -> tuple[bool, str]:
        """Validate MTC data"""
        return self.validator.validate_mtc_data(data)

    def get_survey_summary(self) -> dict:
        """Get summary of current survey data"""
        return {
            'vessel_data': self.survey_data.get_vessel_data(),
            'initial': self.survey_data.initial,
            'final': self.survey_data.final,
        }
