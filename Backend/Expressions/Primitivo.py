from Abstract.Expresion import Expresion
from Abstract.Retorno import *

class Primitivo(Expresion):
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        super().__init__(linea, columna)

    def ejecutar(self, env):
        return Retorno(self.tipo, self.valor)
