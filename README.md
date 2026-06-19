# MOQ-SNC-THERMO-OPTIMIZATION

Temperature-dependent optimization framework for thermodynamic parameters in chemical kinetic mechanisms using Polynomial Response Surfaces (PRS) and Genetic Algorithm (GA).

## Workflow

Step 0: Compile shared libraries
- Compile all required *.so files for your system.

Step 1: Convert CHEMKIN to YAML
Example:
ck2yaml --input=chem.inp --thermo=therm.dat --transport=tran.dat --permissive

Example:
ck2yaml --input=MB_MB2D.inp --thermo=MB+MB2D_therm.dat --transport=Mb+MB2d_trans.dat --permissive

Step 2: Generate XML files
- Generate XML files for spoecies considered in the Senstivity Analysis.

Step 3: Prepare input files
- Target file
- Addendum file
- Mechanism files:
    * mech.yaml
    * therm.dat
    * tran.dat

Step 4: Run simulations

Optimization:
python3.9 MUQ-SNC/run_script.py [target_file]

Nominal simulations:
python3.9 MUQ-SNC/run_nominal_sim.py [target_file]

Sensitivity analysis:
python3.9 SENSITIVITY_ANALYSIS/sens.py [target_file]

## Repository Structure

MOQ-SNC-THERMO-OPTIMIZATION/
├── MUQ-SNC/
├── SENSITIVITY_ANALYSIS/
├── Nominal_Simulations/
└── README.txt
