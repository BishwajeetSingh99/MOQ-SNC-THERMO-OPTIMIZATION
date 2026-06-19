'''
import os
import pandas as pd

def compute_mean_relative_error(original_csv, reduced_csv):
    try:
        df_orig = pd.read_csv(original_csv)
        df_red = pd.read_csv(reduced_csv)

        if len(df_orig) != len(df_red):
            print(f"⚠️ Row count mismatch: {original_csv}")
            return None

        orig_vals = df_orig["Nominal"].astype(float)
        red_vals = df_red["Nominal"].astype(float)

        rel_error = abs(red_vals - orig_vals) / orig_vals * 100
        return rel_error.mean()
    except Exception as e:
        print(f"❌ Error processing {original_csv}: {e}")
        return None

def evaluate_reduction_folder(reduction_folder_path, original_case_folder):
    reduced_plot_dir = os.path.join(reduction_folder_path, "Plot", "Dataset")

    if not os.path.isdir(reduced_plot_dir):
        print(f"⚠️ No reduced plot data in: {reduced_plot_dir}")
        return None

    all_case_errors = []

    # Go through all target types (Tig, RCM, etc.)
    for target_type in os.listdir(reduced_plot_dir):
        orig_target_dir = os.path.join(original_case_folder, target_type)
        red_target_dir = os.path.join(reduced_plot_dir, target_type)

        if not os.path.isdir(orig_target_dir) or not os.path.isdir(red_target_dir):
            continue

        for fname in os.listdir(orig_target_dir):
            if not fname.endswith(".csv"):
                continue

            orig_file = os.path.join(orig_target_dir, fname)
            red_file = os.path.join(red_target_dir, fname)

            if not os.path.isfile(red_file):
                continue

            error = compute_mean_relative_error(orig_file, red_file)
            if error is not None:
                all_case_errors.append(error)

    return sum(all_case_errors) / len(all_case_errors) if all_case_errors else None

def summarize_reduction_errors(home_dir=None, summary_filename="reduction_errors.txt"):
    if home_dir is None:
        home_dir = os.getcwd()

    original_case_folder = os.path.join(home_dir, "Plot", "Dataset")
    summary_txt_file = os.path.join(home_dir, summary_filename)

    reduction_folders = [f for f in os.listdir(home_dir)
                         if f.startswith("reduced_mechanism") and os.path.isdir(os.path.join(home_dir, f))]

    results = []

    for folder in sorted(reduction_folders):
        folder_path = os.path.join(home_dir, folder)
        mean_error = evaluate_reduction_folder(folder_path, original_case_folder)

        if mean_error is not None:
            results.append(f"{folder}: Mean Error = {mean_error:.3f}%")
        else:
            results.append(f"{folder}: No valid data found.")

    with open(summary_txt_file, 'w') as f:
        f.write("Reduction Error Summary\n")
        f.write("========================\n")
        for line in results:
            print(line)
            f.write(line + "\n")

    print(f"\n✅ Summary saved to: {summary_txt_file}")
'''






import os
import pandas as pd

def compute_mean_relative_error(original_csv, reduced_csv):
    try:
        df_orig = pd.read_csv(original_csv)
        df_red = pd.read_csv(reduced_csv)

        if len(df_orig) != len(df_red):
            print(f"⚠️ Row count mismatch: {original_csv}")
            return None

        # Match column names written earlier
        orig_vals = df_orig["Obs(us)"].astype(float)
        red_vals = df_red["Reduced"].astype(float)

        rel_error = abs(red_vals - orig_vals) / orig_vals * 100
        return rel_error.mean()
    except Exception as e:
        print(f"❌ Error processing {original_csv}: {e}")
        return None

def evaluate_single_reduction_case(
    reduced_mech_folder,
    original_dataset_folder,
    target_types=("Tig", "RCM", "JSR", "Fls"),
    verbose=False
):
    """
    Compare reduced results to original and return mean relative error (%)
    Args:
        reduced_mech_folder (str): path to 'reduced_mechanism_xxx' folder
        original_dataset_folder (str): path to 'plot/Dataset'
        target_types (tuple): folders to look under (Tig, RCM, etc.)
        verbose (bool): whether to print per-case info
    Returns:
        float or None: mean relative error (%) for this reduction
    """
    
    reduced_plot_dir = os.path.join(reduced_mech_folder, "plot", "Dataset")
    if not os.path.isdir(reduced_plot_dir):
        print(f"❌ Reduced plot folder not found in {reduced_mech_folder}")
        return None

    all_errors = []

    for target_type in target_types:
        orig_dir = os.path.join(original_dataset_folder, target_type)
        red_dir = os.path.join(reduced_plot_dir, target_type)

        if not os.path.isdir(orig_dir) or not os.path.isdir(red_dir):
            continue

        for fname in os.listdir(orig_dir):
            if not fname.endswith(".csv"):
                continue

            orig_path = os.path.join(orig_dir, fname)
            red_path = os.path.join(red_dir, fname)

            if not os.path.isfile(red_path):
                if verbose:
                    print(f"⚠️ Missing reduced file: {fname}")
                continue

            error = compute_mean_relative_error(orig_path, red_path)
            if error is not None:
                all_errors.append(error)
                if verbose:
                    print(f"{fname}: {error:.2f}%")

    if all_errors:
        mean_error = sum(all_errors) / len(all_errors)
        if verbose:
            print(f"\n✅ Mean Error for {os.path.basename(reduced_mech_folder)}: {mean_error:.2f}%")
        return mean_error
    else:
        print(f"⚠️ No valid CSV comparisons found in {reduced_mech_folder}")
        return None
