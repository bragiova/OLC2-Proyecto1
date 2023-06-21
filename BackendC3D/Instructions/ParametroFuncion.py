from Abstract.Instruccion import Instruccion

class ParametroFuncion(Instruccion):
    def __init__(self, ident, tipo, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.tipo = tipo

    def compilar(self, env):
        return self
