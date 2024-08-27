import json
from tkinter import messagebox

class FileHandler:
    
    @staticmethod
    def save_map(file_path, map_data):
        try:
            with open(file_path, "w") as file:
                json.dump(map_data, file)
            return True
        except IOError as e:
            messagebox.showerror("Save Error", f"Failed to save map: {str(e)}")
            return False

    @staticmethod
    def load_map(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except IOError as e:
            messagebox.showerror("Load Error", f"Failed to load map: {str(e)}")
            return None

    @staticmethod
    def save_path(file_path, path_data):
        try:
            with open(file_path, "w") as file:
                json.dump(path_data, file)
            return True
        except IOError as e:
            messagebox.showerror("Save Error", f"Failed to save path: {str(e)}")
            return False