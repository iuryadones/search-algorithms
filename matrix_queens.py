# -*- coding: utf-8 -*-

## gleidson.ascampos@gmail.com
## Mgranja9@gmail.com

import random


class Rainhas(object):
    """ Atividade que envolve as 8 rainhas do xadrez """

    def __init__(
        self,
        tamanho_populacao=100,
        numero_decendentes=2,
        solucoes_candidatas=[],
        avaliacoes=0,
        max_avaliacoes=10000,
        selecao_pais={"melhores": 2, "qtd_aleatorio": 5},
    ):
        super(Rainhas, self).__init__()

        self.tamanho_populacao = tamanho_populacao
        self.avaliacoes = avaliacoes
        self.max_avaliacoes = max_avaliacoes
        self.selecao_pais = selecao_pais
        self.numero_decendentes = numero_decendentes
        self.solucoes_candidatas = solucoes_candidatas

    def inicializar_matriz(self, linhas=8, colunas=8):
        # Inicializacao das solucoes candidatas
        for tam_pop in range(self.tamanho_populacao):
            # Inicializar a Matriz(tabuleiro) com todas as posicoes igual a zero
            solucao_candidata = []
            for lin in range(linhas):
                linha_temp = []
                for col in range(colunas):
                    linha_temp.append(0)
                solucao_candidata.append(linha_temp)
            # Sortear a posicao da rainha no tabuleiro
            rainhas_sorteadas = []
            for rainha in range(linhas):
                while True:
                    x = random.randint(0, (linhas - 1))
                    y = random.randint(0, (colunas - 1))
                    if (x, y) not in rainhas_sorteadas:
                        solucao_candidata[x][y] = 1
                        rainhas_sorteadas.append((x, y))
                        break
            # Calcular a fitness(aptidao) da solucao candidata
            fitness = self.avaliar_matriz(solucao_candidata)
            # Adicionar a solucao candidata no conjunto das solucoes candidatas
            self.solucoes_candidatas.append([fitness, solucao_candidata])

    def exibir_solucoes(self, solucoes_candidatas=None):
        if solucoes_candidatas == None:
            solucoes_candidatas = self.solucoes_candidatas

        for i in range(len(solucoes_candidatas)):
            print("Fitness: {}".format(solucoes_candidatas[i][0]))
            if solucoes_candidatas[i][0] == 0:
                print("Solucao:")
                for tabela in solucoes_candidatas[i][1]:
                    print(tabela)

    def exibir(self, solucao):
        for linha in solucao:
            print(linha)

    def avaliar_matriz(self, solucao):
        # Calcular o Fitness da solucao candidata (melhor a zero)
        self.avaliacoes += 1
        fitness = 0
        linhas = len(solucao)
        for x in range(linhas):
            colunas = len(solucao[x])
            for y in range(colunas):
                if solucao[x][y] == 1:
                    pos = [(x, y)]
                    for lin in range(linhas):
                        for col in range(colunas):
                            if ((lin, col) not in pos) and (
                                solucao[lin][col] == 1
                            ):
                                if lin == x:
                                    fitness += 1
                                elif col == y:
                                    fitness += 1
                                if abs((lin - x)) == abs((col - y)):
                                    fitness += 1
        return fitness

    def selecionar_melhor_solucao(self):
        pais = self.solucoes_candidatas
        pais_selecionados = []
        for pai_fitness in pais:
            if len(pais_selecionados) < 1:
                pais_selecionados.append(pai_fitness)
            for i in range(len(pais_selecionados)):
                if pai_fitness in pais_selecionados:
                    pass
                elif pai_fitness[0] < pais_selecionados[i][0]:
                    pais_selecionados.remove(pais_selecionados[i])
                    pais_selecionados.append(pai_fitness)
        return pais_selecionados

    def selecionar_pais(self):
        # Selecinar os Indices dos pais de forma aleatoria
        indices_sorteados = []
        for n in range(self.selecao_pais["qtd_aleatorio"]):
            indice = random.randint(0, (len(self.solucoes_candidatas) - 1))
            while indice in indices_sorteados:
                indice = random.randint(0, (len(self.solucoes_candidatas) - 1))
            indices_sorteados.append(indice)

        # Selecinar os pais com os indices ja sorteados aleatoriamente
        pais = []
        for pai in indices_sorteados:
            pais.append(self.solucoes_candidatas[pai])

        # Escolher os melhores pais para o cruzamento
        pais_selecionados = []
        for pai_fitness in pais:
            if len(pais_selecionados) < self.selecao_pais["melhores"]:
                pais_selecionados.append(pai_fitness)
            for i in range(len(pais_selecionados)):
                if pai_fitness in pais_selecionados:
                    pass
                elif pai_fitness[0] < pais_selecionados[i][0]:
                    pais_selecionados.remove(pais_selecionados[i])
                    pais_selecionados.append(pai_fitness)
        return pais_selecionados

    def recombinar_pais(self, melhores_pais):
        nova_solucao_candidata = []
        col = len(melhores_pais[0][1][0])
        linhas = len(melhores_pais[0][1])
        limit = linhas - 2
        lin_sorteados = []
        while len(lin_sorteados) < limit:
            lin = random.randint(1, limit)
            if lin not in lin_sorteados:
                matriz = (
                    melhores_pais[0][1][:lin:] + melhores_pais[1][1][lin:col:]
                )
                lin_sorteados.append(lin)
            quantidade_rainhas = 0
            for linha in matriz:
                for coluna in linha:
                    quantidade_rainhas += coluna
            if quantidade_rainhas == col:
                nova_solucao_candidata.append(
                    [self.avaliar_matriz(matriz), matriz]
                )
                break
        else:
            escolha = random.choice([0, 1])
            nova_solucao_candidata.append(melhores_pais[escolha])
        return nova_solucao_candidata

    def mutar_solucao(self, candidata, probabilidade):
        solucao_mutante = []
        matriz_fix = candidata[0][1][::]
        matriz_mov = candidata[0][1][::]
        tam = len(matriz_fix)
        for i in range(tam):
            for j in range(tam):
                if matriz_fix[i][j] == 1:
                    prob = random.random()
                    if prob <= probabilidade:
                        while True:
                            x = random.choice([(i - 1), (i + 1)])
                            y = random.choice([(j - 1), (j + 1)])
                            if x not in [-1, tam] and y not in [-1, tam]:
                                if (
                                    matriz_fix[x][y] != 0
                                    and matriz_mov[x][y] != 1
                                ):
                                    matriz_mov[x][y] = 1
                                    matriz_mov[i][j] = 0
                                    break
                                else:
                                    break

        solucao_mutante.append([self.avaliar_matriz(matriz_mov), matriz_mov])
        # self.exibir(matriz_mov)
        return solucao_mutante

    def selecionar_aptos(self):
        # Escolher os melhores pais para o cruzamento
        pais_selecionados = []
        for pai_fitness in self.solucoes_candidatas:
            if len(pais_selecionados) < self.tamanho_populacao - 1:
                pais_selecionados.append(pai_fitness)
            for i in range(len(pais_selecionados)):
                if pai_fitness in pais_selecionados:
                    pass
                elif pai_fitness[0] < pais_selecionados[i][0]:
                    pais_selecionados.remove(pais_selecionados[i])
                    pais_selecionados.append(pai_fitness)
        self.solucoes_candidatas = pais_selecionados[::]

    def inserir_descedentes_aptos(self, filhos):
        self.solucoes_candidatas += filhos

    def exibir_total_solucoes(self):
        print("Solucoes Candidatas: {}".format(len(self.solucoes_candidatas)))

    def exibir_media_solucoes(self, solucoes_candidatas=None):
        if solucoes_candidatas == None:
            solucoes_candidatas = self.solucoes_candidatas
        media = 0.0
        total = 0.0
        quantidade = len(solucoes_candidatas)
        for i in range(quantidade):
            total += solucoes_candidatas[i][0]
        media = total / quantidade
        print("Media: {:.2f}".format(media))
        return media


def main(rainhas, N, P, Rainhas_qtd):

    rainhas.inicializar_matriz(linhas=Rainhas_qtd, colunas=Rainhas_qtd)
    # rainhas.exibir_solucoes()
    probabilidade = P
    for x in range(N):
        solucao_filha = rainhas.recombinar_pais(rainhas.selecionar_pais())
        solucao_mutante = rainhas.mutar_solucao(solucao_filha, probabilidade)
        rainhas.selecionar_aptos()
        rainhas.inserir_descedentes_aptos(solucao_mutante)
        # rainhas.exibir_solucoes()
        # melhor_solucao = rainhas.selecionar_melhor_solucao()[0][0]
        # medias.append(rainhas.exibir_media_solucoes())
        # rainhas.exibir_total_solucoes()
        for melhor_solucao in rainhas.solucoes_candidatas:
            if melhor_solucao[0] == 0:
                rainhas.exibir(melhor_solucao[1])
                return x
                break
        if rainhas.avaliacoes == rainhas.max_avaliacoes:
            print("Max Avaliacoes")
            break
    return 0


if __name__ == "__main__":

    # import matplotlib.pyplot as plt
    vec = []
    for i in range(30):
        rainhas = Rainhas()
        res = main(rainhas, 10001, 0.3, 4)
        vec.append(res)
        print("Res {}: {}".format(i, res))
    print("Vec:\n{}".format(vec))
    print("Media: {}".format(sum(vec) / len(vec)))
    # plt.title('Probabilidade da mutação = {}'.format(probabilidade))
    # plt.xlabel('Passos')
    # plt.ylabel('Média do Fitness')
    # plt.plot(medias, '-b')
    # plt.show()
