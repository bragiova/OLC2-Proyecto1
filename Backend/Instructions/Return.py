from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class Return(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion

    def ejecutar(self, env):
        result = Retorno(Tipo.RETURNST, None)

        if self.expresion is not None:
            valExp = self.expresion.ejecutar(env)
            if isinstance(valExp, Error): return valExp

            result.valor = valExp.valor
        
        return result