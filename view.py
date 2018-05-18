#!/usr/bin/env python3
import pylab


class ViewQueens(object):

    def __init__(self, *args, **kwargs):
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
                        clone_m[row][col] = fg_black(' \u2654 ')
                    else:
                        clone_m[row][col] = fg_white(' \u265A ')

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
                        clone_m[row][col] = fg_black(' \u2654 ')
                    else:
                        clone_m[row][col] = fg_white(' \u265A ')

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


class ViewPlots(object):

    def __init__(self, *args, **kwargs):
        pass

    def plot_bests(self, bests):
        pylab.title(
            f'population={self.population}; '
            f'k={self.k}\n'
            f"batch_selection={self.params['selection']['batch']}; "
            f"mating-point_crossover={self.params['crossover']['mating_point']}\n"
            f"n-point_mutation={self.params['mutation']['n_point']}"
        )
        pylab.plot(bests, 'g.')
        pylab.ylim(ymin=0)
        pylab.xlim(xmin=0)
        pylab.show()
        pylab.close()

    def plot_average_bests(self, average, bests):
        pylab.title(
            f'population={self.population}; '
            f'k={self.k}\n'
            f"batch_selection={self.params['selection']['batch']}; "
            f"mating-point_crossover={self.params['crossover']['mating_point']}\n"
            f"n-point_mutation={self.params['mutation']['n_point']}"
        )
        pylab.plot(average, 'b.-')

        pylab.plot(bests, 'g.')
        pylab.ylim(ymin=0)
        pylab.xlim(xmin=0)
        pylab.show()
        pylab.close()

if __name__ == "__main__":
    pass
