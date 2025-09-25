import re
from typing import Any, Dict


class DraftValidator:
    """Validator class for Draft Survey inputs"""

    @staticmethod
    def is_valid_number(value: str) -> bool:
        """
        Validate if string is a valid number (integer or float)
        """
        if not value:
            return False
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_draft_range(value: float, min_val: float = 0, max_val: float = 20) -> bool:
        """
        Validate if draft value is within acceptable range
        """
        return min_val <= value <= max_val

    @staticmethod
    def is_valid_density(value: float) -> bool:
        """
        Validate if density is within realistic range (0.95 to 1.1)
        """
        return 0.95 <= value <= 1.1

    @staticmethod
    def is_valid_lbp(value: float) -> bool:
        """
        Validate if LBP (Length Between Perpendiculars) is within realistic range
        """
        return 50 <= value <= 400  # meters

    @staticmethod
    def is_valid_distance(value: float) -> bool:
        """
        Validate if distance value is within realistic range
        """
        return 0 <= value <= 200  # meters

    @staticmethod
    def is_valid_bunker_quantity(value: float) -> bool:
        """
        Validate if bunker quantity is within realistic range
        """
        return 0 <= value <= 10000  # metric tons

    @staticmethod
    def is_valid_ballast_quantity(value: float) -> bool:
        """
        Validate if ballast quantity is within realistic range
        """
        return 0 <= value <= 12000  # metric tons

    @staticmethod
    def is_valid_light_ship(value: float) -> bool:
        """
        Validate if light ship value is within realistic range
        """
        return 1000 <= value <= 200000  # metric tons

    @staticmethod
    def is_valid_declared_constant(value: float) -> bool:
        """
        Validate if declared constant value is within realistic range
        """
        return -500 <= value <= 500  # metric tons

    @staticmethod
    def is_valid_quantity_bl(value: float) -> bool:
        """Validate if quantity-BL is within realistic range"""
        return 0 <= value <= 200000  # metric tons

    @staticmethod
    def is_valid_position(value: str) -> bool:
        """
        Validate if position is valid (A, F, N/A)
        """
        return value in ['A', 'F', 'N/A']

    @staticmethod
    def is_valid_operation_type(value: str) -> bool:
        """
        Validate if operation type is valid
        """
        return value in ['load', 'discharge']

    @staticmethod
    def validate_draft_inputs(data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate all draft survey inputs
        Returns: (is_valid: bool, error_message: str)
        """
        required_fields = ['draft_aft', 'draft_forward', 'density']

        # Check required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"

            if not DraftValidator.is_valid_number(str(data[field])):
                return False, f"Invalid number format in {field}"

        # Convert to float for range validation
        try:
            draft_aft = float(data['draft_aft'])
            draft_forward = float(data['draft_forward'])
            density = float(data['density'])
        except ValueError:
            return False, "Error converting values to numbers"

        # Validate ranges
        if not DraftValidator.is_valid_draft_range(draft_aft):
            return False, "Draft aft out of valid range (0-20m)"

        if not DraftValidator.is_valid_draft_range(draft_forward):
            return False, "Draft forward out of valid range (0-20m)"

        if not DraftValidator.is_valid_density(density):
            return False, "Density out of valid range (0.95-1.1)"

        return True, ""

    @staticmethod
    def validate_observed_drafts(data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate observed draft readings
        """
        required_fields = ['draft_for_port', 'draft_for_star',
                           'draft_aft_port', 'draft_aft_star']

        # Check required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"

            if not DraftValidator.is_valid_number(str(data[field])):
                return False, f"Invalid number format in {field}"

        # Convert to float for range validation
        try:
            draft_for_port = float(data['draft_for_port'])
            draft_for_star = float(data['draft_for_star'])
            draft_aft_port = float(data['draft_aft_port'])
            draft_aft_star = float(data['draft_aft_star'])

            # Optional fields
            draft_mid_port = float(data.get('draft_mid_port', 0))
            draft_mid_star = float(data.get('draft_mid_star', 0))

        except ValueError:
            return False, "Error converting values to numbers"

        # Validate ranges
        for draft in [draft_for_port, draft_for_star, draft_aft_port, draft_aft_star,
                      draft_mid_port, draft_mid_star]:
            if not DraftValidator.is_valid_draft_range(draft):
                return False, "Draft value out of valid range (0-20m)"

        return True, ""

    @staticmethod
    def validate_vessel_data(data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate vessel data inputs
        """
        # Validate LBP if provided
        if 'lbp' in data and data['lbp']:
            if not DraftValidator.is_valid_number(str(data['lbp'])):
                return False, "Invalid LBP format"
            lbp = float(data['lbp'])
            if not DraftValidator.is_valid_lbp(lbp):
                return False, "LBP out of valid range (50-400m)"

        if 'light_ship' in data and data['light_ship']:
            if not DraftValidator.is_valid_number(str(data['light_ship'])):
                return False, "Invalid Light Ship format"
            light_ship = float(data['light_ship'])
            if not DraftValidator.is_valid_light_ship(light_ship):
                return False, "Light Ship out of valid range (1000-200000 mt)"

        if 'declared_constant' in data and data['declared_constant']:
            if not DraftValidator.is_valid_number(str(data['declared_constant'])):
                return False, "Invalid Declared Constant format"
            declared_constant = float(data['declared_constant'])
            if not DraftValidator.is_valid_declared_constant(declared_constant):
                return False, "Declared Constant out of valid range (-500-500 mt)"

        if 'quantity_bl' in data and data['quantity_bl']:
            if not DraftValidator.is_valid_number(str(data['quantity_bl'])):
                return False, "Invalid Quantity BL format"

        # Validate distances if provided
        distance_fields = ['distance_from_for_pp',
                           'distance_from_aft_pp', 'distance_from_mid_pp']
        for field in distance_fields:
            if field in data and data[field]:
                if not DraftValidator.is_valid_number(str(data[field])):
                    return False, f"Invalid {field} format"
                distance = float(data[field])
                if not DraftValidator.is_valid_distance(distance):
                    return False, f"{field} out of valid range (0-200m)"

        # Validate positions if provided
        position_fields = ['position_from_for_pp',
                           'position_from_aft_pp', 'position_from_mid_pp']
        for field in position_fields:
            if field in data and data[field]:
                if not DraftValidator.is_valid_position(data[field]):
                    return False, f"Invalid {field} (must be A, F, or N/A)"

        return True, ""

    @staticmethod
    def validate_bunker_data(data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate bunker quantity data
        """
        bunker_validators = {
            'ballast': (DraftValidator.is_valid_ballast_quantity, "0-12000 mt"),
            'fuel': (DraftValidator.is_valid_bunker_quantity, "0-10000 mt"),
            'gas_oil': (DraftValidator.is_valid_bunker_quantity, "0-10000 mt"),
            'lub_oil': (DraftValidator.is_valid_bunker_quantity, "0-10000 mt"),
            'slops': (DraftValidator.is_valid_bunker_quantity, "0-10000 mt"),
            'others': (DraftValidator.is_valid_bunker_quantity, "0-10000 mt"),
            'fresh_water': (DraftValidator.is_valid_bunker_quantity, "0-10000 mt")
        }

        for field, (validator, range_str) in bunker_validators.items():
            if field in data and data[field]:
                if not DraftValidator.is_valid_number(str(data[field])):
                    return False, f"Invalid {field} format"
                quantity = float(data[field])
                if not validator(quantity):
                    return False, f"{field.replace('_', ' ').title()} out of valid range ({range_str})"

        return True, ""

    @staticmethod
    def validate_interpolation_data(data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate interpolation table data
        """
        required_fields = ['draft_sup', 'draft_inf', 'displacement_sup', 'displacement_inf',
                           'tpc_sup', 'tpc_inf', 'lcf_sup', 'lcf_inf']

        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"

            if not DraftValidator.is_valid_number(str(data[field])):
                return False, f"Invalid number format in {field}"

        # Validate draft ranges
        try:
            draft_sup = float(data['draft_sup'])
            draft_inf = float(data['draft_inf'])

            if not DraftValidator.is_valid_draft_range(draft_sup):
                return False, "Draft sup out of valid range (0-20m)"

            if not DraftValidator.is_valid_draft_range(draft_inf):
                return False, "Draft inf out of valid range (0-20m)"

            if draft_sup <= draft_inf:
                return False, "Draft sup must be greater than draft inf"

        except ValueError:
            return False, "Error converting draft values to numbers"

        return True, ""

    @staticmethod
    def validate_mtc_data(data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate MTC calculation data
        """
        required_fields = ['d_plus50_sup', 'd_plus50_inf', 'd_plus50',
                           'mtc_plus50_sup', 'mtc_plus50_inf',
                           'd_moins50_sup', 'd_moins50_inf', 'd_moins50',
                           'mtc_moins50_sup', 'mtc_moins50_inf']

        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"

            if not DraftValidator.is_valid_number(str(data[field])):
                return False, f"Invalid number format in {field}"

        # Validate draft ranges
        try:
            d_plus50_sup = float(data['d_plus50_sup'])
            d_plus50_inf = float(data['d_plus50_inf'])
            d_plus50 = float(data['d_plus50'])

            d_moins50_sup = float(data['d_moins50_sup'])
            d_moins50_inf = float(data['d_moins50_inf'])
            d_moins50 = float(data['d_moins50'])

            if not DraftValidator.is_valid_draft_range(d_plus50_sup):
                return False, "D+50 sup out of valid range (0-20m)"

            if not DraftValidator.is_valid_draft_range(d_plus50_inf):
                return False, "D+50 inf out of valid range (0-20m)"

            if not DraftValidator.is_valid_draft_range(d_plus50):
                return False, "D+50 out of valid range (0-20m)"

            if not DraftValidator.is_valid_draft_range(d_moins50_sup):
                return False, "D-50 sup out of valid range (0-20m)"

            if not DraftValidator.is_valid_draft_range(d_moins50_inf):
                return False, "D-50 inf out of valid range (0-20m)"

            if not DraftValidator.is_valid_draft_range(d_moins50):
                return False, "D-50 out of valid range (0-20m)"

        except ValueError:
            return False, "Error converting draft values to numbers"

        return True, ""

    @staticmethod
    def validate_entry_callback(P: str) -> bool:
        """
        Validation callback for tkinter Entry widgets
        Allows only numbers and one decimal point
        """
        if P == "":  # Allow empty field
            return True

        # Allow only digits and one decimal point
        if re.match(r'^\d*\.?\d*$', P):
            return True

        return False

    @staticmethod
    def validate_numeric_entry_callback(P: str) -> bool:
        """
        Enhanced validation callback for numeric entries
        Allows numbers, one decimal point, and negative sign
        """
        if P == "" or P == "-":  # Allow empty field or negative sign
            return True

        # Allow digits, one decimal point, and negative sign
        if re.match(r'^-?\d*\.?\d*$', P):
            return True

        return False

    @staticmethod
    def validate_positive_numeric_entry_callback(P: str) -> bool:
        """
        Validation callback for positive numeric entries only
        """
        if P == "":  # Allow empty field
            return True

        # Allow only positive digits and one decimal point
        if re.match(r'^\d*\.?\d*$', P):
            return True

        return False
