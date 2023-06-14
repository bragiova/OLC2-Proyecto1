from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *

class Return(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion

    def ejecutar(self, env):
        result = Retorno(Tipo.RETURNST, None)

        if self.expresion is not None:
            valExp = self.expresion.ejecutar(env)
            result.valor = valExp.valor
        
        return result