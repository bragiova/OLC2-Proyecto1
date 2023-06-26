
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []
        self.contador = 0
        self.grafo = ''

    def insertHijo(self, hijo):
        self.hijos.append(hijo)

    def getGrafoAST(self):
        # self.grafo = 'digraph AST{\n'
        self.grafo += 'nodo0[label=\"' + str(self.valor) + '\"];\n'
        self.contador = 1
        self.grafoAST('nodo0', self)
        # self.grafo += '}'
        return self.grafo
    
    def grafoAST(self, padre, listHijos):
        for hijo in listHijos.hijos:
            hijoN = 'nodo' + str(self.contador)
            self.grafo += hijoN + '[label=\"' + str(hijo.valor) + '\"];\n'
            self.grafo += padre + '->' + hijoN + ';\n'
            self.contador += 1
            # print(self.grafo)
            self.grafoAST(hijoN, hijo)