import os
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ==========================================
# USER CONFIGURATION
# ==========================================
# List your 3 raw data files here
FILE_PATHS = [
    "FM_sensitivity_T_759_case_0.txt",  # Replace with actual path to file 1
    "FM_sensitivity_T_759_case_1.txt",  # Replace with actual path to file 2
    "FM_sensitivity_T_759_case_2.txt",  # Replace with actual path to file 3
]

# Provide a descriptive label for each file corresponding to the order above
# e.g., Pressure or Temperature values
CONDITION_LABELS = ["20.0", "30.0", "40.0"]
LEGEND_TITLE = "Pressure"  # Placeholder title for the legend

# Force certain species to be included in the plots regardless of top-5 status.
# Leave empty [] if you don't want to enforce anything.
MANDATORY_SPECIES = ["OH", "O2"]


# ==========================================
# DATA PARSING & PROCESSING
# ==========================================
def parse_sensitivity_file(file_path, condition_label):
    """Parses a Cantera sensitivity text file into a structured DataFrame."""
    data = []
    # Regex to extract numeric value and the compound trailing identifier (e.g., NC3H7_S)
    pattern = re.compile(r"^\s*(-?\d+\.\d+)\s+([A-Za-z0-9\-\*_]+)_([A-Za-z0-9]+)")

    if not os.path.exists(file_path):
        # Creating mock dataframe data if testing without all 3 physical files
        print(f"Warning: File {file_path} not found. Skipping.")
        return pd.DataFrame()

    with open(file_path, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                val = float(match.group(1))
                species = match.group(2)
                property_type = match.group(3)

                # Standardize common naming styles to match your image reference
                if species.startswith("NC3H7"):
                    species = "N-C3H7"
                elif species.startswith("IC3H7"):
                    species = "I-C3H7"
                elif "C3H6OOH" in species:
                    # Clean complex isomers down to base group for clean plotting
                    species = "C3H6OOH"

                data.append(
                    {
                        "Sensitivity": val,
                        "Species": species,
                        "Property": property_type,
                        "Condition": condition_label,
                    }
                )

    return pd.DataFrame(data)


# Combine all parsed datasets
all_data_list = []
for path, label in zip(FILE_PATHS, CONDITION_LABELS):
    df = parse_sensitivity_file(path, label)
    if not df.empty:
        all_data_list.append(df)

# Fallback generator for a mock template dataframe if local files aren't set up yet
if not all_data_list:
    raise FileNotFoundError(
        "Please update FILE_PATHS with actual paths to your sensitivity files."
    )

df_all = pd.concat(all_data_list, ignore_index=True)

# Define properties to plot sequentially
properties = ["cp", "H", "S"]

# Set up beautiful, clear publication styles
plt.rcParams.update(
    {
        "font.size": 14,
        "axes.labelsize": 16,
        "axes.titlesize": 18,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "figure.titlesize": 22,
    }
)

fig, axes = plt.subplots(
    nrows=3, ncols=1, figsize=(14, 18), dpi=300, sharex=False
)
fig.suptitle(
    f"Top Species Sensitivities ({', '.join(properties)})", y=0.98, weight="bold"
)

# Custom color palette matching your blue, orange, and green bars
custom_palette = sns.color_palette(["#1f77b4", "#ff7f0e", "#2ca02c"])

# ==========================================
# PLOTTING MAIN LOOP
# ==========================================
for i, prop in enumerate(properties):
    ax = axes[i]

    # Filter data for the specific thermo property (cp, H, S)
    df_prop = df_all[df_all["Property"].str.lower() == prop.lower()]

    if df_prop.empty:
        ax.text(
            0.5,
            0.5,
            f"No data found for Property: {prop}",
            ha="center",
            va="center",
        )
        continue

    # Determine Top 5 species based on maximum absolute sensitivity across all states
    top_species = (
        df_prop.groupby("Species")["Sensitivity"]
        .apply(lambda x: x.abs().max())
        .nlargest(5)
        .index.tolist()
    )

    # Append user-requested mandatory species if they aren't already captured in Top 5
    for mandatory in MANDATORY_SPECIES:
        if (
            mandatory in df_prop["Species"].unique()
            and mandatory not in top_species
        ):
            top_species.append(mandatory)

    # Filter data to include only selected species
    df_plot = df_prop[df_prop["Species"].isin(top_species)].copy()

    # Sort species so they cleanly display sequentially on the Y-Axis
    df_plot["Species"] = pd.Categorical(
        df_plot["Species"], categories=top_species, ordered=True
    )
    df_plot = df_plot.sort_values("Species")

    # Draw grouped horizontal barplot using Seaborn
    sns.barplot(
        data=df_plot,
        y="Species",
        x="Sensitivity",
        hue="Condition",
        ax=ax,
        palette=custom_palette,
        edgecolor="none",
    )

    # Styling and Labels
    ax.set_title(f"Sensitivity on {prop}", pad=10)
    ax.set_ylabel("Species", labelpad=10)
    ax.set_xlabel("Sensitivity", labelpad=10)
    ax.axvline(0, color="gray", linestyle="-", linewidth=0.8, alpha=0.7)

    # Clean layout tuning for individual subplots
    ax.legend(title=LEGEND_TITLE, loc="lower right", frameon=False)
    ax.spines["top"].set_visible(True)
    ax.spines["right"].set_visible(True)
    ax.tick_params(direction="out", length=6, width=1.5)

# Adjust design margins to eliminate overlapping text elements
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save high-resolution figure file
output_filename = "top_species_sensitivities.png"
plt.savefig(output_filename, bbox_inches="tight", dpi=300)
print(f"Success! High-resolution plot generated and saved as '{output_filename}'.")
plt.show()
