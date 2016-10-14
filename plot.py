
import matplotlib.pyplot as plt
import networkx as nx


def drawGraph(g):
    G = nx.Graph()


class NodeTest:

    def __init__(self, n):
        self.__n = n

    def get_name(self):
        return self.__n

    def get_quantities(self):
        return QuantityTest("0", -1), QuantityTest("+", 0), QuantityTest("MAX", 1)

    def get_child(self):
        return None


class QuantityTest:

    def __init__(self, v, d):
        self.__v = v
        self.__d = d

    def get_values(self):
        return "0", "+", "MAX"

    def get_derivatives(self):
        return "+", "0", "-"

    def get_val(self):
        return self.__v

    def get_dev(self):
        return self.__d
