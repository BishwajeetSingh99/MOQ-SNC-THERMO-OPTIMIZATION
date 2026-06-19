import os
import re

def generate_master_and_unique(folder_path):
    
    master_file = os.path.join(folder_path, "master_5%_reactions.txt")
    unique_file = os.path.join(folder_path, "unique_reactions_lists.txt")
    
    case_files = []
    
    # Collect case files with index
    for file in os.listdir(folder_path):
        if file.endswith(".txt") and "case_" in file:
            match = re.search(r'case_(\d+)', file)
            if match:
                case_index = int(match.group(1))
                case_files.append((case_index, file))
    
    # Sort serially by case index
    case_files.sort(key=lambda x: x[0])
    
    unique_dict = {}  # {reaction_no: reaction_eq}
    
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
                    if len(parts) < 3:
                        continue
                    
                    try:
                        sens = float(parts[0])
                    except ValueError:
                        continue
                    
                    if abs(sens) > 0.05:
                        rxn_no = parts[1]
                        rxn_eq = parts[2]
                        selected.append((sens, rxn_no, rxn_eq))
                        
                        # Store unique reactions
                        if rxn_no not in unique_dict:
                            unique_dict[rxn_no] = rxn_eq
            
            # Write case block to master file
            master_out.write(f"\nCase: {case_index}\n")
            master_out.write("Sensitivity\tReaction_No\tReaction\n")
            
            for sens, rxn_no, rxn_eq in selected:
                master_out.write(f"{sens}\t{rxn_no}\t{rxn_eq}\n")
    
    # Write unique reactions file
    sorted_unique = sorted(unique_dict.items(), key=lambda x: int(x[0]))
    
    with open(unique_file, 'w') as unique_out:
        unique_out.write("Reaction_No\tReaction\n")
        for rxn_no, rxn_eq in sorted_unique:
            unique_out.write(f"{rxn_no}\t{rxn_eq}\n")
    
    print("Files generated successfully.")
    print(f"Master file: {master_file}")
    print(f"Unique file: {unique_file}")
    # -------- Create unique reaction numbers list --------
    rxn_numbers_file = os.path.join(folder_path, "unique_rxn_numbers.txt")

    rxn_numbers = sorted([int(rxn_no) for rxn_no in unique_dict.keys()])

    with open(rxn_numbers_file, 'w') as f_out:
        f_out.write("[")
        f_out.write(", ".join(str(rxn) for rxn in rxn_numbers))
        f_out.write("]")

    print(f"Reaction numbers file: {rxn_numbers_file}")


# -------- RUN --------
folder_path = "/home/user/Desktop/Thermo+reaction_opt/RUN_C7H16/Sensitivity_analysis_m_heptane_v2/rxn/Data"
generate_master_and_unique(folder_path)

