import tkinter as tk
from map_ui import MapUI

if __name__ == "__main__":
    root = tk.Tk()
    app = MapUI(root=root, pxl_width=600, pxl_height=400, cell_size=10)
    root.mainloop()
