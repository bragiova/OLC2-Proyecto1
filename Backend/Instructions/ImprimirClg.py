
from Abstract.Instruccion import Instruccion

class ImprimirClg(Instruccion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        super().__init__(linea, columna)

    def ejecutar(self, env):
        expre = self.expresion.ejecutar(env)
        print(expre.valor)
        return expre.valor