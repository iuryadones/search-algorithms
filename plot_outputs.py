#!/usr/bin/env python3
import pylab as plt
import os


if __name__ == "__main__":

    pathout = os.getcwd() + '/outputs/'

    list_files = os.listdir(pathout)


    for dataset in list_files:
        path = pathout + dataset

        print(dataset)

        if 'data-bests' in dataset:

            with open(path) as arq:

                matrix = [
                    [int(item) for item in line.strip().split(',') if item]
                    for line in arq.readlines()
                ]

            matrix_sum = [0 for _ in range(100)]

            for m in matrix:
                for n, item in enumerate(m):
                    matrix_sum[n] += item

            matrix_mean = list(map(lambda m: m/len(matrix), matrix_sum))

            plt.title('Simulations')
            plt.plot(matrix_mean, '.r')
            plt.xlabel('Steps')
            plt.ylabel('Fitness bests')
            plt.show()
            plt.close()

        elif 'data-average' in dataset:

            with open(path) as arq:

                matrix = [
                    [float(item) for item in line.strip().split(',') if item]
                    for line in arq.readlines()
                ]

            matrix_sum = [0 for _ in range(100)]

            for m in matrix:
                for n, item in enumerate(m):
                    matrix_sum[n] += item

            matrix_mean = list(map(lambda m: m/len(matrix), matrix_sum))


            plt.title('Simulations')
            plt.xlabel('Steps')
            plt.ylabel('Fitness mean')
            plt.plot(matrix_mean, '.r')

            plt.show()
            plt.close()
