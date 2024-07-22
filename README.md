## Neural Network Energy Consumption Analyzer
# Overview
This application calculates and analyzes the energy consumption of various neural network layers. It allows users to configure custom neural networks, calculate the energy and power consumption for different configurations, and visualize the results.

# Features
Network Configuration: Create new neural network configurations or load predefined models (e.g., AlexNet, ZynqNet, YOLO, VGG16, ResNet152).
Energy Calculation: Compute the total energy consumption for multiply-accumulate operations (MACCs) and memory operations (MEMs).
Power Calculation: Calculate dynamic power based on data sample rate and total inference energy.
Visualization: Generate graphs to compare energy consumption between MACCs and MEMs.

# Requirements
- Python 3.x
- Tkinter
- Matplotlib
- Pandas

# Usage
Run the application:
- python views.py
  
Use the GUI to:

- Enter the dimensions of the input (height, width, channels).
- Select the type of layer to add and configure its parameters.
- Save or load network configurations.
- Click "Calculate" to compute the energy consumption for each layer.
- Click "Calculate Energy" to determine the total inference energy.
- Click "Calculate Power" to compute the dynamic power.
- Click "Draw Graph" to visualize the energy consumption breakdown.

# Code Overview
# controller.py
Contains the logic for calculating energy and power consumption:

energy(): Calculates the total energy for MACCs and MEMs.
dynamic_power(): Computes the dynamic power based on data sample rate and inference energy.
show_graph(): Displays a graph comparing energy consumption for MACCs and MEMs.

# views.py
Defines the GUI for the application using Tkinter:

Provides input fields for network dimensions, layer configuration, and energy parameters.
Buttons for saving/loading configurations, calculating energy/power, and drawing graphs.
Displays results for total energy, MACC energy, MEM energy, and dynamic power.

# models
provides the skeleton of how layer types are organised

# Future Work
Implementing the application in a less demanding language, such as Java, to enhance the user interface.
Adding support for more types of layers (e.g., LSTM, custom user-defined layers).
Integrating more sophisticated energy consumption models.
Implementing automated optimization techniques for energy-efficient network configurations.
Investigating the impact of calculating in FLOPS on computation and results.

# Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss potential changes or improvements.

# Acknowledgements
Special thanks to all contributors and supporters of this project.
