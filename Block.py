# -*- coding: utf-8 -*-
import sys
import copy
import time

class Fila:
    #Fila, Very normal
    def __init__(self):
        self.data = []

    def deq(self):
        a = copy.deepcopy(self.data[0])
        self.data = self.data[1:]
        return a
    def add(self, i):
        self.data.append(i)
    def empty(self):
        return len(self.data) == 0
    def front(self):
        return self.data[0]
    def __str__(self):
        return str(self.data)

class Action:
    def __init__(self, data):
        #contem:
        # a ação (uma lista contendo um elemento),
        # as precondições (uma lista com as condições)
        # as pos condições (uma lista com as condições)
        self.act = data[0]
        self.pre = data[1]
        self.pos = data[2]
    def __str__(self):
        #just a very normal printing string
        return "Action: " + str(self.act)+"\nPre: " + str(self.pre) + "\nPos: " + str(self.pos)
    def pre(self):
        return self.pre
    def pos(self):
        return self.pos
    def act(self):
        return self.act

class Arvore:
    def __init__(self):
        #Arvore bem normal, n-ária
        #cada nó pode ter qualquer quantidade de filhos
        #a raiz sempre é 1
        #se a raiz tiver três nós filhos, eles serão obrigatóriamente: 2, 3, 4
        #a lista para a qual a raiz aponta é: [2, 3, 4]
        #porém, se o nó 2 tiver filhos: 5, 6, 7 ...
        #a lista para a qual o nó 2 apota será: [x, 1, 5, 6, 7 ...]
        #sendo x a ação que levou de 1 até 2, e o segundo elemento será sempre o pai
        #assim é possível fazer o caminho de retorno de um nó filho
        #até a raiz, recuperando o conjunto de ações que levou
        #da raiz até esse filho
        self.root = 1
        self.struct = {1:[]}
    def add(self, pai, filho, action):
        self.struct[pai].append(filho)
        self.struct[filho] = [action, pai]
    def returnpath(self,node):
        path = []
        i = node
        j = 0
        while i != 1:
            j = self.struct[i][0]
            i = self.struct[i][1]
            path.append(j)
        path.reverse()
        return path

def normaliza_linha(linha):
    #remove /n do final e separa cada coisa
    # pelos ;
    # retorna uma lista contendo cada coisa
    l = linha[0:-1]
    l = l.split(';')
    return l    

def sublist(a, b):
    #se a lista b está inteiramente contida em a
    #retorna true
    for i in b:
        if not i in a:
            return False
    return True

def intersect_count(a, b):
    #conta quantos elementos de b estão em a
    c = 0
    for i in b:
        if i in a:
            c += 1
    return c

def neg(a, b):
    #retorna true se A for a negação de B
    if '~'+a == b:
        return True

def main(arg):
    #CPU
    time_init = time.time()
    #lendo o arquivo passado como parametro na chamada do programa
    f = open(arg,"r")
    linhas = f.readlines()
    #pegando listas de condições iniciais e finais:
    init_state = normaliza_linha(linhas[-2])
    final_state = normaliza_linha(linhas[-1])
    #action list:
    action_list = []
    #pegando todas as ações em forma da class Action
    i = 0
    while linhas[i] != '\n':
        action_list.append(Action([normaliza_linha(linhas[i]), normaliza_linha(linhas[i+1]), normaliza_linha(linhas[i+2])]))
        i += 3
    
    #fila para guardar os estados
    fila = Fila()
    #fila para guardar os indices dos estados
    fila_de_ids = Fila()
    #as duas filas sempre correspondem uma a outra, SEMPRE, SEMPRE!!
    #se o 3 sair da fila_de_ids, o estado 3 tem que sair da fila dos estados

    
    arvore = Arvore()
    fila.add(init_state)
    fila_de_ids.add(1)
    last_state_id = 1 # ultimo estado olhado, na Fila de estados 
    #al_len: action_list length, pegando o tamnho da lista
    #para que não tenhamos que ler a lista toda vida
    #que precisarmos só do tamanho dela. já que ela é estática
    al_len = len(action_list)
    #enquanto o estado atual (primeiro da fila)
    #não conter o estado final como subconjunto
    #ou seja, enquanto não satisfazemos o estado final
    while not sublist(fila.front(),final_state):
        #coletar todas as ações possíveis a partir do estado atual fila.front()
        possible_actions = []
        i = 0
        while i < al_len:
            #se as pré-condições da ação atual estão
            #todas satisfeitas pelo estado atual em fila.front()
            #então essa é uma açao possível
            if sublist(fila.front(), action_list[i].pre):
                possible_actions.append(i)
            i += 1
        #para cada ação:
        for j in possible_actions:
            #criamos um novo estado identico ao estado atual
            #lembrando que o estado atual é o fila.front()
            new_state = copy.deepcopy(fila.front())
            #agora vamos modificar o new_state
            #para satisfazer as pós-condições da ação J
            k = 0
            while k < len(action_list[j].pos):
                m = 0 
                while m < len(new_state):
                    #se a pós condição K for a negação de uma 
                    #condição M do estado atual
                    if neg(action_list[j].pos[k], new_state[m]) or neg(new_state[m], action_list[j].pos[k]):
                        #então a condição M é trocada pela condição K
                        new_state[m] = action_list[j].pos[k]
                        break
                    m += 1
                #se não, então a condição K é adicionada ao novo estado:
                if m == len(new_state) and not action_list[j].pos[k] in new_state:
                    new_state.append(action_list[j].pos[k])
                k += 1
            #adicionamos o novo estado na FILA
            fila.add(copy.deepcopy(new_state))
            last_state_id += 1
            #adicionamos no nó do antigo estado o novo nó, com a ação J
            arvore.add(fila_de_ids.front(), last_state_id, j)
            #mantendo a fila_de_ids correspondendo a fila de estados
            fila_de_ids.add(last_state_id)
        #obviamente, devemos remover os FRONTs das filas
        #para começar uma nova etapa de nossas vidas
        fila.deq()
        fila_de_ids.deq()

    #a solução é obtida através do maravilhoso método Arvore.returnpath
    solution = arvore.returnpath(fila_de_ids.front())
    for i in solution:
        print action_list[i].act
    print "Tempo de Execução: "+ str(time.time() - time_init)

if __name__ == '__main__':
    main(sys.argv[1])   