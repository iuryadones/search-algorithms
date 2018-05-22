
def choice_yourself(self):

    if issubclass(self.individual, int):
        for _ in range(self.population):
            chromosome = []
            for allele in self.alleles:
                choice = self.params['initialization']['choice'](allele)
                chromosome.append(choice)

            self.chromosomes.append(chromosome)

    elif issubclass(self.individual, list):
        for _ in range(self.population):
            chromosome = []
            for allele in self.alleles:
                choice = self.params['initialization']['choice'](allele)
                chromosome.append(choice)

            self.chromosomes.append(chromosome)

    elif issubclass(self.individual, float):
        for _ in range(self.population):
            chromosome = []
            for _min, _max in self.alleles:
                choice = self.params['initialization']['choice'](_min, _max)
                chromosome.append(choice)

            self.chromosomes.append(chromosome)
    else:
        raise NotImplemented

