from enum import Enum
import tkinter as tk
from tkinter import messagebox, filedialog
import json
from astar import AStar
import random

class CellType(Enum):
    WALL = "W"
    PATH = " "
    START = "S"
    END = "E"
    VISITED_PATH = "P"

class MapUI:
    def __init__(self, root, width, height):
        self._root = root
        self._root.title("Map Builder")

        self._cell_size = 50
        self._grid_width = width // self._cell_size
        self._grid_height = height // self._cell_size

        self._canvas = tk.Canvas(
            self._root,
            width=self._grid_width * self._cell_size,
            height=self._grid_height * self._cell_size,
            bg="white",
        )
        self._canvas.pack()

        self._start_pos = None
        self._target_pos = None
        self._obstacles = set()

        self._grid = [
            [CellType.PATH for _ in range(self._grid_width)]
            for _ in range(self._grid_height)
        ]

        self._pathfinder = None
        self._canvas.bind("<Button-1>", self._add_point)

        self._create_buttons()
        self._draw_grid()

    def _create_buttons(self):
        self._button_frame = tk.Frame(self._root)
        self._button_frame.pack()

        self._mode = None

        self._start_button = tk.Button(
            self._button_frame, text="Set Start", command=self._set_start_position
        )
        self._start_button.grid(row=0, column=0)

        self._target_button = tk.Button(
            self._button_frame, text="Set Target", command=self._set_target_position
        )
        self._target_button.grid(row=0, column=1)

        self._obstacle_button = tk.Button(
            self._button_frame, text="Set Obstacles", command=self._add_obstacle
        )
        self._obstacle_button.grid(row=0, column=2)

        self._clear_button = tk.Button(
            self._button_frame, text="Clear", command=self._clear
        )
        self._clear_button.grid(row=0, column=3)

        self._save_button = tk.Button(
            self._button_frame, text="Save Map", command=self._save_map
        )
        self._save_button.grid(row=0, column=4)

        self._load_button = tk.Button(
            self._button_frame, text="Load Map", command=self._load_map
        )
        self._load_button.grid(row=0, column=5)

        self._path_button = tk.Button(
            self._button_frame, text="Find Path", command=self._find_path
        )
        self._path_button.grid(row=0, column=6)

        self._maze_button = tk.Button(
            self._button_frame, text="Build Maze", command=self._build_maze
        )
        self._maze_button.grid(row=0, column=7)

        self._save_path_button = tk.Button(
            self._button_frame, text="Save Path", command=self._save_path
        )
        self._save_path_button.grid(row=1, column=2)

    def _set_start_position(self):
        self._mode = "start"
        self._root.title("Map Builder [Mode: Set Start Position]")

    def _set_target_position(self):
        self._mode = "target"
        self._root.title("Map Builder [Mode: Set Target Position]")

    def _add_obstacle(self):
        self._mode = "obstacle"
        self._root.title("Map Builder [Mode: Add Obstacles]")

    def _clear(self):
        self._canvas.delete("all")
        self._grid = [
            [CellType.PATH for _ in range(self._grid_width)]
            for _ in range(self._grid_height)
        ]
        self._start_pos = None
        self._target_pos = None
        self._obstacles = set()
        self._pathfinder = None
        self._mode = None
        self._draw_grid()
        self._root.title("Map Builder")

    def _draw_grid(self):
        for y in range(self._grid_height):
            for x in range(self._grid_width):
                self._draw_cell(x, y, self._grid[y][x])

    def _draw_cell(self, x, y, cell_type):
        x1, y1 = x * self._cell_size, y * self._cell_size
        x2, y2 = x1 + self._cell_size, y1 + self._cell_size

        color_map = {
            CellType.START: "green",
            CellType.END: "red",
            CellType.WALL: "black",
            CellType.VISITED_PATH: "blue",
            CellType.PATH: "white"
        }

        self._canvas.create_rectangle(x1, y1, x2, y2, fill=color_map[cell_type], outline="black")

    def _add_point(self, event):
        x, y = event.x // self._cell_size, event.y // self._cell_size

        if self._mode == "start":
            if self._start_pos:
                self._grid[self._start_pos[1]][self._start_pos[0]] = CellType.PATH
                self._draw_cell(self._start_pos[0], self._start_pos[1], CellType.PATH)
            self._grid[y][x] = CellType.START
            self._start_pos = (x, y)

        elif self._mode == "target":
            if self._target_pos:
                self._grid[self._target_pos[1]][self._target_pos[0]] = CellType.PATH
                self._draw_cell(self._target_pos[0], self._target_pos[1], CellType.PATH)
            self._grid[y][x] = CellType.END
            self._target_pos = (x, y)

        elif self._mode == "obstacle":
            if (x, y) in self._obstacles:
                self._grid[y][x] = CellType.PATH
                self._obstacles.remove((x, y))
            else:
                self._grid[y][x] = CellType.WALL
                self._obstacles.add((x, y))

        self._draw_cell(x, y, self._grid[y][x])

    def _find_path(self):
        if not self._start_pos or not self._target_pos:
            messagebox.showwarning("Warning", "Start or target position is not set!")
            return

        if self._pathfinder:
            for x, y in self._pathfinder:
                self._draw_cell(x, y, CellType.PATH)
        
        self._pathfinder = AStar(
            self._grid_height,
            self._grid_width,
            self._obstacles,
            self._start_pos,
            self._target_pos,
        ).find_path()

        if self._pathfinder:
            for x, y in self._pathfinder:
                if (x, y) not in [self._start_pos, self._target_pos]:
                    self._draw_cell(x, y, CellType.VISITED_PATH)
        else:
            messagebox.showinfo("No Path", "No path found!")

    def _save_map(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'w') as file:
                json.dump({
                    'start': self._start_pos,
                    'target': self._target_pos,
                    'obstacles': list(self._obstacles),
                    'grid': [[cell.value for cell in row] for row in self._grid]
                }, file)

    def _load_map(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r') as file:
                data = json.load(file)
                self._start_pos = tuple(data['start'])
                self._target_pos = tuple(data['target'])
                self._obstacles = set(tuple(obs) for obs in data['obstacles'])
                self._grid = [[CellType(cell).value for cell in row] for row in data['grid']]
                self._clear()
                self._draw_grid()

    def _build_maze(self):
        if self._start_pos is None or self._target_pos is None:
            messagebox.showwarning("Warning", "Start or target position is not set!")
            return
        
        self._clear()
        self._start_pos = (random.randint(0, self._grid_width - 1), random.randint(0, self._grid_height - 1))
        self._target_pos = (random.randint(0, self._grid_width - 1), random.randint(0, self._grid_height - 1))
        self._obstacles = set()
        
        for y in range(self._grid_height):
            for x in range(self._grid_width):
                if (x, y) not in [self._start_pos, self._target_pos]:
                    self._grid[y][x] = CellType.WALL if random.random() < 0.3 else CellType.PATH
        
        self._grid[self._start_pos[1]][self._start_pos[0]] = CellType.START
        self._grid[self._target_pos[1]][self._target_pos[0]] = CellType.END
        self._draw_grid()

    def _save_path(self):
        if not self._pathfinder:
            messagebox.showwarning("Warning", "No path found to save!")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'w') as file:
                json.dump(self._pathfinder, file)
