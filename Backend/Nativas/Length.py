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

        # Esta verificación solo cuando se pide el length de un arreglo que está dentro de otro arreglo
        if isinstance(valLength, list):
            resultado.valor = len(valLength)
            return resultado

        if valLength is not None and (valLength.tipo == Tipo.STRING or valLength.tipo == Tipo.ARREGLO):
            resultado.valor = len(valLength.valor)
        else:
            return Error('Semántico', 'El tipo no es aplicable a la función length', self.linea, self.columna)
        
        return resultado