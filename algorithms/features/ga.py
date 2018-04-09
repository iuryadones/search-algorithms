

class Base(object):

    """
    Docstring for GA.
        - Initialization
        - Fitness
        - Selection
        - Crossover
        - Mutation
    """

    def __init__(self, *args, **kwargs):
        """
        Define init
            - length population
            - type individual
            - setattr chromosomes
            - method of initialization
            - method of selection
            - method of crossover
            - method of mutation
        """

        self.chromosomes = kwargs.get('chromosomes', [])
        self.individual = kwargs.get('individual', list)
        self.population = kwargs.get('population', 30)


if __name__ == "__main__":
    ga_base = Base()
    print(ga_base.chromosomes)
    print(ga_base.individual)
    print(ga_base.population)

