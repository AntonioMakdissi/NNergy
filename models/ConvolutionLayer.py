import tkinter as tk
from models import AnyLayer

# class ConvolutionLayer:
#     def __init__(self, parent, values):
#         self.frame = tk.Frame(parent)
#         self.frame.pack(pady=5)
#         self.layer_type = "convolution"
        
#         tk.Label(self.frame, text="Convolution").grid(row=0, column=0, padx=1)
        
#         tk.Label(self.frame, text="Height:").grid(row=0, column=2, padx=1)
#         self.height_entry = tk.Entry(self.frame)
#         self.height_entry.grid(row=0, column=3, padx=1)
#         self.height_entry.insert(tk.END, values[0] if values else "1")
        
#         tk.Label(self.frame, text="Width:").grid(row=0, column=4, padx=1)
#         self.width_entry = tk.Entry(self.frame)
#         self.width_entry.grid(row=0, column=5, padx=1)
#         self.width_entry.insert(tk.END, values[1] if values else "1")
        
#         tk.Label(self.frame, text="Filters:").grid(row=0, column=6, padx=1)
#         self.filters_entry = tk.Entry(self.frame)
#         self.filters_entry.grid(row=0, column=7, padx=1)
#         self.filters_entry.insert(tk.END, values[2] if values else "1")

#         tk.Label(self.frame, text="Stride:").grid(row=1, column=2, padx=1)
#         self.stride_entry = tk.Entry(self.frame)
#         self.stride_entry.grid(row=1, column=3, padx=1)
#         self.stride_entry.insert(tk.END, values[3] if values else "1")

#         tk.Label(self.frame, text="Padding:").grid(row=1, column=4, padx=1)
#         self.padding_entry = tk.Entry(self.frame)
#         self.padding_entry.grid(row=1, column=5, padx=1)
#         self.padding_entry.insert(tk.END, values[4] if values else "1")

#         tk.Label(self.frame, text="Activation:").grid(row=1, column=6, padx=1)
#         self.activation_entry = tk.Entry(self.frame)
#         self.activation_entry.grid(row=1, column=7, padx=1)
#         self.activation_entry.insert(tk.END, values[5] if values else "relu")
        
#         tk.Button(self.frame, text="Delete", command=self.frame.destroy).grid(row=0, column=1, padx=1)

#     def get_entries(self):
#         return [
#             self.height_entry, self.width_entry, self.filters_entry,
#             self.stride_entry, self.padding_entry, self.activation_entry
#         ]


class ConvolutionLayer(AnyLayer.AnyLayer):
    def __init__(self, parent, values=None, layer_number=0, layer_list=None):
        super().__init__(parent, layer_type="convolution", layer_number=layer_number, layer_list=layer_list, values=values)
    
    def create_widgets(self, values=None):
        
        tk.Label(self.frame, text="Height:").grid(row=0, column=2, padx=1)
        self.height_entry = tk.Entry(self.frame, width=self.entry_width)
        self.height_entry.grid(row=0, column=3, padx=1)
        self.height_entry.insert(tk.END, values[0] if values else "1")
        
        tk.Label(self.frame, text="Width:").grid(row=0, column=4, padx=1)
        self.width_entry = tk.Entry(self.frame, width=self.entry_width)
        self.width_entry.grid(row=0, column=5, padx=1)
        self.width_entry.insert(tk.END, values[1] if values else "1")
        
        tk.Label(self.frame, text="Filters:").grid(row=0, column=6, padx=1)
        self.filters_entry = tk.Entry(self.frame, width=self.entry_width)
        self.filters_entry.grid(row=0, column=7, padx=1)
        self.filters_entry.insert(tk.END, values[2] if values else "1")

        tk.Label(self.frame, text="Stride:").grid(row=1, column=2, padx=1)
        self.stride_entry = tk.Entry(self.frame, width=self.entry_width)
        self.stride_entry.grid(row=1, column=3, padx=1)
        self.stride_entry.insert(tk.END, values[3] if values else "1")

        tk.Label(self.frame, text="Padding:").grid(row=1, column=4, padx=1)
        self.padding_entry = tk.Entry(self.frame, width=self.entry_width)
        self.padding_entry.grid(row=1, column=5, padx=1)
        self.padding_entry.insert(tk.END, values[4] if values else "1")

        tk.Label(self.frame, text="Activation:").grid(row=1, column=6, padx=1)
        self.activation_entry = tk.Entry(self.frame, width=self.entry_width+5)
        self.activation_entry.grid(row=1, column=7, padx=1)
        self.activation_entry.insert(tk.END, values[5] if values else "relu")
        
        self.entries = [
            self.height_entry, self.width_entry, self.filters_entry,
            self.stride_entry, self.padding_entry, self.activation_entry
        ]