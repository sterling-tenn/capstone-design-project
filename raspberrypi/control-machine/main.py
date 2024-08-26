import tkinter as tk
from map_ui import MapUI  # Import the MapUI class from the file where it is defined

def main():
    root = tk.Tk()
    width = 800  # Define the width of the canvas
    height = 600  # Define the height of the canvas
    map = MapUI(root, width, height)
    root.mainloop()

if __name__ == "__main__":
    main()