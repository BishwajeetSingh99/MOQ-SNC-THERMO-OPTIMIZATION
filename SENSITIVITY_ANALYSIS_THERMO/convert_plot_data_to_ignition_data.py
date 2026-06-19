















import os
import pandas as pd

# <- paste your file path here
file_path = "/data2/RANA/FINAL_RUN_7nc/PROPNANE_SENSITIVITY/PROPANE_MECH_data/paper_ignition_delay_data.txt"

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


