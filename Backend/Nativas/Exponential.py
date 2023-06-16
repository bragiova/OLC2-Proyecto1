from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class ToExponential(Instruccion):
    def __init__(self, expresion, cantDecimal, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion
        self.cantDecimal = cantDecimal

    def ejecutar(self, env):
        valToExponencial = self.expresion.ejecutar(env)
        if isinstance(valToExponencial, Error): return valToExponencial

        resultado = Retorno(Tipo.STRING, '')

        if valToExponencial is not None:
            decimales = self.cantDecimal.ejecutar(env)
            if isinstance(decimales, Error): return decimales

            if decimales is not None:
                if (valToExponencial.tipo == Tipo.NUMBER or valToExponencial.tipo == Tipo.ANY) and (decimales.tipo == Tipo.NUMBER or decimales.tipo == Tipo.ANY):
                    strExponencial = ('%.' + str(decimales.valor) + 'e') % float(valToExponencial.valor)
                    resultado.valor = str(strExponencial)
                else:
                    return Error('Semántico', 'Tipo de dato no es Number para toExponential', self.linea, self.columna)
        
        return resultado