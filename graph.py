from graphViz import Digraph

# BFS to build the graph
def trace(root):
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v.prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges

# Visualize the graph
def draw_dot(root):
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'})  # LR = left to right

    # create set of nodes and edges with trace()
    nodes, edges = trace(root)
    # create nodes, edges, and operators using .node & .edge
    for n in nodes:
        # instantiate node
        dot.node(name=str(id(n)), label="{ data %.4f | grad %.4f }" %(n.data, n.grad), shape='record')
        # if created by an operation, create an op node
        if n._op:
            dot.node(name=str(id(n)) + n._op, label=n._op)
            # connect op node to value node
            dot.edge(str(id(n)) + n._op, str(id(n)))

    for n1, n2 in edges:
        # connect value node to op node
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)

    return dot