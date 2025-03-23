import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt

ox.settings.use_cache = True

# Map around Loughborough
# download street network data from OSM and construct a MultiDiGraph model

network_type = "drive_service"
G = ox.graph.graph_from_point(
    (52.7723859, -1.2077985), dist=3500, network_type=network_type
)

# impute edge (driving) speeds and calculate edge travel times
G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

# you can convert MultiDiGraph to/from GeoPandas GeoDataFrames
gdf_nodes, gdf_edges = ox.convert.graph_to_gdfs(G)
G = ox.convert.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs=G.graph)

# convert MultiDiGraph to DiGraph to use nx.betweenness_centrality function
# choose between parallel edges by minimising travel_time attribute value
D = ox.convert.to_digraph(G, weight="travel_time")

# calculate node betweenness centrality, weighted by travel time
bc = nx.betweenness_centrality(D, weight="travel_time", normalized=True)
nx.set_node_attributes(G, values=bc, name="bc")

# plot the graph, coloring nodes by betweenness centrality
nc = ox.plot.get_node_colors_by_attr(G, "bc", cmap="plasma")
fig, ax = ox.plot.plot_graph(
    G,
    bgcolor="k",
    node_color=nc,
    node_size=5,
    edge_linewidth=2,
    edge_color="#333333",
    save=True,
    filepath=f"./graph_models/{network_type}/graph.png",
    show=False,
)

# save graph as a geopackage or graphml file
ox.io.save_graph_geopackage(
    G, filepath=f"./graph_models/{network_type}/graph.gpkg"
)
ox.io.save_graphml(G, filepath=f"./graph_models/{network_type}/graph.graphml")

print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

# for node in G.nodes(data=True):
#     print(f"Node: {node}")

for edge in G.edges(data=True):
    print(f"Edge: {edge}")
