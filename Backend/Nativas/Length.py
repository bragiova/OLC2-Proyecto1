from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class Length(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion

    def ejecutar(self, env):
        valLength = self.expresion.ejecutar(env)
        if isinstance(valLength, Error): return Error

        resultado = Retorno(Tipo.NUMBER, 0)

        if valLength is not None and valLength.tipo == Tipo.STRING:
            resultado.valor = len(valLength.valor)
        else:
            return Error('Semántico', 'El tipo no es aplicable a la función length', self.linea, self.columna)
        
        return resultado