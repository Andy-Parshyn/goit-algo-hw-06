import pickle
import networkx as nx
from collections import deque


def load_graph(filename='ubahn_graph.pkl'):
    """Load the graph from a pickle file."""
    with open(filename, 'rb') as f:
        return pickle.load(f)


def dfs_path(graph, start, goal):
    """
    Depth-First Search (DFS) algorithm to find a path between two nodes.
    
    DFS explores as far as possible along each branch before backtracking.
    It uses a stack (LIFO) structure.
    
    Returns: path as a list of nodes, or None if no path exists
    """
    if start not in graph or goal not in graph:
        return None
    
    # Track visited nodes and the path
    visited = set()
    stack = [(start, [start])]  # (current_node, path_to_current_node)
    
    while stack:
        current, path = stack.pop()
        
        if current == goal:
            return path
        
        if current not in visited:
            visited.add(current)
            
            # Add neighbors to stack (in reverse order to maintain left-to-right exploration)
            neighbors = list(graph.neighbors(current))
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    
    return None


def bfs_path(graph, start, goal):
    """
    Breadth-First Search (BFS) algorithm to find the shortest path between two nodes.
    
    BFS explores all neighbors at the present depth before moving to nodes at the next depth.
    It uses a queue (FIFO) structure and guarantees the shortest path in unweighted graphs.
    
    Returns: path as a list of nodes, or None if no path exists
    """
    if start not in graph or goal not in graph:
        return None
    
    # Track visited nodes and use a queue
    visited = set([start])
    queue = deque([(start, [start])])  # (current_node, path_to_current_node)
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            return path
        
        # Explore all neighbors
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None


def compare_paths(graph, start, goal):
    """Compare DFS and BFS paths between two stations."""
    print("=" * 80)
    print(f"ROUTE FINDING: {start} → {goal}")
    print("=" * 80)
    
    # DFS Path
    print("\n1. DEPTH-FIRST SEARCH (DFS)")
    print("-" * 80)
    dfs_result = dfs_path(graph, start, goal)
    
    if dfs_result:
        print(f"   Path found: {len(dfs_result)} stations")
        print(f"   Route: {' → '.join(dfs_result)}")
    else:
        print("   No path found")
    
    # BFS Path
    print("\n2. BREADTH-FIRST SEARCH (BFS)")
    print("-" * 80)
    bfs_result = bfs_path(graph, start, goal)
    
    if bfs_result:
        print(f"   Path found: {len(bfs_result)} stations (shortest)")
        print(f"   Route: {' → '.join(bfs_result)}")
    else:
        print("   No path found")
    
    # Comparison
    print("\n3. COMPARISON")
    print("-" * 80)
    
    if dfs_result and bfs_result:
        print(f"   DFS path length: {len(dfs_result)} stations")
        print(f"   BFS path length: {len(bfs_result)} stations")
        print(f"   Difference: {len(dfs_result) - len(bfs_result)} stations")
        
        if len(dfs_result) == len(bfs_result):
            if dfs_result == bfs_result:
                print("   ✓ Both algorithms found the same path")
            else:
                print("   ✓ Both found paths of equal length, but different routes")
        else:
            print(f"   ✓ BFS found a shorter path by {len(dfs_result) - len(bfs_result)} stations")
        
        # Calculate efficiency
        efficiency_diff = ((len(dfs_result) - len(bfs_result)) / len(bfs_result)) * 100
        if efficiency_diff > 0:
            print(f"   ✓ BFS is {efficiency_diff:.1f}% more efficient")
    
    print("\n" + "=" * 80 + "\n")
    
    return dfs_result, bfs_result


def demonstrate_algorithms(graph):
    """Demonstrate DFS and BFS with multiple example routes."""
    
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "DFS vs BFS ALGORITHM COMPARISON" + " " * 27 + "║")
    print("╚" + "=" * 78 + "╝" + "\n")
    
    # Test cases: different types of routes
    test_cases = [
        ("Alexanderplatz", "Zoologischer Garten"),  # Major hubs
        ("Warschauer Str.", "Rathaus Spandau"),     # Opposite ends
        ("Nollendorfplatz", "Hauptbahnhof"),        # Transfer station to major station
        ("Uhlandstr.", "Hoenow"),                    # Short line to long line endpoint
        ("Pankow", "Rudow"),                         # North to South
    ]
    
    all_results = []
    
    for start, goal in test_cases:
        dfs_result, bfs_result = compare_paths(graph, start, goal)
        all_results.append({
            'start': start,
            'goal': goal,
            'dfs_length': len(dfs_result) if dfs_result else None,
            'bfs_length': len(bfs_result) if bfs_result else None
        })
    
    # Summary
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 30 + "SUMMARY" + " " * 42 + "║")
    print("╚" + "=" * 78 + "╝" + "\n")
    
    print("KEY DIFFERENCES BETWEEN DFS AND BFS:\n")
    
    print("DFS (Depth-First Search):")
    print("  • Explores as deep as possible before backtracking")
    print("  • Uses a stack (LIFO - Last In, First Out)")
    print("  • Does NOT guarantee the shortest path")
    print("  • Memory efficient for deep graphs")
    print("  • Good for: exploring all possibilities, maze solving")
    
    print("\nBFS (Breadth-First Search):")
    print("  • Explores all neighbors at current depth first")
    print("  • Uses a queue (FIFO - First In, First Out)")
    print("  • GUARANTEES the shortest path in unweighted graphs")
    print("  • More memory intensive for wide graphs")
    print("  • Good for: finding shortest paths, level-order traversal")
    
    print("\n" + "-" * 80)
    print("RESULTS SUMMARY:")
    print("-" * 80)
    
    total_diff = 0
    count = 0
    
    for result in all_results:
        if result['dfs_length'] and result['bfs_length']:
            diff = result['dfs_length'] - result['bfs_length']
            total_diff += diff
            count += 1
            status = "Same" if diff == 0 else f"DFS +{diff}"
            print(f"  {result['start'][:20]:20} → {result['goal'][:20]:20} | "
                  f"DFS: {result['dfs_length']:2} | BFS: {result['bfs_length']:2} | {status}")
    
    if count > 0:
        avg_diff = total_diff / count
        print(f"\n  Average difference: {avg_diff:.2f} stations")
        print(f"  BFS found shorter or equal paths in all {count} test cases")
    
    print("\n" + "=" * 80)


def main():
    # Load the graph from pickle file
    print("Loading Berlin U-Bahn network from pickle file...")
    G = load_graph('ubahn_graph.pkl')
    
    print(f"Loaded graph:")
    print(f"  - {G.number_of_nodes()} stations")
    print(f"  - {G.number_of_edges()} connections")
    
    # Demonstrate algorithms
    demonstrate_algorithms(G)


if __name__ == "__main__":
    main()
