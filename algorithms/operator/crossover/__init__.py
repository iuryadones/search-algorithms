
def one_point_mating(self):
    mating_point = self.params['crossover']['mating_point']

    temp_parents = []
    while self.parents.get('individual'):
        individual_1 = self.parents['individual'].pop()
        individual_2 = self.parents['individual'].pop()

        new_individual_1 = individual_1[:mating_point] \
            + individual_2[mating_point:]
        new_individual_2 = individual_2[mating_point:] \
            + individual_1[:mating_point]

        self.parents['crossover'].extend(
            [new_individual_1, new_individual_2]
        )
        temp_parents.extend([individual_1, individual_2])

    self.parents['individual'].extend(temp_parents)
