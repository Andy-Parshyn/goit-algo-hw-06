import json
import pickle
import networkx as nx
import matplotlib.pyplot as plt


def load_ubahn_data(file_path):
    """Load the U-Bahn data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def create_graph_from_ubahn(data):
    """Create a NetworkX graph from U-Bahn data.
    
    Each station is a vertex, and edges connect consecutive stations on each line.
    Transfer stations (appearing on multiple lines) create connections between lines.
    """
    G = nx.Graph()
    
    # Store line information for each station
    station_lines = {}
    line_colors = {}
    
    # Process each U-Bahn line
    for line_name, line_data in data.items():
        stations = line_data['stations']
        color = line_data['color']
        line_colors[line_name] = color
        
        # Add edges between consecutive stations on the line
        for i in range(len(stations) - 1):
            station1 = stations[i]
            station2 = stations[i + 1]
            
            # Add nodes with line information
            if station1 not in station_lines:
                station_lines[station1] = []
            if station2 not in station_lines:
                station_lines[station2] = []
            
            station_lines[station1].append(line_name)
            station_lines[station2].append(line_name)
            
            # Add edge between consecutive stations
            G.add_edge(station1, station2, line=line_name, color=color)
    
    # Add station line information as node attributes
    for station, lines in station_lines.items():
        G.nodes[station]['lines'] = list(set(lines))  # Remove duplicates
        G.nodes[station]['is_transfer'] = len(set(lines)) > 1
    
    return G, station_lines, line_colors


def analyze_graph(G, station_lines):
    """Analyze the graph and return main characteristics."""
    print("=" * 60)
    print("GRAPH ANALYSIS - Berlin U-Bahn Network")
    print("=" * 60)
    
    # 1. Number of vertices (stations)
    num_vertices = G.number_of_nodes()
    print(f"\n1. Number of vertices (stations): {num_vertices}")
    
    # 2. Number of edges (connections)
    num_edges = G.number_of_edges()
    print(f"2. Number of edges (connections): {num_edges}")
    
    # 3. Degree of vertices
    print("\n3. Degree of vertices (Power of vertices):")
    print("-" * 60)
    
    degrees = dict(G.degree())
    
    # Statistics
    avg_degree = sum(degrees.values()) / len(degrees)
    max_degree = max(degrees.values())
    min_degree = min(degrees.values())
    
    print(f"   Average degree: {avg_degree:.2f}")
    print(f"   Maximum degree: {max_degree}")
    print(f"   Minimum degree: {min_degree}")
    
    # Find transfer stations (degree > 2 or multiple lines)
    print("\n   Transfer stations (connecting multiple lines):")
    transfer_stations = []
    for station, lines in station_lines.items():
        unique_lines = set(lines)
        if len(unique_lines) > 1:
            transfer_stations.append((station, len(unique_lines), sorted(unique_lines)))
    
    transfer_stations.sort(key=lambda x: x[1], reverse=True)
    
    for station, num_lines, lines in transfer_stations[:10]:  # Top 10 transfer stations
        degree = degrees[station]
        print(f"   - {station}: degree={degree}, connects {num_lines} lines {lines}")
    
    # Stations with highest degree
    print("\n   Stations with highest degree (most connections):")
    sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    for station, degree in sorted_degrees[:10]:
        lines = station_lines.get(station, [])
        print(f"   - {station}: degree={degree}, lines={sorted(set(lines))}")
    
    # 4. Additional characteristics
    print("\n4. ADDITIONAL GRAPH CHARACTERISTICS:")
    print("-" * 60)
    
    # Check if graph is connected
    is_connected = nx.is_connected(G)
    print(f"   Is the graph connected: {is_connected}")
    
    if is_connected:
        # Diameter (longest shortest path)
        diameter = nx.diameter(G)
        print(f"   Diameter (longest shortest path): {diameter}")
        
        # Average shortest path length
        avg_path_length = nx.average_shortest_path_length(G)
        print(f"   Average shortest path length: {avg_path_length:.2f}")
    else:
        # Number of connected components
        num_components = nx.number_connected_components(G)
        print(f"   Number of connected components: {num_components}")
    
    # Density
    density = nx.density(G)
    print(f"   Graph density: {density:.4f}")
    
    # Total number of transfer stations
    total_transfers = len(transfer_stations)
    print(f"   Number of transfer stations: {total_transfers}")
    
    print("\n" + "=" * 60)
    
    return degrees, transfer_stations


def visualize_graph(G, station_lines, line_colors):
    """Visualize the U-Bahn network graph."""
    plt.figure(figsize=(24, 20))
    
    # Use Kamada-Kawai layout for better visualization
    pos = nx.kamada_kawai_layout(G)
    
    # Separate transfer and regular stations
    transfer_stations = [node for node in G.nodes() if G.nodes[node].get('is_transfer', False)]
    regular_stations = [node for node in G.nodes() if not G.nodes[node].get('is_transfer', False)]
    
    # Draw edges with their respective line colors
    for edge in G.edges(data=True):
        node1, node2, data = edge
        edge_color = data.get('color', 'gray')
        nx.draw_networkx_edges(G, pos, [(node1, node2)], 
                              edge_color=edge_color, 
                              width=2.5, 
                              alpha=0.7)
    
    # Draw regular stations
    nx.draw_networkx_nodes(G, pos, nodelist=regular_stations, 
                           node_color='lightblue', 
                           node_size=150, 
                           alpha=0.9,
                           edgecolors='black',
                           linewidths=1,
                           label='Regular stations')
    
    # Draw transfer stations (highlighted)
    nx.draw_networkx_nodes(G, pos, nodelist=transfer_stations, 
                           node_color='red', 
                           node_size=350, 
                           alpha=0.95,
                           edgecolors='darkred',
                           linewidths=2,
                           label='Transfer stations')
    
    # Draw labels for all stations
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=5, font_weight='normal')
    
    # Create legend for U-Bahn lines
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='lightblue', edgecolor='black', label='Regular stations'),
                      Patch(facecolor='red', edgecolor='darkred', label='Transfer stations')]
    
    # Add U-Bahn line colors to legend
    for line_name in sorted(line_colors.keys()):
        color = line_colors[line_name]
        legend_elements.append(Patch(facecolor=color, label=line_name))
    
    plt.title('Berlin U-Bahn Network Graph', 
              fontsize=16, fontweight='bold')
    plt.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)
    plt.axis('off')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('ubahn_graph.png', dpi=300, bbox_inches='tight')
    print("\nGraph visualization saved as 'ubahn_graph.png'")
    plt.close()


def save_graph(G, filename='ubahn_graph.pkl'):
    """Save the graph to a pickle file for reuse in other scripts."""
    with open(filename, 'wb') as f:
        pickle.dump(G, f)
    print(f"Graph saved as '{filename}'")


def load_graph(filename='ubahn_graph.pkl'):
    """Load a graph from a pickle file."""
    with open(filename, 'rb') as f:
        return pickle.load(f)


def main():
    # Load data
    data = load_ubahn_data('data/ubahn.json')
    
    # Create graph
    G, station_lines, line_colors = create_graph_from_ubahn(data)
    
    # Analyze graph
    degrees, transfer_stations = analyze_graph(G, station_lines)
    
    # Visualize graph
    visualize_graph(G, station_lines, line_colors)
    
    # Save graph for reuse in other files
    save_graph(G, 'ubahn_graph.pkl')


if __name__ == "__main__":
    main()
