
class Simbolo:
    def __init__(self, ident, tipo, valor, linea, columna, tipoArray = None):
        self.ident = ident
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipoArray = tipoArray
    
    def setId(self, id):
        self.ident = id

    def getId(self):
        return self.ident

    def setTipo(self, tipo):
        self.tipo = tipo

    def getTipo(self):
        return self.tipo

    def setValor(self, valor):
        self.valor = valor

    def getValor(self):
        return self.valor

    def setLinea(self, linea):
        self.linea = linea

    def getLinea(self):
        return self.linea

    def setColumna(self, col):
        self.columna = col

    def getColumna(self):
        return self.columna

    def setTipoArray(self, tipo):
        self.tipoArray = tipo

    def getTipoArray(self):
        return self.tipoArray 

