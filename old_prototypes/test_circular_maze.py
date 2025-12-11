#!/usr/bin/env python3
"""
Test script for circular maze prototype - non-interactive version
"""

import math
from dataclasses import dataclass, field

def test_circular_maze_structure():
    """Test the basic circular maze structure without pygame"""
    
    # Constants
    MAZE_RADIUS = 200
    CENTER_X, CENTER_Y = 300, 300
    
    @dataclass
    class PolarCell:
        """Cell class for circular maze using polar coordinates"""
        radius: float  # Distance from center
        angle: float   # Angle in radians
        ring: int      # Which ring this cell belongs to
        position: int  # Position within the ring
        walls: list[bool] = field(default_factory=lambda: [True, True, True, True])
        visited: bool = False
        
        def __str__(self):
            return f"Cell(ring={self.ring}, pos={self.position}, r={self.radius:.1f}, angle={self.angle:.2f})"
    
    def create_circular_grid():
        """Create a grid of cells in a circular pattern"""
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
    
    # Test grid creation
    print("Testing circular maze structure...")
    grid = create_circular_grid()
    print(f"Created {len(grid)} cells in circular pattern")
    
    # Test a few cells
    print("\nSample cells:")
    for i, cell in enumerate([grid[0], grid[5], grid[10], grid[-1]]):
        print(f"  {i}: {cell}")
    
    # Test neighbor finding
    def test_neighbors(cell, grid):
        """Test neighbor finding logic"""
        neighbors = []
        
        # Find cells in the same ring (tangential neighbors)
        for other_cell in grid:
            if other_cell.ring == cell.ring and abs(other_cell.position - cell.position) == 1:
                neighbors.append(other_cell)
        
        # Find cells in adjacent rings (radial neighbors)
        for other_cell in grid:
            if abs(other_cell.ring - cell.ring) == 1 and abs(other_cell.position - cell.position) <= 1:
                neighbors.append(other_cell)
        
        return neighbors
    
    print("\nTesting neighbor finding:")
    test_cell = grid[len(grid) // 2]  # Middle cell
    neighbors = test_neighbors(test_cell, grid)
    print(f"Cell {test_cell} has {len(neighbors)} neighbors")
    for i, neighbor in enumerate(neighbors[:3]):  # Show first 3 neighbors
        print(f"  Neighbor {i}: {neighbor}")
    
    print("\nCircular maze structure test completed successfully!")

if __name__ == "__main__":
    test_circular_maze_structure()