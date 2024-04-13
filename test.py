import tkinter as tk
from tkinter import ttk

""" this code is used for implmenting drag selection 
if we want to select more than a item from a treeview of tk then this is the solution
"""

class app:
    list = []
    def on_mouse_drag(self,event):
        item_id = self.tree.identify_row(event.y)  # Get the item ID under the mouse cursor
        self.list.append(item_id)
        self.tree.item(item_id, tags=(item_id))
        self.tree.tag_configure(item_id, background='green')  # Change color

    def onclick(self,event):
        item_id = self.tree.identify_row(event.y)
        for x in self.list:
           self.tree.tag_configure(x, background='white')
        self.list = []



    def createwindow(self):
        self.root = tk.Tk()
        self.tree = ttk.Treeview(self.root)
        for i in range(10):
            self.tree.insert("", "end", text=f"Item {i + 1}", tags=('ttk', 'simple'))
        self.tree.pack()
        self.tree.bind("<B1-Motion>", self.on_mouse_drag)
        self.tree.bind("<Button-1>", self.onclick)
        self.root.mainloop()

app().createwindow()