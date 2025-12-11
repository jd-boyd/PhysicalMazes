#!/usr/bin/env python3
"""Maze generation functions using graph algorithms"""

import random
from graphs import Graph, Node, Edge, RectGridGraph


def generate_maze_dfs(graph, start_idx, end_idx=None):
    """
    Generate a maze using Depth-First Search algorithm on a graph.
    
    Args:
        graph: A Graph object (should have nodes and edges)
        start_idx: Starting node index for the maze
        end_idx: Optional ending node index (if None, will use a random far node)
        
    Returns:
        tuple: (maze_edges, path) where maze_edges are the edges in the maze
               and path is the solution path from start to end
    """
    # Validate inputs
    if start_idx < 0 or start_idx >= len(graph.nodes):
        raise ValueError(f"Start index {start_idx} is out of range for graph with {len(graph.nodes)} nodes")
    
    if end_idx is not None:
        if end_idx < 0 or end_idx >= len(graph.nodes):
            raise ValueError(f"End index {end_idx} is out of range for graph with {len(graph.nodes)} nodes")
    
    # If no end is specified, choose a far node (opposite corner for grid graphs)
    if end_idx is None and hasattr(graph, 'w') and hasattr(graph, 'h'):
        # For RectGridGraph, choose opposite corner
        end_idx = (graph.w - 1) + (graph.h - 1) * graph.w
    elif end_idx is None:
        # For other graphs, choose a random node far from start
        max_distance = -1
        best_end = start_idx
        
        for i, node in enumerate(graph.nodes):
            if i == start_idx:
                continue
            # Simple distance metric (could be improved)
            distance = abs(node.x - graph.nodes[start_idx].x) + abs(node.y - graph.nodes[start_idx].y)
            if distance > max_distance:
                max_distance = distance
                best_end = i
        end_idx = best_end
    
    # Create adjacency list for easier traversal
    adjacency = {}
    for node_idx, node in enumerate(graph.nodes):
        adjacency[node_idx] = []
    
    for edge in graph.edges:
        adjacency[edge.a_id].append(edge.b_id)
        adjacency[edge.b_id].append(edge.a_id)
    
    # DFS to generate maze (similar to recursive backtracker algorithm)
    visited = set()
    stack = [start_idx]
    maze_edges = []  # Edges that are part of the maze
    
    while stack:
        current_idx = stack[-1]
        visited.add(current_idx)
        
        # Get unvisited neighbors
        unvisited_neighbors = []
        for neighbor_idx in adjacency[current_idx]:
            if neighbor_idx not in visited:
                unvisited_neighbors.append(neighbor_idx)
        
        if unvisited_neighbors:
            # Choose random neighbor
            next_idx = random.choice(unvisited_neighbors)
            
            # Add the edge between current and next to maze
            # Find the actual edge in the graph
            for edge in graph.edges:
                if (edge.a_id == current_idx and edge.b_id == next_idx) or \
                   (edge.a_id == next_idx and edge.b_id == current_idx):
                    maze_edges.append(edge)
                    break
            
            stack.append(next_idx)
        else:
            # Backtrack
            stack.pop()
    
    # Now find a path from start to end using the maze edges
    # We'll use DFS again to find a path through the maze
    path = find_path_dfs(start_idx, end_idx, maze_edges, graph.nodes)
    
    return maze_edges, path


def find_path_dfs(start_idx, end_idx, maze_edges, nodes):
    """
    Find a path from start to end using only the maze edges.
    
    Args:
        start_idx: Starting node index
        end_idx: Ending node index  
        maze_edges: List of edges that form the maze
        nodes: List of nodes in the graph
        
    Returns:
        list: List of node indices forming the path from start to end
    """
    # Create adjacency list from maze edges
    adjacency = {}
    for node_idx in range(len(nodes)):
        adjacency[node_idx] = []
    
    for edge in maze_edges:
        adjacency[edge.a_id].append(edge.b_id)
        adjacency[edge.b_id].append(edge.a_id)
    
    # DFS to find path
    visited = set()
    stack = [(start_idx, [start_idx])]  # (current_idx, path_so_far)
    
    while stack:
        current_idx, path_so_far = stack.pop()
        
        if current_idx == end_idx:
            return path_so_far
        
        if current_idx not in visited:
            visited.add(current_idx)
            
            # Add neighbors to stack in reverse order to process them in order
            for neighbor_idx in reversed(adjacency[current_idx]):
                if neighbor_idx not in visited:
                    stack.append((neighbor_idx, path_so_far + [neighbor_idx]))
    
    # If no path found (shouldn't happen in a connected maze)
    return [start_idx, end_idx]


def generate_maze_with_solution(graph, start_idx, end_idx=None):
    """
    Convenience function that generates a maze and returns both the maze and solution.
    
    Args:
        graph: A Graph object
        start_idx: Starting node index
        end_idx: Optional ending node index
        
    Returns:
        dict: Dictionary containing maze_edges and solution_path
    """
    maze_edges, solution_path = generate_maze_dfs(graph, start_idx, end_idx)
    
    return {
        'maze_edges': maze_edges,
        'solution_path': solution_path,
        'start_node': graph.nodes[start_idx],
        'end_node': graph.nodes[end_idx]
    }


def print_maze_info(maze_result):
    """
    Print information about a generated maze.
    
    Args:
        maze_result: Dictionary from generate_maze_with_solution
    """
    print(f"Maze generated with {len(maze_result['maze_edges'])} edges")
    print(f"Solution path has {len(maze_result['solution_path'])} steps")
    print(f"Start: ({maze_result['start_node'].x}, {maze_result['start_node'].y})")
    print(f"End: ({maze_result['end_node'].x}, {maze_result['end_node'].y})")
    print("Solution path:", " -> ".join(str(idx) for idx in maze_result['solution_path']))


if __name__ == "__main__":
    # Demo usage
    print("=== Maze Generation Demo ===")
    
    # Create a small grid
    grid = RectGridGraph(5, 5)
    print(f"Created {grid.w}x{grid.h} grid with {len(grid.nodes)} nodes and {len(grid.edges)} edges")
    
    # Generate maze from top-left (0) to bottom-right (24 in 5x5 grid)
    start_idx = 0
    end_idx = 24
    
    print(f"\nGenerating maze from node {start_idx} to node {end_idx}...")
    maze_result = generate_maze_with_solution(grid, start_idx, end_idx)
    
    print_maze_info(maze_result)