def elitism(self):
    """
    Elitism -> choice n_best individuals:

    operator={
        'selection': elitism
    }

    params={
        'selection': {
            'n_best': <class 'int'>
        }
    }
    """

    n_best = self.params["selection"]["n_best"]

    n_best_chromosomes = [
        [chromosome, value_fitness]
        for n, (chromosome, value_fitness) in enumerate(self.fitness)
        if n < n_best
    ]

    for best_chromosome, fitness in n_best_chromosomes:
        self.parents["individual"].append(
            self.chromosomes.pop(self.chromosomes.index(best_chromosome))
        )


def choice_pairs_in_batch(self):
    batch = self.params["selection"]["batch"]
    choice_individual = self.params["selection"]["choice_individual"]
    len_chunks = len(self.chromosomes) // batch

    chuncks = [
        [
            self.chromosomes.pop(
                self.chromosomes.index(choice_individual(self.chromosomes))
            )
            for _ in range(batch)
        ]
        for _ in range(len_chunks)
    ]

    for chunck in chuncks:

        if self.params.get("fitness", {}).get("chromosomes"):
            self.params["fitness"].update(
                {"chromosomes": [c[::] for c in chunck]}
            )
        else:
            self.params["fitness"] = {"chromosomes": [c[::] for c in chunck]}

        self.parents["individual"].extend(
            [
                chunck.pop(chunck.index(chromosome))
                for n, (chromosome, fitness) in enumerate(self.fitness)
                if n < 2
            ]
        )

        self.chromosomes.extend(chunck)
