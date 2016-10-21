from quantity import Quantity
from problem import Problem
from plot import Plot

class Search:

    def __init__():
        pass

    def equal_states(state1, state2):
        return (len(set(state1.items()) & set(state2.items())) == len(state1.items()))

    def already_in_states(state1, state2):
        return (len(set(state1.items()) & set(state2.items())) == len(state1.items))

    # @staticmethod
    # def hash_state(state):
    #     sorted_keys = sorted(state.keys())
    #     result_hash = ''
    #
    #     for key in sorted_keys:
    #         result_hash += key + str(state[key]) + '\n'
    #
    #     return result_hash

    @staticmethod
    def recursive(problem, state, depth, visited_states):
        results = problem.succ(state)
        for result in results:
            print(depth * '\t' + str(result))
            Search.recursive(problem, result, depth+1, visited_states)

    @staticmethod
    def iterative(problem, state):
        result = {problem.hash_state(state): {'state': state, 'children': set([])}}
        if problem.logfile!= None:
            print("The program starts to explore from the initial state "+problem.state2printstring(state)+" iteratively expanding the graph of possible beahaviours")

        processing_list = [state]
        while processing_list:
            processing_state = processing_list.pop(0)
            if problem.logfile!= None:
                print("Popping the state "+problem.state2printstring(state)+" from the list of the states to explore")
            succesors = problem.succ(processing_state)
            for succ in succesors:
                hashed_state = problem.hash_state(succ)
                result[problem.hash_state(processing_state)]['children'].add(hashed_state)
                if hashed_state not in result:
                    if problem.logfile!= None:
                        print("Adding the state "+problem.state2printstring(state)+" to the list of the states to explore")
                    result[hashed_state] = {'state': succ, 'children': set([])}
                    processing_list.append(succ)
                elif problem.logfile!= None:
                    print("The state "+problem.state2printstring(state)+" was already explored")

        if problem.logfile!= None:
                        print("The list of the states to explore is empty: terminating the program")
        return result


if __name__ == "__main__":
    inflow = Quantity("Inflow", [("Zero", False, 0), ("Plus", True, 1)])
    tank = Quantity("Tank", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])
    height = Quantity("Height", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])
    pressure = Quantity("Pressure", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])
    outflow = Quantity("Outflow", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])

    tank.influence(inflow, positive=True)
    tank.influence(outflow, positive=False)
    height.proportional(tank, positive=True)
    pressure.proportional(height, positive=True)
    outflow.proportional(pressure, positive=True)

    tank.value_constraint(outflow, "Max", "Max")
    outflow.value_constraint(tank, "Max", "Max")
    tank.value_constraint(height, "Max", "Max")
    height.value_constraint(tank, "Max", "Max")
    tank.value_constraint(pressure, "Max", "Max")
    pressure.value_constraint(tank, "Max", "Max")
    tank.value_constraint(outflow, "Zero", "Zero")
    outflow.value_constraint(tank, "Zero", "Zero")
    tank.value_constraint(height, "Zero", "Zero")
    height.value_constraint(tank, "Zero", "Zero")
    tank.value_constraint(pressure, "Zero", "Zero")
    pressure.value_constraint(tank, "Zero", "Zero")

    prob1 = Problem([inflow, tank, height, pressure, outflow], fixed=False, logfile=True)

    start_state = {"Inflow": ["Plus", 0], "Tank": ["Zero", 1], "Outflow": ["Zero", 1]}
    start_state = {"Inflow": ["Zero", 0], "Tank": ["Zero", 0], "Height": ["Zero", 0], "Pressure": ["Zero", 0], "Outflow": ["Zero", 0]}
    # for i in prob1.succ(start_state):
    #     print(i)
    # for k, v in Search.iterative(prob1, start_state).items():
    #     print(v['state'])
    # for i in prob1.succ(start_state):
    #     print(i)
    result = Search.iterative(prob1, start_state)
    print(len(result))
    Plot.draw(result, 'result.png')
    # results = prob1.succ({"Inflow": ("Zero", 1), "Tank": ("Zero", 0), "Outflow": ("Zero", 0)})
    # for res in results:
    #     print(res)


