from copy import deepcopy, copy


class Problem:


    def __init__(self, quantities, fixed=False,logfile=None):
        self.quantities = quantities
        self.fixed = fixed
        self.logfile=logfile

    def hash_state(self, state):
        sorted_keys = [q.name for q in self.quantities]
        result_hash = ''

        for key in sorted_keys:
            result_hash += key + ": "
            for q in state[key][:-1]:
                result_hash += str(q) + ", "
            result_hash += str(state[key][-1]) + '\n'

        return result_hash
    def state2printstring(self,state):
        s=self.hash_state(state)
        return "("+s.replace("\n", " ").replace(", None","")+")"

    def succ(self, state):
        new_states = [{}]

        # Evolving, i.e. changing values based on derivatives
        if self.logfile!=None:
            print("--->Expanding the node ("+self.state2printstring(state)+") to determine its successors:")
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



        if self.logfile!=None:
            print("\t\t for each quantity we determine the possible values in which it can trasition (using its actual value and its derivative):")
        if self.logfile!=None:
            if new_states:

                for quantity in self.quantities:
                    value, derivative = state[quantity.name]
                    print("\t\t\t  "+quantity.name+" : "+str(quantity.next_value(value, derivative)).replace("["," ").replace("]"," "))
            else:
                print("\t\t One of the quantities has no successors, thus the state is a terminal state\n")



        # Value constraints, i.e. filtering out states not matching value constraints
        if self.logfile!=None:
            print("\t\t For each possible combinaton of values we then check if they respect the value constraints ")
        vc_new_states = []
        for s in new_states:
            if not self.check_constraints(s):
                vc_new_states.append(s)
        new_states = vc_new_states

        if self.logfile!=None:
            if not new_states:
                print("\t\t After imposing value constraints one of the quntities has no successors, thus the state is a terminal state\n")
            else:
                print("\t\t Now for each possible combination of values we propagate the constraints to determine the possible values the derivative can assume\n")
                print("\t\t First for each quantity we propagate influences")

        # Influence propogations, i.e. computing new derivatives based on influences
        for quantity in self.quantities:
            if quantity.hasInfluences():
                if self.logfile!=None and new_states:
                    print("\t\t\t The quantity "+quantity.name+" receives the influences " + str([(q[0].name, '+' if q[1] else '-') for q in quantity.influences]))
                quantity_new_states = []
                while new_states:
                    new_dict = new_states.pop(0)
                    if self.logfile!=None :
                        print("\t\t\t\t In the state "+self.state2printstring(new_dict)+" the quantity "+quantity.name+" can have derivative "+str([deri for deri in self.propagate_influences(quantity, state, new_dict)]) )

                    for deri in self.propagate_influences(quantity, state, new_dict):
                        value_new_dict = deepcopy(new_dict)
                        value_new_dict[quantity.name][1] = deri
                        quantity_new_states.append(value_new_dict)
                new_states = quantity_new_states


        final_new_states = []
        if self.logfile!=None and new_states:
                    print("\n\t\t Now for each state we propagate proportionals, we resolve proportionality chains using recursive calls")
        for new_state in new_states:
            final_new_states += self.propagate_proportionals(state, new_state)

        if self.logfile!=None:
            print("---> The state"+self.state2printstring(state)+" can transition to "+str([self.state2printstring(i) for i in  final_new_states]))
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

        if self.logfile!=None:
                print("\t\t\t Processing partial state "+self.state2printstring(new_state))

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
                    elif (deri_new_dict[quantity.name][0] != old_state[quantity.name][0] and interval and deri != old_state[quantity.name][1]) and self.logfile!=None:
                        print("\t\t\t\t discarding partial state "+self.state2printstring(deri_new_dict)+" because it violates continuity constraints")
            new_states = quantity_new_states

        if self.logfile!=None:
            for i in new_states:
                print("\t\t\t\t adding "+self.state2printstring(i)+" to the list of future states")
        return new_states

    def propagate_proportional(self, quantity, visited_quantities, derivatives, old_state, new_state):
        if self.logfile!=None:
            print("\t\t\t\t recursive call "+quantity.name)
        visited_quantities[quantity.name] = set()
        if not quantity.hasProportionals() and not quantity.hasInfluences():
            if self.logfile!=None :
                print("\t\t\t\t\t the quantity receives no influence or proportionality thus we can determine its derivative arbitrarily")
            _, der = old_state[quantity.name]
            if self.fixed:
                if self.logfile!=None :
                    print("\t\t\t\t\t the settings are derivative='fixed' thus the derivative of "+quantity.name+" remains "+str(der))
                visited_quantities[quantity.name] = set({der})
                derivatives = set({der})
            else:

                visited_quantities[quantity.name] = set({der, min(1, der+1), max(-1, der-1)})
                derivatives = set({der, min(1, der+1), max(-1, der-1)})
                if self.logfile!=None :
                    print("\t\t\t\t\t the settings are derivative='random transition' thus the derivative of "+quantity.name+" takes all the possible value which respect continuity constraints: "+str(derivatives))
        elif not quantity.hasProportionals():
            if self.logfile!=None :
                    print("\t\t\t\t\t the quantity receives only influences thus its derivatives are already assigned ")
            _, der = new_state[quantity.name]
            visited_quantities[quantity.name].add(der)
            derivatives.add(der)
        else:
            if self.logfile!=None :
                print("\t\t\t\t\t the quantity receives the following proportionalities: " + str([(q[0].name, '+' if q[1] else '-') for q in quantity.proportionals]))
            _, der = new_state[quantity.name]
            if der is not None:

                derivatives.add(der)
                visited_quantities[quantity.name].add(der)
            if self.logfile!=None :
                pass
                   # print("\t\t\t\t\t the current partial assignment : is "+ self.state2printstring(new_state))
            for prop_quantity, prop_positive in quantity.proportionals:
                if prop_quantity.name not in visited_quantities:
                    if self.logfile!=None :
                        print("\t\t\t\t\t the derivative of quantity : "+ prop_quantity.name+" is still unassigned.... performing recursive call")
                    visited_quantities, derivatives = self.propagate_proportional(prop_quantity, visited_quantities, derivatives, old_state, new_state)

                derivatives |= set([(1 if prop_positive else -1)*i for i in visited_quantities[prop_quantity.name]])
                if -1 in derivatives and 1 in derivatives:
                    derivatives.add(0)
            if self.logfile!=None :
                print("\t\t\t\t\t propagating proportionality: "+ quantity.name+" can take derivatives : "+str(list(derivatives)))


            visited_quantities[quantity.name] = copy(derivatives)

        return visited_quantities, derivatives

    def check_constraints(self, state):
        for quantity in self.quantities:
            for other_quantity, own_val, other_val in quantity.value_constraints:
                if state[quantity.name][0] == own_val and state[other_quantity.name][0] != other_val:
                    if self.logfile!=None:
                        print("\t\t\t Discard the state "+self.state2printstring(state)+" because "+quantity.name+" = "+state[quantity.name][0]+" and "+other_quantity.name+" = "+state[other_quantity.name][0]+" do not respect the value constraints")
                    return True
        if self.logfile!=None:
            print("\t\t\t In "+self.state2printstring(state)+" all the values respect the value constraints")

        return False
