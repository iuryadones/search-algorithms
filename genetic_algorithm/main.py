import random
from collections import Counter

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

def method_fitness(chromosomes, k, memoize_fitness):
    chromosomes_fitness = []
    for chromosome in chromosomes:
        chromosome_str = ''.join([f'{gene}' for gene in chromosome])
        chromosome_resp = memoize_fitness.get(chromosome_str)
        if not chromosome_resp:
            resp_side = [(chromosome.count(gene) - 1) for gene in chromosome]
            resp_diag = [
                [
                    False,
                    (row, col) != (chromosome[i], i)
                ][abs(row-chromosome[i]) == abs(col - i)]
                for i in range(k)
                for col, row in enumerate(chromosome)
            ]
            chromosome_resp = sum(resp_side) + resp_diag.count(True)
            memoize_fitness[chromosome_str] = chromosome_resp
            chromosomes_fitness.append([chromosome, chromosome_resp])
        else:
            chromosomes_fitness.append([chromosome, chromosome_resp])
    return sorted(chromosomes_fitness,
                  key=lambda chromo_fitness: chromo_fitness[1])

class Queens(GA):

    """Docstring for K-Queens. """

    def __init__(self, *args, **kwargs):
        GA.__init__(self, *args, **kwargs)
        self.k = kwargs.get('k', 4)
        self.alleles = kwargs.get(
            'alleles', [list(range(self.k)) for _ in range(self.k)])
        self._memoize_fitness = {}
        self.prob_selection = kwargs.get('prob_selection', 0.2)
        self.prob_mating = kwargs.get('prob_mating', 0.2)
        self.select_parents = kwargs.get('select_parents', 2)
        self.pair_recobinition = kwargs.get('pair_recobinition', 2)
        self.parents = []

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

    def fitness(self, pairs_individuals=None):
        """docstring for fitness"""
        if pairs_individuals:
            return method_fitness(pairs_individuals, self.k, self._memoize_fitness)
        else:
            return method_fitness(self.chromosomes, self.k, self._memoize_fitness)

    def selection(self):
        """docstring for selection"""
        self.parents = []
        chromosomes = [
            [chromosome, fitness] for n, (chromosome, fitness) in
            enumerate(self.fitness())
            if n < self.select_parents + 2
        ]


        for _ in range(self.select_parents):
            chromosome = chromosomes.pop(
                chromosomes.index(random.choice(chromosomes))
            )
            self.parents.append(self.chromosomes.pop(self.chromosomes.index(chromosome[0])))

    def crossover(self):
        """docstring for crossover"""
        pairs_individual = []
        for _ in range(int(len(self.parents)/2)):
            point = random.randint(1, 6)
            individual_1 = self.parents.pop(
                self.parents.index(random.choice(self.parents))
            )
            individual_2 = self.parents.pop(
                self.parents.index(random.choice(self.parents))
            )
            new_individual_1 = individual_1[:point] + individual_2[point:]
            new_individual_2 = individual_2[point:] + individual_1[:point]

            pairs_individual.append(individual_1)
            pairs_individual.append(individual_2)
            pairs_individual.append(new_individual_1)
            pairs_individual.append(new_individual_2)

        pairs_individual = [
            chromosome
            for n, (chromosome, fitness) in enumerate(
                self.fitness(pairs_individual)
            ) if n < self.select_parents
        ]

        self.parents = pairs_individual
        self.chromosomes.extend(pairs_individual)

    def mutation(self):
        """docstring for mutation"""
        individuals_mutants = []
        points = random.randint(1, len(self.alleles)-1)
        for _ in range(len(self.parents)):
            chromosome = self.parents.pop(
                self.parents.index(
                    random.choice(self.parents)
                )
            )
            random_choice = []
            while len(random_choice) == points:
                gene = random.randint(0, len(self.alleles)-1)
                if not (gene in random_choice):
                    chromosome[gene] = random.choice(self.alleles[gene])
                    random_choice.append(gene)
            individuals_mutants.append(chromosome)

        individuals_mutants = [
            chromosome
            for n, (chromosome, fitness) in enumerate(
                self.fitness(individuals_mutants)
            ) if n < self.select_parents
        ]

        self.chromosomes.extend(individuals_mutants)
        self.chromosomes = [
            chromosome
            for n, (chromosome, fitness) in enumerate(
                self.fitness(self.chromosomes)
            ) if n < self.population
        ]


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
    queens = Queens(population=6, k=4)
    queens.initialization()
    queens.show_chromosomes_fitness
    for _ in range(10):
        queens.selection()
        queens.crossover()
        queens.mutation()
        queens.show_chromosomes_fitness
        print(Counter([fitness[1] for fitness in queens.fitness()]))


if __name__ == "__main__":
    main()

