import tkinter as tk
from tkinter import ttk
import controller
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_graph():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Example plot
    ax.set_title('Example Graph')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def load_configurations_and_display(total_mac, total_mem, name_entry, input_height, input_width, input_channels, results_display, layer_frames, layers, layers_container, layer_canvas):
    configurations = controller.load_configurations()
    if configurations:
        selected_configuration = selected_config.get()
        for config in configurations:
            if config["name"] == selected_configuration:
                controller.load_configuration_to_app(total_mac, total_mem, config, name_entry, input_height, input_width, input_channels, results_display, layer_frames, layers, layers_container, layer_canvas)
                break
    else:
        print("No configurations found.")

def update_bits_options(event):
    precision = layer_varprecision.get()
    if precision == "Floating Point":
        layer_dropdownbits['values'] = ("16", "32")
        if layer_varbits.get() not in ("16", "32"):
            layer_varbits.set("16")
    elif precision == "Fixed Point":
        layer_dropdownbits['values'] = ("8", "32")
        if layer_varbits.get() not in ("8", "32"):
            layer_varbits.set("8")

def update_configurations_dropdown():
    configurations = controller.load_configurations()
    options = [config["name"] for config in configurations]
    dropdown['values'] = options
    if options:
        selected_config.set(options[-1])  # Set the default value to the latest config's name

def save_configuration(input_height, input_width, input_channels, layer_frames, layers, name_entry):
    controller.save(input_height, input_width, input_channels, layer_frames, layers, name_entry.get())
    update_configurations_dropdown()  # Update dropdown after saving

# Create the main window
root = tk.Tk()
root.title("Dynamic Layer Configuration")

layer_frames = []
layers = []

# Calculate screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size as a fraction of screen size
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

# Set window geometry
root.geometry(f"{window_width}x{window_height}")

# Left frame for configuration
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Middle frame for graph (empty for now)
graph_frame = tk.Frame(root, bg="white")
graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Example button to draw graph
draw_button = tk.Button(left_frame, text="Draw Graph", command=draw_graph)
draw_button.pack(pady=20)

# Right frame for output
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Frame for name, load, and clear buttons
name_button_frame = tk.Frame(left_frame)
name_button_frame.pack(pady=10)

# Load configurations
configurations = controller.load_configurations()

# Create a StringVar to hold the selected option
selected_config = tk.StringVar(left_frame)

# If there are configurations, set the default value
if configurations:
    selected_config.set(configurations[0]["name"])  # Set the default value to the first config's name

# Create the dropdown menu (Combobox)
options = [config["name"] for config in configurations]
dropdown = ttk.Combobox(name_button_frame, textvariable=selected_config, values=options)
dropdown.grid(row=0, column=0, padx=5)

# Load button
load_button = tk.Button(name_button_frame, text="Load Configuration", command=lambda: load_configurations_and_display(total_mac, total_mem, name_entry, input_height, input_width, input_channels, results_display, layer_frames, layers, layers_container, layer_canvas))
load_button.grid(row=0, column=1, padx=5)

# Label for name
name_label = tk.Label(name_button_frame, text="Name:")
name_label.grid(row=0, column=2, padx=5)

# Entry for name
name_entry = tk.Entry(name_button_frame)
name_entry.grid(row=0, column=3, padx=5)

# Clear button
clear_button = tk.Button(name_button_frame, text="Clear Configuration", command=lambda: controller.clear_configuration_and_display(total_mac, total_mem, name_entry, input_height, input_width, input_channels, results_display, layer_frames, layers, layers_container))
clear_button.grid(row=0, column=4, padx=5)

# Frame for input size and input channels
input_frame = tk.Frame(left_frame)
input_frame.pack(pady=window_height // 60)

# Create labels and entries for input size and input channels
label1 = tk.Label(input_frame, text="Input Height:")
label1.grid(row=0, column=0, padx=window_width // 90)
input_height = tk.Entry(input_frame)
input_height.grid(row=0, column=1, padx=window_width // 90)
input_height.insert(tk.END, "1")

label2 = tk.Label(input_frame, text="Input Width:")
label2.grid(row=0, column=2, padx=window_width // 90)
input_width = tk.Entry(input_frame)
input_width.grid(row=0, column=3, padx=window_width // 90)
input_width.insert(tk.END, "1")

label3 = tk.Label(input_frame, text="Input Channels:")
label3.grid(row=0, column=4, padx=window_width // 90)
input_channels = tk.Entry(input_frame)
input_channels.grid(row=0, column=5, padx=window_width // 90)
input_channels.insert(tk.END, "1")

# Frame for layer selection and add button
top_frame = tk.Frame(left_frame)
top_frame.pack(pady=window_height // 90)

# Label and dropdown for layer selection
labellayer = tk.Label(top_frame, text="Layer Type:")
labellayer.grid(row=0, column=0, padx=window_width // 90)
layer_var = tk.StringVar(value="dense")
layer_dropdown = ttk.Combobox(top_frame, textvariable=layer_var)
layer_dropdown['values'] = ("dense", "convolution", "pooling", "flatten")
layer_dropdown.grid(row=0, column=1, padx=window_width // 90)

# Add layer button
add_button = tk.Button(top_frame, text="Add Layer", command=lambda: controller.add_layer(layer_var.get(), layers_container, layer_frames, layers, layer_canvas))
add_button.grid(row=0, column=2, padx=window_width // 90)

# Frame for layers with scrollbar
layer_frame = tk.Frame(left_frame)
layer_frame.pack(pady=window_height // 60, fill=tk.BOTH, expand=True)

# Canvas for layers with scrollbar
layer_canvas = tk.Canvas(layer_frame, width=750)
layer_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

layer_scrollbar = tk.Scrollbar(layer_frame, orient="vertical", command=layer_canvas.yview)
layer_scrollbar.pack(side=tk.RIGHT, fill="y")

layer_canvas.configure(yscrollcommand=layer_scrollbar.set)
layer_canvas.bind('<Configure>', lambda e: layer_canvas.configure(scrollregion=layer_canvas.bbox("all")))

# Frame to contain the layers within the canvas
layers_container = tk.Frame(layer_canvas)
layer_canvas.create_window((0, 0), window=layers_container, anchor="nw")

# Results display using Text widget with a scrollbar
results_frame = tk.Frame(right_frame)
results_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

results_scrollbar = tk.Scrollbar(results_frame)
results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

results_display = tk.Text(results_frame, height=20, width=100, yscrollcommand=results_scrollbar.set)
results_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
results_scrollbar.config(command=results_display.yview)

# Buttons and dropdowns at the bottom of the left frame
button_frame = tk.Frame(left_frame)
button_frame.pack(pady=window_height // 30)

# Calculate button
calculate_button = tk.Button(button_frame, text="Calculate", command=lambda: controller.calculate(total_mac, total_mem, input_height, input_width, input_channels, results_display, layer_frames, layers))
calculate_button.grid(row=0, column=0, padx=10)

# Save button
save_button = tk.Button(button_frame, text="Save", command=lambda: save_configuration(input_height, input_width, input_channels, layer_frames, layers, name_entry))
save_button.grid(row=0, column=1, padx=10)

# Technology selection
labeltech = tk.Label(button_frame, text="Technology:")
labeltech.grid(row=0, column=2, pady=5)
layer_vartech = tk.StringVar(value="45nm")
layer_dropdowntech = ttk.Combobox(button_frame, textvariable=layer_vartech)
layer_dropdowntech['values'] = ("7nm", "45nm")
layer_dropdowntech.grid(row=0, column=3, padx=5)

# Precision selection
labelprecision = tk.Label(button_frame, text="Precision:")
labelprecision.grid(row=0, column=4, pady=5)
layer_varprecision = tk.StringVar(value="Floating Point")
layer_dropdownprecision = ttk.Combobox(button_frame, textvariable=layer_varprecision)
layer_dropdownprecision['values'] = ("Floating Point", "Fixed Point")
layer_dropdownprecision.grid(row=0, column=5, padx=5)

# Bind the update function to the precision dropdown's selection event
layer_dropdownprecision.bind("<<ComboboxSelected>>", update_bits_options)

# Bits selection
labelbits = tk.Label(button_frame, text="Bits:")
labelbits.grid(row=0, column=6, pady=5)
layer_varbits = tk.StringVar(value="16")
layer_dropdownbits = ttk.Combobox(button_frame, textvariable=layer_varbits)
layer_dropdownbits['values'] = ("16", "32")
layer_dropdownbits.grid(row=0, column=7, padx=5)

# Memory Type selection
labelmemory_type = tk.Label(button_frame, text="Memory Type:")
labelmemory_type.grid(row=0, column=8, pady=5)
layer_varmemory_type = tk.StringVar(value="8KB SRAM")
layer_dropdownmemory_type = ttk.Combobox(button_frame, textvariable=layer_varmemory_type)
layer_dropdownmemory_type['values'] = ("8KB SRAM", "32KB SRAM", "1MB SRAM")
layer_dropdownmemory_type.grid(row=0, column=9, padx=5)

# Frame for energy calculations
energy_frame = tk.Frame(right_frame)
energy_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Total MAC
labeltotal_mac = tk.Label(energy_frame, text="Total MAC op:")
labeltotal_mac.grid(row=0, column=0, padx=5, pady=5)
total_mac = tk.Entry(energy_frame)
total_mac.grid(row=0, column=1, padx=5, pady=5)
total_mac.insert(0, "0")  # Set default value to 0

# Total Mem
labeltotal_mem = tk.Label(energy_frame, text="Total MEM op:")
labeltotal_mem.grid(row=0, column=2, padx=5, pady=5)
total_mem = tk.Entry(energy_frame)
total_mem.grid(row=0, column=3, padx=5, pady=5)
total_mem.insert(0, "0")  # Set default value to 0

# Energy button
energy_button = tk.Button(energy_frame, text="Calculate Energy", command=lambda: controller.energy(total_mac.get(), total_mem.get(), layer_dropdowntech, layer_dropdownprecision, layer_dropdownbits, layer_dropdownmemory_type, energy, energy_per_mac, energy_per_mem, tot_mac_energy, tot_mem_energy))
energy_button.grid(row=1, column=0, columnspan=4, pady=10)

# Label and entry for Energy per MAC
labelenergy_per_mac = tk.Label(energy_frame, text="Energy per MAC(pJ):")
labelenergy_per_mac.grid(row=2, column=0, padx=5, pady=5)
energy_per_mac = tk.Entry(energy_frame)
energy_per_mac.grid(row=2, column=1, padx=5, pady=5)
energy_per_mac.insert(0, "0")

# Label and entry for Energy per Mem
labelenergy_per_mem = tk.Label(energy_frame, text="Energy per MEM(pJ):")
labelenergy_per_mem.grid(row=2, column=2, padx=5, pady=5)
energy_per_mem = tk.Entry(energy_frame)
energy_per_mem.grid(row=2, column=3, padx=5, pady=5)
energy_per_mem.insert(0, "0")

# Label and entry for Total MAC Energy
labeltot_mac_energy = tk.Label(energy_frame, text="Total MAC Energy(pJ):")
labeltot_mac_energy.grid(row=3, column=0, padx=5, pady=5)
tot_mac_energy = tk.Entry(energy_frame)
tot_mac_energy.grid(row=3, column=1, padx=5, pady=5)
tot_mac_energy.insert(0, "0")

# Label and entry for Total Mem Energy
labeltot_mem_energy = tk.Label(energy_frame, text="Total Mem Energy(pJ):")
labeltot_mem_energy.grid(row=3, column=2, padx=5, pady=5)
tot_mem_energy = tk.Entry(energy_frame)
tot_mem_energy.grid(row=3, column=3, padx=5, pady=5)
tot_mem_energy.insert(0, "0")

# Label and entry for Total Energy
labelenergy = tk.Label(energy_frame, text="Total Inference Energy(pJ):")
labelenergy.grid(row=4, column=0, padx=5, pady=5)
energy = tk.Entry(energy_frame)
energy.grid(row=4, column=1, padx=5, pady=5)
energy.insert(0, "0")

# Label and entry for Data sample rate
labelsample_rate = tk.Label(energy_frame, text="Data sample rate Fs(GHz):")
labelsample_rate.grid(row=5, column=0, padx=5, pady=5)
sample_rate = tk.Entry(energy_frame)
sample_rate.grid(row=5, column=1, padx=5, pady=5)
sample_rate.insert(0, "0.64")

# Dynamic power button
power_button = tk.Button(energy_frame, text="Calculate Power", command=lambda: controller.dynamic_power(input_height,input_width,input_channels,sample_rate, energy, dynamic_power))
power_button.grid(row=5, column=2, columnspan=4, pady=10)

# Label and entry for Dynamic Power
labeldynamic_power = tk.Label(energy_frame, text="Dynamic Power(W):")
labeldynamic_power.grid(row=6, column=0, padx=5, pady=5)
dynamic_power = tk.Entry(energy_frame)
dynamic_power.grid(row=6, column=1, padx=5, pady=5)
dynamic_power.insert(0, "0")

# Start the Tkinter event loop
root.mainloop()
