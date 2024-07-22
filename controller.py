import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import csv
import models
import models.ConvolutionLayer
import models.DenseLayer
import models.FlattenLayer
import models.GRULayer
import models.PoolingLayer


def save(input_height, input_width, input_channels, layer_frames, layers, configuration_name=None):
    # Get input values
    input_height_value = input_height.get()
    input_width_value = input_width.get()
    input_channels_value = input_channels.get()

    # Get layer configurations
    layer_configurations = []
    for frame in layers:
        layer_type = frame.layer_type
        entries = [entry for entry in frame.get_entries()]
        layer_configurations.append((layer_type, entries))

    # Load existing configurations
    existing_configurations = []
    try:
        with open("network_config.csv", mode="r", newline='') as file:
            reader = csv.reader(file)
            existing_configurations = [
                row[0] for row in reader if row and row[0].startswith("Configuration")]
    except FileNotFoundError:
        # File does not exist yet, which is fine for initial save
        pass

    # Determine configuration name
    if configuration_name:
        if configuration_name.startswith("Configuration"):
            configuration_header = configuration_name
        else:
            configuration_header = f"Configuration {configuration_name}"
    else:
        # Generate new configuration name
        configuration_base = "Configuration"
        configuration_count = 1
        existing_names = set(existing_configurations)

        while f"{configuration_base} {configuration_count}" in existing_names:
            configuration_count += 1

        configuration_header = f"{configuration_base} {configuration_count}"

    # Write data to CSV file
    with open("network_config.csv", mode="a", newline='') as file:
        writer = csv.writer(file)

        # Add a header for the new configuration
        writer.writerow([configuration_header])
        writer.writerow(["Input Height", input_height_value])
        writer.writerow(["Input Width", input_width_value])
        writer.writerow(["Input Channels", input_channels_value])

        # Write layer configurations
        for layer_type, entries in layer_configurations:
            writer.writerow([layer_type] + entries)

        writer.writerow([])  # Add an empty row for separation

    print("Data saved to network_config.csv file.")

# get from csv file
def load_configurations():
    configurations = []
    with open("network_config.csv", mode="r", newline='') as file:
        reader = csv.reader(file)
        current_configuration = {}
        for row in reader:
            if row:
                if row[0].startswith("Configuration"):
                    if current_configuration:
                        configurations.append(current_configuration)
                    # Extract the name without "Configuration"
                    name = row[0].replace("Configuration", "").strip()
                    current_configuration = {"name": name, "data": []}
                else:
                    current_configuration["data"].append(row)
        if current_configuration:
            configurations.append(current_configuration)
    return configurations

# put them in layers
def load_configuration_to_app(total_mac, total_mem, configuration, name_entry,  input_height, input_width, input_channels, results_display, layer_frames, layers,  layers_container, layer_canvas):
    # Clear previous configurations
    for frame in layer_frames:
        frame.destroy()
    layers.clear()

    # Load input values
    input_height.delete(0, tk.END)
    input_width.delete(0, tk.END)
    input_channels.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    input_height.insert(0, configuration["data"][0][1])
    input_width.insert(0, configuration["data"][1][1])
    input_channels.insert(0, configuration["data"][2][1])
    name_entry.insert(0, configuration["name"])

    # Load layer configurations
    for layer_data in configuration["data"][3:]:
        layer_type = layer_data[0]
        entries = layer_data[1:]
        add_layer(layer_type, layers_container, layer_frames,
                  layers, layer_canvas, *entries)

    # Display results
    calculate(total_mac, total_mem, input_height, input_width,
              input_channels, results_display, layer_frames, layers)
    #
    # results_display.delete("1.0", tk.END)
    # results_display.insert("1.0", configuration["data"][-1][0])

# clear and reset
def clear_configuration_and_display(total_mac, total_mem, name_entry, input_height, input_width, input_channels, results_display, layer_frames, layers,  layers_container):
    # Clear previous configurations
    for frame in layer_frames:
        frame.destroy()
    layers.clear()

    # clear input values
    input_height.delete(0, tk.END)
    input_width.delete(0, tk.END)
    input_channels.delete(0, tk.END)
    total_mac.delete(0, tk.END)
    total_mem.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    results_display.delete("1.0", tk.END)

# add layers
def add_layer(layer_type, layers_container, layer_frames, layers, layer_canvas, *values):
    layer = None  # Default value for layer
    layer_number = len(layers) + 1
    if layer_type == "convolution":
        layer = models.ConvolutionLayer.ConvolutionLayer(
            layers_container, values, layer_number, layers)
    elif layer_type == "pooling":
        layer = models.PoolingLayer.PoolingLayer(
            layers_container, values, layer_number, layers)
    elif layer_type == "dense":
        layer = models.DenseLayer.DenseLayer(
            layers_container, values, layer_number, layers)
    elif layer_type == "flatten":
        layer = models.FlattenLayer.FlattenLayer(
            layers_container, layer_number, layers)
    elif layer_type == "gru":
        layer = models.GRULayer.GRULayer(
            layers_container, values, layer_number, layers)

    if layer:  # Check if layer is defined
        layer_frames.append(layer.frame)
        layer.frame.layer_type = layer_type  # Add layer_type attribute to the frame
        # layer.frame.layer_number=layer_number
        layers.append(layer)

        # Update the scroll region
        layer_canvas.configure(scrollregion=layer_canvas.bbox("all"))
    else:
        print("Unsupported layer type:", layer_type)


# Function to calculate and display the values
def calculate(total_mac, total_mem, input_height, input_width, input_channels, results_display, layer_frames, layers):
    results_display.delete("1.0", tk.END)  # Clear previous results
    prev_output_height = int(input_height.get())  # Initial input size
    prev_output_width = int(input_width.get())
    prev_output_size = prev_output_height * prev_output_width
    prev_output_channels = int(input_channels.get())  # Initial input channels

    total_maccs = 0
    total_params = 0
    total_mems = 0

    for i, layer in enumerate(layers):
        layer_number = i + 1  # Layer numbering starts from 1
        entries = layer.get_entries()
        if layer.layer_type == "convolution":
            height = int(entries[0])
            width = int(entries[1])
            filters = int(entries[2])
            stride = int(entries[3])
            padding = entries[4]

            if padding == "same":
                output_height = prev_output_height
                output_width = prev_output_width
            else:
                padding = int (padding)
                output_height = (
                    (prev_output_height - height + 2 * padding) // stride) + 1
                output_width = (
                    (prev_output_width - width + 2 * padding) // stride) + 1
            output_channels = filters

            params = (height * width * prev_output_channels + 1) * filters
            activation = output_height * output_width * output_channels
            maccs = output_height * output_width * filters * height * width * prev_output_channels
            
            mem = prev_output_height * prev_output_width * prev_output_channels * height * width * filters+ (params + activation) #remove prev_output_size for parallel computing

            result_text = (f"Layer {layer_number} - Convolution Layer: \n Input Size: {prev_output_height}x{prev_output_width}x{prev_output_channels}, "
                           f"Filter Size: {height}x{width}, Filters: {
                               filters}, Stride: {stride}, Padding: {padding}, "
                           f"Output Size: {output_height}x{
                               output_width}x{output_channels}, "
                           f"MACCs: {maccs}, Params: {params}, Activation: {activation}, MEM: {mem}\n")
            results_display.insert(tk.END, result_text)

            prev_output_height = output_height
            prev_output_width = output_width
            prev_output_size = output_height * output_width
            prev_output_channels = output_channels

        elif layer.layer_type == "pooling":
            pool_size = int(entries[0])
            stride = int(entries[1])
            params = 0 
            maccs = 0
            mem = 0

            output_height = ((prev_output_height - pool_size) // stride) + 1
            output_width = ((prev_output_width - pool_size) // stride) + 1
            output_channels = prev_output_channels

            result_text = (f"Layer {layer_number} - Pooling Layer: \n Input Size: {prev_output_height}x{prev_output_width}x{prev_output_channels}, "
                           f"Pool Size: {pool_size}, Stride: {stride}, "
                           f"Output Size: {output_height}x{output_width}x{output_channels}\n")
            results_display.insert(tk.END, result_text)

            prev_output_height = output_height
            prev_output_width = output_width
            prev_output_size = output_height*output_width*output_channels

        elif layer.layer_type == "flatten":
            # Flatten the output
            prev_output_size = prev_output_height * prev_output_width * prev_output_channels
            prev_output_height = 1
            prev_output_width = 1
            params = 0 
            maccs = 0
            mem = 0
            result_text = (
                f"Layer {layer_number} - Flatten Layer: \n Input Size: {prev_output_size}\n")
            results_display.insert(tk.END, result_text)

        elif layer.layer_type == "dense":
            num_neurons = int(entries[0])
            params = (prev_output_size + 1) * num_neurons
            maccs = prev_output_size * num_neurons
            #mem = num_neurons + params  + prev_output_size #
            #  for parallel computing
            mem = (2*prev_output_size + 1) * num_neurons + num_neurons
            result_text = (f"Layer {layer_number} - Dense Layer: \n Input Size: {prev_output_size}, Neurons: {num_neurons}, "
                           f"MACCs: {maccs}, Params: {params}, MEM: {mem}, Activation: {num_neurons}\n")
            results_display.insert(tk.END, result_text)
            prev_output_size = num_neurons  # Update for the next layer

        # elif layer.layer_type == "gru":
        #     units = int(entries[0])
        #     return_sequences = entries[1]
        #     # return_sequences = return_sequences.get()  # Get the boolean value

        #     # 3 matrices per gate, i.e., update gate, reset gate, and new memory gate
        #     params = 3 * (prev_output_size + units) * units
        #     maccs = prev_output_size * units
        #     mem = units + params + prev_output_size #remove prev_output_size for parallel computing
        #     result_text = (f"Layer {layer_number} - GRU Layer: \n Input Size: {prev_output_size}, Units: {units}, "
        #                    f"MACCs: {maccs}, Params: {params}, MEM: {mem}, Return Sequences: {return_sequences}\n")
        #     results_display.insert(tk.END, result_text)
        #     # Update for the next layer
        #     prev_output_size = units if not return_sequences else prev_output_size

        # Accumulate totals
        #print(i, params , "\n")#debugging
        total_maccs += maccs
        total_params += params
        total_mems += mem

    # Display total results
    total_text = (f"Total MACCs: {total_maccs}, Total Params: {
                  total_params}, Total MEM: {total_mems}\n")
    results_display.insert(tk.END, total_text)
    total_mac.delete(0, tk.END)
    total_mem.delete(0, tk.END)
    total_mac.insert(0, total_maccs)
    total_mem.insert(0, total_mems)


# Energy values dictionary based on the table
energy_values = {
    '45nm': {
        'Int8': {'add': 0.03, 'mul': 0.2},
        'Int32': {'add': 0.1, 'mul': 3.1},
        'BFloat16': {'add': None, 'mul': None},  # No values for 45nm
        'FP16': {'add': 0.4, 'mul': 1.1},
        'FP32': {'add': 0.9, 'mul': 3.7},
        'SRAM': {'8KB SRAM': 10, '32KB SRAM': 20, '1MB SRAM': 100}
    },
    '7nm': {
        'Int8': {'add': 0.007, 'mul': 0.07},
        'Int32': {'add': 0.03, 'mul': 1.48},
        'BFloat16': {'add': 0.11, 'mul': 0.21},
        'FP16': {'add': 0.16, 'mul': 0.34},
        'FP32': {'add': 0.38, 'mul': 1.31},
        'SRAM': {'8KB SRAM': 7.5, '32KB SRAM': 8.5, '1MB SRAM': 14}
    }
}


def energy(total_mac, total_mem, layer_vartech, layer_varprecision, layer_varbits, layer_varmemory_type, energy_out, energy_per_mac, energy_per_mem, tot_mac_energy, tot_mem_energy, results_display, root):
    tech = layer_vartech.get()
    precision = layer_varprecision.get()
    bits = layer_varbits.get()
    mem_type = layer_varmemory_type.get()
    energy_per_mac_value=float(energy_per_mac.get())
    energy_per_mem_value=float(energy_per_mem.get())

    # Determine the key for energy values lookup
    # if precision == "Fixed Point":
    #     if bits == "8":
    #         key = 'Int8'
    #     elif bits == "32":
    #         key = 'Int32'
    # elif precision == "Floating Point":
    #     if bits == "16":
    #         key = 'FP16'
    #     elif bits == "32":
    #         key = 'FP32'
    #     elif bits == "BFloat16":
    #         key = 'BFloat16'

    # # Fetch the energy values from the dictionary
    # energy_per_mac_value = energy_values[tech].get(key, {}).get(
    #     'add', 0) + energy_values[tech].get(key, {}).get('mul', 0)
    # energy_per_mac_value = round(energy_per_mac_value, 3)
    # energy_per_mem_value = energy_values[tech]['SRAM'].get(mem_type, 0)

    total_maccs = float(total_mac)
    total_mems = float(total_mem)

    energy_mac = round(energy_per_mac_value * total_maccs, 3)
    energy_mem = round(energy_per_mem_value * total_mems, 3)
    total_energy = round(energy_mac + energy_mem, 3)

    energy_out.delete(0, tk.END)
    energy_out.insert(tk.END, total_energy)
    tot_mem_energy.delete(0, tk.END)
    tot_mem_energy.insert(tk.END, energy_mem)
    tot_mac_energy.delete(0, tk.END)
    tot_mac_energy.insert(tk.END, energy_mac)
    # energy_per_mac.delete(0, tk.END)
    # energy_per_mac.insert(tk.END, energy_per_mac_value)
    # energy_per_mem.delete(0, tk.END)
    # energy_per_mem.insert(tk.END, energy_per_mem_value)
    # keep info
    results_display.insert(tk.END, f"--------------------\n")
    results_display.insert(tk.END, f"Technology: {tech}\n")
    results_display.insert(tk.END, f"Precision: {precision}\n")
    results_display.insert(tk.END, f"Bits: {bits}\n")
    results_display.insert(tk.END, f"Memory Type: {mem_type}\n")
    results_display.insert(tk.END, f"Total Energy for MAC Operations (pJ): {energy_mac}\n")
    results_display.insert(tk.END, f"Total Energy for Memory Operations (pJ): {energy_mem}\n")
    results_display.insert(tk.END, f"Total Inference Energy (pJ): {total_energy}\n")

    # Call show_graph with the calculated data
    #show_graph(root, total_maccs, total_energy)

def show_graph(root, total_maccs_str, total_energy_str, total_mem_str):
    try:
        total_maccs = int(total_maccs_str)
    except ValueError:
        try:
            total_maccs = float(total_maccs_str)
        except ValueError:
            print(f"Invalid total_maccs value: {total_maccs_str}")
            return

    try:
        total_energy = int(total_energy_str)
    except ValueError:
        try:
            total_energy = float(total_energy_str)
        except ValueError:
            print(f"Invalid total_energy value: {total_energy_str}")
            return

    try:
        total_mem = int(total_mem_str)
    except ValueError:
        try:
            total_mem = float(total_mem_str)
        except ValueError:
            print(f"Invalid total_mem value: {total_mem_str}")
            return

    # Create a new Tkinter window
    graph_window = tk.Toplevel(root)
    graph_window.title("Energy Consumption Graph")

    # Create a figure and a plot
    fig, ax = plt.subplots()
    ax.bar(['Tot MAC Consumption', 'Tot Energy', 'Tot MEM Consumption'],
           [total_maccs, total_energy, total_mem], color=['blue', 'red', 'green'])
    ax.set_title("Energy Consumption Analysis")
    ax.set_ylabel("Values (pJ)")

    # Create a canvas to embed the figure
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Create a toolbar for the canvas
    toolbar = ttk.Frame(graph_window)
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def dynamic_power(height, width, channels, sample_rate, energy, dynamic_power):
    sample_rate_value = float(sample_rate.get())
    energy_value = float(energy.get())
    height_value = float(height.get())
    width_value = float(width.get())
    channels_value = float(channels.get())
    nbr_input = height_value*width_value*channels_value
    # dynamic_power_value=energy_value*sample_rate_value
    dynamic_power_value = (energy_value/nbr_input)*sample_rate_value
    dynamic_power.delete(0, tk.END)
    dynamic_power.insert(tk.END, dynamic_power_value)

def update_power_consumption(layer_vartech, layer_varprecision, layer_varbits, layer_varmemory_type,energy_per_mac, energy_per_mem):
    tech = layer_vartech.get()
    precision = layer_varprecision.get()
    bits = layer_varbits.get()
    mem_type = layer_varmemory_type.get()

    # Determine the key for energy values lookup
    if precision == "Fixed Point":
        if bits == "8":
            key = 'Int8'
        elif bits == "32":
            key = 'Int32'
    elif precision == "Floating Point":
        if bits == "16":
            key = 'FP16'
        elif bits == "32":
            key = 'FP32'
        elif bits == "BFloat16":
            key = 'BFloat16'

    # Fetch the energy values from the dictionary
    energy_per_mac_value = energy_values[tech].get(key, {}).get(
        'add', 0) + energy_values[tech].get(key, {}).get('mul', 0)
    energy_per_mac_value = round(energy_per_mac_value, 3)
    energy_per_mem_value = energy_values[tech]['SRAM'].get(mem_type, 0)
    energy_per_mac.delete(0, tk.END)
    energy_per_mac.insert(tk.END, energy_per_mac_value)
    energy_per_mem.delete(0, tk.END)
    energy_per_mem.insert(tk.END, energy_per_mem_value)
