import csv
from pyvis.network import Network
import networkx as nx
import re

def normalize_number(proposition):
    parts = proposition.split('.')
    new_parts = [parts[0]]  

    for part in parts[1:]:
        new_parts.extend(part)

    return '.'.join(new_parts)

def get_parent(proposition):
    prop = normalize_number(proposition)
    parts = prop.split('.')

    if len(parts) == 1:
        return None  

    parent = '.'.join(parts[:-1])

    while parent.endswith(".0"):
        parent = parent[:-2]

    return parent

def assign_depths(G):
    depths = {}
    queue = []

    for node in G.nodes:
        if G.in_degree(node) == 0:
            depths[node] = 0  
            queue.append(node)

    while queue:
        current = queue.pop(0)
        for neighbor in G.successors(current):  
            if neighbor not in depths:  
                depths[neighbor] = depths[current] + 1
                queue.append(neighbor)

    return depths

def depth_to_color(depth, max_depth):
    if max_depth == 0:  
        return "#FF0000"  
    
    red = int(255 * (1 - depth / max_depth))  
    blue = int(255 * (depth / max_depth))  
    return f"rgb({red},0,{blue})"

def create_graph_from_csv(csv_file, output_html):
    G = nx.DiGraph()
    propositions = []
    node_colors = {}
    node_tooltips = {}

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  

        for row in reader:
            raw_number, content = row
            prop_number = normalize_number(raw_number)  
            propositions.append(prop_number)
            G.add_node(prop_number, title=content)
            node_tooltips[prop_number] = content  # Store tooltip content

            parent = get_parent(prop_number)
            if parent and parent in G.nodes:  
                G.add_edge(parent, prop_number)

    depths = assign_depths(G)
    max_depth = max(depths.values(), default=0)  

    net = Network(directed=True, notebook=True, height="750px", width="100%")
    net.from_nx(G)

    for node in net.nodes:
        node_id = node["id"]
        node["title"] = f"{node_id}: {G.nodes[node_id]['title']}"  
        node["label"] = node_id  
        node["color"] = depth_to_color(depths[node_id], max_depth)  
        node_colors[node_id] = node["color"]  # Store original colors

    # JavaScript for handling key events and copying tooltips
    custom_js = f"""
    <script>
        let propositions = {propositions};  
        let currentIndex = 0;
        let mode = 1;  // 1: Highlight mode, 2: Original mode
        let zoomedIn = false;

        function highlightNode(index) {{
            let nodes = network.body.nodes;
            Object.values(nodes).forEach(node => {{
                node.setOptions({{ color: mode === 1 ? "gray" : originalColors[node.id], borderWidth: 1 }});  
            }});
            
            let selectedNode = nodes[propositions[index]];
            if (selectedNode) {{
                selectedNode.setOptions({{ color: "yellow", borderWidth: 5 }});
                if (zoomedIn) {{
                    zoomToNode(selectedNode.id);
                }}
            }}
        }}

        function zoomToNode(nodeId) {{
            let position = network.getPositions([nodeId])[nodeId];
            network.moveTo({{
                position: position,
                scale: 1.5  
            }});
        }}

        function resetZoom() {{
            network.fit();  
        }}

        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(() => {{
                showNotification("Copied to clipboard!");
            }}).catch(err => {{
                console.error("Failed to copy: ", err);
            }});
        }}

        function showNotification(message) {{
            let notification = document.createElement("div");
            notification.innerText = message;
            notification.style.position = "fixed";
            notification.style.bottom = "20px";
            notification.style.right = "20px";
            notification.style.backgroundColor = "black";
            notification.style.color = "white";
            notification.style.padding = "10px";
            notification.style.borderRadius = "5px";
            notification.style.zIndex = "1000";
            document.body.appendChild(notification);
            
            setTimeout(() => {{
                notification.remove();
            }}, 1500);
        }}

        document.addEventListener('keydown', function(event) {{
            if (event.key === 'ArrowRight' && currentIndex < propositions.length - 1) {{
                currentIndex++;
                highlightNode(currentIndex);
            }} else if (event.key === 'ArrowLeft' && currentIndex > 0) {{
                currentIndex--;
                highlightNode(currentIndex);
            }} else if (event.key === 'Enter') {{
                mode = mode === 1 ? 2 : 1;
                highlightNode(currentIndex);
            }} else if (event.key === 'ArrowUp') {{
                zoomedIn = true;
                zoomToNode(propositions[currentIndex]);
            }} else if (event.key === 'ArrowDown') {{
                zoomedIn = false;
                resetZoom();
            }}
        }});

        let originalColors = {str(node_colors)}; 

        network.on("click", function(params) {{
            if (params.nodes.length > 0) {{
                let nodeId = params.nodes[0];
                let tooltipText = nodeTooltips[nodeId];
                copyToClipboard(tooltipText);
            }}
        }});

        let nodeTooltips = {str(node_tooltips)};

        highlightNode(0);  
    </script>
    """

    net.save_graph(output_html)

    with open(output_html, "a") as file:
        file.write(custom_js)  

    print(f"Graph saved to {output_html}")

if __name__ == "__main__":
    input_csv = "output.csv"  
    output_html = "tractatus_network2.html"
    create_graph_from_csv(input_csv, output_html)
