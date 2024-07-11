import tkinter as tk
from models import AnyLayer

# class FlattenLayer:
#     def __init__(self, parent):
#         self.frame = tk.Frame(parent)
#         self.frame.pack(pady=5)
#         self.layer_type = "flatten"
        
#         tk.Label(self.frame, text="Flatten").grid(row=0, column=0, padx=5)
#         tk.Label(self.frame, text="No parameters for Flatten layer").grid(row=0, column=2, padx=5, columnspan=2)
        
#         tk.Button(self.frame, text="Delete", command=self.frame.destroy).grid(row=0, column=1, padx=5)

#     def get_entries(self):
#         return []

class FlattenLayer(AnyLayer.AnyLayer):
    def __init__(self, parent, layer_number=0, layer_list=None):
        super().__init__(parent, layer_type="flatten", layer_number=layer_number, layer_list=layer_list)
    
    def create_widgets(self, **kwargs):
        tk.Label(self.frame, text="No parameters for Flatten layer").grid(row=0, column=2, padx=5, columnspan=2)
        
        self.entries = []
