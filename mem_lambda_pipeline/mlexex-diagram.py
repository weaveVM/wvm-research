from diagrams import Diagram, Cluster, Edge
from diagrams.programming.flowchart import Action, InputOutput, Collate

graph_attr = {
    "fontsize": "10",
    "fontname": "Verdana",
    "pad": "0.5",
    "nodesep": "0.5",
    "ranksep": "1.2"
}

node_attr = {
    "style": "filled",
    "fillcolor": "white",
    "height": "1.5",
    "width": "3.0"
}

with Diagram("MEM-Lambda Data Processing Pipeline", show=False, direction="TB", graph_attr=graph_attr, node_attr=node_attr, outformat="png"):
    with Cluster("User"):
        user = InputOutput("Construct MEM-Lambda TX")
    
    with Cluster("WeaveVM\nNetwork"):
        data = InputOutput("MEM-Lambda\ntransaction\ncalldata - canonical chain")

    with Cluster("MLExEx"):
        exex = Action("Detect and Forward\nMEM-Lambda TXs")

    with Cluster("MEM-Lambda\nSequencer"):
        sequencer = Collate("Order and Evaluate\nTXs")

    user >> Edge(label=" posting it onchain") >> data >> Edge(label=" ExEx notification") >> exex >> Edge(label=" forward to sequencer") >> sequencer
