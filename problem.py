from copy import deepcopy, copy
from itertools import filterfalse

class Problem:


    def __init__(self, quantities, fixed=False):
        self.quantities = quantities
        self.fixed = fixed

    def hash_state(self, state):
        sorted_keys = [q.name for q in self.quantities]
        result_hash = ''

        for key in sorted_keys:
            result_hash += key + ": "
            for q in state[key][:-1]:
                result_hash += str(q) + ", "
            result_hash += str(state[key][-1]) + '\n'

        return result_hash

    def succ(self, state):
        new_states = [{}]

        # Evolving, i.e. changing values based on derivatives
        for quantity in self.quantities:
            value, derivative = state[quantity.name]
            quantity_new_states = []
            while new_states:
                new_dict = new_states.pop(0)
                for v in quantity.next_value(value, derivative):
                    value_new_dict = deepcopy(new_dict)
                    value_new_dict[quantity.name] = [v, None]
                    quantity_new_states.append(value_new_dict)
                    # print(quantity_new_states)
            new_states = quantity_new_states
            # print('NS: ' + str(new_states))

        # Value constraints, i.e. filtering out states not matching value constraints
        vc_new_states = []
        for s in new_states:
            if not self.check_constraints(s):
                vc_new_states.append(s)
        new_states = vc_new_states

        # Influence propogations, i.e. computing new derivatives based on influences
        for quantity in self.quantities:
            if quantity.hasInfluences():
                quantity_new_states = []
                while new_states:
                    new_dict = new_states.pop(0)
                    for deri in self.propagate_influences(quantity, state, new_dict):
                        value_new_dict = deepcopy(new_dict)
                        value_new_dict[quantity.name][1] = deri
                        quantity_new_states.append(value_new_dict)
                new_states = quantity_new_states


        final_new_states = []
        for new_state in new_states:
            final_new_states += self.propagate_proportionals(state, new_state)

        return final_new_states

    def propagate_influences(self, quantity, old_state, new_state):
        new_der = set()
        change = False
        for infl_quantity, infl_positive in quantity.influences:
            _, der = old_state[infl_quantity.name]
            value, _ = new_state[infl_quantity.name]
            value_idx = infl_quantity.value2index(value)
            sign = infl_quantity.signs[value_idx]

            if sign != 0:
                if infl_positive:
                    new_der.add(sign)
                else:
                    new_der.add(-sign)
            if (der != 0):
                change = True

        if not change:
            new_der = set([old_state[quantity.name][1]])
        elif -1 in new_der and 1 in new_der:
            new_der.add(0)
        elif not new_der:
            new_der.add(0)

        # print(new_der)
        # print(old_state[quantity.name][1])

        new_der = new_der & set([old_state[quantity.name][1], min(1, max(-1, old_state[quantity.name][1] + 1)), min(1, max(-1, old_state[quantity.name][1] - 1))])

        return new_der

    def propagate_proportionals(self, old_state, new_state):

        new_states = [deepcopy(new_state)]

        visited_quantities = {}
        for quantity in self.quantities:
            derivatives = set()
            if quantity.name not in visited_quantities:
                visited_quantities, derivatives = self.propagate_proportional(quantity, visited_quantities, derivatives, old_state, new_state)

            quantity_new_states = []
            while new_states:
                new_dict = new_states.pop(0)
                for deri in visited_quantities[quantity.name]:
                    deri_new_dict = deepcopy(new_dict)
                    new_value = deri_new_dict[quantity.name][0]
                    value_idx = quantity.value2index(new_value)
                    interval = quantity.intervals[value_idx]
                    # print(deri_new_dict[quantity.name][0] != old_state[quantity.name][0])
                    # print(interval)
                    # print(deri != old_state[quantity.name][1])
                    if (not ((deri < 0 and quantity.isMin(new_value)) or (deri > 0 and quantity.isMax(new_value))) \
                            and not (deri_new_dict[quantity.name][0] != old_state[quantity.name][0] \
                                     and interval and deri != old_state[quantity.name][1])):
                        deri_new_dict[quantity.name][1] = deri
                        quantity_new_states.append(deri_new_dict)
            new_states = quantity_new_states

        return new_states

    def propagate_proportional(self, quantity, visited_quantities, derivatives, old_state, new_state):
        visited_quantities[quantity.name] = set()
        if not quantity.hasProportionals() and not quantity.hasInfluences():
            _, der = old_state[quantity.name]
            if self.fixed:
                visited_quantities[quantity.name] = set({der})
                derivatives = set({der})
            else:
                visited_quantities[quantity.name] = set({der, min(1, der+1), max(-1, der-1)})
                derivatives = set({der, min(1, der+1), max(-1, der-1)})
        elif not quantity.hasProportionals():
            _, der = new_state[quantity.name]
            visited_quantities[quantity.name].add(der)
            derivatives.add(der)
        else:
            _, der = new_state[quantity.name]
            if der is not None:
                derivatives.add(der)
                visited_quantities[quantity.name].add(der)

            for prop_quantity, prop_positive in quantity.proportionals:
                if prop_quantity.name not in visited_quantities:
                    visited_quantities, derivatives = self.propagate_proportional(prop_quantity, visited_quantities, derivatives, old_state, new_state)

                derivatives |= set([(1 if prop_positive else -1)*i for i in visited_quantities[prop_quantity.name]])
                if -1 in derivatives and 1 in derivatives:
                    derivatives.add(0)

            visited_quantities[quantity.name] = copy(derivatives)

        return visited_quantities, derivatives

    def check_constraints(self, state):
        for quantity in self.quantities:
            for other_quantity, own_val, other_val in quantity.value_constraints:
                if state[quantity.name][0] == own_val and state[other_quantity.name][0] != other_val:
                    return True

        return False
