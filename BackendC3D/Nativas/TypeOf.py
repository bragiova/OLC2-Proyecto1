from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error

class TypeOf(Instruccion):
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna)
        self.expresion = expresion

    def ejecutar(self, env):
        valType = self.expresion.ejecutar(env)
        if isinstance(valType, Error): return valType

        resultado = Retorno(Tipo.ANY, '')

        if valType is not None:
            if valType.tipo == Tipo.NUMBER:
                resultado.tipo = Tipo.NUMBER
                resultado.valor = 'number'
            elif valType.tipo == Tipo.STRING:
                resultado.tipo = Tipo.STRING
                resultado.valor = 'string'
            elif valType.tipo == Tipo.ANY:
                resultado.tipo = Tipo.ANY
                resultado.valor = 'any'
            elif valType.tipo == Tipo.BOOL:
                resultado.tipo = Tipo.BOOL
                resultado.valor = 'boolean'
            elif valType.tipo == Tipo.NULL:
                resultado.tipo = Tipo.NULL
                resultado.valor = 'null'
        else:
            return Error('Semántico', 'No es posible utilizar la función typeof', self.linea, self.columna)
    
        return resultado