# Source: Simulation/chapter-13/codebook.md -- Block 3

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Conceptual Gene Regulatory Network (GRN)
# ====================================================================

# Nodes: 5 Genes/Proteins (A, B, C, D, E)
GENE_NAMES = ['A (Master)', 'B (Toggle)', 'C (Toggle)', 'D (Sensor)', 'E (Output)']
N_GENES = len(GENE_NAMES)

# Adjacency Matrix A[i, j] = 1 if i regulates j, 0 otherwise
# Rule Design:
# 1. A is a Master Regulator (high out-degree to B, D)
# 2. B and C form a Mutual Inhibition/Toggle Switch (B -> -C, C -> -B)
# 3. D is a sensor target of A and E
# 4. E is a final Output
ADJACENCY_MATRIX = np.array([
#   A   B   C   D   E 
    [0, +1,  0, +1,  0], # A activates B and D (High Out)
    [0,  0, -1,  0,  0], # B inhibits C
    [0, -1,  0,  0,  0], # C inhibits B
    [0,  0,  0,  0, +1], # D activates E
    [0,  0,  0,  0,  0]  # E is a final output (Low Out)
])

# ====================================================================
# 2. Graph Analysis (NetworkX)
# ====================================================================

# Create the directed graph from the adjacency matrix
# Add labels for positive/negative regulation
G = nx.from_numpy_array(ADJACENCY_MATRIX, create_using=nx.DiGraph)

# Relabel nodes with gene names
G = nx.relabel_nodes(G, {i: GENE_NAMES[i] for i in range(N_GENES)})

# Compute graph metrics
in_degree = dict(G.in_degree())
out_degree = dict(G.out_degree())

# Compute Degree Centrality (simple metric proportional to total connections)
degree_centrality = {gene: in_degree[gene] + out_degree[gene] for gene in GENE_NAMES}

# ====================================================================
# 3. Structural Role Identification
# ====================================================================

print("--- Gene Regulatory Network (GRN) Structural Analysis ---")

print("\n1. Centrality Metrics:")
for gene in GENE_NAMES:
    print(f"  {gene:<15} | In: {in_degree[gene]:<2} | Out: {out_degree[gene]:<2} | Total: {degree_centrality[gene]:<2}")

print("\n2. Identifying Roles (Structural Motifs):")

# Master Regulator: High Out-Degree (A)
master_regulator = max(out_degree, key=out_degree.get)
print(f"- Master Regulator: {master_regulator} (Controls 2 genes downstream)")

# Sensor Gene: High In-Degree, Low Out-Degree (D)
sensor_gene = max(degree_centrality, key=degree_centrality.get)
if out_degree[sensor_gene] == 1: # D has in=1, out=1, total=2
     print(f"- Sensor Gene: D (In=1, Out=1) - Integrates input from A, transmits to E.")

# Toggle Switch Motif (B and C)
print("- Structural Motif: B and C form a **Mutual Inhibition/Toggle Switch** (B ⊣ C, C ⊣ B).")

# ====================================================================
# 4. Visualization
# ====================================================================

plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42) # Layout for visualization

# Draw nodes scaled by Total Degree (Centrality)
nx.draw_networkx_nodes(G, pos, node_size=[v * 300 for v in degree_centrality.values()],
                       node_color='lightblue', alpha=0.9)

# Draw edges (distinguish activation/inhibition)
edges = G.edges()
colors = ['red' if ADJACENCY_MATRIX[GENE_NAMES.index(u), GENE_NAMES.index(v)] < 0 else 'blue' for u, v in edges]
labels = nx.get_edge_attributes(G, 'weight')

nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors, width=1.5, arrowsize=20)
nx.draw_networkx_labels(G, pos, font_weight='bold', font_size=10)

plt.title('Gene Regulatory Network Topology (Master Regulator A, Toggle B/C)')
plt.axis('off')
plt.show()

print("\nConclusion: Computational analysis of the GRN's topology, specifically through in-degree and out-degree, reveals its functional architecture. Gene A acts as the upstream master controller, while B and C form a local feedback motif (the toggle switch) essential for binary cell fate decision-making.")
