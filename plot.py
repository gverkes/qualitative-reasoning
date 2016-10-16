
import matplotlib.pyplot as plt
import networkx as nx

graph = {
    0: {'T': ['0', 1], 'O': ['0', 1], 'I': ['+', 1], 'child': [1, 2]},
    1: {'T': ['+', -1], 'O': ['0', -1], 'I': ['M', 0]},
    2: {'T': ['-', 0], 'O': ['0', 0], 'I': ['+', 1]}
}


def status_to_str(status):
    def dev_to_str(dev):
        if dev > 0:
            return '+'
        elif dev < 0:
            return '-'
        else:
            return '0'

    return'\n'.join((k + ':(' + str(v[0]) + ',' + dev_to_str(v[1]) + ')' for k, v in sorted(status.items()) if k != 'child'))


def drawGraph():
    G = nx.DiGraph()
    G.add_nodes_from(graph.keys())
    G.add_edges_from(((k, c) for k, v in graph.items() if 'child' in v for c in v['child']))
    nx.draw_networkx(G, node_shape='s', node_size=2500, labels={k: status_to_str(v) for k, v in graph.items()})

    plt.axis('off')
    plt.savefig('fig')
    plt.show()

drawGraph()
