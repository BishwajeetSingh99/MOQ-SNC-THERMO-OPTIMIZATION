'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === CONFIG ===
file_path = "/home/user/Desktop/butane_data/kerosean/kerosean_trial/plot/Dataset/Tig/all_tig_data.csv"  # change this to your file path
output_plot = "obs_vs_nominal_lines.png"

# === READ FILE ===
df = pd.read_csv(file_path)
df = df.rename(columns={"Obs(us)": "Obs", "Nominal": "Nominal"})

# Sort by observed values (ascending)
df_sorted = df.sort_values(by="Obs", ascending=True).reset_index(drop=True)
df_sorted["Target_No"] = df_sorted.index + 1

# === PLOT ===
plt.figure(figsize=(10, 6))

# Blue line for Observed
plt.plot(df_sorted["Target_No"], df_sorted["Obs"], marker='o', color="blue", linestyle='-', linewidth=2, label="Observed (Experimental)")

# Green line for Nominal
plt.plot(df_sorted["Target_No"], df_sorted["Nominal"], marker='s', color="green", linestyle='-', linewidth=2, label="Nominal (Model)")

plt.xlabel("Target Number (sorted by Obs)")
plt.ylabel("Values (us)")
plt.title("Observed vs Nominal Values")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(output_plot, dpi=300)
plt.close()

# === ERROR METRICS ===
residuals = df_sorted["Nominal"] - df_sorted["Obs"]
relative_error = np.abs(residuals) / df_sorted["Obs"]

mean_relative_error = relative_error.mean()
max_residual_error = np.max(np.abs(residuals))
percent_error = (relative_error * 100).mean()

print(f"✅ Plot saved as: {output_plot}")
print(f"📊 Mean relative error: {mean_relative_error:.4f} ({mean_relative_error*100:.2f} %)")
print(f"📊 Max residual error: {max_residual_error:.4f}")
print(f"📊 Average % error: {percent_error:.2f} %")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === CONFIG ===
file_path = "1d3a4079-47ff-4f70-b285-ecc102f0ff9a.csv"  # change this to your file path
output_plot = "obs_vs_nominal_sorted.png"

# === READ FILE ===
df = pd.read_csv(file_path)
df = df.rename(columns={"Obs(us)": "Obs", "Nominal": "Nominal"})

# ✅ Sort by Obs in ascending order
df_sorted = df.sort_values(by="Obs", ascending=True).reset_index(drop=True)

# ✅ Assign new index for plotting (1, 2, 3, …)
x_idx = np.arange(1, len(df_sorted) + 1)

# === PLOT ===
plt.figure(figsize=(12, 6))

# Observed values (blue line)
plt.plot(x_idx, df_sorted["Obs"], marker='o', color="blue", linestyle='-', linewidth=2, label="Observed (Experimental)")

# Nominal values (green line)
plt.plot(x_idx, df_sorted["Nominal"], marker='s', color="green", linestyle='-', linewidth=2, label="Nominal (Model)")

plt.xlabel("Target Number (sorted by Obs)")
plt.ylabel("Values (us)")
plt.title("Observed vs Nominal Values (Sorted by Observed)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(output_plot, dpi=300)
plt.close()

# === ERROR METRICS ===
residuals = df_sorted["Nominal"] - df_sorted["Obs"]
relative_error = np.abs(residuals) / df_sorted["Obs"]

mean_relative_error = relative_error.mean()
max_residual_error = np.max(np.abs(residuals))
percent_error = (relative_error * 100).mean()

print(f"✅ Plot saved as: {output_plot}")
print(f"📊 Mean relative error: {mean_relative_error:.4f} ({mean_relative_error*100:.2f} %)")
print(f"📊 Max residual error: {max_residual_error:.4f}")
print(f"📊 Average % error: {percent_error:.2f} %")

'''






'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === CONFIG ===
file_path = "/home/user/Desktop/butane_data/kerosean/kerosean_trial/plot/Dataset/Tig/all_tig_data.csv"  # change this to your file path
output_plot = "obs_vs_nominal_logscale.png"

# === READ FILE ===
df = pd.read_csv(file_path)
df = df.rename(columns={"Obs(us)": "Obs", "Nominal": "Nominal"})

# ✅ Sort by Obs in ascending order
df_sorted = df.sort_values(by="Obs", ascending=True).reset_index(drop=True)

# ✅ Assign new index for plotting (1, 2, 3, …)
x_idx = np.arange(1, len(df_sorted) + 1)

# === CALCULATE ERRORS ===
df_sorted["Abs_Error"] = np.abs(df_sorted["Obs"] - df_sorted["Nominal"])
df_sorted["Percent_Error"] = (df_sorted["Abs_Error"] / df_sorted["Obs"]) * 100

# === SUMMARY STATS ===
mean_abs_error = df_sorted["Abs_Error"].mean()
max_abs_error = df_sorted["Abs_Error"].max()
mean_percent_error = df_sorted["Percent_Error"].mean()
max_percent_error = df_sorted["Percent_Error"].max()

print("=== ERROR SUMMARY ===")
print(f"📊 Mean Absolute Error: {mean_abs_error:.4f}")
print(f"📊 Max Absolute Error: {max_abs_error:.4f}")
print(f"📊 Mean % Error: {mean_percent_error:.2f} %")
print(f"📊 Max % Error: {max_percent_error:.2f} %")
print("=====================")

# === PLOT ===
plt.figure(figsize=(12, 6))

# Observed values (blue line)
plt.plot(x_idx, df_sorted["Obs"], marker='o', color="blue", linestyle='-', linewidth=2, label="Observed (Experimental)")

# Nominal values (green line)
plt.plot(x_idx, df_sorted["Nominal"], marker='s', color="green", linestyle='-', linewidth=2, label="Nominal (Model)")

plt.xlabel("Target Number (sorted by Obs)")
plt.ylabel("Values (us, log scale)")
plt.title("Observed vs Nominal Values (Sorted by Obs)")
plt.yscale("log")  # ✅ log scale
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(output_plot, dpi=300)
plt.close()

print(f"✅ Plot saved as: {output_plot}")
'''






import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === CONFIG ===
file_path = "/home/user/Desktop/butane_data/kerosean/kerosean_trial/all_targets/plot/Dataset/Tig/all_tig_data.csv"
sorted_csv = "sorted_targets.csv"
output_plot = "obs_vs_nominal_logscale.png"
top50_file = "top50_errors.txt"

# === READ ORIGINAL FILE ===
df = pd.read_csv(file_path)
df = df.rename(columns={"Obs(us)": "Obs", "Nominal": "Nominal"})

# ✅ Add original target numbers (from input order)
df["Target_No"] = np.arange(1, len(df) + 1)

# === SORT BY Obs (whole rows) ===
df_sorted = df.sort_values(by="Obs", ascending=True).reset_index(drop=True)
df_sorted["Sorted_Index"] = np.arange(1, len(df_sorted) + 1)

# === SAVE SORTED DATA ===
df_sorted.to_csv(sorted_csv, index=False)
print(f"✅ Sorted targets saved to {sorted_csv}")

# === PLOT USING SORTED FILE ===
plt.figure(figsize=(12, 6))

plt.plot(df_sorted["Sorted_Index"], df_sorted["Obs"], marker='o', color="blue",
         linestyle='-', linewidth=2, label="Observed (Experimental)")
plt.plot(df_sorted["Sorted_Index"], df_sorted["Nominal"], marker='s', color="green",
         linestyle='-', linewidth=2, label="Nominal (Model)")

plt.xlabel("Target Number (sorted by Obs)")
plt.ylabel("Values (us, log scale)")
plt.title("Observed vs Nominal Values (Sorted by Obs)")
plt.yscale("log")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(output_plot, dpi=300)
plt.close()

print(f"✅ Plot saved as: {output_plot}")

# === CALCULATE ABSOLUTE ERRORS ON ORIGINAL FILE ===
df["Abs_Error"] = np.abs(df["Nominal"] - df["Obs"])

# === TOP 50 TARGETS WITH HIGHEST ERROR (original file) ===
top_targets = df.nlargest(50, "Abs_Error")[["Target_No", "Obs", "Nominal", "Abs_Error"]]

# === SAVE TO TEXT FILE ===
with open(top50_file, "w") as f:
    f.write("Top 50 Targets with Highest Absolute Errors\n")
    f.write("="*60 + "\n")
    for _, row in top_targets.iterrows():
        f.write(f"Target {int(row['Target_No'])}: Obs={row['Obs']}, Nominal={row['Nominal']}, Abs_Error={row['Abs_Error']}\n")

print(f"✅ Top 50 targets with highest errors saved to {top50_file}")

