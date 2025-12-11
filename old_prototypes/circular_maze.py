#!/usr/bin/env python3
"""
Circular Maze Prototype
A prototype for generating circular mazes within a rectangular area using pygame.
"""

import json
import random
import math
from dataclasses import dataclass, field

import pygame

# Constants
WIDTH, HEIGHT = 600, 600
MAZE_RADIUS = 200  # Radius of the circular maze
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255, 100)
GREEN = (0, 255, 0, 150)
BLUE = (0, 0, 255, 150)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Seed
seed = random.randrange(0, 2**32, 1)
print("Using seed:", seed)
random.seed(seed)

# Grid for circular maze
# We'll use polar coordinates for the circular maze
grid = []
stack = []
current = None

def reset_state():
    """Reset the maze generation state"""
    global seed, grid, stack, current
    seed = random.randrange(0, 2**32, 1)
    print("Using seed:", seed)
    random.seed(seed)
    grid = []
    stack = []
    current = None

@dataclass
class PolarCell:
    """Cell class for circular maze using polar coordinates"""
    radius: float  # Distance from center
    angle: float   # Angle in radians
    ring: int      # Which ring this cell belongs to
    position: int  # Position within the ring
    walls: list[bool] = field(default_factory=lambda: [True, True, True, True])  # Radial, tangential, inner, outer
    visited: bool = False
    
    def show(self):
        """Draw the cell on screen"""
        # Convert polar to cartesian coordinates
        x = CENTER_X + self.radius * math.cos(self.angle)
        y = CENTER_Y + self.radius * math.sin(self.angle)
        
        # Draw cell representation
        if self.visited:
            pygame.draw.circle(screen, MAGENTA, (int(x), int(y)), 5)
        else:
            pygame.draw.circle(screen, WHITE, (int(x), int(y)), 3)
        
        # Draw walls with better visualization
        if self.walls[0]:  # Radial wall (outward)
            next_x = CENTER_X + (self.radius + 15) * math.cos(self.angle)
            next_y = CENTER_Y + (self.radius + 15) * math.sin(self.angle)
            pygame.draw.line(screen, WHITE, (int(x), int(y)), (int(next_x), int(next_y)), 2)
            
        if self.walls[1]:  # Tangential wall (clockwise)
            # Calculate position of next cell in same ring
            next_angle = self.angle + 0.1  # Small angle offset
            next_x = CENTER_X + self.radius * math.cos(next_angle)
            next_y = CENTER_Y + self.radius * math.sin(next_angle)
            pygame.draw.line(screen, WHITE, (int(x), int(y)), (int(next_x), int(next_y)), 1)
    
    def highlight(self):
        """Highlight the current cell"""
        x = CENTER_X + self.radius * math.cos(self.angle)
        y = CENTER_Y + self.radius * math.sin(self.angle)
        pygame.draw.circle(screen, GREEN, (int(x), int(y)), 8)
    
    def check_neighbors(self):
        """Check for unvisited neighbors"""
        neighbors = []
        
        # Find cells in the same ring (tangential neighbors)
        for cell in grid:
            if cell.ring == self.ring and abs(cell.position - self.position) == 1:
                if not cell.visited:
                    neighbors.append(cell)
        
        # Find cells in adjacent rings (radial neighbors)
        for cell in grid:
            if abs(cell.ring - self.ring) == 1 and abs(cell.position - self.position) <= 1:
                if not cell.visited:
                    neighbors.append(cell)
        
        return random.choice(neighbors) if neighbors else None

def create_circular_grid():
    """Create a grid of cells in a circular pattern"""
    global grid
    grid = []
    
    # Create concentric rings of cells
    num_rings = 6
    cells_per_ring = 12
    
    for ring in range(1, num_rings + 1):
        radius = ring * (MAZE_RADIUS / num_rings)
        for cell_num in range(cells_per_ring):
            angle = 2 * math.pi * cell_num / cells_per_ring
            grid.append(PolarCell(radius, angle, ring, cell_num))
    
    return grid

def remove_walls(a, b):
    """Remove walls between two cells"""
    # This will need to be implemented for polar coordinates
    pass

# Create circular grid
print("Creating circular grid...")
create_circular_grid()

if grid:
    current = grid[0]
    print(f"Created {len(grid)} cells in circular pattern")
else:
    print("Failed to create grid")

# Main loop
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw center point
    pygame.draw.circle(screen, BLUE, (CENTER_X, CENTER_Y), 10)
    
    # Draw outer circle boundary
    pygame.draw.circle(screen, WHITE, (CENTER_X, CENTER_Y), MAZE_RADIUS, 1)
    
    # Draw instructions
    font = pygame.font.SysFont('Arial', 16)
    instructions = [
        "Circular Maze Prototype",
        "Press Q to quit, R to reset, S to save"
    ]
    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10 + i * 20))
    
    # Draw grid
    for cell in grid:
        cell.show()
    
    # Maze generation logic using depth-first search
    if current:
        current.visited = True
        current.highlight()
        
        # Check for unvisited neighbors
        next_cell = current.check_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current)
            # remove_walls(current, next_cell)  # TODO: Implement wall removal
            current = next_cell
        elif stack:
            current = stack.pop()
        else:
            # Maze generation complete
            print("Maze generation complete!")
    
    # Handle keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        fileName = "circular_maze-%d.json" % seed
        with open(fileName, "w") as fh:
            json.dump([c.__dict__ for c in grid], fh)
        print("Maze dumped to:", fileName)
    
    if keys[pygame.K_q]:
        print("Exiting.")
        running = False
    
    if keys[pygame.K_r]:
        print("Resetting maze.")
        reset_state()
        create_circular_grid()
        if grid:
            current = grid[0]
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()