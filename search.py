from quantity import Quantity
from problem import Problem
from plot import Plot


class Search:

    # def __init__(self):
    #    pass

    # def equal_states(state1, state2):
    #     return (len(set(state1.items()) & set(state2.items())) == len(state1.items()))
    #
    # def already_in_states(state1, state2):
    #     return (len(set(state1.items()) & set(state2.items())) == len(state1.items))

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
            successors = problem.succ(processing_state)
            for succ in successors:
                if problem.hash_state(succ) != problem.hash_state(processing_state):
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

def base_prob():
    inflow = Quantity("Inflow", [("Zero", False, 0), ("Plus", True, 1)])
    volume = Quantity("Tank", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])
    outflow = Quantity("Outflow", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])

    volume.influence(inflow, positive=True)
    volume.influence(outflow, positive=False)
    outflow.proportional(volume, positive=True)

    volume.value_constraint(outflow, "Max", "Max")
    outflow.value_constraint(volume, "Max", "Max")
    volume.value_constraint(outflow, "Zero", "Zero")
    outflow.value_constraint(volume, "Zero", "Zero")

    return inflow, volume, outflow

def frog_prob():
    population = Quantity("Population", [("Zero", False, 0), ("Small", True, 1), ("Medium", False, 1), ("Large", True, 1)])
    birth = Quantity("Birth", [("Zero", False, 0), ("Plus", True, 1)])
    death = Quantity("Death", [("Zero", False, 0), ("Plus", True, 1)])

    population.influence(birth, positive=True)
    population.influence(death, positive=False)
    birth.proportional(population, positive=True)
    death.proportional(population, positive=True)

    return population, birth, death

def extra_prob():
    inflow = Quantity("Inflow", [("Zero", False, 0), ("Plus", True, 1)])
    volume = Quantity("Tank", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])
    height = Quantity("Height", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])
    pressure = Quantity("Pressure", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])
    outflow = Quantity("Outflow", [("Zero", False, 0), ("Plus", True, 1), ("Max", False, 1)])

    volume.influence(inflow, positive=True)
    volume.influence(outflow, positive=False)
    outflow.proportional(pressure, positive=True)
    pressure.proportional(height, positive=True)
    height.proportional(volume, positive=True)

    pressure.value_constraint(outflow, "Max", "Max")
    outflow.value_constraint(pressure, "Max", "Max")
    pressure.value_constraint(outflow, "Zero", "Zero")
    outflow.value_constraint(pressure, "Zero", "Zero")

    pressure.value_constraint(height, "Max", "Max")
    height.value_constraint(pressure, "Max", "Max")
    pressure.value_constraint(height, "Zero", "Zero")
    height.value_constraint(pressure, "Zero", "Zero")

    volume.value_constraint(height, "Max", "Max")
    height.value_constraint(volume, "Max", "Max")
    volume.value_constraint(height, "Zero", "Zero")
    height.value_constraint(volume, "Zero", "Zero")

    return inflow, volume, height, pressure, outflow

if __name__ == "__main__":
<<<<<<< HEAD
    inflow, tank, outflow, height, pressure = extra_prob()

    #inflow, tank, outflow = base_prob()
    prob1 = Problem([inflow, tank, outflow, height, pressure], fixed=False, logfile=True)

    start_state = {"Inflow": ["Zero", 1], "Tank": ["Zero", 0], "Outflow": ["Zero", 0], "Height": ["Zero", 0], "Pressure": ["Zero", 0]}
    # start_state = {"Inflow": ["Plus", 1], "Tank": ["Plus", -1], "Outflow": ["Plus", -1]}

    # for i in prob1.succ(start_state):
    #     print(i)
    # for k, v in Search.iterative(prob1, start_state).items():
    #     print(v['state'])
    # for i in prob1.succ(start_state):
    #     print(i)
    result = Search.iterative(prob1, start_state)
    print(len(result))
    #Plot.draw(result, 'result.png')
    # results = prob1.succ({"Inflow": ("Zero", 1), "Tank": ("Zero", 0), "Outflow": ("Zero", 0)})
    # for res in results:
    #     print(res)





=======
    inflow, tank, outflow = base_prob()
    base_problem = Problem([inflow, tank, outflow], fixed=False, logfile=True)
    base_start_state = {"Inflow": ["Zero", 0], "Tank": ["Zero", 0], "Outflow": ["Zero", 0]}
    result_base_problem = Search.iterative(base_problem, base_start_state)
    Plot.draw(result_base_problem, 'result_base_problem.png')

    # inflow, tank, height, pressure, outflow = extra_prob()
    # extra_problem = Problem([inflow, tank, height, pressure, outflow], fixed=False, logfile=True)
    # extra_start_state = {"Inflow": ["Zero", 0], "Tank": ["Zero", 0], "Height": ["Zero", 0], "Pressure": ["Zero", 0], "Outflow": ["Zero", 0]}
    # result_extra_problem = Search.iterative(extra_problem, extra_start_state)
    # Plot.draw(result_extra_problem, 'result_extra_problem.png')

    print(len(result_base_problem))
    # print(len(result_extra_problem))

    # population, birth, death = frog_prob()
    # prob1 = Problem([population, birth, death], fixed=True, logfile=True)
    # start_state = {"Population": ["Small", 1], "Birth": ["Plus", 1], "Death": ["Plus", 1]}
>>>>>>> 03b8defbea0b5604eef48a89f9ddc38da8609bd1


