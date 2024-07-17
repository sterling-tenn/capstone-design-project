import tkinter as tk
from tkinter import messagebox, filedialog
import json
from Astar import *

class MapUI:
    def __init__(self, root, width, height):
        self.root = root
        self.root.title("Particle Filter Map Builder")

        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack()

        self.start_pos = None
        self.target_pos = None
        self.obstacles = []
        
        self.width = width
        self.height = height

        self.cell_size = 5
        
        self.canvas.bind("<Button-1>", self.add_point)  # Bind left click to add_point function

        self.create_buttons()

    def create_buttons(self):
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.mode = None  # Initialize mode as None

        self.start_button = tk.Button(self.button_frame, text="Set Start Position", command=self.set_start_position)
        self.start_button.grid(row=0, column=0)

        self.target_button = tk.Button(self.button_frame, text="Set Target Position", command=self.set_target_position)
        self.target_button.grid(row=0, column=1)

        self.obstacle_button = tk.Button(self.button_frame, text="Add Obstacles", command=self.add_obstacle)
        self.obstacle_button.grid(row=0, column=2)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear)
        self.clear_button.grid(row=0, column=3)

        self.save_button = tk.Button(self.button_frame, text="Save Map", command=self.save_map)
        self.save_button.grid(row=0, column=4)

        self.load_button = tk.Button(self.button_frame, text="Load Map", command=self.load_map)
        self.load_button.grid(row=0, column=5)
        
        self.path_button = tk.Button(self.button_frame, text="Find Path", command=self.find_path)
        self.path_button.grid(row=0, column=6)

    def set_start_position(self):
        self.mode = "start"
        self.root.title("Particle Filter Map Builder [Mode: Set Start Position]")

    def set_target_position(self):
        self.mode = "target"
        self.root.title("Particle Filter Map Builder [Mode: Set Target Position]")

    def add_obstacle(self):
        self.mode = "obstacle"
        self.root.title("Particle Filter Map Builder [Mode: Add Obstacles]")

    def clear(self):
        self.canvas.delete("all")
        self.start_pos = None
        self.target_pos = None
        self.obstacles = []
        self.mode = None
        self.root.title("Particle Filter Map Builder")

    def add_point(self, event):
        x, y = event.x, event.y

        if self.mode == "start":
            if self.start_pos:
                self.canvas.delete(self.start_pos)
            self.start_pos = self.canvas.create_rectangle(x-self.cell_size, y-self.cell_size, x+self.cell_size, y+self.cell_size, fill="green")

        elif self.mode == "target":
            if self.target_pos:
                self.canvas.delete(self.target_pos)
            self.target_pos = self.canvas.create_rectangle(x-self.cell_size, y-self.cell_size, x+self.cell_size, y+self.cell_size, fill="red")

        elif self.mode == "obstacle":
            self.canvas.create_rectangle(x-self.cell_size, y-self.cell_size, x+self.cell_size, y+self.cell_size, fill="black")
            self.obstacles.append((x, y))

    def save_map(self):
        if not self.start_pos or not self.target_pos:
            messagebox.showwarning("Incomplete Map", "Please set both start and target positions before saving.")
            return

        map_data = {
            'start': self.canvas.coords(self.start_pos)[:2],
            'target': self.canvas.coords(self.target_pos)[:2],
            'obstacles': self.obstacles,
            'dimensions': {
                "width": self.width,
                "height": self.height
            }
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(map_data, file)
            messagebox.showinfo("Save Successful", f"Map saved to {file_path}")

    def find_path(self):
        start = tuple(map(int, self.canvas.coords(self.start_pos)[:2]))
        dest = tuple(map(int, self.canvas.coords(self.target_pos)[:2]))
        
        astar = Astar(self.height, self.width, self.obstacles, start, dest, self.cell_size)
        path = astar.find_path()
        
        print(path)
        
        if not path:
            print("path not found via A*")
        
        for x, y in path:
            self.canvas.create_rectangle(x-self.cell_size, y-self.cell_size, x+self.cell_size, y+self.cell_size, fill="blue")

    def load_map(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, 'r') as file:
            map_data = json.load(file)

        self.clear()

        start_coords = map_data['start']
        target_coords = map_data['target']
        obstacles_coords = map_data['obstacles']

        self.start_pos = self.canvas.create_rectangle(start_coords[0]-self.cell_size, start_coords[1]-self.cell_size, start_coords[0]+self.cell_size, start_coords[1]+self.cell_size, fill="green")
        self.target_pos = self.canvas.create_rectangle(target_coords[0]-self.cell_size, target_coords[1]-self.cell_size, target_coords[0]+self.cell_size, target_coords[1]+self.cell_size, fill="red")

        for x, y in obstacles_coords:
            self.canvas.create_rectangle(x-self.cell_size, y-self.cell_size, x+self.cell_size, y+self.cell_size, fill="black")
            self.obstacles.append((x, y))

        self.root.title("Particle Filter Map Builder [Map Loaded]")
        messagebox.showinfo("Load Successful", f"Map loaded from {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MapUI(
        root=root,
        width=500,
        height=500
    )
    
    root.mainloop()
