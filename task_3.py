import pickle
import random
import networkx as nx


def load_graph(filename='ubahn_graph.pkl'):
    """Load the graph from a pickle file."""
    with open(filename, 'rb') as f:
        return pickle.load(f)


def add_random_weights(graph, min_weight=2, max_weight=3, seed=42):
    """
    Add random weights to all edges in the graph.
    
    Args:
        graph: NetworkX graph
        min_weight: Minimum weight value
        max_weight: Maximum weight value
        seed: Random seed for reproducibility
    
    Returns:
        NetworkX graph with weighted edges
    """
    # Set seed for reproducibility
    random.seed(seed)
    
    # Create a copy of the graph to avoid modifying the original
    weighted_graph = graph.copy()
    
    # Add random weights to each edge
    for u, v in weighted_graph.edges():
        weight = random.uniform(min_weight, max_weight)
        weighted_graph[u][v]['weight'] = round(weight, 2)
    
    return weighted_graph


def dijkstra_shortest_path(graph, start, goal):
    """
    Find the shortest path using Dijkstra's algorithm.
    
    Dijkstra's algorithm finds the shortest path in a weighted graph
    by exploring nodes in order of their distance from the start node.
    
    Args:
        graph: NetworkX graph with weighted edges
        start: Starting node
        goal: Goal node
    
    Returns:
        tuple: (path, total_distance, edge_details)
    """
    try:
        # Use NetworkX's implementation of Dijkstra's algorithm
        path = nx.dijkstra_path(graph, start, goal, weight='weight')
        total_distance = nx.dijkstra_path_length(graph, start, goal, weight='weight')
        
        # Get detailed information about each edge in the path
        edge_details = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            weight = graph[u][v]['weight']
            edge_details.append((u, v, weight))
        
        return path, total_distance, edge_details
    
    except nx.NetworkXNoPath:
        return None, None, None
    except nx.NodeNotFound:
        return None, None, None


def display_shortest_path(graph, start, goal):
    """Display the shortest path found by Dijkstra's algorithm."""
    
    print("=" * 80)
    print(f"DIJKSTRA'S ALGORITHM: Finding shortest weighted path")
    print("=" * 80)
    print(f"\nRoute: {start} → {goal}")
    print("-" * 80)
    
    path, total_distance, edge_details = dijkstra_shortest_path(graph, start, goal)
    
    if path is None:
        print(f"❌ No path found between {start} and {goal}")
        return
    
    print(f"\n✓ Shortest path found!")
    print(f"\nTotal distance: {total_distance:.2f} units")
    print(f"Number of stations: {len(path)}")
    print(f"Number of segments: {len(edge_details)}")
    
    print("\n" + "-" * 80)
    print("DETAILED ROUTE:")
    print("-" * 80)
    
    # Display the complete path
    print("\nPath: " + " → ".join(path))
    
    # Display edge-by-edge breakdown
    print("\n" + "-" * 80)
    print("SEGMENT BREAKDOWN:")
    print("-" * 80)
    print(f"{'#':<5} {'From':<30} {'To':<30} {'Weight':<10}")
    print("-" * 80)
    
    for i, (u, v, weight) in enumerate(edge_details, 1):
        print(f"{i:<5} {u:<30} {v:<30} {weight:<10.2f}")
    
    print("-" * 80)
    print(f"{'TOTAL DISTANCE:':<65} {total_distance:.2f}")
    print("=" * 80)
    
    return path, total_distance


def compare_with_bfs(graph, start, goal, dijkstra_distance):
    """Compare Dijkstra's result with BFS (unweighted shortest path)."""
    
    print("\n" + "=" * 80)
    print("COMPARISON: Dijkstra vs BFS (Unweighted)")
    print("=" * 80)
    
    # Get unweighted shortest path using BFS
    try:
        bfs_path = nx.shortest_path(graph, start, goal)
        bfs_length = len(bfs_path)
        
        # Calculate the total weight if we followed the BFS path
        bfs_weighted_distance = 0
        for i in range(len(bfs_path) - 1):
            u, v = bfs_path[i], bfs_path[i + 1]
            bfs_weighted_distance += graph[u][v]['weight']
        
        print(f"\nBFS (unweighted shortest path):")
        print(f"  - Number of stations: {bfs_length}")
        print(f"  - Weighted distance: {bfs_weighted_distance:.2f} units")
        print(f"  - Path: {' → '.join(bfs_path)}")
        
        print(f"\nDijkstra (weighted shortest path):")
        print(f"  - Weighted distance: {dijkstra_distance:.2f} units")
        
        print(f"\n📊 Analysis:")
        if abs(bfs_weighted_distance - dijkstra_distance) < 0.01:
            print(f"  ✓ Both algorithms found the same path")
        else:
            savings = bfs_weighted_distance - dijkstra_distance
            savings_percent = (savings / bfs_weighted_distance) * 100
            print(f"  ✓ Dijkstra found a path {savings:.2f} units shorter ({savings_percent:.1f}% better)")
            print(f"  ✓ This demonstrates the importance of considering edge weights!")
        
    except nx.NetworkXNoPath:
        print("  ❌ No path found with BFS")
    
    print("=" * 80)


def demonstrate_dijkstra(graph, start, goal):
    """Main function to demonstrate Dijkstra's algorithm."""
    
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "DIJKSTRA'S ALGORITHM DEMO" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")
    
    print(f"\nGraph Statistics:")
    print(f"  - Total stations: {graph.number_of_nodes()}")
    print(f"  - Total connections: {graph.number_of_edges()}")
    print(f"  - Edge weights: randomly assigned between 2.0 and 3.0 units")
    
    # Display some sample weights
    print(f"\nSample edge weights (first 5):")
    for i, (u, v, data) in enumerate(list(graph.edges(data=True))[:5], 1):
        weight = data.get('weight', 'N/A')
        print(f"  {i}. {u} ↔ {v}: {weight:.2f} units")
    
    print("\n" + "=" * 80)
    
    # Find shortest path using Dijkstra
    path, distance = display_shortest_path(graph, start, goal)
    
    if path:
        # Compare with BFS
        compare_with_bfs(graph, start, goal, distance)
    
    print("\n" + "=" * 80)
    print("KEY CONCEPTS:")
    print("=" * 80)
    print("""
Dijkstra's Algorithm:
  • Finds the shortest path in a weighted graph
  • Always explores the node with the smallest known distance first
  • Guarantees optimal solution for non-negative edge weights
  • Time complexity: O((V + E) log V) with binary heap
  • Use case: Navigation systems, network routing, cost optimization

BFS (for comparison):
  • Finds shortest path by number of edges (unweighted)
  • Does NOT consider edge weights
  • Simpler but less accurate when weights matter
  • Use case: When all edges have equal cost
""")
    print("=" * 80)


def main():
    # Load the graph
    print("Loading Berlin U-Bahn network from pickle file...")
    G = load_graph('ubahn_graph.pkl')
    print(f"✓ Graph loaded: {G.number_of_nodes()} stations, {G.number_of_edges()} connections")
    
    # Add random weights to edges
    print("\nAdding random weights (2.0 - 3.0) to all edges...")
    weighted_G = add_random_weights(G, min_weight=2, max_weight=3, seed=42)
    print(f"✓ Weights added to {weighted_G.number_of_edges()} edges")
    
    # Run Dijkstra's algorithm
    start_station = "Viktoria-Luise-Platz"
    goal_station = "Weberwiese"
    
    demonstrate_dijkstra(weighted_G, start_station, goal_station)


if __name__ == "__main__":
    main()
