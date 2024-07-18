from enum import Enum
import tkinter as tk
from tkinter import messagebox, filedialog
import json
from Astar import *
import random

class CellType(Enum):
    WALL = 'W'
    PATH = ' '
    START = 'S'
    END = 'E'
    VISITED_PATH = 'P'

class MapUI:
    def __init__(self, root, width, height):
        self.root = root
        self.root.title("Particle Filter Map Builder")

        self.cell_size = 10
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.canvas = tk.Canvas(self.root, width=self.grid_width * self.cell_size, height=self.grid_height * self.cell_size, bg="white")
        self.canvas.pack()

        self.start_pos = None
        self.target_pos = None
        self.obstacles = set()
        
        self.grid = [[CellType.PATH for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        self.width = width
        self.height = height
        
        self.canvas.bind("<Button-1>", self.add_point)

        self.create_buttons()
        self.draw_grid()

    def create_buttons(self):
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.mode = None

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

        self.maze_button = tk.Button(self.button_frame, text="Build Maze", command=self.build_maze)
        self.maze_button.grid(row=0, column=7)

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
        self.grid = [[CellType.PATH for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.start_pos = None
        self.target_pos = None
        self.obstacles = set()
        self.mode = None
        self.draw_grid()
        self.root.title("Particle Filter Map Builder")

    def draw_grid(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                self.draw_cell(x, y, self.grid[y][x])

    def draw_cell(self, x, y, cell_type):
        x1, y1 = x * self.cell_size, y * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size

        if cell_type == CellType.START:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")
        elif cell_type == CellType.END:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")
        elif cell_type == CellType.WALL:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
        elif cell_type == CellType.VISITED_PATH:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black")
        else:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

    def add_point(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size

        if self.mode == "start":
            if self.start_pos:
                self.grid[self.start_pos[1]][self.start_pos[0]] = CellType.PATH
                self.draw_cell(self.start_pos[0], self.start_pos[1], CellType.PATH)
            self.grid[y][x] = CellType.START
            self.start_pos = (x, y)

        elif self.mode == "target":
            if self.target_pos:
                self.grid[self.target_pos[1]][self.target_pos[0]] = CellType.PATH
                self.draw_cell(self.target_pos[0], self.target_pos[1], CellType.PATH)
            self.grid[y][x] = CellType.END
            self.target_pos = (x, y)

        elif self.mode == "obstacle":
            if self.grid[y][x] == CellType.PATH:
                self.grid[y][x] = CellType.WALL
                self.obstacles.add((x, y))
            elif self.grid[y][x] == CellType.WALL:
                self.grid[y][x] = CellType.PATH
                self.obstacles.remove((x, y))

        self.draw_cell(x, y, self.grid[y][x])

    def save_map(self):
        if not self.start_pos or not self.target_pos:
            messagebox.showwarning("Incomplete Map", "Please set both start and target positions before saving.")
            return

        map_data = {
            'start': self.start_pos,
            'target': self.target_pos,
            'obstacles': list(self.obstacles),
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
        if not self.start_pos or not self.target_pos:
            messagebox.showwarning("Incomplete Map", "Please set both start and target positions before finding the path.")
            return

        start = self.start_pos
        dest = self.target_pos
        
        astar = Astar(self.grid_height, self.grid_width, self.obstacles, start, dest)
        path = astar.find_path()
        
        print(path)
        
        if not path:
            print("path not found via A*")
        
        for x, y in path:
            self.grid[y][x] = CellType.VISITED_PATH
            self.draw_cell(x, y, CellType.VISITED_PATH)

    def load_map(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, 'r') as file:
            map_data = json.load(file)

        self.clear()

        self.start_pos = tuple(map_data['start'])
        self.target_pos = tuple(map_data['target'])
        self.obstacles = set(tuple(obstacle) for obstacle in map_data['obstacles'])

        self.grid[self.start_pos[1]][self.start_pos[0]] = CellType.START
        self.grid[self.target_pos[1]][self.target_pos[0]] = CellType.END
        for x, y in self.obstacles:
            self.grid[y][x] = CellType.WALL

        self.draw_grid()

        self.root.title("Particle Filter Map Builder [Map Loaded]")
        messagebox.showinfo("Load Successful", f"Map loaded from {file_path}")
        
    def build_maze(self):
        
        # uses prims algo with dfs to make dynamic mazes for testing, this will not be part of the final project
        if not self.start_pos or not self.target_pos:
            messagebox.showwarning("Incomplete Map", "Please set both start and target positions before building the maze.")
            return
        
        self.obstacles = set()

        def is_valid(nx, ny):
            return 0 <= nx < self.grid_width and 0 <= ny < self.grid_height and self.grid[ny][nx] == CellType.WALL

        def neighbors(x, y):
            dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            result = []
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny):
                    result.append((nx, ny))
            return result

        def break_wall(x1, y1, x2, y2):
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            self.grid[my][mx] = CellType.PATH
            self.draw_cell(mx, my, CellType.PATH)

        start_x, start_y = self.start_pos
        end_x, end_y = self.target_pos

        self.grid = [[CellType.WALL for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        self.grid[start_y][start_x] = CellType.START
        self.draw_cell(start_x, start_y, CellType.START)

        stack = [(start_x, start_y)]
        while stack:
            x, y = stack[-1]
            nbrs = neighbors(x, y)
            if nbrs:
                nx, ny = random.choice(nbrs)
                break_wall(x, y, nx, ny)
                self.grid[ny][nx] = CellType.PATH
                self.draw_cell(nx, ny, CellType.PATH)
                stack.append((nx, ny))
            else:
                stack.pop()

        additional_paths = 3
        for _ in range(additional_paths):
            x, y = random.randint(0, self.grid_width-1), random.randint(0, self.grid_height-1)
            if self.grid[y][x] == CellType.WALL:
                self.grid[y][x] = CellType.PATH
                self.draw_cell(x, y, CellType.PATH)

        self.grid[end_y][end_x] = CellType.END
        self.draw_cell(end_x, end_y, CellType.END)

        self.obstacles = set((x, y) for y in range(self.grid_height) for x in range(self.grid_width) if self.grid[y][x] == CellType.WALL)
        
        for x, y in self.obstacles:
            self.draw_cell(x, y, CellType.WALL)

        self.root.title("Particle Filter Map Builder [Maze Built]")
        messagebox.showinfo("Maze Built", "The maze has been successfully built.")
            
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MapUI(
        root=root,
        width=500,
        height=500
    )
    
    root.mainloop()
