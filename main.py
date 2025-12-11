# -*- coding: utf-8 -*-
"""
Pathfinding Visualizer
@author: praisejamesx
"""

import pygame
import sys
import random
import time
import math
from collections import deque

# Import the Cell class
try:
    from Cell_2D import Cell, make_grid, decorate_grid
except:
    # Fallback Cell class
    class Cell:
        def __init__(self, pos, status, constants, istarget=False):
            self.pos = pos
            self.status = status
            self.istarget = istarget
            self.tile_size = constants['TILESIZE']
            self.colors = constants['COLORS']
            margin = constants['MARGIN']
            realx = pos[0] * constants['TILESIZE']
            realy = pos[1] * constants['TILESIZE']
            self.rect = pygame.Rect(realx + margin, realy + margin, 
                                   self.tile_size - 2*margin, self.tile_size - 2*margin)
            self.neighbours = []
            self.parent = None
            self.f_cost = float('inf')
            self.h_cost = float('inf')
            self.g_cost = float('inf')
            self.visited_time = 0
        
        def add_neighbours(self, cell_list):
            coords = self.get_neighbour_coords()
            self.neighbours = []
            for c in coords:
                if c in cell_list:
                    self.neighbours.append(cell_list[c])
        
        def get_neighbour_coords(self):
            vectors = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if not (dx == 0 == dy):
                        neighbour = (self.pos[0] + dx, self.pos[1] + dy)
                        if self.in_bounds(neighbour):
                            vectors.append(neighbour)
            return vectors
        
        def in_bounds(self, pos):
            return 0 <= pos[0] < 20 and 0 <= pos[1] < 20
        
        def update(self, new_status, surf):
            if self.status != new_status:
                self.status = new_status
                self.draw_cell(surf)
        
        def draw_cell(self, surf):
            if self.istarget:
                col = self.colors['TARGET_COL']
            elif self.status == 'blocked':
                col = self.colors['BLOCK_COL']
            elif self.status == 'start':
                col = self.colors['START_COL']
            elif self.status == 'path':
                col = self.colors['PATH_COL']
            elif self.status == 'active':
                col = self.colors['ACTIVE_COL']
            elif self.status == 'closed':
                col = self.colors['CLOSED_COL']
            else:
                col = self.colors['EMPTY_COL']
            
            pygame.draw.rect(surf, col, self.rect)
        
        def get_h(self, goal_pos):
            dx = abs(goal_pos[0] - self.pos[0])
            dy = abs(goal_pos[1] - self.pos[1])
            self.h_cost = 10 * (dx + dy)
        
        def get_distance_to(self, other_cell):
            dx = abs(other_cell.pos[0] - self.pos[0])
            dy = abs(other_cell.pos[1] - self.pos[1])
            if dx == 1 and dy == 1:
                return 14
            return 10
        
        def get_g(self, neighbour):
            distance = self.get_distance_to(neighbour)
            new_g = neighbour.g_cost + distance
            if new_g < self.g_cost:
                self.g_cost = new_g
                return True
            return False
        
        def get_f(self):
            self.f_cost = self.g_cost + self.h_cost
        
        def reset(self):
            self.parent = None
            self.f_cost = float('inf')
            self.h_cost = float('inf')
            self.g_cost = float('inf')
            self.visited_time = 0
    
    def make_grid(constants, surface=None):
        cell_list = {}
        for x in range(constants['X']):
            for y in range(constants['Y']):
                cell_list[(x, y)] = Cell((x, y), 'empty', constants)
        
        for cell in cell_list.values():
            cell.add_neighbours(cell_list)
            if surface:
                cell.draw_cell(surface)
        
        return cell_list
    
    def decorate_grid(surface, cell_list, obstacle_list):
        if obstacle_list:
            for pos in obstacle_list:
                if pos in cell_list:
                    cell_list[pos].update('blocked', surface)
        return cell_list

#------------- CONSTANTS ---------------
colordict = {
    'EMPTY_COL': (255, 255, 255),
    'BLOCK_COL': (50, 50, 70),
    'ACTIVE_COL': (100, 200, 100),
    'CLOSED_COL': (200, 100, 100),
    'TARGET_COL': (100, 100, 200),
    'PATH_COL': (200, 100, 200),
    'START_COL': (150, 100, 200),
    'BG_COL': (30, 30, 40),
    'UI_BG': (50, 50, 60),
    'UI_TEXT': (220, 220, 220),
    'BUTTON_COL': (80, 120, 200),
    'BUTTON_HOVER': (100, 150, 220),
    'BUTTON_ACTIVE': (150, 200, 255),
    'TAB_ACTIVE': (70, 100, 180),
    'TAB_INACTIVE': (60, 80, 160),
    'GRID_LINE': (60, 60, 70)
}

# Algorithms organized by category
ALGORITHMS = {
    "Basic": [
        "A* Search",
        "Dijkstra's Algorithm",
        "Breadth-First Search",
        "Depth-First Search",
        "Greedy Best-First"
    ],
    "Advanced": [
        "Bidirectional Search",
        "Jump Point Search",
        "IDA* Search"
    ],
    "Heuristic": [
        "Swarm Algorithm",
        "Convergent Swarm"
    ]
}

# Maze types
MAZE_TYPES = [
    "Random Obstacles",
    "Recursive Division",
    "Prim's Algorithm",
    "Kruskal's Algorithm",
    "Depth-First Search Maze",
    "Cellular Automata",
    "Spiral Maze",
    "Sidewinder Maze",
    "Binary Tree Maze",
    "Eller's Algorithm"
]

constants = {
    'TILESIZE': 20,
    'MARGIN': 1,
    'X': 40,
    'Y': 30,
    'FPS': 60,
    'SEARCH_SPEED': 30,
    'COLORS': colordict,
    'GOALPOS': (38, 28),
    'STARTPOS': (2, 2),
    'SIDEBAR_WIDTH': 250,
    'TAB_HEIGHT': 30
}

#------------ UI COMPONENTS ------------

class Button:
    def __init__(self, x, y, w, h, text, is_toggle=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = constants['COLORS']['BUTTON_COL']
        self.hover_color = constants['COLORS']['BUTTON_HOVER']
        self.active_color = constants['COLORS']['BUTTON_ACTIVE']
        self.current_color = self.color
        self.font = pygame.font.SysFont('Arial', 12)
        self.is_toggle = is_toggle
        self.active = False
        self.hovered = False
    
    def draw(self, surface):
        # Determine color
        if self.active and self.is_toggle:
            color = self.active_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.color
        
        # Draw button
        pygame.draw.rect(surface, color, self.rect, border_radius=3)
        pygame.draw.rect(surface, constants['COLORS']['UI_TEXT'], self.rect, 1, border_radius=3)
        
        # Draw text (with word wrap)
        words = self.text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = self.font.size(test_line)[0]
            
            if test_width <= self.rect.width - 10:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw each line
        total_height = len(lines) * self.font.get_height()
        start_y = self.rect.centery - total_height // 2
        
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, constants['COLORS']['UI_TEXT'])
            text_rect = text_surf.get_rect(center=(self.rect.centerx, start_y + i * self.font.get_height()))
            surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos, clicked):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered and clicked:
            if self.is_toggle:
                self.active = not self.active
            return True
        return False
    
    def set_active(self, active):
        if self.is_toggle:
            self.active = active

class TabButton:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = constants['COLORS']['TAB_INACTIVE']
        self.active_color = constants['COLORS']['TAB_ACTIVE']
        self.current_color = self.color
        self.font = pygame.font.SysFont('Arial', 14, bold=True)
        self.active = False
        self.hovered = False
    
    def draw(self, surface):
        color = self.active_color if self.active else self.current_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, constants['COLORS']['UI_TEXT'], self.rect, 1)
        
        text_surf = self.font.render(self.text, True, constants['COLORS']['UI_TEXT'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos, clicked):
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = constants['COLORS']['BUTTON_HOVER'] if self.hovered else constants['COLORS']['TAB_INACTIVE']
        
        if self.hovered and clicked:
            return True
        return False
    
    def set_active(self, active):
        self.active = active

#------------ ALGORITHM IMPLEMENTATIONS ------------

class PathfindingAlgorithms:
    @staticmethod
    def astar_step(open_set, closed_set, goal_pos, cells, surface):
        """A* Algorithm"""
        if not open_set:
            return open_set, closed_set, None, True, False
        
        current = min(open_set, key=lambda c: (c.f_cost, c.h_cost))
        open_set.remove(current)
        closed_set.append(current)
        
        if current.status != 'start':
            current.update('closed', surface)
        
        if current.istarget:
            return open_set, closed_set, current, True, True
        
        for neighbor in current.neighbours:
            if neighbor.status == 'blocked' or neighbor in closed_set:
                continue
            
            new_g = current.g_cost + current.get_distance_to(neighbor)
            
            if new_g < neighbor.g_cost or neighbor not in open_set:
                neighbor.parent = current
                neighbor.g_cost = new_g
                neighbor.get_h(goal_pos)
                neighbor.get_f()
                
                if neighbor not in open_set:
                    neighbor.update('active', surface)
                    open_set.append(neighbor)
        
        return open_set, closed_set, current, False, False
    
    @staticmethod
    def dijkstra_step(open_set, closed_set, goal_pos, cells, surface):
        """Dijkstra's Algorithm"""
        if not open_set:
            return open_set, closed_set, None, True, False
        
        open_set.sort(key=lambda c: c.g_cost)
        current = open_set.pop(0)
        closed_set.append(current)
        
        if current.status != 'start':
            current.update('closed', surface)
        
        if current.istarget:
            return open_set, closed_set, current, True, True
        
        for neighbor in current.neighbours:
            if neighbor.status == 'blocked' or neighbor in closed_set:
                continue
            
            new_g = current.g_cost + 10
            
            if new_g < neighbor.g_cost or neighbor not in open_set:
                neighbor.parent = current
                neighbor.g_cost = new_g
                
                if neighbor not in open_set:
                    neighbor.update('active', surface)
                    open_set.append(neighbor)
        
        return open_set, closed_set, current, False, False
    
    @staticmethod
    def bfs_step(queue, visited, goal_pos, cells, surface):
        """Breadth-First Search"""
        if not queue:
            return queue, visited, None, True, False
        
        current = queue.popleft()
        visited.append(current)
        
        if current.status != 'start':
            current.update('closed', surface)
        
        if current.istarget:
            return queue, visited, current, True, True
        
        for neighbor in current.neighbours:
            if (neighbor.status == 'blocked' or 
                neighbor in visited or 
                neighbor in queue):
                continue
            
            neighbor.parent = current
            neighbor.update('active', surface)
            queue.append(neighbor)
        
        return queue, visited, current, False, False
    
    @staticmethod
    def dfs_step(stack, visited, goal_pos, cells, surface):
        """Depth-First Search"""
        if not stack:
            return stack, visited, None, True, False
        
        current = stack.pop()
        visited.append(current)
        
        if current.status != 'start':
            current.update('closed', surface)
        
        if current.istarget:
            return stack, visited, current, True, True
        
        for neighbor in reversed(current.neighbours):
            if (neighbor.status == 'blocked' or 
                neighbor in visited or 
                neighbor in stack):
                continue
            
            neighbor.parent = current
            neighbor.update('active', surface)
            stack.append(neighbor)
        
        return stack, visited, current, False, False
    
    @staticmethod
    def greedy_step(open_set, closed_set, goal_pos, cells, surface):
        """Greedy Best-First Search"""
        if not open_set:
            return open_set, closed_set, None, True, False
        
        current = min(open_set, key=lambda c: c.h_cost)
        open_set.remove(current)
        closed_set.append(current)
        
        if current.status != 'start':
            current.update('closed', surface)
        
        if current.istarget:
            return open_set, closed_set, current, True, True
        
        for neighbor in current.neighbours:
            if (neighbor.status == 'blocked' or 
                neighbor in closed_set or 
                neighbor in open_set):
                continue
            
            neighbor.parent = current
            neighbor.get_h(goal_pos)
            neighbor.update('active', surface)
            open_set.append(neighbor)
        
        return open_set, closed_set, current, False, False
    
    @staticmethod
    def bidirectional_step(open_set_start, open_set_goal, closed_set_start, closed_set_goal, 
                          goal_pos, cells, surface):
        """Bidirectional Search - FIXED VERSION"""
        # Check if either open set is empty
        if not open_set_start or not open_set_goal:
            return open_set_start, open_set_goal, closed_set_start, closed_set_goal, None, None, True, False
        
        meeting_cell = None
        
        # Search from start
        if open_set_start:
            current_start = min(open_set_start, key=lambda c: c.f_cost)
            open_set_start.remove(current_start)
            closed_set_start.append(current_start)
            
            if current_start.status != 'start':
                current_start.update('closed', surface)
            
            # Check if meeting point found
            if current_start in closed_set_goal:
                meeting_cell = current_start
                return open_set_start, open_set_goal, closed_set_start, closed_set_goal, current_start, meeting_cell, True, True
            
            for neighbor in current_start.neighbours:
                if neighbor.status == 'blocked' or neighbor in closed_set_start:
                    continue
                
                new_g = current_start.g_cost + current_start.get_distance_to(neighbor)
                if new_g < neighbor.g_cost or neighbor not in open_set_start:
                    neighbor.parent = current_start
                    neighbor.g_cost = new_g
                    neighbor.get_h(goal_pos)
                    neighbor.get_f()
                    
                    if neighbor not in open_set_start:
                        neighbor.update('active', surface)
                        open_set_start.append(neighbor)
        
        # Search from goal
        if open_set_goal:
            current_goal = min(open_set_goal, key=lambda c: c.f_cost)
            open_set_goal.remove(current_goal)
            closed_set_goal.append(current_goal)
            
            if current_goal.status != 'target':
                current_goal.update('closed', surface)
            
            # Check if meeting point found
            if current_goal in closed_set_start:
                meeting_cell = current_goal
                return open_set_start, open_set_goal, closed_set_start, closed_set_goal, current_goal, meeting_cell, True, True
            
            for neighbor in current_goal.neighbours:
                if neighbor.status == 'blocked' or neighbor in closed_set_goal:
                    continue
                
                new_g = current_goal.g_cost + current_goal.get_distance_to(neighbor)
                if new_g < neighbor.g_cost or neighbor not in open_set_goal:
                    neighbor.parent = current_goal
                    neighbor.g_cost = new_g
                    # For goal search, heuristic is to start
                    neighbor.get_h(cells[goal_pos].pos)  # This should be start pos, but we need start pos
                    neighbor.get_f()
                    
                    if neighbor not in open_set_goal:
                        neighbor.update('active', surface)
                        open_set_goal.append(neighbor)
        
        return open_set_start, open_set_goal, closed_set_start, closed_set_goal, None, meeting_cell, False, False
    
    @staticmethod
    def jps_step(open_set, closed_set, goal_pos, cells, surface):
        """Jump Point Search (simplified)"""
        if not open_set:
            return open_set, closed_set, None, True, False
        
        current = min(open_set, key=lambda c: (c.f_cost, c.h_cost))
        open_set.remove(current)
        closed_set.append(current)
        
        if current.status != 'start':
            current.update('closed', surface)
        
        if current.istarget:
            return open_set, closed_set, current, True, True
        
        # Simplified jump point logic
        for neighbor in current.neighbours:
            if neighbor.status == 'blocked' or neighbor in closed_set:
                continue
            
            new_g = current.g_cost + current.get_distance_to(neighbor)
            
            if new_g < neighbor.g_cost or neighbor not in open_set:
                neighbor.parent = current
                neighbor.g_cost = new_g
                neighbor.get_h(goal_pos)
                neighbor.get_f()
                
                if neighbor not in open_set:
                    neighbor.update('active', surface)
                    open_set.append(neighbor)
        
        return open_set, closed_set, current, False, False
    
    @staticmethod
    def idastar_step(open_set, closed_set, goal_pos, cells, surface, threshold, next_threshold):
        """IDA* Search"""
        if not open_set:
            return open_set, closed_set, None, True, False, threshold, next_threshold
        
        current = min(open_set, key=lambda c: c.f_cost)
        
        if current.f_cost > threshold:
            next_threshold = min(next_threshold, current.f_cost)
            return open_set, closed_set, current, False, False, threshold, next_threshold
        
        open_set.remove(current)
        closed_set.append(current)
        
        if current.status != 'start':
            current.update('closed', surface)
        
        if current.istarget:
            return open_set, closed_set, current, True, True, threshold, next_threshold
        
        for neighbor in current.neighbours:
            if neighbor.status == 'blocked' or neighbor in closed_set:
                continue
            
            new_g = current.g_cost + current.get_distance_to(neighbor)
            
            if new_g < neighbor.g_cost or neighbor not in open_set:
                neighbor.parent = current
                neighbor.g_cost = new_g
                neighbor.get_h(goal_pos)
                neighbor.get_f()
                
                if neighbor not in open_set:
                    neighbor.update('active', surface)
                    open_set.append(neighbor)
        
        return open_set, closed_set, current, False, False, threshold, next_threshold
    
    @staticmethod
    def swarm_step(open_set, closed_set, goal_pos, cells, surface, pheromones):
        """Swarm Algorithm (simplified)"""
        if not open_set:
            return open_set, closed_set, None, True, False
        
        # Add pheromone influence to cost
        for cell in open_set:
            pheromone = pheromones.get(cell.pos, 1.0)
            cell.f_cost = (cell.g_cost + cell.h_cost) * pheromone
        
        current = min(open_set, key=lambda c: c.f_cost)
        open_set.remove(current)
        closed_set.append(current)
        
        if current.status != 'start':
            current.update('closed', surface)
        
        if current.istarget:
            return open_set, closed_set, current, True, True
        
        # Update pheromones
        pheromones[current.pos] = pheromones.get(current.pos, 1.0) * 1.1
        
        for neighbor in current.neighbours:
            if neighbor.status == 'blocked' or neighbor in closed_set:
                continue
            
            new_g = current.g_cost + current.get_distance_to(neighbor)
            
            if new_g < neighbor.g_cost or neighbor not in open_set:
                neighbor.parent = current
                neighbor.g_cost = new_g
                neighbor.get_h(goal_pos)
                neighbor.get_f()
                
                if neighbor not in open_set:
                    neighbor.update('active', surface)
                    open_set.append(neighbor)
        
        return open_set, closed_set, current, False, False

#------------ MAZE GENERATION ------------

class MazeGenerator:
    @staticmethod
    def random_obstacles(cells, start_pos, goal_pos, width, height, surface, density=0.3):
        """Random Obstacles"""
        for cell in cells.values():
            if cell.pos != start_pos and cell.pos != goal_pos:
                if random.random() < density:
                    cell.update('blocked', surface)
                else:
                    cell.update('empty', surface)
    
    @staticmethod
    def recursive_division(cells, start_pos, goal_pos, width, height, surface):
        """Recursive Division Maze"""
        # Clear grid
        for cell in cells.values():
            if cell.pos != start_pos and cell.pos != goal_pos:
                cell.update('empty', surface)
        
        def divide(x, y, w, h, orientation):
            if w < 3 or h < 3:
                return
            
            horizontal = orientation
            
            # Wall position
            wx = x + (0 if horizontal else random.randint(1, w-2))
            wy = y + (random.randint(1, h-2) if horizontal else 0)
            
            # Passage position
            px = wx + (0 if horizontal else random.randint(0, w-1))
            py = wy + (random.randint(0, h-1) if horizontal else 0)
            
            # Draw wall
            for i in range(w if horizontal else h):
                cx = wx + (i if horizontal else 0)
                cy = wy + (0 if horizontal else i)
                
                if (cx, cy) == (px, py) or (cx, cy) == start_pos or (cx, cy) == goal_pos:
                    continue
                
                if 0 <= cx < width and 0 <= cy < height:
                    cells[(cx, cy)].update('blocked', surface)
            
            # Recursively divide
            if horizontal:
                divide(x, y, w, wy-y, not horizontal)
                divide(x, wy+1, w, y+h-wy-1, not horizontal)
            else:
                divide(x, y, wx-x, h, not horizontal)
                divide(wx+1, y, x+w-wx-1, h, not horizontal)
        
        divide(0, 0, width, height, random.choice([True, False]))
    
    @staticmethod
    def prims_algorithm(cells, start_pos, goal_pos, width, height, surface):
        """Prim's Algorithm Maze"""
        # Start with all walls
        for cell in cells.values():
            if cell.pos != start_pos and cell.pos != goal_pos:
                cell.update('blocked', surface)
        
        # Start with a random cell
        start_x = random.randint(1, width-2)
        start_y = random.randint(1, height-2)
        cells[(start_x, start_y)].update('empty', surface)
        
        frontier = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = start_x + dx, start_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                frontier.append((nx, ny))
        
        while frontier:
            fx, fy = random.choice(frontier)
            frontier.remove((fx, fy))
            
            # Find neighbors
            neighbors = []
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = fx + dx, fy + dy
                if 0 <= nx < width and 0 <= ny < height and cells[(nx, ny)].status == 'empty':
                    neighbors.append((nx, ny))
            
            if neighbors:
                nx, ny = random.choice(neighbors)
                # Carve path
                mx, my = (fx + nx) // 2, (fy + ny) // 2
                cells[(fx, fy)].update('empty', surface)
                cells[(mx, my)].update('empty', surface)
                
                # Add new frontier
                for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    nx, ny = fx + dx, fy + dy
                    if 0 <= nx < width and 0 <= ny < height and cells[(nx, ny)].status == 'blocked':
                        frontier.append((nx, ny))
    
    @staticmethod
    def cellular_automata(cells, start_pos, goal_pos, width, height, surface, iterations=4):
        """Cellular Automata Maze"""
        # Random initial state
        for cell in cells.values():
            if cell.pos != start_pos and cell.pos != goal_pos:
                if random.random() < 0.45:
                    cell.update('blocked', surface)
                else:
                    cell.update('empty', surface)
        
        # Apply rules
        for _ in range(iterations):
            new_state = {}
            for x in range(width):
                for y in range(height):
                    if (x, y) == start_pos or (x, y) == goal_pos:
                        continue
                    
                    # Count wall neighbors
                    wall_count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                if cells[(nx, ny)].status == 'blocked':
                                    wall_count += 1
                    
                    # Apply rules
                    if cells[(x, y)].status == 'blocked':
                        new_state[(x, y)] = 'empty' if wall_count < 3 else 'blocked'
                    else:
                        new_state[(x, y)] = 'blocked' if wall_count > 4 else 'empty'
            
            # Update grid
            for pos, status in new_state.items():
                if pos != start_pos and pos != goal_pos:
                    cells[pos].update(status, surface)
    
    @staticmethod
    def spiral_maze(cells, start_pos, goal_pos, width, height, surface):
        """Spiral Maze"""
        # Start with all walls
        for cell in cells.values():
            if cell.pos != start_pos and cell.pos != goal_pos:
                cell.update('blocked', surface)
        
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        dir_idx = 0
        x, y = width // 4, height // 4
        step = 2
        
        while 0 <= x < width and 0 <= y < height:
            for _ in range(step):
                # Carve path
                for i in range(3):
                    nx, ny = x + directions[dir_idx][0] * i, y + directions[dir_idx][1] * i
                    if 0 <= nx < width and 0 <= ny < height:
                        cells[(nx, ny)].update('empty', surface)
                
                x += directions[dir_idx][0] * 3
                y += directions[dir_idx][1] * 3
                
                if not (0 <= x < width and 0 <= y < height):
                    break
            
            dir_idx = (dir_idx + 1) % 4
            if dir_idx % 2 == 0:
                step += 2

#------------ MAIN VISUALIZER ------------

class PathfindingVisualizer:
    def __init__(self):
        self.sidebar_width = constants['SIDEBAR_WIDTH']
        self.grid_width = constants['X'] * constants['TILESIZE']
        self.grid_height = constants['Y'] * constants['TILESIZE']
        self.total_width = self.grid_width + self.sidebar_width
        self.total_height = self.grid_height
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.total_width, self.total_height))
        pygame.display.set_caption("Ultimate Pathfinding Visualizer - Tabbed Interface")
        self.clock = pygame.time.Clock()
        
        # Surfaces
        self.grid_surf = pygame.Surface((self.grid_width, self.grid_height))
        self.sidebar_surf = pygame.Surface((self.sidebar_width, self.total_height))
        
        # Grid
        self.cells = make_grid(constants, self.grid_surf)
        self.obstacles = []
        
        # Positions
        self.start_pos = constants['STARTPOS']
        self.goal_pos = constants['GOALPOS']
        
        # Current selections
        self.current_algo_category = "Basic"
        self.current_algo_category_num = 0
        self.current_algorithm = 0  # Index in current category
        self.current_maze = 0
        
        # Tab system
        self.tabs = ["Algorithms", "Mazes", "Controls"]
        self.current_tab = 0  # 0: Algorithms, 1: Mazes, 2: Controls
        
        # Search state
        self.searching = False
        self.paused = False
        self.finished = False
        self.path_found = False
        
        # Algorithm state
        self.open_set = []
        self.closed_set = []
        self.queue = deque()
        self.stack = []
        self.visited = []
        
        # Advanced algorithm states
        self.open_set_start = []
        self.open_set_goal = []
        self.closed_set_start = []
        self.closed_set_goal = []
        self.pheromones = {}
        self.ida_threshold = 0
        self.ida_next_threshold = float('inf')
        
        # Statistics
        self.stats = {
            'visited': 0,
            'path_length': 0,
            'time': 0,
            'start_time': 0
        }
        
        # Drawing
        self.drawing = False
        self.draw_mode = 'block'
        self.last_drawn = None
        
        # UI Elements
        self.create_ui()
        
        # Initialize grid
        self.initialize_grid()
    
    def initialize_grid(self):
        """Initialize the grid"""
        self.grid_surf.fill(constants['COLORS']['BG_COL'])
        
        # Draw grid lines
        for x in range(constants['X'] + 1):
            pygame.draw.line(self.grid_surf, constants['COLORS']['GRID_LINE'],
                           (x * constants['TILESIZE'], 0),
                           (x * constants['TILESIZE'], self.grid_height))
        for y in range(constants['Y'] + 1):
            pygame.draw.line(self.grid_surf, constants['COLORS']['GRID_LINE'],
                           (0, y * constants['TILESIZE']),
                           (self.grid_width, y * constants['TILESIZE']))
        
        # Set start and goal
        self.cells[self.start_pos].update('start', self.grid_surf)
        self.cells[self.goal_pos].istarget = True
        self.cells[self.goal_pos].update('target', self.grid_surf)
    
    def create_ui(self):
        """Create tabbed sidebar UI"""
        self.tab_buttons = []
        self.algo_buttons = []
        self.maze_buttons = []
        self.control_buttons = []
        
        # Create tab buttons
        tab_width = self.sidebar_width // 3
        for i, tab_name in enumerate(self.tabs):
            tab = TabButton(i * tab_width, 0, tab_width, constants['TAB_HEIGHT'], tab_name)
            self.tab_buttons.append(tab)
        
        # Make first tab active
        self.tab_buttons[0].active = True
        
        # Create algorithm buttons (will be shown when Algorithms tab is active)
        button_width = self.sidebar_width - 20
        button_height = 30
        start_y = constants['TAB_HEIGHT'] + 10
        
        # Category tabs for algorithms
        self.category_buttons = []
        category_width = self.sidebar_width // 3
        categories = list(ALGORITHMS.keys())
        for i, category in enumerate(categories):
            btn = TabButton(i * category_width, start_y, category_width, 25, category[:6])
            self.category_buttons.append(btn)
        
        # Make first category active
        self.category_buttons[0].active = True
        
        # Algorithm buttons for current category
        algo_start_y = start_y + 35
        current_category = list(ALGORITHMS.keys())[0]
        for i, algo in enumerate(ALGORITHMS[current_category]):
            btn = Button(10, algo_start_y + i * (button_height + 5), 
                        button_width, button_height, algo, is_toggle=True)
            self.algo_buttons.append(btn)
        
        # Make first algorithm active
        if self.algo_buttons:
            self.algo_buttons[0].active = True
        
        # Maze buttons (will be shown when Mazes tab is active)
        maze_start_y = start_y + 10
        for i, maze in enumerate(MAZE_TYPES):
            btn = Button(10, maze_start_y + i * (button_height + 5), 
                        button_width, button_height, maze, is_toggle=True)
            self.maze_buttons.append(btn)
        
        # Make first maze active
        if self.maze_buttons:
            self.maze_buttons[0].active = True
        
        # Control buttons (will be shown when Controls tab is active)
        control_start_y = start_y + 10
        self.control_buttons = {
            'generate': Button(10, control_start_y, button_width, button_height, "Generate Maze"),
            'clear': Button(10, control_start_y + button_height + 10, 
                          button_width // 2 - 5, button_height, "Clear Grid"),
            'reset': Button(self.sidebar_width // 2 + 5, control_start_y + button_height + 10,
                          button_width // 2 - 5, button_height, "Reset Search"),
            'start': Button(10, control_start_y + 2 * (button_height + 10),
                          button_width, button_height, "Start Search"),
            'speed_up': Button(10, control_start_y + 3 * (button_height + 10),
                             button_width // 2 - 5, button_height, "Speed +"),
            'speed_down': Button(self.sidebar_width // 2 + 5, control_start_y + 3 * (button_height + 10),
                               button_width // 2 - 5, button_height, "Speed -")
        }
    
    def draw_grid(self):
        """Draw the grid"""
        # Draw cells
        for cell in self.cells.values():
            cell.draw_cell(self.grid_surf)
        
        # Blit grid to screen
        self.screen.blit(self.grid_surf, (self.sidebar_width, 0))
    
    def draw_sidebar(self):
        """Draw the tabbed sidebar"""
        self.sidebar_surf.fill(constants['COLORS']['UI_BG'])
        
        # Draw title
        title_font = pygame.font.SysFont('Arial', 16, bold=True)
        title = title_font.render("PATHFINDING VISUALIZER", True, constants['COLORS']['UI_TEXT'])
        self.sidebar_surf.blit(title, (self.sidebar_width // 2 - title.get_width() // 2, 35))
        
        # Draw tab buttons
        for tab in self.tab_buttons:
            tab.draw(self.sidebar_surf)
        
        # Draw content based on active tab
        if self.current_tab == 0:  # Algorithms tab
            self.draw_algorithms_tab()
        elif self.current_tab == 1:  # Mazes tab
            self.draw_mazes_tab()
        else:  # Controls tab
            self.draw_controls_tab()
        
        # Draw stats (always visible at bottom)
        self.draw_stats()
        
        # Draw instructions (always visible)
        self.draw_instructions()
        
        # Blit sidebar to screen
        self.screen.blit(self.sidebar_surf, (0, 0))
    
    def draw_algorithms_tab(self):
        """Draw the algorithms tab content"""
        start_y = constants['TAB_HEIGHT'] + 40
        
        # Draw category buttons
        for btn in self.category_buttons:
            btn.draw(self.sidebar_surf)
        
        # Draw algorithm buttons for current category
        for btn in self.algo_buttons:
            btn.draw(self.sidebar_surf)
        
        # Draw current selection info
        font = pygame.font.SysFont('Arial', 12)
        current_category = list(ALGORITHMS.keys())[self.current_algo_category_num]
        # current_category = self.current_algo_category
        print(current_category)
        current_algo_name = ALGORITHMS[current_category][self.current_algorithm]
        print(current_algo_name)
        
        info_text = font.render(f"Selected: {current_algo_name}", True, constants['COLORS']['UI_TEXT'])
        self.sidebar_surf.blit(info_text, (10, start_y + len(self.algo_buttons) * 35 + 20))
    
    def draw_mazes_tab(self):
        """Draw the mazes tab content"""
        start_y = constants['TAB_HEIGHT'] + 40
        
        # Draw maze buttons
        for btn in self.maze_buttons:
            btn.draw(self.sidebar_surf)
        
        # Draw current selection info
        font = pygame.font.SysFont('Arial', 12)
        current_maze_name = MAZE_TYPES[self.current_maze]
        info_text = font.render(f"Selected: {current_maze_name}", True, constants['COLORS']['UI_TEXT'])
        self.sidebar_surf.blit(info_text, (10, start_y + len(self.maze_buttons) * 35 + 20))
    
    def draw_controls_tab(self):
        """Draw the controls tab content"""
        start_y = constants['TAB_HEIGHT'] + 40
        
        # Draw control buttons
        for btn in self.control_buttons.values():
            btn.draw(self.sidebar_surf)
        
        # Draw speed info
        font = pygame.font.SysFont('Arial', 12)
        speed_text = font.render(f"Speed: {constants['SEARCH_SPEED']}x", True, constants['COLORS']['UI_TEXT'])
        self.sidebar_surf.blit(speed_text, (10, constants['TAB_HEIGHT'] + 250))
    
    def draw_stats(self):
        """Draw statistics at bottom of sidebar"""
        stats_y = self.total_height - 180
        
        font = pygame.font.SysFont('Arial', 12)
        stats = [
            f"Algorithm: {self.get_current_algorithm_name()}",
            f"Maze: {MAZE_TYPES[self.current_maze]}",
            f"Visited: {self.stats['visited']}",
            f"Path Length: {self.stats['path_length']}",
            f"Time: {self.stats['time']:.2f}s",
            f"Status: {'Searching' if self.searching else 'Ready'}",
            f"Paused: {'Yes' if self.paused else 'No'}"
        ]
        
        for i, text in enumerate(stats):
            text_surf = font.render(text, True, constants['COLORS']['UI_TEXT'])
            self.sidebar_surf.blit(text_surf, (10, stats_y + i * 18))
    
    def draw_instructions(self):
        """Draw instructions at very bottom"""
        instructions_y = self.total_height - 40
        
        font = pygame.font.SysFont('Arial', 10)
        instructions = [
            "Left Click: Draw/Erase | Right Click: Move Start | Space: Pause/Resume",
            "R: Reset | C: Clear | G: Generate Maze | ESC: Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surf = font.render(instruction, True, constants['COLORS']['UI_TEXT'])
            self.sidebar_surf.blit(text_surf, (5, instructions_y + i * 12))
    
    def get_current_algorithm_name(self):
        """Get the name of the currently selected algorithm"""
        categories = list(ALGORITHMS.keys())
        current_category = self.current_algo_category
        print(current_category)
        print(ALGORITHMS[current_category][self.current_algorithm])
        return ALGORITHMS[current_category][self.current_algorithm]
    
    def handle_events(self):
        """Handle all events"""
        mouse_pos = pygame.mouse.get_pos()
        sidebar_mouse_pos = mouse_pos
        
        # Check for mouse click
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
                
                # Check if click is in grid area
                if mouse_pos[0] > self.sidebar_width:
                    grid_mouse_pos = (mouse_pos[0] - self.sidebar_width, mouse_pos[1])
                    grid_pos = self.get_grid_pos(grid_mouse_pos)
                    
                    if event.button == 1:  # Left click
                        self.drawing = True
                        self.last_drawn = grid_pos
                        cell = self.cells[grid_pos]
                        
                        if cell.status == 'blocked':
                            self.draw_mode = 'erase'
                            cell.update('empty', self.grid_surf)
                            if grid_pos in self.obstacles:
                                self.obstacles.remove(grid_pos)
                        else:
                            self.draw_mode = 'block'
                            if cell.status not in ['start', 'target']:
                                cell.update('blocked', self.grid_surf)
                                if grid_pos not in self.obstacles:
                                    self.obstacles.append(grid_pos)
                    
                    elif event.button == 3:  # Right click - move start
                        if grid_pos != self.start_pos and grid_pos != self.goal_pos:
                            if self.cells[grid_pos].status == 'empty':
                                self.cells[self.start_pos].update('empty', self.grid_surf)
                                self.start_pos = grid_pos
                                self.cells[self.start_pos].update('start', self.grid_surf)
                                self.reset_search()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.drawing = False
                    self.last_drawn = None
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.searching:
                        self.paused = not self.paused
                    else:
                        self.start_search()
                elif event.key == pygame.K_r:
                    self.reset_search()
                elif event.key == pygame.K_c:
                    self.clear_grid()
                elif event.key == pygame.K_g:
                    self.generate_maze()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_TAB:
                    self.current_tab = (self.current_tab + 1) % len(self.tabs)
                    self.update_tab_buttons()
                elif event.key == pygame.K_1 and self.current_tab == 0:
                    self.select_algorithm(0)
                elif event.key == pygame.K_2 and self.current_tab == 0:
                    self.select_algorithm(1)
                elif event.key == pygame.K_3 and self.current_tab == 0:
                    self.select_algorithm(2)
                elif event.key == pygame.K_4 and self.current_tab == 0:
                    self.select_algorithm(3)
                elif event.key == pygame.K_5 and self.current_tab == 0:
                    self.select_algorithm(4)
        
        # Handle tab button clicks
        for i, tab in enumerate(self.tab_buttons):
            if tab.update(sidebar_mouse_pos, mouse_clicked):
                self.current_tab = i
                self.update_tab_buttons()
        
        # Handle content based on active tab
        if self.current_tab == 0:  # Algorithms tab
            self.handle_algorithms_tab(mouse_pos, mouse_clicked)
        elif self.current_tab == 1:  # Mazes tab
            self.handle_mazes_tab(mouse_pos, mouse_clicked)
        else:  # Controls tab
            self.handle_controls_tab(mouse_pos, mouse_clicked)
        
        # Handle continuous drawing
        if self.drawing and mouse_pos[0] > self.sidebar_width:
            grid_mouse_pos = (mouse_pos[0] - self.sidebar_width, mouse_pos[1])
            grid_pos = self.get_grid_pos(grid_mouse_pos)
            if grid_pos != self.last_drawn:
                self.last_drawn = grid_pos
                cell = self.cells[grid_pos]
                
                if self.draw_mode == 'block':
                    if cell.status not in ['start', 'target', 'blocked']:
                        cell.update('blocked', self.grid_surf)
                        if grid_pos not in self.obstacles:
                            self.obstacles.append(grid_pos)
                else:  # erase
                    if cell.status == 'blocked':
                        cell.update('empty', self.grid_surf)
                        if grid_pos in self.obstacles:
                            self.obstacles.remove(grid_pos)
    
    def handle_algorithms_tab(self, mouse_pos, mouse_clicked):
        """Handle interactions in algorithms tab"""
        # Handle category buttons
        categories = list(ALGORITHMS.keys())
        for i, btn in enumerate(self.category_buttons):
            if btn.update(mouse_pos, mouse_clicked):
                self.current_algo_category_num = i
                self.update_category_buttons()
                # Update algorithm buttons for this category
                self.update_algorithm_buttons_for_category(categories[i])
        
        # Handle algorithm buttons
        for i, btn in enumerate(self.algo_buttons):
            if btn.update(mouse_pos, mouse_clicked):
                self.select_algorithm(i)
    
    def handle_mazes_tab(self, mouse_pos, mouse_clicked):
        """Handle interactions in mazes tab"""
        for i, btn in enumerate(self.maze_buttons):
            if btn.update(mouse_pos, mouse_clicked):
                self.select_maze(i)
    
    def handle_controls_tab(self, mouse_pos, mouse_clicked):
        """Handle interactions in controls tab"""
        for name, btn in self.control_buttons.items():
            if btn.update(mouse_pos, mouse_clicked):
                if name == 'generate':
                    self.generate_maze()
                elif name == 'start':
                    self.start_search()
                elif name == 'clear':
                    self.clear_grid()
                elif name == 'reset':
                    self.reset_search()
                elif name == 'speed_up':
                    constants['SEARCH_SPEED'] = min(100, constants['SEARCH_SPEED'] + 10)
                elif name == 'speed_down':
                    constants['SEARCH_SPEED'] = max(5, constants['SEARCH_SPEED'] - 10)
    
    def update_tab_buttons(self):
        """Update which tab button is active"""
        for i, tab in enumerate(self.tab_buttons):
            tab.active = (i == self.current_tab)
    
    def update_category_buttons(self):
        """Update which category button is active"""
        for i, btn in enumerate(self.category_buttons):
            btn.active = (i == self.current_algo_category)
    
    def update_algorithm_buttons_for_category(self, category):
        """Update algorithm buttons for the given category"""
        # Clear existing algorithm buttons
        self.algo_buttons = []
        
        # Create new buttons for this category
        button_width = self.sidebar_width - 20
        button_height = 30
        start_y = constants['TAB_HEIGHT'] + 70
        
        for i, algo in enumerate(ALGORITHMS[category]):
            btn = Button(10, start_y + i * (button_height + 5), 
                        button_width, button_height, algo, is_toggle=True)
            self.algo_buttons.append(btn)
        
        # Reset algorithm selection
        self.current_algorithm = 0
        if self.algo_buttons:
            self.algo_buttons[0].active = True
    
    def select_algorithm(self, index):
        """Select an algorithm"""
        self.current_algorithm = index
        for i, btn in enumerate(self.algo_buttons):
            btn.active = (i == index)
    
    def select_maze(self, index):
        """Select a maze type"""
        self.current_maze = index
        for i, btn in enumerate(self.maze_buttons):
            btn.active = (i == index)
    
    def get_grid_pos(self, mouse_pos):
        """Convert mouse position to grid coordinates"""
        x = mouse_pos[0] // constants['TILESIZE']
        y = mouse_pos[1] // constants['TILESIZE']
        x = max(0, min(constants['X'] - 1, x))
        y = max(0, min(constants['Y'] - 1, y))
        return (x, y)
    
    def generate_maze(self):
        """Generate a maze"""
        self.reset_search()
        
        # Clear old obstacles
        self.obstacles = []
        for cell in self.cells.values():
            if cell.status == 'blocked':
                cell.update('empty', self.grid_surf)
        
        # Place start and goal at far corners
        self.start_pos = (2, 2)
        self.goal_pos = (constants['X'] - 3, constants['Y'] - 3)
        
        # Clear old start and goal
        for cell in self.cells.values():
            if cell.status == 'start' or cell.istarget:
                cell.istarget = False
                cell.update('empty', self.grid_surf)
        
        # Generate maze based on selected type
        generator = MazeGenerator()
        maze_type = MAZE_TYPES[self.current_maze]
        
        if maze_type == "Random Obstacles":
            generator.random_obstacles(
                self.cells, self.start_pos, self.goal_pos,
                constants['X'], constants['Y'], self.grid_surf, 0.3
            )
        elif maze_type == "Recursive Division":
            generator.recursive_division(
                self.cells, self.start_pos, self.goal_pos,
                constants['X'], constants['Y'], self.grid_surf
            )
        elif maze_type == "Prim's Algorithm":
            generator.prims_algorithm(
                self.cells, self.start_pos, self.goal_pos,
                constants['X'], constants['Y'], self.grid_surf
            )
        elif maze_type == "Cellular Automata":
            generator.cellular_automata(
                self.cells, self.start_pos, self.goal_pos,
                constants['X'], constants['Y'], self.grid_surf, 4
            )
        elif maze_type == "Spiral Maze":
            generator.spiral_maze(
                self.cells, self.start_pos, self.goal_pos,
                constants['X'], constants['Y'], self.grid_surf
            )
        else:
            # Fallback to random
            generator.random_obstacles(
                self.cells, self.start_pos, self.goal_pos,
                constants['X'], constants['Y'], self.grid_surf, 0.3
            )
        
        # Update start and goal
        self.cells[self.start_pos].update('start', self.grid_surf)
        self.cells[self.goal_pos].istarget = True
        self.cells[self.goal_pos].update('target', self.grid_surf)
        
        # Update obstacles list
        for pos, cell in self.cells.items():
            if cell.status == 'blocked':
                self.obstacles.append(pos)
    
    def clear_grid(self):
        """Clear all obstacles"""
        self.reset_search()
        self.obstacles = []
        for cell in self.cells.values():
            if cell.status == 'blocked':
                cell.update('empty', self.grid_surf)
    
    def reset_search(self):
        """Reset the search"""
        self.searching = False
        self.paused = False
        self.finished = False
        self.path_found = False
        
        # Reset algorithm state
        self.open_set = []
        self.closed_set = []
        self.queue.clear()
        self.stack = []
        self.visited = []
        self.open_set_start = []
        self.open_set_goal = []
        self.closed_set_start = []
        self.closed_set_goal = []
        self.pheromones = {}
        self.ida_threshold = 0
        self.ida_next_threshold = float('inf')
        
        # Reset cells (but keep obstacles, start, and goal)
        for cell in self.cells.values():
            if cell.status in ['active', 'closed', 'path']:
                if cell.pos == self.start_pos:
                    cell.update('start', self.grid_surf)
                elif cell.istarget:
                    cell.update('target', self.grid_surf)
                else:
                    cell.update('empty', self.grid_surf)
            cell.reset()
        
        # Re-draw start and goal
        self.cells[self.start_pos].update('start', self.grid_surf)
        self.cells[self.goal_pos].update('target', self.grid_surf)
        
        # Reset stats
        self.stats = {'visited': 0, 'path_length': 0, 'time': 0, 'start_time': 0}
    
    def start_search(self):
        """Start the pathfinding search"""
        if self.searching:
            return
        
        self.reset_search()
        self.searching = True
        self.stats['start_time'] = time.time()
        
        # Get current algorithm name
        algo_name = self.get_current_algorithm_name()
        
        # Initialize based on selected algorithm
        if "A*" in algo_name:
            start_cell = self.cells[self.start_pos]
            start_cell.g_cost = 0
            start_cell.get_h(self.goal_pos)
            start_cell.get_f()
            self.open_set = [start_cell]
            
        elif "Dijkstra" in algo_name:
            start_cell = self.cells[self.start_pos]
            start_cell.g_cost = 0
            self.open_set = [start_cell]
            
        elif "Breadth-First" in algo_name:
            start_cell = self.cells[self.start_pos]
            self.queue = deque([start_cell])
            
        elif "Depth-First" in algo_name:
            start_cell = self.cells[self.start_pos]
            self.stack = [start_cell]
            
        elif "Greedy" in algo_name:
            start_cell = self.cells[self.start_pos]
            start_cell.get_h(self.goal_pos)
            self.open_set = [start_cell]
            
        elif "Bidirectional" in algo_name:
            start_cell = self.cells[self.start_pos]
            goal_cell = self.cells[self.goal_pos]
            start_cell.g_cost = 0
            start_cell.get_h(self.goal_pos)
            start_cell.get_f()
            goal_cell.g_cost = 0
            goal_cell.get_h(self.start_pos)
            goal_cell.get_f()
            self.open_set_start = [start_cell]
            self.open_set_goal = [goal_cell]
            
        elif "Jump Point" in algo_name:
            start_cell = self.cells[self.start_pos]
            start_cell.g_cost = 0
            start_cell.get_h(self.goal_pos)
            start_cell.get_f()
            self.open_set = [start_cell]
            
        elif "IDA*" in algo_name:
            start_cell = self.cells[self.start_pos]
            start_cell.g_cost = 0
            start_cell.get_h(self.goal_pos)
            start_cell.get_f()
            self.open_set = [start_cell]
            self.ida_threshold = start_cell.h_cost
            self.ida_next_threshold = float('inf')
            
        elif "Swarm" in algo_name:
            start_cell = self.cells[self.start_pos]
            start_cell.g_cost = 0
            start_cell.get_h(self.goal_pos)
            start_cell.get_f()
            self.open_set = [start_cell]
            self.pheromones = {}
    
    def update_search(self):
        """Update the search algorithm"""
        if not self.searching or self.paused or self.finished:
            return
        
        # Control speed
        if pygame.time.get_ticks() % max(1, 60 // constants['SEARCH_SPEED']) != 0:
            return
        
        # Update time
        self.stats['time'] = time.time() - self.stats['start_time']
        
        # Get current algorithm name
        algo_name = self.get_current_algorithm_name()
        
        # Execute algorithm step
        if "A*" in algo_name:
            self.step_astar()
        elif "Dijkstra" in algo_name:
            self.step_dijkstra()
        elif "Breadth-First" in algo_name:
            self.step_bfs()
        elif "Depth-First" in algo_name:
            self.step_dfs()
        elif "Greedy" in algo_name:
            self.step_greedy()
        elif "Bidirectional" in algo_name:
            self.step_bidirectional()
        elif "Jump Point" in algo_name:
            self.step_jps()
        elif "IDA*" in algo_name:
            self.step_idastar()
        elif "Swarm" in algo_name:
            self.step_swarm()
        else:
            # Default to A*
            self.step_astar()
        
        # Update stats
        if "Breadth-First" in algo_name or "Depth-First" in algo_name:
            self.stats['visited'] = len(self.visited)
        elif "Bidirectional" in algo_name:
            self.stats['visited'] = len(self.closed_set_start) + len(self.closed_set_goal)
        else:
            self.stats['visited'] = len(self.closed_set)
    
    def step_astar(self):
        """A* algorithm step"""
        self.open_set, self.closed_set, current, self.finished, self.path_found = \
            PathfindingAlgorithms.astar_step(
                self.open_set, self.closed_set, self.goal_pos, self.cells, self.grid_surf
            )
        
        if self.finished and self.path_found:
            self.trace_path()
    
    def step_dijkstra(self):
        """Dijkstra's algorithm step"""
        self.open_set, self.closed_set, current, self.finished, self.path_found = \
            PathfindingAlgorithms.dijkstra_step(
                self.open_set, self.closed_set, self.goal_pos, self.cells, self.grid_surf
            )
        
        if self.finished and self.path_found:
            self.trace_path()
    
    def step_bfs(self):
        """BFS algorithm step"""
        self.queue, self.visited, current, self.finished, self.path_found = \
            PathfindingAlgorithms.bfs_step(
                self.queue, self.visited, self.goal_pos, self.cells, self.grid_surf
            )
        
        if self.finished and self.path_found:
            self.trace_path()
    
    def step_dfs(self):
        """DFS algorithm step"""
        self.stack, self.visited, current, self.finished, self.path_found = \
            PathfindingAlgorithms.dfs_step(
                self.stack, self.visited, self.goal_pos, self.cells, self.grid_surf
            )
        
        if self.finished and self.path_found:
            self.trace_path()
    
    def step_greedy(self):
        """Greedy Best-First step"""
        self.open_set, self.closed_set, current, self.finished, self.path_found = \
            PathfindingAlgorithms.greedy_step(
                self.open_set, self.closed_set, self.goal_pos, self.cells, self.grid_surf
            )
        
        if self.finished and self.path_found:
            self.trace_path()
    
    def step_bidirectional(self):
        """Bidirectional Search step - FIXED"""
        (self.open_set_start, self.open_set_goal, self.closed_set_start, 
         self.closed_set_goal, current, meeting_cell, self.finished, self.path_found) = \
            PathfindingAlgorithms.bidirectional_step(
                self.open_set_start, self.open_set_goal, self.closed_set_start,
                self.closed_set_goal, self.goal_pos, self.cells, self.grid_surf
            )
        
        if self.finished and self.path_found and meeting_cell:
            # Trace path from meeting cell to start
            current = meeting_cell.parent
            while current and current.pos != self.start_pos:
                if current.status != 'start':
                    current.update('path', self.grid_surf)
                current = current.parent
    
    def step_jps(self):
        """Jump Point Search step"""
        self.open_set, self.closed_set, current, self.finished, self.path_found = \
            PathfindingAlgorithms.jps_step(
                self.open_set, self.closed_set, self.goal_pos, self.cells, self.grid_surf
            )
        
        if self.finished and self.path_found:
            self.trace_path()
    
    def step_idastar(self):
        """IDA* Search step"""
        (self.open_set, self.closed_set, current, self.finished, self.path_found, 
         self.ida_threshold, self.ida_next_threshold) = \
            PathfindingAlgorithms.idastar_step(
                self.open_set, self.closed_set, self.goal_pos, self.cells, self.grid_surf,
                self.ida_threshold, self.ida_next_threshold
            )
        
        if self.finished:
            if self.path_found:
                self.trace_path()
            else:
                # Restart with new threshold
                start_cell = self.cells[self.start_pos]
                self.open_set = [start_cell]
                self.closed_set = []
                self.ida_threshold = self.ida_next_threshold
                self.ida_next_threshold = float('inf')
    
    def step_swarm(self):
        """Swarm Algorithm step"""
        self.open_set, self.closed_set, current, self.finished, self.path_found = \
            PathfindingAlgorithms.swarm_step(
                self.open_set, self.closed_set, self.goal_pos, self.cells, self.grid_surf,
                self.pheromones
            )
        
        if self.finished and self.path_found:
            self.trace_path()
    
    def trace_path(self):
        """Trace and draw the found path"""
        if not self.path_found:
            return
        
        current = self.cells[self.goal_pos].parent
        path_length = 0
        
        while current and current.pos != self.start_pos:
            if current.status != 'start':
                current.update('path', self.grid_surf)
                path_length += 1
            current = current.parent
        
        self.stats['path_length'] = path_length
    
    def run(self):
        """Main game loop"""
        while True:
            self.handle_events()
            
            if self.searching and not self.paused:
                self.update_search()
            
            self.draw_grid()
            self.draw_sidebar()
            
            pygame.display.flip()
            self.clock.tick(constants['FPS'])

#------------ MAIN ------------

def main():
    visualizer = PathfindingVisualizer()
    visualizer.run()

if __name__ == "__main__":
    main()