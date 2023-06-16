from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class ToString(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion

    def ejecutar(self, env):
        valString = self.expresion.ejecutar(env)
        if isinstance(valString, Error): return valString

        resultado = Retorno(Tipo.STRING, '')

        if valString is not None:
            resultado.valor = str(valString.valor)
        
        return resultado
