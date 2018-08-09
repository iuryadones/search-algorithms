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
            - operator of initialization
            - operator of selection
            - operator of crossover
            - operator of mutation
        """

        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])

        self.chromosomes = kwargs.get("chromosomes", [])
        self.individual = kwargs.get("individual", list)
        self.population = kwargs.get("population", 30)
        self.parents = {"individual": [], "crossover": [], "mutation": []}
        self._counter_fitness = 0
        self._memoize_fitness = {}

    @property
    def initialization(self):
        """docstring for initialization."""
        self.operator["initialization"](self)

    @property
    def fitness(self):
        """docstring for fitness"""
        return self.operator["fitness"](self)

    @property
    def selection(self):
        """docstring for selection"""
        self.operator["selection"](self)

    @property
    def crossover(self):
        """docstring for crossover"""
        self.operator["crossover"](self)

    @property
    def evaluation(self):
        """docstring for evaluation"""
        self.operator["evaluation"](self)

    @property
    def mutation(self):
        """docstring for mutation"""
        self.operator["mutation"](self)

    def best(self, n=1):
        return self.fitness[0:n]

    @property
    def average(self):
        return sum(map(lambda f: f[1], self.fitness)) / self.population


if __name__ == "__main__":
    ga_base = Base()
    print(ga_base.chromosomes)
    print(ga_base.individual)
    print(ga_base.population)
