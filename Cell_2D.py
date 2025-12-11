# -*- coding: utf-8 -*-
"""
Cell class for pathfinder
"""

import pygame

class Cell:
    def __init__(self, pos, status, constants, istarget=False):
        self.pos = pos
        self.status = status
        self.istarget = istarget  # CRITICAL: Only one cell should have this True!
        
        self.tile_size = constants['TILESIZE']
        self.X = constants['X']
        self.Y = constants['Y']
        self.colors = constants['COLORS']

        # Screen geometry object        
        margin = constants['MARGIN']
        realx = pos[0] * constants['TILESIZE']
        realy = pos[1] * constants['TILESIZE']
        self.rect = pygame.Rect(realx + margin, realy + margin, 
                               self.tile_size - 2*margin, self.tile_size - 2*margin)
        
        self.neighbours = None
        self.parent = None
        
        self.f_cost = float('inf')
        self.h_cost = float('inf')
        self.g_cost = float('inf')
        
    def add_neighbours(self, cell_list):
        """Add neighboring cells"""
        coords = self.get_neighbour_coords()
        self.neighbours = []
        for c in coords:
            if c in cell_list:
                self.neighbours.append(cell_list[c])
        return

    def get_neighbour_coords(self):
        """Get coordinates of neighboring cells (8-directional)"""
        vectors = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not (dx == 0 == dy):
                    neighbour = (self.pos[0] + dx, self.pos[1] + dy)
                    if self.in_bounds(neighbour):
                        vectors.append(neighbour)
        return vectors
    
    def in_bounds(self, pos):
        """Check if position is within grid bounds"""
        return 0 <= pos[0] < self.X and 0 <= pos[1] < self.Y

    def update(self, new_status, surf):
        """Update cell status and redraw"""
        if self.status != new_status:
            self.status = new_status
            self.draw_cell(surf)
        return
    
    def draw_cell(self, surf):
        """Draw the cell with appropriate color"""
        # FIXED: Only use TARGET_COL if istarget is True
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
        elif self.status == 'empty':
            col = self.colors['EMPTY_COL']
        else:
            col = (255, 0, 255)  # Magenta for error
        
        pygame.draw.rect(surf, col, self.rect, border_radius=2)
        
        return
        
    def get_h(self, goal_pos):
        """Calculate heuristic cost to goal (Manhattan distance)"""
        dx = abs(goal_pos[0] - self.pos[0])
        dy = abs(goal_pos[1] - self.pos[1])
        self.h_cost = 10 * (dx + dy)
        return self.h_cost
        
    def get_distance_to(self, other_cell):
        """Get distance to another cell"""
        dx = abs(other_cell.pos[0] - self.pos[0])
        dy = abs(other_cell.pos[1] - self.pos[1])
        if dx == 1 and dy == 1:
            return 14  # Diagonal cost
        return 10  # Cardinal cost
    
    def get_g(self, neighbour):
        """Update g-cost if a better path is found through neighbour"""
        distance = self.get_distance_to(neighbour)
        new_g = neighbour.g_cost + distance
        
        if new_g < self.g_cost:
            self.g_cost = new_g
            return True  # Change occurred
        return False  # No change
    
    def get_f(self):
        """Calculate total cost f = g + h"""
        self.f_cost = self.g_cost + self.h_cost
        return self.f_cost
    
    def reset(self):
        """Reset cell to initial state (but keep istarget if it is the target)"""
        self.parent = None
        self.f_cost = float('inf')
        self.h_cost = float('inf')
        self.g_cost = float('inf')

def make_grid(constants, surface=None):
    """Create a grid of cells"""
    cell_list = {}
    for x in range(constants['X']):
        for y in range(constants['Y']):
            cell_list[(x, y)] = Cell((x, y), 'empty', constants)
    
    # Build graph data structure
    for cell in cell_list.values():
        cell.add_neighbours(cell_list)
        if surface:
            cell.draw_cell(surface)
    
    return cell_list

def decorate_grid(surface, cell_list, obstacle_list):
    """Place obstacles in grid"""
    if obstacle_list:
        for pos in obstacle_list:
            if pos in cell_list:
                cell_list[pos].update('blocked', surface)
    return cell_list