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
        self.firstkey = None
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


    def getselection_list(self):
        return self.selection()

    def unselect_allitems(self):
        self.selection_set([])

    def start_selection(self, event):
        self.keyholdding = True
        self.firstkey  = self.identify('item', event.x, event.y)
        self.selection_set(self.firstkey)


    def update_selection(self,event):
        if self.keyholdding:

            item = self.identify('item', event.x, event.y)

            if item and not item in self.selection() and self.firstkey:

                first_item = self.firstkey
                first_item_index = self.get_children("").index(first_item)
                last_item = self.get_children("").index(item)
                maxmum = max(first_item_index,last_item)
                minmum = min(first_item_index, last_item)
                self.selection_set(self.get_children("")[minmum:maxmum+1])
    def end_selection(self, event):
        self.keyholdding = False


class scrollselection(DragSelectTreeView):
    """
    automatic scrolling when dragged. and
    when button release then all selected item will get tickmark in checkbox
    """
    def __init__(self,root,**kw):
        self.lasty = None
        super().__init__(root,**kw)
        self.bind("<B1-Motion>", self.dragged)

    def dragged(self, event):
        if self.keyholdding:
           self.update_selection(event)
           self.generate_scrollingevent(event)

    def get_item_location(treeview, item):
        # Get the bounding box coordinates of the specified item
        x,y = 0,0
        bbox = treeview.bbox(item)
        if bbox:
            x, y = bbox[0], bbox[1]

        return x, y
    
    def generate_scrollingevent(self,event):
        if self.lasty:
            items = self.__getvisible_items()
            firstitem ,lastitem = items[0], items[-1]
            firstitem_x, firstitem_y = self.get_item_location(firstitem)
            lastitem_x,lastitem_y = self.get_item_location(lastitem)
            if  firstitem_y == 0 and lastitem_y == 0:
               print("first item and lastiem both not found so autoscroll never work")
            else:
               if self.lasty < event.y and event.y >= lastitem_y :
                   self.yview_scroll(1, "units")
               elif self.lasty > event.y  and event.y <= firstitem_y:
                   self.yview_scroll(-1, "units")
        self.lasty = event.y
    def __getvisible_items(treeview):

        total_items = treeview.get_children("")
        y_scroll = treeview.yview()
        first_item_index = int(y_scroll[0] * len(total_items))
        last_item_index = int(y_scroll[1] * len(total_items))
        visible_items = total_items[first_item_index:last_item_index + 1]
        return visible_items


class sorter(scrollselection):
    "this class provides sort function for normal treeview widget"
    "if you need custom sorting then override methods provided here"

    def __init__(self, *kw, **kws):
        super().__init__(*kw, **kws)
        if kws.get("columns"):
            for colum in kws["columns"]:
                self.bind_sort_to_colum(colum)
        self.bind_sort_to_colum("#0")

    def bind_sort_to_colum(self, colum):
        self.heading(colum,text=colum, command=lambda: self.sort(colum, reverse=True))

    def backup(self, col):
            data = []
            allitems = self.get_children("")
            for item in allitems:
                if col == "#0":
                    columval = self.item(item, 'text')
                else:
                    columval = self.set(item, col)
                if columval.isdigit():
                    columval = int(columval)
                one_row = self.item(item)
                data.append((columval,one_row))
            return data

    def restore(self, data):
        for _, val in data:
            self.insert("", "end",**val)

    def sort(self, col, reverse=True):
        data = self.backup(col)
        self.delete(*self.get_children(""))
        data.sort(reverse=reverse,key=lambda x: x[0])
        self.restore(data)
        self.heading(col, command=lambda: self.sort(col=col, reverse=not reverse))

