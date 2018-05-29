#!/usr/bin/env python3
import pylab as plt
import os
import pathlib
import numpy as np


if __name__ == "__main__":
    path = pathlib.Path('./outputs')
    path_data = path.glob('**/*.dat')

    problems = ['rosenbrock', 'sphere', 'rastrigin', 'zakharov']

    step_bests = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    boxplot_bests = {}
    for problem in problems:
        boxplot_bests[problem] = {}

    for _id, dataset in enumerate(path_data, 1):

        if 'bests' in dataset.absolute().as_posix():

            matrix = []
            for lines in dataset.read_text().split('\n'):
                if lines:
                    temp = []
                    for item in lines.split(','):
                        temp.append(float(item))
                    matrix.append(temp)

            posix = dataset.parent.as_posix().split("/")
            posix.pop(0)
            method = '\n'.join(posix)

            print(f'N Parameters: {_id}', end='\n\n')
            print(method, end='\n\n')

            matrix = np.array(matrix)

            for problem in problems:
                for step in step_bests:
                    if problem in method:
                        if not boxplot_bests[problem].get(step):
                            boxplot_bests[problem][step] = {
                                'method': [],
                                'data': []
                            }
                            boxplot_bests[problem][step]['method'].append(_id)
                            boxplot_bests[problem][step]['data'].append(matrix[:, step])
                        else:
                            boxplot_bests[problem][step]['method'].append(_id)
                            boxplot_bests[problem][step]['data'].append(matrix[:, step])

            matrix_sum = [0 for _ in matrix[0]]

            title = ''
            temp = ''

            posix = dataset.parent.as_posix().split("/")
            for n, p in enumerate(posix):
                if 'outputs' in p:
                    continue

                if any([p == label for label in [
                    "initialization", "fitness",
                    "selection", "evaluation", "crossover"]]):
                    temp += '\n' + p + ':\n'
                    continue

                if '::' in p:
                    temp += '\n'.join(p.split('::')) + ' '
                else:
                    temp += p + ' '

                if n % 2 == 0:
                    title += temp
                    temp = ''

            plt.title(f'Simulations all\n{title}', size=8)

            for m in matrix:
                plt.plot(m)
                for n, item in enumerate(m):
                    matrix_sum[n] += item

            plt.xlabel('Steps')
            plt.ylabel('Fitness bests')
            plt.tight_layout()
            plt.show()
            plt.close()

            matrix_mean = list(map(lambda m: m/len(matrix), matrix_sum))

            plt.title(f'Simulations mean\n{title}', size=8)
            plt.plot(matrix_mean, '.r')
            plt.xlabel('Steps')
            plt.ylabel('Fitness bests')
            plt.tight_layout()
            plt.show()
            plt.close()

        elif 'average' in dataset.absolute().as_posix():
            continue

            matrix = []
            for lines in dataset.read_text().split('\n'):
                if lines:
                    temp = []
                    for item in lines.split(','):
                        temp.append(float(item))
                    matrix.append(temp)

            matrix_sum = [0 for _ in matrix[0]]

            posix = dataset.parent.as_posix().split("/")

            title = ''
            temp = ''

            for n, p in enumerate(posix):
                if 'outputs' in p:
                    continue

                if any([p == label for label in [
                    "initialization", "fitness",
                    "selection", "evaluation", "crossover"]]):
                    temp += '\n' + p + ':\n'
                    continue

                if '::' in p:
                    temp += '\n'.join(p.split('::')) + ' '
                else:
                    temp += p + ' '

                if n%2 == 0:
                    title += temp
                    temp = ''

            plt.title(f'Simulations all\n{title}', size=8)

            for m in matrix:
                plt.plot(m)
                for n, item in enumerate(m):
                    matrix_sum[n] += item

            plt.xlabel('Steps')
            plt.ylabel('Fitness average')
            plt.tight_layout()
            plt.show()
            plt.close()

            matrix_mean = list(map(lambda m: m/len(matrix), matrix_sum))

            plt.title(f'Simulations mean\n{title}', size=8)
            plt.plot(matrix_mean, '.r')
            plt.xlabel('Steps')
            plt.ylabel('Fitness average')
            plt.tight_layout()
            plt.show()
            plt.close()

    for problem in problems:
        for step in step_bests:
            plt.boxplot(
                boxplot_bests[problem][step]['data'],
                labels=boxplot_bests[problem][step]['method'],
                showmeans=True
            )
            plt.title(f'Problem {problem}\nThe bests in step {step}')
            plt.tight_layout()
            plt.show()
            plt.close()
