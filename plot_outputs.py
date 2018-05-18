#!/usr/bin/env python3
import pylab as plt
import os
import pathlib


if __name__ == "__main__":
    path = pathlib.Path('./outputs')
    path_data = path.glob('**/*.dat')

    for dataset in path_data:

        if 'bests' in dataset.absolute().as_posix():

            matrix = [
                [int(item) for item in lines if item.isdigit()]
                for lines in dataset.read_text().split('\n')
            ]

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

        # elif 'average' in dataset.absolute().as_posix():

        #     matrix = [
        #         [int(item) for item in lines if item.isdigit()]
        #         for lines in dataset.read_text().split('\n')
        #     ]

        #     print(matrix)

        #     matrix_sum = [0 for _ in matrix[0]]
        #     print(matrix_sum)

        #     posix = dataset.parent.as_posix().split("/")

        #     title = ''
        #     temp = ''

        #     for n, p in enumerate(posix):
        #         if 'outputs' in p:
        #             continue

        #         if any([p == label for label in [
        #             "initialization", "fitness",
        #             "selection", "evaluation", "crossover"]]):
        #             temp += '\n' + p + ':\n'
        #             continue

        #         if '::' in p:
        #             temp += '\n'.join(p.split('::')) + ' '
        #         else:
        #             temp += p + ' '

        #         if n%2 == 0:
        #             title += temp
        #             temp = ''

        #     plt.title(f'Simulations all\n{title}', size=8)

        #     for m in matrix:
        #         plt.plot(m)
        #         for n, item in enumerate(m):
        #             matrix_sum[n] += item

        #     plt.xlabel('Steps')
        #     plt.ylabel('Fitness average')
        #     plt.tight_layout()
        #     plt.show()
        #     plt.close()


        #     matrix_mean = list(map(lambda m: m/len(matrix), matrix_sum))

        #     plt.title(f'Simulations mean\n{title}', size=8)
        #     plt.plot(matrix_mean, '.r')
        #     plt.xlabel('Steps')
        #     plt.ylabel('Fitness average')
        #     plt.tight_layout()
        #     plt.show()
        #     plt.close()
