import os
import pandas as pd
import numpy as np
import csv

nmos_path = r"C:\Users\raaga\OneDrive\Desktop\Eval3_Final\Eval3_Final\NMOS\Tables"
pmos_path = r"C:\Users\raaga\OneDrive\Desktop\Eval3_Final\Eval3_Final\PMOS\Tables"

base_dir = r"C:\Users\raaga\OneDrive\Desktop\Eval3_Final\Eval3_Final\ngspice"
template_file = os.path.join(base_dir, 'CLA_adder.sub')
output_folder = os.path.join(base_dir, 'writings')

# Ensure the output folder exists   
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_main_file = os.path.join(output_folder, 'output.txt')
output_leakage_file = os.path.join(output_folder, 'total_leakage.csv')

# Mapping of transistor types and states to corresponding text file paths
leakage_data_files = {
    ('nmos', 'on'): os.path.join(nmos_path, 'NMOS_ON_W1.txt'),
    ('nmos', 'off'): os.path.join(nmos_path, 'NMOS_OFF_W1.txt'),
    ('pmos', 'on'): os.path.join(pmos_path, 'PMOS_ON_W1.txt'),
    ('pmos', 'off'): os.path.join(pmos_path, 'PMOS_OFF_W1.txt'),
    # Stack files for gates that use stacks
    ('nmos', '00'): os.path.join(nmos_path, 'NMOS_Stack_00_W1.txt'),
    ('nmos', '01'): os.path.join(nmos_path, 'NMOS_Stack_01_W1.txt'),
    ('nmos', '10'): os.path.join(nmos_path, 'NMOS_Stack_10_W1.txt'),
    ('nmos', '11'): os.path.join(nmos_path, 'NMOS_Stack_11_W1.txt'),
    ('pmos', '00'): os.path.join(pmos_path, 'PMOS_Stack_00_W1.txt'),
    ('pmos', '01'): os.path.join(pmos_path, 'PMOS_Stack_01_W1.txt'),
    ('pmos', '10'): os.path.join(pmos_path, 'PMOS_Stack_10_W1.txt'),
    ('pmos', '11'): os.path.join(pmos_path, 'PMOS_Stack_11_W1.txt'),
}

def read_leakage_data():
    leakage_data = {}
    for key, file_name in leakage_data_files.items():
        if os.path.exists(file_name):
            data = pd.read_csv(file_name, sep=r'\s+')
            leakage_data[key] = data
        else:
            print(f"Leakage data file {file_name} not found.")
    return leakage_data

leakage_data = read_leakage_data()

def get_transistor_leakage(np_type, state, vout):
    key = (np_type, state)
    data = leakage_data.get(key)

    if data is None:
        print(f"No data available for {np_type} in state {state}")
        return None

    # Choose the correct voltage column based on transistor type
    if np_type == 'nmos':
        voltage_column = 'V(drain)'
    elif np_type == 'pmos':
        voltage_column = 'V(source)'
    else:
        print(f"Unknown transistor type: {np_type}")
        return None

    # Find the row with voltage closest to vout
    data['voltage_diff'] = abs(data[voltage_column] - vout)
    min_voltage_diff = data['voltage_diff'].min()
    row = data.loc[data['voltage_diff'] == min_voltage_diff].iloc[0]

    # Remove the temporary column
    data.drop(columns=['voltage_diff'], inplace=True)

    # Extract leakage currents
    subthreshold_leakage = row['I(Vd)']
    gate_leakage = row['I(Vg)']
    body_leakage = row['I(Vb)']

    return subthreshold_leakage, gate_leakage, body_leakage

def calculate_inverter_leakage(input_value):
    global total_subthreshold_leakage, total_gate_leakage, total_body_leakage, total_leakage

    print(f"\nCalculating leakage for Inverter with input {input_value}")

    if input_value == 0:
        nmos_state = 'off'
        pmos_state = 'on'
        vout = 1.1
    else:
        nmos_state = 'on'
        pmos_state = 'off'
        vout = 0.0

    # NMOS leakage currents
    nmos_leakages = get_transistor_leakage('nmos', nmos_state, vout)
    if nmos_leakages is None:
        return 0
    nmos_sub, nmos_gate, nmos_body = nmos_leakages

    # PMOS leakage currents
    pmos_leakages = get_transistor_leakage('pmos', pmos_state, vout)
    if pmos_leakages is None:
        return 0
    pmos_sub, pmos_gate, pmos_body = pmos_leakages

    # Initialize total leakages
    total_subthreshold_leakage = 0
    total_gate_leakage = 0
    total_body_leakage = 0

    # NMOS leakage contributions
    if nmos_state == 'off':
        total_subthreshold_leakage += abs(nmos_sub)
    total_gate_leakage += abs(nmos_gate)
    total_body_leakage += abs(nmos_body)

    # PMOS leakage contributions
    if pmos_state == 'off':
        total_subthreshold_leakage += abs(pmos_sub)
    total_gate_leakage += abs(pmos_gate)
    total_body_leakage += abs(pmos_body)

    # Sum total leakage
    total_leakage = total_subthreshold_leakage + total_gate_leakage + total_body_leakage

    # Convert to nA
    total_subthreshold_leakage *= 1e9
    total_gate_leakage *= 1e9
    total_body_leakage *= 1e9
    total_leakage *= 1e9

    print(f"Total Subthreshold Leakage: {total_subthreshold_leakage:.2f} nA")
    print(f"Total Gate Leakage: {total_gate_leakage:.2f} nA")
    print(f"Total Body Leakage: {total_body_leakage:.2f} nA")
    print(f"Total Leakage Current: {total_leakage:.2f} nA")

    return total_leakage

def get_nmos_stack_leakage(state, vout):
    key = ('nmos', state)
    data = leakage_data.get(key)

    if data is None:
        print(f"No data available for NMOS stack in state {state}")
        return None

    voltage_column = 'V(drain1)'

    # Find the row with voltage closest to vout
    data['voltage_diff'] = abs(data[voltage_column] - vout)
    min_voltage_diff = data['voltage_diff'].min()
    row = data.loc[data['voltage_diff'] == min_voltage_diff].iloc[0]
    data.drop(columns=['voltage_diff'], inplace=True)

    # Sum I(Vd) and I(Vd2) for total subthreshold leakage
    subthreshold_leakage = row['I(Vd)'] + row['I(Vd2)']
    gate_leakage = row['I(Vg1)'] + row['I(Vg2)']
    body_leakage = row['I(Vb1)'] + row['I(Vb2)']

    return subthreshold_leakage, gate_leakage, body_leakage

def get_pmos_stack_leakage(state, vout):
    key = ('pmos', state)
    data = leakage_data.get(key)

    if data is None:
        print(f"No data available for PMOS stack in state {state}")
        return None

    voltage_column = 'V(source1)'

    # Find the row with voltage closest to vout
    data['voltage_diff'] = abs(data[voltage_column] - vout)
    min_voltage_diff = data['voltage_diff'].min()
    row = data.loc[data['voltage_diff'] == min_voltage_diff].iloc[0]
    data.drop(columns=['voltage_diff'], inplace=True)

    # Sum I(Vnet) and I(Vd2) for total subthreshold leakage
    subthreshold_leakage = row['I(Vnet)'] + row['I(Vd2)']
    gate_leakage = row['I(Vg1)'] + row['I(Vg2)']
    body_leakage = row['I(Vb1)'] + row['I(Vb2)']

    return subthreshold_leakage, gate_leakage, body_leakage


def calculate_nand_leakage(input_a, input_b):
    print(f"\nCalculating leakage for NAND gate with inputs A={input_a}, B={input_b}")

    # Determine output voltage
    if input_a == 1 and input_b == 1:
        vout = 0.0  # Output is low
    else:
        vout = 1.1  # Output is high

    total_subthreshold_leakage = 0
    total_gate_leakage = 0
    total_body_leakage = 0

    # PMOS transistors in parallel
    for input_value in [input_a, input_b]:
        pmos_state = 'on' if input_value == 0 else 'off'
        pmos_leakages = get_transistor_leakage('pmos', pmos_state, vout)
        if pmos_leakages is None:
            return 0
        p_sub, p_gate, p_body = map(abs, pmos_leakages)
        if pmos_state == 'off':
            total_subthreshold_leakage += p_sub
        total_gate_leakage += p_gate
        total_body_leakage += p_body

    # NMOS transistors in series (stack)
    nmos_stack_state = f"{input_a}{input_b}"
    nmos_leakages = get_nmos_stack_leakage(nmos_stack_state, vout)
    if nmos_leakages is None:
        return 0
    n_sub, n_gate, n_body = map(abs, nmos_leakages)
    if vout == 1.1:
        # When output is high, NMOS stack is OFF
        total_subthreshold_leakage += n_sub
    total_gate_leakage += n_gate
    total_body_leakage += n_body

    total_leakage = total_subthreshold_leakage + total_gate_leakage + total_body_leakage

    # Convert to nA
    total_subthreshold_leakage *= 1e9
    total_gate_leakage *= 1e9
    total_body_leakage *= 1e9
    total_leakage *= 1e9

    print(f"Total Subthreshold Leakage: {total_subthreshold_leakage:.2f} nA")
    print(f"Total Gate Leakage: {total_gate_leakage:.2f} nA")
    print(f"Total Body Leakage: {total_body_leakage:.2f} nA")
    print(f"Total Leakage Current: {total_leakage:.2f} nA")

    return total_leakage


def calculate_nor_leakage(input_a, input_b):
    print(f"\nCalculating leakage for NOR gate with inputs A={input_a}, B={input_b}")

    # Determine output voltage
    if input_a == 0 and input_b == 0:
        vout = 1.1  # Output is high
    else:
        vout = 0.0  # Output is low

    total_subthreshold_leakage = 0
    total_gate_leakage = 0
    total_body_leakage = 0

    # PMOS transistors in series (stack)
    pmos_stack_state = f"{int(input_a == 0)}{int(input_b == 0)}"
    pmos_leakages = get_pmos_stack_leakage(pmos_stack_state, vout)
    if pmos_leakages is None:
        return 0
    p_sub, p_gate, p_body = map(abs, pmos_leakages)
    if vout == 0.0:
        # When output is low, PMOS stack is OFF
        total_subthreshold_leakage += p_sub
    total_gate_leakage += p_gate
    total_body_leakage += p_body

    # NMOS transistors in parallel
    for input_value in [input_a, input_b]:
        nmos_state = 'on' if input_value == 1 else 'off'
        nmos_leakages = get_transistor_leakage('nmos', nmos_state, vout)
        if nmos_leakages:
            n_sub, n_gate, n_body = map(abs, nmos_leakages)
            if nmos_state == 'off':
                total_subthreshold_leakage += n_sub
            total_gate_leakage += n_gate
            total_body_leakage += n_body

    total_leakage = total_subthreshold_leakage + total_gate_leakage + total_body_leakage

    # Convert to nA
    total_subthreshold_leakage *= 1e9
    total_gate_leakage *= 1e9
    total_body_leakage *= 1e9
    total_leakage *= 1e9

    print(f"Total Subthreshold Leakage: {total_subthreshold_leakage:.2f} nA")
    print(f"Total Gate Leakage: {total_gate_leakage:.2f} nA")
    print(f"Total Body Leakage: {total_body_leakage:.2f} nA")
    print(f"Total Leakage Current: {total_leakage:.2f} nA")

    return total_leakage

def calculate_and2_leakage(input_a, input_b):
    print(f"\nCalculating leakage for AND2 gate with inputs A={input_a}, B={input_b}")

    # NAND gate output
    nand_output = int(not (input_a and input_b))

    # Inverter output (AND gate output)
    and_output = int(not nand_output)

    # Calculate leakage for NAND gate
    leakage_nand = calculate_nand_leakage(input_a, input_b)

    # Calculate leakage for inverter
    leakage_inv = calculate_inverter_leakage(nand_output)

    # Sum leakages
    total_leakage = leakage_nand + leakage_inv
    print(f"Total Leakage for AND2 gate: {total_leakage:.2f} nA")

    return total_leakage

def calculate_and3_leakage(input_a, input_b, input_c):
    print(f"\nCalculating leakage for AND3 gate with inputs A={input_a}, B={input_b}, C={input_c}")

    # NOR gate output
    nor_output = int(not (input_a or input_b))

    # Inverter output
    inv_output = int(not input_c)

    # NAND gate inputs
    nand_input_a = nor_output
    nand_input_b = inv_output

    # NAND gate output (AND3 gate output)
    and3_output = int(not (nand_input_a and nand_input_b))

    # Calculate leakage for NOR gate
    leakage_nor = calculate_nor_leakage(input_a, input_b)

    # Calculate leakage for inverter
    leakage_inv = calculate_inverter_leakage(input_c)

    # Calculate leakage for NAND gate
    leakage_nand = calculate_nand_leakage(nand_input_a, nand_input_b)

    # Sum leakages
    total_leakage = leakage_nor + leakage_inv + leakage_nand
    print(f"Total Leakage for AND3 gate: {total_leakage:.2f} nA")

    return total_leakage

def calculate_and4_leakage(input_a, input_b, input_c, input_d):
    print(f"\nCalculating leakage for AND4 gate with inputs A={input_a}, B={input_b}, C={input_c}, D={input_d}")

    # NAND gate outputs
    nand1_output = int(not (input_a and input_b))
    nand2_output = int(not (input_c and input_d))

    # NOR gate input
    nor_input_a = nand1_output
    nor_input_b = nand2_output

    # AND4 output
    and4_output = int(not (nor_input_a or nor_input_b))

    # Calculate leakage for NAND gates
    leakage_nand1 = calculate_nand_leakage(input_a, input_b)
    leakage_nand2 = calculate_nand_leakage(input_c, input_d)

    # Calculate leakage for NOR gate
    leakage_nor = calculate_nor_leakage(nand1_output, nand2_output)

    # Sum leakages
    total_leakage = leakage_nand1 + leakage_nand2 + leakage_nor
    print(f"Total Leakage for AND4 gate: {total_leakage:.2f} nA")

    return total_leakage

def calculate_or3_leakage(input_a, input_b, input_c):
    print(f"\nCalculating leakage for OR3 gate with inputs A={input_a}, B={input_b}, C={input_c}")

    # NAND gate output
    nand_output = int(not (input_a and input_b))

    # Inverter output
    inv_output = int(not input_c)

    # NOR gate input
    nor_input_a = nand_output
    nor_input_b = inv_output

    # OR3 output
    or3_output = int(not (nor_input_a or nor_input_b))

    # Calculate leakage for NAND gate
    leakage_nand = calculate_nand_leakage(input_a, input_b)

    # Calculate leakage for inverter
    leakage_inv = calculate_inverter_leakage(input_c)

    # Calculate leakage for NOR gate
    leakage_nor = calculate_nor_leakage(nand_output, inv_output)

    # Sum leakages
    total_leakage = leakage_nand + leakage_inv + leakage_nor
    print(f"Total Leakage for OR3 gate: {total_leakage:.2f} nA")

    return total_leakage

def calculate_or4_leakage(input_a, input_b, input_c, input_d):
    print(f"\nCalculating leakage for OR4 gate with inputs A={input_a}, B={input_b}, C={input_c}, D={input_d}")

    # NOR gate outputs
    nor1_output = int(not (input_a or input_b))
    nor2_output = int(not (input_c or input_d))

    # NAND gate input
    nand_input_a = nor1_output
    nand_input_b = nor2_output

    # OR4 output
    or4_output = int(not (nand_input_a and nand_input_b))

    # Calculate leakage for NOR gates
    leakage_nor1 = calculate_nor_leakage(input_a, input_b)
    leakage_nor2 = calculate_nor_leakage(input_c, input_d)

    # Calculate leakage for NAND gate
    leakage_nand = calculate_nand_leakage(nor1_output, nor2_output)

    # Sum leakages
    total_leakage = leakage_nor1 + leakage_nor2 + leakage_nand
    print(f"Total Leakage for OR4 gate: {total_leakage:.2f} nA")

    return total_leakage


def main():
    output_folder = "/Users/rishabhpatnaik/Documents/IIITH/Academic/THIRD YEAR/SEM1/COURSES/Digital VLSI Design/Project/Project 1/Eval3"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "leakage_data.csv")
    headers = ["Gate Type", "Input(s)", "Total Subthreshold Leakage (nA)", "Total Gate Leakage (nA)", "Total Body Leakage (nA)", "Total Leakage (nA)"]

    # Write headers to file if not present
    write_headers = not os.path.exists(output_file) or os.path.getsize(output_file) == 0
    if write_headers:
        with open(output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    total_leakage_for_all_inputs = 0

    # Test inverter
    for input_value in [0, 1]:
        total_leakage = calculate_inverter_leakage(input_value)
        total_leakage_for_all_inputs += total_leakage

        # Append results to CSV file
        with open(output_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Inverter",
                f"{input_value}",
                f"{total_subthreshold_leakage:.2f}",
                f"{total_gate_leakage:.2f}",
                f"{total_body_leakage:.2f}",
                f"{total_leakage:.2f}"
            ])

    # Test NAND gate
    for input_a in [0, 1]:
        for input_b in [0, 1]:
            total_leakage = calculate_nand_leakage(input_a, input_b)
            total_leakage_for_all_inputs += total_leakage

            # Append results to CSV file
            with open(output_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "NAND",
                    f"{input_a}{input_b}",
                    f"{total_subthreshold_leakage:.2f}",
                    f"{total_gate_leakage:.2f}",
                    f"{total_body_leakage:.2f}",
                    f"{total_leakage:.2f}"
                ])
   
    print(f"Leakage data saved to {output_file}")

    # Test NOR gate
    for input_a in [0, 1]:
        for input_b in [0, 1]:
            total_leakage = calculate_nor_leakage(input_a, input_b)
            total_leakage_for_all_inputs += total_leakage

            # Append results to CSV file
            with open(output_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "NOR",
                    f"{input_a}{input_b}",
                    f"{total_subthreshold_leakage:.2f}",
                    f"{total_gate_leakage:.2f}",
                    f"{total_body_leakage:.2f}",
                    f"{total_leakage:.2f}"
                ])
    
    # Test for AND2
    for input_a in [0, 1]:
        for input_b in [0, 1]:
            total_leakage = calculate_and2_leakage(input_a, input_b)
            total_leakage_for_all_inputs += total_leakage

            # Append results to CSV file
            with open(output_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "AND2",
                    f"{input_a}{input_b}",
                    f"{total_subthreshold_leakage:.2f}",
                    f"{total_gate_leakage:.2f}",
                    f"{total_body_leakage:.2f}",
                    f"{total_leakage:.2f}"
                ])   

    # Test for AND3
    for input_a in [0, 1]:
        for input_b in [0, 1]:
            for input_c in [0, 1]:
                total_leakage = calculate_and3_leakage(input_a, input_b, input_c)
                total_leakage_for_all_inputs += total_leakage

                # Append results to CSV file
                with open(output_file, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        "AND3",
                        f"{input_a}{input_b}{input_c}",
                        f"{total_subthreshold_leakage:.2f}",
                        f"{total_gate_leakage:.2f}",
                        f"{total_body_leakage:.2f}",
                        f"{total_leakage:.2f}"
                    ])

    # Test for AND4
    for input_a in [0, 1]:
        for input_b in [0, 1]:
            for input_c in [0, 1]:
                for input_d in [0, 1]:
                    total_leakage = calculate_and4_leakage(input_a, input_b, input_c, input_d)
                    total_leakage_for_all_inputs += total_leakage

                    # Append results to CSV file
                    with open(output_file, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            "AND4",
                            f"{input_a}{input_b}{input_c}{input_d}",
                            f"{total_subthreshold_leakage:.2f}",
                            f"{total_gate_leakage:.2f}",
                            f"{total_body_leakage:.2f}",
                            f"{total_leakage:.2f}"
                        ])

    # Test for OR3
    for input_a in [0, 1]:
        for input_b in [0, 1]:
            for input_c in [0, 1]:
                total_leakage = calculate_or3_leakage(input_a, input_b, input_c)
                total_leakage_for_all_inputs += total_leakage

                # Append results to CSV file
                with open(output_file, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        "OR3",
                        f"{input_a}{input_b}{input_c}",
                        f"{total_subthreshold_leakage:.2f}",
                        f"{total_gate_leakage:.2f}",
                        f"{total_body_leakage:.2f}",
                        f"{total_leakage:.2f}"
                    ])

    # Test for OR4
    for input_a in [0, 1]:
        for input_b in [0, 1]:
            for input_c in [0, 1]:
                for input_d in [0, 1]:
                    total_leakage = calculate_or4_leakage(input_a, input_b, input_c, input_d)
                    total_leakage_for_all_inputs += total_leakage

                    # Append results to CSV file
                    with open(output_file, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            "OR4",
                            f"{input_a}{input_b}{input_c}{input_d}",
                            f"{total_subthreshold_leakage:.2f}",
                            f"{total_gate_leakage:.2f}",
                            f"{total_body_leakage:.2f}",
                            f"{total_leakage:.2f}"
                        ])

# Run the main function to calculate leakage
main()
