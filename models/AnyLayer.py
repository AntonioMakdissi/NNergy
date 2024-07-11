import tkinter as tk

#Blueprint for any layer
class AnyLayer:
    def __init__(self, parent, layer_type="any", layer_number=0, layer_list=None, **kwargs):
        self.frame = tk.Frame(parent)
        self.frame.pack(pady=5)
        self.layer_type = layer_type
        self.layer_number = layer_number
        self.layer_list = layer_list
        self.entry_width = 5
        
        self.label = tk.Label(self.frame, text=f"L{self.layer_number} {self.layer_type}")
        self.label.grid(row=0, column=0, padx=5)
        
        self.delete_button = tk.Button(self.frame, text="Delete", command=self.delete_layer)
        self.delete_button.grid(row=0, column=1, padx=5)
        
        self.entries = []
        self.create_widgets(**kwargs)

    def create_widgets(self, **kwargs):
        """Method to create and add custom widgets to the frame. Override in subclasses."""
        pass

    def get_entries(self):
        """Method to retrieve data from custom widgets. Override in subclasses."""
        return [entry.get() for entry in self.entries]

    def delete_layer(self):
        """Remove the layer from the list and destroy the frame."""
        if self.layer_list is not None:
            self.layer_list.remove(self)
        self.frame.destroy()
