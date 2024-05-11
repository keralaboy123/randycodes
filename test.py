import tkinter as tk
from tkinter import ttk

"""
this costumized treeview widget provide drag selection of multiple items
it is achieved by capturing motion event with mouse scroll event
this is a treeview with all of its properties so 
you can use classs DragSelectTreeView instead treeview of tk
author : github.com/keralaboy123
"""


class DragSelectTreeView(ttk.Treeview):
    "inheritable treeview customized for multiple drag selection"
    def __init__(self,root, **kw):
        super().__init__(root, **kw )
        self.items = []
        self.keyholdding = False
        super().bind("<Button-1>", self.start_selection)
        super().bind("<B1-Motion>", self.update_selection)
        super().bind("<ButtonRelease-1>", self.end_selection)
        self.bind("<MouseWheel>", self.update_selection)

    def getselection_list(self):
        return self.items

    def _press(self,event):
        pass
    def _release(self,event):
        pass
    def _motion (self,event):
        pass


    def bind(self,event_string,function):
        if event_string == "<Button-1>":
            self._press = function
        elif event_string == "<B1-Motion>":
            self._motion = function
        elif event_string == "<ButtonRelease-1>":
            self._release = function
        else:
            super().bind(event_string,function)


    def start_selection(self, event):
        self.items = []
        self.keyholdding = True
        item = self.identify('item', event.x, event.y)
        self.items.append(item)
        self._press(event)

    def show_multiple_selection(self):
        self.selection_set(self.items)

    def update_selection(self, event):
        if self.keyholdding:
            
           item = self.identify('item', event.x, event.y)
           if not item in self.items:
              self.items.append(item)
              
        self.show_multiple_selection()
        self._motion(event)

    def end_selection(self, event):
        self.keyholdding = False
        self._release(event)


if __name__ == "__main__":
        root = tk.Tk()
        tree = DragSelectTreeView(root, columns=("Name", "Age", "Country"))
        tree.configure(selectmode="extended")
        style = ttk.Style()
        style.map("Treeview", background=[('selected', 'orange')])

        for i in range(110):
             tree.insert("", "end", text=f"orange {i}",values=("John Doe", "30", "USA"))

        tree.pack(side ='left')
        tree.bind("<ButtonRelease-1>", lambda x: print("selected items are = ",tree.selection()))
        scroll = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll.set)

        root.mainloop()