from algorithms.features.ga import Base
from collections import Counter
import random
import pylab


# TODO: Organizar no modulo algorithms
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

# TODO: Organizar no modulo algorithms
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
        self._memoize_fitness = {}
        self.k = kwargs.get('k', 4)
        self.alleles = kwargs.get(
            'alleles', [list(range(self.k)) for _ in range(self.k)]
        )
        self.mating_point_crossover = random.randint(1, len(self.alleles)-1)
        self.npoint_mutation = random.randint(1, len(self.alleles)-1)
        self.parents = {'crossover': [], 'mutation': [], 'individual': []}
        self.select_parents = kwargs.get('select_parents', 2)

    def initialization(self, method=None):
        """docstring for initialization."""

        kwargs = {
            'population': self.population,
            'chromosomes': self.chromosomes,
            'individual': self.individual,
            'alleles': self.alleles,
            'method': method
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

    @property
    def selection(self):
        """docstring for selection"""
        self.parents['individual'] = []

        chromosomes = [
            [chromosome, fitness] for n, (chromosome, fitness) in
            enumerate(self.fitness())
            if n < self.select_parents
        ]

        for _ in range(self.select_parents):
            chromosome = chromosomes.pop(
                chromosomes.index(random.choice(chromosomes))
            )

            self.parents['individual'].append(
                self.chromosomes.pop(self.chromosomes.index(chromosome[0]))
            )

    @property
    def crossover(self):
        """docstring for crossover"""
        self.parents['crossover'] = []

        len_pairs = len(self.parents['individual']) // 2

        temp_parents = []
        for _ in range(len_pairs):
            individual_1 = self.parents['individual'].pop(
                self.parents['individual'].index(
                    random.choice(self.parents['individual'])
                )
            )
            individual_2 = self.parents['individual'].pop(
                self.parents['individual'].index(random.choice(self.parents['individual']))
            )

            new_individual_1 = individual_1[:self.mating_point_crossover] \
                + individual_2[self.mating_point_crossover:]
            new_individual_2 = individual_2[self.mating_point_crossover:] \
                + individual_1[:self.mating_point_crossover]

            self.parents['crossover'].extend([new_individual_1, new_individual_2])
            temp_parents.extend([individual_1, individual_2])

        self.parents['individual'].extend(temp_parents)

    @property
    def evaluation(self):
        for method in self.parents.keys():
            print(method)
            print(self.parents[method])
            self.chromosomes.extend(self.parents[method])

        self.chromosomes = [
            chromosome for n, (chromosome, fitness) in
            enumerate(self.fitness())
            if n < self.population
        ]

    @property
    def mutation(self):
        """docstring for mutation"""
        self.parents['mutation'] = []

        if self.parents['crossover']:
            for _ in range(self.select_parents // 2):
                chromosome = self.parents['crossover'].pop(
                    self.parents['crossover'].index(
                        random.choice(self.parents['crossover'])
                    )
                )

                random_choice = []

                while (len(random_choice) < self.npoint_mutation):
                    gene = random.randint(0, len(self.alleles)-1)
                    if not (gene in random_choice):
                        chromosome[gene] = random.choice(self.alleles[gene])
                        random_choice.append(gene)

                self.parents['mutation'].append(chromosome)

        elif self.parents['individual']:
            for _ in range(self.select_parents):
                chromosome = self.parents['individual'].pop(
                    self.parents['individual'].index(
                        random.choice(self.parents['individual'])
                    )
                )
                random_choice = []
                while (len(random_choice) < self.npoint_mutation):
                    gene = random.randint(0, len(self.alleles)-1)
                    if not (gene in random_choice):
                        chromosome[gene] = random.choice(self.alleles[gene])
                        random_choice.append(gene)
                self.parents['mutation'].append(chromosome)


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
    queens = Queens(
        population=50,
        k=8,
        select_parents=16,
    )

    queens.initialization(method=random.choice)
    queens.show_chromosomes_fitness

    MAX_CHECK_FITNESS = 1000
    MAX_INTERATIONS = 100

    median = []
    for step in range(MAX_INTERATIONS):
        queens.selection
        queens.crossover
        queens.mutation
        queens.evaluation

        counter = Counter([fitness[1] for fitness in queens.fitness()])
        add = sum(map(lambda item: item[0] * item[1], counter.items()))
        median.append(add / queens.population)

        individuals = sorted(
            queens._memoize_fitness.items(), key=lambda x: x[1]
        )

        if len(individuals) >= MAX_CHECK_FITNESS:
            break

    # TODO: Criar um modulo para functions utils
    pylab.title(
        f'population={queens.population}; '
        f'k={queens.k}\n'
        f'select_parents={queens.select_parents}; '
        f'mating-point_crossover={queens.mating_point_crossover}\n'
        f'n-point_mutation={queens.npoint_mutation}'
    )
    pylab.plot(median, '.-')
    pylab.ylim(ymin=0)
    pylab.xlim(xmin=0)
    pylab.show()
    pylab.close()

    queens.show_chromosomes_fitness

    # TODO: criar show_best modulo algorithms
    print('\nShow 5 best individuals\n')
    for n, individual in enumerate(individuals):
        if n < 5:
            print(individual)
        else:
            break
    print(f'\nChecked Individuals: {len(individuals)}')


if __name__ == "__main__":
    main()
