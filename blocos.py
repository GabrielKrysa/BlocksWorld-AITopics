# -*- coding: utf-8 -*-
# 26 de Abril Data de Entrega
# Problema da Busca em Largura: ex: 17 blocos estouro de Pilha
# Precisamos de um Algoritmo de Propósito Geral

import sys
import copy
import time

def remove_ander(linha):
    ln = []
    s = linha.split('_')
    for l in s:
        l = l.replace('\n',"")
        ln.append(l)
    return ln

def remove_ponto(linha):
    ln = []
    s = linha.split(';')
    for l in s:
        ln.append(remove_ander(l))
    return ln

def substr(a, b):
    i = 0
    while i < len(a):
        if a[i] == b[0]:
            if a[i:i+len(b)] == b:
                return True
        i += 1
    return False

class Fila:
    
    def __init__(self, d):
        self.d = d
    def deq(self):
        a = copy.deepcopy(self.d[0])
        self.d = self.d[1:]
        return a
    def queue(self, a):
        self.d.append(a)
    def empty(self):
        return len(self.d) == 0


class Estado:
    
    def __init__(self, data, ident=1):
        self.data = data
        self.ident = ident

    def subconjunto(self, data):
        if set(data) <= set(self.data):
            return True
        else:
            return False

    def __str__(self):
        return str(self.data)

class Acao:

    def __init__(self, acao, pre, efeito):
        self.acao = acao
        self.pre = pre
        self.efeito = efeito

    def __str__(self):
        return "Ação: " + str(self.acao) + "\nPre-Condição: " + str(self.pre) + "\nEfeito: " + str(self.efeito)

class Arvore:

    def __init__(self):
        self.raiz = 1
        self.no = {1:[]} # 1:[2:[1,3, 2,3,4,,5,6]]

    def adicionar(self, pai, filho, acao):
        self.no[pai].append(filho)
        self.no[filho] = [acao,pai]

    def caminho(self, no):
        nos = []
        i = no
        j = 0
        '''
        '''
        while i != 1:
            j = self.no[i][0]
            i = self.no[i][1]
            nos.append(j)
        nos.reverse()
        return nos

def main(arg):
    #CPU
    time_init = time.time()

    arquivo = open(arg, 'r')
    linhas = arquivo.readlines()

    # Pegando a linha referente ao Estado Inicial
    e_inicial = linhas[-2]

    # Pegando a linha referente ao Objetivo
    o_final = linhas[-1]
    #Quebrando linhas
    estado_inicial = e_inicial.split(';')
    objetivo_final = o_final.split(';')
    # Lista de preposições do estado inicial
    prepo_iniciais = []
    # Lista de preposições do estado final
    prepo_finais =  []

    for p in estado_inicial:
        p = p.replace('\n',"")
        prepo_iniciais.append(p.split('_'))

    for o in objetivo_final:
        o = o.replace('\n',"")
        prepo_finais.append(o.split('_'))

    iniciar_estadoInicial = Estado(prepo_iniciais)
    iniciar_estadoFinal = Estado(prepo_finais)
    lista_acoes = []
    i = 0;
    while linhas[i] != '\n':
        lista_acoes.append(Acao(remove_ponto(linhas[i]), remove_ponto(linhas[i+1]), remove_ponto(linhas[i+2])))
        i += 3

    print lista_acoes[0]

    #CPU time cont
    print "Tempo de execução: " + str(time.time() - time_init)

    # Parte 01 - Parte Inicial terminada, ou seja o tratamento do estado inicial e final estão concluídos. 
    # Parte 02 - Teste entre as ações e os estados. Fazer o mesmo processo para cada linha.

if __name__ == '__main__':
    main(sys.argv[1])



# Criar a árvore de estados ao ler as ações, fazendo as comparações e mudanças
# Adicionar cada novo estado a uma fila e realizar os teste de compatibilidade

