
class Simbolo:
    def __init__(self, ident, tipo, varGlobal, posicion, enHeap, linea, columna):
        self.ident = ident
        self.tipo = tipo
        # self.valor = valor
        self.linea = linea
        self.columna = columna
        self.posicion = posicion
        self.enHeap = enHeap
        self.length = 0
        self.referencia = False
        self.params = None
        self.esGlobal = varGlobal
        self.tipoAux = ''
    
    def setId(self, id):
        self.ident = id

    def getId(self):
        return self.ident

    def setTipo(self, tipo):
        self.tipo = tipo

    def getTipo(self):
        return self.tipo

    # def setValor(self, valor):
    #     self.valor = valor

    # def getValor(self):
    #     return self.valor

    def setLinea(self, linea):
        self.linea = linea

    def getLinea(self):
        return self.linea

    def setColumna(self, col):
        self.columna = col

    def getColumna(self):
        return self.columna

    def setPosicion(self, pos):
        self.posicion = pos
    
    def getPosicion(self):
        return self.posicion
    
    def setEnHeap(self, valor):
        self.enHeap = valor
    
    def getEnHeap(self):
        return self.enHeap
    
    def setLength(self, length):
        self.length = length
    
    def getLength(self):
        return self.length
    
    def setReferencia(self, refe):
        self.referencia = refe
    
    def getReferencia(self):
        return self.referencia
    
    def setParams(self, params):
        self.params = params
    
    def getParams(self):
        return self.params
    
    def setTipoAux(self, tipoAux):
        self.tipoAux = tipoAux
    
    def getTipoAux(self):
        return self.tipoAux
