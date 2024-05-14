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

    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.keyholdding = False
        super().bind("<Button-1>", self.start_selection)
        super().bind("<B1-Motion>", self.update_selection)
        super().bind("<ButtonRelease-1>", self.end_selection)
        super().bind("<MouseWheel>", self.update_selection)

    def _scroll(self,event):
        pass

    def _press(self, event):
        pass

    def _release(self, event):
        pass

    def _motion(self, event):

        pass

    def bind(self, event_string, function,val=None, **kw):
        if event_string == "<Button-1>":
            self._press = function
        elif event_string == "<B1-Motion>":
            self._motion = function
        elif event_string == "<ButtonRelease-1>":
            self._release = function
        elif event_string == "<MouseWheel>":
            self._scroll = function
        else:
            super().bind(event_string, function)

    def getselection_list(self):
        return self.selection()

    def unselect_allitems(self):
        self.selection_set([])

    def start_selection(self, event):
        self.keyholdding = True
        item = self.identify('item', event.x, event.y)
        self.selection_set(item)
        self._press(event)

    def update_selection(self, event):
        if self.keyholdding:
            item = self.identify('item', event.x, event.y)
            if not item in self.selection():
                self.selection_add(item)
        self._motion(event)

    def end_selection(self, event):
        self.keyholdding = False
        self._release(event)



class scrollselection(DragSelectTreeView):
    """automatic scrolling of treeview when selected and dragged
     treeview items will scroll and a selection will appear over the items
    """
    def __init__(self,root,**kw):
        super().__init__(root,**kw)
        self.bind("<B1-Motion>",self.generate_scrollingevent)
        super().unbind("<MouseWheel>")
    def generate_scrollingevent(self,event):
        "this is for an experiment"
        self.event_generate("<MouseWheel>", delta=-120, x=50, y=50)

if __name__ == "__main__":

    root = tk.Tk()
    style = ttk.Style()
    style.map("Treeview", background=[('selected', 'orange')])

    tree = scrollselection(root, columns=("Name", "Age", "Country"))
    tree.configure(selectmode="extended")


    for i in range(1100):
        item = tree.insert("", "end", text=f"orange {i}", values=("John Doe", "30", "USA"))


    tree.pack(expand=True,side='left')

    scroll = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    scroll.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scroll.set)
    root.mainloop()
