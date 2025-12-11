#!/usr/bin/env python3
"""
Pygame visualization script for graph JSON files.

Usage: python vizfile.py <graph_json_file>
"""

import sys
import json
import pygame
import argparse
from graphs import Graph


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Visualize a graph from a JSON file')
    parser.add_argument('json_file', help='Path to the JSON file containing graph data')
    parser.add_argument('--width', type=int, default=800, help='Window width')
    parser.add_argument('--height', type=int, default=600, help='Window height')
    parser.add_argument('--node-size', type=int, default=10, help='Node radius in pixels')
    parser.add_argument('--edge-width', type=int, default=2, help='Edge width in pixels')
    
    return parser.parse_args()


def load_graph_from_json(filepath):
    """Load a graph from a JSON file"""
    try:
        return Graph.from_json_file(filepath)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{filepath}' is not valid JSON.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading graph: {e}")
        sys.exit(1)


def calculate_layout(graph, width, height):
    """
    Calculate node positions for visualization.
    For grid graphs, use actual coordinates. For others, use force-directed layout.
    """
    if not graph.nodes:
        return {}
    
    # Check if this looks like a grid graph
    is_grid = all(node.x >= 0 and node.y >= 0 for node in graph.nodes)
    
    if is_grid:
        # For grid graphs, use the actual coordinates
        max_x = max(node.x for node in graph.nodes) if graph.nodes else 1
        max_y = max(node.y for node in graph.nodes) if graph.nodes else 1
        
        scale_x = (width * 0.8) / max_x if max_x > 0 else 1
        scale_y = (height * 0.6) / max_y if max_y > 0 else 1  # Use 60% of height to leave room for margin
        scale = min(scale_x, scale_y)
        
        offset_x = (width - (max_x + 1) * scale) / 2
        offset_y = (height * 0.25) + (height * 0.6 - (max_y + 1) * scale) / 2  # Add 25% top margin
        
        positions = {}
        for node in graph.nodes:
            x = node.x * scale + offset_x
            y = node.y * scale + offset_y
            positions[node.n_id] = (x, y)
        
    else:
        # Simple circular layout for non-grid graphs
        center_x, center_y = width / 2, height / 2
        radius = min(width, height) * 0.4
        
        positions = {}
        for i, node in enumerate(graph.nodes):
            angle = (i / len(graph.nodes)) * 2 * 3.14159
            x = center_x + radius * 0.8 * (1 + 0.2 * i) * (1 + 0.1 * (i % 3)) * 0.5
            y = center_y + radius * 0.8 * (1 + 0.2 * i) * (1 + 0.1 * (i % 2)) * 0.5
            positions[node.n_id] = (x, y)
    
    return positions


def draw_graph(screen, graph, positions, node_size, edge_width, args):
    """Draw the graph on the Pygame screen"""
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (200, 200, 200)
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw title and info at the top
    font_large = pygame.font.SysFont('Arial', 18, bold=True)
    font_small = pygame.font.SysFont('Arial', 14)
    
    title_text = font_large.render("Graph Visualization", True, BLACK)
    info_text = font_small.render(f"Nodes: {len(graph.nodes)} | Edges: {len(graph.edges)} | File: {args.json_file.split('/')[-1]}", True, BLACK)
    
    screen.blit(title_text, (20, 20))
    screen.blit(info_text, (20, 50))
    
    # Draw edges
    for edge in graph.edges:
        if edge.a_id in positions and edge.b_id in positions:
            start_pos = positions[edge.a_id]
            end_pos = positions[edge.b_id]
            pygame.draw.line(screen, GRAY, start_pos, end_pos, edge_width)
    
    # Draw nodes
    for node in graph.nodes:
        if node.n_id in positions:
            pos = positions[node.n_id]
            pygame.draw.circle(screen, BLUE, (int(pos[0]), int(pos[1])), node_size)
            
            # Draw node ID at upper right
            font = pygame.font.SysFont('Arial', 12)
            text = font.render(str(node.n_id), True, BLACK)
            text_rect = text.get_rect(midbottom=(pos[0] + node_size + 10, pos[1] - node_size - 10))
            screen.blit(text, text_rect)
    
    # Draw node coordinates at upper left (for grid graphs)
    font = pygame.font.SysFont('Arial', 12)
    for node in graph.nodes:
        if node.n_id in positions:
            pos = positions[node.n_id]
            coords_text = f"({node.x},{node.y})"
            text = font.render(coords_text, True, BLACK)
            # Position at upper left: subtract from x, subtract from y
            text_rect = text.get_rect(midbottom=(pos[0] - node_size - 10, pos[1] - node_size - 10))
            screen.blit(text, text_rect)


def main():
    """Main function"""
    args = parse_arguments()
    
    # Initialize Pygame
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((args.width, args.height))
    pygame.display.set_caption(f"Graph Visualization: {args.json_file}")
    
    # Load graph
    print(f"Loading graph from {args.json_file}...")
    graph = load_graph_from_json(args.json_file)
    print(f"Loaded graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
    
    # Calculate node positions
    positions = calculate_layout(graph, args.width, args.height)
    
    # Main loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s:
                    # Save screenshot
                    pygame.image.save(screen, "graph_screenshot.png")
                    print("Saved screenshot as graph_screenshot.png")
        
        # Draw graph
        draw_graph(screen, graph, positions, args.node_size, args.edge_width, args)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("Visualization closed.")


if __name__ == "__main__":
    main()