import random
import tkinter as tk
from tkinter import messagebox, filedialog
from astar import Astar
from file_handler import FileHandler
from celltype import CellType

class MapUI:
    def __init__(self, root, pxl_width, pxl_height, cell_size=50):
        self._root = root
        self._pxl_width = pxl_width
        self._pxl_height = pxl_height
        self._cell_size = cell_size
        self._width = pxl_width // self._cell_size
        self._height = pxl_height // self._cell_size
        self._pathfinder = Astar  # Pathfinding algorithm class

        # Canvas setup
        self._canvas = tk.Canvas(
            self._root,
            width=self._width * self._cell_size,
            height=self._height * self._cell_size,
            bg="white",
        )
        self._canvas.pack()
        self._canvas.bind("<Button-1>", self._add_point)

        self._init_grid()
        self._draw_grid()
        self._create_buttons()

    def _init_grid(self) -> None:
        self._start_pos = None
        self._target_pos = None
        self._obstacles = set()
        self._mode = None
        self._root.title("Particle Filter Map Builder")
        self._grid = [
            [CellType.EMPTY for _ in range(self._width)]
            for _ in range(self._height)
        ]

    def _draw_grid(self) -> None:
        for x in range(self._width):
            for y in range(self._height):
                self._draw_cell(x, y)

    def _set_cell_type(self, x, y, type: CellType) -> None:
        self._grid[y][x] = type

    def _get_cell_type(self, x, y) -> CellType:
        return self._grid[y][x]

    def _draw_cell(self, x, y) -> None:
        x1, y1 = x * self._cell_size, y * self._cell_size
        x2, y2 = x1 + self._cell_size, y1 + self._cell_size
        tag = f"cell-{x}-{y}"

        self._canvas.delete(tag)  # Clear the previous drawing on this cell

        match self._get_cell_type(x, y):
            case CellType.START:
                self._canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black", tags=tag)
            case CellType.END:
                self._canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black", tags=tag)
            case CellType.WALL:
                self._canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black", tags=tag)
            case CellType.PATH:
                self._canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black", tags=tag)
            case CellType.EMPTY:
                self._canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black", tags=tag)
            case _:
                raise ValueError("Unsupported Celltype")

    def _create_buttons(self) -> None:
        button_frame = tk.Frame(self._root)
        button_frame.pack()

        start_button = tk.Button(
            button_frame, text="Set Start", command=self.set_start_position
        )
        start_button.grid(row=0, column=0)

        target_button = tk.Button(
            button_frame, text="Set Target", command=self.set_target_position
        )
        target_button.grid(row=0, column=1)

        obstacle_button = tk.Button(
            button_frame, text="Set Obstacles", command=self.add_obstacle
        )
        obstacle_button.grid(row=0, column=2)

        clear_button = tk.Button(
            button_frame, text="Clear", command=self.clear
        )
        clear_button.grid(row=0, column=3)

        save_button = tk.Button(
            button_frame, text="Save Map", command=self.save_map
        )
        save_button.grid(row=1, column=0)

        load_button = tk.Button(
            button_frame, text="Load Map", command=self.load_map
        )
        load_button.grid(row=1, column=1)

        maze_button = tk.Button(
            button_frame, text="Build Maze", command=self.build_maze
        )
        maze_button.grid(row=1, column=2)

        path_button = tk.Button(
            button_frame, text="Find Path", command=self.find_path
        )
        path_button.grid(row=2, column=1)

        save_path_button = tk.Button(
            button_frame, text="Save Path", command=self.save_path
        )
        save_path_button.grid(row=2, column=2)

        self._buttons = {
            "start": start_button,
            "target": target_button,
            "obstacle": obstacle_button,
        }

    def _update_button_styles(self, active_mode: str) -> None:
        for mode, button in self._buttons.items():
            if mode == active_mode:
                button.config(bg="lightblue")
            else:
                button.config(bg="SystemButtonFace")

    def set_start_position(self) -> None:
        self._mode = "start"
        self._update_button_styles(self._mode)
        self._root.title("Particle Filter Map Builder [Mode: Set Start Position]")

    def set_target_position(self) -> None:
        self._mode = "target"
        self._update_button_styles(self._mode)
        self._root.title("Particle Filter Map Builder [Mode: Set Target Position]")

    def add_obstacle(self) -> None:
        self._mode = "obstacle"
        self._update_button_styles(self._mode)
        self._root.title("Particle Filter Map Builder [Mode: Add Obstacles]")

    def clear(self) -> None:
        self._canvas.delete("all")
        self._init_grid()
        self._draw_grid()

    def _add_point(self, event) -> None:
        point = (event.x // self._cell_size, event.y // self._cell_size)

        match self._mode:
            case "start":
                if self._start_pos:
                    self._set_cell_type(*self._start_pos, CellType.EMPTY)
                    self._draw_cell(*self._start_pos)
                if point == self._target_pos:
                    messagebox.showwarning("Warning", "Cannot set Start at Target position!")
                    return
                self._start_pos = point
                self._set_cell_type(*point, CellType.START)
                self._draw_cell(*point)
            case "target":
                if self._target_pos:
                    self._set_cell_type(*self._target_pos, CellType.EMPTY)
                    self._draw_cell(*self._target_pos)
                if point == self._start_pos:
                    messagebox.showwarning("Warning", "Cannot set Target at Start position!")
                    return
                self._target_pos = point
                self._set_cell_type(*point, CellType.END)
                self._draw_cell(*point)
            case "obstacle":
                if point not in {self._start_pos, self._target_pos}:
                    if self._get_cell_type(*point) == CellType.WALL:
                        self._set_cell_type(*point, CellType.EMPTY)
                        self._obstacles.remove(point)
                    else:
                        self._set_cell_type(*point, CellType.WALL)
                        self._obstacles.add(point)
                    self._draw_cell(*point)
            case _:
                messagebox.showwarning("No Mode Selected", "Please select a mode first.")

    def save_map(self) -> None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
        )
        if file_path:
            map_data = {
                "width": self._width,
                "height": self._height,
                "start_pos": self._start_pos,
                "target_pos": self._target_pos,
                "obstacles": list(self._obstacles),
            }
            if FileHandler.save_map(file_path, map_data):
                messagebox.showinfo("Success", "Map saved successfully.")

    def load_map(self) -> None:
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
        )
        if file_path:
            map_data = FileHandler.load_map(file_path)
            if map_data:
                self.clear()
                self._width = map_data["width"]
                self._height = map_data["height"]
                self._start_pos = tuple(map_data["start_pos"])
                self._target_pos = tuple(map_data["target_pos"])
                self._obstacles = set(tuple(x) for x in map_data["obstacles"])

                self._set_cell_type(*self._start_pos, CellType.START)
                self._set_cell_type(*self._target_pos, CellType.END)
                for obs in self._obstacles:
                    self._set_cell_type(*obs, CellType.WALL)

                self._draw_grid()
                messagebox.showinfo("Success", "Map loaded successfully.")

    def save_path(self) -> None:
        if not self._start_pos or not self._target_pos:
            messagebox.showwarning("Warning", "Start or Target positions are not set!")
            return

        path = self._find_path()  # Call _find_path to get the path
        if path:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json")],
            )
            if file_path:
                if FileHandler.save_path(file_path, path):
                    messagebox.showinfo("Success", "Path saved successfully.")

    def build_maze(self) -> None:
        # Ensures start and target positions are set before maze generation
        if not self._start_pos or not self._target_pos:
            messagebox.showwarning(
                "Incomplete Map",
                "Please set both start and target positions before building the maze.",
            )
            return

        def is_valid(x, y):
            return 0 <= x < self._width and 0 <= y < self._height and self._grid[y][x] == CellType.WALL

        def neighbors(x, y):
            dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            return [(x + dx, y + dy) for dx, dy in dirs if is_valid(x + dx, y + dy)]

        def break_wall(x1, y1, x2, y2):
            self._set_cell_type((x1 + x2) // 2, (y1 + y2) // 2, CellType.EMPTY)

        # Initialize the grid as entirely filled with walls
        self._grid = [[CellType.WALL for _ in range(self._width)] for _ in range(self._height)]
        self._set_cell_type(*self._start_pos, CellType.START)
        self._set_cell_type(*self._target_pos, CellType.END)
        self._obstacles.clear()

        # Begin maze generation using DFS with a stack
        stack = [self._start_pos]
        while stack:
            curr = stack[-1]
            nbrs = neighbors(*curr)
            if nbrs:
                nbr = random.choice(nbrs)
                break_wall(*curr, *nbr)
                self._set_cell_type(*nbr, CellType.EMPTY)
                stack.append(nbr)
            else:
                stack.pop()

        # Optionally add random additional paths
        additional_paths = random.randint(1, 5)
        for _ in range(additional_paths):
            x, y = random.randint(0, self._width - 1), random.randint(0, self._height - 1)
            if self._grid[y][x] == CellType.WALL:
                self._set_cell_type(x, y, CellType.EMPTY)

        # Update obstacle set and redraw the grid
        self._obstacles = {(x, y) for y in range(self._height) for x in range(self._width) if self._grid[y][x] == CellType.WALL}
        self._draw_grid()

        # Notify user of successful maze generation
        self._root.title("Particle Filter Map Builder [Maze Built]")
        messagebox.showinfo("Maze Built", "The maze has been successfully built.")

    def find_path(self) -> None:
        if not self._start_pos or not self._target_pos:
            messagebox.showwarning("Warning", "Start or Target positions are not set!")
            return

        path = self._find_path()
        if path:
            for (x, y) in path:
                if (x, y) not in {self._start_pos, self._target_pos}:
                    self._set_cell_type(x, y, CellType.PATH)
                    self._draw_cell(x, y)
            messagebox.showinfo("Path Found", "A path has been found!")
        else:
            messagebox.showwarning("No Path Found", "No path could be found between the start and target.")

    def _find_path(self) -> list:
        pathfinder = self._pathfinder(
            col=self._height, 
            row=self._width, 
            obstacles=self._obstacles, 
            start=self._start_pos, 
            dest=self._target_pos
            )
        return pathfinder.find_path()
        

