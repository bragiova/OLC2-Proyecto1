from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class LowerCase(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion

    def ejecutar(self, env):
        expreLow = self.expresion.ejecutar(env)
        if isinstance(expreLow, Error): return expreLow

        resultado = Retorno(Tipo.STRING, '')

        if expreLow is not None:
            if expreLow.tipo == Tipo.STRING or expreLow.tipo == Tipo.ANY:
                resultado.valor = str(expreLow.valor).lower()
            else:
                return Error('Semántico', 'toLowerCase aplica solamente para expresiones de tipo String', self.linea, self.columna)
        
        return resultado