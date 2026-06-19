import os
import re

def generate_master_and_unique_species(folder_path):
    
    master_file = os.path.join(folder_path, "master_5%_species.txt")
    unique_file = os.path.join(folder_path, "unique_species_lists.txt")
    
    case_files = []
    
    # Collect case files
    for file in os.listdir(folder_path):
        if file.endswith(".txt") and "case_" in file:
            match = re.search(r'case_(\d+)', file)
            if match:
                case_index = int(match.group(1))
                case_files.append((case_index, file))
    
    # Sort serially
    case_files.sort(key=lambda x: x[0])
    
    unique_dict = {}  # {species_property: True}
    
    with open(master_file, 'w') as master_out:
        
        for case_index, file in case_files:
            input_path = os.path.join(folder_path, file)
            selected = []
            
            with open(input_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    if not line or line.startswith("Sensitivity"):
                        continue
                    
                    parts = line.split('\t')
                    if len(parts) < 2:
                        continue
                    
                    try:
                        sens = float(parts[0])
                    except ValueError:
                        continue
                    
                    if abs(sens) > 0.05:
                        species_prop = parts[1]
                        selected.append((sens, species_prop))
                        
                        if species_prop not in unique_dict:
                            unique_dict[species_prop] = True
            
            # Write to master file
            master_out.write(f"\nCase: {case_index}\n")
            master_out.write("Sensitivity\tSpecies_Property\n")
            
            for sens, species_prop in selected:
                master_out.write(f"{sens}\t{species_prop}\n")
    
    # Write unique species file
    sorted_unique = sorted(unique_dict.keys())
    
    with open(unique_file, 'w') as unique_out:
        unique_out.write("Species_Property\n")
        for species_prop in sorted_unique:
            unique_out.write(f"{species_prop}\n")
    
    print("Files generated successfully.")
    print(f"Master file: {master_file}")
    print(f"Unique file: {unique_file}")
    # -------- Create final species list (only core names) --------
    final_file = os.path.join(folder_path, "final_species_list.txt")

    core_species = sorted(set([sp.split('_')[0] for sp in sorted_unique]))

    with open(final_file, 'w') as final_out:
        final_out.write("[")
        final_out.write(", ".join(f'"{sp}"' for sp in core_species))
        final_out.write("]")

    print(f"Final species list: {final_file}")


# -------- RUN --------
folder_path = "/home/user/Desktop/Thermo+reaction_opt/RUN_C7H16/Sensitivity_analysis_m_heptane_v2/Thermo/SA/Data"
generate_master_and_unique_species(folder_path)

