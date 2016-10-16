class Quantity:

    def __init__(self, name, values):
        self.name = name
        self.values, self.intervals, self.signs = zip(*values)
        self.derivatives = [-1, 0, 1]
        self.influences = []
        self.proportionals = []
        self.value_constraints = []
        self.child = False

    def influence(self, quantity, positive=True):
        quantity.child = True
        self.influences.append((quantity, positive))

    def proportional(self, quantity, positive=True):
        quantity.child = True
        self.proportionals.append((quantity, positive))

    def value_constraint(self, quantity, own_val, other_val):
        quantity.child = True
        if own_val in self.values and other_val in quantity.values:
            self.value_constraints.append((quantity, own_val, other_val))
        else:
            raise ValueError('Incorrect value specified')

    def hasProportionals(self):
        return len(self.proportionals) > 0

    def hasInfluences(self):
        return len(self.influences) > 0

    def value2index(self, value):
        return self.values.index(value)

    def next_value(self, value, derivative):
        result = []
        index = self.value2index(value)
        if derivative == 0 or self.intervals[index]:
            result.append(value)

        # Check if there is a next value
        if derivative > 0 and index+1 < len(self.values):
            result.append(self.values[index+1])
        elif derivative < 0 and index-1 >= 0:
            result.append(self.values[index-1])

        return result
