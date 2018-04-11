
def n_queens(self):

    if self.params.get('fitness', {}).get('chromosomes'):
        chromosomes = [
            chromosome
            for chromosome in self.params['fitness'].get('chromosomes')
        ]
        self.params['fitness']['chromosomes'].clear()

    else:
        chromosomes = self.chromosomes

    chromosomes_fitness = []
    for chromosome in chromosomes:
        chromosome_str = ''.join([f'{gene}' for gene in chromosome])
        chromosome_resp = self._memoize_fitness.get(chromosome_str)

        if not chromosome_resp:
            resp_side = [(chromosome.count(gene) - 1) for gene in chromosome]
            resp_diag = [
                [
                    False,
                    (row, col) != (chromosome[i], i)
                ][abs(row-chromosome[i]) == abs(col - i)]
                for i in range(self.k)
                for col, row in enumerate(chromosome)
            ]

            chromosome_resp = sum(resp_side) + resp_diag.count(True)
            self._counter_fitness += 1
            self._memoize_fitness[chromosome_str] = chromosome_resp
            chromosomes_fitness.append([chromosome, chromosome_resp])

        else:
            chromosomes_fitness.append([chromosome, chromosome_resp])

    return sorted(chromosomes_fitness,
                  key=lambda chromo_fitness: chromo_fitness[1])

