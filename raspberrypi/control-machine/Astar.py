import heapq
import math

class Astar:
    def __init__(self, row, col, obstacles, start, dest):
        self.row = row
        self.col = col        
        self.start = start
        self.dest = dest
        self.obstacles = set(tuple(obstacle) for obstacle in obstacles)
        
        self.g_score = {}
        self.f_score = {}
        self.open = heapq.heapify([])
        self.closed = set()
        
        # TODO
        self.came_from = {}
        
    def euclidean_distance(self, curr, dest):
        x, y = curr
        dest_x, dest_y = dest
        
        delta_x = dest_x - x
        delta_y = dest_y - y
        
        return math.sqrt(delta_x ** 2 + delta_y ** 2)
    
    
    def reconstruct_path(self, current):
        path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    
    def available_neighbors(self, curr):
        # down, right, up, left
        # no diagonals
        
        dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        r, c = curr
        
        neighbors = []
        
        for rdir, cdir in dirs:
            ccal = c - cdir
            rcal = r - rdir
            
            if (
                ccal in range(self.col)
                and rcal in range(self.row)
                and curr not in self.obstacles
            ):
                neighbors.append((rcal, ccal))
                
        return neighbors
    
    def find_path(self):
        starting_h_score = self.euclidean_distance(self.start, self.dest)
        starting_g_score = 0
        starting_f_score = starting_h_score + starting_g_score
        
        self.g_score[self.start] = 0
        self.f_score[self.start] = starting_f_score
        
        minheap = [(starting_f_score, self.start)]
        heapq.heapify(minheap)
        
        while minheap:
            curr = heapq.heappop(minheap)[1]
            
            if curr == self.dest:
                return self.reconstruct_path(curr)
            
            neighbors = self.available_neighbors(curr)
            
            neighbors_cost = self.g_score[curr] + 1
            
            for neighbor in neighbors:
                if neighbor not in self.f_score:
                    self.f_score[neighbor] = self.euclidean_distance(curr, self.dest)
                
                if neighbor not in self.g_score or self.g_score[neighbor] > neighbors_cost:
                    self.came_from[neighbor] = curr
                    self.g_score[neighbor] = neighbors_cost
                    final_cost = self.f_score[neighbor] + self.g_score[neighbor]
                    heapq.heappush(minheap, (final_cost, neighbor))
                    
        return []
                    
                    
            

        
    
    
        

