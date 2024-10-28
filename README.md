# Leakage Current Calculation for Digital Logic Circuits

This project is focused on calculating leakage currents for various digital logic gates (such as Inverter, NAND, NOR, AND, OR) and integrating them to form a Carry Lookahead Adder (CLA) and find its leakages. The code estimates leakage currents for different input combinations and writes the results to CSV files.

## Project Structure

1. **Leakage Data Files**:
   - Leakage data is organized into text files for NMOS and PMOS transistors with data based on states (e.g., on/off) and configurations (e.g., stacks).
   - Paths to leakage files are defined for NMOS and PMOS and are located in subdirectories `NMOS/Tables` and `PMOS/Tables`.

2. **Logic Gates**:
   - Functions are implemented to simulate logic gates (Inverter, AND2, AND3, AND4, OR3, OR4, NAND, NOR) using their respective transistor models.
   - Each function calculates subthreshold, gate, and body leakage, using data from leakage files.
   - Total leakage is calculated and printed in nanometers (nA).

3. **Carry Lookahead Adder (CLA)**:
   - Simulates a 4-bit CLA design based on generated logic gates.
   Each stage in the CLA (CNX, CNY, CNZ) and intermediate values are generated using logic gates, and their leakage values are summed to obtain total leakage.
   - The CLA function writes output (input values, calculated outputs, and leakage data) to `cla_leakage_data.csv`.

4. **Main Function**:
   - The `main` function iterates over all possible inputs for each logic gate and CLA adder.
   - Leakage data is calculated and saved in `leakage_data.csv` for gates and `cla_leakage_data.csv` for the CLA adder.
   - Provides a detailed breakdown of each gate's total leakage for different input combinations.

## Running the Code

Ensure the following directory structure and files are available:
   - `NMOS/Tables` and `PMOS/Tables` directories contain leakage data files.
   - `CLA_adder.sub` is a SPICE file used for the CLA adder's simulation.

### Key Files and Paths
- `nmos_path`: Path to NMOS leakage files.
- `pmos_path`: Path to PMOS leakage files.
- `base_dir`: Base directory for subcircuit files and output folder.
- `output_folder`: Directory for storing output files like `output.txt` and `total_leakage.csv`.

### Functions Overview
- `read_leakage_data`: Reads leakage data for NMOS and PMOS transistors from specified files.
- `get_transistor_leakage`: Retrieves leakage values (subthreshold, gate, body) based on transistor type, state, and output voltage.
- `calculate_[gate]_leakage`: Functions for each gate type (Inverter, NAND, NOR, AND2, AND3, AND4, OR3, OR4) that calculate and print total leakage.
- `CLA_adder`: Simulates the 4-bit CLA adder using logic gates and calculates total leakage.

### Output
The code generates the following output files:
- `leakage_data.csv`: Contains leakage data for all tested gates with various input combinations.
- `cla_leakage_data.csv`: Stores CLA adder results, including input combinations, outputs, and total leakage currents.

### Notes
- Ensure all paths and files are set correctly before running.
- Output leakage values are reported in nanometers (nA) for consistency and easy comparison.
