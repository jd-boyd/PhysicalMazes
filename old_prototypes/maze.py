import json
import random
from dataclasses import dataclass, field

import pygame

# Constants
WIDTH, HEIGHT = 400, 400
COLS, ROWS = 12, 12
W = min(WIDTH // COLS, HEIGHT // ROWS)  # Cell size

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255, 100)
GREEN = (0, 255, 0, 150)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#Seed
seed = random.randrange(0, 2**32, 1)
print("Using seed: ", seed)
random.seed(seed)

# Grid
grid = []
stack = []
current = None

def reset_state():
    seed = random.randrange(0, 2**32, 1)
    print("Using seed: ", seed)
    random.seed(seed)
    grid = []
    stack = []
    current = None


# Helper to get grid index
def index(i, j):
    if i < 0 or j < 0 or i >= COLS or j >= ROWS:
        return -1
    return i + j * COLS

# Cell class
@dataclass
class Cell:
    i: int
    j: int
    walls: list[bool] = field(default_factory = lambda: list((True, True, True, True))) #self.walls = [True, True, True, True]  # Top, right, bottom, left
    visited: bool = False

    # def __init__(self, i, j):
    #     self.i = i
    #     self.j = j
    #     self.walls = [True, True, True, True]  # Top, right, bottom, left
    #     self.visited = False

    def show(self):
        x, y = self.i * W, self.j * W
        if self.visited:
            pygame.draw.rect(screen, MAGENTA, (x, y, W, W))
        if self.walls[0]:
            pygame.draw.line(screen, WHITE, (x, y), (x + W, y))  # Top
        if self.walls[1]:
            pygame.draw.line(screen, WHITE, (x + W, y), (x + W, y + W))  # Right
        if self.walls[2]:
            pygame.draw.line(screen, WHITE, (x + W, y + W), (x, y + W))  # Bottom
        if self.walls[3]:
            pygame.draw.line(screen, WHITE, (x, y + W), (x, y))  # Left

    def highlight(self):
        x, y = self.i * W, self.j * W
        pygame.draw.rect(screen, GREEN, (x, y, W, W))

    def check_neighbors(self):
        neighbors = []

        top = grid[index(self.i, self.j - 1)] if index(self.i, self.j - 1) != -1 else None
        right = grid[index(self.i + 1, self.j)] if index(self.i + 1, self.j) != -1 else None
        bottom = grid[index(self.i, self.j + 1)] if index(self.i, self.j + 1) != -1 else None
        left = grid[index(self.i - 1, self.j)] if index(self.i - 1, self.j) != -1 else None

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        if neighbors:
            return random.choice(neighbors)
        else:
            return None

# Remove walls between two cells
def remove_walls(a, b):
    dx = a.i - b.i
    if dx == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif dx == -1:
        a.walls[1] = False
        b.walls[3] = False

    dy = a.j - b.j
    if dy == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif dy == -1:
        a.walls[2] = False
        b.walls[0] = False

# Create grid
for j in range(ROWS):
    for i in range(COLS):
        grid.append(Cell(i, j))

current = grid[0]

# Main loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw grid
    for cell in grid:
        cell.show()

    # Maze generation logic
    current.visited = True
    current.highlight()

    next_cell = current.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current)
        remove_walls(current, next_cell)
        current = next_cell
    elif stack:
        current = stack.pop()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        fileName = "maze-%d.json" % seed
        with open(fileName, "w") as fh:
            json.dump([c.__dict__ for c in grid], fh)
        print("Maze dumped to: ", fileName)
    if keys[pygame.K_q]:
        print("Exiting.")
        running = False
    if keys[pygame.K_r]:
        print("Resetting maze.")
        reset_state()


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
