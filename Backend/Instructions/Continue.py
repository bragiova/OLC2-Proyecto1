from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *

class Continue(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def ejecutar(self, env):
        return Retorno(Tipo.CONTIST, None)