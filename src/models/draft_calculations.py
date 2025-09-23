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

        trim_corrected = round(draft_aft_corrected - draft_for_corrected, 2)

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
            return round(draft, 2)

        if position == "N/A":
            return round(draft, 2)

        correction_factor = distance / lbm

        if trim > 0:  # Vessel trimmed by aft
            if position == "A":
                return round(draft - (trim * correction_factor), 2)
            elif position == "F":
                return round(draft + (trim * correction_factor), 2)
        else:  # Vessel trimmed by forward
            if position == "A":
                return round(draft + (abs(trim) * correction_factor), 2)
            elif position == "F":
                return round(draft - (abs(trim) * correction_factor), 2)

        return round(draft, 2)

    @staticmethod
    def calculate_mfa_mom_qm(draft_for_corrected: float, draft_aft_corrected: float,
                             draft_mid_corrected: float) -> dict:
        """
        Calculate Mean Fore-Aft (MFA), Mean of Means (MOM), and Quarter Mean (QM)
        """
        mfa = round((draft_for_corrected + draft_aft_corrected) / 2, 2)
        mom = round((mfa + draft_mid_corrected) / 2, 2)
        qm = round((mom + draft_mid_corrected) / 2, 2)

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
                displacement_inf + (ratio * (displacement_sup - displacement_inf)), 3)
        else:
            results['displacement'] = displacement_inf

        # Calculate interpolated TPC
        if draft_sup != draft_inf:
            ratio = (qm - draft_inf) / (draft_sup - draft_inf)
            results['tpc'] = round(tpc_inf + (ratio * (tpc_sup - tpc_inf)), 3)
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
            (trim_corrected * 100 * tpc * lcf) / lbp, 2)
        second_trim_correction = round(
            (trim_corrected * trim_corrected * 50 * delta_mtc) / lbp, 2)

        corrected_displacement_for_trim = round(
            displacement + first_trim_correction + second_trim_correction, 2)

        return {
            'trim_corrected': trim_corrected,
            'first_trim_correction': first_trim_correction,
            'second_trim_correction': second_trim_correction,
            'corrected_displacement_for_trim': corrected_displacement_for_trim
        }

    def calculate_density_corrections(self, table_density: float, dock_density: float,
                                      corrected_displacement_for_trim: float) -> float:
        """
        Calculate density correction for displacement
        """
        if table_density == 0:
            return corrected_displacement_for_trim

        return round((corrected_displacement_for_trim * dock_density) / table_density, 3)

    @staticmethod
    def calculate_total_deductibles(ballast: float, fuel: float, gas_oil: float,
                                    lub_oil: float, slops: float, others: float) -> float:
        """
        Calculate total deductibles from all bunker quantities
        """
        return round(ballast + fuel + gas_oil + lub_oil + slops + others, 3)

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

    @staticmethod
    def format_survey_report(vessel_data: dict, draft_data: dict, calculation_data: dict) -> str:
        """
        Format the complete survey report as text
        """
        report_lines = []

        # Header
        report_lines.append('***Final Draft Survey ***')
        report_lines.append('')

        # Vessel information
        if 'vessel_name' in vessel_data:
            report_lines.append(f"Vessel: {vessel_data['vessel_name']}")
        if 'draft_number' in vessel_data:
            report_lines.append(f"Draft Number: {vessel_data['draft_number']}")
        report_lines.append('')

        # Time sheet data
        if 'time_sheet' in vessel_data:
            for key, value in vessel_data['time_sheet'].items():
                report_lines.append(f"{key}: {value}")
        report_lines.append('')

        # Observed drafts
        report_lines.append('===========================')
        report_lines.append('Observed Draft')
        if 'observed_drafts' in draft_data:
            obs = draft_data['observed_drafts']
            report_lines.append(
                f'Dfp: {obs.get("draft_for_port", 0)} m\t Dfs: {obs.get("draft_for_star", 0)}m')
            report_lines.append(
                f'Dmp: {obs.get("draft_mid_port", 0)} m\t Dms: {obs.get("draft_mid_star", 0)}m')
            report_lines.append(
                f'Dap: {obs.get("draft_aft_port", 0)} m\t Das: {obs.get("draft_aft_star", 0)}m')
        report_lines.append('')

        # Corrected drafts
        report_lines.append('===========================')
        report_lines.append('Corrected Draft:')
        if 'corrected_drafts' in draft_data:
            corr = draft_data['corrected_drafts']
            report_lines.append(
                f'Trim Ob: {corr.get("trim_observed", 0)}m\t Lbm:{corr.get("lbm", 0)}m')
            report_lines.append(
                f'Dfc: {corr.get("draft_for_corrected", 0)} m\t Dac: {corr.get("draft_aft_corrected", 0)}m')
            report_lines.append(f'Dmc: {corr.get("draft_mid_corrected", 0)} m')
        report_lines.append('')

        # MFA/MOM/QM
        if 'mfa_mom_qm' in draft_data:
            mfa_data = draft_data['mfa_mom_qm']
            report_lines.append(f'MFA: {mfa_data.get("mfa", 0)} m')
            report_lines.append(f'MOM: {mfa_data.get("mom", 0)} m')
            report_lines.append(f'QM: {mfa_data.get("qm", 0)} m')
        report_lines.append('')

        # Displacement corrections
        report_lines.append('===========================')
        report_lines.append('Displacement Corrections:')
        if 'displacement_corrections' in calculation_data:
            disp = calculation_data['displacement_corrections']
            report_lines.append(
                f'Displacement: {disp.get("displacement", 0)} mt')
            report_lines.append(
                f'Dis Corrected for trim: {disp.get("corrected_displacement_for_trim", 0)} mt')
            report_lines.append(
                f'Dis Corrected for density: {disp.get("corrected_displacement_for_density", 0)} mt')
            report_lines.append(
                f'Total deductibles: {disp.get("total_deductibles", 0)} mt')
            report_lines.append(
                f'Net Displacement: {disp.get("load_displacement", 0)} mt')
            report_lines.append(f'Cargo + const: {disp.get("cargo", 0)} mt')

        return '\n'.join(report_lines)
