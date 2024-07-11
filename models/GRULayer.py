import tkinter as tk
from models import AnyLayer

# class GRULayer:
#     def __init__(self, parent, values):
#         self.frame = tk.Frame(parent)
#         self.frame.pack(pady=5)
#         self.layer_type = "gru"
        
#         tk.Label(self.frame, text="GRU").grid(row=0, column=0, padx=5)
        
#         tk.Label(self.frame, text="Units:").grid(row=0, column=2, padx=5)
#         self.units_entry = tk.Entry(self.frame)
#         self.units_entry.grid(row=0, column=3, padx=5)
#         self.units_entry.insert(tk.END, values[0] if values else "1")

#         tk.Label(self.frame, text="Return Sequences:").grid(row=0, column=6, padx=5)
#         self.return_sequences_var = tk.BooleanVar()
#         self.return_sequences_checkbox = tk.Checkbutton(self.frame, variable=self.return_sequences_var)
#         self.return_sequences_checkbox.grid(row=0, column=7, padx=5)
#         if values and values[1] == "True":
#             self.return_sequences_checkbox.select()

#         tk.Button(self.frame, text="Delete", command=self.frame.destroy).grid(row=0, column=1, padx=5)

#     def get_entries(self):
#         return [self.units_entry, self.return_sequences_var]
    
class GRULayer(AnyLayer.AnyLayer):
    def __init__(self, parent, values=None, layer_number=0, layer_list=None):
        super().__init__(parent, layer_type="gru", layer_number=layer_number, layer_list=layer_list, values=values)
    
    def create_widgets(self, values=None):
        tk.Label(self.frame, text="Units:").grid(row=0, column=2, padx=5)
        self.units_entry = tk.Entry(self.frame, width=self.entry_width)
        self.units_entry.grid(row=0, column=3, padx=5)
        self.units_entry.insert(tk.END, values[0] if values else "1")

        tk.Label(self.frame, text="Return Sequences:").grid(row=0, column=6, padx=5)
        self.return_sequences_var = tk.BooleanVar()
        self.return_sequences_checkbox = tk.Checkbutton(self.frame, variable=self.return_sequences_var)
        self.return_sequences_checkbox.grid(row=0, column=7, padx=5)
        if values and values[1] == "True":
            self.return_sequences_checkbox.select()
        
        self.entries = [self.units_entry, self.return_sequences_var]

    def get_entries(self):
        return [self.units_entry.get(), self.return_sequences_var.get()]