#!/usr/bin/env python3
"""
Create one target-id per (phi,P) pair; inside each target-id produce numbered targets 1,2,3,...

Edit input_csv and output_path and run with python3.
"""
import os, re, math
import pandas as pd

# ---------- EDIT THESE ----------
input_csv = "/data2/RANA/FINAL_RUN_7nc/PROPNANE_SENSITIVITY/PROPANE_MECH_data/propane/transformed_data.csv"
output_path = "targets.txt"
start_target_number = 10001001   # first group -> x10001001
# -------------------------------
### define the fuel composition here for any new fuel . Following is for propnae
PHI_COMPOSITION = {
    0.5: {"fuel_name": "C3H8", "fuel": 0.02,   "O2": 0.2057,  "N2": 0.7743},
    1.0: {"fuel_name": "C3H8", "fuel": 0.04,   "O2": 0.2020,  "N2": 0.7580},
    2.0: {"fuel_name": "C3H8", "fuel": 0.775,  "O2": 0.1937,  "N2": 0.7288},
}
## define the units
UNITS_LITERAL = "{'conc': 'mol', 'P': 'atm', 'T': 'K', 'observed': 'us', 'flow': ''}"

def parse_phi_P(group_text):
    if group_text is None:
        return (None, None)
    s = str(group_text).replace(',', ' ').lower()
    phi_m = re.search(r"phi\s*=\s*([0-9]*\.?[0-9]+)", s)
    p_m   = re.search(r"\bp\s*=\s*([0-9]*\.?[0-9]+)", s)
    phi = float(phi_m.group(1)) if phi_m else None
    p   = float(p_m.group(1))   if p_m   else None
    return phi, p

def find_phi_comp(phi_val):
    if phi_val is None: return None
    for k in PHI_COMPOSITION:
        if abs(k - float(phi_val)) < 1e-6:
            return PHI_COMPOSITION[k]
    nearest = min(PHI_COMPOSITION.keys(), key=lambda k: abs(k - float(phi_val)))
    if abs(nearest - float(phi_val)) <= 0.25:
        return PHI_COMPOSITION[nearest]
    return None

def format_line(index_in_group, target_id, T, P, phi_s, observed, comp):
    fuel_name = comp['fuel_name']
    fuel_s = f"{comp['fuel']:.8f}"
    o2_s   = f"{comp['O2']:.8f}"
    n2_s   = f"{comp['N2']:.8f}"
    T_s = f"{T:.1f}"
    P_s = f"{P:.2f}" if P is not None else ""
    obs_s = f"{observed:.1f}"
    # first column is the per-group index (1,2,3...), target_id is same for all rows of the group
    return (
        f"{index_in_group}\t|{target_id}\t| target -- Tig\t| simulation -- Isochor Homo Reactor\t"
        f"| measurnment_type -- OHEX;max\t|Ignition_mode -- reflected\t| Flame_type -- \t"
        f"| Reactor_type -- \t| Fuel_type -- Multi\t"
        f"| Fuel -- x->{{'a': '{fuel_name}'}} = {{'a': {fuel_s}}}\t"
        f"| Oxidizer -- x->O2 = {o2_s}\t"
        f"| Bath_gas -- x->{{'a': 'N2'}}={{'a':{n2_s}}}\t"
        f"|T -- {T_s}\t| P -- {P_s}\t| flow_rate -- \t"
        f"|Phi -- {phi_s}\t| observed -- {obs_s}\t| obs_unit --us \t| deviation -- 0.0\t"
        f"|data_weight -- 1\t|units -- {UNITS_LITERAL}"
    )

def read_csv_flex(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    df = pd.read_csv(path, engine='python', dtype=str)
    df.columns = [c.strip().lstrip('\ufeff') for c in df.columns]
    cols = df.columns.tolist()
    x_col = next((c for c in cols if '1000' in c or '1000/x' in c or c.lower().startswith('x')), cols[0])
    y_col = next((c for c in cols if c.lower()=='y' or 'observed' in c.lower()), (cols[1] if len(cols)>1 else cols[0]))
    g_col = next((c for c in cols if 'group' in c.lower() or 'phi' in c.lower()), (cols[2] if len(cols)>2 else cols[-1]))
    def to_float(s): 
        return pd.to_numeric(s.astype(str).str.replace(',', '.').str.strip(), errors='coerce')
    return pd.DataFrame({
        'x_trans': to_float(df[x_col]),
        'y': to_float(df[y_col]),
        'group': df[g_col].astype(str).str.strip()
    })

def main():
    df = read_csv_flex(input_csv)
    total_rows = len(df)
    # Build ordered unique keys (phi,P) in order of first appearance
    key_order = []
    key_to_rows = {}
    for _, row in df.iterrows():
        g = row['group']
        x = row['x_trans']; y = row['y']
        phi, P = parse_phi_P(g)
        key = (None if phi is None else float(phi), None if P is None else float(P))
        # we include rows even if x/y are NaN; we'll filter later
        if key not in key_to_rows:
            key_order.append(key)
            key_to_rows[key] = []
        key_to_rows[key].append((x, y, g))

    lines = []
    group_index = 0
    total_written = 0
    for key in key_order:
        group_index += 1
        phi_val, P_val = key
        # assign target id per group
        target_num = start_target_number + (group_index - 1)
        target_id = f"x{target_num}"
        # get composition for phi
        comp = find_phi_comp(phi_val) if phi_val is not None else None
        if comp is None:
            comp = {"fuel_name": "C3H8", "fuel": 0.0, "O2": 0.0, "N2": 0.0}
        rows = key_to_rows[key]
        # enumerate rows inside this group: 1,2,3,...
        idx_in_group = 0
        for (x, y, gtext) in rows:
            if pd.isna(x) or pd.isna(y):
                continue
            idx_in_group += 1
            phi_s = f"{phi_val:.1f}" if phi_val is not None else ""
            # Use the row's x_trans as T and y as observed
            T_val = float(x)
            observed_val = float(y)
            line = format_line(idx_in_group, target_id, T_val, P_val, phi_s, observed_val, comp)
            lines.append(line)
            total_written += 1

    # write output
    with open(output_path, 'w', encoding='utf-8') as fh:
        for L in lines:
            fh.write(L + "\n")

    print(f"Total rows in CSV: {total_rows}")
    print(f"Unique (phi,P) groups: {len(key_order)}")
    print(f"Wrote {total_written} target lines to {output_path}")

if __name__ == "__main__":
    main()

    
    
    
    
    
    
    
    
    
    
    
    

