import tkinter as tk
from models import AnyLayer

# class DenseLayer(AnyLayer.AnyLayer):
#     def __init__(self, parent, values, layer_number=0):
#         super().__init__(parent, layer_type="dense", layer_number=layer_number, values=values)
#         # self.frame = tk.Frame(parent)
#         # self.frame.pack(pady=5)
#         # self.layer_type = "dense"
#         # self.layer_number = layer_number
        
#         # tk.Label(self.frame, text=f"{self.layer_number} Dense").grid(row=0, column=0, padx=5)
        
#         tk.Label(self.frame, text="Output Neurons:").grid(row=0, column=2, padx=5)
#         self.output_neurons_entry = tk.Entry(self.frame)
#         self.output_neurons_entry.grid(row=0, column=3, padx=5)
#         self.output_neurons_entry.insert(tk.END, values[0] if values else "1")

#         tk.Label(self.frame, text="Activation:").grid(row=0, column=6, padx=5)
#         self.activation_entry = tk.Entry(self.frame)
#         self.activation_entry.grid(row=0, column=7, padx=5)
#         self.activation_entry.insert(tk.END, values[1] if values else "relu")
        
#         #tk.Button(self.frame, text="Delete", command=self.frame.destroy).grid(row=0, column=1, padx=5)

#     def get_entries(self):
#         return [self.output_neurons_entry,self.activation_entry]


class DenseLayer(AnyLayer.AnyLayer):
    def __init__(self, parent, values=None, layer_number=0, layer_list=None):
        super().__init__(parent, layer_type="dense", layer_number=layer_number, layer_list=layer_list, values=values)

        tk.Label(self.frame, text="Output Neurons:").grid(row=0, column=2, padx=5)
        self.output_neurons_entry = tk.Entry(self.frame, width=self.entry_width)
        self.output_neurons_entry.grid(row=0, column=3, padx=5)
        self.output_neurons_entry.insert(tk.END, values[0] if values else "1")

        tk.Label(self.frame, text="Activation:").grid(row=0, column=4, padx=5)
        self.activation_entry = tk.Entry(self.frame, width=self.entry_width+5)
        self.activation_entry.grid(row=0, column=5, padx=5)
        self.activation_entry.insert(tk.END, values[1] if values else "relu")
        
        self.entries = [self.output_neurons_entry, self.activation_entry]