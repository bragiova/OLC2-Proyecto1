from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class UpperCase(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion

    def ejecutar(self, env):
        expreUp = self.expresion.ejecutar(env)
        if isinstance(expreUp, Error): return expreUp

        resultado = Retorno(Tipo.STRING, '')

        if expreUp is not None:
            if expreUp.tipo == Tipo.STRING or expreUp.tipo == Tipo.ANY:
                resultado.valor = str(expreUp.valor).upper()
            else:
                return Error('Semántico', 'toUpperCase aplica solamente para expresiones de tipo String', self.linea, self.columna)
        
        return resultado
        

