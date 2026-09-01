# NFL v1.1 Google Sheets Round-Trip Verification

**Status: PASS**

- Native Google Sheet ID: `1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew`
- Source SHA-256: `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f`
- Round-trip XLSX SHA-256: `fbfda1be9657b422e502baa5761fb4907e8e21f4908f5c1751b7c4ab715ab0fb`
- Sheets: 21 (11 visible / 10 hidden)
- Formula cells: 57,399
- 2026 regular-season games: 272 (unscored: 272)
- Usable market spreads: 0
- Active adjustments: 0
- Nonzero QB deltas: 0
- Team-rating overrides: 0

## Verification
- PASS — sheet_order_states_exact
- PASS — sheet_count_21
- PASS — formula_count_exact
- PASS — formula_coordinates_text_exact
- PASS — formula_cached_values_exact
- PASS — nonformula_constants_exact
- PASS — defined_names_exact_order_insensitive
- PASS — data_validations_exact_order_insensitive
- PASS — meaningful_cell_visual_styles_exact
- PASS — used_column_widths_exact
- PASS — zip_members_same
- PASS — drawings_persons_byte_exact
- PASS — schedule_2026_272_reg_unscored
- PASS — usable_market_spreads_zero
- PASS — active_adjustments_zero
- PASS — nonzero_qb_deltas_zero
- PASS — team_overrides_zero
- PASS — dq_current_week_clean
- PASS — banner_v11
- PASS — changelog_alignment_entry_preserved
- PASS — cached_error_cells_exact

## Accepted Google package differences

- Style IDs were deduplicated and no-op style metadata removed; every meaningful cell retains equivalent visual formatting.
- Formatting-only cells and column spans beyond populated ranges were omitted; populated/used column widths are unchanged.
- Named ranges and validation rules were reordered only; their definitions and targets are unchanged.
- Shared strings and worksheet XML were repackaged; formulas, constants, cached results, drawings, and workbook behavior are unchanged.
