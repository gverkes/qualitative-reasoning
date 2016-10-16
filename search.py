from quantity import Quantity
from problem import Problem

class Search:

    def __init__():
        pass

    # def equal_states(state1, state2):
    #     return (len(set(state1.items()) & set(state2.items())) == len(state1.items))
    #
    # def already_in_states(state1, state2):
    #     return (len(set(state1.items()) & set(state2.items())) == len(state1.items))


    @staticmethod
    def recursive(problem, state, depth, visited_states):
        if depth < 4:
            results = problem.succ(state)
            for result in results:
                print(depth * '\t' + str(result))
                Search.recursive(problem, result, depth+1, visited_states)

if __name__ == "__main__":
    inflow = Quantity("Inflow", [("Zero", False, 0), ("Plus", True, 1)])
    tank = Quantity("Tank", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])
    outflow = Quantity("Outflow", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])

    tank.influence(inflow, positive=True)
    tank.influence(outflow, positive=False)
    outflow.proportional(tank, positive=True)

    tank.value_constraint(outflow, "Max", "Max")
    outflow.value_constraint(tank, "Max", "Max")
    tank.value_constraint(tank, "Zero", "Zero")
    outflow.value_constraint(tank, "Zero", "Zero")

    prob1 = Problem([tank,inflow, outflow], fixed=True)


    visited_states = []
    Search.recursive(prob1, {"Inflow": ("Zero", 1), "Tank": ("Zero", 0), "Outflow": ("Zero", 0)}, 0, visited_states)
    # results = prob1.succ({"Inflow": ("Zero", 1), "Tank": ("Zero", 0), "Outflow": ("Zero", 0)})
    # for res in results:
    #     print(res)


