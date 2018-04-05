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
        self._memoize_fitness = {}

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
        chromosomes_fitness = []
        for chromosome in self.chromosomes:
            chromosome_str = ''.join([f'{gene}' for gene in chromosome])
            chromosome_resp = self._memoize_fitness.get(chromosome_str)
            if not chromosome_resp:
                resp_side = [(chromosome.count(gene) - 1) for gene in chromosome]
                resp_diag = []
                for n, gene in enumerate(chromosome):
                    print(gene, [n+gene == n**2+chromosome[i]**2 for i in
                        range(self.k)])
                chromosome_resp = sum(resp_side)
                self._memoize_fitness[chromosome_str] = chromosome_resp
                chromosomes_fitness.append((chromosome, chromosome_resp))
            else:
                chromosomes_fitness.append((chromosome, chromosome_resp))
        return sorted(chromosomes_fitness,
                      key=lambda chromo_fitness: chromo_fitness[1])


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

    @property
    def show_chromosomes(self):
        bg_black = lambda text: f'\x1b[0;37;40m{text}\x1b[0m'
        bg_white = lambda text: f'\x1b[0;30;47m{text}\x1b[0m'
        fg_black = lambda text: f'\x1b[0;37;40m{text}\x1b[0m'
        fg_white = lambda text: f'\x1b[0;30;47m{text}\x1b[0m'

        _matrix = []

        if self.k < 41:
            for i,_ in enumerate(range(self.k)):
                temp = []
                for j,_ in enumerate(range(self.k)):
                    if (i + j) % 2 == 0:
                        temp.append(bg_black('   '))
                    else:
                        temp.append(bg_white('   '))
                _matrix.append(temp)

            for ind, chromosome in enumerate(self.chromosomes):
                clone_m = [[n for n in m] for m in _matrix]

                for col, row in enumerate(chromosome):
                    if (col + row) % 2 == 0:
                        clone_m[row][col] = fg_black(' Q ')
                    else:
                        clone_m[row][col] = fg_white(' Q ')

                print(f'Individual: {ind}')
                for m in clone_m:
                    print(''.join(m))
                print(end='\n')
        else:
            print('Show chromosomes for (k < 41)')

        print(f'Population: {len(self.chromosomes)}\nK: {self.k}')

    @property
    def show_chromosomes_fitness(self):
        bg_black = lambda text: f'\x1b[0;37;40m{text}\x1b[0m'
        bg_white = lambda text: f'\x1b[0;30;47m{text}\x1b[0m'
        fg_black = lambda text: f'\x1b[0;37;40m{text}\x1b[0m'
        fg_white = lambda text: f'\x1b[0;30;47m{text}\x1b[0m'

        _matrix = []

        if self.k < 41:
            for i,_ in enumerate(range(self.k)):
                temp = []
                for j,_ in enumerate(range(self.k)):
                    if (i + j) % 2 == 0:
                        temp.append(bg_black('   '))
                    else:
                        temp.append(bg_white('   '))
                _matrix.append(temp)

            for chromosome, chromo_fitness in self.fitness():
                clone_m = [[n for n in m] for m in _matrix]

                for col, row in enumerate(chromosome):
                    if (col + row) % 2 == 0:
                        clone_m[row][col] = fg_black(' Q ')
                    else:
                        clone_m[row][col] = fg_white(' Q ')

                print(f'Fitness: {chromo_fitness}')
                for m in clone_m:
                    print(''.join(m))
                print(end='\n')
        else:
            print('Show chromosomes for (k < 41)')

        print(f'Population: {len(self.chromosomes)}\nK: {self.k}')


def main():
    queens = Queens(population=4, k=4)
    queens.initialization()
    # queens.show_chromosomes
    queens.fitness()
    queens.show_chromosomes_fitness


if __name__ == "__main__":
    main()

