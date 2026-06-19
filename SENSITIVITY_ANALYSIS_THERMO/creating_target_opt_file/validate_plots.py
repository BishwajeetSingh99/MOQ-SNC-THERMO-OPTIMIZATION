'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_ignition_delay(csv_file, output_file="ignition_delay.png"):
    # Read CSV
    df = pd.read_csv(csv_file)

    # Extract columns
    T = df["T"].values
    obs = df["Obs(us)"].values
    nom = df["Nominal"].values

    # X-axis as 1000/T
    x = 1000.0 / T

    # Sort nominal values for smooth curve
    order = np.argsort(x)
    x_nom, y_nom = x[order], nom[order]

    # Plot
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_yscale("log")

    # Nominal as curve
    ax.plot(x_nom, y_nom, "-", color="orange", linewidth=1.5, label="Nominal")

    # Obs as scatter
    ax.plot(x, obs, "x", color="black", markersize=6, label="Obs")

    # Labels
    ax.set_xlabel("1000/T, [1/K]", fontsize=12)
    ax.set_ylabel(r"$\tau_{ig}\; [\mu s]$", fontsize=12)

    # Axis limits (matching your reference style)
    ax.set_xlim(0.6, 1.6)
    ax.set_ylim(1e0, 1e5)  # since values are in µs, adjust range if needed

    # Grid
    ax.grid(which="major", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.minorticks_on()
    ax.grid(which="minor", linestyle=":", linewidth=0.4, alpha=0.5)

    # Legend
    ax.legend(frameon=False, fontsize=9)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.show()


# Example:
# plot_ignition_delay("01322afc-bdbb-47ce-9447-e747a8f8951f.csv", "plot.png")

plot_ignition_delay("/home/user/Desktop/butane_data/kerosean/kerosean_trial/plot/Dataset/Tig/all_tig_data.csv", "ig_plot.png")
'''


# use this when used V3 styyle, various csv files


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os,sys

def plot_ignition_delay(csv_file, output_file="ignition_delay.png"):
    # Read CSV
    df = pd.read_csv(csv_file)

    # Extract columns
    T = df["T"].values
    obs_us = df["Obs(us)"].values
    nom_us = df["Nominal"].values

    # Convert µs → ms
    obs = obs_us * 1e-4
    nom = nom_us * 1e-3


    # X-axis: 1000/T
    x = 1000.0 / T

    # Sort nominal for smooth curve
    order = np.argsort(x)
    x_nom, y_nom = x[order], nom[order]

    # Plot
    fig, ax = plt.subplots(figsize=(3, 3))
    #fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_yscale("log")

    # Nominal as smooth blue curve
    ax.plot(x_nom, y_nom, "-", color="blue", linewidth=1.8, label="Nominal")

    # Obs as scatter
    ax.plot(x, obs, "x", color="black", markersize=6, label="Obs")

    # Labels
    ax.set_xlabel("1000/T, [1/K]", fontsize=12)
    ax.set_ylabel(r"$\tau_{ig}\; [s]$", fontsize=12)

    # Axis limits (like reference figure)
    ax.set_xlim(0.8, 1.6)
    ax.set_ylim(1e0 , 1e3)

    # Grid
    ax.grid(which="major", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.minorticks_on()
    ax.grid(which="minor", linestyle=":", linewidth=0.4, alpha=0.5)

    # Legend
    ax.legend(frameon=False, fontsize=9)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    #plt.show()


# Example:
# plot_ignition_delay("01322afc-bdbb-47ce-9447-e747a8f8951f.csv", "plot.png")

plot_ignition_delay("/data2/RANA/FINAL_RUN_7nc/PROPNANE_SENSITIVITY/SENS_PROPANE/NOMINAL_SIMULATIONS_PROPANE/Plot/Dataset/Tig/x10001001.csv", "x10001001" )
plot_ignition_delay("/data2/RANA/FINAL_RUN_7nc/PROPNANE_SENSITIVITY/SENS_PROPANE/NOMINAL_SIMULATIONS_PROPANE/Plot/Dataset/Tig/x10001002.csv", "x10001002" )
plot_ignition_delay("/data2/RANA/FINAL_RUN_7nc/PROPNANE_SENSITIVITY/SENS_PROPANE/NOMINAL_SIMULATIONS_PROPANE/Plot/Dataset/Tig/x10001003.csv", "x10001003" )
plot_ignition_delay("/data2/RANA/FINAL_RUN_7nc/PROPNANE_SENSITIVITY/SENS_PROPANE/NOMINAL_SIMULATIONS_PROPANE/Plot/Dataset/Tig/x10001004.csv", "x10001004" )
plot_ignition_delay("/data2/RANA/FINAL_RUN_7nc/PROPNANE_SENSITIVITY/SENS_PROPANE/NOMINAL_SIMULATIONS_PROPANE/Plot/Dataset/Tig/x10001005.csv" , "x10001005")
plot_ignition_delay("/data2/RANA/FINAL_RUN_7nc/PROPNANE_SENSITIVITY/SENS_PROPANE/NOMINAL_SIMULATIONS_PROPANE/Plot/Dataset/Tig/x10001006.csv","x10001006" )

