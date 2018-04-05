import random

class GA(object):

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


def method_initialization(population=None, chromosomes=None,
                          individual=None, alleles=None, method=None):

    if issubclass(individual, list):
        for _ in range(population):
            chromosome = []
            for allele in alleles:
                choice = method(allele)
                chromosome.append(choice)

            chromosomes.append(chromosome)

        return chromosomes

    else:
        raise NotImplemented


class Queens(GA):

    """Docstring for K-Queens. """

    def __init__(self, *args, **kwargs):
        GA.__init__(self, *args, **kwargs)
        self.k = kwargs.get('k', 4)
        self.alleles = kwargs.get(
            'alleles', [list(range(self.k)) for _ in range(self.k)])

    def initialization(self):
        """docstring for initialization."""

        kwarg = {
            'population': self.population,
            'chromosomes': self.chromosomes,
            'individual': self.individual,
            'alleles': self.alleles,
            'method': random.choice
        }

        self.chromosomes = method_initialization(**kwarg)

    def fitness(self):
        """docstring for fitness"""
        return

    def selection(self):
        """docstring for selection"""
        pass

    def crossover(self):
        """docstring for crossover"""
        pass

    def mutation(self):
        """docstring for mutation"""
        pass

    def __repr__(self):
        _matrix = []
        _len = len(self.chromosomes[0])
        for i,_ in enumerate(range(_len)):
            temp = []
            for j,_ in enumerate(range(_len)):
                if (i + j) % 2 == 0:
                    temp.append(u'\x1b[0;37;40m   \x1b[0m')
                else:
                    temp.append(u'\x1b[0;30;47m   \x1b[0m')
            _matrix.append(temp)

        for chromosome in self.chromosomes:
            clone_m = [[n for n in m] for m in _matrix]

            for col, row in enumerate(chromosome):
                if (col + row) % 2 == 0:
                    clone_m[row][col] = (u'\x1b[0;37;40m Q \x1b[0m')
                else:
                    clone_m[row][col] = (u'\x1b[0;30;47m Q \x1b[0m')

            print(end='\n')
            for m in clone_m:
                print(''.join(m))
            print(end='\n')

        return(f'Population: {len(self.chromosomes)}')

def main():

    queens = Queens(population=4, k=4)
    print(queens.population)
    print(queens.individual)
    queens.initialization()
    print(queens.chromosomes)
    print(queens)

if __name__ == "__main__":
    main()

