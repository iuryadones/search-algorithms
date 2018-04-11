

def n_gene(self):
    n_point = self.params['mutation']['n_point']
    choice_individual = self.params['mutation']['choice_individual']
    choice_gene = self.params['mutation']['choice_gene']
    mutation_gene = self.params['mutation']['mutation_gene']

    if self.parents['crossover']:
        sample = 'crossover'
        n_choice = len(self.parents[sample]) // 2

    elif self.parents['individual']:
        sample = 'individual'
        n_choice = len(self.parents[sample])

    for _ in range(n_choice):
        chromosome = self.parents[sample].pop(
            self.parents[sample].index(
                choice_individual(self.parents[sample])
            )
        )

        random_choice = []
        while (len(random_choice) < n_point):
            gene = choice_gene(0, len(self.alleles)-1)
            if not (gene in random_choice):
                chromosome[gene] = mutation_gene(self, chromosome, gene)
                random_choice.append(gene)

        self.parents['mutation'].append(chromosome)

def n_swap(self):
    n_point = self.params['mutation']['n_point']
    choice_individual = self.params['mutation']['choice_individual']
    choice_gene = self.params['mutation']['choice_gene']

    if self.parents['crossover']:
        sample = 'crossover'
        n_choice = len(self.parents[sample]) // 2

    elif self.parents['individual']:
        sample = 'individual'
        n_choice = len(self.parents[sample])

    for _ in range(n_choice):
        chromosome = self.parents[sample].pop(
            self.parents[sample].index(
                choice_individual(self.parents[sample])
            )
        )

        random_choice = []
        while ((len(random_choice) // 2) < n_point):
            genes = [choice_gene(0, len(self.alleles)-1) for _ in range(2)]
            if all([not (gene in random_choice) for gene in genes]):
                temp = chromosome[genes[0]]
                chromosome[genes[0]] = chromosome[genes[1]]
                chromosome[genes[1]] = temp
                random_choice.extend(genes)

        self.parents['mutation'].append(chromosome)

