Neural Network Energy Consumption Analyzer
Overview
This application calculates and analyzes the energy consumption of various neural network layers. It allows users to configure custom neural networks, calculate the energy and power consumption for different configurations, and visualize the results.

Features
Network Configuration: Create new neural network configurations or load predefined models (e.g., AlexNet, ZynqNet, YOLO, VGG16, ResNet152).
Energy Calculation: Compute the total energy consumption for multiply-accumulate operations (MACCs) and memory operations (MEMs).
Power Calculation: Calculate dynamic power based on data sample rate and total inference energy.
Visualization: Generate graphs to compare energy consumption between MACCs and MEMs.
Requirements
Python 3.x
Tkinter
Matplotlib
Pandas
