from algorithms.features.ga import Base
from collections import Counter
import random
import pylab


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

def method_fitness(chromosomes=None, k=None, memoize_fitness=None):
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

class Queens(Base):

    """Docstring for K-Queens. """

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        self.k = kwargs.get('k', 4)
        self.alleles = kwargs.get(
            'alleles', [list(range(self.k)) for _ in range(self.k)])
        self._memoize_fitness = {}
        self.prob_selection = kwargs.get('prob_selection', 0.2)
        self.prob_mating = kwargs.get('prob_mating', 0.2)
        self.select_parents = kwargs.get('select_parents', 2)
        self.pair_recobinition = kwargs.get('pair_recobinition', 2)
        self.fragment_inside = True
        self.parents = []
        self.point_crossover = random.randint(1, len(self.alleles)-1)
        self.points_mutation = random.randint(1, len(self.alleles)-1)

    def initialization(self):
        """docstring for initialization."""

        kwargs = {
            'population': self.population,
            'chromosomes': self.chromosomes,
            'individual': self.individual,
            'alleles': self.alleles,
            'method': random.choice
        }

        self.chromosomes = method_initialization(**kwargs)

    def fitness(self, pairs_individuals=None):
        """docstring for fitness"""

        kwargs = {
            'chromosomes': self.chromosomes,
            'k': self.k,
            'memoize_fitness': self._memoize_fitness
        }

        if pairs_individuals:
            kwargs['chromosomes'] = pairs_individuals
            return method_fitness(**kwargs)
        else:
            return method_fitness(**kwargs)

    def selection(self):
        """docstring for selection"""
        self.parents = []
        chromosomes = [
            [chromosome, fitness] for n, (chromosome, fitness) in
            enumerate(self.fitness())
            if n < self.select_parents
        ]

        for _ in range(self.select_parents):
            chromosome = chromosomes.pop(
                chromosomes.index(random.choice(chromosomes))
            )
            self.parents.append(
                self.chromosomes.pop(self.chromosomes.index(chromosome[0]))
            )

        if self.fragment_inside:
            for _ in range(self.select_parents):
                self.chromosomes.remove(random.choice(self.chromosomes))


    def crossover(self):
        """docstring for crossover"""
        pairs_individual = []
        for _ in range(int(len(self.parents)/2)):

            individual_1 = self.parents.pop(
                self.parents.index(random.choice(self.parents))
            )
            individual_2 = self.parents.pop(
                self.parents.index(random.choice(self.parents))
            )

            new_individual_1 = individual_1[:self.point_crossover] \
                + individual_2[self.point_crossover:]
            new_individual_2 = individual_2[self.point_crossover:] \
                + individual_1[:self.point_crossover]

            pairs_individual.append(new_individual_1)
            pairs_individual.append(new_individual_2)

        self.parents = pairs_individual
        self.chromosomes.extend(pairs_individual)

    def mutation(self):
        """docstring for mutation"""
        individuals_mutants = []

        for _ in range(len(self.parents)):
            chromosome = self.parents.pop(
                self.parents.index(
                    random.choice(self.parents)
                )
            )
            random_choice = []
            while len(random_choice) == self.points_mutation:
                gene = random.randint(0, len(self.alleles)-1)
                if not (gene in random_choice):
                    chromosome[gene] = random.choice(self.alleles[gene])
                    random_choice.append(gene)
            individuals_mutants.append(chromosome)

        self.chromosomes.extend(individuals_mutants)

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
    queens = Queens(population=30, k=4, select_parents=4)
    queens.initialization()
    queens.show_chromosomes_fitness

    median = []
    for step in range(100):
        queens.selection()
        queens.crossover()
        queens.mutation()
        # queens.show_chromosomes_fitness

        counter = Counter([fitness[1] for fitness in queens.fitness()])

        add = sum(map(lambda item: item[0] * item[1], counter.items()))
        median.append(add/queens.population)

    pylab.title(
        f'point-crossover: {queens.point_crossover}\n'
        f'points-mutation: {queens.points_mutation}'
    )
    pylab.plot(median)
    pylab.show()
    pylab.close()

if __name__ == "__main__":
    main()

