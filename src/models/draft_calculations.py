class DraftCalculations:
    """Class handling all draft survey calculations"""

    @staticmethod
    def calculate_trim(draft_aft: float, draft_forward: float) -> float:
        """Calculate trim from aft and forward drafts"""
        return draft_aft - draft_forward

    @staticmethod
    def calculate_mean_draft(draft_aft: float, draft_forward: float) -> float:
        """Calculate mean draft"""
        return (draft_aft + draft_forward) / 2

    @staticmethod
    def calculate_density_correction(displacement: float, density: float) -> float:
        """Calculate density correction"""
        return displacement * (1.025 - density) / density

    @staticmethod
    def calculate_trim_correction(trim: float, lcf: float, mtc: float) -> float:
        """Calculate trim correction"""
        return (trim * lcf * mtc) / 100

    @staticmethod
    def interpolate_displacement(draft: float, lower_draft: float, upper_draft: float,
                                 lower_disp: float, upper_disp: float) -> float:
        """
        Interpolate displacement based on draft values
        """
        if upper_draft == lower_draft:
            return lower_disp

        ratio = (draft - lower_draft) / (upper_draft - lower_draft)
        return lower_disp + (ratio * (upper_disp - lower_disp))

    def calculate_total_displacement(self, observed_draft: float, density: float,
                                     trim: float, lcf: float, mtc: float,
                                     displacement_table: dict) -> float:
        """
        Calculate total displacement including all corrections
        """
        # Find nearest draft values in table
        drafts = sorted(displacement_table.keys())
        for i, table_draft in enumerate(drafts[:-1]):
            if table_draft <= observed_draft <= drafts[i + 1]:
                interpolated_disp = self.interpolate_displacement(
                    observed_draft,
                    table_draft,
                    drafts[i + 1],
                    displacement_table[table_draft],
                    displacement_table[drafts[i + 1]]
                )
                break
        else:
            raise ValueError("Draft value out of table range")

        # Apply corrections
        density_correction = self.calculate_density_correction(
            interpolated_disp, density)
        trim_correction = self.calculate_trim_correction(trim, lcf, mtc)

        return interpolated_disp + density_correction + trim_correction

    # New methods from p2.py integration

    @staticmethod
    def calculate_lbm(lbp: float, distance_from_for_pp: float, distance_from_aft_pp: float,
                      position_from_for_pp: str, position_from_aft_pp: str) -> float:
        """
        Calculate Longitudinal Center of Buoyancy Moment (LBM)
        """
        lbm_dict = {
            ('A', 'A'): lbp - distance_from_aft_pp - distance_from_for_pp,
            ('A', 'F'): lbp - distance_from_aft_pp + distance_from_for_pp,
            ('F', 'A'): lbp + distance_from_aft_pp + distance_from_for_pp,
            ('F', 'F'): lbp + distance_from_for_pp - distance_from_aft_pp,
            ('A', 'N/A'): lbp - distance_from_for_pp,
            ('F', 'N/A'): lbp + distance_from_for_pp,
            ('N/A', 'A'): lbp + distance_from_aft_pp,
            ('N/A', 'F'): lbp - distance_from_aft_pp
        }
        return lbm_dict.get((position_from_for_pp, position_from_aft_pp), lbp)

    def calculate_corrected_drafts(self, lbp: float, draft_for_port: float, draft_for_star: float,
                                   draft_aft_port: float, draft_aft_star: float,
                                   draft_mid_port: float, draft_mid_star: float,
                                   distance_from_for_pp: float, distance_from_aft_pp: float,
                                   distance_from_mid_pp: float, position_from_for_pp: str,
                                   position_from_aft_pp: str, position_from_mid_pp: str,
                                   trim_observed: float) -> dict:
        """
        Calculate corrected drafts based on observed values and positions
        """
        # Calculate mean drafts
        draft_for = (draft_for_star + draft_for_port) / 2
        draft_aft = (draft_aft_star + draft_aft_port) / 2
        draft_mid = (draft_mid_star + draft_mid_port) / 2

        # Calculate LBM
        lbm = self.calculate_lbm(lbp, distance_from_for_pp, distance_from_aft_pp,
                                 position_from_for_pp, position_from_aft_pp)

        # Calculate corrected drafts
        draft_for_corrected = self._calculate_single_draft_correction(
            draft_for, trim_observed, distance_from_for_pp, lbm, position_from_for_pp)

        draft_aft_corrected = self._calculate_single_draft_correction(
            draft_aft, trim_observed, distance_from_aft_pp, lbm, position_from_aft_pp)

        draft_mid_corrected = self._calculate_single_draft_correction(
            draft_mid, trim_observed, distance_from_mid_pp, lbm, position_from_mid_pp)

        trim_corrected = round(draft_aft_corrected - draft_for_corrected, 3)

        return {
            'draft_for': draft_for,
            'draft_aft': draft_aft,
            'draft_mid': draft_mid,
            'draft_for_corrected': draft_for_corrected,
            'draft_aft_corrected': draft_aft_corrected,
            'draft_mid_corrected': draft_mid_corrected,
            'trim_observed': trim_observed,
            'lbm': lbm,
            'trim_corrected': trim_corrected
        }

    def _calculate_single_draft_correction(self, draft: float, trim: float, distance: float,
                                           lbm: float, position: str) -> float:
        """
        Calculate correction for a single draft reading
        """
        if abs(trim) < 0.001:  # Trim is zero
            return round(draft, 3)

        if position == "N/A":
            return round(draft, 3)

        correction_factor = distance / lbm

        if trim > 0:  # Vessel trimmed by aft
            if position == "A":
                return round(draft - (trim * correction_factor), 3)
            elif position == "F":
                return round(draft + (trim * correction_factor), 3)
        else:  # Vessel trimmed by forward
            if position == "A":
                return round(draft + (abs(trim) * correction_factor), 3)
            elif position == "F":
                return round(draft - (abs(trim) * correction_factor), 3)

        return round(draft, 3)

    @staticmethod
    def calculate_mfa_mom_qm(draft_for_corrected: float, draft_aft_corrected: float,
                             draft_mid_corrected: float) -> dict:
        """
        Calculate Mean Fore-Aft (MFA), Mean of Means (MOM), and Quarter Mean (QM)
        """
        mfa = round((draft_for_corrected + draft_aft_corrected) / 2, 3)
        mom = round((mfa + draft_mid_corrected) / 2, 3)
        qm = round((mom + draft_mid_corrected) / 2, 3)

        return {
            'mfa': mfa,
            'mom': mom,
            'qm': qm
        }

    def calculate_interpolation_values(self, qm: float, draft_sup: float, draft_inf: float,
                                       displacement_sup: float, displacement_inf: float,
                                       tpc_sup: float, tpc_inf: float,
                                       lcf_sup: float, lcf_inf: float) -> dict:
        """
        Calculate interpolated values for displacement, TPC, and LCF
        """
        results = {}

        # Calculate interpolated displacement
        if draft_sup != draft_inf:
            ratio = (qm - draft_inf) / (draft_sup - draft_inf)
            results['displacement'] = round(
                abs(displacement_inf + (ratio * (displacement_sup - displacement_inf))), 3)
        else:
            results['displacement'] = displacement_inf

        # Calculate interpolated TPC
        if draft_sup != draft_inf:
            ratio = (qm - draft_inf) / (draft_sup - draft_inf)
            results['tpc'] = round(
                abs(tpc_inf + (ratio * (tpc_sup - tpc_inf))), 3)
        else:
            results['tpc'] = tpc_inf

        # Calculate interpolated LCF
        if draft_sup != draft_inf:
            ratio = (qm - draft_inf) / (draft_sup - draft_inf)
            # This formula is correct for both positive and negative values
            results['lcf'] = round(lcf_inf + (ratio * (lcf_sup - lcf_inf)), 3)
        else:
            results['lcf'] = lcf_inf

        return results

    def calculate_mtc_values(self, d_plus50_sup: float, d_plus50_inf: float, d_plus50: float,
                             mtc_plus50_sup: float, mtc_plus50_inf: float,
                             d_moins50_sup: float, d_moins50_inf: float, d_moins50: float,
                             mtc_moins50_sup: float, mtc_moins50_inf: float) -> dict:
        """
        Calculate MTC+ and MTC- values using interpolation
        """
        results = {}

        # Calculate MTC+ (MTC1)
        if d_plus50_sup != d_plus50_inf:
            ratio = (d_plus50_sup - d_plus50) / (d_plus50_sup - d_plus50_inf)
            mtc1 = round(
                (((mtc_plus50_sup - mtc_plus50_inf) / (d_plus50_sup - d_plus50_inf)) *
                 (d_plus50_sup - d_plus50)) + mtc_plus50_inf, 2)
        else:
            mtc1 = mtc_plus50_inf
        results['mtc1'] = mtc1

        # Calculate MTC- (MTC2)
        if d_moins50_sup != d_moins50_inf:
            ratio = (d_moins50_sup - d_moins50) / \
                (d_moins50_sup - d_moins50_inf)
            mtc2 = round(
                (((mtc_moins50_sup - mtc_moins50_inf) / (d_moins50_sup - d_moins50_inf)) *
                 (d_moins50_sup - d_moins50)) + mtc_moins50_inf, 2)
        else:
            mtc2 = mtc_moins50_inf
        results['mtc2'] = mtc2

        # Calculate Delta MTC
        if isinstance(mtc1, (int, float)) and isinstance(mtc2, (int, float)):
            results['delta_mtc'] = round(abs(mtc1 - mtc2), 2)
        else:
            results['delta_mtc'] = 0.0

        return results

    def calculate_trim_corrections(self, draft_for_corrected: float, draft_aft_corrected: float,
                                   tpc: float, lcf: float, lbp: float, delta_mtc: float,
                                   displacement: float) -> dict:
        """
        Calculate first and second trim corrections
        """
        trim_corrected = draft_aft_corrected - draft_for_corrected

        first_trim_correction = round(
            (trim_corrected * 100 * tpc * lcf) / lbp, 3)
        second_trim_correction = round(
            (trim_corrected * trim_corrected * 50 * delta_mtc) / lbp, 3)

        corrected_displacement_for_trim = round(
            displacement + first_trim_correction + second_trim_correction, 3)

        return {
            'trim_corrected': trim_corrected,
            'first_trim_correction': first_trim_correction,
            'second_trim_correction': second_trim_correction,
            'corrected_displacement_for_trim': corrected_displacement_for_trim
        }

    def calculate_density_corrections(self, table_density: float, dock_density: float,
                                      corrected_displacement_for_trim: float) -> dict:
        """
        Calculate density correction for displacement
        """
        if table_density == 0:
            corrected_displacement = corrected_displacement_for_trim
        else:
            corrected_displacement = round(
                (corrected_displacement_for_trim * dock_density) / table_density, 3)
        return {'corrected_displacement_for_density': corrected_displacement}

    @staticmethod
    def calculate_total_deductibles(ballast: float, fuel: float, gas_oil: float,
                                    lub_oil: float, slops: float, others: float, fresh_water: float) -> float:
        """
        Calculate total deductibles from all bunker quantities
        """
        return round(ballast + fuel + gas_oil + lub_oil + slops + others + fresh_water, 3)

    def calculate_load_displacement(self, corrected_displacement: float, total_deductibles: float,
                                    net_init_displacement: float, operation_type: str) -> dict:
        """
        Calculate load displacement and cargo based on operation type
        """
        if operation_type == 'load':
            # For Loading operation
            load_displacement = round(
                corrected_displacement - total_deductibles, 3)
            cargo = round(load_displacement - net_init_displacement, 3)
        elif operation_type == 'discharge':
            # For Discharging operation
            net_displacement = round(
                corrected_displacement - total_deductibles, 3)
            cargo = round(net_init_displacement - net_displacement, 3)
        else:
            raise ValueError(
                "Invalid operation type. Must be 'load' or 'discharge'")

        return {
            'load_displacement': load_displacement if operation_type == 'load' else net_displacement,
            'cargo': cargo
        }

    @staticmethod  # type: ignore
    def format_two_column_report(vessel_data: dict, initial_data: dict, final_data: dict) -> str:
        """Formats a two-column report for initial and final surveys."""

        def get_val(data_dict, *keys, default='N/A', precision=3):
            """Safely get nested dictionary values."""
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

        lines = []
        col_width = 35
        title_width = col_width * 2 + 1

        # --- Report Header ---
        lines.append('*** DRAFT SURVEY REPORT ***'.center(title_width))
        lines.append('=' * title_width)

        # --- Vessel Information ---
        lines.append("\n" + "--- VESSEL INFORMATION ---".center(title_width))
        lines.append(f"{'Vessel Name:':<20} {get_val(vessel_data, 'vessel_name', default=''):<25} {'Port of Registry:':<20} {get_val(vessel_data, 'port_of_registry', default=''):<25}")
        lines.append(
            f"{'Draft Number:':<20} {get_val(vessel_data, 'draft_number', default=''):<25} {'IMO:':<20} {get_val(vessel_data, 'imo', default=''):<25}")
        lines.append(
            f"{'Client:':<20} {get_val(vessel_data, 'client', default=''):<25} {'Product:':<20} {get_val(vessel_data, 'product', default=''):<25}")
        lines.append(
            f"{'LBP (m):':<20} {get_val(vessel_data, 'lbp'):<25} {'Loading Port:':<20} {get_val(vessel_data, 'loading_port', default=''):<25}")
        lines.append(
            f"{'Light Ship (mt):':<20} {get_val(vessel_data, 'light_ship'):<25} {'Discharging Port:':<20} {get_val(vessel_data, 'discharging_port', default=''):<25}")
        lines.append(
            f"{'Declared Constant:':<20} {get_val(vessel_data, 'declared_constant'):<25} {'Quantity B/L (mt):':<20} {get_val(vessel_data, 'quantity_bl'):<25}")
        lines.append(f"{'Table Density:':<20} {get_val(vessel_data, 'table_density'):<25} {'Operation Type:':<20} {get_val(vessel_data, 'operation_type', default='').upper():<25}")
        lines.append('=' * title_width)

        # --- Time Sheet ---
        lines.append("\n" + "--- TIME SHEET ---".center(title_width))
        time_sheet = vessel_data.get('time_sheet', {})
        time_sheet_items = list(time_sheet.keys())
        for i in range(0, len(time_sheet_items), 2):
            key1 = time_sheet_items[i]
            label1 = key1.replace('_', ' ').title() + ':'
            val1 = time_sheet.get(key1, 'N/A')
            line = f"{label1:<25} {val1:<20}"

            if i + 1 < len(time_sheet_items):
                key2 = time_sheet_items[i+1]
                label2 = key2.replace('_', ' ').title() + ':'
                val2 = time_sheet.get(key2, 'N/A')
                line += f"|  {label2:<25} {val2:<20}"
            lines.append(line)
        lines.append('=' * title_width)

        # --- Observed Drafts and Distances ---
        lines.append(
            "\n" + "--- OBSERVED DRAFTS & DISTANCES ---".center(title_width))
        header = f"{'DESCRIPTION':<25} | {'INITIAL':^{col_width}} | {'FINAL':^{col_width}}"
        lines.append(header)
        lines.append('-' * title_width)

        observed_items = [
            ("Fwd Port", 'draft_data', 'observed_drafts', 'draft_for_port'),
            ("Fwd Starboard", 'draft_data', 'observed_drafts', 'draft_for_star'),
            ("Mid Port", 'draft_data', 'observed_drafts', 'draft_mid_port'),
            ("Mid Starboard", 'draft_data', 'observed_drafts', 'draft_mid_star'),
            ("Aft Port", 'draft_data', 'observed_drafts', 'draft_aft_port'),
            ("Aft Starboard", 'draft_data', 'observed_drafts', 'draft_aft_star'),
            ("--- Distances & Density ---",),
            ("Dock Density", 'vessel_params', 'dock_density'),
            ("Dist. Fwd PP (m)", 'vessel_params', 'distance_from_for_pp'),
            ("Pos. Fwd PP", 'vessel_params', 'position_from_for_pp'),
            ("Dist. Mid PP (m)", 'vessel_params', 'distance_from_mid_pp'),
            ("Pos. Mid PP", 'vessel_params', 'position_from_mid_pp'),
            ("Dist. Aft PP (m)", 'vessel_params', 'distance_from_aft_pp'),
            ("Pos. Aft PP", 'vessel_params', 'position_from_aft_pp'),
        ]

        for item in observed_items:
            label = item[0]
            if len(item) == 1:
                lines.append(f"\n{label.center(title_width)}")
                continue
            keys = item[1:]
            i_val_str = get_val(initial_data, *keys)
            f_val_str = get_val(final_data, *keys)
            line = f"{label:<25} | {i_val_str:^{col_width}} | {f_val_str:^{col_width}}"
            lines.append(line)

        # --- Survey Data Comparison ---
        lines.append(
            "\n" + "--- SURVEY DATA COMPARISON ---".center(title_width))
        header = f"{'DESCRIPTION':<25} | {'INITIAL':^{col_width}} | {'FINAL':^{col_width}}"
        lines.append(header)
        lines.append('-' * title_width)

        report_items = [
            ("--- Corrected Drafts ---",),
            ("Fwd Draft Corrected", 'draft_data',
             'corrected_drafts', 'draft_for_corrected'),
            ("Aft Draft Corrected", 'draft_data',
             'corrected_drafts', 'draft_aft_corrected'),
            ("Mid Draft Corrected", 'draft_data',
             'corrected_drafts', 'draft_mid_corrected'),
            ("Corrected Trim", 'draft_data', 'corrected_drafts', 'trim_corrected'),
            ("LBM", 'draft_data', 'corrected_drafts', 'lbm'),
            ("--- MFA/MOM/QM ---",),
            ("MFA", 'draft_data', 'mfa_mom_qm', 'mfa'),
            ("MOM", 'draft_data', 'mfa_mom_qm', 'mom'),
            ("QM", 'draft_data', 'mfa_mom_qm', 'qm'),
            ("--- Interpolation ---",),
            ("Displacement", 'draft_data', 'interpolation_results', 'displacement'),
            ("TPC", 'draft_data', 'interpolation_results', 'tpc'),
            ("LCF", 'draft_data', 'interpolation_results', 'lcf'),
            ("--- Trim Corrections ---",),
            ("1st Trim Correction", 'calculation_data',
             'trim_corrections', 'first_trim_correction'),
            ("2nd Trim Correction", 'calculation_data',
             'trim_corrections', 'second_trim_correction'),
            ("Disp Corrected (Trim)", 'calculation_data',
             'trim_corrections', 'corrected_displacement_for_trim'),
            ("--- Final Displacement ---",),
            ("Disp Corrected (Density)", 'calculation_data',
             'density_corrections', 'corrected_displacement_for_density'),
            ("Total Deductibles", 'calculation_data',
             'displacement_corrections', 'total_deductibles'),
        ]

        for item in report_items:
            label = item[0]
            if len(item) == 1:
                lines.append(f"\n{label.center(title_width)}")
                continue

            keys = item[1:]
            i_val_str = get_val(initial_data, *keys)
            f_val_str = get_val(final_data, *keys)

            line = f"{label:<25} | {i_val_str:^{col_width}} | {f_val_str:^{col_width}}"
            lines.append(line)

        # --- Final Summary ---
        lines.append("\n" + "--- FINAL CARGO SUMMARY ---".center(title_width))
        lines.append('-' * title_width)

        i_net_disp = get_val(initial_data, 'calculation_data',
                             'initial_results', 'net_displacement', default=0.0)
        # This is not right, need to get final load/net disp
        f_load_disp = get_val(final_data, 'calculation_data', 'density_corrections',
                              'corrected_displacement_for_density', default=0.0)

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

        op_type = vessel_data.get('operation_type', 'load')
        cargo_qty = abs(f_net - i_net)
        qty_bl = float(vessel_data.get('quantity_bl', 0))
        diff = cargo_qty - qty_bl

        lines.append(f"{'Initial Net Displacement:':<30} {i_net:.3f} mt")
        lines.append(f"{'Final Net Displacement:':<30} {f_net:.3f} mt")
        lines.append(f"{'Cargo Quantity (Survey):':<30} {cargo_qty:.3f} mt")
        lines.append(f"{'Cargo Quantity (B/L):':<30} {qty_bl:.3f} mt")
        lines.append(f"{'Difference:':<30} {diff:.3f} mt")
        lines.append('=' * title_width)

        return '\n'.join(lines)
