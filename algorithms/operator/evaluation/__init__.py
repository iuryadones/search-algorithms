

def elitism(self):
    for level in self.parents.keys():
        self.chromosomes.extend(self.parents[level])
        self.parents[level].clear()

    self.chromosomes = [
        chromosome for n, (chromosome, fitness) in
        enumerate(self.fitness)
        if n < self.population
    ]

