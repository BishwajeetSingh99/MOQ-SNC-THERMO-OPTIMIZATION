

# create a text file with raw data (generally taken from plots ) and arrange them in following order in a text file..pass the text file as an input argument 
'''
#Phi = 0.5 P = 37
1.0505263157894738, 129.6590909090909
1.0905263157894738, 262.10227272727275
1.1726315789473685, 303.72727272727275
1.12, 375.625
1.1494736842105264, 421.03409090909093
1.1494736842105264, 523.2045454545455
1.1831578947368422, 568.6136363636364
1.231578947368421, 561.0454545454545
1.2821052631578946, 564.8295454545455
1.3305263157894736, 595.1022727272727
1.3789473684210527, 667
1.4, 807.0113636363636
# phi = 2.0 P = 30
1.2020942408376964, 399.0689655172414
1.250261780104712, 445
1.2774869109947644, 425.8620689655172
1.3109947643979059, 460.31034482758616
1.336125654450262, 425.8620689655172
1.350785340314136, 506.2413793103448
1.3989528795811519, 487.10344827586204
1.3989528795811519, 636.3793103448276
1.3801047120418848, 670.8275862068965
1.4219895287958115, 697.6206896551724
1.4282722513089006, 793.3103448275862
1.430366492146597, 843.0689655172414
#phi = 1.0 P = 30
1.0372703412073492, 77.55172413793103
1.0792650918635172, 261.2758620689655
1.1317585301837272, 402.8965517241379
1.1611548556430447, 510.06896551724134
1.2115485564304462, 575.1379310344828
1.2514435695538058, 529.2068965517241
1.310236220472441, 513.8965517241379
1.3606299212598425, 590.448275862069
1.320734908136483, 628.7241379310344
1.411023622047244, 743.551724137931

#phi = 0.5 P = 27
1.051968503937008, 226.82758620689654
1.093963254593176, 379.9310344827586
1.1191601049868767, 517.7241379310344
1.1506561679790026, 632.551724137931
1.1716535433070867, 709.1034482758621
1.2115485564304462, 674.655172413793
1.2409448818897637, 586.6206896551724
1.2598425196850394, 712.9310344827586
1.2871391076115486, 670.8275862068965
1.3270341207349081, 674.655172413793
1.358530183727034, 712.9310344827586
1.4026246719160105, 774.1724137931034
1.3984251968503938, 881.3448275862069

#### in this way store all the data and pass the file. Be aware of the scale for y as in ms, us, s?
'''










'''
import os
import pandas as pd

# <- paste your file path here
file_path = "/data/TEST-THERMO-sens/sens_code/creating_target_opt_file/paper_ignition_delay_data_raw.txt"

def read_and_transform(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    # quick preview for debugging
    with open(path, 'rb') as f:
        start_bytes = f.read(512)
    try:
        start_text = start_bytes.decode('utf-8')
    except UnicodeDecodeError:
        start_text = start_bytes.decode('latin-1', errors='replace')
    print("=== File preview (first 512 bytes) ===")
    print(start_text)
    print("=== End preview ===\n")

    rows = []
    current_header = None
    malformed_lines = []
    total_lines = 0

    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for lineno, raw in enumerate(fh, start=1):
            total_lines += 1
            line = raw.strip()
            if not line:
                # blank line
                continue
            if line.lstrip().startswith('#'):
                # capture header text (without leading '#')
                hdr = line.lstrip().lstrip('#').strip()
                if hdr:
                    current_header = hdr
                continue
            # attempt to split on whitespace (tabs or spaces)
            parts = line.split()
            if len(parts) < 2:
                malformed_lines.append((lineno, line))
                continue
            # Take first two tokens as x and y
            x_str, y_str = parts[0], parts[1]
            try:
                x = float(x_str)
                y = float(y_str)
                rows.append((x, y, current_header))
            except ValueError:
                malformed_lines.append((lineno, line))
                continue

    print(f"Total lines read: {total_lines}")
    print(f"Numeric data rows found: {len(rows)}")
    if malformed_lines:
        print(f"Malformed / skipped lines count: {len(malformed_lines)}")
        # print first few malformed for debugging
        for ln, txt in malformed_lines[:10]:
            print(f"  line {ln}: {txt!r}")

    if not rows:
        print("\nNo numeric rows were parsed. Possible causes:")
        print(" - Wrong file path or file is empty")
        print(" - Numeric values use a comma instead of a dot (e.g. '1,23')")
        print(" - Lines have nonstandard separators or hidden characters")
        return pd.DataFrame(columns=['x (1000/x)', 'y', 'group'])

    # build DataFrame
    df = pd.DataFrame(rows, columns=['x_orig', 'y', 'group'])
    # transform x -> 1000/x
    df['x (1000/x)'] = 1000.0 / df['x_orig']
    out_df = df[['x (1000/x)', 'y', 'group']].reset_index(drop=True)

    return out_df

if __name__ == "__main__":
    out = read_and_transform(file_path)
    if out.empty:
        print("\nResult: DataFrame is empty.")
    else:
        print("\nResult: first 20 rows:")
        print(out.head(20))
        # save output
        out.to_csv("transformed_data.csv", index=False)
        print("\nSaved to transformed_data.csv")

'''









import os
import pandas as pd

# Set the path to the raw data file created above
# IMPORTANT: This assumes 'paper_ignition_delay_data_raw.txt' is in the same directory.
file_path = "/data2/RANA/FINAL_RUN_7nc/PROPNANE_SENSITIVITY/PROPANE_MECH_data/propane/paper_ignition_delay_raw_data.txt"

def read_and_transform(path):
    """
    Reads raw ignition delay data (X, Y) from a text file, parses the
    experimental group headers (e.g., # Phi = 0.5 P = 37), and transforms
    the X-axis data (typically 1000/T, where T is the original X-value).

    Args:
        path (str): The file path to the raw data.

    Returns:
        pd.DataFrame: A DataFrame containing the transformed data and group labels.
    """
    if not os.path.isfile(path):
        # Using a simple print and exit for demonstration in this environment
        print(f"Error: File not found at the specified path: {path}")
        return pd.DataFrame(columns=['x (1000/x)', 'y', 'group'])

    # --- Debugging Preview ---
    # This section helps confirm the file content looks as expected
    with open(path, 'rb') as f:
        start_bytes = f.read(512)
    try:
        start_text = start_bytes.decode('utf-8')
    except UnicodeDecodeError:
        start_text = start_bytes.decode('latin-1', errors='replace')
    print("=== File preview (first 512 bytes) ===")
    print(start_text)
    print("=== End preview ===\n")
    # -------------------------

    rows = []
    current_header = None
    malformed_lines = []
    total_lines = 0

    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for lineno, raw in enumerate(fh, start=1):
            total_lines += 1
            line = raw.strip()

            if not line:
                # blank line
                continue
            
            if line.lstrip().startswith('#'):
                # capture header text (without leading '#')
                hdr = line.lstrip().lstrip('#').strip()
                if hdr:
                    current_header = hdr
                continue
            
            # --- CRITICAL FIX: Split on comma (',') instead of whitespace ---
            # Data format is 'X, Y'
            parts = line.split(',')
            
            if len(parts) < 2:
                malformed_lines.append((lineno, line))
                continue
            
            # Extract and strip whitespace from parts
            x_str = parts[0].strip()
            y_str = parts[1].strip()
            
            try:
                x = float(x_str)
                y = float(y_str)
                rows.append((x, y, current_header))
            except ValueError:
                # This catches cases where the parts aren't valid numbers
                malformed_lines.append((lineno, line))
                continue

    print(f"Total lines read: {total_lines}")
    print(f"Numeric data rows found: {len(rows)}")
    
    if malformed_lines:
        print(f"Malformed / skipped lines count: {len(malformed_lines)}")
        # print first few malformed for debugging
        for ln, txt in malformed_lines[:5]:
            print(f"  line {ln}: {txt!r}")

    if not rows:
        print("\nResult: DataFrame is empty. Check file path and format.")
        return pd.DataFrame(columns=['x (1000/x)', 'y', 'group'])

    # build DataFrame
    df = pd.DataFrame(rows, columns=['x_orig', 'y', 'group'])
    
    # transform x -> 1000/x
    # We must ensure x_orig is not zero before dividing
    df['x (1000/x)'] = 1000.0 / df['x_orig']
    out_df = df[['x (1000/x)', 'y', 'group']].reset_index(drop=True)

    return out_df

if __name__ == "__main__":
    out = read_and_transform(file_path)
    if out.empty:
        print("\nResult: DataFrame is empty.")
    else:
        print("\nResult: Parsed and transformed data (first 20 rows):")
        print(out.head(20))
        # save output
        out.to_csv("transformed_data.csv", index=False)
        print("\nSaved output to transformed_data.csv")

