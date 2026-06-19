'''
import os
import csv
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def extract_simulation_data(home_dir,main_output_folder num_cases, mechanism_dirs,
                                         nominal_csv='nominal_results.csv',
                                         reduced_csv='reduced_results.csv'):

    nominal_mechs = [m for m in mechanism_dirs if m.lower() == 'nominal']
    reduced_mechs = [m for m in mechanism_dirs if m.lower() != 'nominal']

    reduced_mechs = sorted(reduced_mechs, key=natural_sort_key)

    def read_mechanism_data(mechs):
        all_data = []
        for mech_dir in mechs:
            row = []
            for case_num in range(num_cases):
                tau_file = os.path.join(home_dir, mech_dir, f'case-{case_num}', 'output', 'tau.out')
                try:
                    with open(tau_file, 'r') as f:
                        lines = f.readlines()
                        if len(lines) >= 2 and len(lines[1].strip().split()) >= 2:
                            tau_value = lines[1].strip().split()[1]
                            row.append(tau_value)
                        else:
                            print(f"Invalid format in file: {tau_file}")
                            row.append('NA')
                except FileNotFoundError:
                    print(f"Missing file: {tau_file}")
                    row.append('NA')
            all_data.append(row)
        return all_data

    nominal_data = read_mechanism_data(nominal_mechs)
    reduced_data = read_mechanism_data(reduced_mechs)

    # Write nominal CSV (no header)
    if nominal_mechs:
        output_path = os.path.join(home_dir, nominal_csv)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in nominal_data:
                writer.writerow(row)
        print(f"✅ Nominal results saved to: {output_path}")
    else:
        print("⚠️ No nominal mechanism found, nominal CSV not created.")

    # Write reduced mechanisms CSV (no header)
    if reduced_mechs:
        output_path = os.path.join(home_dir, reduced_csv)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in reduced_data:
                writer.writerow(row)
        print(f"✅ Reduced mechanisms results saved to: {output_path}")
    else:
        print("⚠️ No reduced mechanisms found, reduced CSV not created.")

'''




import os
import csv
import re

def natural_sort_key(s):
    # Helper for natural sorting: e.g., ['sample_2', 'sample_10'] => ['sample_2', 'sample_10']
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def extract_simulation_data(home_dir, main_output_folder, num_cases, mechanism_dirs,
                            nominal_csv='nominal_results.csv',
                            reduced_csv='reduced_results.csv'):

    nominal_mechs = [m for m in mechanism_dirs if m.lower() == 'nominal']
    reduced_mechs = [m for m in mechanism_dirs if m.lower() != 'nominal']
    reduced_mechs = sorted(reduced_mechs, key=natural_sort_key)

    def read_mechanism_data(mechs, base_dir):
        all_data = []
        for mech_dir in mechs:
            row = []
            for case_num in range(num_cases):
                tau_file = os.path.join(base_dir, mech_dir, f'case-{case_num}', 'output', 'tau.out')
                try:
                    with open(tau_file, 'r') as f:
                        lines = f.readlines()
                        if len(lines) >= 2 and len(lines[1].strip().split()) >= 2:
                            tau_value = lines[1].strip().split()[1]
                            row.append(tau_value)
                        else:
                            print(f"⚠️ Invalid format in file: {tau_file}")
                            row.append('NA')
                except FileNotFoundError:
                    print(f"❌ Missing file: {tau_file}")
                    row.append('NA')
            all_data.append(row)
        return all_data

    nominal_data = read_mechanism_data(nominal_mechs, home_dir)
    reduced_data = read_mechanism_data(reduced_mechs, main_output_folder)

    # Write nominal CSV
    if nominal_mechs:
        nominal_path = os.path.join(home_dir, nominal_csv)
        with open(nominal_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in nominal_data:
                writer.writerow(row)
        print(f"✅ Nominal results saved to: {nominal_path}")
    else:
        raise AssertionError("NO nominal simulations found")
    # Write reduced CSV
    if reduced_mechs:
        reduced_path = os.path.join(home_dir, reduced_csv)
        with open(reduced_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in reduced_data:
                writer.writerow(row)
        print(f"✅ Reduced mechanisms results saved to: {reduced_path}")
    else:
        raise AssertionError("⚠️ No reduced mechanisms found, reduced CSV not created.")

