# Part 1 Generating Clustered Independant Casacde Model
# Install libraries
pip install networkx
pip install pandas
pip install matplotlib
pip install python-louvain==0.15
pip install tqdm

# Import libraries
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random
import community
from tqdm import tqdm

# Sample data
data = pd.read_csv('dataset')

# Create a directed graph
G = nx.Graph()

# Add edges based on the 'Group No' and 'Individual ID' columns
for _, row in data.iterrows():
    group_No = row['Group No']
    individual_id = row['Individual ID']

    # Add edges from the current individual to all others in the same group
    group_members = data[data['Group No'] == group_No]['Individual ID'].tolist()
    edges = [(individual_id, neighbor) for neighbor in group_members if neighbor != individual_id]
    G.add_edges_from(edges)

# Louvain community detection (clustering)
partition = community.best_partition(G)

# Visualize the original graph with Louvain community colors
pos = nx.kamada_kawai_layout(G) # I used Kamada Kawai layout to ensure nodes in the same cluster are joined by the same edges. Also, this layout is aesthetically pleasing.
colors = [partition[node] for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_size=700, node_color=colors, cmap=plt.cm.Oranges, font_size=8, font_color='black', font_weight='bold') #Alter arguements to your satifaction)
plt.title('Clustering Independent Cascade Model') # Input title of your choice
plt.show()

# Part 2: Generating graph of the dataset
# Step 1: Generate a graph from a dataset
df = pd.read_csv('dataset')

# Add a new column 'Area' based on 'Day' and 'Group No'
df['Area'] = df['Day'].astype(str) + '-' + df['Group No'].astype(str)

# Create a graph from the updated DataFrame
G = nx.from_pandas_edgelist(df, 'Group No', 'Individual ID')

# Step 2: Find the top 10 Nodes with the highest centrality
centrality_measures = {
    'Degree Centrality': nx.degree_centrality,# Degree centrality measures the number of edges connected to a node. Nodes with higher degree centrality have more connections and are often considered more central to the network.
    'Closeness Centrality': nx.closeness_centrality, #  Closeness Centrality measures how close a node is to all other nodes in a network.
    'Eigenvector Centrality': nx.eigenvector_centrality, # Eigenvector Centrality measures a node's influence in a network (how many edges the node is connected to other important nodes).  Nodes with high eigenvector centrality are well-connected to other influential nodes, making them important in terms of overall network influence.
    'Betweenness Centrality': nx.betweenness_centrality,  #  Betweenness Centrality quantifies the influence of a node in facilitating the spread in a network
    'Random': lambda G: {node: random.random() for node in G.nodes()},  # Random centrality
}

# Step 3 and 4: Remove top Nodes in descending order and calculate density for each centrality measure
# Density measures the overall connectivity of a network. This measure can be used to quantify the effect of removing particular nodes
results = {measure_name: {'Top Nodes': [], 'Density': []} for measure_name in centrality_measures}

for measure_name, measure_function in centrality_measures.items():
    centrality = measure_function(G)
    top_nodes = sorted(G.nodes(), key=lambda node: centrality[node], reverse=True)[:10]
    results[measure_name]['Top Nodes'] = top_nodes

    densities = []
    for node in tqdm(top_nodes, desc=f'Calculating Density for {measure_name}'):
        G_copy = G.copy()
        G_copy.remove_node(node)
        density = nx.density(G_copy)
        densities.append(density)

    results[measure_name]['Density'] = densities

# Step 5: Generate a graph showing the densities for each centrality measure (sloping downwards)
plt.figure(figsize=(12, 8))

for measure_name, data in results.items():
    plt.plot(range(1, 11), data['Density'][::-1], marker='o', linestyle='-', label=measure_name)

plt.xlabel('No of Nodes Removed')
plt.ylabel('Spread size proportion (Density)')
plt.title('Clustering Independant Casacde mode()') # Input title of your choice
plt.xticks(range(1, 11))
plt.legend()
plt.grid(True)
plt.show()

# Appendix (number of nodes can be altered to your satifaction)
betweenness = nx.betweenness_centrality(G, normalized=False)
sorted(betweenness.items(), key=lambda x:x[1], reverse=True)[0:10]

eigenvector = nx.eigenvector_centrality(G)
sorted(eigenvector.items(), key=lambda x:x[1], reverse=True)[0:10] 

closeness = nx.closeness_centrality(G)
sorted(closeness.items(), key=lambda x:x[1], reverse=True)[0:10]

degree = nx.degree_centrality(G)
sorted(degree.items(), key=lambda x:x[1], reverse=True)[0:10]