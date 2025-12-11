#!/usr/bin/env python3
"""Test suite for graphs.py module"""

import unittest
import tempfile
import os
from graphs import Node, Edge, Graph, RectGridGraph, xyToIdx


class TestGraphFunctions(unittest.TestCase):
    """Test the graph utility functions"""

    def test_xyToIdx(self):
        """Test xyToIdx function"""
        # Test basic conversion
        self.assertEqual(xyToIdx(0, 0, 10), 0)
        self.assertEqual(xyToIdx(5, 0, 10), 5)
        self.assertEqual(xyToIdx(0, 1, 10), 10)
        self.assertEqual(xyToIdx(5, 1, 10), 15)
        self.assertEqual(xyToIdx(9, 9, 10), 99)

        # Test with different widths
        self.assertEqual(xyToIdx(0, 0, 5), 0)
        self.assertEqual(xyToIdx(2, 3, 5), 17)


class TestNode(unittest.TestCase):
    """Test Node dataclass"""

    def test_node_creation(self):
        """Test Node creation and attributes"""
        node = Node(x=2, y=3, n_id=10)
        self.assertEqual(node.x, 2)
        self.assertEqual(node.y, 3)
        self.assertEqual(node.n_id, 10)

    def test_node_equality(self):
        """Test Node equality"""
        node1 = Node(x=1, y=2, n_id=5)
        node2 = Node(x=1, y=2, n_id=5)
        node3 = Node(x=2, y=3, n_id=10)
        
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)


class TestEdge(unittest.TestCase):
    """Test Edge dataclass"""

    def test_edge_creation(self):
        """Test Edge creation and attributes"""
        node_a = Node(x=0, y=0, n_id=0)
        node_b = Node(x=1, y=0, n_id=1)
        
        edge = Edge(a=node_a, b=node_b, a_id=0, b_id=1)
        self.assertEqual(edge.a, node_a)
        self.assertEqual(edge.b, node_b)
        self.assertEqual(edge.a_id, 0)
        self.assertEqual(edge.b_id, 1)

    def test_edge_equality(self):
        """Test Edge equality"""
        node_a = Node(x=0, y=0, n_id=0)
        node_b = Node(x=1, y=0, n_id=1)
        
        edge1 = Edge(a=node_a, b=node_b, a_id=0, b_id=1)
        edge2 = Edge(a=node_a, b=node_b, a_id=0, b_id=1)
        edge3 = Edge(a=node_b, b=node_a, a_id=1, b_id=0)
        
        self.assertEqual(edge1, edge2)
        self.assertNotEqual(edge1, edge3)


class TestRectGridGraph(unittest.TestCase):
    """Test RectGridGraph class"""

    def test_small_grid_creation(self):
        """Test creation of a small grid (2x2)"""
        graph = RectGridGraph(2, 2)
        
        # Test node count
        self.assertEqual(len(graph.nodes), 4)
        
        # Test edge count (2x2 grid should have 2 horizontal + 2 vertical = 4 edges in one direction)
        self.assertEqual(len(graph.edges), 4)
        
        # Test node positions
        self.assertEqual(graph.nodes[0].x, 0)
        self.assertEqual(graph.nodes[0].y, 0)
        self.assertEqual(graph.nodes[1].x, 1)
        self.assertEqual(graph.nodes[1].y, 0)
        self.assertEqual(graph.nodes[2].x, 0)
        self.assertEqual(graph.nodes[2].y, 1)
        self.assertEqual(graph.nodes[3].x, 1)
        self.assertEqual(graph.nodes[3].y, 1)

    def test_1x1_grid_creation(self):
        """Test creation of a 1x1 grid"""
        graph = RectGridGraph(1, 1)
        
        # Test node count
        self.assertEqual(len(graph.nodes), 1)
        
        # Test edge count (1x1 grid should have 0 edges)
        self.assertEqual(len(graph.edges), 0)

    def test_3x3_grid_creation(self):
        """Test creation of a 3x3 grid"""
        graph = RectGridGraph(3, 3)
        
        # Test node count
        self.assertEqual(len(graph.nodes), 9)
        
        # Test edge count (3x3 grid should have 6 horizontal + 6 vertical = 12 edges in one direction)
        self.assertEqual(len(graph.edges), 12)

    def test_grid_width_height(self):
        """Test grid width and height properties"""
        graph = RectGridGraph(5, 3)
        self.assertEqual(graph.w, 5)
        self.assertEqual(graph.h, 3)
        self.assertEqual(len(graph.nodes), 15)

    def test_edge_connections(self):
        """Test that edges connect the correct nodes"""
        graph = RectGridGraph(2, 2)
        
        # Test horizontal edges
        horizontal_edges = [edge for edge in graph.edges if edge.a.y == edge.b.y]
        self.assertEqual(len(horizontal_edges), 2)  # 2 rows * 1 horizontal edge each (right direction only)
        
        # Test vertical edges
        vertical_edges = [edge for edge in graph.edges if edge.a.x == edge.b.x]
        self.assertEqual(len(vertical_edges), 2)  # 2 columns * 1 vertical edge each (down direction only)
        
        # Test specific edge connections
        node_0 = graph.nodes[0]  # (0, 0)
        node_1 = graph.nodes[1]  # (1, 0)
        node_2 = graph.nodes[2]  # (0, 1)
        
        # Find edge between node_0 and node_1 (horizontal)
        edge_0_1 = None
        for edge in graph.edges:
            if (edge.a == node_0 and edge.b == node_1) or (edge.a == node_1 and edge.b == node_0):
                edge_0_1 = edge
                break
        
        self.assertIsNotNone(edge_0_1)
        self.assertTrue((edge_0_1.a == node_0 and edge_0_1.b == node_1) or 
                       (edge_0_1.a == node_1 and edge_0_1.b == node_0))

    def test_edge_directions(self):
        """Test that edges are created in the correct directions (right and down only)"""
        graph = RectGridGraph(3, 3)
        
        # Test that all horizontal edges go from left to right (lower x to higher x)
        horizontal_edges = [edge for edge in graph.edges if edge.a.y == edge.b.y]
        for edge in horizontal_edges:
            self.assertLess(edge.a.x, edge.b.x)
            self.assertEqual(edge.a.y, edge.b.y)
        
        # Test that all vertical edges go from top to bottom (lower y to higher y)
        vertical_edges = [edge for edge in graph.edges if edge.a.x == edge.b.x]
        for edge in vertical_edges:
            self.assertLess(edge.a.y, edge.b.y)
            self.assertEqual(edge.a.x, edge.b.x)

    def test_node_ids(self):
        """Test that node IDs are correctly assigned"""
        graph = RectGridGraph(3, 2)

        # Test ID calculation
        for y in range(2):
            for x in range(3):
                expected_id = x + 3 * y
                node_id = graph.nodes[expected_id].n_id
                self.assertEqual(node_id, expected_id)


class TestGraphJSONSerialization(unittest.TestCase):
    """Test Graph JSON serialization and deserialization"""

    def test_to_json_file_simple_graph(self):
        """Test saving a simple graph to JSON file"""
        # Create a simple graph
        node1 = Node(x=0, y=0, n_id=0)
        node2 = Node(x=1, y=0, n_id=1)
        edge1 = Edge(a=node1, b=node2, a_id=0, b_id=1)
        graph = Graph(nodes=[node1, node2], edges=[edge1])

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name

        try:
            graph.to_json_file(temp_path)

            # Verify file exists
            self.assertTrue(os.path.exists(temp_path))

            # Read and verify content
            import json
            with open(temp_path, 'r') as f:
                data = json.load(f)

            self.assertIn('nodes', data)
            self.assertIn('edges', data)
            self.assertEqual(len(data['nodes']), 2)
            self.assertEqual(len(data['edges']), 1)

            # Verify node data
            self.assertEqual(data['nodes'][0]['x'], 0)
            self.assertEqual(data['nodes'][0]['y'], 0)
            self.assertEqual(data['nodes'][0]['n_id'], 0)

            # Verify edge data
            self.assertEqual(data['edges'][0]['a_id'], 0)
            self.assertEqual(data['edges'][0]['b_id'], 1)
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_from_json_file_simple_graph(self):
        """Test loading a simple graph from JSON file"""
        # Create a simple graph
        node1 = Node(x=0, y=0, n_id=0)
        node2 = Node(x=1, y=0, n_id=1)
        edge1 = Edge(a=node1, b=node2, a_id=0, b_id=1)
        original_graph = Graph(nodes=[node1, node2], edges=[edge1])

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name

        try:
            original_graph.to_json_file(temp_path)

            # Load from file
            loaded_graph = Graph.from_json_file(temp_path)

            # Verify nodes
            self.assertEqual(len(loaded_graph.nodes), 2)
            self.assertEqual(loaded_graph.nodes[0].x, 0)
            self.assertEqual(loaded_graph.nodes[0].y, 0)
            self.assertEqual(loaded_graph.nodes[0].n_id, 0)
            self.assertEqual(loaded_graph.nodes[1].x, 1)
            self.assertEqual(loaded_graph.nodes[1].y, 0)
            self.assertEqual(loaded_graph.nodes[1].n_id, 1)

            # Verify edges
            self.assertEqual(len(loaded_graph.edges), 1)
            self.assertEqual(loaded_graph.edges[0].a_id, 0)
            self.assertEqual(loaded_graph.edges[0].b_id, 1)

            # Verify edge node references
            self.assertEqual(loaded_graph.edges[0].a, loaded_graph.nodes[0])
            self.assertEqual(loaded_graph.edges[0].b, loaded_graph.nodes[1])
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_round_trip_rect_grid_graph(self):
        """Test that a RectGridGraph can be saved and loaded without data loss"""
        # Create a RectGridGraph
        original_graph = RectGridGraph(3, 2)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name

        try:
            original_graph.to_json_file(temp_path)

            # Load from file
            loaded_graph = Graph.from_json_file(temp_path)

            # Verify node count
            self.assertEqual(len(loaded_graph.nodes), len(original_graph.nodes))

            # Verify edge count
            self.assertEqual(len(loaded_graph.edges), len(original_graph.edges))

            # Verify all nodes match
            for i, (orig_node, loaded_node) in enumerate(zip(original_graph.nodes, loaded_graph.nodes)):
                self.assertEqual(orig_node.x, loaded_node.x)
                self.assertEqual(orig_node.y, loaded_node.y)
                self.assertEqual(orig_node.n_id, loaded_node.n_id)

            # Verify all edges match
            for i, (orig_edge, loaded_edge) in enumerate(zip(original_graph.edges, loaded_graph.edges)):
                self.assertEqual(orig_edge.a_id, loaded_edge.a_id)
                self.assertEqual(orig_edge.b_id, loaded_edge.b_id)
                self.assertEqual(orig_edge.a.x, loaded_edge.a.x)
                self.assertEqual(orig_edge.a.y, loaded_edge.a.y)
                self.assertEqual(orig_edge.b.x, loaded_edge.b.x)
                self.assertEqual(orig_edge.b.y, loaded_edge.b.y)
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_empty_graph(self):
        """Test serialization of an empty graph"""
        empty_graph = Graph(nodes=[], edges=[])

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name

        try:
            empty_graph.to_json_file(temp_path)
            loaded_graph = Graph.from_json_file(temp_path)

            self.assertEqual(len(loaded_graph.nodes), 0)
            self.assertEqual(len(loaded_graph.edges), 0)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()