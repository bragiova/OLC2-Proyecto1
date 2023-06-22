from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *

class Break(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def compilar(self, env):
        return Retorno(Tipo.BREAKST, None)