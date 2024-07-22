import tkinter as tk
from models import AnyLayer

# class PoolingLayer:
#     def __init__(self, parent, values):
#         self.parent = parent
#         self.frame = tk.Frame(parent)  # Add parent reference here
#         self.frame.pack(pady=5)
#         self.layer_type = "pooling"
        
#         tk.Label(self.frame, text="Pooling").grid(row=0, column=0, padx=5)
        
#         tk.Label(self.frame, text="Height:").grid(row=0, column=2, padx=5)
#         self.height_entry = tk.Entry(self.frame)
#         self.height_entry.grid(row=0, column=3, padx=5)
#         self.height_entry.insert(tk.END, values[0] if values else "1")
        
#         tk.Label(self.frame, text="Width:").grid(row=0, column=4, padx=5)
#         self.width_entry = tk.Entry(self.frame)
#         self.width_entry.grid(row=0, column=5, padx=5)
#         self.width_entry.insert(tk.END, values[1] if values else "1")
        
#         tk.Label(self.frame, text="Stride:").grid(row=1, column=2, padx=5)
#         self.stride_entry = tk.Entry(self.frame)
#         self.stride_entry.grid(row=1, column=3, padx=5)
#         self.stride_entry.insert(tk.END, values[2] if values else "1")

#         tk.Label(self.frame, text="Padding:").grid(row=1, column=4, padx=5)
#         self.padding_entry = tk.Entry(self.frame)
#         self.padding_entry.grid(row=1, column=5, padx=5)
#         self.padding_entry.insert(tk.END, values[3] if values else "1")

#         tk.Label(self.frame, text="Type:").grid(row=0, column=6, padx=5)  # Correct column index
#         self.type_entry = tk.Entry(self.frame)
#         self.type_entry.grid(row=0, column=7, padx=5)  # Correct column index
#         self.type_entry.insert(tk.END, values[4] if values else "max")
        
#         tk.Button(self.frame, text="Delete", command=self.frame.destroy).grid(row=0, column=1, padx=5)

#     def get_entries(self):
#         return [
#             self.height_entry, self.width_entry, 
#             self.stride_entry, self.padding_entry,
#             self.type_entry
#         ]
    
class PoolingLayer(AnyLayer.AnyLayer):
    def __init__(self, parent, values=None, layer_number=0, layer_list=None):
        super().__init__(parent, layer_type="pooling", layer_number=layer_number, layer_list=layer_list, values=values)
    
    def create_widgets(self, values=None):
        tk.Label(self.frame, text="Height:").grid(row=0, column=2, padx=5)
        self.height_entry = tk.Entry(self.frame, width=self.entry_width)
        self.height_entry.grid(row=0, column=3, padx=5)
        self.height_entry.insert(tk.END, values[0] if values else "1")
        
        tk.Label(self.frame, text="Width:").grid(row=0, column=4, padx=5)
        self.width_entry = tk.Entry(self.frame, width=self.entry_width)
        self.width_entry.grid(row=0, column=5, padx=5)
        self.width_entry.insert(tk.END, values[1] if values else "1")
        
        tk.Label(self.frame, text="Stride:").grid(row=1, column=2, padx=5)
        self.stride_entry = tk.Entry(self.frame, width=self.entry_width)
        self.stride_entry.grid(row=1, column=3, padx=5)
        self.stride_entry.insert(tk.END, values[2] if values else "1")

        tk.Label(self.frame, text="Padding:").grid(row=1, column=4, padx=5)
        self.padding_entry = tk.Entry(self.frame, width=self.entry_width)
        self.padding_entry.grid(row=1, column=5, padx=5)
        self.padding_entry.insert(tk.END, values[3] if values else "same")

        tk.Label(self.frame, text="Type:").grid(row=0, column=6, padx=5)
        self.type_entry = tk.Entry(self.frame, width=self.entry_width+5)
        self.type_entry.grid(row=0, column=7, padx=5)
        self.type_entry.insert(tk.END, values[4] if values else "max")
        
        self.entries = [
            self.height_entry, self.width_entry, 
            self.stride_entry, self.padding_entry,
            self.type_entry
        ]