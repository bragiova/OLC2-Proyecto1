from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class Return(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion
        self.tipo = None
        self.valor = None
        self.trueLbl = ''
        self.falseLbl = ''

    def compilar(self, env):
        valReturn = self.expresion.compilar(env)
        if isinstance(valReturn, Error): return valReturn

        self.tipo = valReturn.tipo
        self.valor = valReturn.valor

        if self.tipo == Tipo.BOOL:
            self.trueLbl = valReturn.getTrueLbl()
            self.falseLbl = valReturn.getFalseLbl()
        
        return self

    def setValor(self, valor):
        self.valor = valor

    def getValor(self):
        return self.valor
    
    def setTipo(self, tipo):
        self.tipo  = tipo

    def getTipo(self):
        return self.tipo
    
    def setTrueLbl(self, lbl):
        self.trueLbl = lbl

    def getTrueLbl(self):
        return self.trueLbl
    
    def setFalseLbl(self, lbl):
        self.falseLbl = lbl

    def getFalseLbl(self):
        return self.falseLbl