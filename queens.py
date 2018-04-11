from algorithms.features.ga import Base
from algorithms.operator import initialization
from algorithms.operator import fitness
from algorithms.operator import selection
from algorithms.operator import crossover
from algorithms.operator import evaluation
from algorithms.operator import mutation
from collections import Counter
import random
import pylab


class Queens(Base):

    """Docstring for K-Queens. """

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)

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

            for chromosome, chromo_fitness in self.fitness:
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

    @property
    def show_best_five_individuals(self):
        individuals = sorted(
            self._memoize_fitness.items(), key=lambda x: x[1]
        )

        print('\nShow 5 best individuals\n')

        for n, individual in enumerate(individuals):
            if n < 5:
                print(individual)

            else:
                break

        print(f'\nChecked Individuals: {len(individuals)}')

    def plot_average_bests(self, median, bests):
        pylab.title(
            f'population={self.population}; '
            f'k={self.k}\n'
            f"batch_selection={self.params['selection']['batch']}; "
            f"mating-point_crossover={self.params['crossover']['mating_point']}\n"
            f"n-point_mutation={self.params['mutation']['n_point']}"
        )
        pylab.plot(median, 'b.-')
        pylab.plot(bests, 'g.')
        pylab.ylim(ymin=0)
        pylab.xlim(xmin=0)
        pylab.show()
        pylab.close()


def run(obj, MAX_INTERATIONS=100, MAX_CHECK_FITNESS=10000):

    obj.initialization
    obj.show_chromosomes_fitness

    average = []
    average.append(obj.average)
    bests = []
    bests.extend(map(lambda b: b[1], obj.best()))

    if not (bests[0] == 0):

        for step in range(1, MAX_INTERATIONS):
            obj.selection
            obj.crossover
            obj.mutation
            obj.evaluation

            bests.extend(map(lambda b: b[1], obj.best()))
            average.append(obj.average)

            if (obj._counter_fitness >= MAX_CHECK_FITNESS) \
                or (bests[step] == 0):
                break

    obj.plot_average_bests(average, bests)
    obj.show_chromosomes_fitness
    obj.show_best_five_individuals


if __name__ == "__main__":
    K = 8

    queens = Queens(
        alleles=[list(range(K)) for _ in range(K)],
        k=K,
        population=100,
        operator={
            'selection': selection.choice_pairs_in_batch,
            'crossover': crossover.one_point_mating,
            'mutation': mutation.n_swap,
            'fitness': fitness.n_queens,
            'initialization': initialization.choice_yourself,
            'evaluation': evaluation.elitism
        },
        params={
            'initialization': {
                'choice': random.choice
            },
            'selection': {
                'batch': 5,
                'choice_individual': random.choice,
            },
            'mutation': {
                'n_point': 1,
                'choice_gene': random.randint,
                'choice_individual': random.choice,
            },
            'crossover': {
                'mating_point': random.randint(1, 7),
            },
        }
    )

    run(queens, MAX_INTERATIONS=100, MAX_CHECK_FITNESS=10000)
