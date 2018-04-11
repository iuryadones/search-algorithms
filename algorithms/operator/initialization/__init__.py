
def choice_yourself(self):

    if issubclass(self.individual, list):
        for _ in range(self.population):
            chromosome = []
            for allele in self.alleles:
                choice = self.params['initialization']['choice'](allele)
                chromosome.append(choice)

            self.chromosomes.append(chromosome)
    else:
        raise NotImplemented

