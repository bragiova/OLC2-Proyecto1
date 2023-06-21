from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class ToFixed(Instruccion):
    def __init__(self, expresion, cantDecimal, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion
        self.cantDecimal = cantDecimal

    def ejecutar(self, env):
        valToFixed = self.expresion.ejecutar(env)
        if isinstance(valToFixed, Error): return valToFixed

        resultado = Retorno(Tipo.STRING, '')

        if valToFixed is not None:
            decimales = self.cantDecimal.ejecutar(env)
            if isinstance(decimales, Error): return decimales

            if decimales is not None:
                if (valToFixed.tipo == Tipo.NUMBER or valToFixed.tipo == Tipo.ANY) and (decimales.tipo == Tipo.NUMBER or decimales.tipo == Tipo.ANY):
                    strFixed = ('%.' + str(decimales.valor) + 'f') % float(valToFixed.valor)
                    resultado.valor = str(strFixed)
                else:
                    return Error('Semántico', 'Tipo de dato no es Number para toFixed', self.linea, self.columna)
        
        return resultado