
import matplotlib.pyplot as plt
#import networkx as nx
#import pygraphviz as pgv

class Plot:

    @staticmethod
    def _status_to_str(status):
        def _dev_to_str(dev):
            if dev > 0:
                return '+'
            elif dev < 0:
                return '-'
            else:
                return '0'

        return '\n'.join((k + ':(' + str(v[0]) + ',' + _dev_to_str(v[1]) + ')' for k, v in sorted(status.items()) if k != 'child'))

    @staticmethod
    def draw(graph, filename, show=True):
        G = pgv.AGraph(directed=True, color='red')

        G.add_nodes_from((k for k, v in graph.items() if v['children']), color='red')
        G.add_nodes_from((k for k, v in graph.items() if not v['children']), color='blue')
        # G.add_nodes_from((k for k, v in graph.items() if 'children' in v for c in v['children'])graph.keys(), color='red')
        G.add_edges_from(((k, c) for k, v in graph.items() if 'children' in v for c in v['children']))
        G.layout(prog='dot')
        G.draw(filename)

        # pos = nx.spring_layout(G,scale=10, iterations=20)

        # nx.draw_networkx(G, pos, node_size=9999, labels={k: Plot._status_to_str(v['state']) for k, v in graph.items()})
        # nx.draw_networkx_nodes(G,pos, node_size=80)
        # nx.draw_networkx_edges(G,pos)

        # plt.axis('off')
        # plt.savefig(filename)
        #
        # if show:
        #     plt.show()
        # A=pgv.AGraph()
        # A.add_edges_from(G.edges())
        # A.layout(prog='dot')
        # A.draw('planar.png')

# test
# g = {
#     'has1': {'state': {'T': ['0', 1], 'O': ['0', 1], 'I': ['+', 1]}, 'children': set(['has2', 'has3'])},
#     'has2': {'state': {'T': ['+', -1], 'O': ['0', -1], 'I': ['M', 0]}},
#     'has3': {'state': {'T': ['-', 0], 'O': ['0', 0], 'I': ['+', 1]}}
# }
#
# Plot.draw(g, 'fig')
