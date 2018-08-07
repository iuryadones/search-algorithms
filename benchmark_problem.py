#!/usr/bin/env python3
from algorithms.features.ga import Base
from algorithms.operator import crossover
from algorithms.operator import evaluation
from algorithms.operator import fitness
from algorithms.operator import initialization
from algorithms.operator import mutation
from algorithms.operator import selection
from algorithms.views import ViewQueens
from collections import Counter
from view import ViewPlots

import random
import pylab as plt
import math
import datetime
import os
import pathlib
import pickle


class Queens(Base, ViewQueens, ViewPlots):

    """Docstring for K-Queens. """

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        ViewQueens.__init__(self, *args, **kwargs)
        ViewPlots.__init__(self, *args, **kwargs)


def run(
    obj,
    MAX_ITERATIONS=100,
    MAX_CHECK_FITNESS=10000,
    name_file="stacked",
    name_paths=".",
):

    # obj.show_chromosomes_fitness

    average = []
    average.append(obj.average)

    bests = []
    bests.extend(map(lambda b: b[1], obj.best()))

    for step in range(1, MAX_ITERATIONS):
        obj.selection
        obj.crossover
        obj.mutation
        obj.evaluation

        bests.extend(map(lambda b: b[1], obj.best()))
        average.append(obj.average)

        # if (obj._counter_fitness >= MAX_CHECK_FITNESS):
        #     break

    script_dir = os.path.dirname(os.path.abspath(__file__))

    target_dir = os.path.join(script_dir, "outputs", os.path.join(*name_paths))

    pathlib.Path(os.path.join(target_dir, "bests")).mkdir(
        parents=True, exist_ok=True
    )
    pathlib.Path(os.path.join(target_dir, "average")).mkdir(
        parents=True, exist_ok=True
    )

    name_file = name_file + ".dat"

    with open(os.path.join(target_dir, "bests", name_file), "a") as arq:
        arq.write(",".join(map(str, bests)) + "\n")

    with open(os.path.join(target_dir, "average", name_file), "a") as arq:
        arq.write(",".join(map(str, average)) + "\n")

    # obj.show_chromosomes_fitness
    obj.show_best_five_individuals


def sphere(chromosome):
    return sum((gene ** 2) for gene in chromosome)


def zakharov(chromosome):
    s1 = sum((gene ** 2) for gene in chromosome)
    s2 = sum((0.5 * i * gene) for i, gene in enumerate(chromosome, 1)) ** 2
    s3 = sum((0.5 * i * gene) for i, gene in enumerate(chromosome, 1)) ** 4
    return sum([s1, s2, s3])


def rastrigin(chromosome):
    s1 = 10 * len(chromosome)
    s2 = sum(
        ((gene ** 2) - (10 * math.cos(2 * math.pi * gene)))
        for gene in chromosome
    )
    return sum([s1, s2])


def rosenbrock(chromosome):
    if len(chromosome) == 1:
        return (100 * (((-1) * chromosome[0] ** 2) ** 2)) + (
            (chromosome[0] - 1) ** 2
        )
    else:
        return sum(
            (100 * ((chromosome[i + 1] - (chromosome[i] ** 2)) ** 2))
            + ((chromosome[i] - 1) ** 2)
            for i in range(len(chromosome) - 1)
        )


if __name__ == "__main__":
    K = 3

    parameters = dict(
        alleles=[[-30, 30] for _ in range(K)],
        k=K,
        individual=float,
        population=100,
        operator={
            "selection": selection.choice_pairs_in_batch,
            "crossover": crossover.one_point_mating,
            "mutation": mutation.n_gene,
            "fitness": fitness.benchmark,
            "initialization": initialization.choice_yourself,
            "evaluation": evaluation.elitism,
        },
        params={
            "initialization": {"choice": random.triangular},
            "fitness": {"problem": zakharov, "otimization": "min"},
            "selection": {"batch": 20, "choice_individual": random.choice},
            "mutation": {
                "n_point": 1,
                "choice_gene": random.randint,
                "choice_individual": random.choice,
                "mutation_gene": random.choice,
            },
            "crossover": {"mating_point": 1},
        },
    )

    # parameters = dict(
    #     alleles=[[-30, 30] for _ in range(K)],
    #     k=K,
    #     individual=float,
    #     population=100,
    #     operator={
    #         'selection': selection.choice_pairs_in_batch,
    #         'crossover': crossover.one_point_mating,
    #         'mutation': mutation.n_swap,
    #         'fitness': fitness.benchmark,
    #         'initialization': initialization.choice_yourself,
    #         'evaluation': evaluation.elitism
    #     },
    #     params={
    #         'initialization': {
    #             'choice': random.triangular
    #         },
    #         'fitness': {
    #             'problem': rosenbrock,
    #             'otimization': 'min'
    #         },
    #         'selection': {
    #             'batch': 5,
    #             'choice_individual': random.choice,
    #         },
    #         'mutation': {
    #             'n_point': 2,
    #             'choice_gene': random.randint,
    #             'choice_individual': random.choice,
    #         },
    #         'crossover': {
    #             'mating_point': 1,
    #         },
    #     }
    # )

    queens = Queens(**parameters)

    name_chromossomes = f"sphere_chromosomes_0_k_{K}.pkl"

    if not os.path.exists(name_chromossomes):
        queens.initialization
        pickle.dump(queens.chromosomes[::], open(name_chromossomes, "wb"))
        chromosomes_base = pickle.load(open(name_chromossomes, "rb"))
    else:
        chromosomes_base = pickle.load(open(name_chromossomes, "rb"))

    MAX_ITERATIONS = 100
    MAX_CHECK_FITNESS = 10000
    MAX_SIMULATIONS = 30

    DATETIME = datetime.datetime.utcnow().isoformat()

    rtn = lambda items: "::".join(
        [f"{k}:{v if not callable(v) else v.__name__}" for k, v in items]
    )

    name_paths = [
        "k",
        f"{queens.k}",
        "population",
        f"{queens.population}",
        "max_iterations",
        f"{MAX_ITERATIONS}",
        "max_check_fitness",
        f"{MAX_CHECK_FITNESS}",
        "max_simulations",
        f"{MAX_SIMULATIONS}",
        "initialization",
        f'{queens.operator.get("initialization").__name__}',
        f'{rtn(queens.params.get("initialization", {}).items())}',
        "fitness",
        f'{queens.operator.get("fitness").__name__}',
        f'{rtn(queens.params.get("fitness", {}).items())}',
        "selection",
        f'{queens.operator.get("selection").__name__}',
        f'{rtn(queens.params.get("selection", {}).items())}',
        "crossover",
        f'{queens.operator.get("crossover").__name__}',
        f'{rtn(queens.params.get("crossover", {}).items())}',
        "mutation",
        f'{queens.operator.get("mutation").__name__}',
        f'{rtn(queens.params.get("mutation", {}).items())}',
        "evaluation",
        f'{queens.operator.get("evaluation").__name__}',
        f'{rtn(queens.params.get("evaluation", {}).items())}',
    ]

    name_file = f"date_run_{DATETIME}"

    memoization = {}

    for _ in range(MAX_SIMULATIONS):

        memoization.update(queens._memoize_fitness)

        queens._memoize_fitness.update(memoization)

        print(len(queens._memoize_fitness.keys()))

        queens = Queens(**parameters)
        chromosomes_base = pickle.load(open(name_chromossomes, "rb"))
        queens.chromosomes = chromosomes_base[::]

        run(queens, MAX_ITERATIONS, MAX_CHECK_FITNESS, name_file, name_paths)
