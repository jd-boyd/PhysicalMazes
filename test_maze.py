#!/usr/bin/env python3
"""Test suite for maze.py module"""

import unittest
import random
from graphs import RectGridGraph
from maze import generate_maze_dfs, generate_maze_with_solution, find_path_dfs


class TestMazeGeneration(unittest.TestCase):
    """Test maze generation functions"""

    def setUp(self):
        """Set up test fixtures"""
        # Use a fixed seed for reproducible tests
        random.seed(42)
        self.small_grid = RectGridGraph(2, 2)
        self.medium_grid = RectGridGraph(3, 3)

    def test_generate_maze_dfs_basic(self):
        """Test basic DFS maze generation"""
        start_idx = 0
        end_idx = 3  # Bottom-right corner in 2x2 grid
        
        maze_edges, path = generate_maze_dfs(self.small_grid, start_idx, end_idx)
        
        # Should generate some edges (spanning tree)
        self.assertGreater(len(maze_edges), 0)
        self.assertLessEqual(len(maze_edges), len(self.small_grid.edges))
        
        # Path should go from start to end
        self.assertEqual(path[0], start_idx)
        self.assertEqual(path[-1], end_idx)
        
    def test_generate_maze_dfs_without_end(self):
        """Test maze generation without specifying end index"""
        start_idx = 0
        
        maze_edges, path = generate_maze_dfs(self.small_grid, start_idx)
        
        # Should generate some edges
        self.assertGreater(len(maze_edges), 0)
        
        # Path should start at specified start
        self.assertEqual(path[0], start_idx)
        
        # End should be different from start
        self.assertNotEqual(path[-1], start_idx)
        
    def test_generate_maze_dfs_invalid_indices(self):
        """Test error handling for invalid indices"""
        with self.assertRaises(ValueError):
            generate_maze_dfs(self.small_grid, -1)  # Negative index
            
        with self.assertRaises(ValueError):
            generate_maze_dfs(self.small_grid, 100)  # Index too large
            
        with self.assertRaises(ValueError):
            generate_maze_dfs(self.small_grid, 0, -1)  # Negative end index
            
        with self.assertRaises(ValueError):
            generate_maze_dfs(self.small_grid, 0, 100)  # End index too large

    def test_maze_connectivity(self):
        """Test that generated maze is connected (all nodes reachable)"""
        start_idx = 0
        maze_edges, path = generate_maze_dfs(self.medium_grid, start_idx)
        
        # Create adjacency from maze edges
        adjacency = {}
        for node_idx in range(len(self.medium_grid.nodes)):
            adjacency[node_idx] = []
            
        for edge in maze_edges:
            adjacency[edge.a_id].append(edge.b_id)
            adjacency[edge.b_id].append(edge.a_id)
        
        # Perform BFS from start to see if all nodes are reachable
        visited = set()
        queue = [start_idx]
        
        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                for neighbor in adjacency[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        # All nodes should be visited (maze is connected)
        self.assertEqual(len(visited), len(self.medium_grid.nodes))

    def test_path_finding(self):
        """Test that path finding works correctly"""
        start_idx = 0
        end_idx = 8  # Bottom-right corner in 3x3 grid
        
        maze_edges, path = generate_maze_dfs(self.medium_grid, start_idx, end_idx)
        
        # Path should be valid
        self.assertEqual(path[0], start_idx)
        self.assertEqual(path[-1], end_idx)
        
        # Create adjacency from maze edges
        adjacency = {}
        for node_idx in range(len(self.medium_grid.nodes)):
            adjacency[node_idx] = []
            
        for edge in maze_edges:
            adjacency[edge.a_id].append(edge.b_id)
            adjacency[edge.b_id].append(edge.a_id)
        
        # Verify that each step in path is connected by an edge
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            self.assertIn(next_node, adjacency[current])

    def test_generate_maze_with_solution(self):
        """Test the convenience function"""
        start_idx = 0
        end_idx = 3
        
        result = generate_maze_with_solution(self.small_grid, start_idx, end_idx)
        
        # Should contain all expected keys
        self.assertIn('maze_edges', result)
        self.assertIn('solution_path', result)
        self.assertIn('start_node', result)
        self.assertIn('end_node', result)
        
        # Start and end nodes should match
        self.assertEqual(result['start_node'].n_id, start_idx)
        self.assertEqual(result['end_node'].n_id, end_idx)
        
        # Solution path should be valid
        self.assertEqual(result['solution_path'][0], start_idx)
        self.assertEqual(result['solution_path'][-1], end_idx)

    def test_different_grid_sizes(self):
        """Test maze generation with different grid sizes"""
        test_sizes = [(1, 1), (2, 3), (4, 2), (3, 4)]
        
        for w, h in test_sizes:
            with self.subTest(w=w, h=h):
                grid = RectGridGraph(w, h)
                start_idx = 0
                end_idx = (w - 1) + (h - 1) * w  # Bottom-right corner
                
                maze_edges, path = generate_maze_dfs(grid, start_idx, end_idx)
                
                # Should generate a spanning tree
                expected_edges = len(grid.nodes) - 1  # Spanning tree has n-1 edges
                self.assertEqual(len(maze_edges), expected_edges)
                
                # Path should be valid
                self.assertEqual(path[0], start_idx)
                self.assertEqual(path[-1], end_idx)

    def test_find_path_dfs_directly(self):
        """Test the path finding function directly"""
        # Create a simple maze with a known path
        grid = RectGridGraph(2, 2)
        
        # Use all edges for this test (complete graph)
        all_edges = grid.edges
        
        start_idx = 0
        end_idx = 3
        
        path = find_path_dfs(start_idx, end_idx, all_edges, grid.nodes)
        
        # Should find a path
        self.assertEqual(path[0], start_idx)
        self.assertEqual(path[-1], end_idx)
        self.assertGreater(len(path), 1)


if __name__ == '__main__':
    unittest.main()