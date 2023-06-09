
from Abstract.Expresion import Expresion
from Abstract.Retorno import Retorno
from Sym.Error import Error

class Identificador(Expresion):
    def __init__(self, ident, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident

    def ejecutar(self, env):
        variable = env.getSimbolo(self.ident)

        if variable is None:
            return Error('Semántico', 'Variable no encontrada', self.linea, self.columna)
        
        return Retorno(variable.tipo, variable.valor)
