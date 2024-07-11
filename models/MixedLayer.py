import tkinter as tk
from models import AnyLayer

# class MixedLayer:
#     def __init__(self, parent):
#         self.frame = tk.Frame(parent)
#         self.frame.pack(pady=5)
#         self.layer_type = "mixed"
        
#         tk.Label(self.frame, text="Mixed").grid(row=0, column=0, padx=5)
#         tk.Label(self.frame, text="No parameters for Mixed layer").grid(row=0, column=2, padx=5, columnspan=2)
        
#         tk.Button(self.frame, text="Delete", command=self.frame.destroy).grid(row=0, column=1, padx=5)

#     def get_entries(self):
#         return []


class MixedLayer(AnyLayer.AnyLayer):
    def __init__(self, parent, values=None, layer_number=0, layer_list=None):
        super().__init__(parent, layer_type="mixed", layer_number=layer_number, layer_list=layer_list, values=values)
    
    def create_widgets(self, values=None):
        # Units
        tk.Label(self.frame, text="Units:").grid(row=0, column=2, padx=5)
        self.units_entry = tk.Entry(self.frame)
        self.units_entry.grid(row=0, column=3, padx=5)
        self.units_entry.insert(tk.END, values[0] if values else "1")

        # Activation
        tk.Label(self.frame, text="Activation:").grid(row=0, column=4, padx=5)
        self.activation_entry = tk.Entry(self.frame)
        self.activation_entry.grid(row=0, column=5, padx=5)
        self.activation_entry.insert(tk.END, values[1] if values else "relu")

        # Dropout
        tk.Label(self.frame, text="Dropout:").grid(row=0, column=6, padx=5)
        self.dropout_entry = tk.Entry(self.frame)
        self.dropout_entry.grid(row=0, column=7, padx=5)
        self.dropout_entry.insert(tk.END, values[2] if values else "0.5")

        # Return Sequences
        tk.Label(self.frame, text="Return Sequences:").grid(row=1, column=2, padx=5)
        self.return_sequences_var = tk.BooleanVar()
        self.return_sequences_checkbox = tk.Checkbutton(self.frame, variable=self.return_sequences_var)
        self.return_sequences_checkbox.grid(row=1, column=3, padx=5)
        if values and values[3] == "True":
            self.return_sequences_checkbox.select()
        
        self.entries = [self.units_entry, self.activation_entry, self.dropout_entry, self.return_sequences_var]

    def get_entries(self):
        return [
            self.units_entry.get(),
            self.activation_entry.get(),
            self.dropout_entry.get(),
            self.return_sequences_var.get()
        ]